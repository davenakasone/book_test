# NOTES — what worked, what fought back (2026-07-02 first pass)

The point of the test book. Ordered by how much time each lesson would save
the friend.

## Traps hit (so the friend doesn't)

1. **Graphviz/Mermaid code blocks stall the render.** Quarto's `{dot}`
   engine wants headless Chromium; without it the render hangs *silently
   on a network socket* (killed ours after 20 min). Wrapping the block in
   html-only conditional content does NOT dodge it — diagram engines run
   before visibility filtering. **Rule: pre-render every diagram** (TikZ
   standalone → PDF, `sips` → PNG; or matplotlib) and include as images.
   Deterministic, offline, works in every format.
2. **Unicode superscripts silently lose glyphs in the PDF.** `10¹⁷` came
   out as `10¹` — Latin Modern has ¹²³ (Latin-1) but not ⁴⁻⁹ (U+2074+),
   and the missing-glyph warning drowns in the log. **Rule: write inline
   math** `$10^{17}$` — pandoc emits `<sup>` for EPUB/HTML automatically.
3. **`quarto render --to pdf` wipes the other formats from `_book/`.**
   One plain `quarto render` builds all formats side by side. Single-format
   renders are for debugging only.
4. **`cover-image` belongs at `book:` level**, not under `format: epub:`.
   And pandoc renames embedded media (`file5.png`) — verify the cover via
   the OPF manifest (`properties="cover-image"`), not by filename.
5. **matplotlib `ax.axis("off")` hides the background patch** — a dark
   cover came out white. Paint an explicit full-bleed Rectangle.
6. **Generate figures BEFORE rendering** — EPUB embeds images at render
   time; a stale PNG ships silently.
7. **Long author strings clip on the PDF title page** — `\maketitle`
   sets authors in a no-wrap tabular. And in book projects, `book.author`
   beats `format: pdf: author:`, so per-format overrides don't rescue
   you. Fix: trim the byline + `\setkomafont{author}{\large}` in the
   preamble. (Discovered giving the author ten credentials.)
8. TinyTeX's `latexmk` flaked once on the memoir build (no log written);
   direct `pdflatex` twice worked. Shrug, but worth knowing.
9. **`pip install quarto-cli` can fail on a network blip** (CI, 2026-09-27,
   run 36340674141). The PyPI package is a 4.6 kB sdist that downloads the
   Quarto binary from GitHub while it builds, so an empty download fails
   the whole `pip install -r requirements.txt` with `ValueError: nothing
   to open` / `Failed building wheel for quarto-cli`. Nothing is wrong with
   the commit: `gh run rerun <id> --failed` went green. If it recurs, give
   setup-python `cache: pip` so the built wheel is reused.

## What just worked (better than expected)

- **pip-installed quarto-cli** (`~/dkn314/bin/quarto`, v1.9.38) — dodged
  the brew-cask sudo prompt entirely. TinyTeX (~150 MB) into
  `~/Library/TinyTeX`, no root anywhere.
- **TinyTeX auto-installs missing LaTeX packages** during render — zero
  manual tlmgr.
- **The index**: raw `\index{...}` in .qmd + `imakeidx` in preamble →
  quarto's engine loop ran makeindex unprompted. Two-column sorted index
  with subentries, PDF-only (EPUB/HTML ignore it cleanly — they have
  search).
- **Citations**: BibTeX file + `[@key]` → author-year in text, all
  formats. *Correction (2026-09-26):* there was no "auto References
  chapter". Without a `references.qmd` holding `::: {#refs}`, the list is
  appended to the last chapter with no heading; in this book it ran into
  Appendix C. Fixed by adding `references.qmd`.
- **Cross-refs** (`@fig- @tbl- @eq- @sec-`): numbered + hyperlinked in
  all formats.
- **Callout boxes** render as tcolorbox in PDF, styled divs in EPUB/HTML.
- **TikZ → `sips`** (macOS built-in) for PDF→PNG spared us ghostscript/
  imagemagick installs.
