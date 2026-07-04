# The Starlight Engine

*How the Ancients Wired the Earth* — by **Dr. Chocolate Daddy**, PhD
(pending), MD, DDS, PPM, PSI, MBA, Esq., HVAC, AM/FM, Notary Public
(revoked).

> **This is a work of satirical fiction.** Every factual claim in the book
> is wrong. Some are wrong in ways that required real effort. Do not cite
> it. *Especially* do not cite it in a school paper.

**📕 Just want to read it?** Download the built book from
**[Releases](https://github.com/davenakasone/book_test/releases/latest)** —
every tagged version ships the reader PDF, the EPUB, and the print-ready
PDF/X-1a as attached binaries (CI builds them; nothing is committed). The
permanent latest-version link:
[The-Starlight-Engine.pdf](https://github.com/davenakasone/book_test/releases/latest/download/The-Starlight-Engine.pdf).

This repo is two things at once:

1. **A complete satirical book** — 21 chapters + 3 appendices of lovingly
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
python -m pip install -r requirements.txt   # pinned: quarto-cli, matplotlib, numpy, pymupdf, epubcheck
quarto install tinytex                      # ~150 MB LaTeX, self-managing, no admin rights

python build.py                             # figures → TikZ → render (all formats) → refresh root PDF
```

`build.py` is the one-command entry point (it also runs the prose-unicode
guard). To render without regenerating figures: `python build.py
--skip-figures`. All generated figures are committed, so a bare
`cd book && quarto render` also works when you're only editing prose.

The hand-typeset comparison chapter: `python latex-shootout/build.py`
(memoir class — drop caps, margin notes, custom chapter opener).
`latex-shootout/build.sh` remains as a wrapper for Unix muscle memory
(there is no repo-root `build.sh` — the root entry point is `build.py`).

## Layout

| Path | What |
|---|---|
| `book/` | Quarto book source: `_quarto.yml`, chapters, appendices, `references.bib`, figures |
| `scripts/` | figure + social-asset generators (matplotlib) |
| `latex-shootout/` | ch. 1 in raw LaTeX/memoir, for typographic comparison |
| `platform/` | author-platform kit: email sequence, YouTube/IG/LinkedIn playbooks, launch plan, generated assets |
| `NOTES.md` | pipeline findings — every trap hit so you don't have to |
| `PUBLISHING.md` | KDP / IngramSpark / D2D specs, pricing, licensing, accessibility, upload checklist |
| `BUSINESS.md` | the investor-frame reality: sales medians, unit economics, earn-out math, backlist thesis, tax |

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

Take it. The **pipeline** (build scripts, config, templates) is **MIT**;
the **book** (prose, figures, cover) is **CC0 / public domain**. See
[LICENSE](LICENSE). Fork the pipeline for your own book without asking.
