#!/usr/bin/env python3
"""A paper-checkable Delsarte identity for any additive (10,2^10,d>=5) code.

No solver, no numerical LP, no external import: check all 11 formal original-
physical Krawtchouk coefficients as exact fractions. The result is known-style
additive-code LP arithmetic, not a publication-priority claim.
"""
from fractions import Fraction as F
from math import comb

N=10
SIZE=1024
LAM={1:F(3,40),2:F(1,32),3:F(3,320),4:F(1,640)}
RHS=[F(72),F(42),F(112,5),F(21,2),F(4),F(1)]+[F(0)]*5

def kraw(j,w):
    return sum((-1)**r*3**(j-r)*comb(w,r)*comb(N-w,j-r)
               for r in range(max(0,j-(N-w)),min(j,w)+1))

for w in range(N+1):
    lhs=F(9,64)+sum(v*kraw(j,w) for j,v in LAM.items())
    lhs+=F(int(w==7),10)
    assert lhs==RHS[w],(w,lhs,RHS[w])

# The checked FORMAL identity is
# (9/64) sum_w A_w + sum_j lambda_j T_j + A_7/10
#   = 72A_0 +42A_1 +(112/5)A_2 +(21/2)A_3 +4A_4 +A_5.
# For a genuine additive code of size 1024 and minimum distance >=5:
# A0=1, A1=...=A4=0, sum A=1024, T_j/1024 are actual
# nonnegative integer symplectic-dual weight counts. Therefore:
# A5 = 72 + sum_j lambda_j T_j + A7/10 >=72.

print("EXACT PASS: 11/11 length-ten quaternary Krawtchouk columns")
print("A5 >=72 for additive (10,1024,d>=5), no self-duality assumption")
print("If the ten-site symplectic hull has 16 words, at least 72-15=57")
print("physical weight-five suffix-only normalizer labels are logical.")
print("This is NECESSARY only; [[14,3,5]] existence remains open.")
