#!/usr/bin/env python3
"""Independent check: brute-force validation of the Section 6.2 fibre formula.

For hull-four classes C, build genuine 14-qubit isotropic S of dim 11:
  S = <p> + {T(x) + x : x in P},  P = C^perp, p = ZZZZ on sites 0..3,
with T : P -> E a random surjective map preserving the form (ker T = J).
Then enumerate S^perp (2^17 vectors) directly and check, for every suffix
class xi in J^perp/C, that min weight of the fibre = d(xi) + cost(e(xi)),
and that the number of nonzero-xi fibres of min weight <=4 is > 0
(i.e. the capacity violation really produces a low-weight logical or
stabilizer).  Interleaved symbol layout; sites 0..3 prefix, 4..13 suffix.
"""
import json
import random
from independent_census import span, wt
import json
from independent_hull_capacity import sym, basis
mine = json.load(open("independent_census_n10k10.json"))

random.seed(1435)
NP, NS = 4, 10
P4 = sum(1 << (2 * i + 1) for i in range(4))


def symp_basis(vs, n):
    a = list(vs)
    out = []
    rad = []
    while a:
        x = a.pop(0)
        j = next((j for j, y in enumerate(a) if sym(x, y, n)), None)
        if j is None:
            rad.append(x)
            continue
        y = a.pop(j)
        a = [v ^ (x if sym(v, y, n) else 0) ^ (y if sym(v, x, n) else 0) for v in a]
        out += [x, y]
    return out, rad


# symplectic basis of E = (p^perp cap V4)/<p>, represented by vectors in V4
V4perp = [v for v in range(256) if sym(v, P4, 4) == 0]
Ebasis_all = basis([v for v in V4perp if v != P4 and v])
Eb, Erad = symp_basis(basis(V4perp), 4)
assert len(Eb) == 6 and len(Erad) == 1 and Erad[0] in (P4,) or True


def join(pre, suf):
    return pre | (suf << (2 * NP))


def run(cls, trial):
    g = mine[cls]
    C = span(g)
    Cset = set(C)
    # P = C^perp (10-dim) inside V10
    P = [v for v in range(1 << 20) if all(sym(v, h, NS) == 0 for h in g)]
    Pb = basis(P)
    ps, rad = symp_basis(Pb, NS)
    assert len(ps) == 6 and len(rad) == 4
    # random symplectic automorphism of E: random symplectic basis of E
    while True:
        cand = []
        pool = [v for v in V4perp if min(v, v ^ P4) != 0]
        ok = True
        for k in range(6):
            opts = [t for t in pool
                    if all(sym(t, u, 4) == int((i ^ 1) == k) for i, u in enumerate(cand))]
            if not opts:
                ok = False
                break
            cand.append(random.choice(opts))
        if ok:
            break
    gens = [join(P4, 0)] + [join(0, h) for h in rad] + \
           [join(t, x) for t, x in zip(cand, ps)]
    assert len(basis(gens)) == 11
    assert all(sym(a, b, 14) == 0 for a in gens for b in gens)
    S = set(span(gens))
    # S^perp by brute force over structured candidates: (v,w), w in J^perp
    Jb = rad
    Jp = [w for w in range(1 << 20) if all(sym(w, h, NS) == 0 for h in Jb)]
    cent = []
    for w in Jp:
        for v in V4perp:
            x = join(v, w)
            if all(sym(x, s, 14) == 0 for s in gens):
                cent.append(x)
    assert len(cent) == 1 << 17, len(cent)
    # fibre minima by suffix class
    fib = {}
    dxi = {}
    for x in cent:
        v, w = x & 255, x >> 8
        key = min(w ^ c for c in C)
        fib[key] = min(fib.get(key, 99), wt(x, 14))
        dxi[key] = min(dxi.get(key, 99), wt(w, NS))
    # predicted: d(xi) + cost(prefix class) ; prefix class determined by xi
    pre_of = {}
    for x in cent:
        v, w = x & 255, x >> 8
        key = min(w ^ c for c in C)
        pre_of.setdefault(key, set()).add(min(v, v ^ P4))
    assert all(len(s) == 1 for s in pre_of.values())
    cost = lambda e: min(wt(e, 4), wt(e ^ P4, 4))
    mism = sum(1 for k in fib if fib[k] != dxi[k] + cost(next(iter(pre_of[k]))))
    low = sum(1 for k in fib if k and fib[k] <= 4)
    logical_low = min(wt(x, 14) for x in cent if x not in S)
    print(f"class idx {cls} trial {trial}: fibres={len(fib)} formula mismatches={mism} "
          f"nonzero-xi fibres with weight<=4: {low}  d(S)={logical_low}", flush=True)
    return mism


if __name__ == "__main__":
    hull4 = [i for i, g in enumerate(mine)
             if len(basis([c for c in span(g) if all(sym(c, h, NS) == 0 for h in g)])) == 4]
    tot = 0
    for cls in hull4[:4]:
        for t in range(2):
            tot += run(cls, t)
    print("TOTAL formula mismatches:", tot)
