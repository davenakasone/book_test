"""One-command build for the whole repo, any OS.

    python build.py                 # figures → TikZ → book (all formats) → root PDF
    python build.py --skip-figures  # just render the book + refresh root PDF
    python build.py --shootout      # also build the memoir comparison chapter
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def find_quarto():
    hit = shutil.which("quarto")
    if hit:
        return hit
    # pip-installed quarto-cli lands next to the python running this script
    sibling = Path(sys.executable).parent / ("quarto.exe" if sys.platform == "win32" else "quarto")
    if sibling.exists():
        return str(sibling)
    sys.exit("quarto not found — pip install -r requirements.txt (or install Quarto)")


def run(desc, cmd, cwd=ROOT):
    print(f"→ {desc}")
    subprocess.run(cmd, cwd=cwd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-figures", action="store_true")
    ap.add_argument("--shootout", action="store_true")
    args = ap.parse_args()

    py = sys.executable
    if not args.skip_figures:
        run("matplotlib figures", [py, "scripts/make_figures.py"])
        run("TikZ diagrams", [py, "scripts/build_tikz.py"])

    run("quarto render (PDF + EPUB + HTML)", [find_quarto(), "render"], cwd=ROOT / "book")

    src = ROOT / "book" / "_book" / "The-Starlight-Engine.pdf"
    shutil.copy(src, ROOT / "The-Starlight-Engine.pdf")
    print("→ refreshed root download copy")

    if args.shootout:
        run("memoir shootout", [py, "latex-shootout/build.py"])

    print("done.")


if __name__ == "__main__":
    main()
