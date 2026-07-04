"""Quarto post-render hook: make the EPUB epubcheck-clean.

Quarto's `fig-alt` writes the alt text onto the <img> (correct, wanted for
accessibility) but ALSO duplicates it onto the wrapping <div> — and `alt`
is not a legal div attribute in XHTML, so epubcheck fails with RSC-005.
(The obvious alternative, a plain `alt=` attribute, gets silently dropped
by pandoc, leaving alt="" — valid but wrong for screen readers.)

This hook strips `alt` from <div> elements in every .xhtml inside the
rendered EPUB, preserving the EPUB zip invariants (mimetype entry first
and STORED uncompressed). Registered in _quarto.yml under
`project: post-render:` so it runs on every render, locally and in CI.
No-ops when no EPUB was produced (e.g. --to html).
"""

import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

BOOK_DIR = Path(__file__).resolve().parent
OUT = BOOK_DIR / "_book"

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
    epubs = list(OUT.glob("*.epub"))
    if not epubs:
        return  # html/pdf-only render; nothing to do
    for e in epubs:
        n = fix(e)
        print(f"[postrender-fix-epub] {e.name}: stripped {n} illegal div alt attribute(s)")


if __name__ == "__main__":
    sys.exit(main())
