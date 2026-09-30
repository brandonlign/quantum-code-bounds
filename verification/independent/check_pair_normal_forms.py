#!/usr/bin/env python3
"""Independent check: every pair of distinct commuting weight-4 Paulis with overlap
t>=2 is, up to site permutation and independent per-site relabelling of
{X,Y,Z} (local Clifford, including the symplectic group Sp(2,2)=S3 at each
site), equivalent to one of the subgroups excluded in Sec. 5.3/5.4,
or generates a weight-<=3 word.  Checked on 8 sites (t>=2 => union<=6).

Canonical form of a pair: the multiset of per-site letter pairs (a,b) with
a,b in {I,1,2,3}, taken modulo a simultaneous S3 action on nonzero letters
per site, and modulo swapping p<->q or replacing (p,q) by (p,p+q) etc.
(subgroup equivalence). We compare subgroup <p,q> to the targets via a
canonical invariant: sorted tuple over sites of the site-local orbit of the
column (p_i, q_i, (p+q)_i), and we take the min over the 6 orderings of the
three nonzero subgroup words.
"""
from itertools import permutations, product

# single-qubit Paulis as 2-bit ints 0=I,1=X,2=Z,3=Y ; addition = xor
S3 = []
for perm in permutations((1, 2, 3)):
    m = {0: 0, 1: perm[0], 2: perm[1], 3: perm[2]}
    # must be additive: m[3] == m[1]^m[2]
    if m[1] ^ m[2] == m[3]:
        S3.append(m)
assert len(S3) == 6  # GL(2,2) is all of S3 on nonzero letters


def site_orbit(col):
    return min(tuple(m[c] for c in col) for m in S3)


def canon(words):  # words: list of 3 nonzero subgroup elements, per-site tuples
    best = None
    for order in permutations(words):
        cols = sorted(site_orbit(tuple(w[i] for w in order)) for i in range(len(order[0])))
        cols = tuple(c for c in cols if c != (0, 0, 0))
        if best is None or cols < best:
            best = cols
    return best


def comm(p, q):
    return sum(1 for a, b in zip(p, q) if a and b and a != b) % 2 == 0


def w(p):
    return sum(1 for a in p if a)


def parse(s, n):
    d = {"I": 0, "X": 1, "Z": 2, "Y": 3}
    return tuple(d[c] for c in s.ljust(n, "I"))


n = 8
targets = {
    "Bell 4-site": ("XXXX", "ZZZZ"),
    "5-site overlap": ("XXZZI", "ZZZIZ"),
    "6-site same-letter": ("ZZZZII", "ZZIIZZ"),
    "6-site crossed": ("ZZZZII", "XXIIXX"),
}
tcanon = {}
for k, (a, b) in targets.items():
    p, q = parse(a, n), parse(b, n)
    tcanon[canon([p, q, tuple(x ^ y for x, y in zip(p, q))])] = k

from collections import Counter
res = Counter()
unmatched = []
supports = [s for s in product((0, 1), repeat=n) if sum(s) == 4]
p = parse("ZZZZ", n)  # WLOG p = ZZZZ on sites 0..3 (local Clifford + perm)
for q in product(range(4), repeat=n):
    if w(q) != 4 or q == p or not comm(p, q):
        continue
    t = sum(1 for a, b in zip(p, q) if a and b)
    if t < 2:
        continue
    r = tuple(x ^ y for x, y in zip(p, q))
    if w(r) <= 3:
        res["generates weight<=3 word (excluded by A2=0 / weight-3 cert)"] += 1
        continue
    c = canon([p, q, r])
    k = tcanon.get(c)
    if k is None:
        unmatched.append((q, t))
    else:
        res[k] += 1
print(dict(res))
print("unmatched:", len(unmatched), unmatched[:5])
