"""Turn raw source files into Quarto chapter stubs.

Drop an author's material into ./incoming/ (any mix of .docx, .odt, .rtf,
.md, .txt), then:

    python scripts/ingest.py                 # -> chapters/NN-slug.qmd + media
    python scripts/ingest.py --project DIR   # a book project somewhere else

Each source file becomes one chapter (sorted by filename — prefix them 01_,
02_, … to control order). Word/ODT/RTF go through pandoc, which also pulls
embedded images into figures/media/. Plain text/markdown is wrapped
with a title heading. Nothing is overwritten; existing chapters are skipped.
Afterward the script prints the chapter list to paste into _quarto.yml.

This is a SCAFFOLDER, not magic: it gives a fresh session clean .qmd to
edit, split, and cross-reference — see START-HERE.md.
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# the book project: this folder if it holds _quarto.yml, else book/ (demo repo)
PROJECT = ROOT if (ROOT / "_quarto.yml").exists() else ROOT / "book"
INCOMING = ROOT / "incoming"
CHAPTERS = PROJECT / "chapters"
MEDIA = PROJECT / "figures" / "media"

PANDOC_EXT = {".docx", ".odt", ".rtf", ".epub", ".html", ".tex"}
TEXT_EXT = {".md", ".markdown", ".txt", ".text"}


def slugify(name):
    s = re.sub(r"^\d+[\s._-]*", "", name)          # strip leading order prefix
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "chapter"


def titleize(name):
    s = re.sub(r"^\d+[\s._-]*", "", name).replace("-", " ").replace("_", " ")
    return s.strip().title() or "Chapter"


def pandoc():
    """System pandoc, else the one bundled with quarto (`quarto pandoc`)."""
    if shutil.which("pandoc"):
        return ["pandoc"]
    quarto = shutil.which("quarto") or str(Path(sys.executable).parent / "quarto")
    if Path(quarto).exists() or shutil.which("quarto"):
        return [quarto, "pandoc"]
    sys.exit("pandoc not found — install quarto (pip install -r requirements.txt) "
             "or pandoc itself.")


def convert(src, dst):
    ext = src.suffix.lower()
    title = titleize(src.stem)
    if ext in PANDOC_EXT:
        MEDIA.mkdir(parents=True, exist_ok=True)
        # markdown output, images extracted, no hard wrapping (Quarto reflows)
        subprocess.run(
            [*pandoc(), str(src), "-t", "markdown", "--wrap=none",
             f"--extract-media={MEDIA}", "-o", str(dst)],
            check=True,
        )
        body = dst.read_text(encoding="utf-8")
        # ensure a top-level H1 title; pandoc rarely emits one from docx
        if not re.match(r"^\s*#\s", body):
            dst.write_text(f"# {title}\n\n{body}", encoding="utf-8")
    elif ext in TEXT_EXT:
        raw = src.read_bytes()
        try:  # UTF-8 (Notepad adds a BOM), else legacy Windows "ANSI"
            body = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            body = raw.decode("cp1252", errors="replace")
        if not re.match(r"^\s*#\s", body):
            body = f"# {title}\n\n{body}"
        dst.write_text(body, encoding="utf-8")
    else:
        return False
    return True


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows pipes default to cp1252
    global INCOMING, CHAPTERS, MEDIA
    ap = argparse.ArgumentParser(description="Turn incoming/ files into chapters.")
    ap.add_argument("--project", help="book project folder (default: auto)")
    args = ap.parse_args()
    if args.project:
        proj = Path(args.project).expanduser().resolve()
        INCOMING, CHAPTERS, MEDIA = proj / "incoming", proj / "chapters", proj / "figures" / "media"
    if not INCOMING.exists():
        INCOMING.mkdir()
        sys.exit(f"Created {INCOMING}/ — drop the author's .docx/.txt/… in "
                 "there and re-run.")
    sources = sorted(
        p for p in INCOMING.iterdir()
        if p.is_file() and p.suffix.lower() in PANDOC_EXT | TEXT_EXT
    )
    if not sources:
        sys.exit(f"No ingestible files in {INCOMING}/ "
                 f"(supported: {sorted(PANDOC_EXT | TEXT_EXT)}).")

    CHAPTERS.mkdir(parents=True, exist_ok=True)
    made, skipped = [], []
    for i, src in enumerate(sources, 1):
        stub = f"{i:02d}-{slugify(src.stem)}"
        dst = CHAPTERS / f"{stub}.qmd"
        if dst.exists():
            skipped.append(dst.name)
            continue
        if convert(src, dst):
            made.append(dst.name)
            print(f"  {src.name} → {dst.relative_to(CHAPTERS.parent)}")

    print(f"\ningested {len(made)} chapter(s); skipped {len(skipped)} existing.")
    if made:
        print("\nPaste into _quarto.yml under book: chapters: (adjust parts/order):")
        for name in made:
            print(f"    - chapters/{name}")
        print("\nNext (see START-HERE.md): set title/author in _quarto.yml, "
              "review each .qmd, add fig-alt to any images under "
              "figures/media/, then `python build.py`.")


if __name__ == "__main__":
    main()
