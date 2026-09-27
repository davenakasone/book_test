"""Make a Quarto EPUB epubcheck-clean.

    python scripts/fix_epub.py path/to/book.epub   # or a folder of .epub files

Quarto's `fig-alt` writes the alt text onto the <img> (correct, wanted for
accessibility) but ALSO duplicates it onto the wrapping <div> — and `alt`
is not a legal div attribute in XHTML, so epubcheck fails with RSC-005.
(The obvious alternative, a plain `alt=` attribute, gets silently dropped
by pandoc, leaving alt="" — valid but wrong for screen readers.)

This strips `alt` from <div> elements in every .xhtml inside the EPUB,
preserving the EPUB zip invariants (mimetype entry first and STORED
uncompressed). `build.py` runs it after every render; running it twice is
harmless.
"""

import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

DIV_ALT = re.compile(rb'(<div\b[^>]*?)\s+alt="[^"]*"')


def fix(epub: Path):
    fixed = 0
    with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as tmp:
        tmppath = Path(tmp.name)
    with zipfile.ZipFile(epub) as zin, zipfile.ZipFile(tmppath, "w") as zout:
        names = zin.namelist()
        # mimetype must be the first entry and uncompressed
        ordered = (["mimetype"] if "mimetype" in names else []) + [
            n for n in names if n != "mimetype"
        ]
        for name in ordered:
            data = zin.read(name)
            if name.endswith(".xhtml"):
                data, n = DIV_ALT.subn(rb"\1", data)
                fixed += n
            comp = zipfile.ZIP_STORED if name == "mimetype" else zipfile.ZIP_DEFLATED
            zout.writestr(zin.getinfo(name).filename, data, compress_type=comp)
    shutil.move(str(tmppath), epub)
    return fixed


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows pipes default to cp1252
    if len(sys.argv) < 2:
        sys.exit("usage: python scripts/fix_epub.py <file.epub | folder> ...")
    epubs = []
    for arg in sys.argv[1:]:
        p = Path(arg)
        epubs += sorted(p.glob("*.epub")) if p.is_dir() else [p]
    for e in epubs:
        n = fix(e)
        print(f"[fix_epub] {e.name}: stripped {n} illegal div alt attribute(s)")


if __name__ == "__main__":
    main()
