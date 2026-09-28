# STATUS — 2026-09-27

**Where it stands:** `doc_writer`, one document toolkit for every
claude_stuff project (David, 2026-09-27: "crawl claude_stuff … unify doc
writing into one tool"). A job is `new.py <kind> <project> [--from RAW]` →
`build.py <project> --out OUT` → `check.py <project>`. Kinds: book, article,
datasheet, report. PLAN.md Phases 0 and 1 are done; publishing is parked.
**Finish line (David):** once every sibling's document flow runs here and I
judge it good, message `foreman`, who tells every session to come here for
documents. Not yet: 1 of 4 sibling documents reproduced.

**Reproduction 1 done: gis storm-weekend packet** (drop + HANDOFF.md at
`gis/in/from_doc_writer_2026-09-27_storm/`). 8 pp / 1.8 MB against gis's
6 pp / 3.7 MB; every number a var; HTML + Word too. Costs: a smaller page-1
map, and more lines than gis's layout code (NOTES, "First reproduction").
Toolkit gains (c1c78fa): `page-margin:`, vector PDF maps, check.py fixes.

**Verified:** four-kind e2e exits 0 under the Windows-encoding guard, and CI
is green, after c1c78fa. The drop rebuilds from a fresh copy (8 pp, 0 break).

**Next:**
- actionable, FIRST (blocks gis's full swap): letter + phone PDF from one
  report source in one build (a Quarto profile + build.py flag); message
  gis when it lands. gis adopted the export (gis 9f1c6b5): report at
  gis/reports/storm_weekend/, 8 pp / 1.57 MB; it keeps its PDF + phone PNG
  until the phone page exists
- reproduction order is by trigger (survey 2026-09-27): port a document
  when it next needs a real edit. doris's action plan by 10-14 (a figure it
  quotes changes then; page `foreman` ~10-07 to open doris); judy's guide
  when its v2 inputs arrive; gis Pemi (no trigger) in scratch between, as a
  stress test (18 pp, a chooser, a two-column packlist). judy and doris
  only inside their `private/`, with their sessions open
- NEEDS DAVID (RULING): two new documents, neither requested yet: a falcon
  ID write-up for its observer group (article kind), and the Christmas trip
  packet once booked (birds + gis → report, the first trip packet born here)
- actionable: `--from` for article/report (PLAN.md 2.2); slides (2.1);
  Windows runner in CI (2.4)
- 2026-10-19: `ubuntu-latest` → Ubuntu 26 (DEADLINES.md); check CI after.
  When the kinds settle: widen the GitHub repo description to say "reports"
- parked: publishing and demo polish (`parked/README.md`)
