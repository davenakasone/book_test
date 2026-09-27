# PLAN — book_test becomes doc_writer (written 2026-09-27)

**Goal:** any document a person or agent brings (book, presentation,
datasheet, paper, report, memo, letter, guide) goes from raw content to
finished files. The tools stay here; the documents live elsewhere
(`new.py <kind> <project> --from RAW` → `build.py <project> --out DIR`).
David picked this direction on 2026-09-27 (option A: rename, park
publishing, focus on document types).

## Phase 0: the rename (David + foreman, no session open in this folder) — DONE 2026-09-27

1. Rename the folder `~/Desktop/claude_stuff/book_test` → `doc_writer`.
2. The foreman updates its own files, which name `book_test`: `CLAUDE.md`
   (index row and the "Work the book" dispatch verb), `SERVICES.md` row 21
   (new contract in bulletin B-260927-2), `MEMORY_HANDOFF.md`, the root
   `.gitignore`, `HARNESS_PLAN.md`, `.hub/baseline.json`, and the project
   list in `~/Desktop/CLAUDE.md`.
3. Optional, David's call: rename the GitHub repo to `doc_writer` (GitHub
   redirects the old URLs), then `git remote set-url origin
   git@github.com:davenakasone/doc_writer.git`.
4. Open a new session in `doc_writer/`, named `doc_writer`.

## Phase 1: first session after the rename (housekeeping) — DONE 2026-09-27

- Update the name inside the repo: README title and links, CLAUDE.md
  title, the GitHub URL in `new.py`'s project CLAUDE.md, the link in
  `templates/book/README.md`, and STATUS.
- Park publishing: `git mv` PUBLISHING.md, BUSINESS.md, `platform/`, and
  `latex-shootout/` under `parked/`, and drop the shootout step from CI.
  No `v*` tags while parked. **Keep CI** (it is the test suite and the only
  place epubcheck runs) and **keep `book/`** (the regression fixture that
  breaks first).
- Trim CLAUDE.md: the demo-voice rule and publishing details move into
  `parked/`. Checkpoint.

## Phase 2: capability, in order

1. **slides** kind: reveal.js (HTML) + PowerPoint, with Beamer PDF if it's
   cheap; placeholder deck; CI templates job builds it.
2. **`--from` for every kind**: articles and reports (raw files →
   `sections/*.qmd` + `{{< include >}}`), slides (an outline → a deck).
3. **Short forms**: memo, letter, report, as article variants or kinds.
4. **Windows runner in CI**, blocked on David's `gh` install.

## Phase 3: the reproduction loop (David's idea)

Sibling projects in `claude_stuff` already produce documents. Per
iteration: open one sibling's session alongside this one, have it say what
it makes and how, reproduce that document with this toolkit, and fix what
breaks in the tools. One sibling at a time.

- **Their content never enters this repo; it pushes to public GitHub.**
  The document's project folder lives in the sibling's folder (personal
  data: its `private/`); raw content is read in place; output goes where
  the sibling wants. This repo gains only tool fixes, templates, and
  generic CI fixtures.
- **One writer per folder.** While the sibling's session is live, this
  session writes nothing in its folder: the sibling runs the tools itself
  (`python <doc_writer>/build.py <its project>`), or this session works on
  a copy in scratch space that holds no personal data.
- **Score honestly:** did the sibling's pipeline get simpler or better by
  using the toolkit? If not, record why and move on. Take a sibling's
  specialty output (a map, a chart) as a figure; don't re-implement it.
- **Each iteration ends with:** the tool fix, a generic CI fixture that
  pins it, a NOTES.md entry, and a bulletin FINDING if the sibling should
  switch.
- **Recon first, cheap:** one read-only `house:sweeper` pass over how each
  sibling makes documents today (its code and STATUS, never `private/`),
  ranked recurring > one-off, painful pipeline > working one, and no
  personal data first. The candidate list is in local memory, not here.

**Budget:** every iteration keeps two sessions open, and the weekly token
limit is real. Sweep first on haiku, and end an iteration once its tool gap
is found and fixed.
