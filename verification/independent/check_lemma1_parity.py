#!/usr/bin/env python3
"""Independent check: Lemma 1 identity and the mod-4096 parity congruence.

Written from the manuscript text only (Sections 3-4). Each formal
variable A_w is a column; both sides are compared coefficientwise.
"""
from fractions import Fraction
from math import comb

n = 14


def K(j, w, n=n):
    return sum((-1) ** r * 3 ** (j - r) * comb(w, r) * comb(n - w, j - r)
               for r in range(0, j + 1))


def T(j, w):  # coefficient of A_w in T_j
    return K(j, w)


def U(j, w):  # coefficient of A_w in U_j
    return (-1) ** w * K(j, w)


# ---- Lemma 1 identity -------------------------------------------------
ok = True
for w in range(15):
    lhs = 989184 * (w == 4)
    rhs = (-296 * U(2, w) - 88 * U(4, w) - 9584640 * (w == 0) + 6309
           - 11685888 * (w == 1) - 1345536 * (w == 2) - 4681728 * (w == 3)
           + 1914 * (T(1, w) - 2048 * (w == 1))
           + 1318 * (T(2, w) - 2048 * (w == 2))
           + 279 * (T(3, w) - 2048 * (w == 3))
           + 161 * (T(4, w) - 2048 * (w == 4))
           - 1081344 * (w == 5) - 254976 * (w == 6) - 15360 * (w == 7)
           - 44032 * (w == 14))
    if lhs != rhs:
        ok = False
        print("Lemma1 column mismatch w=%d lhs=%d rhs=%d" % (w, lhs, rhs))
print("Lemma 1 identity holds coefficientwise:", ok)
const = -9584640 + 6309 * 2048
print("constant bound:", const)
for name, c in [("A1", 11685888), ("A2", 1345536), ("A3", 4681728), ("A4", 989184)]:
    print(name, "<=", const // c)

# ---- Parity congruence -------------------------------------------------
# E0 = sum A ; E_j = T_j - 2048 A_j ; F_j = U_j - 2048 Sh_j.
# L = E0 -2E1 -6E2 -17E3 -95E4 -20F0 -24F1 +1108F2 +246F3.
coef = []
for w in range(15):
    c = 1
    for j, m in zip((1, 2, 3, 4), (-2, -6, -17, -95)):
        c += m * (T(j, w) - 2048 * (w == j))
    for j, m in zip((0, 1, 2, 3), (-20, -24, 1108, 246)):
        c += m * U(j, w)
    coef.append(c)
print("A-coefficients of L:", coef)
claimed = [-4550656, -7348224, -1052672, -2623488, 321536, -634880, 221184,
           -28672, 24576, 24576, -45056, 0, 40960, -16384, -77824]
print("matches manuscript list:", coef == claimed)
print("residues mod 4096:", [c % 4096 for c in coef])
sh = [-2048 * m for m in (-20, -24, 1108, 246)]
print("Sh_j coefficients:", sh, "all div 4096:", all(s % 4096 == 0 for s in sh))
# Value of L on a genuine code: E0 = 2048, E_j = 0 (j<=4), F_j = 0.
print("L value on a code = 2048 (from E0 only)")
# Hence 2048 == 2048*(A3+A4) mod 4096  -> A3+A4 odd.
# Also A0 coefficient: A0=1 contributes coef[0]; check it is 0 mod 4096.
print("A0 coef mod 4096:", coef[0] % 4096)
