#!/usr/bin/env python3
"""Automorphism-group orders of the 37 committed length-ten classes.

For each committed representative C, compute |Aut(C)| (coordinate
permutations and per-site GL(2,2), acting on the code) from its colored
incidence graph. Then check the orbit-stabilizer identity for the target
cell (10, 2^10, >=5):

    sum over classes of 10! * 6^10 / |Aut(C)|  ==  mass of labelled codes,

where the right-hand side is the number of labelled codes counted by
independent_census.py (printed there as mass_lhs for n=10, k=10). Equality
means no equivalence class was lost or duplicated.
"""
import json
import os
from fractions import Fraction
from math import factorial

from pynauty import autgrp

from independent_census import graph
from independent_hull_capacity import theirs, N

LABELLED_MASS_N10_K10 = 2333060795842560  # mass_lhs from independent_census.py

if __name__ == "__main__":
    auts = []
    for g in theirs:
        _, s1, s2, _, _ = autgrp(graph(g, N))
        auts.append(round(s1 * 10 ** s2))
    for i, a in enumerate(auts, 1):
        print(f"class {i:2d}: |Aut| = {a}")
    total = sum(Fraction(factorial(N) * 6 ** N, a) for a in auts)
    print("sum of 10!*6^10/|Aut| =", total)
    assert total == LABELLED_MASS_N10_K10, total
    print("ORBIT-STABILIZER MASS CHECK PASS (37 classes, none lost or duplicated)")
