"""Build the memoir shootout chapter — cross-platform.

Runs pdflatex twice (for cross-references) into build/. We deliberately
skip latexmk: TinyTeX on Windows ships no perl, which latexmk requires.

Run:  python build.py
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE / "build"


def find_tex(cmd="pdflatex"):
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
    BUILD.mkdir(exist_ok=True)
    pdflatex = find_tex()
    for _pass in (1, 2):
        proc = subprocess.run(
            [pdflatex, "-interaction=nonstopmode", "-output-directory=build",
             "giza-memoir.tex"],
            cwd=HERE,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0 and not (BUILD / "giza-memoir.pdf").exists():
            print(proc.stdout[-2000:])
            sys.exit("pdflatex failed (see log tail above)")
    print(f"→ {BUILD / 'giza-memoir.pdf'}")


if __name__ == "__main__":
    main()
