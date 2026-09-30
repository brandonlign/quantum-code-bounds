#!/usr/bin/env python3
"""Independent check: rebuild of every Section-5 relaxation.

Built from the manuscript's description only (no repository code).
Sites are partitioned into blocks; the split enumerator is indexed by the
tuple of block weights. R is a subgroup on the prefix blocks; its cosets in
the prefix normalizer are grouped by their histogram of prefix block-weight
tuples. Variables y[pattern, b] (b = suffix weight). Constraints:
  H_0 = 1, sum H = 2048, T = 2048 H on total weight 1..4,
  2048 H <= T, T >= 0, SH >= 0 on every cell, optional global A_w values.
Feasibility solved with HiGHS; infeasible => relaxation excluded.
Also runs "control" variants (dropping shadow) to see which rows matter.
"""
import sys
from collections import Counter
from itertools import product
from math import comb
import numpy as np
from scipy.optimize import linprog


def K(n, j, w):
    return sum((-1) ** r * 3 ** (j - r) * comb(w, r) * comb(n - w, j - r)
               for r in range(0, j + 1))


def parse(word):
    x = z = 0
    for i, c in enumerate(word):
        if c in "XY":
            x |= 1 << i
        if c in "ZY":
            z |= 1 << i
    return x, z


def patterns(u, gens, blocks):
    """Cosets of R=<gens> in its normalizer inside V_u, grouped by histogram
    of block-weight tuples. blocks: list of site lists partitioning range(u)."""
    G = [parse(g) for g in gens]
    R = {(0, 0)}
    for gx, gz in G:
        R |= {(a ^ gx, b ^ gz) for a, b in R}
    R = sorted(R)
    bm = [sum(1 << s for s in blk) for blk in blocks]

    def comm(x, z):
        return all(((x & gz).bit_count() + (z & gx).bit_count()) % 2 == 0
                   for gx, gz in G)
    seen = set()
    pats = Counter()
    for x in range(1 << u):
        for z in range(1 << u):
            if (x, z) in seen or not comm(x, z):
                continue
            hist = Counter()
            for rx, rz in R:
                v = (x ^ rx, z ^ rz)
                seen.add(v)
                s = v[0] | v[1]
                hist[tuple((s & m).bit_count() for m in bm)] += 1
            pats[tuple(sorted(hist.items()))] += 1
    return pats, len(R)


def build(u, gens, blocks, extra_eq=None, use_shadow=True, n=14):
    f = n - u
    pats, rsize = patterns(u, gens, blocks)
    blens = [len(b) for b in blocks] + [f]
    cells = list(product(*[range(L + 1) for L in blens]))
    cidx = {c: i for i, c in enumerate(cells)}
    plist = sorted(pats)
    nv = len(plist) * (f + 1)
    H = np.zeros((len(cells), nv))
    for k, pat in enumerate(plist):
        for b in range(f + 1):
            for key, mult in pat:
                H[cidx[key + (b,)], k * (f + 1) + b] += mult
    # transform matrix on cells
    Kt = np.zeros((len(cells), len(cells)))
    Ks = np.zeros((len(cells), len(cells)))
    for i, a in enumerate(cells):
        for j, w in enumerate(cells):
            val = 1
            for L, aa, ww in zip(blens, a, w):
                val *= K(L, aa, ww)
            Kt[i, j] = val
            Ks[i, j] = val * (-1) ** sum(w)
    T = Kt @ H
    SH = Ks @ H
    tot = np.array([sum(c) for c in cells])
    Aeq, beq, Aub, bub = [], [], [], []
    Aeq.append(H[cidx[(0,) * len(blens)]]); beq.append(1)
    Aeq.append(H.sum(0)); beq.append(2048)
    for i in range(len(cells)):
        if 1 <= tot[i] <= 4:
            Aeq.append((T[i] - 2048 * H[i]) / 2048); beq.append(0)
    for w, val in (extra_eq or {}).items():
        Aeq.append(H[tot == w].sum(0)); beq.append(val)
    for i in range(len(cells)):
        Aub.append((2048 * H[i] - T[i]) / 2048); bub.append(0)
        Aub.append(-T[i] / 2048); bub.append(0)
        if use_shadow:
            Aub.append(-SH[i] / 2048); bub.append(0)
    res = linprog(np.zeros(nv), A_ub=np.array(Aub), b_ub=bub,
                  A_eq=np.array(Aeq), b_eq=beq, bounds=(0, None),
                  method="highs")
    return res.status, len(plist), nv, sum(pats.values()), rsize


CASES = {
    "weight2 ZZ": (2, ["ZZ"], [[0, 1]], None),
    "weight3 ZZZ": (3, ["ZZZ"], [[0, 1, 2]], None),
    "bell XXXX,ZZZZ": (4, ["XXXX", "ZZZZ"], [[0, 1, 2, 3]], None),
    "5site overlap": (5, ["XXZZI", "ZZZIZ"], [list(range(5))], None),
    "6site same-letter": (6, ["ZZZZII", "ZZIIZZ"], [list(range(6))], None),
    "6site crossed": (6, ["ZZZZII", "XXIIXX"], [list(range(6))], None),
}
G3 = {1: 0, 2: 0, 3: 0, 4: 3}


def zword(u, sup):
    return "".join("Z" if i in sup else "I" for i in range(u))


for name, sets in {
    "rank3 triangle": ((0, 1, 2, 3), (3, 4, 5, 6), (2, 4, 7, 8)),
    "rank3 common": ((0, 1, 2, 3), (3, 4, 5, 6), (3, 7, 8, 9)),
    "rank3 two": ((0, 1, 2, 3), (3, 4, 5, 6), (6, 7, 8, 9)),
    "rank3 one": ((0, 1, 2, 3), (3, 4, 5, 6), (7, 8, 9, 10)),
}.items():
    u = max(max(s) for s in sets) + 1
    CASES[name] = (u, [zword(u, s) for s in sets], [list(range(u))], G3)

if __name__ == "__main__":
    only = sys.argv[1:] or list(CASES)
    status_name = {0: "FEASIBLE", 2: "INFEASIBLE"}
    for name in only:
        u, gens, blocks, eq = CASES[name]
        for shadow in (True, False):
            st, npat, nv, ncos, rs = build(u, gens, blocks, eq, shadow)
            print(f"{name:20s} shadow={shadow!s:5s} cosets={ncos} |R|={rs} "
                  f"patterns={npat} vars={nv} -> {status_name.get(st, st)}",
                  flush=True)
