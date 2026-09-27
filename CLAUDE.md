# book_test — open-source document toolkit + *The Starlight Engine*

@STATUS.md

## What this is

Two things in one repo:

1. **A $0 document toolkit.** Markdown in, publication-grade output out,
   through Quarto. Three kinds, each a template in `templates/`:
   - **book**: 6×9 print PDF (LaTeX), EPUB3, HTML site, PDF/X-1a for print
   - **article**: paper/report PDF (Typst), HTML, Word
   - **datasheet**: product datasheet PDF (Typst), spec tables, curves plotted from CSV

   `python new.py <kind> <folder>` makes a self-contained project: template
   content plus copies of the build/check/review tools, its own README, and
   a CLAUDE.md for the session that works there.
2. **The demo book** (`book/`): a complete satirical book, *The Starlight
   Engine*, where every claim is false on purpose. It exercises every book
   feature (parts, citations, cross-refs, index, TikZ figures, cover), so
   when the pipeline breaks, it breaks here first.

## Orienting a fresh session

| Asked to… | Do this |
|---|---|
| make a new book / paper / datasheet | `python new.py <kind> <folder outside this repo>`, then work *in that folder* (its own session is best) |
| work on the demo book | edit `book/`, build with `python build.py` |
| change the toolkit | edit `build.py`, `check.py`, `new.py`, `scripts/`, `templates/`; then run the end-to-end test below |
| check a document anywhere | `python check.py path/to/project` |

**End-to-end test (run before committing toolkit changes):** for each kind,
`python new.py <kind> <scratch>/t-<kind>`, then inside it `python build.py`
and `python check.py` (exit 0; TEMPLATE-CONTENT warnings are expected). CI's
`templates` job does the same on every push.

## Build (any OS — macOS / Linux / Windows; CI runs Linux only, with a Windows-encoding guard)

```sh
python -m pip install -r requirements.txt   # pinned deps, includes quarto-cli
quarto install tinytex                      # once, for LaTeX PDFs (books); no admin rights
python build.py --doctor                    # what's installed, what's missing, what needs it

python build.py                             # demo book: figures → TikZ → render → root PDF
python build.py path/to/project             # any Quarto project folder
python build.py --ingram                    # + PDF/X-1a CMYK interior for IngramSpark (needs ghostscript)
python build.py --check-only                # just the prose-unicode guard
python check.py [path]                      # mechanical review → tool_output/report-*.md
python latex-shootout/build.py              # the raw-LaTeX comparison chapter
```

Generated demo figures are committed, so `quarto render` alone works. On
Windows use PowerShell; `py` if `python` isn't on PATH.

## Hard-won rules (violate these and the build breaks — see NOTES.md)

1. **The satire disclaimer in `book/index.qmd` is load-bearing. Never
   remove or soften it.** Same for the disclaimer lines baked into covers,
   banners, platform copy, and the README.
2. **No `{dot}`/`{mermaid}` code blocks** — they hang `quarto render`
   waiting on Chromium. Pre-render every diagram to an image (TikZ via
   `scripts/build_tikz.py`, SVG, or matplotlib).
3. **No drop-silent unicode in LaTeX-PDF prose** — superscripts beyond ¹²³
   (`10¹⁷`) and ↔ (`U+2194`) render blank in Latin Modern. Use inline
   math (`$10^{17}$`, `$\leftrightarrow$`). `build.py` and `check.py`
   guard it for LaTeX projects; Typst falls back to another font instead.
4. Render **all formats with plain `quarto render`** — `--to pdf` wipes
   the other formats from `_book/`. `python build.py` does the whole chain.
5. Regenerate figures **before** rendering; EPUB embeds images at render
   time. **Distribution = GitHub Releases:** push a `v*` tag and CI
   attaches PDF + EPUB + PDF/X-1a. Nothing binary lives in git.
6. Long author bylines clip on the PDF title page (`\maketitle` doesn't
   wrap); keep `book.author` short.
