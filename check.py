"""Mechanical manuscript review — recommends, never edits.

    python check.py path/to/project        # full review -> <project>/tool_output/report-*.md
    python check.py                        # the project in the current folder
    python check.py PROJECT --changed-only # only findings in files changed since last run
    python check.py PROJECT --links        # also verify external URLs (network, slower)

The loop this enables:
    edit -> git commit -> python check.py PROJECT -> read report -> repeat

Works on any Quarto project (book, article, datasheet, report): the project is the
path you pass, else the current folder. Book projects also get chapter-list
and per-chapter checks. A `codespell-ignore.txt` in the project allowlists
words the spell check should accept.

Git is the memory: each run logs the HEAD it reviewed (tool_output/log.jsonl),
so --changed-only diffs against the previous run and the report tells you
what moved. Deterministic checks only — prose judgment belongs to a human
or a Claude session reading this report next to `git diff`.

Exit code: 1 if any BREAK-severity finding (CI-able), else 0.
"""

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SKIP_DIRS = {"_book", "_output", ".quarto", "_extensions", "tool_output",
             "incoming", "feedback", "site_libs"}

# same drop-silent class build.py guards (kept in sync manually); LaTeX PDFs only
DROP_RE = re.compile("[⁰-₟←↔⇐-⇿]")
REF_RE = re.compile(r"@(sec|fig|tbl|eq)-[\w-]+")
ANCHOR_RE = re.compile(r"\{#((?:sec|fig|tbl|eq)-[\w-]+)")
CITE_RE = re.compile(r"\[@([\w:-]+)[\],; ]|[^\w\[]@([\w:-]+)")
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)(\{[^}]*\})?")
TODO_RE = re.compile(r"\b(TODO|FIXME|XXX|TK)\b")


def project_dir(arg=None):
    """The path given, else the current folder; either must hold _quarto.yml."""
    p = Path(arg or ".").expanduser().resolve()
    if not (p / "_quarto.yml").exists():
        sys.exit(f"{p} has no _quarto.yml, so it isn't a Quarto project. "
                 "Pass the project folder: python check.py path/to/project")
    return p


def git(cwd, *args):
    try:
        return subprocess.run(["git", *args], cwd=cwd, capture_output=True,
                              encoding="utf-8", errors="replace", check=True).stdout.strip()
    except Exception:
        return ""


def last_run_sha(out):
    log = out / "log.jsonl"
    if not log.exists():
        return None
    for line in reversed(log.read_text(encoding="utf-8").strip().splitlines()):
        e = json.loads(line)
        if e.get("type", "check") == "check":
            return e["sha"]
    return None