- 6×9 PDF (90pp at v1.4) + valid EPUB3 (mimetype stored-first, cover
  flagged in OPF) + searchable HTML site from one `quarto render`, ~90 s
  warm. (Page/chapter counts live in CLAUDE.md STATUS — the one place they
  should be hardcoded; don't re-quote them across docs.)

## Shootout: Quarto PDF vs hand-rolled memoir

Same chapter both ways (`parked/latex-shootout/build/giza-memoir.pdf`):

| | Quarto default (scrbook) | memoir hand-set |
|---|---|---|
| Look | clean, competent, "tech book" | *book* book: drop cap, epigraph, margin notes, custom opener |
| Effort | markdown only | raw LaTeX, layout debugging |
| Formats | PDF+EPUB+HTML same source | PDF only |
| Friend-usable | yes | only if the friend learns LaTeX |

**Verdict:** write in Quarto. If the print interior must get fancy later,
graft memoir-style typography into Quarto via `template-partials` /
`include-in-header` — same source, upgraded page. Or pay Vellum $249 for
the look with zero effort (see parked/PUBLISHING.md).

## Windows-portability pass (2026-07-02)

The pipeline was born on macOS; two Unix-isms had crept in and are now
gone, so a Windows (or Linux) collaborator can build everything:

- `sips` (macOS-only) rasterized the TikZ PDF → replaced by
  `scripts/build_tikz.py` using **pymupdf** — one rasterizer, all OSes.
- `parked/latex-shootout/build.sh` (shell + hardcoded mac TinyTeX path) →
  `build.py`, which finds TeX via PATH then TinyTeX's per-OS locations.
  It runs pdflatex twice instead of latexmk: **TinyTeX on Windows ships
  no perl, and latexmk is a perl script.**
- `.gitattributes` pins line endings (`* text=auto`, LF for `.sh`) so
  CRLF checkouts don't dirty `.qmd`/`.tex` diffs.
- `requirements.txt` covers the whole Python side, including quarto-cli
  itself (`pip install quarto-cli` works on Windows too — no admin).

**What this pass missed: text encoding (found 2026-09-27 by another
session's fresh-clone Windows run).** It was a code read, not a Windows
run, and CI is ubuntu-only, so "any OS" was never tested. Every
`read_text()`/`write_text()`/`open()` used the locale encoding, which is
cp1252 on Windows:

- the prose-unicode guard **crashed** on `10¹⁷` (`⁷` is UTF-8 `e2 81 b7`,
  and cp1252 leaves 0x81 undefined) and was **blind** to `↔` (mojibake);
- `→` progress lines crashed any piped or redirected run
  (`UnicodeEncodeError`), which is how agents run tools;
- check.py would crash writing a report that quotes `Ω`;
- `postrender-fix-epub.py` printed the EPUB name, so a book titled in
  Greek or CJK failed `quarto render` (found by the guard below, not the
  report).

Fix: `encoding="utf-8"` on every text read, write, and subprocess
capture; every tool's `main()` reconfigures stdout to UTF-8. **Guard:**
CI's lint and templates jobs set `PYTHONWARNDEFAULTENCODING=1`,
`PYTHONWARNINGS=error::EncodingWarning:__main__`, and
`PYTHONIOENCODING=cp1252`. That makes a missing `encoding=` fatal and gives
stdout the encoding of a Windows pipe, so both failure classes reproduce on
Linux or macOS. Before the fix, both reproduced locally on
`build.py --check-only`.

## One-command build + CI (2026-07-04)

- **`build.py`** at repo root — one command runs figures → TikZ → `quarto
  render` (all formats) → refreshes the root download PDF. Flags:
  `--skip-figures`, `--shootout`. Finds quarto via PATH or the pip sibling.
- **`.github/workflows/build-book.yml`** — renders on every push, runs
  `epubcheck` (Java is free on the runner, so the deferred local check
  finally happens), uploads PDF+EPUB as a downloadable artifact per commit.
  This also proves a clean-machine build (catches "works on my Mac" drift).

## Accessibility (EAA, June 2025) — WIRED 2026-07-04

Ebooks sold into the EU must meet accessibility rules; our wide path
(D2D → Apple/Kobo) hits the EU. Done:
- **alt text** via `fig-alt="…"` on all six figures — verified as `alt`
  attributes in the EPUB, and doubles as HTML SEO. (Templating rule: every
  new image needs `fig-alt`.)
- **schema.org accessibility metadata** in `book/epub-metadata.xml` (wired
  via `_quarto.yml: epub: epub-metadata:`) — verified in the OPF
  (accessMode, accessibilityFeature: alternativeText/tableOfContents/…,
  hazard none).
- **Trap (found by CI):** Quarto's `fig-alt` writes alt onto the `<img>`
  (correct) but *also* onto the wrapping `<div>` — illegal in XHTML, so
  epubcheck fails RSC-005. And the obvious fix, a plain `alt=` attribute,
  gets silently DROPPED by pandoc (leaving `alt=""` = "decorative" —
  validates, but wrong for accessibility). Resolution: keep `fig-alt` +
  `book/postrender-fix-epub.py` (a Quarto post-render hook) strips the div
  copies while preserving EPUB zip invariants. Runs on every render,
  including CI.
- Still manual: **DAISY ACE** validation (CI runs epubcheck; ACE is a
  separate check). Microenterprise-exemption question unsettled — verify.

## PDF/X-1a for IngramSpark — WIRED 2026-07-04

`python build.py --ingram` → `scripts/make_pdfx.py` runs Ghostscript to
convert the RGB PDF → conforming **PDF/X-1a:2001 + CMYK** at
`book/_book/*-PDFX.pdf`. gs outlines text + flattens transparency (required
by PDF/X-1a), so the file is ~30 MB and not searchable — correct for a
print interior. The script locates gs and its CMYK ICC profile
version-agnostically. Needs `brew install ghostscript`. Ingram's uploader
does the final preflight.

## Deferred / untested

- Print *cover wrap* (back+spine+front single PDF) — needs final page
  count first; Inkscape job.
- Fonts beyond Latin Modern (EB Garamond etc. via `mainfont` + TinyTeX
  font package — one-line change, untested).
- KDP upload dry-run.

## Document toolkit: articles + datasheets via Typst (2026-09-26)

`new.py` + `templates/` turned the book pipeline into a toolkit. Typst
(bundled with quarto-cli, 0.14.2) renders the article and datasheet PDFs:
no LaTeX install, sub-second compiles. What fought back:

- **Custom Typst page designs = two template partials.** `_quarto.yml`
  `format: typst: template-partials: [theme/typst-template.typ,
  theme/typst-show.typ]`; the first defines the page function, the second
  maps front matter onto it. Quarto's own copies (a good starting point)
  are in `quarto_cli/share/formats/typst/pandoc/quarto/`.
- **Don't name a Typst variable `left`/`right`/`center`**: it shadows the
  alignment, and `align(left)` then fails with "expected content, found
  array".
- **Page counters need `context`.** `counter(page).display()` inside a
  plain `let` block fails; make the footer a function and call it as
  `footer: context footer-line()`.
- **Pandoc escapes `#` in front-matter values** (`"#1f4e79"` arrives as
  `\#1f4e79`), so `rgb("$accent$")` fails "non-hexadecimal letters". Strip
  it: `rgb("$accent$".replace("\\", ""))`.
- **Font fallback lists warn once per missing family** ("unknown font
  family"). Use one `mainfont` the user can see and change in
  `_quarto.yml` rather than a hidden list in the theme.
- **Typst's bibliography titles itself "Bibliography".** A manual
  `# References` + `::: {#refs}` gives two headings. Set the title in the
  header instead: `include-in-header: text: '#set bibliography(title:
  "References")'`; for Word, `reference-section-title: References`.
- **Plots as SVG with live text** (`svg.fonttype: none`,
  `svg.hashsalt` fixed): small, diffable, crisp. Avoid mathtext tick
  labels (`10⁻²`); Typst's SVG renderer spaces them badly. Format ticks
  as plain decimals.
- **SVG in Word** embeds fine (Office 2016+), but pandoc warns it can't
  make the PNG fallback without `rsvg-convert`. LaTeX PDFs *need*
  `rsvg-convert` for SVG, so book figures stay PNG/PDF.
- **A default-type Quarto project renders every .md/.qmd in the folder**,
  README and CLAUDE.md included. Templates pin `project: render:` to the
  one document.
- **The pre-commit fence blocks PNGs** in David's repos, one more reason
  template figures are SVG (text) or generated at build time from CSV.

## Code apart from documents (2026-09-27)

The tools stay in the toolkit; a job names raw content (`--from`, read
only), a project folder, and an output folder (`--out`). Choices that
aren't obvious from the code:

- **`--out` copies; it doesn't pass `quarto render --output-dir`.** Quarto
  cleans its output dir on a full project render, so pointing it at a
  folder someone else uses could delete their files. Render in the
  project, then copy: documents to the top, the web version to `html/`.
- **The EPUB fix moved from a `post-render:` hook to `build.py`.** A hook
  needs a script inside the project; now projects hold no code except
  their own `scripts/make_figures.py`. Cost: plain `quarto render` makes
  an EPUB that fails epubcheck (div `alt`); build with `build.py`.
- **Projects made before this change carry their own tool copies** and
  still build with them; `python build.py <old-project>` also works (the
  EPUB fix is idempotent, so the old hook plus the new pass is harmless).
- **Legacy raw files:** ingest reads `.txt`/`.md` as UTF-8 (BOM stripped),
  falling back to cp1252, the "ANSI" old Windows Notepad writes.
- **CI trap:** under `set -e`, `! cmd` never fails a step (bash exempts
  inverted commands from errexit). Negative checks are written
  `if cmd; then exit 1; fi`.

## Report kind: what sibling documents need (2026-09-27)

A crawl of the claude_stuff sibling projects found every human-read document
built by hand: seven reportlab or matplotlib scripts, 9,025 lines in all
(`wc -l`; that counts their map and analysis code too, not only layout) (trip packets, a decision packet, family
guides, an action plan, a 57-page bilingual review). They share one shape:
numbers from a model script, figures from the owner's code, and prose laid
out line by line. The `report` kind is that shape in Quarto: prose in
Markdown, numbers through `_variables.yml` (`{{< var >}}`, written by the
project's `scripts/make_figures.py`), tables from CSV as `{{< include >}}`
files, callouts, full-page figures, phone-sized pages, and a CJK font.

Traps hit building it:

- **A Typst `set` inside an `if` block ends with the block.** The custom
  page size did nothing until it moved into the one `set page(..)` call as
  spread arguments (`..if custom { (width: w, height: h) }`).
- **Quarto owns some front-matter names.** `page-width` is Quarto's own
  option (docx/html), so it never reached the Typst template; `page-height`
  did. Custom template variables need names Quarto doesn't use
  (`paper-width`, `paper-height`). Check `keep-typ: true` output when a
  variable seems ignored.
- **Typst's last-resort fallback hides missing glyphs.** Without a listed
  font for them, Japanese came out in a Chinese face (STSong) and ☐ came
  out as Apple's LastResort placeholder box, with no build warning. Fixes:
  the theme lists DejaVu Sans Mono (bundled) for symbols and takes
  `cjk-font:`; `build.py` now warns when a PDF embeds LastResort.
- **Listing absent fonts is noisy.** A fallback list naming fonts for every
  OS prints "unknown font family" for each missing one on every build; the
  theme names only bundled fonts plus the one the author chooses.
- **CJK embedding: Typst gets it right, matplotlib didn't.** matplotlib
  embeds macOS Hiragino as "CID Type 0C (OT)", which only Preview/poppler
  draw (a sibling converted the fonts to TrueType to work around it).
  Typst embeds bare CFF ("CID Type 0C" in `pdffonts`), and pdf.js renders
  it correctly. Not yet opened in Chrome itself: the Browser pane downloads
  PDFs instead of showing them.
- **Fixed-height full-page figures overflow phone pages.** `height=7.5in`
  spilled off a 4.5×8 in page; `height=75%` is a share of the page body and
  fits both letter and phone.

## First reproduction: a map-heavy trip packet (2026-09-27)

A sibling's 6-page matplotlib trip packet, rebuilt as a `report` project in
scratch space (its content stays out of this repo). The owner's analysis
and maps stayed the owner's; the report read an export (numbers JSON, table
CSV, map images) and owned the prose, tables, and a chart.

- **Score: not a line-count win.** The hand-rolled layout was 71 lines of
  pure layout (241 counting two mixed page functions); the report took
  140 lines of qmd + 275 of `make_figures.py`, plus a 119-line export
  prototype the owner would adopt. The wins: every number from the model
  (the original hard-coded its tide and daylight tables as strings), real
  text at 10 pt instead of 6-7 pt, HTML and Word for free, the plan's
  Markdown tables and bullets kept instead of stripped, and 1.8 MB instead
  of 3.7 MB. Costs: the page-1 map prints 5.6 in square instead of 8.2 in,
  and 8 pages instead of 6.
- **Letter margins cap a map at 6.8 in.** Added `page-margin:` to the
  report template (0.5 in gives 7.5 in).
- **Rasterized maps lose their labels as text.** Fixed with PDF maps and
  extension-less image paths (template README, "Maps with labels").
- **A table cell starting with `+ ` becomes a list** ("1." in the PDF).
  Don't lead a cell with `+`, `-`, or `1.`.
- **Subfigure widths:** a figure div with `layout="[[56,44]]"` stacked its
  two panels in Typst; `layout-ncol=2` put them side by side. A plain div
  (image + table) with `layout="[[35,65]]"` worked.
- **`check.py` read a link inside an image caption as the image path**
  (false BREAK); it now allows one level of brackets in a caption and
  resolves extension-less image paths.
- **A `bbox_inches` crop doesn't remove anything from a PDF.** My map
  crops kept the off-crop legend and tide text (ROUTES, TIDES, LIGHT) in
  the content stream, outside the page. Page-clipped extraction
  (pdftotext, PyMuPDF's default) misses it, so my first check said "clean";
  `get_text(clip=fitz.INFINITE_RECT())` finds it. The owner's session caught
  it; the fix is hiding the other axes before saving.
- **Double rounding in an export shows.** Rounding to 3 decimals and then
  printing `:.1f` turned 66.25 into 66.2 where the original said 66.3.
  Exports carry full precision; the report rounds once.
- **Tide hi/lo from 6-minute predictions:** a parabola through the peak
  sample and its neighbours recovers NOAA's high/low times to the minute
  and heights to 0.1 ft (all 8 times and 7 heights the original printed);
  take the first sample of a tie.


## Phone version and the source mark (2026-09-28)

One report source now builds a letter PDF and a phone PDF, and every PDF
built here says so in its metadata (David, 2026-09-28: stop PDFs with no
tooling behind them).

- **Variants are Quarto profiles.** `build.py` renders each
  `_quarto-<name>.yml` with `quarto render --profile <name> --to typst
  --output-dir <temp dir>` (an absolute path outside the project works), so
  the main render in `_output/` is untouched, then moves each PDF back as
  `<stem>-<name>.pdf`. LaTeX books go the same way with `--to pdf`: a
  `_quarto-large.yml` with `fontsize: 14pt` took body text from 10.9 to
  14.3 pt. Per-variant content: `.content-hidden when-profile="phone"`.
- **A captioned table never breaks across pages in Typst.** Quarto wraps it
  in a figure, and figures don't break, so on a 4.5 x 8 in page a long
  table ran over the footer. The theme now lets a table break only when it
  is taller than the page body (a shorter one still moves to the next page
  whole, as before). Decide that inside `context`, not `layout`: content
  inside `layout` never breaks, whatever the block says (tried; the table
  still ran off).
- **A picture sized by height gets cropped on a narrow page.** Typst gives
  it the full text width and crops the sides (image `fit` defaults to
  "cover"), and `measure()` reports the cropped width, so the theme compares
  the picture's natural aspect ratio with the text width and, when it is
  too wide, rebuilds it sized by width.
- **Hyphenation in tables fixed the phone and moved the letter.** Words
  wider than a narrow column spilled into the next cell; `hyphenate: true`
  fixed that but changed three letter pages, so it is on for small pages
  only.
- **Proof on a real document:** a sibling's map-heavy trip packet (a copy
  in scratch space). With all theme changes, its letter PDF is
  pixel-identical to the owner's build at 40 dpi, all 8 pages; the phone
  PDF is 14 pages at 4.5 x 8 in, whole maps, tables breaking with repeated
  headers.
- **Theme fixes don't reach existing projects on their own.** Typography
  is per-project config, so a report project made before this copies the
  new `theme/typst-template.typ` from `templates/report/` to get them.
- **The mark:** PyMuPDF `set_metadata` + `saveIncr()`; Creator becomes
  `doc_writer (<project folder name>) via <engine>`. No paths.
- **`scripts/pdf_census.py`:** first run over the sibling projects: 80 PDFs,
  24 built, 10 hand-laid (2 of them doc_writer builds from before the mark),
  5 figures, 41 received. Heuristics that mattered: match `TeX`
  case-sensitively (a bank-statement producer is "OpenText"); a PDF printed
  from a regular Chrome window is a saved web page (received), headless
  Chrome is a script (hand-laid); a one-page matplotlib PDF is a figure.
