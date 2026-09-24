# No binary [[14,3,d≥5]] quantum stabilizer code exists

**Brandon Li · 2026 · Quantum error-correcting codes**

A computer-assisted nonexistence proof for a binary quantum stabilizer code encoding three logical qubits in fourteen physical qubits with distance at least five. Together with the known `[[14,3,4]]` construction, the proposed theorem determines the exact stabilizer-code bound `d_max(14,3)=4`.

**[Read the paper (PDF)](output/pdf/QEC1435_NO_BINARY_14_3_5.pdf)** · [Manuscript source](paper/QEC1435_NO_BINARY_14_3_5.md) · [Computational supplement](paper/COMPUTATIONAL_SUPPLEMENT.md)

## The result

The proof addresses **binary qubit stabilizer codes** at these parameters, including pure and degenerate codes. It does **not** rule out general non-stabilizer quantum codes.

The argument has three stages:

1. **Signed-shadow constraints** and exact infeasibility certificates restrict low-weight stabilizers to a unique weight-four check.
2. **Symplectic reduction** shows that a hypothetical code would induce a length-ten additive code of size 1,024, distance at least five, and hull dimension four.
3. **Exhaustive classification and a Hall obstruction** exclude all 37 relevant length-ten additive-code classes: 25 have the wrong hull dimension, and each of the remaining 12 violates a necessary physical coset-capacity bound.

The paper distinguishes necessary relaxations from sufficient conditions. Exact certificates and the reconstructed class representatives are included.

## Reproduce the computations

Requirements: **CPython 3.10+** and **Node.js** with BigInt and ESM support. Run from the repository root:

```bash
bash experiments/qec1435_replay_nonexistence.sh
```

The default replay verifies exact identities and certificates, saved 37-class representatives, and hull/Hall exclusions. To regenerate the equivalence-class census:

```bash
python3 -m pip install -r requirements-qec1435.txt
bash experiments/qec1435_replay_nonexistence.sh --census
```

The full census is substantially more resource-intensive than the default replay. The [computational supplement](paper/COMPUTATIONAL_SUPPLEMENT.md) maps proof obligations to verifiers and data. The reproducibility snapshot referenced by the manuscript is commit [`ad8656883957975fc429895e64fbb497c480cba4`](https://github.com/brandonlign/quantum-code-bounds/tree/ad8656883957975fc429895e64fbb497c480cba4).

To regenerate and mechanically check the manuscript PDF (requires ReportLab and Poppler utilities):

```bash
python3 -m pip install -r requirements-qec1435.txt
bash paper/build_pdf.sh
```

## Repository map

| Location | Contents |
| --- | --- |
| [Paper PDF](output/pdf/QEC1435_NO_BINARY_14_3_5.pdf) | Readable statement and proof |
| [Manuscript source](paper/QEC1435_NO_BINARY_14_3_5.md) | Mathematical text |
| [Computational supplement](paper/COMPUTATIONAL_SUPPLEMENT.md) | Proof-obligation and certificate index |
| [`experiments/`](experiments/) | Exact verifiers, independent checks, class generators, and audit data |
| [`research/`](research/) | Supporting algebraic development notes |

**Verification scope:** computational certificates and class data have been replayed, but successful computation does not substitute for specialist review of the mathematical reductions and completeness arguments.
