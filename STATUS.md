# STATUS — 2026-09-27

NEEDS DAVID (INSTALL): `brew install gh && gh auth login` — lets sessions read CI
logs (the public API returns 403 for logs; sessions diagnose CI blind). Also the
gate for a real Windows CI runner.

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
links. CI green at 4bf72f9 and 02f7dcc; the Phase 1 commit's run is pending.

**Machine:** quarto 1.9.38 at `~/dkn314/bin/quarto` (off PATH), TinyTeX,
Typst 0.14.2 (bundled), ghostscript. No Java (epubcheck is CI-only).

**Next:**
- actionable: confirm CI on the Phase 1 commit; fix anything red
- actionable: Phase 2.1, the slides kind (reveal.js + PowerPoint, Beamer PDF
  if cheap; placeholder deck; the CI templates job builds it)
- actionable: Phase 2.2, `--from` for articles and slides; 2.3 short forms
  (memo, letter, report)
- actionable after Phase 2: Phase 3 recon (one haiku `house:sweeper` pass;
  candidates in local memory)
- blocked on David (gh): Windows runner in CI, the true "any OS" proof
- blocked on David: GitHub repo description still says "pipeline to write a
  book…" (suggested: "Markdown in, finished documents out: books, articles
  and datasheets via Quarto. The tools live here; documents live anywhere.")
- parked: publishing and demo polish (`parked/README.md` has the unpark steps)
