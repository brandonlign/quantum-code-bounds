#!/usr/bin/env python3
"""No-go candidate for a physical weight-two stabilizer in [[14,3,>=5]].

If p=Z0 Z1 is a stabilizer after local Clifford conjugation, the
two-site Pauli normalizer splits into four R=<p> cosets, having weights
(1,0,1),(0,2,0),(0,0,2),(0,0,2) for pair weights 0,1,2.
Therefore H[2,b]>=H[0,b] for every fixed-twelve weight b.
Together with the physical low-distance equalities, nonnegative split
MacWilliams centralizer and split Rains shadow this yields the exact
integer Farkas contradiction below.

The shadow is the AFFINE SYMPLECTIC COSET whose pairing with every
stabilizer s equals wt(s) mod 2; the weight-parity map is a character
on isotropic S. Its 2+12 split enumerator is nonnegative.

All integer coefficients, all 39 column identities, and the negative
normalization are verified without any floating point, solver, or
external small-code classification.
"""
from math import comb

SCALE=2048
LAM={
0:2662400,12:24576,18:319488,21:36864,54:253952,
57:2048,63:14336,91:143360,93:409600,95:43008,
96:49152,98:14336,99:77824
}
NU={
0:-5672960,1:2157,
2:1437696,3:872448,4:227328,5:92160,6:118784,
7:364544,8:43008,9:38912
}
C={
1:2214592512,13:6006243328,
2:301989888,3:1220542464,4:239075328,5:327155712,
14:3028287488,15:2092957696,16:1052770304,
17:494927872,18:188743680,19:29360128,
27:2977955840,28:1686110208,29:813694976,
30:327155712,31:109051904
}
BOUND=2571108352

def kraw(n,j,w):
    return sum(
        (-1)**h*3**(j-h)*comb(w,h)*comb(n-w,j-h)
        for h in range(max(0,j-(n-w)),min(j,w)+1)
    )

def kraw_poly(n,j,w):
    v=[1]
    for _ in range(n-w):
        v=([v[0]]+[v[i]+3*v[i-1] for i in range(1,len(v))]
           +[3*v[-1]])
    for _ in range(w):
        v=([v[0]]+[v[i]-v[i-1] for i in range(1,len(v))]
           +[-v[-1]])
    assert len(v)==n+1
    return v[j]

for n in (2,12):
    for j in range(n+1):
        for w in range(n+1):
            assert kraw(n,j,w)==kraw_poly(n,j,w)
print("PASS independent binomial/polynomial quaternary transforms")

# Enumerate the complete 16-vector physical Pauli space of TWO qubits,
# with X bits 0..1 and Z bits 2..3.
R={0,12}  # I and Z0Z1

def symp(v,w):
    return ((((v&3)&(w>>2)).bit_count()
            +((v>>2)&(w&3)).bit_count())&1)

def wt(v):
    return ((v&3)|(v>>2)).bit_count()

normal={v for v in range(16)
        if all(not symp(v,r) for r in R)}
assert len(normal)==8
cosets={tuple(sorted(v^r for r in R)) for v in normal}
patterns={}
for coset in cosets:
    p=tuple(sum(wt(v)==i for v in coset) for i in range(3))
    assert p[2]>=p[0]
    patterns[p]=patterns.get(p,0)+1
assert patterns=={
    (1,0,1):1,
    (0,2,0):1,
    (0,0,2):2
}
print("PASS all four physical R cosets: H[2,b]>=H[0,b]")

NVAR=39
idx=lambda a,b:13*a+b
unit=lambda k:[int(j==k) for j in range(NVAR)]
sign=[(-1)**(a+b) for a in range(3) for b in range(13)]
K=[
    [kraw(2,a,x)*kraw(12,b,y)
     for x in range(3) for y in range(13)]
    for a in range(3) for b in range(13)
]
E=[];rhs=[];G=[];labels=[]

def eq(row,value=0):
    E.append([SCALE*t for t in row])
    rhs.append(SCALE*value)

def ineq(row,label):
    G.append(row)
    labels.append(label)

eq(unit(idx(0,0)),1)
eq([1]*NVAR,SCALE)

for b in range(13):
    row=[0]*NVAR
    row[idx(0,b)]=SCALE
    row[idx(2,b)]=-SCALE
    ineq(row,("physical coset H2>=H0",b))

for a in range(3):
    for b in range(13):
        j=idx(a,b)
        transform=K[j]
        if 0<a+b<=4:
            E.append([
                transform[t]-SCALE*int(t==j)
                for t in range(NVAR)
            ])
            rhs.append(0)
        ineq([
            SCALE*int(t==j)-transform[t]
            for t in range(NVAR)
        ],("centralizer>=stabilizer",a,b))
        ineq([
            -transform[t] for t in range(NVAR)
        ],("centralizer>=0",a,b))
        ineq([
            -sign[t]*transform[t] for t in range(NVAR)
        ],("split shadow>=0",a,b))

assert (len(E),len(G),NVAR)==(13,130,39)
assert len(LAM)==13 and len(NU)==10 and len(C)==17
assert all(isinstance(v,int) for row in E+G for v in row)
assert min(LAM.values())>0 and min(C.values())>0
assert sum(z*rhs[i] for i,z in NU.items())==-BOUND
for col in range(NVAR):
    total=(
        sum(z*G[i][col] for i,z in LAM.items())
        +sum(z*E[i][col] for i,z in NU.items())
    )
    assert total==C.get(col,0),(col,total,C.get(col,0))
print("EXACT PASS: 39/39 integer coefficient identities,")
print("13 positive inequality multipliers, 10 equality multipliers,")
print("17 positive residuals and contradiction", -BOUND)
print("A [[14,3,d>=5]] stabilizer cannot have ANY weight-two stabilizer.")
print("No proof of code existence/nonexistence or full group triviality.")
