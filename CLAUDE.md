# book_test — open-source book-production pipeline exploration

## STATUS

**2026-07-02 — v1.1: Part IV "The Underlying Code" added** (Census Method
pointer-arithmetic, vortex math / digital roots, Riemann Hypothesis
"proof" built on real math trivia — Montgomery–Dyson tea, GUE statistics,
42 sixth-moment, all really cited). v1.2 adds ch13 *The Dark Ledger* (relativity/dark-matter/dark-energy
as grid power accounting). Now **79-page PDF**, 15 chapters, 5 parts. Everything below still true:

**v1 pipeline proven.** *The Starlight Engine*
(satire disclaimer up front) renders from one
`quarto render`: **55-page 6×9" PDF with working index/citations/cross-refs
+ valid EPUB3 with cover + searchable HTML site** (`book/_book/`). Memoir
shootout built too (`latex-shootout/build/giza-memoir.pdf` — drop caps,
margin notes; verdict in NOTES.md: write in Quarto, graft fancy typography
later if wanted). All open source, $0, no sudo: quarto-cli 1.9.38 (pip,
dkn314) + TinyTeX + pymupdf (added to dkn314 for PDF inspection).
Traps documented in NOTES.md (biggest: `{dot}`/mermaid blocks hang the
render wanting Chromium — pre-render diagrams instead; unicode
superscripts drop glyphs in PDF — use inline math).

**Next (if David wants):** font upgrade via `mainfont`, print cover wrap,
KDP upload dry-run, epubcheck via Java. Foreman still needs to register
this project in the index.

## What this is

A **process test, not a real book.** The content bastardizes math/science/
archaeology on purpose (Great Pyramid = starlight-pumped fusion generator,
etc.) to exercise every book-production feature: parts/chapters, front/back
matter, equations, cross-references, citations (BibTeX), tables, callouts,
generated figures (matplotlib), TikZ diagrams, graphviz, an index, a cover,
and multi-format output. The book self-identifies as satire on page 1.

## Layout

```
book_test/
├── CLAUDE.md           ← you are here (STATUS above)
├── NOTES.md            ← process findings: what worked, what fought back
├── PUBLISHING.md       ← where/how to publish; KDP/IngramSpark/D2D specs
├── scripts/
│   └── make_figures.py ← all matplotlib figures (run with ~/dkn314/bin/python)
├── book/               ← the Quarto book project
│   ├── _quarto.yml     ← single source of truth: formats, trim size, chapters
│   ├── index.qmd       ← preface + satire disclaimer
│   ├── frontmatter/    ← foreword
│   ├── chapters/       ← ch01–ch11 (4 parts)
│   ├── appendices/     ← forbidden equations, alignment tables, glossary
│   ├── references.bib  ← real citations used wrongly + fictional ones
│   ├── latex/          ← preamble.tex (index pkg), after-body.tex
│   ├── figures-src/    ← TikZ sources (compiled standalone → pdf/png)
│   ├── figures/        ← generated figure outputs (committed)
│   └── _book/          ← render output (gitignored)
└── latex-shootout/     ← ch01 typeset raw in memoir class for comparison
```

## Rules of the room

- **Build:** `cd book/ && ~/dkn314/bin/quarto render` (all formats).
  Single format: `--to pdf|epub|html`.
- **Figures:** `~/dkn314/bin/python scripts/make_figures.py` regenerates all.
- Python = shared venv `~/dkn314/bin/python` (house rule, no per-project venv).
- Local git only, **never push** (house hygiene rule). Commit per meaningful step.
- Foreman index (`../CLAUDE.md`) is not ours to edit — foreman registers this
  project.
- The satire disclaimer in `index.qmd` is load-bearing. Never remove it.
