# START HERE — make your own book, paper, or datasheet

This repo is a toolkit plus a demo book. You don't work inside it: you ask
it for a fresh project folder, then work there.

## 1. Set up once

```sh
git clone https://github.com/davenakasone/book_test && cd book_test
python -m pip install -r requirements.txt   # quarto, matplotlib, pymupdf, codespell (pinned)
quarto install tinytex                      # only for books: LaTeX, ~150 MB, no admin rights
python build.py --doctor                    # what's installed, what's missing, what needs it
```

On Windows, use PowerShell and `py` if `python` isn't on PATH.

## 2. Start a project

```sh
python new.py --list
python new.py book      ../my-book    --title "My Book"
python new.py article   ../my-paper   --title "My Paper"
python new.py datasheet ../xr-2000    --title "XR-2000"
```

Put the folder **outside** this repo; it gets its own history
(`git init` inside it). What you get:

- placeholder content that shows how every feature is written, marked
  `TODO: TEMPLATE CONTENT` so `check.py` nags until it's replaced
- `build.py`, `check.py`, and the helper scripts, copied in (the folder
  doesn't depend on this repo)
- a `README.md` for that kind of document: what to edit, conventions, traps
- a `CLAUDE.md` so a Claude Code session opened there knows the rules
- `/review` and `/feedback` commands for Claude Code

Then, inside the new folder:

```sh
python build.py      # render every format
python check.py      # mechanical review; exit 1 means something breaks the build
```

Outputs land in `_output/` (article, datasheet) or `_book/` (book).

## 3. Working with Claude Code

Open a **new session in the project folder** and say what you want, e.g.
*"Read CLAUDE.md, then turn the files in incoming/ into a book"* or
*"Fill in the electrical characteristics from this spec sheet."* The
folder's CLAUDE.md gives Claude the build commands, the traps, and the
authorship boundary below.

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
# in the book folder, after `python new.py book ../my-book`
python scripts/ingest.py   # first run creates incoming/: drop the author's
                           # .docx/.odt/.rtf/.txt/.md there, prefixed 01_, 02_, …
python scripts/ingest.py   # one chapter per file in chapters/, images to figures/media/
```

Paste the chapter list ingest prints into `_quarto.yml`, set the title and
author there, and delete the placeholder chapters. Then the editorial work,
yours or Claude's:

- split long Word files into real chapters; give each a `# Title`
- give figures captions and `fig-alt` text (needed for ebooks sold in the EU)
- add cross-references (`@sec-…`, `@fig-…`), index entries (`\index{…}`),
  and citations (`references.bib` + `[@key]`) if the book wants them

`python build.py --ingram` adds the PDF/X-1a CMYK interior IngramSpark
requires (needs Ghostscript). Specs, pricing, and the upload checklist:
[PUBLISHING.md](PUBLISHING.md).

## The author's loop (once writing starts)

```
write → git commit → python check.py        # mechanical: spelling, refs, glyphs, markers
                   → /review (in Claude Code) # judgment: grammar in context, style, structure
                   → fix what's flagged → commit → repeat
```

- `check.py` findings persist until fixed. Add it to CI to gate pushes.
- `/review` reviews what changed since the last review, leaves
  `TODO(review)` markers at the exact spots, and stores the full write-up in
  `tool_output/review-*.md`. The markers show up in every `check.py` run
  until resolved.
- `tool_output/` is machine-owned and gitignored; git history is the record
  of what the author actually changed.

**When reviewers come back** (marked-up PDFs, Word comments, email):

```
feedback/r1-<name>/  ← drop whatever each reviewer sent
python scripts/extract_feedback.py feedback/r1-<name>/   # annotations → extracted.md
/feedback feedback/r1-<name>   (in Claude Code)          # triage together, decide, route
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
