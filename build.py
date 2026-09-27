"""Build any document project, any OS. The tools live here; projects live anywhere.

    python build.py path/to/project            # figures → TikZ → render (all formats)
    python build.py path/to/project --out DIR  # + copy the finished documents to DIR
    python build.py                            # the project in the current folder
    python build.py --doctor                   # what's installed, what's missing, what for
    python build.py PROJECT --skip-figures     # just render
    python build.py PROJECT --ingram           # + PDF/X-1a CMYK print interior (books)
    python build.py PROJECT --check-only       # only the prose-unicode guard, don't build

The project is the folder holding `_quarto.yml`: the path you pass, else the
current folder. `<project>/scripts/make_figures.py`, if present, regenerates
plotted figures first; TikZ sources in `<project>/figures-src/` are compiled
next; after the render, an EPUB gets the epubcheck fix (scripts/fix_epub.py).

--out copies PDF, EPUB, and Word files to DIR and the web version to
DIR/html/. It adds and overwrites; it never deletes anything in DIR.
"""

import argparse
import importlib.util
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP_DIRS = {"_book", "_output", ".quarto", "_extensions", "tool_output",
             "incoming", "feedback", "site_libs"}

# Glyphs that silently DROP in Latin Modern under our PDF engine (blank on the
# page, no error). Seen twice: superscripts/subscripts beyond ¹²³
# (10¹⁷ → 10¹) and the left-right arrow ↔ (a whole appendix-B column went
# blank). → (U+2192) and − (U+2212) are verified-rendering and deliberately
# NOT flagged. Fix any hit by wrapping it in inline math ($10^{17}$,
# $\leftrightarrow$). Ranges: U+2070–209F super/subscripts, U+2190/2194 and
# U+21D0–21FF arrows (excludes → U+2192, ← is flagged). LaTeX PDFs only:
# Typst falls back to another font for a missing glyph instead of dropping it.
_DROP_RE = re.compile("[⁰-₟←↔⇐-⇿]")


def project_dir(arg=None):
    """The path given, else the current folder; either must hold _quarto.yml."""
    p = Path(arg or ".").expanduser().resolve()
    if not (p / "_quarto.yml").exists():
        sys.exit(f"{p} has no _quarto.yml, so it isn't a Quarto project. "
                 "Pass the project folder: python build.py path/to/project")
    return p


def sources(proj):
    return sorted(q for q in proj.rglob("*.qmd")
                  if not SKIP_DIRS & set(q.relative_to(proj).parts))


def uses_latex(proj):
    """True when the project renders a LaTeX PDF (format `pdf`, not `typst`)."""
    yml = (proj / "_quarto.yml").read_text(encoding="utf-8")
    return bool(re.search(r"^\s*(format:\s*)?pdf\s*:|^\s*format:\s*pdf\s*$", yml, re.M))


def check_prose_unicode(proj):
    """Fail if a dropping-risk glyph appears in .qmd prose (outside $...$)."""
    if not uses_latex(proj):
        print("→ prose-unicode guard: skipped (no LaTeX PDF in this project)")
        return
    offenders = []
    for qmd in sources(proj):
        for lineno, line in enumerate(qmd.read_text(encoding="utf-8").splitlines(), 1):
            prose = re.sub(r"\$[^$]*\$", "", line)  # math-mode glyphs render fine
            for m in _DROP_RE.finditer(prose):
                offenders.append(
                    f"  {qmd.relative_to(proj)}:{lineno}  U+{ord(m.group()):04X} {m.group()!r}"
                )
    if offenders:
        print("PROSE-UNICODE GUARD failed — these drop silently in the PDF:")
        print("\n".join(offenders))
        print("Fix: wrap in inline math, e.g. $10^{17}$ or $\\leftrightarrow$.")
        sys.exit(1)
    print("→ prose-unicode guard: clean")


