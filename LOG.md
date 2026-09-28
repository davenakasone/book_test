# LOG — finished work, newest first

Moved out of CLAUDE.md's STATUS block at the 2026-09-26 split (house rule
6). Current state lives in STATUS.md; standing rules in CLAUDE.md.

**2026-09-28 — phone version; every PDF marked; PDF census.** One report
source builds letter + phone PDFs: `build.py` renders each
`_quarto-<name>.yml` profile as `<stem>-<name>.pdf` (`--no-variants` skips);
the report template ships `_quarto-phone.yml` (4.5 x 8 in) and a
`when-profile` example. Theme fixes found on a sibling's trip packet: long
tables break across pages (only when taller than a page), height-sized
pictures shrink instead of cropping, table words hyphenate on small pages;
its letter PDF stayed pixel-identical (8 of 8 pages). Every PDF built here
carries `doc_writer (<folder>) via <engine>` in Creator;
`scripts/pdf_census.py` counts PDFs by origin (first run over the siblings:
80 PDFs, 10 hand-laid). CI asserts the phone page size, the hidden section,
the mark, and the census on a two-page matplotlib PDF. Moved two stale
untracked PDFs (an old demo copy at the root, a parked shootout render)
into scratch space. NOTES "Phone version and the source mark".

**2026-09-27 — first sibling reproduction (a map-heavy trip packet).**
Rebuilt a sibling's 6-page matplotlib packet as a `report` project in
scratch space (content kept out of this repo; handed to the owner in its
`in/` drop). Owner keeps analysis and maps and exports numbers JSON, table
CSV, and map PDF+JPG; the report owns prose, tables, and a chart. 8 pp /
1.8 MB against 6 pp / 3.7 MB; every number a var; tide times computed and
matched to NOAA's. Toolkit (c1c78fa): report `page-margin:`, vector PDF maps
via extension-less paths + per-format `default-image-extension`, check.py
caption-link and extension-less image fixes; NOTES "First reproduction"
has the score and traps. A stale 107-line count went out in c1c78fa (was
119); fixed, lesson in CLAUDE.md.

**2026-09-27 — report kind; sibling recon; machine + CI upkeep.**
Recon (two read-only haiku sweeps, key claims verified): of the sibling
projects, only three make documents people read, all hand-built in
reportlab or matplotlib (seven scripts, 9,025 lines by `wc -l`; first
reported as ~9,800, a mental-sum error); details stay in
local memory (public repo). New `report` kind for that shape (dfbc77e):
Typst PDF + HTML + Word; `scripts/make_figures.py` writes `_variables.yml`
from `data/model.json` so prose quotes `{{< var >}}`, never numbers; CSV →
`tables/*.md` includes; callouts; full-page figures at `height=75%`;
`paper-width`/`paper-height` phone pages; `cjk-font`; watermark; page X of Y.
`build.py` warns when a PDF embeds LastResort (characters printing as
boxes). CI builds the report and asserts a `{{< var >}}` number reached the
page. Upkeep: CI actions bumped to Node 24 releases (e2e74d5); `gh` authed,
local epubcheck via Homebrew openjdk, rsvg-convert, python-pptx/docx
(a7b8ba8); repo description set; a transient `quarto-cli` sdist download
failure (NOTES trap 9) was rerun green. Ubuntu 26 runner date logged in
DEADLINES.md.

**2026-09-27 — doc_writer Phase 0 + 1 (PLAN.md).** Phase 0 (David + foreman):
folder renamed `book_test` → `doc_writer`, GitHub repo renamed, `origin`
re-pointed; foreman files updated. Phase 1: the name inside the repo (README
title and clone/Releases URLs, START-HERE, CLAUDE.md title, `new.py`'s project
CLAUDE.md URL, `templates/book/README.md` PUBLISHING link, PLATFORM.md).
Publishing parked: `git mv` PUBLISHING.md, BUSINESS.md, `platform/`,
`latex-shootout/` → `parked/`, with `parked/README.md` (why, rules while
parked, unpark steps). CI: memoir-shootout step dropped from `figures`;
`release` job kept but dormant (no `v*` tags). CLAUDE.md trimmed: the demo-voice
rule and the Releases-distribution rule moved to `parked/README.md`. LICENSE,
NOTES, `.gitignore` paths follow the move. Verified: e2e for all three kinds exits 0
under the Windows-encoding guard, `check.py book` exits 0, the shootout builds
from its parked path, the CI YAML parses, no broken Markdown links. CI green at
4bf72f9 and 02f7dcc before this commit.

**2026-09-27 — Code apart from documents.** The tools stay in the toolkit;
a job names raw content, a project, and an output folder. `new.py` stops
copying tools into projects and gains `--from RAW` (books: ingest the raw
files, wire them into `_quarto.yml` in place of the placeholder chapters).
`build.py <project> --out DIR` copies PDF/EPUB/Word to DIR and the web
version to DIR/html/ (never deletes). Every tool resolves the project as the
path given, else the current folder; nothing defaults to `book/`. `ingest.py
<project> --from RAW` reads raw in place (was `<project>/incoming/`). The EPUB
fix moved from a `post-render:` hook to `scripts/fix_epub.py`, run by
`build.py`. Demo-only files moved into the demo: `book/scripts/make_figures.py`,
`book/codespell-ignore.txt`, `platform/make_social.py`; `--shootout` and the
root PDF convenience copy are gone. Template READMEs and project CLAUDE.md
carry the toolkit path (`<toolkit>` filled in by new.py); `/review` and
`/feedback` take a project argument. CI: every job passes explicit paths;
templates job builds from raw fixtures (UTF-8, BOM, cp1252) and asserts the
wiring and delivery; release builds via `build.py --ingram --out dist`.
Verified locally: 40/40 checks under the Windows-encoding guard.

