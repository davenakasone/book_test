# STATUS — 2026-09-27

**Where it stands:** `doc_writer` (was `book_test`), a document toolkit with
the code kept apart from the documents. A job is `new.py <kind> <project> --from RAW`
→ `build.py <project> --out OUT` → `check.py <project>`. Kinds: book,
article, datasheet (`--from` is books-only so far). PLAN.md Phases 0 and 1
are done: the folder and GitHub repo are renamed, the name is updated inside
the repo, and publishing is parked in `parked/` (see `parked/README.md`; no `v*` tags).
The demo book (`book/`) stays as the regression fixture. Details: LOG.md.

**Verified (Phase 1):** e2e for all three kinds exits 0 (new, build, check)
under the Windows-encoding guard; `check.py book` exits 0; the memoir shootout
builds from `parked/latex-shootout/`; the CI YAML parses; no broken Markdown
links. CI green at 8b85614 (the Phase 1 commit), after rerunning a transient
`quarto-cli` download failure (NOTES trap 9).

**Machine (2026-09-27):** quarto 1.9.38 at `~/dkn314/bin/quarto` (off PATH),
TinyTeX (beamer present), Typst (bundled), ghostscript, rsvg-convert, `gh`
(authed: CI logs readable), Java via Homebrew openjdk (unlinked; epubcheck runs
locally, CLAUDE.md says how), PowerPoint/Word/Keynote, python-pptx/docx.

**Next:**
- actionable: Phase 2.1, the slides kind (reveal.js + PowerPoint, Beamer PDF
  if cheap; placeholder deck; the CI templates job builds it)
- actionable: Phase 2.2, `--from` for articles and slides; 2.3 short forms
  (memo, letter, report)
- actionable after Phase 2: Phase 3 recon (one haiku `house:sweeper` pass;
  candidates in local memory)
- actionable (unblocked: gh is in): Windows runner in CI, the true "any OS"
  proof (PLAN.md 2.4)
- small, actionable: CI actions run on deprecated Node 20 (checkout@v4,
  setup-python@v5); bump when touching the workflow next
- when slides/short forms ship: widen the GitHub repo description (set
  2026-09-27 to books, articles, datasheets)
- parked: publishing and demo polish (`parked/README.md` has the unpark steps)
