#!/usr/bin/env python3
"""Exact candidate no-go for a physical weight-three stabilizer in [[14,3,d>=5]].

Only the 3+11 split MacWilliams transform, affine split shadow, and the
three actual physical coset enumerators of <ZZZ> are used. No weight-one/two
purity premise, external code classification, or solver is needed at replay.
"""
from math import comb

W, F, SCALE = 3, 11, 2048
PATS = ((0, 0, 1, 1), (0, 1, 1, 0), (1, 0, 0, 1))
LAM = {49: 22, 50: 5, 51: 8, 52: 1, 63: 4, 72: 31, 73: 20,
       74: 11, 108: 2, 120: 7, 122: 1, 132: 2}
NU = {1: -11, 2: 32, 3: 12, 4: 10, 5: 2, 6: 40, 9: 4,
      11: 20, 12: 12, 13: 40}
RESIDUAL = {3: 8192, 4: 4096, 16: 4096, 29: 4096, 35: 4096}
BOUND = 22528


def kw(n, j, weight):
    return sum((-1)**h * 3**(j-h) * comb(weight, h) * comb(n-weight, j-h)
               for h in range(max(0, j-(n-weight)), min(j, weight)+1))


def kw_poly(n, j, weight):
    p = [1]
    for _ in range(n-weight):
        p = [p[0]] + [p[i]+3*p[i-1] for i in range(1, len(p))] + [3*p[-1]]
    for _ in range(weight):
        p = [p[0]] + [p[i]-p[i-1] for i in range(1, len(p))] + [-p[-1]]
    return p[j]


def sy(v, z, n):
    mask = (1 << n)-1
    return (((v & mask) & (z >> n)).bit_count() +
            ((v >> n) & (z & mask)).bit_count()) % 2


def local_wt(v, n, sites):
    mask = ((1 << n)-1)
    return ((((v & mask) | (v >> n)) & sites)).bit_count()


def physical_patterns():
    p = 7 << 3  # ZZZ; x bits 0:2, z bits 3:5.
    normal = {v for v in range(64) if sy(v, p, 3) == 0}
    assert len(normal) == 32
    cosets = {tuple(sorted((v, v ^ p))) for v in normal}
    assert len(cosets) == 16
    hist = {}
    for cs in cosets:
        pat = tuple(sum(local_wt(v, 3, 7) == j for v in cs) for j in range(4))
        hist[pat] = hist.get(pat, 0) + 1
    assert hist == {PATS[0]: 12, PATS[1]: 3, PATS[2]: 1}, hist
    return hist


def control_four_qubits():
    """Direct affine enumeration checks transforms on a real odd-weight S."""
    n = 4
    p = 7 << n
    s = [0, p]
    cen = [v for v in range(1 << (2*n)) if sy(v, p, n) == 0]
    shadow = [v ^ 1 for v in cen]  # <X0,ZZZ>=q(ZZZ)=1.
    def histogram(words):
        out = [0]*8
        for v in words:
            a = local_wt(v, n, 7)
            b = local_wt(v, n, 8)
            out[2*a+b] += 1
        return out
    h, c, sh = map(histogram, (s, cen, shadow))
    for a in range(4):
        for b in range(2):
            q = 2*a+b
            direct = sum(h[2*i+j]*kw(3, a, i)*kw(1, b, j)
                         for i in range(4) for j in range(2))
            signed = sum((-1)**(i+j)*h[2*i+j]*kw(3, a, i)*kw(1, b, j)
                         for i in range(4) for j in range(2))
            assert direct == 2*c[q], (q, direct, c[q])
            assert signed == 2*sh[q], (q, signed, sh[q])
    print('PASS independent four-qubit odd-weight affine-shadow control')


def check():
    physical_patterns()
    control_four_qubits()
    for n in (W, F):
        for j in range(n+1):
            for i in range(n+1):
                assert kw(n,j,i) == kw_poly(n,j,i)
    print('PASS direct physical coset census + two exact Krawtchouk formulas')
    nf = F + 1
    nvar = len(PATS)*nf
    ncell = (W+1)*nf
    idx = lambda pi, b: pi*nf+b
    cell = lambda a,b: a*nf+b
    H = [[0]*nvar for _ in range(ncell)]
    for pi, pat in enumerate(PATS):
        for b in range(nf):
            for a, num in enumerate(pat):
                H[cell(a,b)][idx(pi,b)] = num
    K = [[kw(W,a,i)*kw(F,b,j) for i in range(W+1) for j in range(nf)]
         for a in range(W+1) for b in range(nf)]
    trans = [[sum(K[q][z]*H[z][v] for z in range(ncell)) for v in range(nvar)]
             for q in range(ncell)]
    signs = [(-1)**(i+j) for i in range(W+1) for j in range(nf)]
    shadow = [[sum(K[q][z]*signs[z]*H[z][v] for z in range(ncell))
               for v in range(nvar)] for q in range(ncell)]
    e, rhs = [], []
    e.append(H[cell(0,0)]); rhs.append(1)
    e.append([sum(H[q][v] for q in range(ncell)) for v in range(nvar)])
    rhs.append(SCALE)
    for a in range(W+1):
        for b in range(nf):
            q=cell(a,b)
            if 1 <= a+b <= 4:
                e.append([trans[q][v]-SCALE*H[q][v] for v in range(nvar)])
                rhs.append(0)
    g=[]
    # All 48 cells: first C>=H, then C>=0, then affine shadow>=0.
    for q in range(ncell):
        g.append([SCALE*H[q][v]-trans[q][v] for v in range(nvar)])
    for q in range(ncell):
        g.append([-trans[q][v] for v in range(nvar)])
    for q in range(ncell):
        g.append([-shadow[q][v] for v in range(nvar)])
    assert (len(g),len(e),nvar,ncell)==(144,15,36,48)
    assert all(z>0 for z in LAM.values())
    assert all(z>0 for z in RESIDUAL.values())
    assert sum(z*rhs[i] for i,z in NU.items()) == -BOUND
    for v in range(nvar):
        lhs = sum(z*g[i][v] for i,z in LAM.items())
        lhs += sum(z*e[i][v] for i,z in NU.items())
        assert lhs == RESIDUAL.get(v,0),(v,lhs,RESIDUAL.get(v,0))
    print('EXACT PASS 36/36 integer identities; 12 positive inequalities;')
    print('10 equality coefficients; 5 positive residuals; bound =', -BOUND)
    print('Candidate conclusion: [[14,3,d>=5]] has no weight-three stabilizer.')


if __name__ == '__main__':
    check()
