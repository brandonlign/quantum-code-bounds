# No binary [[14,3,d≥5]] quantum stabilizer code exists

## A signed-shadow proof and exhaustive additive-code classification

**Brandon Li**

## Abstract

We prove that no binary qubit stabilizer code with parameters `[[14,3,d>=5]]` exists, settling the remaining distance gap for stabilizer codes encoding three qubits into fourteen. The proof first applies a signed affine-shadow inequality and an integrality congruence to restrict low-weight stabilizer words. Exact split-shadow infeasibility certificates then exclude weight-two words and all configurations with three weight-four checks, leaving a unique weight-four check.

That check yields a ten-coordinate binary-additive code of size 1,024, minimum distance at least five, and symplectic hull dimension four. We reconstruct all 37 relevant equivalence classes by exhaustive lengthening: 25 have the wrong hull dimension, and the other twelve violate a necessary 64-coset capacity bound. Together with the known `[[14,3,4]]` construction, this proves `d_max(14,3)=4` for binary stabilizer codes.

## 1. Introduction and main result

### Theorem 1

There is no binary qubit stabilizer code with parameters `[[14,3,d>=5]]`.

Consequently, the maximum distance of a binary qubit stabilizer code with `n=14` and `k=3` is

```text
d_max(14,3) = 4.
```

Grassl's quantum-code tables record a `[[14,3,4]]` construction and an upper bound of five for the distance of a binary `[[14,3]]` stabilizer code. Ball, Centelles, and Huber singled out the existence of `[[14,3,5]]` in Research Problem 1 as the smallest unresolved qubit stabilizer parameter set at the time of their article. Theorem 1 closes this gap. The nonexistence proof for `[[13,5,4]]` by Bierbrauer, Fears, Marcugini, and Pambianco provides a related precedent. Our argument combines signed weight enumerators with the classification of binary-additive codes; it does not assume `GF(4)`-linearity.

The proof has three steps. First, signed-shadow identities restrict the possible small stabilizers. Second, exact linear infeasibility certificates eliminate the remaining configurations of low-weight checks. Third, a symplectic reduction leads to an exhaustive classification of ten-site additive codes and a final coset-counting contradiction. The complete computational record is described in Section 9.

Throughout, *physical* means weight or support on the original qubits, as opposed to a coordinate of an auxiliary relaxation. We use the qualifier when that distinction matters. The result applies to both pure and degenerate binary stabilizer codes, but not to arbitrary non-stabilizer quantum codes.

## 2. Pauli space and notation

Let

```text
V_n = F_2^(2n) = {(x|z): x,z in F_2^n}
```

encode Pauli labels modulo phase. The symplectic form is

```text
< (x|z),(x'|z') > = x dot z' + z dot x'  in F_2.
```

The Pauli weight is

```text
wt(x|z) = #{i : (x_i,z_i) != (0,0)}.
```

A binary stabilizer code with parameters `[[14,3,d]]` is an isotropic subspace `S <= V_14` of binary dimension `14-3=11`. Its centralizer is `S^perp`, and its distance is

```text
d(S) = min { wt(v) : v in S^perp \ S }.
```

We write `d_max(n,k)` for the greatest minimum distance `d(S)` among binary stabilizer codes with fixed `n` and `k`; this should not be confused with the maximum of the minimum weights of distinct logical-Pauli cosets within one fixed code.

We assume for contradiction that `d(S)>=5`. A code is *pure to distance d* if no nonzero stabilizer word has weight below `d`; otherwise it is degenerate (or impure). In particular, the distance formula does not exclude low-weight stabilizer words. If a vector of weight at most four commutes with `S`, it must itself be in `S`.

For a binary subspace `C` of a Pauli space, its symplectic hull is `Hull(C)=C intersect C^perp`. When a block of coordinates is specified, `H_(a,b)` below counts stabilizer words of split weight `(a,b)`; it is an enumerator, not a subspace. The hull in Section 6 is denoted `J` to keep the two notions distinct.

## 3. The signed affine shadow, including split weights

For one qubit define

```text
q(x,z) = x + z + xz in F_2.
```

This is one exactly when `(x,z)` is nonzero, so on `V_n` it satisfies

```text
q(v) = wt(v) mod 2,
q(v+w) = q(v) + q(w) + <v,w>.
```

