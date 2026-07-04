"""One-command build for the whole repo, any OS.

    python build.py                 # figures → TikZ → book (all formats) → root PDF
    python build.py --skip-figures  # just render the book + refresh root PDF
    python build.py --shootout      # also build the memoir comparison chapter
    python build.py --check-only    # only run the prose-unicode guard, don't build
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Glyphs that silently DROP in Latin Modern under our PDF engine (blank on the
# page, no error). Seen twice: superscripts/subscripts beyond ¹²³
# (10¹⁷ → 10¹) and the left-right arrow ↔ (a whole appendix-B column went
# blank). → (U+2192) and − (U+2212) are verified-rendering and deliberately
# NOT flagged. Fix any hit by wrapping it in inline math ($10^{17}$,
# $\leftrightarrow$). Ranges: U+2070–209F super/subscripts, U+2190/2194 and
# U+21D0–21FF arrows (excludes → U+2192, ← is flagged).
_DROP_RE = re.compile("[⁰-₟←↔⇐-⇿]")


def check_prose_unicode():
    """Fail if a dropping-risk glyph appears in .qmd prose (outside $...$)."""
    offenders = []
    for qmd in sorted((ROOT / "book").rglob("*.qmd")):
        for lineno, line in enumerate(qmd.read_text().splitlines(), 1):
            prose = re.sub(r"\$[^$]*\$", "", line)  # math-mode glyphs render fine
            for m in _DROP_RE.finditer(prose):
                offenders.append(
                    f"  {qmd.relative_to(ROOT)}:{lineno}  U+{ord(m.group()):04X} {m.group()!r}"
                )
    if offenders:
        print("PROSE-UNICODE GUARD failed — these drop silently in the PDF:")
        print("\n".join(offenders))
        print("Fix: wrap in inline math, e.g. $10^{17}$ or $\\leftrightarrow$.")
        sys.exit(1)
    print("→ prose-unicode guard: clean")


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
    ap.add_argument("--ingram", action="store_true",
                    help="also emit the PDF/X-1a CMYK interior for IngramSpark")
    ap.add_argument("--check-only", action="store_true",
                    help="run the prose-unicode guard and exit")
    args = ap.parse_args()

    check_prose_unicode()  # cheap; catches the drop-silent glyph class pre-render
    if args.check_only:
        return

    py = sys.executable
    if not args.skip_figures:
        run("matplotlib figures", [py, "scripts/make_figures.py"])
        run("TikZ diagrams", [py, "scripts/build_tikz.py"])

    run("quarto render (PDF + EPUB + HTML)", [find_quarto(), "render"], cwd=ROOT / "book")

    src = ROOT / "book" / "_book" / "The-Starlight-Engine.pdf"
    if not src.exists():
        sys.exit(f"render finished but {src} is missing — "
                 "check _quarto.yml output-dir / book-output-file")
    shutil.copy(src, ROOT / "The-Starlight-Engine.pdf")
    print("→ refreshed root download copy")

    if args.ingram:
        run("PDF/X-1a CMYK interior (IngramSpark)", [py, "scripts/make_pdfx.py"])

    if args.shootout:
        run("memoir shootout", [py, "latex-shootout/build.py"])

    print("done.")


if __name__ == "__main__":
    main()
