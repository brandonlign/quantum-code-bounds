# No binary `[[14,3,d≥5]]` quantum stabilizer code exists

Brandon Li · 2026 · Quantum error-correcting codes

The paper proves nonexistence for binary qubit stabilizer codes, including degenerate codes. It makes no claim about non-stabilizer codes.

## Paper

The LaTeX source is [`paper/QEC1435_NO_BINARY_14_3_5.tex`](paper/QEC1435_NO_BINARY_14_3_5.tex). The compiled paper is [`output/pdf/QEC1435_NO_BINARY_14_3_5.pdf`](output/pdf/QEC1435_NO_BINARY_14_3_5.pdf). Build it with Tectonic, Python 3, and Poppler (`pdfinfo`, `pdffonts`, and `pdftotext`):

```sh
bash paper/build_pdf.sh
```

The script compiles the `.tex` source and checks the PDF metadata, embedded fonts, extracted text, and single pinned code-archive link.

## Reproduce the proof

The paper points to the immutable repository snapshot at commit `c14d6dadf2c5f902d9c149ed992fbac54b63596e`. To check out that snapshot:

```sh
git clone https://github.com/brandonlign/quantum-code-bounds.git
cd quantum-code-bounds
git checkout c14d6dadf2c5f902d9c149ed992fbac54b63596e
bash experiments/qec1435_replay_nonexistence.sh
```

The default exact replay requires Python 3.10+ and Node.js. It verifies the signed-shadow identities, physical subgroup cosets, exact integer certificates, ten-site controls, the committed 37 additive-code representatives, and their hull and Hall audits. It does not regenerate the exhaustive length-ten census.

To regenerate the census, install its pinned dependency and pass `--census`:

```sh
python3 -m pip install -r requirements-qec1435.txt
bash experiments/qec1435_replay_nonexistence.sh --census
```

The census uses `pynauty==2.8.8.1` and rewrites the representative and class-audit JSON files. The default replay uses the committed representatives; it is a distinct, shorter verification run.

## Repository map

| Location | Contents |
| --- | --- |
| `paper/QEC1435_NO_BINARY_14_3_5.tex` | Authoritative LaTeX manuscript source |
| `output/pdf/QEC1435_NO_BINARY_14_3_5.pdf` | Compiled paper |
| `experiments/` | Exact certificate verifiers, census, generator representatives, and audit data |
| `research/` | Dated mathematical derivations and the current verification-boundary record |

The default replay and full census are separate verification levels. The review boundary and remaining concerns are recorded in [`research/UNRESOLVED_GAPS.md`](research/UNRESOLVED_GAPS.md).
