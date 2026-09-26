# No binary `[[14,3,d≥5]]` quantum stabilizer code exists

Brandon Li · 2026

This repository contains the manuscript and computational materials for the nonexistence proof.

## Paper

- [PDF](output/pdf/No_Binary_14_3_5.pdf)
- [LaTeX source](paper/No_Binary_14_3_5.tex)

## Reproduce the computational checks

The standard replay requires Python 3.10 or newer, Node.js, and Git. From the repository root, run:

```sh
bash experiments/qec1435_replay_nonexistence.sh
```

This verifies the integer certificates and the 37 saved length-ten representatives. It does not regenerate the full classification.

To regenerate the classification, install the optional dependency and run:

```sh
python3 -m pip install -r requirements-qec1435.txt
bash experiments/qec1435_replay_nonexistence.sh --census
```

The census requires `pynauty==2.8.8.1`.

## Build the PDF

Requires Tectonic, Python 3.10 or newer, and Poppler (`pdfinfo`, `pdffonts`, and `pdftotext`):

```sh
bash paper/build_pdf.sh
```

For citation details, see [CITATION.cff](CITATION.cff).