Because `S` is isotropic, `q|S` is linear. Nondegeneracy of the symplectic form gives a vector `v_0` such that

```text
<v_0,s> = q(s) for every s in S.
```

Character orthogonality then gives the exact indicator identity

```text
1_{v_0+S^perp}(v)
  = 2^(-11) sum_{s in S} (-1)^(q(s)+<v,s>).
```

Thus the signed transform is not a formal signed polynomial. It is the weight enumerator of the affine coset `v_0+S^perp`; every split cell is a nonnegative integer.

For a partition of the qubits into blocks of lengths `m` and `f`, let `H_(i,j)` count stabilizer words with block weights `(i,j)`. Define the quaternary Krawtchouk coefficients

```text
K_a^(m)(i) = [u^a] (1+3u)^(m-i) (1-u)^i.
```

If `C_(a,b)` counts `S^perp` and `Sh_(a,b)` counts the affine shadow, then

```text
2048 C_(a,b)
  = sum_(i,j) H_(i,j) K_a^(m)(i) K_b^(f)(j),

2048 Sh_(a,b)
  = sum_(i,j) (-1)^(i+j) H_(i,j)
                         K_a^(m)(i) K_b^(f)(j).
```

Both `C_(a,b)` and `Sh_(a,b)` are nonnegative integers, and `C_(a,b)>=H_(a,b)` because `S <= S^perp`. If `1<=a+b<=4`, then

```text
C_(a,b) = H_(a,b),
```

because every centralizer word in that weight range must be a stabilizer word when `d(S)>=5`. This equality is valid even when `S` is impure.

## 4. Global low-weight restrictions and parity

Write `A_j` for the number of stabilizer words of total physical weight `j`, and put

```text
T_j = sum_w A_w K_j^(14)(w),
U_j = sum_w (-1)^w A_w K_j^(14)(w).
```

The quantities `T_j/2048` and `U_j/2048` are the actual total-weight counts in `S^perp` and in the affine shadow. Hence `U_j>=0`, even without purity. Also `A_0=1`, `sum_j A_j=2048`, and `T_j=2048 A_j` for `j=1,2,3,4`.

**Lemma 2 (low-weight restriction).** If `d(S)>=5`, then `A_1=A_3=0`, `A_2<=2`, and `A_4<=3`.

Expanding the Krawtchouk transforms in `T_j` and `U_j` gives the coefficientwise identity

```text
989184 A_4 = -296 U_2 -88 U_4 -9584640 A_0 +6309 sum_j A_j
             -11685888 A_1 -1345536 A_2 -4681728 A_3
             +1914 (T_1-2048 A_1) +1318 (T_2-2048 A_2)
             +279 (T_3-2048 A_3) +161 (T_4-2048 A_4)
             -1081344 A_5 -254976 A_6 -15360 A_7 -44032 A_14.
```

After inserting the code equalities and nonnegativity, this gives

```text
11685888 A_1 +1345536 A_2 +4681728 A_3 +989184 A_4 <= 3336192.
```

Therefore

```text
A_1 = A_3 = 0,   A_2 <= 2,   A_4 <= 3.
```

The remaining possibility `A_2=1` or `2` is removed by the physical weight-two subgroup certificate in Section 5.3.

### 4.1 Integral affine-shadow parity

The inequality alone does not determine whether `A_4` is zero. An integrality congruence supplies the missing condition. The coefficients below were chosen so that expansion of the MacWilliams and shadow equations leaves, modulo 4096, only the terms in `A_3` and `A_4`. Let

```text
E_0 = sum_w A_w,                         RHS(E_0)=2048,
E_j = T_j -2048 A_j,                     j=1,...,4,
F_j = U_j -2048 Sh_j,                    j=0,...,3.
```

Take the exact integer combination

```text
L = E_0 -2E_1 -6E_2 -17E_3 -95E_4
    -20F_0 -24F_1 +1108F_2 +246F_3.
```

The equations give `L=2048`. Direct expansion gives the coefficients on `A_0,...,A_14` as

```text
[-4550656, -7348224, -1052672, -2623488, 321536,
 -634880, 221184, -28672, 24576, 24576,
 -45056, 0, 40960, -16384, -77824].
```

