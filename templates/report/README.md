# Report

A guide, plan, trip packet, playbook, or report: a document someone reads
to decide or do something. `report.qmd` renders to `_output/report.pdf`
(through Typst, so no LaTeX install is needed), `report.html`, and
`report.docx`. Everything in it starts as placeholder text showing how each
feature is written.

## Build

This folder holds only the document. The tools live in the document
toolkit at `<toolkit>` and take this folder as an argument. From here:

```sh
python <toolkit>/build.py --doctor          # what's installed, what's missing
python <toolkit>/build.py .                 # numbers, tables, figures from data/, then PDF + HTML + Word
python <toolkit>/build.py . --out DIR       # + copy the finished documents to DIR
python <toolkit>/check.py .                 # broken refs, missing images, spelling, open TODOs
```

`python` means your Python 3: use `python3` on macOS/Linux if `python` isn't found, `py` on Windows.
Once per machine: `python -m pip install -r <toolkit>/requirements.txt`.

## What goes where

| Edit | To change |
|---|---|
| `report.qmd` front matter | title, subtitle, author, who it's for, version, date, watermark |
| `report.qmd` body | the document |
| `data/model.json` + `scripts/make_figures.py` | every number the prose quotes (written to `_variables.yml`) |
| `data/*.csv` + `scripts/make_figures.py` | tables (`tables/*.md`) and charts (`figures/*.svg`) |
| `figures/` | other images: maps, diagrams, photos (PNG, PDF, or SVG) |
| `theme/typst-template.typ` | the page design: title band, header, footer, colors |
| `_quarto.yml` | formats, font size, page size |

`build.py` runs `scripts/make_figures.py` before every render, so the PDF
always matches the data.

## The one rule: numbers come from the model

The prose never types a number that is computed somewhere. Put the inputs
in `data/model.json`, compute in `scripts/make_figures.py`, and write
`{{< var trip.fuel_cost >}}` in the text. Change an input, rebuild, and
every page follows. A verdict that depends on numbers ("it does not fit")
is computed there too.

If the numbers already come from your own model or analysis code, have
`make_figures.py` call it (or read its output file) and write
`_variables.yml`. Same for maps: keep the map code where it lives, save
its output as an image, and put it on a page with `![caption](path)`.

## Conventions

- Callouts for what the reader must not miss: `::: {.callout-warning}`
  (also `note`, `tip`, `important`, `caution`). Put the most important one
  first.
- A full-page map or diagram: `{{< pagebreak >}}`, then the image with
  `height=75%` (a share of the page, so it fits letter and phone pages alike).
- Cross-references: label with `{#fig-name}` or `{#tbl-name}` and refer
  with `@fig-name`. Numbering is automatic.
- Every figure needs `fig-alt="…"`; `check.py` warns without it.
- Delete `watermark: "TEMPLATE"` for the real document, or change it to
  `"DRAFT"` while it's in review.

## Readers and page sizes

- **Older readers:** `fontsize: 12pt` or `13pt` in `_quarto.yml`, and a
  plain sans font such as `mainfont: "Verdana"`.
- **Phones:** set `paper-width: 4.5in` and `paper-height: 8in` in
  `_quarto.yml` for a PDF shaped like a phone screen; margins shrink to
  match.
- **Maps and big figures:** `page-margin: 0.5in` in `_quarto.yml` widens
  every page's text area (letter default: 0.85 in at the sides), so a map
  prints larger.
- **Maps with labels:** export each map twice, `map.pdf` (labels stay
  vector: sharp when zoomed, searchable) and `map.jpg`, and write
  `![caption](figures/map)` with no extension. Set
  `default-image-extension: pdf` under `typst:` and `jpg` under `html:` and
  `docx:`, and each format picks its file. A matplotlib PDF over satellite
  tiles stores the tiles losslessly (often 10x a JPEG); re-encode them with
  `gs -sDEVICE=pdfwrite -dAutoFilterColorImages=false
  -dColorImageFilter=/DCTEncode -dNOPAUSE -dBATCH -sOutputFile=map.pdf raw.pdf`.
- **Names with marks** (Hawaiʻi, Kōkua, São Paulo) work in the default
  font.
- **Japanese or Chinese:** add `cjk-font:` to the front matter with a
  face installed on the machine: `"Hiragino Sans"` (macOS),
  `"Noto Sans CJK JP"` (Linux), `"Yu Gothic"` (Windows). Typst embeds it
  properly, so the PDF reads correctly in Chrome, Acrobat, and on phones,
  not only in Preview.

## Private documents

A report about real people (money, health, family) stays out of any
public repo: keep the project folder somewhere private, and send `--out`
somewhere private too. The toolkit only reads the folder you give it.