def check_pdf_glyphs(pdfs):
    """Warn when a PDF embeds a last-resort font: some character had no font
    on this machine and prints as a placeholder box (Typst on macOS embeds
    Apple's LastResort face for it; seen with ☐ checklists and CJK text)."""
    try:
        import fitz  # pymupdf, in requirements.txt
    except ImportError:
        return
    for pdf in pdfs:
        with fitz.open(pdf) as doc:
            pages = sorted({n + 1 for n in range(len(doc))
                            for f in doc.get_page_fonts(n) if "LastResort" in f[3]})
        if pages:
            print(f"WARNING: {pdf.name} has characters no installed font covers "
                  f"(page {', '.join(map(str, pages))}); they print as boxes. "
                  "Set a font that has them (mainfont, or cjk-font for Japanese/Chinese).")


def find_quarto(required=True):
    hit = shutil.which("quarto")
    if hit:
        return hit
    # pip-installed quarto-cli lands next to the python running this script
    sibling = Path(sys.executable).parent / ("quarto.exe" if sys.platform == "win32" else "quarto")
    if sibling.exists():
        return str(sibling)
    if required:
        sys.exit("quarto not found — python -m pip install -r requirements.txt "
                 "(or install Quarto from quarto.org)")
    return None


def find_tex():
    """A LaTeX binary on PATH or in TinyTeX's per-OS install dirs."""
    hit = shutil.which("pdflatex") or shutil.which("xelatex")
    if hit:
        return hit
    home = Path.home()
    for c in (home / "Library/TinyTeX/bin/universal-darwin/pdflatex",
              home / ".TinyTeX/bin/x86_64-linux/pdflatex",
              Path(os.environ.get("APPDATA", "")) / "TinyTeX/bin/windows/pdflatex.exe"):
        if c.exists():
            return str(c)
    return None


def run(desc, cmd, cwd=None):
    print(f"→ {desc}")
    subprocess.run(cmd, cwd=cwd, check=True)


def output_dir(proj):
    yml = (proj / "_quarto.yml").read_text(encoding="utf-8")
    m = re.search(r"^\s*output-dir:\s*(\S+)", yml, re.M)
    return proj / m.group(1) if m else proj


def deliver(rendered, proj, dest):
    """Copy the finished documents to dest: PDF/EPUB/Word at the top, the web
    version (HTML plus its assets) under html/. Adds and overwrites only."""
    docs = [p for p in rendered.iterdir() if p.suffix in {".pdf", ".epub", ".docx"}]
    dest.mkdir(parents=True, exist_ok=True)
    for p in docs:
        shutil.copy2(p, dest / p.name)
    web = [p for p in rendered.iterdir() if p not in docs]
    if rendered == proj:  # no output-dir: the render sits among the sources
        web = [p for p in web if p.suffix == ".html" or p.name.endswith("_files")]
    if any(p.suffix == ".html" for p in web):
        for p in web:
            if p.is_dir():
                shutil.copytree(p, dest / "html" / p.name, dirs_exist_ok=True)
            else:
                (dest / "html").mkdir(exist_ok=True)
                shutil.copy2(p, dest / "html" / p.name)
    return docs


