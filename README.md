# No binary [[14,3,5]] stabilizer code exists

**Brandon Li, 2026**

This repository contains a computer-assisted proof that there is no qubit stabilizer code with parameters [[14,3,d ≥ 5]]. Since a [[14,3,4]] code is known, the largest possible distance for n = 14, k = 3 is 4. This settles the open entry in [Grassl's code tables](https://codetables.de/QECC.php?q=4&n=14&k=3) and answers Research Problem 1 of Ball, Centelles and Huber (2023).

**Paper:** [`paper/No_Binary_14_3_5.pdf`](paper/No_Binary_14_3_5.pdf) (LaTeX source: [`paper/No_Binary_14_3_5.tex`](paper/No_Binary_14_3_5.tex))

## Outline of the proof

1. **Low-weight words (Section 4).** Split weight enumerators and a signed shadow inequality give A₁ = A₃ = 0, A₂ ≤ 2 and A₄ ≤ 3. A congruence mod 4096 then gives A₄ ∈ {1, 3}.
2. **Exact infeasibility certificates (Section 5).** Integer Farkas certificates rule out weight-two words and every configuration of three weight-four words, so A₄ = 1.
3. **Reduction (Section 6).** The unique weight-four word forces an additive (10, 2¹⁰, ≥ 5) code with symplectic hull dimension 4 that satisfies a coset-capacity bound.
4. **Classification (Section 7).** There are exactly 37 such length-ten codes up to equivalence. 25 have the wrong hull dimension, and the other 12 violate the capacity bound.

## Checking the proof

You need Python 3.10 or newer and Node.js. No other packages are required.

```sh
bash verification/replay.sh
```

This takes about 10 seconds. It checks every exact certificate, most of them in two separate implementations (Python and JavaScript BigInt), and checks the 37 saved classes. To also regenerate the classification from scratch (about 5 minutes):

```sh
python3 -m pip install -r requirements.txt
bash verification/replay.sh --census
```

### Independent checks

[`verification/independent/`](verification/independent) is a second implementation, written separately from the manuscript text. It re-derives the argument in these steps:

- the Section 4 identity and congruence;
- completeness of the case analysis for pairs of weight-four words;
- every Section 5 relaxation, using a floating-point LP solver (corroboration only);
- a separate census with a different graph encoding and an exact orbit–stabilizer mass check in every cell;
- the hull and coset data of all 37 classes.

It needs the packages in `requirements.txt`.

```sh
bash verification/independent/run_all.sh
```

## Repository layout

| Path | Contents |
|---|---|
| `paper/` | Manuscript source, PDF and build script (`bash paper/build_pdf.sh`, needs [Tectonic](https://tectonic-typesetting.github.io)) |
| `verification/s4_*` … `verification/s7_*` | Exact checks, named by paper section (`.py` = Python, `.mjs` = JavaScript) |
| `verification/s7_37_classes.json` | Generator matrices of the 37 length-ten classes (X part in bits 0–9, Z part in bits 10–19) |
| `verification/replay.sh` | Runs all exact checks |
| `verification/independent/` | Independent re-implementation and expected outputs |

## Citation and license

See [`CITATION.cff`](CITATION.cff). An earlier version of the preprint is archived on Zenodo: [doi:10.5281/zenodo.22885774](https://doi.org/10.5281/zenodo.22885774). Code is released under the MIT License. The paper is released under CC BY 4.0.

## Contact

Brandon Li — brandon.li.gn@gmail.com
