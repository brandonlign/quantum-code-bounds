#!/usr/bin/env python3
"""Standalone exact 6+8 split-shadow no-go for a physical triangular
two-generator weight-four stabilizer subgroup in any putative binary
[[14,3,d>=5]] stabilizer.

Physical six-site subgroup:
     H = < ZZZZII, ZZ IIZZ >
so every nonidentity H word has physical weight four, with pairwise
two-site overlap. This is NOT the six-site GHZ subgroup from the
earlier rank-six exclusion. This verifier derives all actual Pauli
cosets and uses an immutable exact integer Farkas dual, never SciPy.

The source certificate is a NECESSARY additive full-code enumerator
contradiction. It requires distance five, not any monomial involution,
purity, small-code classification or quantum-code existence claim.
"""
from collections import Counter
from math import comb

W,F,SCALE=6,8,2048
MASK=(1<<W)-1
R=(0,15<<W,51<<W,60<<W)
PREFIX=(
 (0,0,0,0,3,0,1),
 (0,1,0,2,0,1,0),
 (0,0,1,0,2,0,1),
 (0,0,0,1,0,3,0),
 (0,0,0,2,0,2,0),
 (0,0,0,0,2,0,2),
 (0,0,0,0,0,0,4),
 (0,0,0,0,0,4,0),
 (0,0,2,0,2,0,0),
 (1,0,0,0,3,0,0),
 (0,0,3,0,0,0,1),
 (0,0,0,4,0,0,0),
 (0,0,0,0,4,0,0),
)
MULT=(64,6,12,64,24,24,16,24,6,1,1,2,12)
LAM={117:218,127:2756,128:52,135:2756,136:428,
     144:428,154:346,162:692,180:376}
NU={0:-127680512,1:58037,2:21262,3:12772,4:4105,
    5:1643,6:12582,7:6435,8:1811,9:684,10:5596,
    11:961,12:417,13:1239,14:338,15:477}
BOUND=8820736

def wt(v):
    return ((v&MASK)|(v>>W)).bit_count()

def symp(v,w):
    return ((((v&MASK)&(w>>W)).bit_count()
             +((w&MASK)&(v>>W)).bit_count())&1)

def kraw(n,j,weight):
    return sum((-1)**k * 3**(j-k)*comb(weight,k)*comb(n-weight,j-k)
               for k in range(max(0,j-(n-weight)),min(j,weight)+1))

def poly(n,weight):
    p=[1]
    for _ in range(n-weight):
        p=[p[0]]+[p[i]+3*p[i-1] for i in range(1,len(p))]+[3*p[-1]]
    for _ in range(weight):
        p=[p[0]]+[p[i]-p[i-1] for i in range(1,len(p))]+[-p[-1]]
    return p

def physical_coset_audit():
    assert len(set(R))==4
    assert all(symp(v,w)==0 for v in R for w in R)
    assert Counter(wt(v) for v in R)=={0:1,4:3}
    central={v for v in range(1<<(2*W))
             if all(symp(v,r)==0 for r in R)}
    cosets={tuple(sorted(v^r for r in R)) for v in central}
    assert len(central)==1024 and len(cosets)==256
    patterns=Counter(tuple(sum(wt(v)==k for v in c)
                           for k in range(W+1)) for c in cosets)
    assert patterns==dict(zip(PREFIX,MULT)),(patterns,dict(zip(PREFIX,MULT)))
    assert sum(MULT)==256
    print("EXACT physical triangle: 1024 centralizer Paulis,")
    print("256 complete subgroup cosets, 13 prefix weight patterns")

def exact_certificate():
    for n in (W,F):
        for w in range(n+1):
            pp=poly(n,w)
            assert all(pp[j]==kraw(n,j,w) for j in range(n+1))
    nvar=len(PREFIX)*(F+1)
    ncell=(W+1)*(F+1)
    idx=lambda a,b:a*(F+1)+b
    H=[[0]*nvar for _ in range(ncell)]
    for typ,pat in enumerate(PREFIX):
        for b in range(F+1):
            for a,num in enumerate(pat):
                H[idx(a,b)][typ*(F+1)+b]=num
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
    assert (nvar,ncell,len(E),len(G))==(117,63,16,189)
    assert (len(LAM),len(NU))==(9,16)
    assert all(0<=i<len(G) and z>0 for i,z in LAM.items())
    assert all(0<=i<len(E) for i in NU)
    normalization=sum(z*rhs[i] for i,z in NU.items())
    assert normalization==-BOUND,normalization
    coefficients=[]
    for v in range(nvar):
        x=sum(z*G[i][v] for i,z in LAM.items())
        x+=sum(z*E[i][v] for i,z in NU.items())
        assert x>=0,(v,x)
        coefficients.append(x)
    assert sum(x>0 for x in coefficients)==75
    assert max(coefficients)==107073536
    print("EXACT PASS 117/117 integer dual coefficients;")
    print("9 positive inequality multipliers, 16 equality multipliers;")
    print("75 nonzero nonnegative residual coefficients;")
    print("strict Farkas contradiction:",normalization)
    print("No hypothetical [[14,3,d>=5]] stabilizer contains H.")
    print("No statement on [[14,3,5]] code existence follows.")

if __name__=="__main__":
    physical_coset_audit()
    exact_certificate()
