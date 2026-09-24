#!/usr/bin/env python3
"""Standalone 6+8 physical split-shadow exclusion of ANY two commuting
weight-four stabilizer Paulis with original-physical supports overlapping
in two qubits and DIFFERENT nonidentity Pauli symbols on both overlapping
qubits. Their product then has physical weight SIX.

By local original-qubit Cliffords and physical permutation, normalize
to physical H=< ZZZZII, XXIIXX > on SIX original physical sites.
This is distinct from same-letter overlap triangle subgroup (4,4,4)
and same-support Bell subgroup (4,4,4 on only four sites).

Exact integer dual: 126 coset-count columns, 14 actual physical
six-site coset weight-pattern classes, negative normalization
-22212608. No optimizer, involution, purity, or external code list
is assumed by this STANDALONE subgroup no-go replayer.
"""
from collections import Counter
from math import comb

W,F,SCALE=6,8,2048
MASK=(1<<W)-1
R=(0,51,15<<W,51^(15<<W))
PREFIX=(
 (0,1,0,1,0,2,0),
 (0,0,0,1,0,3,0),
 (0,0,0,0,4,0,0),
 (0,0,0,0,0,4,0),
 (0,0,0,2,0,2,0),
 (0,0,0,0,2,0,2),
 (0,0,0,0,3,0,1),
 (0,0,1,0,1,0,2),
 (0,0,0,0,1,0,3),
 (0,0,1,0,2,0,1),
 (0,0,2,0,1,0,1),
 (0,0,0,3,0,1,0),
 (0,0,1,0,3,0,0),
 (1,0,0,0,2,0,1),
)
MULT=(4,48,16,32,32,32,40,8,16,16,2,4,5,1)
LAM={54:888,127:8280,128:1614,135:5584,136:2839,
     138:337,144:2732,146:674,154:1455,162:1792,180:444}
NU={0:-311595008,1:141300,2:49068,3:31368,4:8874,
    5:3996,6:34240,7:22408,8:5964,9:2878,10:16112,
    11:3054,12:1760,13:2808,14:1086,15:1300}
BOUND=22212608

def weight(v):
    return ((v&MASK)|(v>>W)).bit_count()

def symp(v,w):
    return ((((v&MASK)&(w>>W)).bit_count()
             +((w&MASK)&(v>>W)).bit_count())&1)

def kraw(n,j,w):
    return sum((-1)**h * 3**(j-h)*comb(w,h)*comb(n-w,j-h)
               for h in range(max(0,j-n+w),min(j,w)+1))

def physical_cosets():
    assert len(set(R))==4
    assert all(symp(a,b)==0 for a in R for b in R)
    assert Counter(weight(v) for v in R)=={0:1,4:2,6:1}
    normal={v for v in range(1<<(2*W))
            if all(symp(v,r)==0 for r in R)}
    cosets={tuple(sorted(v^r for r in R)) for v in normal}
    assert (len(normal),len(cosets))==(1024,256)
    hist=Counter(tuple(sum(weight(v)==i for v in c)
                       for i in range(W+1)) for c in cosets)
    assert hist==dict(zip(PREFIX,MULT)),hist
    assert sum(MULT)==256
    print("EXACT CROSS-OVERLAP PHYSICAL COSETS: 1024 / 256 / 14")

def audit():
    physical_cosets()
    nvar=len(PREFIX)*(F+1)
    ncell=(W+1)*(F+1)
    idx=lambda a,b:a*(F+1)+b
    H=[[0]*nvar for _ in range(ncell)]
    for t,pat in enumerate(PREFIX):
        for b in range(F+1):
            for a,w in enumerate(pat):
                H[idx(a,b)][t*(F+1)+b]=w
    KW=[[kraw(W,a,i) for i in range(W+1)] for a in range(W+1)]
    KF=[[kraw(F,b,j) for j in range(F+1)] for b in range(F+1)]
    T=[[sum(KW[a][i]*KF[b][j]*H[idx(i,j)][v]
             for i in range(W+1) for j in range(F+1))
        for v in range(nvar)]
       for a in range(W+1) for b in range(F+1)]
    SH=[[sum((-1)**(i+j)*KW[a][i]*KF[b][j]*H[idx(i,j)][v]
             for i in range(W+1) for j in range(F+1))
        for v in range(nvar)]
       for a in range(W+1) for b in range(F+1)]
    E=[H[0][:],[sum(row[v] for row in H) for v in range(nvar)]]
    rhs=[1,SCALE]
    for a in range(W+1):
        for b in range(F+1):
            q=idx(a,b)
            if 1<=a+b<=4:
                E.append([T[q][v]-SCALE*H[q][v]
                          for v in range(nvar)])
                rhs.append(0)
    G=[]
    for q in range(ncell):
        G.append([SCALE*H[q][v]-T[q][v] for v in range(nvar)])
    for q in range(ncell):
        G.append([-T[q][v] for v in range(nvar)])
    for q in range(ncell):
        G.append([-SH[q][v] for v in range(nvar)])
    assert (nvar,ncell,len(E),len(G))==(126,63,16,189)
    assert (len(LAM),len(NU))==(11,16)
    assert all(0<=i<len(G) and z>0 for i,z in LAM.items())
    assert sum(rhs[i]*z for i,z in NU.items())==-BOUND
    residual=[]
    for v in range(nvar):
        x=sum(z*G[i][v] for i,z in LAM.items())
        x+=sum(z*E[i][v] for i,z in NU.items())
        assert x>=0,(v,x)
        residual.append(x)
    assert sum(x>0 for x in residual)==78
    assert max(residual)==280477696
    print("EXACT PASS 126/126 integer Farkas dual coefficients")
    print("11 positive inequalities, 16 free equalities")
    print("78 positive nonnegative residual coefficients")
    print("strict contradiction:",-BOUND)
    print("No binary [[14,3,d>=5]] stabilizer contains H.")
    print("No claim [[14,3,5]] exists or does not exist.")

if __name__=="__main__":
    audit()