Modulo 4096 every coefficient vanishes except the coefficients of `A_3` and `A_4`, each of which is 2048 modulo 4096. The coefficients of the four integer shadow variables are

```text
[40960, 49152, -2269184, -503808],
```

and are all divisible by 4096. Hence

```text
A_3 + A_4 is odd.
```

Together with `A_3=0` and `0<=A_4<=3`, this gives

```text
A_4 in {1,3}.
```

## 5. Excluding low-weight stabilizer configurations

We first derive a relaxation that is necessary for any stabilizer containing a specified subgroup. Exact infeasibility certificates then exclude the possible low-weight configurations.

### 5.1 A necessary coset-counting relaxation

Let `R <= S` be an isotropic subgroup supported on `u` of the original qubits, with the remaining `f=14-u` sites forming a suffix. Every element of `S` commutes with `R`, so its prefix lies in `R^perp`. Also, `S` is a union of complete `R`-cosets.

For each complete coset `Q` of `R` in `R^perp`, let

```text
p(Q)=(p_0,...,p_u),
p_a = #{q in Q : prefix physical weight(q)=a}.
```

Let `y_(p,b)` be the number of complete `R`-cosets selected by `S`, aggregated over all suffix Pauli labels of physical weight `b`, and grouped only by the prefix pattern `p`. Then `y_(p,b)>=0` and

```text
H_(a,b) = sum_p p_a y_(p,b).
```

This is a necessary model for a real code. It deliberately forgets the actual prefix coset label, the suffix Pauli label, and all global linear compatibility among different suffixes. It therefore enlarges the feasible set. A contradiction in this relaxation excludes a physical code; feasibility would prove nothing.

For every such model we use the following row families:

* `H_(0,0)=1` and `sum H=2048`;
* physical coset equalities or inequalities forced by the selected subgroup;
* the low-weight distance equations `T_(a,b)-2048H_(a,b)=0` for `1<=a+b<=4`;
* centralizer inclusion `2048H-T<=0`;
* centralizer nonnegativity `-T<=0`;
* signed affine-shadow nonnegativity `-SH<=0`; and
* `y>=0`.

The transforms `T` and `SH` use Pauli weights on the actual prefix and suffix sites. The capacity bound introduced in Section 6 is not used in these exclusions.

### 5.2 Exact Farkas sign convention

After scaling by 2048, write the necessary system as

```text
M y = rhs,     G y <= 0,     y >= 0.
```

An exact certificate consists of nonnegative `lambda`, free-sign `nu`, and a coefficient vector `c` satisfying

```text
lambda >= 0,
c = lambda G + nu M >= 0 coefficientwise,
nu dot rhs < 0.
```

For a putative feasible `y`,

```text
0 <= c dot y = lambda dot (G y) + nu dot (M y)
              <= nu dot rhs < 0,
```

which is impossible. Each certificate is checked by exact integer arithmetic. The physical constraints are derived before applying Farkas' lemma; the certificates establish infeasibility of the resulting necessary systems.

### 5.3 Excluding weight-two stabilizers

Suppose `p=Z_0 Z_1` belongs to `S`. Every weight-two Pauli label is locally Clifford equivalent to this representative; in particular, Hadamards on sites 0 and 1 send `X_0X_1` to `Z_0Z_1`. The eight two-site Paulis commuting with `p` split into four complete cosets of `<p>` with physical two-site pattern

```text
(1,0,1) once,   (0,2,0) once,   (0,0,2) twice.
```

For every fixed suffix Pauli label, complete-coset closure therefore gives

```text
H_(2,b) >= H_(0,b),   b=0,...,12.
```

The variables are `H_(a,b)` for `a=0,1,2` and `b=0,...,12`, hence there are 39. The resulting split-weight system includes the coset inequality above, the low-weight distance equations and the signed-shadow constraints. Its exact Farkas certificate has

```text
nu dot rhs = -2571108352.
```

Thus `A_2=0` for every hypothetical code.

### 5.4 Excluding overlapping low-weight checks

The support argument in Section 5.5 uses the following exclusions. Each subgroup acts on the original qubits, and its normalizer and cosets are enumerated before the linear relaxation is formed.

#### A weight-three subgroup

For `R=<ZZZ>` on three original sites, the 16 normalizer cosets have prefix patterns

