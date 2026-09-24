# Computational supplement to the nonexistence proof

**Brandon Li**

This supplement accompanies *No binary [[14,3,d≥5]] quantum stabilizer code exists*. It supplies the full proof-obligation-to-file map; the mathematical deductions and necessary-relaxation bridges remain in the main paper. The pinned proof-code snapshot is `ad8656883957975fc429895e64fbb497c480cba4`. This file is documentation, not a substitute for the exact data and scripts at that snapshot.

## Full certificate and reproducibility manifest

The exact dual certificates, reconstructed generator matrices, verification scripts, and independent audits are archived at the immutable snapshot https://github.com/brandonlign/quantum-code-bounds/tree/ad8656883957975fc429895e64fbb497c480cba4 . The certificate manifest below identifies the specific files for each computational step. The complete matrices and multipliers are provided as electronic proof data rather than reproduced in the printed paper.

The main reproduction entry point is

```bash
bash experiments/qec1435_replay_nonexistence.sh
```

It checks the compact Stage-I proof chain, the Stage-II controls, the committed 37 representatives, and the exact class audit without rerunning the memory-heavy census. To regenerate the 37 representatives from a clean environment, run

```bash
python3 -m pip install -r requirements-qec1435.txt
bash experiments/qec1435_replay_nonexistence.sh --census
```

The exact certificate checks use integer arithmetic in Python and JavaScript BigInt; approximate numerical feasibility is not used as proof. Runtime requirements and PDF-build dependencies are specified in the repository README and requirements file.

### Certificate manifest

| mathematical obligation | physical relaxation or finite object | verifier | saved certificate or data | expected exact result |
|---|---|---|---|---|
| global low-weight inequality | 14-site total physical enumerator and affine shadow | `experiments/qec1435_shadow_lowweight_unconditional_exact.py` | exact 15-column identity in verifier; independent BigInt replay | `A1=A3=0`, `A2<=2`, `A4<=3` |
| shadow parity | integer `Sh_0,...,Sh_3` and low-weight MacWilliams equations | `experiments/qec1435_shadow_parity_certificate.py`, `experiments/qec1435_shadow_parity_independent.mjs` | exact coefficient combination | `A3+A4` odd; `A4 in {1,3}` |
| no physical weight two | four real cosets of `<ZZ>` and 2+12 split shadow | `experiments/qec1435_order2_weight2_split_shadow_exact.py`, BigInt companion | exact multipliers in verifier | 39 columns; normalization `-2571108352`; `H2>=H0` |
| no physical weight three | 16 real cosets of `<ZZZ>` and 3+11 split shadow | `experiments/qec1435_weight3_split_shadow_exact.py`, BigInt companion | exact multipliers in verifier | 36 columns; normalization `-22528` |
| no same-support Bell pair | 16 real cosets of `<XXXX,ZZZZ>` | `experiments/qec1435_order2_m4_bell_split_shadow_exact.py`, BigInt companion | exact multipliers in verifier | 55 columns; normalization `-320017816092672` |
| no five-site overlap | 64 real cosets of the two-check rank-two subgroup | `experiments/qec1435_weight4_fivesite_triangle_split_shadow_bigint_exact.mjs` | exact BigInt multipliers in verifier | 90 columns; normalization `-52501014528` |
| no six-site same-letter overlap | 256 real cosets, 13 patterns | `experiments/qec1435_triangle_sixsite_split_shadow_exact.py`, BigInt companion | exact multipliers in verifier | 117 columns; normalization `-8820736` |
| no six-site crossed overlap | 256 real cosets, 14 patterns | `experiments/qec1435_crossed_bell_sixsite_split_shadow_exact.py`, BigInt companion | exact multipliers in verifier | 126 columns; normalization `-22212608` |
| no overlapping three-check geometry | four true rank-three normalizers | `experiments/qec1435_sparse_h4_rank3_four_exact.py` plus independent BigInt companion | four embedded exact dual dictionaries | 240/135/300/296 columns; all four negative constants |
| no disjoint three-check geometry | 648 complete `4+4+4+2` physical coset variables | `experiments/qec1435_disjoint_fourblock_shadow_exact.py` plus two independent JS companions | `experiments/qec1435_disjoint_fourblock_exact_dual.json` | 648 columns; normalization `-125829120`; 403 positive residuals |
| unique-check graph reduction | physical quotient `E`, graph map `T`, hull | `research/QEC1435_SINGLECHECK_SURJECTIVITY_HULL4_2026-09-20.md`; Stage-II controls | exact algebra plus standard-library controls | `dim C=10`, `d(C)>=5`, `dim hull(C)=4` |
| exhaustive ten-site classes | exact `r=0,1,2` lengthening recurrence | `experiments/qec1435_n10_additive_lengthening_census.py` | `experiments/qec1435_n10_additive_37_generators_xy.json` | 37 classes; predecessor counts reproduced |
| physical lift obstruction | 64 suffix cosets and prefix cost capacities | `experiments/qec1435_n10_additive_37_class_audit.py` plus two independent JS audits | `experiments/qec1435_n10_additive_37_class_audit.json` | hull counts `{0:7,2:14,4:12,6:2,8:2}`; all 12 hull-four Hall-fail |

The committed replay does not use a numerical infeasibility status or approximate multipliers. It reconstructs the physical cosets, integer transform matrices, multiplier signs, every column residual, and the negative right-hand side.

