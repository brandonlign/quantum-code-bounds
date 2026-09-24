#!/usr/bin/env python3
"""Exact control and self-dual exclusion for the single-H4 existence reduction.

1. Reconstruct (12,4^6,6) cyclic dodecacode and shorten + puncture it to an
   ACTUAL additive (10,2^10,5) code with trace-symplectic hull dimension 8.
2. Prove NO *self-dual* additive (10,2^10,d>=5) code exists by an exact
   one-parameter MacWilliams solution and affine shadow nonnegativity.

Neither ingredient constructs or rules out an ORIGINAL [[14,3,5]] code.
Python standard library only; no optimizer, external data file, or classifier.
"""
from collections import Counter
from fractions import Fraction as F
from math import comb

N=10
SIZE=1024

def kw(n,j,w):
    return sum((-1)**i*3**(j-i)*comb(w,i)*comb(n-w,j-i)
               for i in range(max(0,j-n+w),min(j,w)+1))

def rank_fraction(A):
    m=[[F(v) for v in row] for row in A]
    if not m:return 0
    n=len(m[0]); row=0
    for c in range(n):
        ix=next((i for i in range(row,len(m)) if m[i][c]),None)
        if ix is None:continue
        m[row],m[ix]=m[ix],m[row]
        p=m[row][c]
        m[row]=[x/p for x in m[row]]
        for i in range(len(m)):
            if i!=row and m[i][c]:
                factor=m[i][c]
                m[i]=[a-factor*b for a,b in zip(m[i],m[row])]
        row+=1
        if row==len(m):break
    return row

def selfdual_obstruction():
    K=[[kw(N,j,w) for w in range(N+1)]for j in range(N+1)]
    # A0=1, A1=...=A4=0, and unknowns A5,...,A10.
    coefficient=[[1]*6]+[
        [K[j][w]-SIZE*int(j==w) for w in range(5,11)]
        for j in range(N+1)]
    assert rank_fraction(coefficient)==5  # affine dimension exactly one
    def a(t):
        return [1,0,0,0,0,138-t,5*t-60,660-10*t,10*t-165,450-5*t,t]
    for t in (0,1):
        A=a(t)
        assert sum(A)==SIZE
        assert all(sum(K[j][w]*A[w]for w in range(N+1))==SIZE*A[j]
                   for j in range(N+1))
        S=[F(sum((-1)**w*K[j][w]*A[w]for w in range(N+1)),SIZE)
           for j in range(N+1)]
        assert S[0]==F(t-46,32)
        assert S[2]==F(5*(30-t),32)
        assert S[2]+5*S[0]==F(-5,2)
    print("EXACT n=10 self-dual no-go: rank=5, A5..A10 one parameter t=A10")
    print("shadow[0]=(t-46)/32; shadow[2]=5(30-t)/32")
    print("shadow[2]+5*shadow[0]=-5/2 < 0, contradiction")

def symp(a,b):
    return sum(((x&1)*(y>>1)+(x>>1)*(y&1)) for x,y in zip(a,b))&1

def symplectic_rank(rows):
    M=[[symp(a,b) for b in rows]for a in rows]
    rank=0
    for j in range(len(rows)):
        ix=next((i for i in range(rank,len(rows)) if M[i][j]),None)
        if ix is None:continue
        M[rank],M[ix]=M[ix],M[rank]
        for i in range(len(rows)):
            if i!=rank and M[i][j]:
                M[i]=[a^b for a,b in zip(M[i],M[rank])]
        rank+=1
    return rank

def binary_basis(words):
    basis=[]
    pivots={}
    for row in words:
        mask=sum(((a&1)<<(2*i))+(((a>>1)&1)<<(2*i+1))
                 for i,a in enumerate(row))
        v=mask
        for p in sorted(pivots,reverse=True):
            if v>>p&1:v^=pivots[p]
        if v:
            p=v.bit_length()-1
            pivots[p]=v
            basis.append(row)
    return basis

def dodecacode_control():
    # 1->X, omega->Z, omega^2=1+omega->Y, GF4 additive is Pauli XOR.
    parent="w10100100101"
    assert len(parent)==12
    seed=tuple(2 if c=="w" else int(c) for c in parent)
    gens=[seed[j:]+seed[:j] for j in range(12)]
    assert len(binary_basis(gens))==12
    assert all(symp(a,b)==0 for a in gens for b in gens)
    words=[tuple([0]*12)]
    for g in gens:
        words += [tuple(a^b for a,b in zip(w,g)) for w in words[:]]
    assert len(set(words))==4096
    hist=Counter(sum(x!=0 for x in w) for w in words)
    assert hist=={0:1,6:396,8:1485,10:1980,12:234},hist
    # Shorten at ORIGINAL coordinate 0, then puncture coordinate 1.
    child={w[2:] for w in words if w[0]==0}
    basis=binary_basis(sorted(child))
    assert len(child)==1024 and len(basis)==10
    hist10=Counter(sum(x!=0 for x in w) for w in child)
    assert hist10=={0:1,5:108,6:90,7:360,8:135,9:300,10:30},hist10
    rank=symplectic_rank(basis)
    assert rank==2 and 10-rank==8
    print("EXACT dodecacode: 4096 words, minimum weight 6, self-orthogonal")
    print("shorten + puncture: ACTUAL (10,1024,5) additive code")
    print("length-ten symplectic rank=2; hull dimension=8")
    print("THIS IS NOT A [[14,3,5]] CONSTRUCTION")

if __name__=="__main__":
    selfdual_obstruction()
    dodecacode_control()
