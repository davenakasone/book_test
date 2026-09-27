// Report page design (Typst): guides, plans, trip packets, playbooks.
// Quarto slots this in as the `typst-template.typ` partial; `typst-show.typ`
// maps the front matter of report.qmd onto these parameters. Change the look
// here, not in the .qmd.
//
// Layout: title band on page 1, running header on later pages, footer with
// version / date / "Page X of Y", optional diagonal watermark (DRAFT,
// TEMPLATE, ...). Ragged-right body text, easier to read than justified on
// a phone or for older readers. Page size is letter unless the front matter
// gives `paper-width` and `paper-height` (e.g. a phone-shaped PDF), and
// the margins shrink with it unless `page-margin` sets them.

#let report(
  title: none,
  subtitle: none,
  authors: (),          // names only; the title band lists them
  prepared-for: none,   // who reads it, e.g. "the hiking group"
  version: none,        // e.g. "v2" or a build stamp
  date: none,
  watermark: none,      // e.g. "DRAFT"; none for a finished document
  accent: rgb("#1f5f5b"),
  font: none,
  cjk-font: none,       // e.g. "Hiragino Sans" (macOS), "Noto Sans CJK JP" (Linux), "Yu Gothic" (Windows)
  fontsize: 11pt,
  lang: "en",
  region: "US",
  paper-width: none,     // both set: a custom page (e.g. 4.5in x 8in for phones)
  paper-height: none,
  page-margin: none,     // e.g. 0.5in: more room for maps; default depends on page size
  sectionnumbering: none,
  doc,
) = {
  set document(title: title)
  set text(lang: lang, region: region, size: fontsize)
  // The chosen font, then Typst's bundled fonts (the same on every OS):
  // Libertinus Serif for text, DejaVu Sans Mono for symbols it lacks (☐ ✓ →).
  // Japanese or Chinese: name the face in `cjk-font`. Without it Typst still
  // finds some installed CJK font, but it may be a Chinese face for Japanese.
  set text(font: (
    ..if font != none { (font,) },
    "Libertinus Serif",
    ..if cjk-font != none { (cjk-font,) },
    "DejaVu Sans Mono",
  ))
  set par(justify: false, leading: 0.65em, spacing: 1.1em)

  // (A `set` inside an `if` block would end with the block, so the custom
  // size goes into the one `set page` below as spread arguments.)
  let custom = paper-width != none and paper-height != none
  let small = custom and paper-width < 6in

  set page(
    ..if custom { (width: paper-width, height: paper-height) },
    margin: if page-margin != none { page-margin }
            else if small { (x: 0.4in, top: 0.6in, bottom: 0.55in) }
            else { (x: 0.85in, top: 0.9in, bottom: 0.8in) },
    header: context {
      if here().page() > 1 {
        set text(size: 0.72em, fill: luma(35%))
        grid(
          columns: (1fr, auto),
          text(weight: "bold", fill: accent)[#title],
          align(right)[#subtitle],
        )
        v(-0.5em)
        line(length: 100%, stroke: 0.5pt + accent)
      }
    },
    footer: context {
      set text(size: 0.68em, fill: luma(35%))
      let ident = (version, date).filter(x => x != none)
      grid(
        columns: (1fr, auto),
        align(left)[#ident.join([ · ])],
        align(right)[Page #counter(page).display() of #counter(page).final().first()],
      )
    },
    background: if watermark != none {
      place(center + horizon, rotate(-40deg,
        text(size: 64pt, weight: "bold", fill: rgb(200, 30, 30, 28))[#watermark]))
    },
  )

  set heading(numbering: sectionnumbering)
  show heading: set text(fill: accent)
  show heading.where(level: 1): it => block(above: 1.5em, below: 0.8em, width: 100%)[
    #set text(size: 1.3em, weight: "bold")
    #it
    #v(-0.6em)
    #line(length: 100%, stroke: 0.6pt + accent)
  ]
  show heading.where(level: 2): set text(size: 1.08em, weight: "bold")

  // Tables: hairline grid, shaded header row, a little smaller than body text.
  show table: set text(size: 0.9em)
  show table.cell.where(y: 0): set text(weight: "bold")
  set table(
    inset: (x: 5pt, y: 4pt),
    stroke: 0.4pt + luma(60%),
    fill: (_, y) => if y == 0 { accent.lighten(85%) },
  )
  show figure.caption: set text(size: 0.85em)

  // Page-1 title band.
  block(width: 100%, below: 1.4em)[
    #text(size: if small { 1.9em } else { 2.4em }, weight: "bold")[#title]
    #if subtitle != none {
      v(-0.4em)
      text(size: 1.2em, fill: luma(30%))[#subtitle]
    }
    #v(-0.3em)
    #line(length: 100%, stroke: 2pt + accent)
    #v(-0.3em)
    #set text(size: 0.85em, fill: luma(30%))
    #let meta = (
      if authors.len() > 0 { authors.join(", ") },
      if prepared-for != none [Prepared for #prepared-for],
      date,
    ).filter(x => x != none)
    #meta.join([ · ])
  ]

  doc
}
