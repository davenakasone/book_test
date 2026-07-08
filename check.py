"""Mechanical manuscript review — recommends, never edits.

    python check.py                  # full review -> tool_output/report-*.md
    python check.py --changed-only   # only findings in files changed since last run
    python check.py --links          # also verify external URLs (network, slower)

The loop this enables:
    edit -> git commit -> python check.py -> read report -> repeat

Git is the memory: each run logs the HEAD it reviewed (tool_output/log.jsonl),
so --changed-only diffs against the previous run and the report tells you
what moved. Deterministic checks only — prose judgment belongs to a human
or a Claude session reading this report next to `git diff`.

Exit code: 1 if any BREAK-severity finding (CI-able), else 0.
"""

import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BOOK = ROOT / "book"
OUT = ROOT / "tool_output"

# same drop-silent class build.py guards (kept in sync manually)
DROP_RE = re.compile("[⁰-₟←↔⇐-⇿]")
REF_RE = re.compile(r"@(sec|fig|tbl|eq)-[\w-]+")
ANCHOR_RE = re.compile(r"\{#((?:sec|fig|tbl|eq)-[\w-]+)")
CITE_RE = re.compile(r"\[@([\w:-]+)[\],; ]|[^\w\[]@([\w:-]+)")
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)(\{[^}]*\})?")
TODO_RE = re.compile(r"\b(TODO|FIXME|XXX|TK)\b")


def git(*args):
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return ""


def last_run_sha():
    log = OUT / "log.jsonl"
    if not log.exists():
        return None
    for line in reversed(log.read_text().strip().splitlines()):
        e = json.loads(line)
        if e.get("type", "check") == "check":
            return e["sha"]
    return None