**2026-09-27 — Windows encoding fix (70c40d3, CI green).** A fresh-clone Windows
run from another session found cp1252 bugs: the glyph guard crashed on `¹⁷` and
missed `↔`, and `→` prints crashed piped runs. The guard also caught a fourth
(EPUB post-render crashed on non-cp1252 book titles).
Every text read, write, and subprocess
capture passes `encoding="utf-8"`, and every script's `main()` reconfigures
stdout to UTF-8. Fixed the four cp1252 failure modes in NOTES.md (Windows pass).
CI guard env: `PYTHONWARNDEFAULTENCODING=1`, EncodingWarning as an error in
`__main__`, `PYTHONIOENCODING=cp1252`. Verified locally under the guard,
output piped: all three kinds build and check clean (book titled `Ωmega`), the
glyph guard flags U+2077 and U+2194, check.py quotes `Ω` without crashing, and
ingest, extract_feedback, build_tikz, shootout, and make_pdfx all exit 0.

**2026-09-26 — v1.7: document toolkit.** `new.py <book|article|datasheet>
<folder>` → self-contained project (template content, copies of
build/check/ingest/feedback tools, per-kind README, generated CLAUDE.md,
`git init`). Article template: Typst PDF + HTML + Word. Datasheet template:
custom Typst theme (title band, header/footer, watermark, accent color,
spec tables), curves from `data/*.csv`. Book starter from the demo's config.
`build.py`/`check.py`/`ingest.py`/`build_tikz.py`/`make_pdfx.py` take any
project; `build.py --doctor`; CI `templates` job. Fixed: the book
bibliography had no heading (ran into Appendix C), and NOTES' "auto
References chapter" claim was false; check.py was spell-checking rendered
PDFs/HTML. Reviewed by two agents: an adversarial verifier (found
unescaped quotes in `--title` breaking YAML, and quoted chapter entries
misread as orphans) and a newcomer dry run from a fresh clone (found:
`python` vs `python3`, datasheet `--title` didn't rename the part in the
body/diagram, the book's incoming/ and placeholder-deletion steps were
missing, no git in new projects). All fixed and retested.

**2026-07-08 — v1.6 + editorial loop.** Full author lifecycle now in the
template: `check.py` (mechanical review: codespell, repeated words,
sentence stats, refs/glyphs/markers, `--links`; report → `tool_output/`,
git-aware `--changed-only`, CI `lint` job) + `/review` (judgment layer,
recommendations stored as `TODO(review)` markers + review record) +
`/feedback` with `scripts/extract_feedback.py` (reviewer PDFs/docx/email →
extracted.md → triage.md, committed editorial record). Authorship
boundary is a hard rule: sessions scaffold, authors author; tool-drafted
text carries markers the checker nags. Proven on a second book:
`~/Desktop/juicebook` (6 txt files → PDF/EPUB/PDF-X; caught 2 template
hardcodes + 44 checker false positives — fixed + backported).

**2026-07-04 — v1.6.** 108-page book (21 chapters, 7 parts, 3 appendices,
"Dr. Chocolate Daddy"). New Part VI "The Terms of Service": QM as metering
(observation=audit, entanglement=one account, Bell/Nobel real),
thermodynamics as the service agreement (Landauer's kT·ln2 deletion fee —
real, Carnot=the rake, heat death=disconnection notice), Gödel as the
reason the manual was oral (Gödel numbering = the census method; the
citizenship-loophole story real). v1.6 adds the conclusion: Fermi's
paradox graded (Dark Forest/Zoo/Berserker/Great Filter/Rare Earth all
executed by the book's own machinery) and resolved by the **Semester
Hypothesis** — the galaxy is a campus in session; the silence is
attendance. One `quarto render` → 6×9"
print PDF (index, citations, cross-refs, TikZ figs) + EPUB3 w/ cover +
HTML site w/ newsletter CTA. Cross-platform (macOS/Linux/Windows). Remote
`github.com/davenakasone/book_test`; `build.py` = one-command build;
GitHub Actions renders+validates+releases.

**Big pass (multi-agent research+audit) landed 2026-07-04:** fixed a real
KDP-royalty error and a silent ↔-drop that blanked appendix B's claim
column; added pricing/metadata/accessibility(EAA)/direct-sales sections,
ARC+production tracks, hardened licensing, pinned deps, unicode-guard,
table-overflow fixes. Web-verified numbers in PUBLISHING.md; business
reality in BUSINESS.md.

**Full-pipeline pass 2026-07-04:** now a **complete** publish pipeline —
**PDF/X-1a CMYK** for IngramSpark (`build.py --ingram` → `make_pdfx.py`,
Ghostscript); **EPUB accessibility** (fig-alt on all figures +
schema.org OPF metadata, EAA-ready); **LICENSE** (MIT code / CC0 book —
"they can have it"); and a **reusable-template path** (`START-HERE.md` +
`scripts/ingest.py` turns someone's .docx/.txt/diagrams into chapters).
**Next candidates:** copyright-page front-matter, DAISY ACE run, font
upgrade via `mainfont`, print cover wrap, KDP dry-run.
