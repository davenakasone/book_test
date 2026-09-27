# doc_writer — Markdown to books, papers, and datasheets, free and open source

Write in Markdown; get publication-grade output. One command builds
print-ready PDFs, ebooks, websites, and Word files through
[Quarto](https://quarto.org). The tooling costs nothing, needs no admin
rights, and runs on macOS, Linux, and Windows.

| Kind | You get | PDF engine |
|---|---|---|
| **book** | 6×9" print PDF with index and citations, EPUB3 ebook, HTML site, PDF/X-1a for commercial print | LaTeX |
| **article** | paper, report, or white paper: PDF, HTML, Word; authors, abstract, citations, cross-references | Typst |
| **datasheet** | product datasheet: title band, spec tables, curves plotted from your CSV data, PRELIMINARY watermark | Typst |

## Quick start

The tools stay in this folder. Your document lives wherever you like, and
the finished files go wherever you say:

```sh
git clone https://github.com/davenakasone/doc_writer && cd doc_writer
python -m pip install -r requirements.txt    # quarto, matplotlib, pymupdf, codespell (pinned)
python build.py --doctor                     # checks what's installed and what each tool is for

python new.py book ../my-book --title "My Book" --from ../manuscript   # the author's .docx/.md files
python build.py ../my-book --out ../deliverables                        # → PDF, EPUB, html/
python check.py ../my-book                                              # mechanical review
```

Here `python` means your Python 3: use `python3` on macOS/Linux if `python` isn't found, `py` on Windows.

Three places, kept apart:

| Place | What it holds | Who writes it |
|---|---|---|
| raw content (`--from`) | the author's original files | nobody: only read |
| project folder | the document as Markdown, figures, settings, review reports | the author (and tools that scaffold) |
| output (`--out`) | the finished PDF, EPUB, Word, and web version | `build.py`, which adds and overwrites but never deletes |

`python new.py --list` shows the kinds; articles and datasheets start
from placeholder content (`--from` is books-only so far). A project holds
no copies of the tools, so a fix here reaches every project on the next
build. Books also need LaTeX once: `quarto install tinytex` (about 150 MB,
no admin rights).

**Using Claude Code?** Open a session in this folder and say where the raw
content is and where the output goes. The project's `CLAUDE.md` carries
the traps and one firm rule: the author writes the words, and anything the
tool drafts stays marked until the author replaces it.

## What the toolkit does

- `build.py PROJECT`: figures, then render every format, in one command.
  `--out DIR` copies the finished documents out. `--doctor` reports missing
  tools. `--ingram` makes the PDF/X-1a CMYK file IngramSpark requires.
- `check.py`: a mechanical review that recommends and never edits. It
  checks broken cross-references and citations, missing images, missing
  alt text, spelling, repeated words, glyphs that vanish in LaTeX PDFs, and
  unresolved TODO markers. Reports go to the project's `tool_output/`; exits 1 on
  anything that breaks the build, so it can gate CI.
- `/review` and `/feedback` (Claude Code commands): prose review stored as
  markers the checker nags about, and triage of what reviewers send back
  (marked-up PDFs, Word comments, email) via `scripts/extract_feedback.py`.
- `scripts/ingest.py`: turns an author's `.docx`/`.txt`/`.md` files into
  book chapters (`new.py --from` runs it for you).

Full runbook: **[START-HERE.md](START-HERE.md)**. Every trap already hit:
**[NOTES.md](NOTES.md)**. Publishing (KDP, IngramSpark, Draft2Digital
specs, the money reality, the author-platform kit) is parked for now:
**[parked/](parked/README.md)**.

## The demo book: *The Starlight Engine*

*How the Ancients Wired the Earth*, by **Dr. Chocolate Daddy**, PhD
(pending), MD, DDS, PPM, PSI, MBA, Esq., HVAC, AM/FM, Notary Public
(revoked).

> **This is a work of satirical fiction.** Every factual claim in the book
> is wrong. Some are wrong in ways that required real effort. Do not cite
> it. *Especially* do not cite it in a school paper.

The toolkit's test corpus: 21 chapters and 3 appendices of lovingly abused
math, physics, and archaeology (the Great Pyramid as a starlight-pumped
fusion reactor, Stonehenge as a 56-bit controller, a one-page proof of the
Riemann Hypothesis). It uses every book feature, so the pipeline breaks
here before it breaks on yours. It's an ordinary project that happens to
live in `book/`; `python build.py book` builds it.

**Just want to read it?** Every tagged version ships the PDF, EPUB, and
print PDF/X-1a on the
**[Releases](https://github.com/davenakasone/doc_writer/releases/latest)**
page:
[The-Starlight-Engine.pdf](https://github.com/davenakasone/doc_writer/releases/latest/download/The-Starlight-Engine.pdf).

## Layout

| Path | What |
|---|---|
| `new.py`, `build.py`, `check.py` | start, build, and check a project |
| `templates/` | the book, article, and datasheet starters |
| `scripts/` | ingest, EPUB fix, feedback extraction, TikZ, PDF/X |
| `book/` | the demo book (a project like any other) |
| `parked/` | publishing material, on hold: specs, economics, author-platform kit, LaTeX memoir comparison |

## License

Take it. The **toolkit** (scripts, config, templates) is **MIT**; the
**demo book** (prose, figures, cover) is **CC0 / public domain**. See
[LICENSE](LICENSE).
