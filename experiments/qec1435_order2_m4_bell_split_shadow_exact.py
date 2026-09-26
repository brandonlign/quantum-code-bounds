#!/usr/bin/env python3
"""Exact classification-free exclusion of the last rank-4 Bell involution.

Canonical rank-4 survivor (t,s,r,a,u)=(2,0,2,2,7) has physical
XXXX and ZZZZ stabilizers on four moving sites. Let H[a,b] count
stabilizers of moving/fixed weights a,b (four + ten qubits). The
R=<XXXX,ZZZZ> coset weight patterns force H[1,b]=0 and
H[4,b]=H[2,b]+3*H[0,b] for every fixed b. Stabilizer size is 2^11.

Split MacWilliams C=(K4 tensor K10)H/2048 is the full centralizer
enumerator; distance>=5 gives C[a,b]=H[a,b] for total weights 1..4.
Both C and the split Rains shadow
Sh=(K4 tensor K10)[(-1)^(a+b) H[a,b]]/2048 are nonnegative.
Shadow positivity holds because weight parity is a LINEAR character
on the isotropic S; this Fourier transform enumerates an actual affine
coset of S-perp. All constraints used below are necessary.

The immutable dual proves a contradiction by multiplying integer-
scaled Gx<=0 and Ex=rhs by nonnegative lambda and unrestricted nu,
giving c>=0 and nu rhs=-320017816092672. No numerical optimization
or external small-code classification is invoked in verification.

To reproduce:
  python experiments/qec1435_order2_m4_bell_split_shadow_exact.py
"""
from math import comb
SCALE=2048
LAM={5:6928035840,14:188946432,42:134061392,43:2757441392,46:1326542976,64:70682880,67:122972636160,68:32876679168,74:3464017920,101:11431259136,104:5888830464}
NU={1:-76298193,4:-34682618340,6:-15914513484,7:-9992146944,8:-28004724804,10:6066470636,11:-3695047552,12:-2491478500,13:1761058016,14:622800644,15:2437623040,16:824048764,17:3631687216,18:339941692,19:4082675968,20:407953948,21:3811805376,22:713391828,24:336437820,25:91576037376,26:65942304768,27:17760964608,28:9447321600,34:5605410816,35:2109901824,36:6424178688,37:3763183104,38:153676431360}
C={5:31214958280704,7:4192091504640,22:174004044300288,23:89818247725056,24:86873034719232,25:1031899447296,26:12447287083008,32:3095698341888,33:225792497811456,34:123473218240512,35:56109532446720,36:23314478137344,37:4159844646912,45:168801551253504,46:30699008557056,47:46757943705600,54:644937154560}
BOUND=320017816092672

def kraw(n,j,w):
    return sum((-1)**h*3**(j-h)*comb(w,h)*comb(n-w,j-h)
               for h in range(max(0,j-(n-w)),min(j,w)+1))

def kraw_independent(n,j,w):
    """Coefficient of y^j in (1+3y)^(n-w)(1-y)^w."""
    v=[1]
    for _ in range(n-w):
        v=[v[0]]+[v[i]+3*v[i-1] for i in range(1,len(v))]+[3*v[-1]]
    for _ in range(w):
        v=[v[0]]+[v[i]-v[i-1] for i in range(1,len(v))]+[-v[-1]]
    assert len(v)==n+1
    return v[j]

for n in (4,10):
    for j in range(n+1):
        for w in range(n+1):
            assert kraw(n,j,w)==kraw_independent(n,j,w)
print("PASS: independent polynomial and integer Krawtchouk constructions")

# Exhaust ALL moving four-qubit R cosets to verify the physical
# Bell enumerator relation, without assuming a paper classification.
PX=15
PZ=15<<4
R={0,PX,PZ,PX^PZ}
def symp(v,w):
    return ((((v&15)&(w>>4)).bit_count()
            +((v>>4)&(w&15)).bit_count())&1)
def wt(v):return ((v&15)|(v>>4)).bit_count()
normal={v for v in range(256)
        if all(symp(v,r)==0 for r in R)}
assert len(normal)==64
cosets={tuple(sorted(v^r for r in R)) for v in normal}
assert len(cosets)==16
hist={}
for coset in cosets:
    w=tuple(sum(wt(v)==i for v in coset) for i in range(5))
    assert w[1]==0 and w[4]==w[2]+3*w[0]
    hist[w]=hist.get(w,0)+1
assert hist=={
    (1,0,0,0,3):1,
    (0,0,2,0,2):9,
    (0,0,0,4,0):6
}
print("PASS: all 16 Bell cosets imply H[4,b]=H[2,b]+3 H[0,b]")

def idx(a,b):return 11*a+b
NVAR=55
def unit(j):return [int(i==j) for i in range(NVAR)]
TRANS=[[kraw(4,a,aa)*kraw(10,b,bb)
        for aa in range(5) for bb in range(11)]
       for a in range(5) for b in range(11)]
SIGN=[(-1)**(a+b) for a in range(5) for b in range(11)]
E=[];rhs=[];G=[];labels=[]
def eq(v,target=0):E.append(v);rhs.append(SCALE*target)
def ineq(v,label):G.append(v);labels.append(label)

# Every equality/inequality is scaled by 2048 to be INTEGER.
eq([SCALE*x for x in unit(idx(0,0))],1)
eq([SCALE]*NVAR,SCALE)
eq([SCALE*x for x in unit(idx(0,1))],0)
for b in range(11):
    eq([SCALE*x for x in unit(idx(1,b))])
    row=[0]*NVAR
    row[idx(4,b)]=SCALE
    row[idx(2,b)]=-SCALE
    row[idx(0,b)]=-3*SCALE
    eq(row)
for a in range(5):
    for b in range(11):
        j=idx(a,b)
        tr=TRANS[j]
        if 0<a+b<=4:
            eq([tr[i]-SCALE*int(i==j) for i in range(NVAR)])
        ineq([SCALE*int(i==j)-tr[i] for i in range(NVAR)],
             ("centralizer>=stabilizer",a,b))
        ineq([-tr[i] for i in range(NVAR)],
             ("centralizer>=0",a,b))
        ineq([-SIGN[i]*tr[i] for i in range(NVAR)],
             ("split shadow>=0",a,b))
assert (len(E),len(G),NVAR)==(39,165,55)
assert len(LAM)==11 and len(NU)==28 and len(C)==17
assert all(z>0 for z in LAM.values())
assert all(z>0 for z in C.values())
assert sum(z*rhs[k] for k,z in NU.items())==-BOUND
for col in range(NVAR):
    total=(sum(z*G[k][col] for k,z in LAM.items())
           +sum(z*E[k][col] for k,z in NU.items()))
    assert total==C.get(col,0),(col,total,C.get(col,0))
print("EXACT PASS: all 55 integer column identities; 11 nonnegative")
print("dual inequalities, 28 equality coefficients and 17 positive")
print("residual coefficients; strict contradiction:",-BOUND)
print("Every rank-4 Bell pseudo-stabilizer extension is impossible.")
