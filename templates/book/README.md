# Book

A book written in Markdown. One `python build.py` renders a print-ready
6×9" PDF (through LaTeX), an EPUB3 ebook, and an HTML website into
`_book/`. It starts as two placeholder chapters that show how each feature
is written.

## Build

`python` means your Python 3: use `python3` on macOS/Linux if `python` isn't found, `py` on Windows.

```sh
python -m pip install -r requirements.txt   # once: quarto, matplotlib, pymupdf, codespell
quarto install tinytex                      # once: LaTeX for the print PDF, no admin rights
python build.py --doctor                    # what's installed, what's missing
python build.py                             # PDF + EPUB + HTML in _book/
python build.py --ingram                    # + PDF/X-1a CMYK interior for IngramSpark
python check.py                             # refs, citations, images, alt text, spelling
```

## Bringing in the author's files

Put their `.docx`, `.odt`, `.rtf`, `.txt`, or `.md` files in `incoming/`,
prefixed `01_`, `02_`, … for chapter order, then:

```sh
python scripts/ingest.py      # one chapter per file in chapters/, images to figures/media/
```

Paste the chapter list it prints into `_quarto.yml` in place of the two
placeholder chapters, delete `chapters/01-first-chapter.qmd` and
`chapters/02-second-chapter.qmd`, set the title and author, and build. Ingest converts and never rewrites; splitting long
files into chapters, captions, and alt text are editorial work.

## What goes where

| Edit | To change |
|---|---|
| `_quarto.yml` | title, author, chapter order, parts, trim size, formats |
| `index.qmd` | the preface (Quarto requires this page) |
| `chapters/*.qmd` | one file per chapter |
| `references.bib` | sources, as BibTeX. Cite with `[@key]` |
| `figures/` | images (PNG or PDF for print). TikZ sources in `figures-src/` compile on build |
| `latex/preamble.tex` | print typography (index, fonts, title page) |
| `epub-metadata.xml` | ebook accessibility metadata |

## The author's loop

```
write → git commit → python check.py → /review (in Claude Code) → fix → repeat
```

When beta readers send back marked-up PDFs, Word comments, or email, put
each reviewer's files in `feedback/r1-<name>/` and run
`python scripts/extract_feedback.py feedback/r1-<name>/`, then
`/feedback feedback/r1-<name>` in Claude Code to triage.

## Rules (each one broke a real build)

1. **No `{dot}` or `{mermaid}` code blocks.** They hang the render waiting
   on a browser. Draw diagrams as images (TikZ in `figures-src/`, or any
   drawing tool).
2. **No unicode superscripts beyond ¹²³ and no ↔ in prose.** They print as
   blanks in the PDF with no error. Write `$10^{17}$` and
   `$\leftrightarrow$`. `python build.py` refuses to build until they're
   fixed.
3. **Render all formats together** (`python build.py` or plain
   `quarto render`). `quarto render --to pdf` deletes the other formats.
4. **Every image needs `fig-alt="…"`.** Ebooks sold into the EU must be
   accessible.
5. **Keep the author line short.** Long bylines run off the PDF title page.
6. **Book figures are PNG or PDF, not SVG.** LaTeX needs an extra
   converter (`rsvg-convert`) for SVG.

Publishing specs, pricing, and the upload checklist for KDP, IngramSpark,
and Draft2Digital:
<https://github.com/davenakasone/book_test/blob/main/PUBLISHING.md>.
