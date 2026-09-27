# doc_writer — open-source document toolkit + its test book

@STATUS.md

## What this is

Two things in one repo:

1. **A $0 document toolkit.** Markdown in, publication-grade output out,
   through Quarto. Four kinds, each a template in `templates/`:
   - **book**: 6×9 print PDF (LaTeX), EPUB3, HTML site, PDF/X-1a for print
   - **article**: paper/report PDF (Typst), HTML, Word
   - **datasheet**: product datasheet PDF (Typst), spec tables, curves plotted from CSV
   - **report**: guide / plan / trip packet PDF (Typst), HTML, Word; numbers from
     a model via `_variables.yml`, tables from CSV, callouts, phone pages, CJK font

   **The tools stay here; documents live elsewhere.** A job names three
   places: raw content (`--from`, only read), a project folder (the
   document as Markdown + settings, its own git), and an output folder
   (`--out`, finished files). `new.py <kind> <project> [--from RAW]`
   scaffolds a project (content only, no tool copies);
   `build.py <project> [--out DIR]` and `check.py <project>` work on it.
2. **The demo book** (`book/`): a complete satirical book, *The Starlight
   Engine*, where every claim is false on purpose. It exercises every book
   feature (parts, citations, cross-refs, index, TikZ figures, cover), so
   when the pipeline breaks, it breaks here first.

**The roadmap is [PLAN.md](PLAN.md).** Publishing (store specs, economics,
author platform, releases, the memoir comparison) is parked in
[`parked/`](parked/README.md): kept, not worked, until David unparks it.

## Orienting a fresh session

| Asked to… | Do this |
|---|---|
| someone brings raw content + an output location | `python new.py <kind> <project> --from <raw>` (books), then `python build.py <project> --out <output>`; ask where the project folder should live if they didn't say (default: next to the output) |
| work on an existing document | `python build.py <project>`, `python check.py <project>`, `/review <project>` — from this session |
| work on the demo book | edit `book/`, build with `python build.py book` |
| change the toolkit | edit `build.py`, `check.py`, `new.py`, `scripts/`, `templates/`; then run the end-to-end test below |
| publishing, releases, platform | parked: read `parked/README.md`, and ask David before unparking |

**End-to-end test (run before committing toolkit changes):** for each kind,
`python new.py <kind> <scratch>/t-<kind>` (book: `--from` a folder of raw
files), `python build.py <scratch>/t-<kind> --out <scratch>/out-<kind>`,
`python check.py <scratch>/t-<kind>` (exit 0; TEMPLATE-CONTENT warnings are
expected), all with the Windows-encoding guard env below and output piped.
CI's `templates` job does the same on every push.

## Build (any OS — macOS / Linux / Windows; CI runs Linux only, with a Windows-encoding guard)

```sh
python -m pip install -r requirements.txt   # pinned deps, includes quarto-cli
quarto install tinytex                      # once, for LaTeX PDFs (books); no admin rights
python build.py --doctor                    # what's installed, what's missing, what needs it

python build.py PROJECT                     # figures → TikZ → render → EPUB fix (PROJECT=book: the demo)
python build.py PROJECT --out DIR           # + copy PDF/EPUB/Word to DIR, web version to DIR/html/
python build.py PROJECT --ingram            # + PDF/X-1a CMYK interior for IngramSpark (needs ghostscript)
python build.py PROJECT --check-only        # just the prose-unicode guard
python check.py PROJECT                     # mechanical review → PROJECT/tool_output/report-*.md
```

No PROJECT means the current folder. Generated demo figures are committed.
On Windows use PowerShell; `py` if `python` isn't on PATH.

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
4. **Render with `build.py`**: it renders all formats together (`--to pdf`
   wipes the other formats from `_book/`) and then runs the EPUB fix,
   which plain `quarto render` no longer does (no `post-render:` hook).
5. Regenerate figures **before** rendering; EPUB embeds images at render
   time. Nothing binary lives in git.
6. Long author bylines clip on the PDF title page (`\maketitle` doesn't
   wrap); keep `book.author` short.
7. **A Quarto book needs a `references.qmd` page** (`::: {#refs}`), or
   the reference list gets tacked onto the last chapter with no heading.
8. **SVG figures:** fine in Typst and HTML, embedded as SVG in Word, but a
   LaTeX PDF needs `rsvg-convert`. Book figures are PNG/PDF.

Writing demo-book prose? Its voice rule is in `parked/README.md`.

## Toolkit rules