def scrub(text):
    """Blank YAML front matter and code (fenced + inline), keeping line numbers,
    so examples inside code don't read as refs, images, or headings."""
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() in ("---", "..."):
                lines[: i + 1] = [""] * (i + 1)
                break
    fence = None
    for i, line in enumerate(lines):
        m = re.match(r"\s*(`{3,}|~{3,})", line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
            lines[i] = ""
        elif m:
            fence = m.group(1)
            lines[i] = ""
    return "\n".join(re.sub(r"`[^`\n]*`", lambda m: " " * len(m.group()), l) for l in lines)


def front_matter(text):
    m = re.match(r"---\n(.*?)\n(---|\.\.\.)\s*\n", text, re.S)
    return m.group(1) if m else ""


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows pipes default to cp1252
    ap = argparse.ArgumentParser()
    ap.add_argument("project", nargs="?",
                    help="Quarto project folder (default: the current folder)")
    ap.add_argument("--changed-only", action="store_true")
    ap.add_argument("--links", action="store_true")
    args = ap.parse_args()
    changed_only = args.changed_only

    proj = project_dir(args.project)
    out_dir = proj / "tool_output"
    out_dir.mkdir(exist_ok=True)
    top = Path(git(proj, "rev-parse", "--show-toplevel") or proj)
    yml = (proj / "_quarto.yml").read_text(encoding="utf-8")
    is_book = bool(re.search(r"^\s*type:\s*book\b", yml, re.M))
    latex = bool(re.search(r"^\s*(format:\s*)?pdf\s*:|^\s*format:\s*pdf\s*$", yml, re.M))

    sha = git(proj, "rev-parse", "--short", "HEAD") or "no-git"
    dirty = bool(git(proj, "status", "--porcelain", "."))
    prev = last_run_sha(out_dir)
    changed = set()
    if prev and prev != "no-git":
        changed = set(git(proj, "diff", "--name-only", f"{prev}..HEAD").splitlines())
        changed |= {l[3:] for l in git(proj, "status", "--porcelain").splitlines() if len(l) > 3}

    qmds = sorted(q for q in proj.rglob("*.qmd")
                  if not SKIP_DIRS & set(q.relative_to(proj).parts))
    texts = {q: q.read_text(encoding="utf-8") for q in qmds}
    clean = {q: scrub(t) for q, t in texts.items()}
    findings = []  # (severity, file, msg)

    def rel(f):
        f = Path(f)
        for base in (top, proj):
            try:
                return str(f.resolve().relative_to(base))
            except ValueError:
                pass
        return str(f)

    def add(sev, f, msg):
        r = rel(f) if isinstance(f, Path) else f
        if changed_only and changed and r not in changed:
            return
        findings.append((sev, r, msg))

    # -- collect anchors / refs / cites / images across the manuscript
    anchors, refs, cites = {}, [], set()
    for q in qmds:
        text = clean[q]
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
        if is_book:
            if not h1s:
                add("BREAK", q, "no chapter title (# heading)")
            if len(h1s) > 1:
                add("WARN", q, f"{len(h1s)} top-level headings — split the file?")
            words = len(re.sub(r"[#*|`\-]", " ", text).split())
            if words < 100:
                add("INFO", q, f"stub: only {words} words")
        elif not re.search(r"^title:", front_matter(texts[q]), re.M) and not h1s:
            add("WARN", q, "no title (front matter `title:` or a # heading)")
        for i, l in enumerate(lines, 1):
            if latex:
                prose = re.sub(r"\$[^$]*\$", "", l)
                for m in DROP_RE.finditer(prose):
                    add("BREAK", q, f"line {i}: U+{ord(m.group()):04X} {m.group()!r} drops in PDF — use inline math")
            if TODO_RE.search(l):
                add("WARN", q, f"line {i}: unresolved marker: {l.strip()[:60]}")
        for m in IMG_RE.finditer(text):
            path, attrs = m.group(1), m.group(2) or ""
            if re.match(r"https?://", path):
                continue
            img = (proj / path.lstrip("/")) if path.startswith("/") else (q.parent / path)
            if not img.resolve().exists():
                add("BREAK", q, f"image missing on disk: {path}")
            if "alt=" not in attrs:
                add("WARN", q, f"image without fig-alt (accessibility): {path}")

    # -- repeated words + long sentences (per file, prose only)
    for q in qmds:
        text_np = "\n".join(l for l in clean[q].splitlines() if not l.lstrip().startswith("|"))
        prose = re.sub(r"\$[^$]*\$|<!--.*?-->", " ", text_np, flags=re.S)
        for i, line in enumerate(prose.splitlines(), 1):
            for m in re.finditer(r"\b([A-Za-z]+)\s+\1\b", line, re.I):
                add("WARN", q, f"line {i}: repeated word: '{m.group(0)}'")
        sentences = [s.split() for s in re.split(r"[.!?]", re.sub(r"[#*|>\-]", " ", prose))]
        long_s = [len(s) for s in sentences if len(s) > 40]
        if long_s:
            add("INFO", q, f"{len(long_s)} sentence(s) over 40 words (longest {max(long_s)})")

    # -- bibliography: _quarto.yml or any front matter
    bib_names = re.findall(r"^\s*bibliography:\s*(\S+)", yml, re.M)
    for q in qmds:
        bib_names += re.findall(r"^bibliography:\s*(\S+)", front_matter(texts[q]), re.M)
    bibs = [proj / b.strip("\"'") for b in bib_names] or [proj / "references.bib"]

    # -- codespell (real-word typos; allowlist in codespell-ignore.txt)
    sibling = Path(sys.executable).parent / "codespell"
    codespell = shutil.which("codespell") or (str(sibling) if sibling.exists() else None)
    if codespell and qmds:
        ignore = proj / "codespell-ignore.txt"
        cmd = [codespell, "--quiet-level", "2", *map(str, qmds),
               *(str(b) for b in bibs if b.exists())]
        if ignore.exists():
            cmd[1:1] = ["-I", str(ignore)]
        cs_out = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace",
                                env={**os.environ, "PYTHONIOENCODING": "utf-8"}).stdout
        for line in cs_out.strip().splitlines():
            # format: path:line: word ==> correction
            parts = line.split(":", 2)
            if len(parts) == 3:
                add("WARN", Path(parts[0]), f"line {parts[1]}: spelling: {parts[2].strip()}")
    elif not codespell:
        add("INFO", "check.py", "codespell not installed — `pip install codespell` enables spell checks")

    # -- external links (opt-in: --links)
    if args.links:
        import urllib.request
        urls = set()
        for q in qmds:
            urls |= set(re.findall(r"https?://[^\s)\]}>\"']+", texts[q]))
        for bib in bibs:
            if bib.exists():
                bib_text = bib.read_text(encoding="utf-8")
                urls |= set(re.findall(r"https?://[^\s)\]}>\"']+", bib_text))
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
    existing = [b for b in bibs if b.exists()]
    for b in bibs:
        if b not in existing and bib_names:
            add("BREAK", proj / "_quarto.yml", f"bibliography file missing: {rel(b)}")
    if existing:
        keys = set()
        for b in existing:
            keys |= set(re.findall(r"^@\w+\{([^,]+),", b.read_text(encoding="utf-8"), re.M))
        for c in sorted(cites - keys):
            add("BREAK", existing[0], f"cited key not in bib: @{c}")
        for k in sorted(keys - cites):
            add("INFO", existing[0], f"bib entry never cited: {k}")
    elif cites:
        add("WARN", proj / "_quarto.yml", f"{len(cites)} citation(s) but no references.bib")

    # -- files named in _quarto.yml vs disk (chapters; project render lists)
    listed = set(re.findall(r"^\s*-\s+[\"']?([\w./-]+\.qmd)\b", yml, re.M))
    on_disk = {q.relative_to(proj).as_posix() for q in qmds}
    for miss in sorted(listed - on_disk):
        add("BREAK", proj / "_quarto.yml", f"listed file missing on disk: {miss}")
    if is_book:
        for orphan in sorted(on_disk - listed):
            add("WARN", proj / "_quarto.yml", f"chapter on disk but not in book: {orphan}")

    # -- report
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    order = {"BREAK": 0, "WARN": 1, "INFO": 2}
    findings.sort(key=lambda x: (order[x[0]], x[1]))
    counts = {s: sum(1 for f in findings if f[0] == s) for s in order}

    total_words = sum(len(t.split()) for t in texts.values())
    lines = [
        f"# Manuscript check — {ts}",
        f"- project: `{rel(proj)}` ({'book' if is_book else 'document'})",
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

    report = out_dir / f"report-{ts}-{sha}.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with (out_dir / "log.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({"type": "check", "ts": ts, "sha": sha, "dirty": dirty, "words": total_words, **counts}) + "\n")

    print("\n".join(lines))
    print(f"\nreport: {rel(report)}")
    sys.exit(1 if counts["BREAK"] else 0)


if __name__ == "__main__":
    main()
