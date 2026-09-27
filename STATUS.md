# STATUS

NEEDS DAVID (INSTALL): `brew install gh && gh auth login` — lets sessions read CI
logs (the public API returns 403 for logs; this session diagnosed CI blind).

**2026-09-27 — Windows encoding fix.** A fresh-clone Windows run from another
session found cp1252 bugs: the glyph guard crashed on `¹⁷` and missed `↔`, and
`→` prints crashed piped runs. All text I/O is now explicit UTF-8. CI's lint and
templates jobs run a Windows-encoding guard, which also caught a fourth bug
(EPUB post-render crashed on non-cp1252 book titles). NOTES.md, Windows pass.
Open: the report's structural points (copied tools don't pick up fixes, ingest
defaults into the demo book) await David's call.

**2026-09-26 — v1.7: from book pipeline to document toolkit.**
`python new.py <book|article|datasheet> <folder>` makes a self-contained
project (template content, copies of build/check/review tools, a README,
and a CLAUDE.md), so a newcomer or a fresh Claude session can start
without reading this repo. New: article template (Typst PDF + HTML + Word, authors,
abstract, citations), datasheet template (Typst theme: title band,
watermark, spec tables, curves plotted from CSV), book starter (the demo's
proven 6×9/EPUB/HTML config without the satire), `build.py --doctor`,
`build.py`/`check.py`/`ingest.py` work on any project folder, CI `templates`
job builds all three. Fixes and review in LOG.md.

**Demo book:** *The Starlight Engine*, 21 chapters, 7 parts, 3
appendices, now with a References page. Releases via `v*` tags.

**Machine:** quarto 1.9.38 at `~/dkn314/bin/quarto` (off PATH), TinyTeX,
Typst 0.14.2 (bundled), ghostscript. No Java (epubcheck is CI-only).

**CI:** all green at 87480a8, including the templates job and epubcheck on
the template book. The 0046b65 templates failure never reproduced (cause
unknown, likely transient). Failures now self-report as public annotations.

**Next candidates:**
- slides template (reveal.js / PowerPoint) if a real deck needs it
- first real datasheet or paper through `new.py` (the juicebook lesson:
  a real document finds what a dry run can't)
- demo book: copyright page, DAISY ACE run, font upgrade, cover wrap, KDP dry run
- repo name still says `book_test`; renaming the GitHub repo is David's call
