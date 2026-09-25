#!/usr/bin/env python3
"""FULLY INDEPENDENT re-verification of the length-ten additive data.

Written from the mathematical statements in the manuscript alone, not by
reusing any repository helper.  Checks, for each of the 37 committed
representatives:

  * binary dimension 10 and |C| = 1024
  * minimum quaternary (Pauli) weight
  * symplectic hull dimension dim(C cap C^perp)
  * the 64 coset leaders of J^perp / C, J = hull
  * the three Hall capacities  N_{<=1}<=8, N_{<=2}<=32, N_{<=3}<=59

and independently recomputes the prefix cost distribution on
(p^perp cap V4)/<p> for p = ZZZZ.

Layout of a stored generator: 20-bit integer, X part in bits 0..9,
Z part in bits 10..19.
"""
from collections import Counter
from itertools import combinations
import json
import sys

N = 10


def wt(v):
    """Quaternary/Pauli weight of a 2N-bit label."""
    m = (1 << N) - 1
    return bin((v & m) | ((v >> N) & m)).count("1")


def symp(a, b):
    """Trace-symplectic form x.z' + z.x'."""
    m = (1 << N) - 1
    return (bin((a & m) & ((b >> N) & m)).count("1")
            + bin(((a >> N) & m) & (b & m)).count("1")) & 1


def span(gens):
    out = [0]
    for g in gens:
        out = out + [x ^ g for x in out]
    return out


def rank2(vectors, width):
    piv = {}
    r = 0
    for v in vectors:
        x = v
        while x:
            b = x.bit_length() - 1
            if b in piv:
                x ^= piv[b]
            else:
                piv[b] = x
                r += 1
                break
    return r


def dual_space(gens):
    """Basis of the symplectic dual {y : <y,g>=0 for all g}, brute nullspace."""
    width = 2 * N
    # row for generator g acting on unknown y: coefficients of y bits
    rows = []
    for g in gens:
        m = (1 << N) - 1
        gx, gz = g & m, (g >> N) & m
        # <y,g> = y_x . g_z + y_z . g_x
        rows.append(gz | (gx << N))
    # solve rows . y = 0
    work = list(rows)
    piv = []
    r = 0
    for col in range(width):
        k = next((i for i in range(r, len(work)) if (work[i] >> col) & 1), None)
        if k is None:
            continue
        work[r], work[k] = work[k], work[r]
        for i in range(len(work)):
            if i != r and ((work[i] >> col) & 1):
                work[i] ^= work[r]
        piv.append(col)
        r += 1
    out = []
    for f in range(width):
        if f in piv:
            continue
        y = 1 << f
        for i, pc in enumerate(piv):
            if (work[i] >> f) & 1:
                y |= 1 << pc
        out.append(y)
    for y in out:
        assert all(symp(y, g) == 0 for g in gens)
    return out


def prefix_cost_distribution():
    """cost on (p^perp cap V4)/<p>, p = ZZZZ, independent enumeration."""
    n = 4

    def w4(v):
        m = (1 << n) - 1
        return bin((v & m) | ((v >> n) & m)).count("1")

    def s4(a, b):
        m = (1 << n) - 1
        return (bin((a & m) & ((b >> n) & m)).count("1")
                + bin(((a >> n) & m) & (b & m)).count("1")) & 1

    p = ((1 << n) - 1) << n          # ZZZZ
    perp = [v for v in range(1 << (2 * n)) if s4(v, p) == 0]
    assert len(perp) == 128
    classes = {min(v, v ^ p) for v in perp}
    assert len(classes) == 64
    return Counter(min(w4(v), w4(v ^ p)) for v in classes)


def audit_code(gens):
    assert len(gens) == 10
    assert rank2(gens, 2 * N) == 10
    C = span(gens)
    assert len(set(C)) == 1024
    d = min(wt(v) for v in C if v)

    # hull
    hull = [c for c in C if all(symp(c, g) == 0 for g in gens)]
    hdim = rank2(hull, 2 * N)
    assert len(hull) == 1 << hdim

    result = {"d": d, "hull_dim": hdim}
    if hdim != 4:
        return result

    # J^perp where J = hull
    hbasis = []
    piv = {}
    for v in hull:
        x = v
        while x:
            b = x.bit_length() - 1
            if b in piv:
                x ^= piv[b]
            else:
                piv[b] = x
                hbasis.append(v)
                break
    assert len(hbasis) == 4
    Jperp = span(dual_space(hbasis))
    assert len(Jperp) == 1 << 16

    Cset = set(C)
    # coset leaders of J^perp / C
    leaders = {}
    for v in Jperp:
        key = min(v ^ c for c in C)      # canonical coset key
        wv = wt(v)
        if key not in leaders or wv < leaders[key]:
            leaders[key] = wv
    assert len(leaders) == 64, len(leaders)
    assert leaders[0] == 0

    spec = Counter(leaders.values())
    nz = [w for k, w in leaders.items() if k != 0]
    n1 = sum(1 for w in nz if w <= 1)
    n2 = sum(1 for w in nz if w <= 2)
    n3 = sum(1 for w in nz if w <= 3)
    result.update({
        "spectrum": dict(sorted(spec.items())),
        "N_le1": n1, "N_le2": n2, "N_le3": n3,
        "hall_ok": (n1 <= 8 and n2 <= 32 and n3 <= 59),
    })
    return result


def main():
    cost = prefix_cost_distribution()
    print("independent prefix cost distribution:", dict(sorted(cost.items())))
    assert dict(cost) == {0: 1, 1: 4, 2: 27, 3: 24, 4: 8}
    cap1 = sum(v for k, v in cost.items() if k >= 4)
    cap2 = sum(v for k, v in cost.items() if k >= 3)
    cap3 = sum(v for k, v in cost.items() if k >= 2)
    print(f"independent Hall capacities: N<=1 -> {cap1}, N<=2 -> {cap2}, N<=3 -> {cap3}")
    assert (cap1, cap2, cap3) == (8, 32, 59)

    path = sys.argv[1] if len(sys.argv) > 1 else \
        "experiments/qec1435_n10_additive_37_generators_xy.json"
    gens_list = json.load(open(path))
    print(f"\nloaded {len(gens_list)} representatives from {path}")

    hull_counts = Counter()
    dist_counts = Counter()
    hall_fail = 0
    hull4 = 0
    rows = []
    for i, gens in enumerate(gens_list, 1):
        r = audit_code(gens)
        hull_counts[r["hull_dim"]] += 1
        dist_counts[r["d"]] += 1
        if r["hull_dim"] == 4:
            hull4 += 1
            if not r["hall_ok"]:
                hall_fail += 1
            rows.append((i, r))
    print("distances:", dict(sorted(dist_counts.items())))
    print("hull dimensions:", dict(sorted(hull_counts.items())))
    print(f"\nhull-four classes: {hull4}; Hall failures: {hall_fail}")
    print(f"{'class':>6} {'N<=1':>5} {'N<=2':>5} {'N<=3':>5}  spectrum")
    for i, r in rows:
        print(f"{i:>6} {r['N_le1']:>5} {r['N_le2']:>5} {r['N_le3']:>5}  {r['spectrum']}")

    # pairwise distinctness of the committed representatives as codebooks
    books = [frozenset(span(g)) for g in gens_list]
    print(f"\ndistinct codebooks among representatives: {len(set(books))}")

    ok = (hull4 == 12 and hall_fail == 12
          and dict(hull_counts) == {0: 7, 2: 14, 4: 12, 6: 2, 8: 2})
    print("\nINDEPENDENT AUDIT:", "PASS" if ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
