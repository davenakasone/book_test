# NOTES — what worked, what fought back (2026-07-02 first pass)

The point of the test book. Ordered by how much time each lesson would save
the friend.

## Traps hit (so the friend doesn't)

1. **Graphviz/Mermaid code blocks stall the render.** Quarto's `{dot}`
   engine wants headless Chromium; without it the render hangs *silently
   on a network socket* (killed ours after 20 min). Wrapping the block in
   html-only conditional content does NOT dodge it — diagram engines run
   before visibility filtering. **Rule: pre-render every diagram** (TikZ
   standalone → PDF, `sips` → PNG; or matplotlib) and include as images.
   Deterministic, offline, works in every format.
2. **Unicode superscripts silently lose glyphs in the PDF.** `10¹⁷` came
   out as `10¹` — Latin Modern has ¹²³ (Latin-1) but not ⁴⁻⁹ (U+2074+),
   and the missing-glyph warning drowns in the log. **Rule: write inline
   math** `$10^{17}$` — pandoc emits `<sup>` for EPUB/HTML automatically.
3. **`quarto render --to pdf` wipes the other formats from `_book/`.**
   One plain `quarto render` builds all formats side by side. Single-format
   renders are for debugging only.
4. **`cover-image` belongs at `book:` level**, not under `format: epub:`.
   And pandoc renames embedded media (`file5.png`) — verify the cover via
   the OPF manifest (`properties="cover-image"`), not by filename.
5. **matplotlib `ax.axis("off")` hides the background patch** — a dark
   cover came out white. Paint an explicit full-bleed Rectangle.
6. **Generate figures BEFORE rendering** — EPUB embeds images at render
   time; a stale PNG ships silently.
7. **Long author strings clip on the PDF title page** — `\maketitle`
   sets authors in a no-wrap tabular. And in book projects, `book.author`
   beats `format: pdf: author:`, so per-format overrides don't rescue
   you. Fix: trim the byline + `\setkomafont{author}{\large}` in the
   preamble. (Discovered giving the author ten credentials.)
8. TinyTeX's `latexmk` flaked once on the memoir build (no log written);
   direct `pdflatex` twice worked. Shrug, but worth knowing.

## What just worked (better than expected)

- **pip-installed quarto-cli** (`~/dkn314/bin/quarto`, v1.9.38) — dodged
  the brew-cask sudo prompt entirely. TinyTeX (~150 MB) into
  `~/Library/TinyTeX`, no root anywhere.
- **TinyTeX auto-installs missing LaTeX packages** during render — zero
  manual tlmgr.
- **The index**: raw `\index{...}` in .qmd + `imakeidx` in preamble →
  quarto's engine loop ran makeindex unprompted. Two-column sorted index
  with subentries, PDF-only (EPUB/HTML ignore it cleanly — they have
  search).
- **Citations**: BibTeX file + `[@key]` → author-year in text + auto
  References chapter, all formats.
- **Cross-refs** (`@fig- @tbl- @eq- @sec-`): numbered + hyperlinked in
  all formats.
- **Callout boxes** render as tcolorbox in PDF, styled divs in EPUB/HTML.
- **TikZ → `sips`** (macOS built-in) for PDF→PNG spared us ghostscript/
  imagemagick installs.
- 6×9 PDF (90pp at v1.4) + valid EPUB3 (mimetype stored-first, cover
  flagged in OPF) + searchable HTML site from one `quarto render`, ~90 s
  warm. (Page/chapter counts live in CLAUDE.md STATUS — the one place they
  should be hardcoded; don't re-quote them across docs.)

## Shootout: Quarto PDF vs hand-rolled memoir

Same chapter both ways (`latex-shootout/build/giza-memoir.pdf`):

| | Quarto default (scrbook) | memoir hand-set |
|---|---|---|
| Look | clean, competent, "tech book" | *book* book: drop cap, epigraph, margin notes, custom opener |
| Effort | markdown only | raw LaTeX, layout debugging |
| Formats | PDF+EPUB+HTML same source | PDF only |
| Friend-usable | yes | only if the friend learns LaTeX |

**Verdict:** write in Quarto. If the print interior must get fancy later,
graft memoir-style typography into Quarto via `template-partials` /
`include-in-header` — same source, upgraded page. Or pay Vellum $249 for
the look with zero effort (see PUBLISHING.md).

## Windows-portability pass (2026-07-02)

The pipeline was born on macOS; two Unix-isms had crept in and are now
gone, so a Windows (or Linux) collaborator can build everything:

- `sips` (macOS-only) rasterized the TikZ PDF → replaced by
  `scripts/build_tikz.py` using **pymupdf** — one rasterizer, all OSes.
- `latex-shootout/build.sh` (shell + hardcoded mac TinyTeX path) →
  `build.py`, which finds TeX via PATH then TinyTeX's per-OS locations.
  It runs pdflatex twice instead of latexmk: **TinyTeX on Windows ships
  no perl, and latexmk is a perl script.**
- `.gitattributes` pins line endings (`* text=auto`, LF for `.sh`) so
  CRLF checkouts don't dirty `.qmd`/`.tex` diffs.
- `requirements.txt` covers the whole Python side, including quarto-cli
  itself (`pip install quarto-cli` works on Windows too — no admin).

## One-command build + CI (2026-07-04)

- **`build.py`** at repo root — one command runs figures → TikZ → `quarto
  render` (all formats) → refreshes the root download PDF. Flags:
  `--skip-figures`, `--shootout`. Finds quarto via PATH or the pip sibling.
- **`.github/workflows/build-book.yml`** — renders on every push, runs
  `epubcheck` (Java is free on the runner, so the deferred local check
  finally happens), uploads PDF+EPUB as a downloadable artifact per commit.
  This also proves a clean-machine build (catches "works on my Mac" drift).

## Accessibility (EAA, June 2025) — TODO wired into the pipeline

Ebooks sold into the EU must meet accessibility rules; our wide path
(D2D → Apple/Kobo) hits the EU. Mechanical work, mostly:
- **alt text** on every `![...]()` in the `.qmd` sources (figures are
  script-generated → descriptions are known; also SEO for the HTML edition).
- **schema.org accessibility metadata** in the EPUB OPF (Quarto can inject).
- validate with **DAISY ACE** next to `epubcheck`.
See PUBLISHING.md → "EPUB accessibility" for the microenterprise-exemption
question (unsettled for solo authors — verify).

## Deferred / untested

- Print *cover wrap* (back+spine+front single PDF) — needs final page
  count first; Inkscape job.
- Fonts beyond Latin Modern (EB Garamond etc. via `mainfont` + TinyTeX
  font package — one-line change, untested).
- KDP upload dry-run.
- Alt-text pass + OPF accessibility metadata (see above) — not yet applied
  to the sources.
