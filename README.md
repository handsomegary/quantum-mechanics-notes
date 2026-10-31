# Quantum Mechanics Notes

English rewrites of handwritten quantum mechanics notes, with editable TeX sources and searchable PDFs.

## Review sample

Only note 5 has been rewritten. The remaining notes are pending review of this sample.

| Note | Topic | Source | PDF |
| --- | --- | --- | --- |
| 5 | Section 1.6: Matrix Elements of a Linear Operator | [TeX](notes/005-matrix-elements/note.tex) | [Read](notes/005-matrix-elements/note.pdf) |

The sample preserves both basis expansions, the full double-sum derivation, the matrix representation, and the resolution of the identity. English phrasing and typography have been cleaned up. The completeness assumption is stated explicitly, the state label is consistently written as lowercase `v`, and a short explanation clarifies why the left coefficient column uses an ordinary transpose.

All text and equations in the PDF are typeset from TeX. The handwritten scan is kept outside this repository.

## Build

A standard LaTeX installation with pdfLaTeX, Latin Modern, and the packages listed in the source is sufficient. No images or other external assets are required.

```sh
cd notes/005-matrix-elements
pdflatex -halt-on-error -interaction=nonstopmode note.tex
pdflatex -halt-on-error -interaction=nonstopmode note.tex
```

The generated `note.pdf` is stored beside `note.tex`. Compilation logs and auxiliary files are excluded from version control.
