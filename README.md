# Quantum Mechanics Notes

English rewrites of the supplied handwritten quantum mechanics notes, with editable TeX, searchable PDFs, and native vector diagrams.

All 81 supplied scan pages have a corresponding rewrite, covering note labels 5-84. Note 15 has two source sheets, labeled 15a and 15b here. Notes 13 and 76 are blank in the source and retain explicit placeholders. Notes 1-4 were not supplied.

## Reading order

| Notes | Topics | TeX entry point | PDF | Pages |
| --- | --- | --- | --- | ---: |
| 5 | Matrix elements of a linear operator | [Source](notes/005-matrix-elements/note.tex) | [Read](notes/005-matrix-elements/note.pdf) | 1 |
| 6-20 | Linear algebra, projections, adjoints, diagonalization, continuum bases, and the quantum postulates | [Source](notes/006-020-foundations/main.tex) | [Read](notes/006-020-foundations/main.pdf) | 16 |
| 21-41 | Measurements, translations, dynamics, parity, bound states, and the harmonic oscillator | [Source](notes/021-041-dynamics/main.tex) | [Read](notes/021-041-dynamics/main.pdf) | 21 |
| 42-63 | Rotations, angular momentum, hydrogen, virial relations, and spin | [Source](notes/042-063-angular-momentum/main.tex) | [Read](notes/042-063-angular-momentum/main.pdf) | 22 |
| 64-84 | Pauli matrices, magnetic moments, perturbation theory, selection rules, and scattering | [Source](notes/064-084-approximation-and-scattering/main.tex) | [Read](notes/064-084-approximation-and-scattering/main.pdf) | 21 |

Each PDF is stored beside its TeX entry point. Each source sheet also has its own TeX fragment. The [page index](INDEX.md) links every fragment and identifies its PDF page; [source-coverage.json](source-coverage.json) records the source-file and physical-page mapping.

## Editorial approach

The rewrites retain the supplied derivations, examples, exercises, and diagrams. English phrasing, notation, and layout are cleaned up. Clear source errors and necessary assumptions are identified in short inline **Clarification** notes; the [editorial index](EDITORIAL.md) summarizes the main changes.

This is a rewrite of the available material, rather than a claim to be a complete course or a new answer key. Proofs left as exercises in the source remain exercises. Unidentified textbook reading references are marked as such. The final source sheet ends during a Fourier-contour calculation; that endpoint is preserved explicitly.

The original scans and their annotation metadata are kept outside this repository. Published PDFs contain native text, equations, and vector diagrams, without embedded scan images. Author fields are anonymous. The previously reviewed note 5 is retained unchanged.

## Build from a fresh download

Install Python 3.10 or newer and a standard LaTeX distribution with pdfLaTeX, Latin Modern, AMS packages, mathtools, microtype, enumitem, booktabs, fancyhdr, hyperref, and TikZ. On Debian or Ubuntu, the relevant packages are:

```sh
sudo apt-get install texlive-latex-extra texlive-pictures texlive-fonts-recommended texlive-science texlive-plain-generic lmodern
```

From the repository root:

```sh
python tools/build.py
```

This compiles all five entry points twice and writes logs and PDFs to `.build/`. Use `--engine` to specify a full pdfLaTeX path, `--target 021-041` to build one part, or `--target remaining` to build the four continuation parts. Add `--publish` to copy generated PDFs beside their sources.

The build uses only Python's standard library. No source scans, external image assets, simulation software, or local file paths are required.

## Verify the archive

```sh
python -m pip install -r requirements.txt
python tools/verify_archive.py --pdf
python tools/verify_archive.py --pdf --built
```

The verifier checks source-sheet coverage, TeX dependencies, PDF page counts and note labels, anonymous metadata, absence of raster scans, and the published PDF checksums. `--built` checks the fresh build outputs as well. A GitHub Actions workflow runs the archive and build checks on Linux.
