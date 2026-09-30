#!/usr/bin/env python3
"""Independent check: disjoint 4+4+4+2 geometry (Section 5.7), rebuilt from text.

R = <ZZZZ on block1, ZZZZ on block2, ZZZZ on block3>, 2 free sites.
Cosets of R in its normalizer factor as products of single-block cosets of
<ZZZZ> in its 4-site normalizer. Split enumerator on 5*5*5*3 cells.
"""
from collections import Counter
from itertools import product
from math import comb
import numpy as np
from scipy.optimize import linprog


def K(n, j, w):
    return sum((-1) ** r * 3 ** (j - r) * comb(w, r) * comb(n - w, j - r)
               for r in range(0, j + 1))


# single block: Paulis (x,z) on 4 sites commuting with ZZZZ  <=> x even weight
blk = Counter()
seen = set()
for x in range(16):
    if x.bit_count() % 2:
        continue
    for z in range(16):
        if (x, z) in seen:
            continue
        seen |= {(x, z), (x, z ^ 15)}
        h = [0] * 5
        for zz in (z, z ^ 15):
            h[(x | zz).bit_count()] += 1
        blk[tuple(h)] += 1
print("single-block patterns:", dict(blk), "total", sum(blk.values()))
pats = sorted(blk)


def run(use_shadow=True, global_eq=True):
    cells = list(product(range(5), range(5), range(5), range(3)))
    ci = {c: i for i, c in enumerate(cells)}
    cols = list(product(range(len(pats)), repeat=3))
    nv = len(cols) * 3
    H = np.zeros((len(cells), nv))
    for k, (i, j, l) in enumerate(cols):
        for b in range(3):
            for a1, m1 in enumerate(pats[i]):
                for a2, m2 in enumerate(pats[j]):
                    for a3, m3 in enumerate(pats[l]):
                        if m1 * m2 * m3:
                            H[ci[(a1, a2, a3, b)], 3 * k + b] += m1 * m2 * m3
    L = [4, 4, 4, 2]
    Kt = np.array([[np.prod([K(n, a, w) for n, a, w in zip(L, c, d)])
                    for d in cells] for c in cells], dtype=float)
    sgn = np.array([(-1) ** sum(d) for d in cells])
    T = Kt @ H
    SH = (Kt * sgn) @ H
    tot = np.array([sum(c) for c in cells])
    Aeq = [H[ci[(0, 0, 0, 0)]], H.sum(0)]
    beq = [1, 2048]
    for i in range(len(cells)):
        if 1 <= tot[i] <= 4:
            Aeq.append((T[i] - 2048 * H[i]) / 2048); beq.append(0)
    if global_eq:
        for w, v in {1: 0, 2: 0, 3: 0, 4: 3}.items():
            Aeq.append(H[tot == w].sum(0)); beq.append(v)
    Aub, bub = [], []
    for i in range(len(cells)):
        Aub += [(2048 * H[i] - T[i]) / 2048, -T[i] / 2048]
        bub += [0, 0]
        if use_shadow:
            Aub.append(-SH[i] / 2048); bub.append(0)
    r = linprog(np.zeros(nv), A_ub=np.array(Aub), b_ub=bub,
                A_eq=np.array(Aeq), b_eq=beq, bounds=(0, None), method="highs")
    return {0: "FEASIBLE", 2: "INFEASIBLE"}.get(r.status, r.status), nv


for sh, ge in ((True, True), (False, True), (True, False)):
    print(f"disjoint 4+4+4+2 shadow={sh} globalA={ge}:", run(sh, ge))
