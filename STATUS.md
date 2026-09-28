# STATUS — 2026-09-28

**Where it stands:** `doc_writer`, one document toolkit for every
claude_stuff project. A job is `new.py <kind> <project> [--from RAW]` →
`build.py <project> --out OUT` → `check.py <project>`. Kinds: book, article,
datasheet, report. **Finish line (David):** once every sibling's document
flow runs here and I judge it good, message `foreman`, who tells every
session to come here for documents. Not yet: 1 of 4 sibling documents ported.

**David's ruling 2026-09-28 (option A): stop PDFs with no tooling behind
them.** Done in the toolkit: every PDF `build.py` makes carries
`doc_writer (<folder>) via <engine>` in Creator; `scripts/pdf_census.py`
counts PDFs by origin. First run over claude_stuff: 80 PDFs, 10 hand-laid
(2 are pre-mark doc_writer builds in gis). Still to do: the pitch below.

**Phone version done:** each `_quarto-<name>.yml` profile builds one more PDF
(`report-phone.pdf`, 4.5 x 8 in); the report template ships one. Theme fixes
(long tables break, height-sized maps shrink, phone hyphenation) kept the
gis storm packet's letter PDF pixel-identical, 8 of 8 pages (scratch copy).

**Verified:** four-kind e2e exits 0 under the Windows-encoding guard (a book
`_quarto-large.yml` built too: 10.9 → 14.3 pt). The new CI step passes
locally. CI on push: check it.

**Next:**
- actionable, NOW: push; check CI. Message gis: phone page landed; to get
  it, copy `templates/report/theme/typst-template.typ` + `_quarto-phone.yml`
  into gis/reports/storm_weekend/ and rebuild (also marks its PDFs). David
  then rules whether the phone PDF retires gis's 240-dpi phone PNG
- actionable, NOW: pitch `foreman` the house rule (a document a person reads
  is built by doc_writer from source kept in the owner's folder) and one
  /board line from `pdf_census.py <claude_stuff> --skip _archive`
- port on the next real edit: doris action plan by 10-14 (page `foreman`
  ~10-07 to open doris); judy guide when its v2 inputs arrive; gis Pemi in
  scratch between (no trigger). judy, doris only in their `private/`
- NEEDS DAVID (RULING): falcon ID write-up for its observer group; the
  Christmas trip packet once booked. Neither requested yet
- actionable: `--from` for article/report (PLAN.md 2.2); slides (2.1);
  Windows CI runner (2.4). 2026-10-19: Ubuntu 26 on CI; check after
- parked: publishing and demo polish (`parked/README.md`)
