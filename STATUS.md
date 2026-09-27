# STATUS — 2026-09-27

**Where it stands:** `doc_writer`, one document toolkit for every
claude_stuff project (David, 2026-09-27: "crawl claude_stuff … unify doc
writing into one tool"). A job is `new.py <kind> <project> [--from RAW]` →
`build.py <project> --out OUT` → `check.py <project>`. Kinds: book, article,
datasheet, **report** (new: guides, plans, trip packets; numbers from a model
via `{{< var >}}`, CSV tables, callouts, phone pages, `cjk-font`). PLAN.md
Phases 0 and 1 are done; publishing is parked in `parked/`.

**Recon done:** only gis, judy, and doris make documents people read, all
built by hand in reportlab or matplotlib. Details and pick order are in local memory
(`sibling-document-candidates`), kept out of git because this repo is public.

**Verified:** CI green at dfbc77e (all four kinds on Linux). Locally, e2e
for all four kinds exits 0 under the Windows-encoding guard; the phone variant
is 4.5×8 in; CJK renders in pdf.js; the new LastResort glyph guard fires when
it should. Not yet opened in Chrome itself (the Browser pane downloads PDFs).

**Machine (2026-09-27):** quarto 1.9.38 at `~/dkn314/bin/quarto` (off PATH),
TinyTeX (beamer present), Typst (bundled), ghostscript, rsvg-convert, `gh`
(authed), Java via Homebrew openjdk (unlinked; CLAUDE.md says how),
PowerPoint/Word/Keynote, python-pptx/docx.

**Next:**
- actionable (next session, first): reproduce the gis storm-weekend packet
  as a `report` project in scratch space (no PII; plan in memory). Score it
  against gis's 944-line script and note what gis must export (map PNGs and
  the printed flood table as CSV)
- blocked on David/foreman: open the gis session to hand it the migration
  (it's closed; per David, the foreman or David stands up closed sessions)
- then judy and doris, only inside their `private/` with their sessions
  open; the temple review (doris) is FINAL, so it's low value
- actionable: `--from` for article/report (PLAN.md 2.2); slides (2.1)
  after the sibling migrations, since no sibling makes slides today
- actionable: Windows runner in CI (PLAN.md 2.4)
- 2026-10-19: `ubuntu-latest` → Ubuntu 26 (DEADLINES.md); check CI after
- when the kinds settle: widen the GitHub repo description to say "reports"
- parked: publishing and demo polish (`parked/README.md`)
