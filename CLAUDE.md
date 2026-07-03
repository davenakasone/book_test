# book_test — open-source book-production pipeline exploration

## STATUS

**2026-07-02 — scaffolding.** Goal: prove out an all-open-source book pipeline
(for David's friend who is writing a real book) using a deliberately absurd
satirical test book, *The Starlight Engine* by "Dr. Rex Meridian." Pipeline
chosen: **Quarto spine** (markdown → 6×9" print PDF via TinyTeX + EPUB3 + HTML
site from one source) **+ one-chapter raw-LaTeX (memoir) shootout** for
typographic comparison. Toolchain installed: quarto-cli 1.9.38 (pip, dkn314
venv) + TinyTeX (~/Library/TinyTeX). Nothing rendered yet.

**Next:** generate figures → first render → fix fallout → memoir shootout →
PUBLISHING.md + NOTES.md verdict.

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
