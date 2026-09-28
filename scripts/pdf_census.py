"""Count the PDFs under one or more folders by where they came from.

    python scripts/pdf_census.py ROOT [ROOT ...]              # counts + the hand-laid list
    python scripts/pdf_census.py ROOT --list all              # every PDF with its class
    python scripts/pdf_census.py ROOT --list none             # counts only
    python scripts/pdf_census.py ROOT --skip _archive         # leave out folders by name

Classes:
  built      carries the doc_writer mark that build.py writes into the Creator
             field, or sits inside a Quarto project (its figures and renders)
  hand-laid  made by a layout engine a script drives (ReportLab, matplotlib,
             Typst, LaTeX, headless Chrome, ...) and not built here: a document
             whose source, if it still exists, is layout code. The number to
             drive to zero.
  figure     a one-page matplotlib PDF outside a Quarto project: a chart or a
             map, not a document
  received   everything else: statements, letters, forms, saved web pages

Reads each PDF's metadata and page count only, never its text. Folders whose
names start with "." are skipped.
"""

import argparse
import re
import sys
from pathlib import Path

MARK = "doc_writer"  # build.py's stamp() writes this at the start of Creator
# Engines a script drives to lay out a page. Case matters: "TeX" must not
# match "OpenText" (a bank-statement producer).
ENGINES = re.compile(r"ReportLab|Matplotlib|Typst|TeX|WeasyPrint|wkhtmltopdf|"
                     r"HeadlessChrome|FPDF|xhtml2pdf|Prince")


def in_quarto_project(pdf, root):
    for d in pdf.parents:
        if (d / "_quarto.yml").exists():
            return True
        if d == root:
            return False
    return False


def classify(pdf, root, fitz):
    """(class, engine, pages) for one PDF."""
    try:
        with fitz.open(pdf) as doc:
            meta, pages = doc.metadata or {}, doc.page_count
    except Exception:  # damaged or not really a PDF
        return "received", "unreadable", 0
    creator = meta.get("creator") or ""
    producer = meta.get("producer") or ""
    engine = ENGINES.search(f"{creator} {producer}")
    engine = engine.group() if engine else (producer or creator or "?")[:30]
    if creator.startswith(MARK) or in_quarto_project(pdf, root):
        return "built", engine, pages
    if not ENGINES.search(f"{creator} {producer}"):
        return "received", engine, pages
    if engine == "Matplotlib" and pages == 1:
        return "figure", engine, pages
    return "hand-laid", engine, pages


def walk(root, skip):
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).parts
        if any(part.startswith(".") or part in skip for part in rel[:-1]):
            continue
        if p.suffix.lower() == ".pdf" and p.is_file():
            yield p


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # cp1252 on Windows pipes
    ap = argparse.ArgumentParser()
    ap.add_argument("roots", nargs="+", metavar="ROOT")
    ap.add_argument("--list", choices=["hand-laid", "all", "none"], default="hand-laid")
    ap.add_argument("--skip", action="append", default=[], metavar="NAME",
                    help="leave out folders with this name (repeatable)")
    args = ap.parse_args()
    try:
        import fitz  # pymupdf, in requirements.txt
    except ImportError:
        sys.exit("pdf_census needs pymupdf: python -m pip install -r requirements.txt")

    order = ["built", "hand-laid", "figure", "received"]
    for root in (Path(r).expanduser().resolve() for r in args.roots):
        rows = [(p.relative_to(root), *classify(p, root, fitz)) for p in walk(root, set(args.skip))]
        print(f"PDF census of {root}: {len(rows)} PDFs")
        for cls in order:
            print(f"  {cls:<10} {sum(1 for r in rows if r[1] == cls):>4}")
        shown = [r for r in rows if args.list == "all" or r[1] == args.list]
        if shown:
            print()
            for rel, cls, engine, pages in shown:
                tag = "" if args.list != "all" else f"{cls:<10} "
                print(f"  {tag}{rel}  ({engine}, {pages} pp)")


if __name__ == "__main__":
    main()
