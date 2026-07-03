# book_test — *The Starlight Engine* + open-source book pipeline

## STATUS

**2026-07-02 — v1.3.** 79-page book (15 chapters, 5 parts, 3 appendices)
by "Dr. Chocolate Daddy." One `quarto render` produces: 6×9" print PDF
(index, BibTeX citations, cross-refs, TikZ figures) + EPUB3 with cover +
HTML site with newsletter CTA. Cross-platform verified (macOS-born,
Windows-ready — see NOTES.md portability pass). Author-platform kit in
`platform/`. Remote: `github.com/davenakasone/book_test`.
**Next candidates:** LICENSE file (split: code MIT / prose reserved —
awaiting David), copyright page front-matter, font upgrade via
`mainfont`, print cover wrap, KDP dry-run.

## What this is

Two things at once: a complete **satirical book** (every claim false on
purpose — pyramid fusion reactors, a one-page Riemann proof, dark energy
as a utility bill) and a **proof-of-pipeline** for $0 open-source book
production. It exercises every book feature: parts, front/back matter,
equations, citations, cross-refs, tables, callouts, generated figures,
an index, a cover, multi-format output.

## Build (any OS — macOS / Linux / Windows)

```sh
python -m pip install -r requirements.txt   # quarto-cli, matplotlib, numpy, pymupdf
quarto install tinytex                      # once; no admin rights needed

python scripts/make_figures.py              # matplotlib figures
python scripts/build_tikz.py                # TikZ diagrams → PDF + PNG
cd book && quarto render                    # → _book/ (PDF + EPUB + HTML)
python latex-shootout/build.py              # the raw-LaTeX comparison chapter
```

Generated figures are committed, so `quarto render` alone works out of
the box. On Windows use PowerShell; `py` if `python` isn't on PATH.

## Hard-won rules (violate these and the build breaks — see NOTES.md)

1. **The satire disclaimer in `index.qmd` is load-bearing. Never remove
   or soften it.** Same for the disclaimer lines baked into covers,
   banners, and platform copy.
2. **No `{dot}`/`{mermaid}` code blocks** — they hang `quarto render`
   waiting on Chromium. Pre-render every diagram to an image (TikZ via
   `scripts/build_tikz.py`, or matplotlib).
3. **No unicode superscripts** (`10¹⁷`) in prose — glyphs silently drop
   in the PDF. Write inline math: `$10^{17}$`.
4. Render **all formats with plain `quarto render`** — `--to pdf` wipes
   the other formats from `_book/`.
5. Regenerate figures **before** rendering; EPUB embeds images at render
   time. After a render that changes the book, refresh the root download
   copy: `cp book/_book/The-Starlight-Engine.pdf .`
6. Long author bylines clip on the PDF title page (`\maketitle` doesn't
   wrap); the full credential soup lives on the cover and preface
   signature instead.
7. Keep the voice: supremely confident, aggrieved by "the mainstream,"
   flags its *true* claims explicitly ("this is real, look it up") and
   asserts the false ones without hedging. No lorem ipsum, ever.

## Layout

```
book/            Quarto project — _quarto.yml is the single source of truth
  chapters/      ch01–ch15 (5 parts; anchors #sec-* are cross-referenced)
  appendices/    forbidden equations, alignment tables, glossary
  references.bib real papers cited wrongly + fictional sources
  latex/         preamble.tex (index pkg, author font), after-body.tex
  figures-src/   TikZ sources        figures/  generated outputs (committed)
  html/          newsletter.html CTA (placeholder form — swap in provider embed)
  _book/         render output (gitignored)
scripts/         make_figures.py · make_social.py · build_tikz.py
latex-shootout/  ch01 hand-set in memoir class (typographic comparison)
platform/        email sequence, YT/IG/LinkedIn playbooks, launch plan, assets
NOTES.md         every trap hit, so you don't re-hit them — read before touching render config
PUBLISHING.md    KDP/IngramSpark/D2D specs + the licensing/copyright section
```

## David's-machine specifics (ignore on any other computer)

- Python runs via the shared venv `~/dkn314/bin/python`; quarto lives at
  `~/dkn314/bin/quarto` (house rule: no per-project venvs).
- This folder sits inside David's `claude_stuff/` foreman ecosystem; the
  foreman index (`../CLAUDE.md`) is not ours to edit.
- Pushes to the GitHub remote were explicitly authorized by David
  (2026-07-02). On any other machine: commit freely, but don't push to
  a repo you don't own — fork instead.
