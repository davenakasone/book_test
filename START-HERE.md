# START HERE — make your own book, paper, or datasheet

This repo is a toolkit plus a demo book. The tools stay here. Every job
names three places, and they stay apart:

- **raw content**: the author's original files, which are only read
- **the project**: the document as Markdown, figures, and settings, in a
  folder of its own outside this repo
- **the output**: where the finished PDF, EPUB, Word, and web files go

## 1. Set up once

```sh
git clone https://github.com/davenakasone/book_test && cd book_test
python -m pip install -r requirements.txt   # quarto, matplotlib, pymupdf, codespell (pinned)
quarto install tinytex                      # only for books: LaTeX, ~150 MB, no admin rights
python build.py --doctor                    # what's installed, what's missing, what needs it
```

Every `python` here means Python 3: use `python3` on macOS/Linux if
`python` isn't found, and `py` in PowerShell on Windows.

## 2. Start a project

```sh
python new.py --list
python new.py book      ../my-book    --title "My Book" --from ../manuscript
python new.py article   ../my-paper   --title "My Paper"
python new.py datasheet ../xr-2000    --title "XR-2000"
```

Put the folder **outside** this repo; `new.py` gives it its own git
history (`git init`). What you get:

- placeholder content that shows how every feature is written, marked
  `TODO: TEMPLATE CONTENT` so `check.py` nags until it's replaced
  (a book started `--from` a folder of the author's files gets those as
  its chapters instead of the placeholder chapters)
- a `README.md` for that kind of document: what to edit, conventions, traps
- a `CLAUDE.md` so a Claude Code session opened there knows the rules

No tools are copied in. They stay here and take the project as an argument:

```sh
python build.py ../my-book                    # render every format
python build.py ../my-book --out ../finished  # + copy the finished documents there
python check.py ../my-book                    # mechanical review; exit 1 means something breaks the build
```

Renders land in the project's `_output/` (article, datasheet) or `_book/`
(book). `--out` copies the PDF, EPUB, and Word files to the folder you
name, with the web version under `html/`; it never deletes anything
there.

## 3. Working with Claude Code

Open a session **in this toolkit folder** and say where things are, e.g.
*"The manuscript is in ~/Documents/novel-drafts; make a book in ~/books/novel
and put the PDFs in ~/Dropbox/novel-out"* or *"Start a datasheet in
~/parts/xr-2000 and fill in the electrical characteristics from this spec
sheet."* `/review` and `/feedback` live here too. Each project's CLAUDE.md
carries the traps and the authorship boundary below.

## The authorship boundary (a hard rule for any session)

**The tools and the session scaffold; the author authors.** Nothing
rewrites the author's words in place. When a session must draft something
the author didn't write (a preface Quarto requires, a cover tagline, a
title derived from a filename), it marks it:

```
<!-- TODO: TOOL-DRAFTED, NOT AUTHOR-WRITTEN. <why it exists>. Replace
with your own words — check.py flags this file until the TODO is gone. -->
```

`check.py` warns on every unresolved marker, so nothing tool-written ships
in the author's voice. Corrections count too: if a filename-derived title
fixes the author's typo, flag it; don't silently "improve" it.

## Books: from the author's files to print

```sh
python new.py book ../my-book --title "My Book" --from ../manuscript
```

Each `.docx`/`.odt`/`.rtf`/`.txt`/`.md` file in `../manuscript` becomes
one chapter (prefix the files `01_`, `02_`, … for order; images go to
`figures/media/`) and replaces the placeholder chapters in `_quarto.yml`.
The manuscript folder is only read. More files later:
`python scripts/ingest.py ../my-book --from <folder>`, then paste the
chapter list it prints into `_quarto.yml`. Set the author in
`_quarto.yml`. Then the editorial work, yours or Claude's:

- split long Word files into real chapters; give each a `# Title`
- give figures captions and `fig-alt` text (needed for ebooks sold in the EU)
- add cross-references (`@sec-…`, `@fig-…`), index entries (`\index{…}`),
  and citations (`references.bib` + `[@key]`) if the book wants them

`python build.py ../my-book --ingram` adds the PDF/X-1a CMYK interior IngramSpark
requires (needs Ghostscript). Specs, pricing, and the upload checklist:
[PUBLISHING.md](PUBLISHING.md).

## The author's loop (once writing starts)

```
write → git commit → python check.py <project>   # mechanical: spelling, refs, glyphs, markers
                   → /review <project>            # judgment: grammar in context, style, structure
                   → fix what's flagged → commit → repeat
```

- `check.py` findings persist until fixed. Add it to CI to gate pushes.
- `/review` reviews what changed since the last review, leaves
  `TODO(review)` markers at the exact spots, and stores the full write-up in
  the project's `tool_output/review-*.md`. The markers show up in every `check.py` run
  until resolved.
- `tool_output/` is machine-owned and gitignored; git history is the record
  of what the author actually changed.

**When reviewers come back** (marked-up PDFs, Word comments, email):

```
<project>/feedback/r1-<name>/  ← drop whatever each reviewer sent
python scripts/extract_feedback.py <project>/feedback/r1-<name>/   # annotations → extracted.md
/feedback <project>/feedback/r1-<name>                             # triage together, decide, route
```

Decisions land in `feedback/<round>/triage.md` (committed: the editorial
record). Accepted items become `TODO(feedback:…)` markers the checker nags
until resolved; applied fixes are separate `feedback(…):` commits. Rejected
feedback is recorded, never silently dropped.

## Where the knowledge lives

- **[NOTES.md](NOTES.md)**: every pipeline trap already hit, so you don't.
- **[PUBLISHING.md](PUBLISHING.md)**: KDP / IngramSpark / D2D specs,
  pricing, licensing, accessibility, upload checklist.
- **[BUSINESS.md](BUSINESS.md)**: the money reality before anyone spends on
  a book: sales medians, unit economics, when it earns out. A first book
  rarely earns out its production cost; the value of a free pipeline is
  that books 2, 3, 4… are nearly free, so a backlist can compound.
- **[CLAUDE.md](CLAUDE.md)**: how a Claude session works on *this* repo
  (the toolkit and the demo book).
