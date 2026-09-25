# Mathematical gap and review record

Audit date: 24 September 2026. This file records the proof checks and remaining verification boundary for `output/pdf/QEC1435_NO_BINARY_14_3_5.pdf`. The authoritative manuscript source is `paper/QEC1435_NO_BINARY_14_3_5.tex`; Tectonic compiles it to the PDF.

The repository cleanup reran the default exact replay against the committed representatives and class-audit data. It did not rerun the full lengthening census; the census result below is from the earlier full-census run.

## Findings addressed in the rewrite

1. **The 39-variable weight-two system.** The variables are the 39 physical split-weight counts $H_{a,b}$, with prefix weight $a=0,1,2$ and suffix weight $b=0,\ldots,12$. The four actual cosets of $\langle Z_0Z_1\rangle$ in its two-site normalizer give $H_{2,b}\ge H_{0,b}$. The manuscript lists all remaining equations and inequalities, proves the Farkas sign convention, and identifies the exact dual and independent BigInt verifier.

2. **$X_0X_1$ versus $Z_0Z_1$.** The paper fixes $Z_0Z_1$. Applying Hadamards on both sites maps $X_0X_1$ to this representative. The exact verifiers encode $Z_0Z_1$ as the binary label documented in their source.

3. **Physical-to-computational implications.** The signed transform is derived as the enumerator of a genuine affine coset. Each subgroup model is derived by complete-coset closure in the original physical Pauli space. The main paper states which conditions each certificate uses and treats each model only as a necessary relaxation.

4. **Low-weight, support, and reduction arguments.** The rewrite supplies the integer coefficient identity and parity calculation; enumerates all five triple-support geometries; records the branch equations $A_1=A_2=A_3=0$, $A_4=3$ used in the rank-three certificates; and proves that the single-check graph map is onto. This gives hull dimension exactly four, rather than merely a lower bound.

5. **Ten-site classification and final exclusion.** The complete shortening/lengthening recurrence is stated and proved. The census was regenerated; every predecessor count in the required cells matched. The colored-graph equivalence encoding is explained. The Hall condition is derived from the perfect pairing $(J^\perp/C)\times(P/J)$, and every hull-four representative fails its $N_3\le59$ bound.

6. **References and presentation.** The PDF retains references for the symplectic/additive correspondence, weight and shadow enumerators, the prior open problem, related nonexistence work, the additive lengthening counts, and the stored distance-four construction.

## Remaining review boundary

No unproved implication was located in the rewritten chain during this internal audit. The following verification work remains appropriate before treating the result as accepted by the field:

1. The prior expert comments were supplied to this task, but the revised proof has not been returned to those reviewers. Their independent re-check of the physical coset models, the rank-six Hall pairing, and the ten-site census is outstanding.
2. The full census has one exhaustive implementation using `pynauty`; the JavaScript audits independently recompute the 37 codebooks, hulls, cosets, and Hall failures, but do not regenerate all equivalence classes. The lengthening argument is complete on paper, and the census is reproducible, yet a second exhaustive implementation would reduce software-risk further.
3. The Farkas verifiers independently rebuild the physical cosets, transform matrices, and exact residuals in several cases using Python and JavaScript. Those implementations share the mathematical row definitions. A reviewer should still check that the manuscript's derivation of each row family matches the problem represented by that row.

These are review and computational-trust limits, not a specific counterexample or an identified logical gap. They are not resolved by typesetting or by a passing replay.

## Historical status note

`QEC1435_SINGLECHECK_SURJECTIVITY_HULL4_2026-09-20.md` records the state of the work on 20 September, when the exact hull-four reduction had been established but the rank-six lift obstruction was still described as open. The later class audit and Hall-capacity argument in the present manuscript close that finite lift obstruction for all 12 hull-four classes. The note is retained as research history; its open-status language is superseded by the present working proof and should not be read as current manuscript status.

The earlier open-status wording in the dated research note is historical and is superseded by the paper's length-ten classification and Hall-capacity exclusion. No separate computational supplement is maintained; the paper points once to the immutable code archive, and the repository README gives reproduction instructions.
