# STATUS — 2026-09-27

**Where it stands:** `doc_writer`, one document toolkit for every
claude_stuff project (David, 2026-09-27: "crawl claude_stuff … unify doc
writing into one tool"). A job is `new.py <kind> <project> [--from RAW]` →
`build.py <project> --out OUT` → `check.py <project>`. Kinds: book, article,
datasheet, report. PLAN.md Phases 0 and 1 are done; publishing is parked.
**Finish line (David):** once every sibling's document flow runs here and I
judge it good, message `foreman`, who tells every session to come here for
documents. Not yet: 1 of 4 sibling documents reproduced.

**Reproduction 1 done: gis storm-weekend packet** (scratch, then dropped at
`gis/in/from_doc_writer_2026-09-27_storm/`, with HANDOFF.md holding the
`--export` spec and two gis findings). 8 pp / 1.8 MB against gis's
6 pp / 3.7 MB; every number a var; the plan text keeps its Markdown; HTML +
Word too. Costs: the page-1 map is 5.6 in against 8.2 in, and the report
takes more lines than gis's layout code (NOTES, "First reproduction").
Toolkit gains (c1c78fa, pushed): `page-margin:`, vector PDF maps via
extension-less paths, and check.py caption-link and extension fixes.

**Verified:** the four-kind e2e test exits 0 under the Windows-encoding guard
after c1c78fa. The drop package rebuilds from a fresh copy (8 pp, 0 break).
gis's tree was untouched (git clean; its .pyc dates from 09-25). CI green
for c1c78fa.

**Next:**
- blocked on foreman: David said gis should be open, but no gis session is
  in ListAgents; paged `foreman` (2026-09-27) to stand gis up and relay the
  drop (add `--export`, keep maps, drop its page layout). gis can message
  doc_writer directly
- actionable: reproduce gis Pemi ford packet (18 pp, most prose) the same
  way in scratch; then judy, then doris, only inside their `private/` with
  their sessions open
- actionable (gap found): a phone variant from the same source (a Quarto
  profile with `paper-width`), since gis also ships a phone page
- actionable: `--from` for article/report (PLAN.md 2.2); slides (2.1)
- actionable: Windows runner in CI (PLAN.md 2.4)
- 2026-10-19: `ubuntu-latest` → Ubuntu 26 (DEADLINES.md); check CI after
- when the kinds settle: widen the GitHub repo description to say "reports"
- parked: publishing and demo polish (`parked/README.md`)
