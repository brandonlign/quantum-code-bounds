# Verification scope

The [manuscript](output/pdf/QEC1435_NO_BINARY_14_3_5.pdf) presents a computer-assisted proof. This document distinguishes the verifiable computational evidence from the independent mathematical review still appropriate for a research claim.

## What the standard replay checks

`bash experiments/qec1435_replay_nonexistence.sh` uses the committed length-ten class representatives and runs exact Python and Node.js checks for:

- the signed-shadow coefficient identity and integrality/parity restriction;
- physical subgroup cosets and the exact Farkas multipliers, signs, and residuals used in the low-weight and rank-three exclusions;
- selected ten-site controls and the physical symplectic-lift check;
- rank, distance, symplectic hull, suffix-coset minima, and Hall exclusions for the committed 37 additive-code representatives.

The replay checks exact certificate arithmetic. It is not a substitute for reviewing why each linear constraint is necessary for a hypothetical physical stabilizer code. Some independent arithmetic implementations share the same mathematical row definitions.

## Full census versus saved-representative replay

The default replay checks **the saved 37 classes**; it does not independently generate or classify every length-ten candidate. Running `bash experiments/qec1435_replay_nonexistence.sh --census` first regenerates representatives using the lengthening census and `pynauty`, then rechecks the class-level exclusions. This full census was run previously; the latest repository cleanup did not rerun it. A second independently implemented exhaustive equivalence-class census would provide stronger software-level confirmation.

## Mathematical review priorities

External review should scrutinize:

1. The signed affine-shadow derivation and the implication from each original-physical subgroup to its relaxed split-weight model.
2. The exhaustion of all possible configurations of low-weight checks, and the surjectivity/hull-four reduction.
3. The shortening/lengthening completeness argument and the colored-graph equivalence encoding.
4. The perfect pairing and physical prefix-cost distribution behind the 64-coset Hall capacities.

No specific counterexample or unresolved logical implication was identified in the internal manuscript audit. The revised proof has not yet received an independent field-expert re-check of every reduction and the complete census. Passing the replay does not itself establish expert acceptance of the theorem.

Earlier working hypotheses and dated open-status notes remain in Git history; this file and the current manuscript describe the public-facing proof and its verification limits.
