#!/usr/bin/env python3
"""Independent check: independent lengthening census + orbit-stabilizer mass check.

Codes: binary subspaces of F2^(2n); symbol i = bits (2i, 2i+1).
Equivalence: coordinate permutation + any permutation of the 3 nonzero
symbols per coordinate (= GL(2,2)), which also preserves the symplectic form.

Graph encoding (different from the one in ../s7_census.py): vertices = codewords (color 0)
and (coord, nonzero symbol) (color 1); codeword -- symbol vertex if the word
has that symbol at that coord; the three symbol vertices of one coordinate
form a triangle. Codeword vertices are pairwise non-adjacent, so triangles in
color 1 are exactly the coordinate triples.

Mass check (Kaski-Ostergard style), independent of published counts:
  #labelled codes in (m+1,k) = sum_{r} sum_{parent classes P in (m,k-r)}
        (m! 6^m / |Aut P|) * ext_r(P)
  with ext_0 = 1, ext_1 = 3 * #deep cosets, ext_2 = #ordered pairs (a,b)
  of distinct nonzero deep quotient labels with a^b deep,
  and must equal sum_{classes D in (m+1,k)} (m+1)! 6^(m+1) / |Aut D|.
Each labelled D is counted exactly once on the left (its shortening at the
last coordinate, and the data (r, labels, symbols) are determined by D).
"""
import json
import sys
from fractions import Fraction
from itertools import combinations, product
from math import factorial
from pynauty import Graph, certificate, autgrp

D = 5  # target minimum distance


def span(g):
    out = [0]
    for v in g:
        out += [x ^ v for x in out]
    return out


def wt(v, n):
    return sum(1 for i in range(n) if (v >> (2 * i)) & 3)


def rref(vs):
    piv = {}
    for v in vs:
        x = v
        for b in sorted(piv, reverse=True):
            if (x >> b) & 1:
                x ^= piv[b]
        if x:
            b = x.bit_length() - 1
            for bb in list(piv):
                if (piv[bb] >> b) & 1:
                    piv[bb] ^= x
            piv[b] = x
    return piv


def quotient_labels(gens, n):
    """Label map F2^(2n) -> F2^(2n-k) with kernel <gens>: reduce by RREF,
    then compress the non-pivot bits. Returns function label(v)."""
    piv = rref(gens)
    free = [b for b in range(2 * n) if b not in piv]
    pivs = sorted(piv, reverse=True)

    def label(v):
        x = v
        for b in pivs:
            if (x >> b) & 1:
                x ^= piv[b]
        out = 0
        for i, b in enumerate(free):
            if (x >> b) & 1:
                out |= 1 << i
        return out

    def lift(lab):
        x = 0
        for i, b in enumerate(free):
            if (lab >> i) & 1:
                x |= 1 << b
        return x
    return label, lift, len(free)


def light_errors(n, maxw):
    for w in range(maxw + 1):
        for sites in combinations(range(n), w):
            for syms in product((1, 2, 3), repeat=w):
                yield sum(s << (2 * i) for i, s in zip(sites, syms))


def graph(gens, n):
    words = span(gens)
    W = len(words)
    adj = {v: [] for v in range(W + 3 * n)}
    for r, w in enumerate(words):
        for i in range(n):
            s = (w >> (2 * i)) & 3
            if s:
                adj[r].append(W + 3 * i + s - 1)
    for i in range(n):
        a, b, c = (W + 3 * i + t for t in range(3))
        adj[a] += [b, c]
        adj[b] += [c]
    return Graph(W + 3 * n, directed=False, adjacency_dict=adj,
                 vertex_coloring=[set(range(W)), set(range(W, W + 3 * n))])


def aut_order(g):
    _, s1, s2, _, _ = autgrp(g)
    return round(s1 * 10 ** s2)


def extensions(gens, n):
    """All extensions of parent (length n) to length n+1 keeping d>=D.
    Returns (list of (r, new gens)), ext counts per r."""
    label, lift, q = quotient_labels(gens, n)
    covered = {label(e) for e in light_errors(n, D - 2)}
    deep = [a for a in range(1 << q) if a not in covered]
    deepset = set(deep)
    out = {0: [list(gens)], 1: [], 2: []}
    top = 2 * n
    for a in deep:
        out[1].append(list(gens) + [lift(a) | (1 << top)])
    ordered_pairs = 0
    for i, a in enumerate(deep):
        for b in deep:
            if b != a and (a ^ b) in deepset:
                ordered_pairs += 1
                if b > a:
                    out[2].append(list(gens) + [lift(a) | (1 << top),
                                                lift(b) | (2 << top)])
    ext = {0: 1, 1: 3 * len(deep), 2: ordered_pairs}
    return out, ext


def main(maxn=10, target_k=10):
    # cells[(n,k)] = list of (gens, |Aut|)
    need = set()
    for n in range(maxn, 3, -1):
        pass
    # required cells: (n,k) with k >= target_k - 2*(maxn-n), k <= 2n, k>=0
    cells = {(4, 0): [([], aut_order(graph([], 4)))]}
    assert cells[(4, 0)][0][1] == factorial(4) * 6 ** 4
    report = []
    for n in range(5, maxn + 1):
        ks = [k for k in range(0, 2 * n + 1)
              if k >= target_k - 2 * (maxn - n) and k <= target_k]
        for k in ks:
            classes = {}
            lhs = Fraction(0)
            for r in (0, 1, 2):
                for gens, aut in cells.get((n - 1, k - r), []):
                    exts, ext = extensions(gens, n - 1)
                    lhs += Fraction(factorial(n - 1) * 6 ** (n - 1), aut) * ext[r]
                    for g in exts[r]:
                        G = graph(g, n)
                        c = certificate(G)
                        if c not in classes:
                            classes[c] = (g, aut_order(G))
            lst = list(classes.values())
            for g, a in lst:
                assert (factorial(n) * 6 ** n) % a == 0
                ws = [wt(v, n) for v in span(g) if v]
                assert not ws or min(ws) >= D
                assert len(span(g)) == 1 << k
            rhs = sum(Fraction(factorial(n) * 6 ** n, a) for _, a in lst)
            ok = lhs == rhs
            line = f"cell n={n} k={k}: classes={len(lst)} mass_lhs={lhs} mass_rhs={rhs} match={ok}"
            print(line, flush=True)
            report.append(line)
            assert ok, line
            cells[(n, k)] = lst
    tgt = cells[(maxn, target_k)]
    with open("independent_census_n10k10.json", "w") as fh:
        json.dump([g for g, _ in tgt], fh)
    with open("independent_census_aut.json", "w") as fh:
        json.dump([a for _, a in tgt], fh)
    print("DONE", len(tgt), "classes in target cell")


if __name__ == "__main__":
    main()