```text
(0,0,1,1) twelve times,
(0,1,1,0) three times,
(1,0,0,1) once.
```

The resulting 36-variable system has an exact dual with `nu dot rhs=-22528`. This also excludes a weight-three check, independently of Lemma 2.

#### The four-site Bell subgroup

For `R=<XXXX,ZZZZ>` on four original sites, the 16 complete cosets have patterns

```text
(1,0,0,0,3) once,
(0,0,2,0,2) nine times,
(0,0,0,4,0) six times.
```

For every suffix weight `b`,

```text
H_(1,b)=0,
H_(4,b)=H_(2,b)+3H_(0,b).
```

The split-weight system has an exact Farkas certificate with

```text
nu dot rhs = -320017816092672.
```

It excludes a pair of weight-four Bell checks with the same support.

#### The five-site overlap subgroup

If two commuting weight-four words overlap in three sites and differ on two of those sites, local Clifford conjugation gives

```text
p = X_0 X_1 Z_2 Z_3 I_4,
q = Z_0 Z_1 Z_2 I_3 Z_4.
```

All three nonzero words in `<p,q>` have weight four on five sites. The normalizer has 64 four-element cosets and nine prefix-weight patterns. The resulting 90-variable relaxation has an exact certificate with

```text
nu dot rhs = -52501014528.
```

#### The two six-site overlap subgroups

For the same-letter two-site overlap, use

```text
R = < ZZZZII, ZZIIZZ >.
```

The six-site normalizer has 256 four-element cosets and 13 prefix patterns. The corresponding 117-variable system has a Farkas certificate with `nu dot rhs=-8820736`.

For the crossed two-site overlap, use

```text
R = < ZZZZII, XXIIXX >.
```

The nonzero subgroup words have weights `4,4,6`. Here the normalizer has 14 prefix patterns; the resulting 126-variable system has a certificate with `nu dot rhs=-22212608`. Both six-site exclusions are checked separately, with the complete cosets enumerated in each case.

### 5.5 Support geometry of weight-four checks

Let `p,q` be distinct commuting weight-four stabilizer words. Let `t` be the number of common support sites and `h` the number of common sites on which their nonidentity Pauli letters differ. Commutation makes `h` even, and

```text
wt(p+q) = 8 - 2t + h.
```

The preceding subgroup exclusions remove every case with `t>=2`:

| `t` | `h` | physical obstruction |
|---:|---:|---|
| 4 | 2 | weight-two stabilizer |
| 4 | 4 | four-site Bell subgroup |
| 3 | 0 | weight-two stabilizer |
| 3 | 2 | five-site overlap subgroup |
| 2 | 0 | six-site same-letter triangle subgroup |
| 2 | 2 | six-site crossed-overlap subgroup |

The omitted case `t=4,h=0` would give the same Pauli word twice, not two distinct checks. Thus two distinct weight-four checks meet in at most one qubit. If they meet in one, commutation forces the same local Pauli letter there. Independent local Clifford transformations therefore map all weight-four checks to Z-only words simultaneously. This does not imply that the full stabilizer is CSS.

If `A_4=3`, the three checks are independent, because the sum of two has physical weight six or eight, not four. Their support sets are pairwise disjoint or meet in one site. Up to physical site permutation and reordering of the checks, there are exactly five support patterns:

| type | check supports | union | pair-product weights | triple-product weight |
|---|---|---:|---|---:|
| 0 intersections | `0123`, `4567`, `8,9,10,11` | 12 | `8,8,8` | 12 |
| 1 intersection | `0123`, `3456`, `7,8,9,10` | 11 | `6,8,8` | 10 |
| 2 intersections | `0123`, `3456`, `6789` | 10 | `6,8,6` | 8 |
| 3 distinct intersections | `0123`, `3456`, `2478` | 9 | `6,6,6` | 6 |
| one common site | `0123`, `3456`, `3789` | 10 | `6,6,6` | 10 |

To see that the list is complete, record which of the three pairs of supports intersect. There can be zero, one, two, or three intersecting pairs. When exactly two pairs intersect, their intersection sites must be distinct: if both were the same, that site would lie in all three supports and the third pair would intersect too. When all three pairs intersect, either their three intersection sites differ or all three supports share one site. These are precisely the five cases above.

