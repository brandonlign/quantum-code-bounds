# No binary `[[14,3,d≥5]]` quantum stabilizer code exists

**Brandon Li · 2026 · Quantum error-correcting codes**

The authoritative manuscript is the PDF, titled *No binary `[[14,3,d≥5]]` quantum stabilizer code exists*, with subtitle *A signed-shadow proof and exhaustive additive-code classification*. Its scope is binary qubit stabilizer codes, including degenerate codes; it makes no claim about non-stabilizer codes.

The matching text input is retained only to rebuild the PDF in the same presentation. The mathematical results and section structure follow the PDF.

## Reproduce the proof

The paper's archived code snapshot is commit `c14d6dadf2c5f902d9c149ed992fbac54b63596e`. To reproduce that snapshot from a clean checkout:

```sh
git clone https://github.com/brandonlign/quantum-code-bounds.git
cd quantum-code-bounds
git checkout c14d6dadf2c5f902d9c149ed992fbac54b63596e
```

The default replay requires Python 3.10 or later and Node.js with ES modules and `BigInt`. From the repository root, run:

```sh
bash experiments/qec1435_replay_nonexistence.sh
```

This checks the exact signed-shadow identities, physical subgroup cosets, integer Farkas certificates, physical-lift controls, and the committed 37 additive-code representatives with their hull and Hall audits. It does not regenerate the exhaustive length-ten census.

To regenerate the full census, install the pinned dependency and run:

```sh
python3 -m pip install -r requirements-qec1435.txt
bash experiments/qec1435_replay_nonexistence.sh --census
```

The census uses nauty through `pynauty==2.8.8.1`. It regenerates the representative and class-audit JSON files. The census has one exhaustive implementation; the JavaScript checks independently audit the stored representatives and physical cosets but do not regenerate all equivalence classes.

## Rebuild the paper PDF

The PDF is rendered from `paper/QEC1435_NO_BINARY_14_3_5.source.md`. To rebuild and mechanically preflight it, install the pinned rendering dependency and Poppler utilities (`pdfinfo`, `pdffonts`, and `pdftotext`), then run:

```sh
python3 -m pip install -r requirements-qec1435.txt
bash paper/build_pdf.sh
```

`paper/test_math_rendering.py` checks the renderer’s equation, link, and pagination handling. The preflight checks the PDF metadata, fonts, extracted text, and its single pinned code-archive link.

## Repository map

| Location | Contents |
| --- | --- |
| `output/pdf/QEC1435_NO_BINARY_14_3_5.pdf` | Authoritative paper |
| `paper/QEC1435_NO_BINARY_14_3_5.source.md` | Synchronized input used to rebuild the paper’s presentation |
| `paper/build_nonexistence_pdf.py` | PDF renderer |
| `experiments/` | Exact certificate verifiers, census, generator representatives, and audit data |
| `research/` | Dated mathematical derivations and the current verification-boundary record |

The default replay and full census are distinct verification levels. The known review boundary, including the need for independent specialist review and a second exhaustive census implementation, is recorded in `research/UNRESOLVED_GAPS.md`.
