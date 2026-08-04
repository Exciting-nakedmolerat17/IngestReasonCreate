#set page(paper: "a4", margin: 24mm)
#set text(font: "Libertinus Serif", size: 10.5pt)
#set heading(numbering: "1.")

#let report(title: "Untitled report", body) = [
  #align(center)[
    #text(size: 22pt, weight: "bold")[#title]
  ]
  #v(8mm)
  #body
]

#show: report.with(title: "Report title")

= Executive summary

Replace this synthetic placeholder with source-grounded content in a private output workspace.
