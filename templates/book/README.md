# Book

A book written in Markdown. One build renders a print-ready
6×9" PDF (through LaTeX), an EPUB3 ebook, and an HTML website into
`_book/`. It starts as two placeholder chapters that show how each feature
is written.

## Build

This folder holds only the document. The tools live in the document
toolkit at `<toolkit>` and take this folder as an argument. From here:

```sh
python <toolkit>/build.py --doctor          # what's installed, what's missing
python <toolkit>/build.py .                 # PDF + EPUB + HTML in _book/
python <toolkit>/build.py . --out DIR       # + copy the finished documents to DIR
python <toolkit>/build.py . --ingram        # + PDF/X-1a CMYK interior for IngramSpark
python <toolkit>/check.py .                 # refs, citations, images, alt text, spelling
```

`python` means your Python 3: use `python3` on macOS/Linux if `python` isn't found, `py` on Windows.
Once per machine: `python -m pip install -r <toolkit>/requirements.txt`
and `quarto install tinytex` (LaTeX for the print PDF, no admin rights).

## Bringing in the author's files

`new.py book <folder> --from <raw>` does this when the book is started:
each `.docx`, `.odt`, `.rtf`, `.txt`, or `.md` file in the raw folder
becomes a chapter (prefix them `01_`, `02_`, … for order), in place of the
placeholders. To bring in more files later:

```sh
python <toolkit>/scripts/ingest.py . --from <folder of raw files>
```

It adds one chapter per new file in `chapters/` (images to
`figures/media/`) and prints the list to paste into `_quarto.yml`. The raw
folder is only read. Ingest converts and never rewrites; splitting long
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
write → git commit → check.py → /review → fix → repeat
```

`/review <this folder>` runs in a Claude Code session opened in the toolkit.
When beta readers send back marked-up PDFs, Word comments, or email, put
each reviewer's files in `feedback/r1-<name>/` and run
`python <toolkit>/scripts/extract_feedback.py feedback/r1-<name>/`, then
`/feedback <this folder>/feedback/r1-<name>` in that session to triage.

## Rules (each one broke a real build)

1. **No `{dot}` or `{mermaid}` code blocks.** They hang the render waiting
   on a browser. Draw diagrams as images (TikZ in `figures-src/`, or any
   drawing tool).
2. **No unicode superscripts beyond ¹²³ and no ↔ in prose.** They print as
   blanks in the PDF with no error. Write `$10^{17}$` and
   `$\leftrightarrow$`. `build.py` refuses to build until they're
   fixed.
3. **Build with `build.py`.** It renders all formats together
   (`quarto render --to pdf` deletes the other formats) and then makes the
   EPUB epubcheck-clean, which plain `quarto render` doesn't.
4. **Every image needs `fig-alt="…"`.** Ebooks sold into the EU must be
   accessible.
5. **Keep the author line short.** Long bylines run off the PDF title page.
6. **Book figures are PNG or PDF, not SVG.** LaTeX needs an extra
   converter (`rsvg-convert`) for SVG.

Publishing specs, pricing, and the upload checklist for KDP, IngramSpark,
and Draft2Digital:
<https://github.com/davenakasone/doc_writer/blob/main/parked/PUBLISHING.md>.