def doctor():
    """Report each tool: found or not, and what needs it."""
    def cmd_ok(*cmd):
        try:
            r = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace",
                               timeout=30)
            out = (r.stdout or r.stderr).strip().splitlines()
            return r.returncode == 0, (out[0] if out else "")
        except (OSError, subprocess.TimeoutExpired):
            return False, ""

    def module(name):
        return importlib.util.find_spec(name) is not None

    q = find_quarto(required=False)
    q_ok, q_ver = cmd_ok(q, "--version") if q else (False, "")
    t_ok, t_ver = cmd_ok(q, "typst", "--version") if q else (False, "")
    tex = find_tex()
    pandoc = shutil.which("pandoc")
    codespell = shutil.which("codespell") or next(
        (str(p) for p in [Path(sys.executable).parent / "codespell"] if p.exists()), None)
    gs = shutil.which("gs") or shutil.which("gswin64c")
    java_ok, _ = cmd_ok("java", "-version") if shutil.which("java") else (False, "")

    rows = [
        ("python", True, sys.version.split()[0], "everything", ""),
        ("quarto", q_ok, q_ver, "rendering", "python -m pip install -r requirements.txt"),
        ("typst", t_ok, t_ver, "article, datasheet, report PDFs", "comes with quarto"),
        ("LaTeX", bool(tex), tex or "", "book PDF", "quarto install tinytex"),
        ("pandoc", bool(pandoc or q_ok), pandoc or "via quarto", "scripts/ingest.py", "comes with quarto"),
        ("matplotlib", module("matplotlib"), "", "plotted figures", "pip install -r requirements.txt"),
        ("pymupdf", module("fitz"), "", "TikZ figures, feedback extraction", "pip install -r requirements.txt"),
        ("codespell", bool(codespell), codespell or "", "spell check in check.py", "pip install -r requirements.txt"),
        ("ghostscript", bool(gs), gs or "", "--ingram (print PDF/X-1a)", "brew install ghostscript / apt install ghostscript"),
        ("java", java_ok, "", "epubcheck (EPUB validation)", "install a JDK, e.g. Temurin 17"),
    ]
    print(f"toolkit doctor ({sys.executable})\n")
    for name, ok, detail, needed_for, fix in rows:
        mark = "ok " if ok else "-- "
        line = f"  {mark} {name:<12} {needed_for:<34}"
        line += f" {detail}" if ok else f" missing: {fix}"
        print(line.rstrip())
    core = q_ok
    print("\ncore toolchain " + ("ready." if core else "NOT ready: install quarto first."))
    sys.exit(0 if core else 1)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace",  # cp1252 on Windows pipes
                           line_buffering=True)  # our lines interleave with quarto's
    ap = argparse.ArgumentParser()
    ap.add_argument("project", nargs="?",
                    help="Quarto project folder (default: the current folder)")
    ap.add_argument("--out", metavar="DIR",
                    help="also copy the finished documents here (never deletes)")
    ap.add_argument("--skip-figures", action="store_true")
    ap.add_argument("--ingram", action="store_true",
                    help="also emit the PDF/X-1a CMYK interior for IngramSpark")
    ap.add_argument("--check-only", action="store_true",
                    help="run the prose-unicode guard and exit")
    ap.add_argument("--doctor", action="store_true",
                    help="report which tools are installed and what needs them")
    args = ap.parse_args()

    if args.doctor:
        doctor()
    proj = project_dir(args.project)
    print(f"→ project: {proj}")

    check_prose_unicode(proj)  # cheap; catches the drop-silent glyph class pre-render
    if args.check_only:
        return

    py = sys.executable
    if not args.skip_figures:
        figs = proj / "scripts" / "make_figures.py"
        if figs.exists():
            run("plotted figures", [py, str(figs)], cwd=proj)
        if list((proj / "figures-src").glob("*.tex")):
            run("TikZ diagrams", [py, str(ROOT / "scripts" / "build_tikz.py"),
                                  "--project", str(proj)])

    run("quarto render (all formats)", [find_quarto(), "render"], cwd=proj)

    out = output_dir(proj)
    if list(out.glob("*.epub")):
        run("EPUB fix (epubcheck-clean alt text)",
            [py, str(ROOT / "scripts" / "fix_epub.py"), str(out)])
    built = sorted(p for p in out.glob("*")
                   if p.suffix in {".pdf", ".epub", ".docx", ".html"})
    for p in built:
        print(f"   {p.relative_to(proj)}")
    pdfs = [p for p in built if p.suffix == ".pdf" and not p.name.endswith("-PDFX.pdf")]
    check_pdf_glyphs(pdfs)

    if args.ingram:
        if not pdfs:
            sys.exit("--ingram needs a rendered PDF.")
        src = pdfs[0]
        run("PDF/X-1a CMYK interior (IngramSpark)",
            [py, str(ROOT / "scripts" / "make_pdfx.py"), str(src),
             str(src.with_name(src.stem + "-PDFX.pdf"))])

    if args.out:
        dest = Path(args.out).expanduser().resolve()
        docs = deliver(out, proj, dest)
        print(f"→ delivered to {dest}: " + (", ".join(p.name for p in docs) or "no documents")
              + (" + html/" if (dest / "html").exists() else ""))

    print("done.")


if __name__ == "__main__":
    main()
