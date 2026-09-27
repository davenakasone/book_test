"""Start a new document project from a template.

    python new.py --list
    python new.py book      ../my-book    --title "My Book"
    python new.py article   ../my-paper   --title "My Paper"
    python new.py datasheet ../xr-2000    --title "XR-2000"

Creates a self-contained folder: the template's placeholder content, this
toolkit's build/check/review tools, a README for that kind of document,
and a CLAUDE.md so a Claude Code session opened there knows the rules.
Nothing links back to this repo; the new folder builds on its own:

    cd ../my-paper && python build.py

Put the new folder OUTSIDE this repo (it gets its own git history).
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATES = ROOT / "templates"

KINDS = {
    "book": "print + ebook + web book: 6x9 PDF (LaTeX), EPUB3, HTML site",
    "article": "paper, report, or white paper: PDF (Typst), HTML, Word",
    "datasheet": "product datasheet: PDF (Typst), spec tables, curves plotted from CSV",
}

# file holding the title line that --title rewrites
MAIN = {"book": "_quarto.yml", "article": "article.qmd", "datasheet": "datasheet.qmd"}

# toolkit files copied into every new project: (source in this repo, dest)
TOOLS = [
    ("build.py", "build.py"),
    ("check.py", "check.py"),
    ("requirements.txt", "requirements.txt"),
    ("scripts/extract_feedback.py", "scripts/extract_feedback.py"),
    (".claude/commands/review.md", ".claude/commands/review.md"),
    (".claude/commands/feedback.md", ".claude/commands/feedback.md"),
]
EXTRA_TOOLS = {
    "book": [
        ("scripts/ingest.py", "scripts/ingest.py"),
        ("scripts/build_tikz.py", "scripts/build_tikz.py"),
        ("scripts/make_pdfx.py", "scripts/make_pdfx.py"),
        # the demo book's proven infrastructure, single-sourced from book/
        ("book/postrender-fix-epub.py", "postrender-fix-epub.py"),
        ("book/latex/preamble.tex", "latex/preamble.tex"),
        ("book/latex/after-body.tex", "latex/after-body.tex"),
    ],
}

GITIGNORE = """\
# render output (rebuild with `python build.py`)
_output/
_book/
.quarto/
*_files/
*.quarto_ipynb

# machine-owned review output; the author's raw source files
tool_output/
incoming/

.DS_Store
__pycache__/
"""

CLAUDE_MD = """\
# {title} ({kind})

A {kind} written in Markdown and built with Quarto. It was created from the
document toolkit at https://github.com/davenakasone/book_test and is
self-contained: everything below runs from this folder.

@README.md

## Rules for any Claude session working here

1. **The author authors; you scaffold.** Don't rewrite the author's text in
   place unless they ask. Anything you draft yourself carries
   `<!-- TODO: TOOL-DRAFTED, NOT AUTHOR-WRITTEN. <why> -->`, and
   `python check.py` flags it until the author replaces it.
2. **Placeholders stay flagged until they're replaced.** Remove a
   `TODO: TEMPLATE CONTENT` marker only when the content under it is real.
3. **Build and check before calling anything done:** `python build.py`, then
   `python check.py` (exit 1 means something will break the build).
4. **Review loop:** `/review` gives prose judgment, stored as `TODO(review)`
   markers plus `tool_output/review-*.md`. `/feedback feedback/<round>`
   triages what reviewers sent back.
"""


def copy(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def set_title(path, title):
    text = path.read_text()
    new, n = re.subn(r'^(\s*title:\s*)".*"', lambda m: f'{m.group(1)}"{title}"',
                     text, count=1, flags=re.M)
    if n:
        path.write_text(new)


def main():
    ap = argparse.ArgumentParser(description="Start a new document project.")
    ap.add_argument("kind", nargs="?", choices=sorted(KINDS))
    ap.add_argument("dest", nargs="?", help="folder to create (outside this repo)")
    ap.add_argument("--title", help="document title (default: the template's placeholder)")
    ap.add_argument("--list", action="store_true", help="list the kinds and exit")
    args = ap.parse_args()

    if args.list or not args.kind:
        print("kinds:")
        for k, what in KINDS.items():
            print(f"  {k:<10} {what}")
        print("\nusage: python new.py <kind> <folder> [--title ...]")
        return
    if not args.dest:
        ap.error("give a destination folder, e.g. ../my-" + args.kind)

    dest = Path(args.dest).expanduser().resolve()
    if dest.exists() and any(dest.iterdir()):
        sys.exit(f"{dest} exists and isn't empty; pick a new folder.")
    if dest == ROOT or ROOT in dest.parents:
        print(f"note: {dest} is inside the toolkit repo, so the toolkit's git "
              "will see it. A folder outside the repo is usually what you want.")

    shutil.copytree(TEMPLATES / args.kind, dest, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("_output", "_book", ".quarto", "__pycache__",
                                                  "tool_output", "*_files"))
    for src, rel in TOOLS + EXTRA_TOOLS.get(args.kind, []):
        copy(ROOT / src, dest / rel)
    (dest / ".gitignore").write_text(GITIGNORE)

    title = args.title or {"book": "Book Title", "article": "Title of the Paper",
                           "datasheet": "XR-1000"}[args.kind]
    if args.title:
        set_title(dest / MAIN[args.kind], args.title)
    (dest / "CLAUDE.md").write_text(CLAUDE_MD.format(title=title, kind=args.kind))

    # generate plotted figures now, so a bare `quarto render` works too
    figs = dest / "scripts" / "make_figures.py"
    if figs.exists():
        r = subprocess.run([sys.executable, str(figs)], cwd=dest)
        if r.returncode:
            print("note: figure generation failed (is matplotlib installed? "
                  "`python -m pip install -r requirements.txt`); "
                  "`python build.py` retries it.")

    print(f"\ncreated {args.kind}: {dest}\n\nnext:\n"
          f"  cd {dest}\n"
          "  python build.py --doctor   # what's installed, what's missing\n"
          "  python build.py            # render\n"
          "  git init                   # optional: its own history\n"
          "then read README.md in that folder.")


if __name__ == "__main__":
    main()
