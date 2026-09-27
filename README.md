# Markdown to books, papers, and datasheets — free and open source

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

```sh
git clone https://github.com/davenakasone/book_test && cd book_test
python -m pip install -r requirements.txt    # quarto, matplotlib, pymupdf, codespell (pinned)
python build.py --doctor                     # checks what's installed and what each tool is for

python new.py datasheet ../my-part --title "XR-2000"
cd ../my-part && python build.py             # → _output/datasheet.pdf
```

Here `python` means your Python 3: use `python3` on macOS/Linux if `python` isn't found, `py` on Windows.

`python new.py --list` shows the kinds. Each new folder is self-contained:
its own copy of the build and check tools, a README for that kind of
document, and placeholder content you replace. Books also need LaTeX once:
`quarto install tinytex` (about 150 MB, no admin rights).

**Using Claude Code?** Open a session in the new folder. Its `CLAUDE.md`
gives Claude the build commands, the traps, and one firm rule: the author
writes the words, and anything the tool drafts stays marked until the
author replaces it.

## What the toolkit does

- `build.py`: figures, then render every format, in one command. `--doctor`
  reports missing tools. `--ingram` makes the PDF/X-1a CMYK file
  IngramSpark requires.
- `check.py`: a mechanical review that recommends and never edits. It
  checks broken cross-references and citations, missing images, missing
  alt text, spelling, repeated words, glyphs that vanish in LaTeX PDFs, and
  unresolved TODO markers. Reports go to `tool_output/`; exits 1 on
  anything that breaks the build, so it can gate CI.
- `/review` and `/feedback` (Claude Code commands): prose review stored as
  markers the checker nags about, and triage of what reviewers send back
  (marked-up PDFs, Word comments, email) via `scripts/extract_feedback.py`.
- `scripts/ingest.py`: turns an author's `.docx`/`.txt`/`.md` files into
  book chapters.

Full runbook: **[START-HERE.md](START-HERE.md)**. Every trap already hit:
**[NOTES.md](NOTES.md)**. Publishing specs (KDP, IngramSpark, Draft2Digital):
**[PUBLISHING.md](PUBLISHING.md)**. The money reality:
**[BUSINESS.md](BUSINESS.md)**.

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
here before it breaks on yours. Source in `book/`; `python build.py`
builds it.

**Just want to read it?** Every tagged version ships the PDF, EPUB, and
print PDF/X-1a on the
**[Releases](https://github.com/davenakasone/book_test/releases/latest)**
page:
[The-Starlight-Engine.pdf](https://github.com/davenakasone/book_test/releases/latest/download/The-Starlight-Engine.pdf).

## Layout

| Path | What |
|---|---|
| `new.py`, `build.py`, `check.py` | start, build, and check a project |
| `templates/` | the book, article, and datasheet starters |
| `scripts/` | ingest, feedback extraction, TikZ, PDF/X, demo figures |
| `book/` | the demo book's source |
| `latex-shootout/` | demo chapter 1 hand-set in LaTeX memoir, for comparison |
| `platform/` | demo author-platform kit: email sequence, social playbooks, launch plan |

## License

Take it. The **toolkit** (scripts, config, templates) is **MIT**; the
**demo book** (prose, figures, cover) is **CC0 / public domain**. See
[LICENSE](LICENSE).
