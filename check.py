"""Mechanical manuscript review — recommends, never edits.

    python check.py                  # full review -> tool_output/report-*.md
    python check.py --changed-only   # only findings in files changed since last run

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
    lines = log.read_text().strip().splitlines()
    return json.loads(lines[-1])["sha"] if lines else None


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
            cites.add(m.group(1) or m.group(2))

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

    lines = [
        f"# Manuscript check — {ts}",
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
        f.write(json.dumps({"ts": ts, "sha": sha, "dirty": dirty, **counts}) + "\n")

    print("\n".join(lines))
    print(f"\nreport: {report.relative_to(ROOT)}")
    sys.exit(1 if counts["BREAK"] else 0)


if __name__ == "__main__":
    main()