7. Demo-book voice: supremely confident, aggrieved by "the mainstream,"
   flags its *true* claims ("this is real, look it up"), asserts the false
   ones without hedging. No lorem ipsum, ever.
8. **A Quarto book needs a `references.qmd` page** (`::: {#refs}`), or
   the reference list gets tacked onto the last chapter with no heading.
9. **SVG figures:** fine in Typst and HTML, embedded as SVG in Word, but a
   LaTeX PDF needs `rsvg-convert`. Book figures are PNG/PDF.

## Toolkit rules

- **The authorship boundary.** Sessions scaffold; authors author. Tool-drafted
  text carries `<!-- TODO: TOOL-DRAFTED, NOT AUTHOR-WRITTEN … -->`;
  template text carries `<!-- TODO: TEMPLATE CONTENT … -->`. `check.py`
  nags every marker until it's gone. Never remove a marker whose content
  is still placeholder.
- **`build.py`, `check.py`, and `scripts/*` get copied into every new
  project** (list: `TOOLS` in `new.py`). No demo-only assumptions in
  them: resolve the project as "this folder if it has `_quarto.yml`, else
  `book/`, or the path given." Keep them standalone; no imports between them.
- **Templates stay placeholder-honest.** The datasheet ships with a
  `TEMPLATE` watermark and a fictional part; the article cites real papers
  correctly. A template must never pass as a real document.
- Book infrastructure is single-sourced from `book/` (`postrender-fix-epub.py`,
  `latex/`); `new.py` copies it. Fix it there.
- **UTF-8 explicitly, everywhere.** Every text read, write, and subprocess
  capture passes `encoding="utf-8"`, and every script's `main()` starts
  with `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`.
  Windows defaults to cp1252 and breaks on `¹⁷`, `→`, and `Ω` (NOTES.md,
  Windows pass). CI enforces this; to reproduce locally, set
  `PYTHONWARNDEFAULTENCODING=1 PYTHONWARNINGS=error::EncodingWarning:__main__
  PYTHONIOENCODING=cp1252` and pipe the output.

## Layout

```
new.py           start a new project: python new.py <book|article|datasheet> <folder>
build.py         build any project (--doctor, --ingram, --check-only, --shootout)
check.py         mechanical review of any project → tool_output/
templates/       book/ article/ datasheet/ — starter content + per-kind README
book/            the demo book (Quarto project; _quarto.yml is its source of truth)
  chapters/ appendices/ references.bib latex/ figures-src/ figures/ html/
scripts/         make_figures (demo) · build_tikz · make_pdfx · ingest · extract_feedback · make_social
latex-shootout/  demo ch01 hand-set in memoir (typographic comparison)
platform/        demo author-platform kit (email, social, launch plan)
.claude/commands/ /review and /feedback (also copied into new projects)
START-HERE.md    newcomer runbook   NOTES.md  every trap hit   LOG.md  finished work
PUBLISHING.md    KDP/IngramSpark/D2D specs   BUSINESS.md  money reality   LICENSE  MIT + CC0
```

## David's-machine specifics (ignore on any other computer)

- Python runs via the shared venv `~/dkn314/bin/python`; quarto is
  `~/dkn314/bin/quarto` (pip `quarto-cli`, **not on PATH** — `which quarto`
  misses it; `build.py` finds it next to the interpreter). TinyTeX is in
  `~/Library/TinyTeX`. No Java here, so epubcheck runs in CI only.
- dkn314 is shared: don't run `pip install -r requirements.txt` into it
  blind. Its `==` pins and quarto-cli's jupyter dependencies can move
  packages other projects use. Every pin matched on 2026-09-27; compare
  with `pip show` first.
- This folder sits inside David's `claude_stuff/` foreman ecosystem; the
  foreman index (`../CLAUDE.md`) is not ours to edit.
- Pushes to the GitHub remote are authorized by David (2026-07-02, again
  2026-09-26). On any other machine: commit freely, but don't push to a
  repo you don't own — fork instead.
