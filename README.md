# No binary `[[14,3,d≥5]]` quantum stabilizer code exists

**Brandon Li · 2026 · Quantum error-correcting codes**

This repository contains the manuscript and exact computational evidence for the claimed nonexistence of a binary `[[14,3,d≥5]]` qubit stabilizer code. The argument includes degenerate stabilizer codes and does not address non-stabilizer quantum codes or assume GF(4)-linearity.

## Manuscript

- [Read the paper (PDF)](output/pdf/QEC1435_NO_BINARY_14_3_5.pdf)
- [LaTeX source](paper/QEC1435_NO_BINARY_14_3_5.tex)

The proof uses signed-shadow constraints and exact Farkas certificates to isolate a unique weight-four stabilizer; reduces a hypothetical code to a ten-site additive code with 1,024 words, distance at least five, and symplectic hull dimension four; and excludes all 37 relevant additive-code classes by hull dimension or a necessary physical coset-capacity bound.

## Verify the computational evidence

Run from the repository root with **Python 3.10+, Node.js, and Git**:

```sh
bash experiments/qec1435_replay_nonexistence.sh
```

This checks the integer identities, physical subgroup models, exact infeasibility certificates, committed length-ten generator matrices, hull dimensions, and Hall exclusions. It **does not regenerate the exhaustive 37-class census**.

To regenerate the census, install the pinned optional dependency and run:

```sh
python3 -m pip install -r requirements-qec1435.txt
bash experiments/qec1435_replay_nonexistence.sh --census
```

The census is substantially more computationally expensive and rewrites the tracked generator and class-audit JSON files. See [Verification scope](VERIFICATION.md) for what each check establishes and what still warrants external review.

## Build the PDF

Requires **Tectonic, Python 3, and Poppler** (`pdfinfo`, `pdffonts`, and `pdftotext`):

```sh
bash paper/build_pdf.sh
```

The build compiles the authoritative LaTeX source and checks the PDF's metadata, fonts, extractable text, and single ordinary GitHub repository link.

## Repository contents

| Path | Purpose |
| --- | --- |
| `paper/` | LaTeX manuscript and PDF build/preflight scripts |
| `output/pdf/` | Compiled manuscript |
| `experiments/` | Exact verifiers, independent arithmetic checks, census generator, and committed certificate data |
| `requirements-qec1435.txt` | Pinned optional dependency for full census regeneration |
| `VERIFICATION.md` | Reproducibility and independent-review boundary |

For citation details, see [CITATION.cff](CITATION.cff).
