# No binary `[[14,3,d≥5]]` quantum stabilizer code exists

This repository contains the authoritative LaTeX manuscript, its compiled PDF, and the exact computational record for the nonexistence proof. The result concerns binary qubit stabilizer codes, including degenerate codes; it makes no claim about non-stabilizer codes.

## Paper

- Source: [`paper/QEC1435_NO_BINARY_14_3_5.tex`](paper/QEC1435_NO_BINARY_14_3_5.tex)
- PDF: [`output/pdf/QEC1435_NO_BINARY_14_3_5.pdf`](output/pdf/QEC1435_NO_BINARY_14_3_5.pdf)

To rebuild the PDF, install Tectonic, Python 3.10 or newer, and Poppler (`pdfinfo`, `pdffonts`, and `pdftotext`), then run:

```sh
bash paper/build_pdf.sh
```

## Reproduce the proof

From a clone of this repository, run the standard exact replay at its root:

```sh
bash experiments/qec1435_replay_nonexistence.sh
```

The replay requires Python 3.10 or newer and Node.js. It verifies the signed-shadow identities, physical subgroup cosets, exact Farkas certificates, ten-site control cases, the 37 committed additive-code representatives, and their hull and coset-capacity audits. It uses the committed representatives and does not regenerate their exhaustive classification. Replay outputs are temporary; the committed certificate and representative data are not rewritten.

To reconstruct the length-ten classification, install the pinned optional dependency and run the census mode:

```sh
python3 -m pip install -r requirements-qec1435.txt
bash experiments/qec1435_replay_nonexistence.sh --census
```

The census mode performs the standard exact replay, then regenerates the classification using `pynauty==2.8.8.1`. Its generated representatives and audit output are temporary and do not replace the committed data.

[`VERIFICATION.md`](VERIFICATION.md) documents the proof replay, certificate locations, census recurrence, and verification limits. The pinned dependency is listed in [`requirements-qec1435.txt`](requirements-qec1435.txt).
