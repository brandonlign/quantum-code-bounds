#!/usr/bin/env python3
"""Four original 4-qubit blocks (and 2 ordinary sites), each containing ZZZZ:
exact 648-column signed-shadow no-go for H4=3 disjoint supports.

Every coefficient is rebuilt using actual original-physical Pauli cosets and
independently evaluated Krawtchouk polynomials. No optimizer or floating point
is used.
"""
from collections import Counter
from itertools import product
from math import comb
from json import loads
from pathlib import Path

MOD=2048
DATA=loads((Path(__file__).resolve().parent /
    "qec1435_disjoint_fourblock_exact_dual.json").read_text())
L={int(i):v for i,v in DATA["L"].items()}
NU={int(i):v for i,v in DATA["NU"].items()}
assert (len(L),len(NU),DATA["columns"])==(43,68,648)
assert all(v>0 and 750<=i<1125 for i,v in L.items())
assert DATA["constant"] == -125829120

def kraw(n):
    def multiply(p,s):
        q=[0]*(len(p)+1)
        for j,v in enumerate(p):
            q[j]+=v
            q[j+1]+=v*s
        return q
    K=[[sum((-1)**r*3**(j-r)*comb(w,r)*comb(n-w,j-r)
            for r in range(max(0,j-(n-w)),min(j,w)+1))
        for w in range(n+1)] for j in range(n+1)]
    for w in range(n+1):
        poly=[1]
        for slope in [3]*(n-w)+[-1]*w:
            poly=multiply(poly,slope)
        assert [K[j][w] for j in range(n+1)]==poly
    return K

# A single physical 4-site subgroup <ZZZZ> has 64 full normalizer cosets:
# even-parity X on these ORIGINAL sites, and Z modulo ZZZZ.
PATS=Counter()
REP=sorted({min(z,z^15) for z in range(16)})
XS=[x for x in range(16) if x.bit_count()%2==0]
assert len(REP)==8 and len(XS)==8
for x in XS:
    for z in REP:
        p=[0]*5
        for r in (0,15):
            p[(x|(z^r)).bit_count()]+=1
        PATS[tuple(p)]+=1
assert sum(PATS.values())==64 and len(PATS)==6
assert sorted(PATS.values())==[1,3,4,8,24,24]
assert all(sum(p)==2 for p in PATS)
patterns=sorted(PATS)
K4,K2=kraw(4),kraw(2)
def transform(p,sign=False):
    return [sum(K4[j][w]*p[w]*((-1)**w if sign else 1)
            for w in range(5)) for j in range(5)]
ordinary=[transform(p) for p in patterns]
signed=[transform(p,True) for p in patterns]

# Fully distinct ORIGINAL-physical split cells in lexicographic order.
CELLS=list(product(range(5),range(5),range(5),range(3)))
LOW=[cell for cell in CELLS if 1<=sum(cell)<=4]
assert len(CELLS)==375 and len(LOW)==64
assert len(NU)<=70 and max(NU)<70
SH_CELLS={i-750:CELLS[i-750] for i in L}
assert all(0<=i<375 for i in SH_CELLS)

def physical_h(a,b,c,d,p,q,r,suffix):
    return p[a]*q[b]*r[c] if d==suffix else 0

def combined_cell(row,v1,v2,v3,suffix,sign=False):
    a,b,c,d=row
    return (v1[a]*v2[b]*v3[c]*K2[d][suffix]
            *((-1)**suffix if sign else 1))

positive=0
minres=None
for i,j,k,b in product(range(6),range(6),range(6),range(3)):
    p,q,r=patterns[i],patterns[j],patterns[k]
    t1,t2,t3=ordinary[i],ordinary[j],ordinary[k]
    s1,s2,s3=signed[i],signed[j],signed[k]
    e=[0]*70
    origin=physical_h(0,0,0,0,p,q,r,b)
    e[0]=MOD*origin
    e[1]=MOD*8   # exact R-coset size, not a normalized pseudoqubit
    for m,row in enumerate(LOW):
        e[m+2]=(combined_cell(row,t1,t2,t3,b)
                 -MOD*physical_h(*row,p,q,r,b))
    for w in range(1,5):
        e[65+w]=MOD*sum(physical_h(*row,p,q,r,b)
                        for row in CELLS if sum(row)==w)
    assert len(e)==70
    val=sum(v*e[idx] for idx,v in NU.items())
    for idx,v in L.items():
        row=SH_CELLS[idx-750]
        # G row for the ACTUAL affine-shadow nonnegativity, with
        # original unnormalized integer numerator.
        val-=v*combined_cell(row,s1,s2,s3,b,sign=True)
    assert val>=0,(i,j,k,b,val)
    positive+=val>0
    if minres is None or val<minres:minres=val

rhs=[0]*70
rhs[0]=MOD
rhs[1]=MOD*MOD
rhs[69]=MOD*3
constant=sum(v*rhs[idx] for idx,v in NU.items())
assert constant == DATA["constant"] == -125829120
assert positive==DATA["positive"]==403 and minres==0
print("EXACT FOUR-BLOCK DISJOINT H4=3 NO-GO PASS")
print("64 physical single-block cosets, 6 patterns; 648 4+4+4+2 columns")
print("43 signed-shadow nonnegativity multipliers, 68 equality multipliers")
print("403 positive residual columns, 245 zero, zero negative")
print("exact Farkas normalization:",constant)
print("H4=3 cannot occur with three disjoint ZZZZ checks, conditional on")
print("physical distance-five equalities, H2=0 and signed-shadow integrality.")
