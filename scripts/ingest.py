"""Turn an author's raw files into Quarto chapter stubs.

    python scripts/ingest.py path/to/book --from path/to/raw-files

Each file in the --from folder (any mix of .docx, .odt, .rtf, .md, .txt)
becomes one chapter in <book>/chapters/, sorted by filename — prefix them
01_, 02_, … to control order. The raw folder is only read: nothing in it
is moved or changed. Word/ODT/RTF go through pandoc, which also pulls
embedded images into <book>/figures/media/. Plain text/markdown is wrapped
with a title heading. Nothing is overwritten; existing chapters are
skipped. Afterward the script prints the chapter list to paste into
_quarto.yml (`new.py book DIR --from RAW` wires it in for you).

This is a SCAFFOLDER, not magic: it gives a fresh session clean .qmd to
edit, split, and cross-reference — see START-HERE.md.
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

CHAPTERS = MEDIA = None  # set from the project in main()

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
    global CHAPTERS, MEDIA
    ap = argparse.ArgumentParser(description="Turn an author's raw files into chapters.")
    ap.add_argument("project", help="the book project folder (holds _quarto.yml)")
    ap.add_argument("--from", dest="raw", required=True, metavar="DIR",
                    help="folder of the author's raw files (read only)")
    args = ap.parse_args()
    proj = Path(args.project).expanduser().resolve()
    yml = proj / "_quarto.yml"
    if not yml.exists() or not re.search(r"^\s*type:\s*book\b",
                                         yml.read_text(encoding="utf-8"), re.M):
        sys.exit(f"{proj} isn't a Quarto book project; ingest makes chapters, "
                 "so start one with: python new.py book <folder> --from <raw>")
    raw = Path(args.raw).expanduser().resolve()
    if not raw.is_dir():
        sys.exit(f"--from {raw}: not a folder.")
    CHAPTERS, MEDIA = proj / "chapters", proj / "figures" / "media"
    sources = sorted(
        p for p in raw.iterdir()
        if p.is_file() and p.suffix.lower() in PANDOC_EXT | TEXT_EXT
    )
    if not sources:
        sys.exit(f"No ingestible files in {raw}/ "
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
              "figures/media/, then `python build.py <book>`.")


if __name__ == "__main__":
    main()
