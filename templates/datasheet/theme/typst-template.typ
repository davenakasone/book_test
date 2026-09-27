// Datasheet page design (Typst). Quarto slots this in as the
// `typst-template.typ` partial; `typst-show.typ` maps the front matter of
// datasheet.qmd onto these parameters. Change the look here, not in the .qmd.
//
// Layout: title band on page 1, running header on later pages, footer with
// doc number / revision / "Page X of Y", optional diagonal watermark
// (PRELIMINARY, TEMPLATE, ...), compact spec tables with a shaded header row.

#let datasheet(
  title: none,          // part number, e.g. "XR-1000"
  subtitle: none,       // one-line description
  company: none,
  doc-number: none,
  revision: none,
  date: none,
  watermark: none,      // e.g. "PRELIMINARY"; none for production documents
  accent: rgb("#1f4e79"),
  font: none,
  fontsize: 9pt,
  lang: "en",
  region: "US",
  sectionnumbering: "1.1",
  doc,
) = {
  set document(title: title)
  set text(lang: lang, region: region, size: fontsize)
  set text(font: font) if font != none
  set par(justify: true, leading: 0.55em, spacing: 0.9em)

  let footer-line() = {
    set text(size: 7pt, fill: luma(35%))
    let ident = (doc-number, if revision != none [Rev. #revision]).filter(x => x != none)
    grid(
      columns: (1fr, auto, 1fr),
      align(left)[#ident.join([ · ])],
      align(center)[#company],
      align(right)[Page #counter(page).display() of #counter(page).final().first()],
    )
  }

  set page(
    margin: (x: 0.7in, top: 0.85in, bottom: 0.75in),
    header: context {
      if here().page() > 1 {
        set text(size: 7.5pt)
        grid(
          columns: (auto, 1fr),
          text(weight: "bold", fill: accent)[#title],
          align(right)[#subtitle],
        )
        v(-0.5em)
        line(length: 100%, stroke: 0.5pt + accent)
      }
    },
    footer: context footer-line(),
    background: if watermark != none {
      place(center + horizon, rotate(-40deg,
        text(size: 72pt, weight: "bold", fill: rgb(200, 30, 30, 28))[#watermark]))
    },
  )

  // Headings: numbered, accent-colored, rule under level 1.
  set heading(numbering: sectionnumbering)
  show heading: set text(fill: accent)
  show heading.where(level: 1): it => block(above: 1.4em, below: 0.7em, width: 100%)[
    #set text(size: 11pt, weight: "bold")
    #it
    #v(-0.6em)
    #line(length: 100%, stroke: 0.6pt + accent)
  ]
  show heading.where(level: 2): set text(size: 9.5pt, weight: "bold")

  // Spec tables: small type, hairline grid, shaded header row.
  show table: set text(size: 7.5pt)
  show table.cell.where(y: 0): set text(weight: "bold")
  set table(
    inset: (x: 4pt, y: 3.5pt),
    stroke: 0.4pt + luma(60%),
    fill: (_, y) => if y == 0 { accent.lighten(85%) },
  )
  show figure.caption: set text(size: 8pt, weight: "bold")

  // Page-1 title band.
  block(width: 100%, below: 1.2em)[
    #grid(
      columns: (1fr, auto),
      align(left + bottom)[
        #text(size: 8pt, weight: "bold", fill: accent)[#company] \
        #text(size: 26pt, weight: "bold")[#title]
      ],
      align(right + bottom)[
        #set text(size: 8pt)
        #doc-number #if revision != none [· Rev. #revision] \
        #date
      ],
    )
    #v(-0.4em)
    #line(length: 100%, stroke: 2pt + accent)
    #v(-0.2em)
    #text(size: 13pt, weight: "semibold")[#subtitle]
  ]

  doc
}
