# No binary `[[14,3,d≥5]]` quantum stabilizer code exists

**Brandon Li · 2026 · Quantum error-correcting codes**

This repository contains the LaTeX manuscript and exact computational evidence for the claimed nonexistence of a binary `[[14,3,d≥5]]` qubit stabilizer code. The argument includes degenerate stabilizer codes, does not address non-stabilizer codes, and does not assume GF(4)-linearity.

## Manuscript

- [Read the paper (PDF)](output/pdf/QEC1435_NO_BINARY_14_3_5.pdf)
- [LaTeX source](paper/QEC1435_NO_BINARY_14_3_5.tex)

The proof derives signed-shadow constraints and exact Farkas certificates, reduces a hypothetical code to a ten-site additive code of binary dimension ten and symplectic hull dimension four, and excludes the 37 relevant additive-code classes by hull dimension or a necessary physical coset-capacity bound.

## Verify the computational evidence

From the repository root, run the standard exact replay (Python 3.10+, Node.js, and Git required):

```sh
bash experiments/qec1435_replay_nonexistence.sh
```

The replay checks the exact certificate arithmetic and audits the 37 committed length-ten representatives. It does not regenerate the exhaustive classification.

To regenerate the classification, install the pinned optional dependency and run census mode:

```sh
python3 -m pip install -r requirements-qec1435.txt
bash experiments/qec1435_replay_nonexistence.sh --census
```

The census uses `pynauty==2.8.8.1`. It writes generated representatives and audit output to a temporary directory; it does not replace committed data. The census was run during the final manuscript audit, but is not part of the standard replay.

[`VERIFICATION.md`](VERIFICATION.md) describes the checks, their limits, and the computational data map.

## Build the PDF

Requires Tectonic, Python 3.10+, and Poppler (`pdfinfo`, `pdffonts`, and `pdftotext`):

```sh
bash paper/build_pdf.sh
```

The build compiles the LaTeX source and checks PDF metadata, page count, link annotations, embedded fonts, and extractable text. It does not replace visual inspection or mathematical review.

## Repository contents

| Path | Purpose |
| --- | --- |
| `paper/` | LaTeX manuscript and PDF build/preflight scripts |
| `output/pdf/` | Compiled manuscript |
| `experiments/` | Exact verifiers, arithmetic audits, census generator, and certificate data |
| `requirements-qec1435.txt` | Pinned optional census dependency |
| `VERIFICATION.md` | Reproducibility scope and review boundary |

For citation details, see [`CITATION.cff`](CITATION.cff).