- **Every number you write comes from a command.** Counts, totals, sizes in
  commits, NOTES, LOG, and chat get computed (`wc`, `python -c`) and pasted,
  never summed in your head: "~9,800 lines" went into a commit, NOTES, and
  LOG when `wc -l` said 9,025 (2026-09-27). Same rule the report kind
  enforces for documents. Measure after the last edit: a 107-line count
  went into a pushed commit after the file had grown to 119 (2026-09-27).

- **The authorship boundary.** Sessions scaffold; authors author. Tool-drafted
  text carries `<!-- TODO: TOOL-DRAFTED, NOT AUTHOR-WRITTEN … -->`;
  template text carries `<!-- TODO: TEMPLATE CONTENT … -->`. `check.py`
  nags every marker until it's gone. Never remove a marker whose content
  is still placeholder.
- **Code stays apart from documents.** Tools never live in a project and
  never assume one: the project is the path given, else the current folder
  (must hold `_quarto.yml`), never `book/` by default. Per-project files
  (`tool_output/`, `codespell-ignore.txt`, `scripts/make_figures.py`) live
  in the project. Raw content is only read; `--out` adds and overwrites,
  never deletes. The demo book gets no special cases. Keep the tools
  standalone; no imports between them (new.py calls ingest.py as a subprocess).
- **Templates stay placeholder-honest.** The datasheet ships with a
  `TEMPLATE` watermark and a fictional part; the article cites real papers
  correctly. A template must never pass as a real document.
- `templates/book/latex/` and `book/latex/` are separate copies (typography
  is per-project config). The EPUB fix is a tool (`scripts/fix_epub.py`).
- **UTF-8 explicitly, everywhere.** Every text read, write, and subprocess
  capture passes `encoding="utf-8"`, and every script's `main()` starts
  with `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`.
  Windows defaults to cp1252 and breaks on `¹⁷`, `→`, and `Ω` (NOTES.md,
  Windows pass). CI enforces this; to reproduce locally, set
  `PYTHONWARNDEFAULTENCODING=1 PYTHONWARNINGS=error::EncodingWarning:__main__
  PYTHONIOENCODING=cp1252` and pipe the output.

## Layout

```
new.py           start a project: python new.py <book|article|datasheet|report> <folder> [--from RAW]
build.py         build any project (--out, --doctor, --ingram, --check-only)
check.py         mechanical review of any project → <project>/tool_output/
templates/       book/ article/ datasheet/ report/ — starter content + per-kind README (<toolkit> filled in)
book/            the demo book, an ordinary project (_quarto.yml is its source of truth)
  chapters/ appendices/ references.bib latex/ figures-src/ figures/ html/ scripts/make_figures.py
scripts/         ingest · fix_epub · build_tikz · make_pdfx · extract_feedback
parked/          publishing on hold: PUBLISHING.md BUSINESS.md platform/ latex-shootout/ (README.md says why)
.claude/commands/ /review <project> and /feedback <project>/feedback/<round>
START-HERE.md    newcomer runbook   NOTES.md  every trap hit   LOG.md  finished work
PLAN.md          the roadmap        LICENSE   MIT + CC0
```

## David's-machine specifics (ignore on any other computer)

- Python runs via the shared venv `~/dkn314/bin/python`; quarto is
  `~/dkn314/bin/quarto` (pip `quarto-cli`, **not on PATH** — `which quarto`
  misses it; `build.py` finds it next to the interpreter). TinyTeX is in
  `~/Library/TinyTeX`. `rsvg-convert` (brew librsvg) is installed for SVG in LaTeX PDFs.
- Java is Homebrew openjdk, **not linked**: `java` on PATH is the macOS
  stub. Local epubcheck: `PATH=/opt/homebrew/opt/openjdk/bin:$PATH
  ~/dkn314/bin/epubcheck FILE.epub` (silent + exit 0 means valid).
- `gh` is installed and signed in: read a red CI run with `gh run view <id>
  --log-failed`; rerun a flake with `gh run rerun <id> --failed`.
- PowerPoint, Word, and Keynote are installed (eyeball `.pptx`/`.docx`);
  `python-pptx` and `python-docx` are in dkn314 (added 2026-09-27) for
  checking them from code.
- dkn314 is shared: don't run `pip install -r requirements.txt` into it
  blind. Its `==` pins and quarto-cli's jupyter dependencies can move
  packages other projects use. Every pin matched on 2026-09-27; compare
  with `pip show` first.
- This folder sits inside David's `claude_stuff/` foreman ecosystem; the
  foreman index (`../CLAUDE.md`) is not ours to edit.
- Pushes to the GitHub remote are authorized by David (2026-07-02, again
  2026-09-26). On any other machine: commit freely, but don't push to a
  repo you don't own — fork instead.
