#show: doc => report(
$if(title)$
  title: [$title$],
$endif$
$if(subtitle)$
  subtitle: [$subtitle$],
$endif$
$if(by-author)$
  authors: ($for(by-author)$[$it.name.literal$],$endfor$),
$endif$
$if(prepared-for)$
  prepared-for: [$prepared-for$],
$endif$
$if(version)$
  version: [$version$],
$endif$
$if(date)$
  date: [$date$],
$endif$
$if(watermark)$
  watermark: [$watermark$],
$endif$
$if(accent)$
  accent: rgb("$accent$".replace("\\", "")),   // pandoc escapes the #
$endif$
$if(mainfont)$
  font: "$mainfont$",
$endif$
$if(cjk-font)$
  cjk-font: "$cjk-font$",
$endif$
$if(fontsize)$
  fontsize: $fontsize$,
$endif$
$if(lang)$
  lang: "$lang$",
$endif$
$if(paper-width)$
  paper-width: $paper-width$,
$endif$
$if(paper-height)$
  paper-height: $paper-height$,
$endif$
$if(page-margin)$
  page-margin: $page-margin$,
$endif$
$if(section-numbering)$
  sectionnumbering: "$section-numbering$",
$endif$
  doc,
)
