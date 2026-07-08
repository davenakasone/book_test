# START HERE — turn your material into a book with this pipeline

This repo is **two things**: a finished satirical book (*The Starlight
Engine*), and a **reusable open-source pipeline** that takes raw material —
Word docs, text files, diagrams — and produces a print-ready PDF, an EPUB,
and a website. This page is for using it as a **template for your own book**.

## The short answer (the workflow)

1. **Copy this repo to a new folder** for the new book — don't work inside
   the demo:
   ```sh
   git clone https://github.com/davenakasone/book_test my-book && cd my-book
   rm -rf .git && git init          # start the new book's own history
   ```
2. **Put the author's material in `incoming/`** — any mix of `.docx`,
   `.odt`, `.rtf`, `.txt`, `.md`. Prefix filenames `01_`, `02_`, … to set
   chapter order. Drop diagrams/photos in too (or leave them embedded in
   the Word docs — ingest extracts them).
3. **Open a fresh Claude Code session in that folder** and say:
   *"Read START-HERE.md and CLAUDE.md, then turn the files in incoming/
   into a book."*
   Claude will run the ingest, split/clean chapters, wire up
   `_quarto.yml`, handle figures, and build. **Point it at this project's
   docs — that's exactly what they're written for.**

A new session in the new folder is the right call: the book's content stays
separate from this demo, and Claude gets a clean CLAUDE.md/STATUS to track
its own work.

## What the pipeline does vs. what a human/Claude does

**Automated:**
- `python scripts/ingest.py` — converts `incoming/*` → `book/chapters/NN-slug.qmd`
  via pandoc, extracts embedded images to `book/figures/media/`, prints the
  chapter list for `_quarto.yml`.
- `python build.py` — figures → render → **PDF + EPUB + HTML** in one shot.
- `python build.py --ingram` — also emits the **PDF/X-1a CMYK** interior for
  IngramSpark.

**Editorial (you or Claude, per chapter):**
- Split a long Word doc into real chapters; set each chapter's `# Title`.
- Give figures captions and **`fig-alt`** text (accessibility — required for
  EU sales; see the existing figures in `book/chapters/` for the pattern).
- Add cross-references (`@sec-…`, `@fig-…`), an index (`\index{…}`), and
  citations (`references.bib` + `[@key]`) if the book wants them.

**The authorship boundary (hard rule for any session working here):**
The tool and the session **scaffold; the author authors.** Ingest never
rewrites the author's words — but some pieces have no source (the preface
page Quarto requires, a cover tagline, a title derived from a filename).
When a session must draft such a piece, it marks it:

```
<!-- TODO: TOOL-DRAFTED, NOT AUTHOR-WRITTEN. <why it exists>. Replace
with your own words — check.py flags this file until the TODO is gone. -->
```

`python check.py` WARNs on every unresolved marker, so nothing tool-written
can silently ship in the author's voice. Corrections count too: if a
filename-derived title fixes the author's typo, *flag it, don't silently
"improve" it* — it's their book, including the mistakes they want.

## Step by step

```sh
# 0. one-time setup
python -m pip install -r requirements.txt
quarto install tinytex

# 1. drop the author's files in incoming/, then:
python scripts/ingest.py            # creates book/chapters/NN-*.qmd

# 2. edit _quarto.yml: set title/subtitle/author/date, and paste the
#    chapter list ingest printed (group into parts if you want).

# 3. build and look
python build.py                     # PDF + EPUB + HTML → book/_book/
open book/_book/The-Starlight-Engine.pdf   # (rename per your book)

# 4. when ready for print/wide distribution
python build.py --ingram            # adds the PDF/X-1a CMYK interior
```

## What to keep vs. replace when templating

| Keep (the pipeline) | Replace (the content) |
|---|---|
| `build.py`, `scripts/`, `latex-shootout/` | `book/chapters/*`, `book/index.qmd`, `book/frontmatter/*` |
| `book/_quarto.yml` **structure** (edit title/author/chapters) | title, author, date, cover image |
| `book/latex/`, `book/html/`, `book/epub-metadata.xml` | `book/references.bib` (your sources) |
| `.github/workflows/`, `requirements.txt`, `.gitattributes` | `book/figures/*` (your figures) |
| `CLAUDE.md` rules (update STATUS for the new book) | `README.md`, this file's book-specific bits |

## The author's loop (once writing starts)

```
write → git commit → python check.py      # mechanical: spelling, refs, glyphs, markers
                   → /review (in Claude Code)   # judgment: grammar-in-context, style, structure
                   → fix what's flagged → commit → repeat
```

- `check.py` findings persist until fixed; CI runs the same gate on push.
- `/review` (repo-local command in `.claude/commands/`) reviews what changed
  since the last review, leaves `TODO(review)` markers at the exact spots,
  and stores the full write-up in `tool_output/review-*.md`. The markers
  show up in every `check.py` run until resolved — advice can't evaporate.
- `tool_output/` is machine-owned and gitignored; git history is the log
  of what the author actually changed.

## Rename the outputs

The output filename comes from the book title in `_quarto.yml`
(`book-output-file` if set, else the title). Update the `cp` line's target in
`build.py` (`The-Starlight-Engine.pdf`) to match your book, or set
`book-output-file: my-book` in `_quarto.yml`.

## Where the knowledge lives

- **[CLAUDE.md](CLAUDE.md)** — build commands + the hard-won rules (unicode
  traps, no mermaid blocks, etc.). A fresh Claude session reads this first.
- **[NOTES.md](NOTES.md)** — every pipeline trap already hit, so you don't.
- **[PUBLISHING.md](PUBLISHING.md)** — KDP/IngramSpark/D2D specs, pricing,
  licensing, accessibility, the upload checklist.
- **[BUSINESS.md](BUSINESS.md)** — the blunt money reality before anyone
  spends on this: sales medians, unit economics, when it earns out.

## The honest expectation

Read **BUSINESS.md** before committing money. A first book rarely earns out
its production cost; this pipeline's value is that it makes book 2, 3, 4…
nearly free, so a *backlist* can compound. It's a book *factory*, cheap to
run — not a lottery ticket on one title.
