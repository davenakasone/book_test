# LOG — finished work, newest first

Moved out of CLAUDE.md's STATUS block at the 2026-09-26 split (house rule
6). Current state lives in STATUS.md; standing rules in CLAUDE.md.

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
