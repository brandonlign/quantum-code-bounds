# Verification guide

This guide maps the paper's computational claims to the reproducible checks and data in this repository. The default replay uses exact integer arithmetic and the committed length-ten representatives. The optional census mode reconstructs those representatives.

## Requirements and commands

The standard replay requires Python 3.10 or newer and Node.js. From the repository root, run:

```sh
bash experiments/qec1435_replay_nonexistence.sh
```

The replay checks the signed-shadow identities, each physical subgroup model, the Farkas multipliers and residuals, the ten-site control calculations, and the committed length-ten representatives and their lift audits. Python verifiers use arbitrary-precision integers; the independent JavaScript verifiers use `BigInt`. No floating-point feasibility result is used as a certificate. The default replay does not regenerate the length-ten classification. Its audit output is written to a temporary directory and removed at exit.

To reconstruct the classification as well as run the standard replay, install the pinned dependency and use the optional census mode:

```sh
python3 -m pip install -r requirements-qec1435.txt
bash experiments/qec1435_replay_nonexistence.sh --census
```

The dependency is `pynauty==2.8.8.1`. Census representatives and their class audit are written to a temporary directory, so this command does not replace the committed scientific data. The census generates candidates by the shortening/lengthening recurrence in Section 7, applies the exact colored-graph equivalence test, and checks its resulting cell counts against the published counts. Those published counts are regression checks, not the enumeration or its completeness argument.

To rebuild and mechanically inspect the paper PDF, install Tectonic, Python 3.10 or newer, and Poppler (`pdfinfo`, `pdffonts`, and `pdftotext`), then run:

```sh
bash paper/build_pdf.sh
```

The script compiles the authoritative `.tex` source and runs the PDF preflight. The preflight checks metadata, page count, link annotations, embedded fonts, and extracted text. It does not replace visual inspection of the rendered pages or mathematical review.

## Certificate and data map

- `experiments/qec1435_shadow_lowweight_unconditional_exact.py` verifies the global low-weight inequality and its integer coefficients.
- `experiments/qec1435_shadow_parity_certificate.py` and `experiments/qec1435_shadow_parity_independent.mjs` verify the integral shadow-parity congruence independently.
- `experiments/qec1435_order2_weight2_split_shadow_exact.py` contains the exact 39-variable weight-two certificate. It reconstructs the physical (2+12) split rows and verifies all 39 column identities and the negative normalization. `experiments/qec1435_order2_weight2_split_shadow_bigint_independent.mjs` independently rebuilds the rows and checks the same certificate with JavaScript `BigInt`.
- The weight-three, Bell-subgroup, five-site, six-site, rank-three overlap, and disjoint-support certificates are implemented in the corresponding `qec1435_*_exact.py` and independent `qec1435_*_independent.mjs` or `*_audit.mjs` files under `experiments/`. The disjoint four-block dual is also stored in `experiments/qec1435_disjoint_fourblock_exact_dual.json`.
- `experiments/qec1435_n10_additive_37_generators_xy.json` contains the 37 committed length-ten representatives. `experiments/qec1435_n10_additive_37_class_audit.py` and `experiments/qec1435_n10_additive_37_class_audit.json` record their exact hull, quotient-spectrum, and coset-capacity audits. The JavaScript audits in `qec1435_n10_additive_37_hull_hall_independent.mjs` and `qec1435_n10_additive_37_js_independent_audit.mjs` independently replay the saved representatives.
- `experiments/qec1435_n10_additive_lengthening_census.py` regenerates the additive-code classes with the pinned `pynauty` dependency. Its equivalence certificates come from colored incidence graphs of complete codebooks; weight and pair-rank invariants only filter candidates before canonicalization.

The default replay's final `NONEXISTENCE CORE REPLAY PASS` confirms the checks in that mode. The separate census mode must be run to claim that the exhaustive classification was regenerated. Running either mode does not constitute an independent mathematical review of the necessity of the physical constraints or of the proof's interpretation of the certificates.
