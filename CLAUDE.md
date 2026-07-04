# book_test — *The Starlight Engine* + open-source book pipeline

## STATUS

**2026-07-04 — v1.4 + big-pass hardening.** 90-page book (17 chapters, 6
parts, 3 appendices, "Dr. Chocolate Daddy"). One `quarto render` → 6×9"
print PDF (index, citations, cross-refs, TikZ figs) + EPUB3 w/ cover +
HTML site w/ newsletter CTA. Cross-platform (macOS/Linux/Windows). Remote
`github.com/davenakasone/book_test`; `build.py` = one-command build;
GitHub Actions renders+validates+releases.

**Big pass (multi-agent research+audit) landed 2026-07-04:** fixed a real
KDP-royalty error and a silent ↔-drop that blanked appendix B's claim
column; added pricing/metadata/accessibility(EAA)/direct-sales sections,
ARC+production tracks, hardened licensing, pinned deps, unicode-guard,
table-overflow fixes. Web-verified numbers in PUBLISHING.md; business
reality in BUSINESS.md.

**Full-pipeline pass 2026-07-04:** now a **complete** publish pipeline —
**PDF/X-1a CMYK** for IngramSpark (`build.py --ingram` → `make_pdfx.py`,
Ghostscript); **EPUB accessibility** (fig-alt on all figures +
schema.org OPF metadata, EAA-ready); **LICENSE** (MIT code / CC0 book —
"they can have it"); and a **reusable-template path** (`START-HERE.md` +
`scripts/ingest.py` turns someone's .docx/.txt/diagrams into chapters).
**Next candidates:** copyright-page front-matter, DAISY ACE run, font
upgrade via `mainfont`, print cover wrap, KDP dry-run.

## What this is

Two things at once: a complete **satirical book** (every claim false on
purpose — pyramid fusion reactors, a one-page Riemann proof, dark energy
as a utility bill) and a **proof-of-pipeline** for $0 open-source book
production. It exercises every book feature: parts, front/back matter,
equations, citations, cross-refs, tables, callouts, generated figures,
an index, a cover, multi-format output.

## Build (any OS — macOS / Linux / Windows)

```sh
python -m pip install -r requirements.txt   # pinned deps
quarto install tinytex                      # once; no admin rights needed
brew install ghostscript                    # only if you need --ingram (PDF/X-1a)

python build.py                             # figures → render → PDF+EPUB+HTML → root PDF
python build.py --ingram                    # + PDF/X-1a CMYK interior for IngramSpark
python build.py --check-only                # just the prose-unicode guard
python latex-shootout/build.py              # the raw-LaTeX comparison chapter
```

**Templating a new book from this repo:** copy the repo, drop the author's
`.docx/.txt/…` in `incoming/`, `python scripts/ingest.py` → chapter stubs,
then edit `_quarto.yml` + build. Full runbook: `START-HERE.md`.

Generated figures are committed, so `quarto render` alone works out of
the box. On Windows use PowerShell; `py` if `python` isn't on PATH.

## Hard-won rules (violate these and the build breaks — see NOTES.md)

1. **The satire disclaimer in `index.qmd` is load-bearing. Never remove
   or soften it.** Same for the disclaimer lines baked into covers,
   banners, and platform copy.
2. **No `{dot}`/`{mermaid}` code blocks** — they hang `quarto render`
   waiting on Chromium. Pre-render every diagram to an image (TikZ via
   `scripts/build_tikz.py`, or matplotlib).
3. **No drop-silent unicode in prose** — superscripts beyond ¹²³ (`10¹⁷`)
   and the ↔ arrow (`U+2194`) render blank in Latin Modern. Use inline
   math (`$10^{17}$`, `$\leftrightarrow$`). `python build.py --check-only`
   guards this and CI runs it. (→ `U+2192`, − `U+2212` are verified-safe.)
4. Render **all formats with plain `quarto render`** — `--to pdf` wipes
   the other formats from `_book/`. Simplest: `python build.py` does the
   whole chain (figures → TikZ → render → refresh root PDF).
5. Regenerate figures **before** rendering; EPUB embeds images at render
   time. `python build.py` refreshes the root download PDF automatically.
   (The `keep-tex` `book/*.tex` is generated for debugging but **not**
   committed — gitignored, since it drifts every render.)
6. Long author bylines clip on the PDF title page (`\maketitle` doesn't
   wrap); the full credential soup lives on the cover and preface
   signature instead.
7. Keep the voice: supremely confident, aggrieved by "the mainstream,"
   flags its *true* claims explicitly ("this is real, look it up") and
   asserts the false ones without hedging. No lorem ipsum, ever.

## Layout

```
START-HERE.md    runbook for reusing this as a template for a NEW book
build.py         one-command build (--ingram, --check-only, --shootout)
book/            Quarto project — _quarto.yml is the single source of truth
  chapters/      ch01–ch17 (6 parts; anchors #sec-* are cross-referenced)
  appendices/    forbidden equations, alignment tables, glossary
  references.bib real papers cited wrongly + fictional sources
  latex/         preamble.tex (index pkg, author font), after-body.tex
  figures-src/   TikZ sources        figures/  generated outputs (committed)
  html/          newsletter.html CTA (placeholder form — swap in provider embed)
  epub-metadata.xml  schema.org accessibility metadata (EAA)
  _book/         render output (gitignored)
scripts/         make_figures · make_social · build_tikz · make_pdfx (PDF/X-1a) · ingest (docx→qmd)
latex-shootout/  ch01 hand-set in memoir class (typographic comparison)
platform/        email sequence, YT/IG/LinkedIn playbooks, launch plan, assets
incoming/        (template mode) author's raw source files — gitignored
NOTES.md         every trap hit, so you don't re-hit them — read before touching render config
PUBLISHING.md    KDP/IngramSpark/D2D specs, pricing, accessibility, licensing, upload checklist
BUSINESS.md      investor-frame reality: sales medians, unit economics, earn-out, tax
LICENSE          MIT (pipeline) + CC0 (book)
```

## David's-machine specifics (ignore on any other computer)

- Python runs via the shared venv `~/dkn314/bin/python`; quarto lives at
  `~/dkn314/bin/quarto` (house rule: no per-project venvs).
- This folder sits inside David's `claude_stuff/` foreman ecosystem; the
  foreman index (`../CLAUDE.md`) is not ours to edit.
- Pushes to the GitHub remote were explicitly authorized by David
  (2026-07-02). On any other machine: commit freely, but don't push to
  a repo you don't own — fork instead.
