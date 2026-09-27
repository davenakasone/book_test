# Datasheet

A product datasheet written in Markdown: `datasheet.qmd` renders to
`_output/datasheet.pdf` through Typst, so no LaTeX install is needed. It
starts as a fictional part (the XR-1000) with a `TEMPLATE` watermark; every
value in it is a placeholder.

## Build

`python` means your Python 3: use `python3` on macOS/Linux if `python` isn't found, `py` on Windows.

```sh
python -m pip install -r requirements.txt   # once: quarto, matplotlib, pymupdf, codespell
python build.py --doctor                    # what's installed, what's missing
python build.py                             # curves from data/*.csv, then the PDF
python check.py                             # broken refs, missing images, alt text, spelling
```

Once the figures exist, a plain `quarto render` works too.

## What goes where

| Edit | To change |
|---|---|
| `datasheet.qmd` front matter | part number (`title`), one-line description, company, doc number, revision, date, watermark, accent color |
| `datasheet.qmd` body | features, pin table, ratings, electrical specs, application notes, ordering, revision history |
| `data/*.csv` | measured curves: first column is x, each other column is one curve, header row gives the labels |
| `scripts/make_figures.py` (`PLOTS`) | which CSV becomes which figure, the y-axis label, log or linear x |
| `figures/` | diagrams: block diagram, pinout, package drawing. SVG or PNG. `typical-application.svg` has the part number drawn in; `new.py --title` sets it, later renames need an edit there too |
| `theme/typst-template.typ` | the page design: title band, running header, footer, table style |
| `_quarto.yml` | paper size (`papersize: a4`), font, font size |

## Conventions

- **Tables** are pipe tables with the caption underneath:
  `: Electrical characteristics {#tbl-ec}`. Refer to one as `@tbl-ec`.
- **Subscripts** are `V~OUT~`. Equations go in `$$ … $$ {#eq-name}`.
- **Every figure needs `fig-alt="…"`** (a sentence describing it); `check.py` warns without it.
- **Watermark:** keep `PRELIMINARY` until the specs are verified on
  silicon, then delete the `watermark:` line.
- **Releases:** bump `revision:` and add a Revision History row every time
  the PDF goes out.

## Traps

- `warning: unknown font family` means the `mainfont` in `_quarto.yml`
  isn't installed on this machine. Pick one that is (`quarto typst fonts`
  lists them).
- Pandoc escapes `#` in front-matter values; the theme strips it back out
  for `accent`. Any new color parameter you add needs the same
  `.replace("\\", "")` (see `theme/typst-show.typ`).
