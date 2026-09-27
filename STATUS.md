# STATUS — 2026-09-27

NEEDS DAVID (INSTALL): `brew install gh && gh auth login` — lets sessions read CI
logs (the public API returns 403 for logs; sessions diagnose CI blind). Also the
gate for a real Windows CI runner.

**Where it stands:** a document toolkit with code kept apart from documents
(David, 2026-09-27: "a person or agent comes for the tools, says where the raw
content is and where the output goes"). The tools stay here; a job is
`new.py <kind> <project> --from RAW` → `build.py <project> --out OUT` →
`check.py <project>`. Projects hold content only (no tool copies); raw is
only read; `--out` never deletes. The demo book (`book/`) is an ordinary
project. Details: LOG.md 2026-09-27, NOTES.md "Code apart from documents".

**Verified:** 40/40 local checks under the Windows-encoding guard (three
kinds, `--from` with UTF-8/BOM/cp1252 raw files, `--out`, `--ingram`, demo
full render, the expected-failure cases). CI green at 70c40d3 (the encoding
fix); the decoupling commit's CI run is pending (actionable: check it next
session; the templates job now asserts `--from`/`--out` too).

**Machine:** quarto 1.9.38 at `~/dkn314/bin/quarto` (off PATH), TinyTeX,
Typst 0.14.2 (bundled), ghostscript. No Java (epubcheck is CI-only).

**PLAN.md is the roadmap** (David, 2026-09-27, option A): rename to
`doc_writer` (Phase 0: David + foreman), park publishing, add slides and
`--from` for every kind, then reproduce sibling projects' documents.

**Next:**
- blocked on David: Phase 0 rename (PLAN.md), then Phase 1 housekeeping
- actionable: confirm CI on the decoupling commit (02f7dcc); fix anything red
- actionable after Phase 1: slides kind, then `--from` for every kind (PLAN.md Phase 2)
- actionable: first real document through the new flow (the juicebook
  lesson: a real document finds what a dry run can't)
- blocked on David (gh): Windows runner in CI, the true "any OS" proof
- parked: publishing and demo polish (copyright page, DAISY ACE, fonts,
  cover wrap, KDP dry run, releases)
