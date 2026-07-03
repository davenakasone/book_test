# The Starlight Engine

*How the Ancients Wired the Earth* — by **Dr. Chocolate Daddy**, PhD
(pending), MD, DDS, PPM, PSI, MBA, Esq., HVAC, AM/FM, Notary Public
(revoked).

> **This is a work of satirical fiction.** Every factual claim in the book
> is wrong. Some are wrong in ways that required real effort. Do not cite
> it. *Especially* do not cite it in a school paper.

**📕 Just want to read it? Grab
[The-Starlight-Engine.pdf](The-Starlight-Engine.pdf)** — the built
79-page 6×9" book, committed at the repo root for easy download.

This repo is two things at once:

1. **A complete satirical book** — 15 chapters + 3 appendices of lovingly
   abused math, physics, and archaeology: the Great Pyramid as a
   starlight-pumped fusion reactor, Stonehenge as a 56-bit controller, a
   one-page proof of the Riemann Hypothesis, and dark energy as the
   galaxy's unpaid standby bill.
2. **A proof-of-pipeline for all-open-source book production** — one
   markdown source tree renders a print-ready 6×9" PDF (index, BibTeX
   citations, cross-references, TikZ figures), a valid EPUB3 with cover,
   and a searchable HTML site. Total tooling cost: $0, no sudo.

## Build (macOS / Linux / Windows)

Everything is Python + Quarto — both first-class on all three OSes.
On Windows, run the same commands in PowerShell (use `py` if `python`
isn't on PATH).

```sh
python -m pip install -r requirements.txt   # quarto-cli, matplotlib, numpy, pymupdf
quarto install tinytex                      # ~150 MB LaTeX, self-managing, no admin rights

python scripts/make_figures.py              # regenerate matplotlib figures
python scripts/build_tikz.py                # compile TikZ diagrams → PDF + PNG
cd book && quarto render                    # → _book/  (PDF + EPUB + HTML)
```

All generated figures are committed, so `quarto render` works out of the
box — the two figure scripts are only needed when *editing* figures.

The hand-typeset comparison chapter: `python latex-shootout/build.py`
(memoir class — drop caps, margin notes, custom chapter opener).
`build.sh` remains as a wrapper for Unix muscle memory.

## Layout

| Path | What |
|---|---|
| `book/` | Quarto book source: `_quarto.yml`, chapters, appendices, `references.bib`, figures |
| `scripts/` | figure + social-asset generators (matplotlib) |
| `latex-shootout/` | ch. 1 in raw LaTeX/memoir, for typographic comparison |
| `platform/` | author-platform kit: email sequence, YouTube/IG/LinkedIn playbooks, launch plan, generated assets |
| `NOTES.md` | pipeline findings — every trap hit so you don't have to |
| `PUBLISHING.md` | KDP / IngramSpark / Draft2Digital specs and the money-worth-spending list |

## Highlights of the findings (full list in NOTES.md)

- Quarto's `{dot}`/mermaid blocks silently hang renders waiting on
  Chromium — pre-render diagrams as images.
- Unicode superscripts (`10¹⁷`) drop glyphs in Latin Modern PDF — write
  inline math (`$10^{17}$`).
- `quarto render --to pdf` wipes the other formats from `_book/` — plain
  `quarto render` builds all three side by side.
- LaTeX `\maketitle` will not wrap an author line, a problem for authors
  with ten credentials.

## License

TBD — all rights reserved until the author (either of them) decides.
