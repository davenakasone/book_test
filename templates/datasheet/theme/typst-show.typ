#show: doc => datasheet(
$if(title)$
  title: [$title$],
$endif$
$if(subtitle)$
  subtitle: [$subtitle$],
$endif$
$if(company)$
  company: [$company$],
$endif$
$if(doc-number)$
  doc-number: [$doc-number$],
$endif$
$if(revision)$
  revision: [$revision$],
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
  font: ("$mainfont$",),
$endif$
$if(fontsize)$
  fontsize: $fontsize$,
$endif$
$if(lang)$
  lang: "$lang$",
$endif$
$if(section-numbering)$
  sectionnumbering: "$section-numbering$",
$endif$
  doc,
)