### 5.6 The four overlapping rank-three geometries

For each of the four non-disjoint rows in the table, let `R` be the physical rank-three subgroup generated by the three displayed Z-only checks. Its complete cosets in the original-site normalizer are enumerated and grouped by their prefix-weight histograms. The exact relaxations are:

In each branch, the system includes the global equations

```text
sum_(a+b=j) H_(a,b) = 0,   j=1,2,3,
sum_(a+b=4) H_(a,b) = 3.
```

The first three follow from the low-weight restrictions and the weight-two exclusion; the last is the branch assumption `A_4=3`. They are necessary conditions on the hypothetical code, not consequences of subgroup containment alone.

| geometry | prefix + suffix | pattern classes | nonnegative variables | positive dual multipliers | negative normalization |
|---|---|---:|---:|---:|---:|
| three distinct intersections | 9+5 | 40 | 240 | 12 | `-86470656` |
| one common site | 10+4 | 27 | 135 | 13 | `-9031680` |
| two intersections | 10+4 | 60 | 300 | 14 | `-20484096` |
| one intersection | 11+3 | 74 | 296 | 14 | `-61440` |

For each row, the exact certificate has nonnegative inequality multipliers, nonnegative column residuals and the negative normalization shown. The four necessary systems are therefore infeasible by the Farkas argument in Section 5.2. Each system also imposes the global equations

```text
A_1=A_2=A_3=0,   A_4=3.
```

### 5.7 The disjoint `4+4+4+2` geometry

The only possible `A_4=3` geometry left by Section 5.6 would be

```text
R = < ZZZZIIIIIIIIII, IIIIZZZZIIIIII, IIIIIIIIZZZZII >.
```

Each four-site block has 64 cosets of `<ZZZZ>` in its even-X-parity normalizer. The six weight patterns below have multiplicities totaling `1+4+3+24+24+8=64`:

| pattern `(p_0,p_1,p_2,p_3,p_4)` | multiplicity |
|---|---:|
| `(1,0,0,0,1)` | 1 |
| `(0,1,0,1,0)` | 4 |
| `(0,0,2,0,0)` | 3 |
| `(0,0,1,0,1)` | 24 |
| `(0,0,0,2,0)` | 24 |
| `(0,0,0,0,2)` | 8 |

For each of the three blocks and the two untouched physical sites, let `y_(p,q,r,b)` count complete `R`-cosets grouped by those literal patterns and suffix weight `b`. There are `6*6*6*3=648` nonnegative variables. The grouping forgets the actual coset labels, suffix letters, and global linearity, so it is a necessary relaxation.

The resulting split-weight system has 375 cells and 70 equalities. A Farkas certificate using the signed-shadow nonnegativity constraints gives

```text
lambda >= 0,
c = lambda G + nu M >= 0 on all 648 columns,
nu dot rhs = -125829120.
```

The equality rows include the same global weight equations used in Section 5.6: `A_1=A_2=A_3=0` and the branch assumption `A_4=3`. They do not follow from containment of the disjoint subgroup alone. All 648 residual coefficients are nonnegative (403 positive and 245 zero), so the exact Farkas certificate excludes this final geometry as well.

**Lemma 3 (unique weight-four check).** Every binary `[[14,3,d>=5]]` stabilizer would have exactly one stabilizer word of weight four. This follows from the parity restriction of Section 4 and the exclusions in Section 5.

## 6. Reduction to a ten-site additive code

Let `p` be the unique weight-four stabilizer word. Physical local Clifford conjugation and a site permutation put

```text
p = Z_0 Z_1 Z_2 Z_3,
```

on the first four original qubits. Write `V_4` for their Pauli space and `W_10` for the remaining ten-qubit Pauli space, so `V_14=V_4 orthogonal-sum W_10`.

Define the physical six-dimensional quotient

```text
E = (p^perp intersect V_4) / <p>.
```

The quotient is nondegenerate symplectic: `p^perp intersect V_4` has binary dimension seven, and quotienting by its one-dimensional radical `<p>` leaves dimension six.

Since `S intersect V_4=<p>`, projection of `S/<p>` to `W_10` is injective. Let its image be a binary ten-space `P<=W_10`. Then there is a linear map `T:P->E` such that

