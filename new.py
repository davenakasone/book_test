"""Start a new document project from a template.

    python new.py --list
    python new.py book      ../my-book    --title "My Book" --from ../raw
    python new.py article   ../my-paper   --title "My Paper"
    python new.py datasheet ../xr-2000    --title "XR-2000"

The new folder holds only the document: the template's placeholder content,
a README for that kind of document, and a CLAUDE.md so a Claude Code
session opened there knows the rules. The tools stay here and take the
folder as an argument:

    python build.py ../my-book --out ../deliverables
    python check.py ../my-book

--from (books): the author's raw files (.docx, .odt, .rtf, .md, .txt) become
the chapters, replacing the placeholders. The raw folder is only read.

Put the new folder OUTSIDE this repo (it gets its own git history).
"""

import argparse
import html
import os
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

# placeholder chapters in the book template, replaced by --from
PLACEHOLDER_CHAPTERS = ["chapters/01-first-chapter.qmd", "chapters/02-second-chapter.qmd"]

GITIGNORE = """\
# render output (rebuild with `python build.py`)
_output/
_book/
.quarto/
*_files/
*.quarto_ipynb

# machine-owned review output
tool_output/

.DS_Store
__pycache__/
"""

CLAUDE_MD = """\
# {title} ({kind})

A {kind} written in Markdown and built with Quarto by the document toolkit
at `{toolkit}` (https://github.com/davenakasone/book_test). This folder holds
only the document: text, figures, data, and settings. The tools stay in the
toolkit and take this folder as an argument, from here:

    python {toolkit}/build.py .              # render into _book/ or _output/
    python {toolkit}/build.py . --out DIR    # + copy the finished documents to DIR
    python {toolkit}/check.py .              # mechanical review -> tool_output/

@README.md

## Rules for any Claude session working here

1. **The author authors; you scaffold.** Don't rewrite the author's text in
   place unless they ask. Anything you draft yourself carries
   `<!-- TODO: TOOL-DRAFTED, NOT AUTHOR-WRITTEN. <why> -->`, and
   `check.py` flags it until the author replaces it.
2. **Placeholders stay flagged until they're replaced.** Remove a
   `TODO: TEMPLATE CONTENT` marker only when the content under it is real.
3. **Build and check before calling anything done** (commands above;
   `check.py` exit 1 means something will break the build).
4. **Review loop:** from a session in the toolkit folder, `/review <this
   folder>` gives prose judgment, stored as `TODO(review)` markers plus
   `tool_output/review-*.md`; `/feedback <this folder>/feedback/<round>`
   triages what reviewers sent back.
5. **Git is the memory.** `/review` and `check.py --changed-only` diff
   against the last reviewed commit, so commit the author's changes before
   each review round (`git init` first if this folder has no repo yet).
"""


def cmd_path(p):
    """p as typed from the current folder: relative when that's shorter, quoted if spaced."""
    try:
        r = os.path.relpath(p)
    except ValueError:  # another drive on Windows
        r = str(p)
    r = r if len(r) < len(str(p)) else str(p)
    return f'"{r}"' if " " in r else r


def set_title(path, title):
    text = path.read_text(encoding="utf-8")
    quoted = title.replace("\\", "\\\\").replace('"', '\\"')  # YAML double-quoted
    new, n = re.subn(r'^(\s*title:\s*)".*"', lambda m: f'{m.group(1)}"{quoted}"',
                     text, count=1, flags=re.M)
    if n:
        path.write_text(new, encoding="utf-8")


def rename_part(dest, part):
    """Datasheet: the placeholder part number appears in the body, the doc
    number, and the block diagram, not just the title."""
    qmd = dest / "datasheet.qmd"
    text = qmd.read_text(encoding="utf-8")
    text = text.replace("DS-XR1000", f"DS-{part}").replace("XR-1000", part)
    qmd.write_text(text, encoding="utf-8")
    for svg in (dest / "figures").glob("*.svg"):
        art = svg.read_text(encoding="utf-8").replace("XR-1000", html.escape(part))
        svg.write_text(art, encoding="utf-8")


def in_git_repo(path):
    r = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=path,
                       capture_output=True, encoding="utf-8", errors="replace")
    return r.returncode == 0


