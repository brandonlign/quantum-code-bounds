# Verification scope

The manuscript gives a computer-assisted nonexistence proof. The standard replay verifies the exact arithmetic and saved finite data used by the paper; it does not by itself establish that every computational constraint is necessary for a hypothetical physical stabilizer code.

## Standard replay

Run from the repository root:

```sh
bash experiments/qec1435_replay_nonexistence.sh
```

The replay uses Python 3.10+, Node.js, and Git. It performs exact integer checks for:

- the signed-shadow coefficient identity and integrality/parity restriction;
- physical subgroup cosets and the Farkas multipliers, signs, and residuals used in the low-weight and rank-three exclusions;
- selected ten-site controls and the physical symplectic-lift check;
- rank, distance, symplectic hull, quotient-coset minima, and Hall exclusions for the 37 committed additive-code representatives.

Python verifiers use arbitrary-precision integers; the independent JavaScript verifiers use `BigInt`. No floating-point feasibility result is used as a certificate. Replay outputs are temporary, and the committed certificate and representative data are not rewritten. Some independent arithmetic implementations share the manuscript's mathematical row definitions.

The separate `experiments/audit_independent_review.py` script independently reconstructs the length-ten hull and coset-capacity calculations directly from the generator data. It is not needed by the standard replay.

## Census and saved representatives

The default replay checks the saved 37 classes; it does not regenerate or classify every length-ten candidate. To regenerate the classification, install `pynauty==2.8.8.1` and run:

```sh
python3 -m pip install -r requirements-qec1435.txt
bash experiments/qec1435_replay_nonexistence.sh --census
```

The census command first runs the standard replay, then regenerates candidates by the shortening/lengthening recurrence in Section 7, applies the colored-graph equivalence test, and checks the resulting predecessor-cell counts against the published counts. The generated representatives and audit output are temporary. The full census was run during the final manuscript audit; it was not rerun for the current repository push. The published counts are regression checks, not an input to the enumeration or a proof of its completeness.

## Certificate and data map

- `experiments/qec1435_shadow_lowweight_unconditional_exact.py` verifies the global low-weight inequality and its integer coefficients.
- `experiments/qec1435_shadow_parity_certificate.py` and `experiments/qec1435_shadow_parity_independent.mjs` verify the integral shadow-parity congruence independently.
- `experiments/qec1435_order2_weight2_split_shadow_exact.py` contains the exact 39-variable weight-two certificate. It reconstructs the physical split-weight rows and verifies all 39 column identities and the negative normalization. `experiments/qec1435_order2_weight2_split_shadow_bigint_independent.mjs` independently rebuilds the rows and checks the same certificate with JavaScript `BigInt`.
- The weight-three, Bell-subgroup, five-site, six-site, rank-three overlap, and disjoint-support certificates are implemented in the corresponding `qec1435_*_exact.py` and independent `qec1435_*_independent.mjs` or `*_audit.mjs` files under `experiments/`. The disjoint four-block dual is stored in `experiments/qec1435_disjoint_fourblock_exact_dual.json`.
- `experiments/qec1435_n10_additive_37_generators_xy.json` contains the 37 committed length-ten representatives. The Python class audit and its JSON output record their exact hull, quotient-spectrum, and coset-capacity calculations. The JavaScript audits independently replay the saved representatives.
- `experiments/qec1435_n10_additive_lengthening_census.py` regenerates the additive-code classes using the pinned `pynauty` dependency. Its equivalence certificates come from colored incidence graphs of complete codebooks; weight and pair-rank invariants only filter candidates before canonicalization.

The standard replay's final `NONEXISTENCE CORE REPLAY PASS` confirms the checks in that mode. The census mode must be run to regenerate the exhaustive classification. Neither mode replaces review of the mathematical necessity of the physical constraints or of the proof's interpretation of the certificates.

## Mathematical review boundary

Independent review should check that the mathematical reductions match the computational models, in particular:

1. The signed affine-shadow derivation and the implication from each original-physical subgroup to its relaxed split-weight model.
2. The exhaustion of low-weight stabilizer configurations and the surjectivity/hull-four reduction.
3. The shortening/lengthening completeness argument and the colored-graph equivalence encoding.
4. The perfect pairing and physical prefix-cost distribution behind the 64-coset Hall capacities.

The internal manuscript audit found no specific counterexample or invalid deduction. The revised proof has not received an independent field-expert re-check of every reduction and the complete census. Passing the replay does not establish expert acceptance of the theorem.