def main():
    changed_only = "--changed-only" in sys.argv
    OUT.mkdir(exist_ok=True)

    sha = git("rev-parse", "--short", "HEAD") or "no-git"
    dirty = bool(git("status", "--porcelain"))
    prev = last_run_sha()
    changed = set()
    if prev and prev != "no-git":
        changed = set(git("diff", "--name-only", f"{prev}..HEAD").splitlines())
        changed |= {l[3:] for l in git("status", "--porcelain").splitlines() if len(l) > 3}

    qmds = sorted(BOOK.rglob("*.qmd"))
    findings = []  # (severity, file, msg)

    def add(sev, f, msg):
        rel = str(f.relative_to(ROOT)) if isinstance(f, Path) else f
        if changed_only and changed and rel not in changed:
            return
        findings.append((sev, rel, msg))

    # -- collect anchors / refs / cites / images across the book
    anchors, refs, cites = {}, [], set()
    for q in qmds:
        text = q.read_text()
        for m in ANCHOR_RE.finditer(text):
            if m.group(1) in anchors:
                add("BREAK", q, f"duplicate anchor #{m.group(1)} (also in {anchors[m.group(1)]})")
            anchors[m.group(1)] = q.name
        refs += [(q, m.group(0)[1:]) for m in REF_RE.finditer(text)]
        for m in CITE_RE.finditer(text):
            key = (m.group(1) or m.group(2)).rstrip(":.,;")
            # @sec-/@fig-/@tbl-/@eq- are cross-refs, not citations
            if not re.match(r"(sec|fig|tbl|eq)-", key):
                cites.add(key)

        # per-file checks
        lines = text.splitlines()
        h1s = [l for l in lines if l.startswith("# ")]
        if not h1s:
            add("BREAK", q, "no chapter title (# heading)")
        if len(h1s) > 1:
            add("WARN", q, f"{len(h1s)} top-level headings — split the file?")
        words = len(re.sub(r"[#*|`\-]", " ", text).split())
        if words < 100:
            add("INFO", q, f"stub: only {words} words")
        for i, l in enumerate(lines, 1):
            prose = re.sub(r"\$[^$]*\$", "", l)
            for m in DROP_RE.finditer(prose):
                add("BREAK", q, f"line {i}: U+{ord(m.group()):04X} {m.group()!r} drops in PDF — use inline math")
            if TODO_RE.search(l):
                add("WARN", q, f"line {i}: unresolved marker: {l.strip()[:60]}")
        for m in IMG_RE.finditer(text):
            path, attrs = m.group(1), m.group(2) or ""
            img = (q.parent / path).resolve()
            if not img.exists():
                add("BREAK", q, f"image missing on disk: {path}")
            if "alt=" not in attrs:
                add("WARN", q, f"image without fig-alt (EPUB accessibility): {path}")

    # -- repeated words + long sentences (per file, prose only)
    for q in qmds:
        text = q.read_text()
        text_np = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("|"))
        prose = re.sub(r"`[^`]*`|\$[^$]*\$|<!--.*?-->", " ", text_np, flags=re.S)
        for i, line in enumerate(prose.splitlines(), 1):
            for m in re.finditer(r"\b([A-Za-z]+)\s+\1\b", line, re.I):
                add("WARN", q, f"line {i}: repeated word: '{m.group(0)}'")
        sentences = [s.split() for s in re.split(r"[.!?]", re.sub(r"[#*|>\-]", " ", prose))]
        long_s = [len(s) for s in sentences if len(s) > 40]
        if long_s:
            add("INFO", q, f"{len(long_s)} sentence(s) over 40 words (longest {max(long_s)})")

    # -- codespell (real-word typos; allowlist in codespell-ignore.txt)
    import shutil as _sh
    if _sh.which("codespell"):
        ignore = ROOT / "codespell-ignore.txt"
        cmd = ["codespell", "--quiet-level", "2", str(BOOK)]
        if ignore.exists():
            cmd[1:1] = ["-I", str(ignore)]
        out = subprocess.run(cmd, capture_output=True, text=True).stdout
        for line in out.strip().splitlines():
            # format: path:line: word ==> correction
            parts = line.split(":", 2)
            if len(parts) == 3:
                add("WARN", parts[0], f"line {parts[1]}: spelling: {parts[2].strip()}")
    else:
        add("INFO", "check.py", "codespell not installed — `pip install codespell` enables spell checks")

    # -- external links (opt-in: --links)
    if "--links" in sys.argv:
        import urllib.request
        urls = set()
        for q in qmds:
            urls |= set(re.findall(r"https?://[^\s)\]}>\"']+", q.read_text()))
        bib = BOOK / "references.bib"
        if bib.exists():
            urls |= set(re.findall(r"https?://[^\s)\]}>\"']+", bib.read_text()))
        for u in sorted(urls):
            try:
                req = urllib.request.Request(u, method="HEAD",
                                             headers={"User-Agent": "book-check/1.0"})
                urllib.request.urlopen(req, timeout=6)
            except Exception as e:
                add("WARN", "links", f"{u} — {getattr(e, 'code', e)}")

    # -- dangling refs
    for q, r in refs:
        if r not in anchors:
            add("BREAK", q, f"dangling cross-reference @{r}")

    # -- citations vs bib
    bib = BOOK / "references.bib"
    if bib.exists():
        keys = set(re.findall(r"^@\w+\{([^,]+),", bib.read_text(), re.M))
        for c in sorted(cites - keys):
            add("BREAK", bib, f"cited key not in bib: @{c}")
        for k in sorted(keys - cites):
            add("INFO", bib, f"bib entry never cited: {k}")
    elif cites:
        add("WARN", BOOK / "_quarto.yml", f"{len(cites)} citation(s) but no references.bib")

    # -- _quarto.yml chapter list vs disk
    yml = (BOOK / "_quarto.yml").read_text()
    listed = set(re.findall(r"-\s+(chapters/[\w./-]+\.qmd)", yml))
    on_disk = {f"chapters/{q.name}" for q in (BOOK / "chapters").glob("*.qmd")}
    for miss in sorted(listed - on_disk):
        add("BREAK", BOOK / "_quarto.yml", f"listed chapter missing on disk: {miss}")
    for orphan in sorted(on_disk - listed):
        add("WARN", BOOK / "_quarto.yml", f"chapter on disk but not in book: {orphan}")

    # -- report
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    order = {"BREAK": 0, "WARN": 1, "INFO": 2}
    findings.sort(key=lambda x: (order[x[0]], x[1]))
    counts = {s: sum(1 for f in findings if f[0] == s) for s in order}

    total_words = sum(len(q.read_text().split()) for q in qmds)
    lines = [
        f"# Manuscript check — {ts}",
        f"- manuscript: {len(qmds)} file(s), ~{total_words:,} words",
        f"- git: `{sha}`{' (uncommitted changes)' if dirty else ''}",
        f"- since last check (`{prev or '—'}`): {len(changed) or 'all'} file(s) considered"
        + (" [--changed-only]" if changed_only else ""),
        f"- findings: {counts['BREAK']} break / {counts['WARN']} warn / {counts['INFO']} info",
        "",
    ]
    cur = None
    for sev, f, msg in findings:
        if sev != cur:
            lines.append(f"\n## {sev}\n")
            cur = sev
        lines.append(f"- `{f}` — {msg}")
    if not findings:
        lines.append("clean. render it: `python build.py`")

    report = OUT / f"report-{ts}-{sha}.md"
    report.write_text("\n".join(lines) + "\n")
    with (OUT / "log.jsonl").open("a") as f:
        f.write(json.dumps({"type": "check", "ts": ts, "sha": sha, "dirty": dirty, "words": total_words, **counts}) + "\n")

    print("\n".join(lines))
    print(f"\nreport: {report.relative_to(ROOT)}")
    sys.exit(1 if counts["BREAK"] else 0)


if __name__ == "__main__":
    main()
