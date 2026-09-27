# parked — publishing, on hold

Parked on 2026-09-27, David's call (PLAN.md, option A): the repo is now
`doc_writer`, a toolkit for any document, and publishing the demo book is
not the work. Everything here is kept as-is, not deleted; git has the
history under the old paths.

| What | Was at | What it is |
|---|---|---|
| `PUBLISHING.md` | repo root | KDP / IngramSpark / Draft2Digital specs, pricing, licensing, accessibility, upload checklist |
| `BUSINESS.md` | repo root | the money reality: sales medians, unit economics, earn-out |
| `platform/` | repo root | demo author-platform kit: email sequence, social playbooks, launch plan, `make_social.py` |
| `latex-shootout/` | repo root | demo chapter 1 hand-set in LaTeX memoir, for comparison |

## While parked

- **No `v*` tags.** CI's `release` job still exists and fires on one. The
  old releases (v1.4.0–v1.6.0) stay up.
- The memoir shootout is out of CI. It still builds by hand:
  `python parked/latex-shootout/build.py`.
- `build.py --ingram` (PDF/X-1a) stays: it's a toolkit feature, not
  publishing work.
- `book/` stays active as the regression fixture, and its satire
  disclaimer stays load-bearing (CLAUDE.md, hard-won rule 1). The same
  goes for the disclaimer lines in `platform/` copy.

## Rules that moved here from CLAUDE.md

- **Distribution = GitHub Releases.** Push a `v*` tag and CI attaches the
  PDF, EPUB, and PDF/X-1a. Nothing binary lives in git.
- **Demo-book voice.** Supremely confident, aggrieved by "the mainstream,"
  flags its *true* claims ("this is real, look it up"), asserts the false
  ones without hedging. No lorem ipsum, ever.

## To unpark

It's David's call. `git mv` the files back to the root, restore the
"Memoir shootout still compiles" step in the CI `figures` job, move the
two rules above back into CLAUDE.md, and fix the links that point here
(README, START-HERE, `templates/book/README.md`, NOTES).