```text
S/<p> = { T(x)+x : x in P },
<x,y>_W = <T(x),T(y)>_E.
```

### 6.1 Distance forces surjectivity

Suppose `z in E` is orthogonal to `im(T)`. Choose a four-site representative `v` of `z` in `p^perp`. It commutes with `p` and with every element of the graph, hence `v in S^perp`. Its original physical weight is at most four. Distance at least five forces `v in S`. But `S intersect V_4=<p>`, so `z=0`. Therefore

```text
im(T)=E,   rank(T)=6,   dim ker(T)=10-6=4.
```

Surjectivity also identifies the radical of the pairing on `P`:

```text
rad(P)=P intersect P^perp_W=ker(T),   dim rad(P)=4.
```

Put

```text
C = P^perp_W.
```

Then `dim C=10`, so `|C|=1024`. If a nonzero `c in C` had physical weight at most four, the suffix-only vector `(0,c)` would be in `S^perp` and distance would force it into `S`; the unique-shortest-check condition then makes this impossible. Thus `d(C)>=5`. Because `C^perp=P`,

```text
dim(C intersect C^perp_W)=dim(P intersect C)=4.
```

**Lemma 4 (ten-site reduction).** A binary `[[14,3,d>=5]]` stabilizer with a unique weight-four check would induce an additive length-ten code `C` with `|C|=1024`, `d(C)>=5`, and `dim Hull(C)=4`. No `GF(4)`-linearity assumption is used.

### 6.2 A necessary coset-capacity bound

Let `J=C intersect C^perp_W`, so `dim J=4`, and let `P=C^perp_W`. The quotient `P/J` is a nondegenerate six-dimensional symplectic space. Also `J^perp_W/C` has 64 suffix cosets. For each quotient label `q`, let `d(q)` be the minimum original ten-site physical weight in that coset.

The four-site quotient `E` has physical prefix-class cost distribution

```text
cost 0: 1,   cost 1: 4,   cost 2: 27,   cost 3: 24,   cost 4: 8.
```

Every compatible graph map is a symplectic isomorphism `P/J -> E`, equivalently an ordered symplectic basis of `E`. For the image `e(q)`, the mixed centralizer fibre has minimum physical weight `d(q)+cost(e(q))`. Consequently a necessary condition is `d(q)+cost(e(q))>=5` for every nonzero `q`.

Before enumerating the `1,451,520` ordered symplectic bases, this gives the physical Hall capacities

```text
#{q != 0 : d(q)<=1} <= 8,
#{q != 0 : d(q)<=2} <= 32,
#{q != 0 : d(q)<=3} <= 59.
```

The capacities are the numbers of nonzero prefix classes of cost at least 4, 3, and 2, respectively. The Hall bounds follow by relaxing the required linear symplectic isomorphism to an arbitrary bijection between the 63 nonzero suffix cosets and the 63 nonzero prefix classes. Failure of these relaxed bounds excludes every physical symplectic lift; passing them does not establish that such a lift exists.

## 7. Exhaustive additive-code classification

### 7.1 What is classified

Represent a quaternary symbol by two binary bits. A length-`n` additive code is a binary subspace of `F_2^(2n)`, with quaternary Hamming weight equal to physical Pauli weight. Equivalence is coordinate permutation plus an arbitrary local `GL(2,2)` map on each two-bit symbol plane. This is exactly the binary local symplectic monomial equivalence relevant here. No global `GF(4)` scalar-linearity is assumed.

Grassl, Krotov, Sok, and Solé report 37 equivalence classes in the `(n,k)=(10,10)` cell of their additive `(n,2^k,>=5)_4` classification (Section 2.3, Table 1 of *The punctured dodecacode is unique*). Their paper reports the count, not the 37 generator matrices. We reconstruct the representatives using the described lengthening method.

### 7.2 Why the lengthening census is exhaustive for this cell

Shortening a target code at its last coordinate changes binary dimension by `r in {0,1,2}`. Conversely, lengthening a parent of length `m` and binary dimension `k` uses one new coordinate of rank `r`:

* `r=0`: append a zero coordinate;
* `r=1`: choose one quotient coset of the parent whose old minimum weight is at least four and attach a nonzero new symbol;
* `r=2`: choose two quotient labels whose three nonzero XOR combinations all have old minimum weight at least four and attach independent new symbols.

