"""Turn raw source files into Quarto chapter stubs.

Drop an author's material into ./incoming/ (any mix of .docx, .odt, .rtf,
.md, .txt), then:

    python scripts/ingest.py                 # -> book/chapters/NN-slug.qmd + media

Each source file becomes one chapter (sorted by filename — prefix them 01_,
02_, … to control order). Word/ODT/RTF go through pandoc, which also pulls
embedded images into book/figures/media/. Plain text/markdown is wrapped
with a title heading. Nothing is overwritten; existing chapters are skipped.
Afterward the script prints the chapter list to paste into _quarto.yml.

This is a SCAFFOLDER, not magic: it gives a fresh session clean .qmd to
edit, split, and cross-reference — see START-HERE.md.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCOMING = ROOT / "incoming"
CHAPTERS = ROOT / "book" / "chapters"
MEDIA = ROOT / "book" / "figures" / "media"

PANDOC_EXT = {".docx", ".odt", ".rtf", ".epub", ".html", ".tex"}
TEXT_EXT = {".md", ".markdown", ".txt", ".text"}


def slugify(name):
    s = re.sub(r"^\d+[\s._-]*", "", name)          # strip leading order prefix
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "chapter"


def titleize(name):
    s = re.sub(r"^\d+[\s._-]*", "", name).replace("-", " ").replace("_", " ")
    return s.strip().title() or "Chapter"


def have_pandoc():
    if shutil.which("pandoc"):
        return True
    sys.exit("pandoc not found — install it (brew install pandoc / apt install pandoc).")


def convert(src, dst):
    ext = src.suffix.lower()
    title = titleize(src.stem)
    if ext in PANDOC_EXT:
        have_pandoc()
        MEDIA.mkdir(parents=True, exist_ok=True)
        # markdown output, images extracted, no hard wrapping (Quarto reflows)
        subprocess.run(
            ["pandoc", str(src), "-t", "markdown", "--wrap=none",
             f"--extract-media={MEDIA}", "-o", str(dst)],
            check=True,
        )
        body = dst.read_text()
        # ensure a top-level H1 title; pandoc rarely emits one from docx
        if not re.match(r"^\s*#\s", body):
            dst.write_text(f"# {title}\n\n{body}")
    elif ext in TEXT_EXT:
        body = src.read_text()
        if not re.match(r"^\s*#\s", body):
            body = f"# {title}\n\n{body}"
        dst.write_text(body)
    else:
        return False
    return True


def main():
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
            print(f"  {src.name} → book/chapters/{dst.name}")

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