def wire_chapters(dest, made):
    """Book --from: the ingested chapters replace the placeholder ones."""
    yml = dest / "_quarto.yml"
    lines = yml.read_text(encoding="utf-8").splitlines(keepends=True)
    at = [n for n, l in enumerate(lines) if l.strip() in (f"- {c}" for c in PLACEHOLDER_CHAPTERS)]
    indent = lines[at[0]][:len(lines[at[0]]) - len(lines[at[0]].lstrip())]
    lines[at[0]:at[-1] + 1] = [f"{indent}- chapters/{m.name}\n" for m in made]
    yml.write_text("".join(lines), encoding="utf-8")
    for c in PLACEHOLDER_CHAPTERS:
        (dest / c).unlink()


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows pipes default to cp1252
    ap = argparse.ArgumentParser(description="Start a new document project.")
    ap.add_argument("kind", nargs="?", choices=sorted(KINDS))
    ap.add_argument("dest", nargs="?", help="folder to create (outside this repo)")
    ap.add_argument("--title", help="document title (default: the template's placeholder)")
    ap.add_argument("--from", dest="raw", metavar="DIR",
                    help="books: folder of the author's raw files to turn into chapters")
    ap.add_argument("--list", action="store_true", help="list the kinds and exit")
    args = ap.parse_args()

    if args.list or not args.kind:
        print("kinds:")
        for k, what in KINDS.items():
            print(f"  {k:<10} {what}")
        print("\nusage: python new.py <kind> <folder> [--title ...] [--from RAW]")
        return
    if not args.dest:
        ap.error("give a destination folder, e.g. ../my-" + args.kind)
    raw = None
    if args.raw:
        if args.kind != "book":
            ap.error("--from works for books so far; for an article or datasheet, "
                     "start the project and bring the text into its .qmd")
        raw = Path(args.raw).expanduser().resolve()
        if not raw.is_dir():
            sys.exit(f"--from {raw}: not a folder.")

    dest = Path(args.dest).expanduser().resolve()
    if dest.exists() and any(dest.iterdir()):
        sys.exit(f"{dest} exists and isn't empty; pick a new folder.")
    if dest == ROOT or ROOT in dest.parents:
        print(f"note: {dest} is inside the toolkit repo, so the toolkit's git "
              "will see it. A folder outside the repo is usually what you want.")

    shutil.copytree(TEMPLATES / args.kind, dest, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("_output", "_book", ".quarto", "__pycache__",
                                                  "tool_output", "*_files"))
    (dest / ".gitignore").write_text(GITIGNORE, encoding="utf-8")
    readme = dest / "README.md"
    tk = str(ROOT)
    tk = f'"{tk}"' if " " in tk else tk
    readme.write_text(readme.read_text(encoding="utf-8").replace("<toolkit>", tk),
                      encoding="utf-8")

    title = args.title or {"book": "Book Title", "article": "Title of the Paper",
                           "datasheet": "XR-1000"}[args.kind]
    if args.title:
        set_title(dest / MAIN[args.kind], args.title)
        if args.kind == "datasheet":
            if re.fullmatch(r"[\w .+/#-]+", args.title):
                rename_part(dest, args.title)
            else:
                print("note: the part number has special characters, so only the "
                      "title was set; replace XR-1000 in datasheet.qmd and "
                      "figures/typical-application.svg by hand.")
    (dest / "CLAUDE.md").write_text(CLAUDE_MD.format(title=title, kind=args.kind, toolkit=tk),
                                    encoding="utf-8")

    if raw:
        before = set((dest / "chapters").glob("*.qmd"))
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "ingest.py"), str(dest),
                            "--from", str(raw)])
        made = sorted(set((dest / "chapters").glob("*.qmd")) - before)
        if r.returncode or not made:
            print("note: nothing was ingested, so the placeholder chapters stay; "
                  f"fix the above, then: python {cmd_path(ROOT / 'scripts' / 'ingest.py')} "
                  f"{cmd_path(dest)} --from {cmd_path(raw)}")
        else:
            wire_chapters(dest, made)
            print(f"wired {len(made)} chapter(s) into _quarto.yml in place of the placeholders.")

    # generate plotted figures now, so a bare `quarto render` works too
    figs = dest / "scripts" / "make_figures.py"
    if figs.exists():
        r = subprocess.run([sys.executable, str(figs)], cwd=dest)
        if r.returncode:
            print("note: figure generation failed (is matplotlib installed? "
                  f"`python -m pip install -r {cmd_path(ROOT / 'requirements.txt')}`); "
                  "build.py retries it.")

    # its own history: /review and check.py --changed-only diff against git
    git_note = ""
    if shutil.which("git") and not in_git_repo(dest):
        subprocess.run(["git", "init", "-q"], cwd=dest)
        git_note = "  (git repo initialized; commit when you're ready)\n"

    build, check, d = cmd_path(ROOT / "build.py"), cmd_path(ROOT / "check.py"), cmd_path(dest)
    print(f"\ncreated {args.kind}: {dest}\n{git_note}\nnext:\n"
          f"  python {build} --doctor            # what's installed, what's missing\n"
          f"  python {build} {d}                 # render\n"
          f"  python {build} {d} --out DIR       # + copy the finished documents to DIR\n"
          f"  python {check} {d}                 # mechanical review\n"
          f"then read {d}/README.md.")


if __name__ == "__main__":
    main()
