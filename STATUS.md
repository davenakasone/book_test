# STATUS

NEEDS DAVID (INSTALL): `brew install gh && gh auth login` — lets sessions read CI
logs (the public API returns 403 for logs; this session diagnosed CI blind).

**2026-09-26 — v1.7: from book pipeline to document toolkit.**
`python new.py <book|article|datasheet> <folder>` makes a self-contained
project (template content, copies of build/check/review tools, a README,
and a CLAUDE.md), so a newcomer or a fresh Claude session can start
without reading this repo. New: article template (Typst PDF + HTML + Word, authors,
abstract, citations), datasheet template (Typst theme: title band,
watermark, spec tables, curves plotted from CSV), book starter (the demo's
proven 6×9/EPUB/HTML config without the satire), `build.py --doctor`,
`build.py`/`check.py`/`ingest.py` work on any project folder, CI `templates`
job builds all three. Fixed: book reference list had no heading (ran into
the last appendix in the demo; `references.qmd` added). Reviewed by an adversarial
verifier + a fresh-clone newcomer run; all findings fixed (LOG.md).

**Demo book:** *The Starlight Engine*, 21 chapters, 7 parts, 3
appendices, now with a References page. Releases via `v*` tags.

**Machine:** quarto 1.9.38 at `~/dkn314/bin/quarto` (off PATH), TinyTeX,
Typst 0.14.2 (bundled), ghostscript. No Java (epubcheck is CI-only).

**Open:** CI `templates` job failed on Linux at 0046b65 (passes locally on
macOS); failures now self-report as public annotations. Read them first.

**Next candidates:**
- slides template (reveal.js / PowerPoint) if a real deck needs it
- first real datasheet or paper through `new.py` (the juicebook lesson:
  a real document finds what a dry run can't)
- demo book: copyright page, DAISY ACE run, font upgrade, cover wrap, KDP dry run
- repo name still says `book_test`; renaming the GitHub repo is David's call