The threshold four is exact: a word with nonzero new symbol gains one physical unit of weight, while a word with zero new symbol is already a distance-five parent. Thus every target code appears in one of these three cases.

The reconstructed counts for the predecessor cells and the target cell are:

| length `n` | checked binary dimensions `k: count` |
|---:|---|
| 5 | `0:1, 1:1, 2:1, 3:0, 4:0` |
| 6 | `2:5, 3:1, 4:0, 5:0, 6:0` |
| 7 | `4:43, 5:1, 6:0, 7:0, 8:0` |
| 8 | `6:1579, 7:0, 8:0, 9:0, 10:0` |
| 9 | `8:2298, 9:0, 10:0` |
| 10 | `10:37` |

The high-rate zero predecessor cells are explicitly installed and checked; they are not silently interpreted as missing dictionary entries. Therefore the recurrence covers every source cell that can feed `(10,10)`.

### 7.3 Exact equivalence certificates

For every candidate the census constructs a colored incidence graph with one vertex for every codeword, three nonzero-symbol vertices for every coordinate, and one coordinate-group vertex binding each triple of symbols. The colors separate the three vertex types. A color-preserving graph isomorphism is exactly a codeword reorder, a coordinate permutation, and an arbitrary permutation of the three nonzero symbols in each coordinate. The latter is `GL(2,2)`. The final `pynauty` certificate is therefore an exact additive-monomial equivalence certificate; the weight and pair-rank invariants are only performance filters. The graph-isomorphism implementation is based on nauty [McKay and Piperno (2014)].

### 7.4 Hull and physical Hall results

The enumeration produces 37 generator matrices, each defining 1,024 words of minimum distance five. Independent exact checks recompute their ranks, distances, hull dimensions and coset minima. The hull dimensions are

| binary symplectic hull dimension | number of classes |
|---:|---:|
| 0 | 7 |
| 2 | 14 |
| 4 | 12 |
| 6 | 2 |
| 8 | 2 |

The 25 classes with hull dimension different from four cannot arise from Stage II. For the 12 hull-four classes, the exact physical quotient audit gives:

| class | suffix spectrum `{weight:count}` | `N<=1` | `N<=2` | `N<=3` | result |
|---:|---|---:|---:|---:|---|
| 9 | `{0:1,2:39,3:24}` | 0 | 39 | 63 | Hall fail |
| 12 | `{0:1,1:2,2:37,3:24}` | 2 | 39 | 63 | Hall fail |
| 14 | `{0:1,2:39,3:24}` | 0 | 39 | 63 | Hall fail |
| 15 | `{0:1,2:27,3:36}` | 0 | 27 | 63 | Hall fail |
| 17 | `{0:1,1:2,2:37,3:24}` | 2 | 39 | 63 | Hall fail |
| 20 | `{0:1,2:35,3:27,4:1}` | 0 | 35 | 62 | Hall fail |
| 21 | `{0:1,1:2,2:37,3:24}` | 2 | 39 | 63 | Hall fail |
| 22 | `{0:1,2:23,3:40}` | 0 | 23 | 63 | Hall fail |
| 26 | `{0:1,2:35,3:27,4:1}` | 0 | 35 | 62 | Hall fail |
| 34 | `{0:1,1:2,2:37,3:24}` | 2 | 39 | 63 | Hall fail |
| 35 | `{0:1,1:2,2:37,3:24}` | 2 | 39 | 63 | Hall fail |
| 37 | `{0:1,1:2,2:37,3:24}` | 2 | 39 | 63 | Hall fail |

In every row `N_{<=3}` is 62 or 63, exceeding its capacity 59 (and several rows already fail at `N_{<=2}>32`).

**Lemma 5 (additive lift exclusion).** None of the 37 length-ten classes can supply the code in Lemma 4: 25 have a different hull dimension, and the other twelve violate the necessary Hall capacity bound before any search over the full `Sp(6,2)` is needed.

## 8. Discussion and conclusion

