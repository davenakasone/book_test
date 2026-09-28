# STATUS — 2026-09-28

**Where it stands:** `doc_writer`, one document toolkit for every
claude_stuff project. A job is `new.py <kind> <project> [--from RAW]` →
`build.py <project> --out OUT` → `check.py <project>`. Kinds: book, article,
datasheet, report. **Finish line (David):** once every sibling's document
flow runs here and I judge it good, message `foreman`, who tells every
session to come here for documents. Not yet: 1 of 4 sibling documents ported.

**David's ruling 2026-09-28 (option A): stop PDFs with no tooling behind
them.** Toolkit side done (0fee6b1, CI green, all 4 jobs): every PDF
`build.py` makes carries `doc_writer (<folder>) via <engine>` in Creator;
`scripts/pdf_census.py` counts PDFs by origin (claude_stuff: 80 PDFs, 10
hand-laid, 2 of them pre-mark builds in gis). Pitched to `foreman`: it
widened SERVICES row 21 (root 4ff2542); the house rule and the /board census
line wait on David's yes in the foreman's chat. It will message me.

**Phone version done:** each `_quarto-<name>.yml` profile builds one more PDF
(`report-phone.pdf`, 4.5 x 8 in); the report template ships one. On a
scratch copy of gis's storm packet the letter PDF stayed pixel-identical
(8 of 8 pages), phone 14 pp. Handoff for gis at
`gis/in/from_doc_writer_2026-09-28_phone/HANDOFF.md` (copy 2 files,
rebuild); foreman put it first in gis's next brief (B-260928-2).

**Next:**
- blocked on David (via foreman): house rule "a document a person reads is
  built by doc_writer" + the /board census line. On yes, nothing to do here
- blocked on gis waking: it adopts the phone drop; then David rules whether
  the phone PDF retires gis's 240-dpi phone PNG
- port on the next real edit: doris action plan by 10-14 (DEADLINES
  2026-10-07: page `foreman` to open doris); judy guide when its v2 inputs
  arrive; gis Pemi in scratch between (no trigger). judy, doris only in
  their `private/`, with their sessions open
- NEEDS DAVID (RULING): two new documents, neither requested yet: a falcon
  ID write-up for its observer group, and the Christmas trip packet once
  booked — each would be a document born here, not ported
- actionable: `--from` for article/report (PLAN.md 2.2); slides (2.1);
  Windows CI runner (2.4). 2026-10-19: Ubuntu 26 on CI; check after
- parked: publishing and demo polish (`parked/README.md`)
