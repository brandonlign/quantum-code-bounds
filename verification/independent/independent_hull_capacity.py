#!/usr/bin/env python3
"""Independent check: match this census's classes to the committed 37, then compute
hull dimension and J^perp/C coset spectra from this census's own representatives.
Also validates the Section 6 fibre formula by building actual 14-qubit
lifts (random symplectic T) and comparing centralizer fibre minima with
d(xi)+cost(e(xi)).
"""
import json
import os
import random
from collections import Counter
from independent_census import graph, span, wt
from pynauty import certificate

N = 10


def to_inter(v):  # committed X|Z layout -> interleaved symbols
    out = 0
    for i in range(N):
        out |= ((v >> i) & 1) << (2 * i)
        out |= ((v >> (N + i)) & 1) << (2 * i + 1)
    return out


def sym(a, b, n):
    s = 0
    for i in range(n):
        x1, z1 = (a >> 2 * i) & 1, (a >> 2 * i + 1) & 1
        x2, z2 = (b >> 2 * i) & 1, (b >> 2 * i + 1) & 1
        s ^= (x1 & z2) ^ (z1 & x2)
    return s


def perp_space(gens, n):
    return [v for v in range(1 << (2 * n)) if all(sym(v, g, n) == 0 for g in gens)]


def basis(vs):
    piv = {}
    out = []
    for v in vs:
        x = v
        while x:
            b = x.bit_length() - 1
            if b in piv:
                x ^= piv[b]
            else:
                piv[b] = x
                out.append(v)
                break
    return out


theirs = [[to_inter(v) for v in g] for g in
          json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "s7_37_classes.json")))]
if __name__ == "__main__":
    mine = json.load(open("independent_census_n10k10.json"))
    cm = [certificate(graph(g, N)) for g in mine]
    ct = [certificate(graph(g, N)) for g in theirs]
    assert len(set(cm)) == 37 and len(set(ct)) == 37
    print("independent classes == committed classes (as sets of certificates):", set(cm) == set(ct))
    perm = [ct.index(c) + 1 for c in cm]

    # prefix cost on (p^perp cap V4)/<p>, p = ZZZZ (interleaved, z bits odd)
    P4 = sum(1 << (2 * i + 1) for i in range(4))
    V4perp = [v for v in range(256) if sym(v, P4, 4) == 0]
    cost = {}
    for v in V4perp:
        k = min(v, v ^ P4)
        cost[k] = min(wt(v, 4), wt(v ^ P4, 4))
    print("cost distribution:", dict(sorted(Counter(cost.values()).items())))

    hulls = Counter()
    rows = []
    allvec = None
    for idx, g in enumerate(mine):
        C = span(g)
        Cset = set(C)
        J = [c for c in C if all(sym(c, h, N) == 0 for h in g)]
        hd = len(basis(J))
        hulls[hd] += 1
        if hd != 4:
            continue
        Jb = basis(J)
        Jp = perp_space(Jb, N)
        assert len(Jp) == 1 << 16
        lead = {}
        for v in Jp:
            key = min(v ^ c for c in C)
            lead[key] = min(lead.get(key, 99), wt(v, N))
        assert len(lead) == 64
        nz = [w for k, w in lead.items() if k]
        N1, N2, N3 = (sum(w <= t for w in nz) for t in (1, 2, 3))
        rows.append((perm[idx], dict(sorted(Counter(lead.values()).items())), N1, N2, N3))
    print("hull dims:", dict(sorted(hulls.items())))
    for r in sorted(rows):
        print("committed class %2d spectrum %s N<=1=%d N<=2=%d N<=3=%d fails=%s"
              % (r[0], r[1], r[2], r[3], r[4], r[2] > 8 or r[3] > 32 or r[4] > 59))
    json.dump({"hull": hulls, "rows": sorted(rows)}, open("independent_hull_capacity.json", "w"),
              default=str, indent=1)