Assume a binary `[[14,3,d>=5]]` stabilizer exists. Sections 3 and 4 give `A_1=A_2=A_3=0`, `A_4 in {1,3}`. Sections 5.3-5.5 show that all overlapping weight-four support pairs are physically impossible and classify the three-check case into five support geometries. Section 5.6 excludes the four overlapping rank-three geometries, and Section 5.7 excludes the disjoint `4+4+4+2` geometry. Hence `A_4=1`.

Section 6 then forces a ten-site additive code of size 1,024, distance at least five, and hull dimension four. Section 7 exhausts the 37 equivalence classes of such ten-site additive codes and rejects every one: 25 by hull dimension and 12 by the physical Hall capacity. This contradiction proves Theorem 1.

The known `[[14,3,4]]` construction gives the matching lower bound, so `d_max(14,3)=4`. This determines the optimum distance at these parameters within the stabilizer family. The proof also illustrates how exact signed-shadow certificates can be combined with a smaller additive-code classification, but does not establish a general bound for other lengths, nor does it exclude non-stabilizer quantum codes.

## 9. Computational material

The proof uses exact integer certificates for the necessary split-weight systems and an exhaustive classification of length-ten additive codes. The default replay checks the coefficient identities, Farkas multipliers, physical coset models, saved class representatives and Hall obstructions. It uses the committed representatives; the full lengthening census is a separate, more resource-intensive run. The archived package contains the exact certificate data, generator matrices, verification programs and concise reproduction instructions. No floating-point feasibility result is used as a proof certificate. The [immutable code archive](https://github.com/brandonlign/quantum-code-bounds/archive/c14d6dadf2c5f902d9c149ed992fbac54b63596e.zip) contains the complete computational record.

## References

* J. Bierbrauer, R. Fears, S. Marcugini, and F. Pambianco, “The nonexistence of a `[[13,5,4]]`-quantum stabilizer code,” *IEEE Transactions on Information Theory* 57 (2011), 4788–4793, DOI [10.1109/TIT.2011.2146430](https://doi.org/10.1109/TIT.2011.2146430).
* S. Ball, A. Centelles, and F. Huber, “Quantum error-correcting codes and their geometries,” *Annales de l'Institut Henri Poincaré D: Combinatorics, Physics and Their Interactions* 10 (2023), no. 2, 337–405, DOI [10.4171/AIHPD/160](https://doi.org/10.4171/AIHPD/160). Research Problem 1 states that `[[14,3,5]]` is the smallest qubit stabilizer parameter set whose existence was unknown there.
* M. Grassl, D. Krotov, L. Sok, and P. Solé, “The punctured dodecacode is unique,” *Mathematics and Education in Mathematics* 55 (2026), 393–404, DOI [10.55630/mem.2026.55.393-404](https://doi.org/10.55630/mem.2026.55.393-404). Section 2.3 and Table 1 are the primary source for the published 37-class length-ten additive-code count and the lengthening method.
* B. D. McKay and A. Piperno, “Practical graph isomorphism, II,” *Journal of Symbolic Computation* 60 (2014), 94–112, DOI [10.1016/j.jsc.2013.09.003](https://doi.org/10.1016/j.jsc.2013.09.003).
* M. Grassl, [Bounds on the minimum distance of additive quantum codes, n=14,k=3,q=4](https://codetables.de/QECC.php?k=3&n=14&q=4), maintained code table, accessed 24 September 2026. It records lower bound 4, upper bound 5, and the stored `[[14,3,4]]` construction (last-modified date shown there: 30 June 2005 for that entry).
* A. R. Calderbank, E. M. Rains, P. W. Shor, and N. J. A. Sloane, “Quantum error correction via codes over GF(4),” *IEEE Transactions on Information Theory* 44 (1998), 1369–1387, DOI [10.1109/18.681315](https://doi.org/10.1109/18.681315).
* E. M. Rains, “Quantum weight enumerators,” *IEEE Transactions on Information Theory* 44 (1998), 1388–1394, DOI [10.1109/18.681316](https://doi.org/10.1109/18.681316); and “Quantum shadow enumerators,” *IEEE Transactions on Information Theory* 45 (1999), 2361–2366, DOI [10.1109/18.796376](https://doi.org/10.1109/18.796376).

The `[[14,3,4]]` construction, signed-shadow identities and additive-code classification cited above are prior results. The nonexistence conclusion of Theorem 1 is the result established here.
