# Article

A paper, report, or white paper written in Markdown. `article.qmd`
renders to `_output/article.pdf` (through Typst, so no LaTeX install is
needed), `article.html`, and `article.docx` for co-authors who work in
Word. Everything in it starts as placeholder text showing how each feature
is written.

## Build

`python` means your Python 3: use `python3` on macOS/Linux if `python` isn't found, `py` on Windows.

```sh
python -m pip install -r requirements.txt   # once: quarto, matplotlib, pymupdf, codespell
python build.py --doctor                    # what's installed, what's missing
python build.py                             # figures from data/*.csv, then PDF + HTML + Word
python check.py                             # broken refs and citations, missing images, spelling
```

## What goes where

| Edit | To change |
|---|---|
| `article.qmd` front matter | title, authors and affiliations, abstract, keywords, date |
| `article.qmd` body | the paper |
| `references.bib` | sources, as BibTeX (most reference managers and Google Scholar export it). Cite with `[@key]` |
| `data/*.csv` + `scripts/make_figures.py` | plotted figures, rebuilt on every `python build.py` |
| `figures/` | other images (SVG or PNG) |
| `_quarto.yml` | formats, font, two-column layout (`columns: 2`), section numbering |

## Conventions

- Cross-references: label with `{#fig-name}`, `{#tbl-name}`, `{#eq-name}`,
  or `{#sec-name}`, and refer with `@fig-name`. Numbering is automatic.
- Every figure needs `fig-alt="…"`; `check.py` warns without it.
- The reference list is generated at the end; don't write one by hand.

## Submitting to a journal

Most journals want their own LaTeX class. Quarto has ready-made journal
formats (Elsevier, ACM, PLOS, and others) at
<https://quarto.org/docs/extensions/listing-journals.html>:

```sh
quarto add quarto-journals/elsevier    # installs into _extensions/
```

Then set `format: elsevier-pdf` in `_quarto.yml`. Journal formats render
through LaTeX, so run `quarto install tinytex` first. The same Markdown
source keeps working; only the format changes.

## Traps

- The Word output warns `Could not convert image … rsvg-convert`. Word
  2016 and later show the SVG figures anyway; the warning is about a PNG
  fallback for older Word. `brew install librsvg` (or
  `apt install librsvg2-bin`) silences it.
- LaTeX formats (journal classes, `format: pdf`) can't take SVG figures
  without that same `rsvg-convert`. Use PNG or PDF figures there.
