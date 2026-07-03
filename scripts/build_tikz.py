"""Compile TikZ sources (book/figures-src/*.tex) to PDF + rasterize to PNG.

Cross-platform (macOS / Linux / Windows) — replaces the old
pdflatex-then-sips step, since sips exists only on macOS.

Run:  python scripts/build_tikz.py [--width 1800]
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

import fitz  # pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "book" / "figures-src"
OUT = ROOT / "book" / "figures"


def find_tex(cmd="pdflatex"):
    """Locate a TeX binary: PATH first, then TinyTeX's per-OS install dirs."""
    hit = shutil.which(cmd)
    if hit:
        return hit
    home = Path.home()
    candidates = [
        home / "Library/TinyTeX/bin/universal-darwin" / cmd,  # macOS
        home / ".TinyTeX/bin/x86_64-linux" / cmd,  # Linux
        Path(os.environ.get("APPDATA", "")) / "TinyTeX/bin/windows" / f"{cmd}.exe",
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    sys.exit(
        f"{cmd} not found. Install TinyTeX (`quarto install tinytex`) "
        "or put a TeX distribution on PATH."
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, default=1800, help="PNG pixel width")
    args = ap.parse_args()
    pdflatex = find_tex()

    for tex in sorted(SRC.glob("*.tex")):
        proc = subprocess.run(
            [pdflatex, "-interaction=nonstopmode", tex.name],
            cwd=SRC,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            print(proc.stdout[-2000:])
            sys.exit(f"pdflatex failed on {tex.name} (see log tail above)")
        pdf = tex.with_suffix(".pdf")
        shutil.copy(pdf, OUT / pdf.name)
        page = fitz.open(pdf)[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(*(args.width / page.rect.width,) * 2))
        pix.save(OUT / f"{tex.stem}.png")
        print(f"{tex.name} → {pdf.name} + {tex.stem}.png ({pix.width}x{pix.height})")


if __name__ == "__main__":
    main()
