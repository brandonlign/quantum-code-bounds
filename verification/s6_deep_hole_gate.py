#!/usr/bin/env python3
"""A physical four-deep-hole necessary condition for hypothetical [[14,3,5]].

If the target's unique four-site stabilizer is p=ZZZZ, the FOUR
distinct one-site physical Z-prefix quotient classes have cost ONE.
The induced linear suffix-coset map forces FOUR DISTINCT nonzero
ten-site additive C cosets with minimum ORIGINAL physical weight >=4,
all in H^perp/C, and their four binary quotient labels XOR to ZERO.

Compute the full ambient (F2^20)/C radius-three syndrome coverage for
any actual ten-site additive (10,1024,d>=5) code; fewer than four
uncovered syndromes rules out ANY physical unique-check lift, without
computing the hull or assuming GF4-linearity.
Full zero-X Pauli label quaternary Hamming weight; standard library.
"""
import argparse,json
from itertools import combinations,product
from collections import Counter
N=10;MASK=(1<<N)-1
M=((0,0,0,0),(0,1,2,3),(0,2,3,1),(0,3,1,2))
def wt(v):return ((v&MASK)|(v>>N)).bit_count()
def sym(a,b):
 return ((((a&MASK)&(b>>N)).bit_count()
          +((b&MASK)&(a>>N)).bit_count())&1)
def basis(vals):
 piv={};out=[]
 for v in vals:
  x=v
  while x:
   p=x.bit_length()-1
   if p in piv:x^=piv[p]
   else:piv[p]=x;out.append(v);break
 return out
def nullspace(rows,n):
 a=list(rows);r=0;piv=[]
 for j in range(n):
  k=next((k for k in range(r,len(a))if a[k]>>j&1),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r]
  for i in range(len(a)):
   if i!=r and a[i]>>j&1:a[i]^=a[r]
  piv.append(j);r+=1
 out=[]
 for j in range(n):
  if j in piv:continue
  v=1<<j
  for i,p in enumerate(piv):
   if a[i]>>j&1:v|=1<<p
  out.append(v)
 return out
def span(g):
 out=[0]
 for v in g:out +=[v^w for w in out]
 return out
def from_gf4(rows):
 out=[]
 for row in rows:
  for a in (1,2):
   vals=[M[a][x]for x in row]
   out.append(sum(((x&1)<<i)|((x>>1)<<(i+10))
                  for i,x in enumerate(vals)))
 return out
def deep_holes(g):
 assert len(g)==len(basis(g))==10
 C=span(g);assert len(C)==len(set(C))==1024
 d=min(wt(v)for v in C if v);assert d>=5
 P=nullspace([((v>>N)&MASK)|((v&MASK)<<N)for v in g],20)
 assert len(P)==10
 leaders={}
 # Radius-three coverage already settles the necessary gate. Continue
 # only to determine the ACTUAL covering radius, without assuming <=4
 # for arbitrary additive input codes.
 for r in range(11):
  for sites in combinations(range(10),r):
   for labels in product((1,2,3),repeat=r):
    v=0
    for i,x in zip(sites,labels):
     v|=((x&1)<<i)|((x>>1)<<(i+10))
    syndrome=sum(sym(v,p)<<i for i,p in enumerate(P))
    leaders.setdefault(syndrome,r)
  if r==2:assert len(leaders)==436
  if r==3:
   radius3=Counter(leaders.values())
   holes=1024-len(leaders)
   assert radius3[0]==1 and radius3[1]==30 and radius3[2]==405
  if len(leaders)==1024:break
 assert len(leaders)==1024 and 3<=max(leaders.values())<=10
 return {'d':d,'radius3':dict(sorted(radius3.items())),
         'distinct_C_cosets_min_distance_at_least_4':holes,
         'covering_radius':max(leaders.values()),
         'four_deep_hole_necessary_gate':holes>=4}
if __name__=='__main__':
 parser=argparse.ArgumentParser()
 parser.add_argument('--generators',help='JSON list of 10 independent 20-bit physical Pauli generators')
 args=parser.parse_args()
 if args.generators:
  g=json.load(open(args.generators))
  print(deep_holes(g))
 else:
  control=from_gf4([tuple(map(int,s))for s in(
   '1111000011','0000111111','3100121020',
   '0010212010','1001321000')])
  result=deep_holes(control)
  assert result['distinct_C_cosets_min_distance_at_least_4']==0
  print('ACTUAL GF4 C10 d5 hull4 control:',result)
  qr=[]
  for sh in range(1,6):
   rr=[0]*11
   for j,x in enumerate((1,3,1,1,2,1)):rr[sh+j]=x
   qr.append(tuple(rr[1:]))
  result=deep_holes(from_gf4(qr))
  assert result['distinct_C_cosets_min_distance_at_least_4']==3
  print('ACTUAL QUADRATIC-RESIDUE C10 d5 child:',result)
  seed=tuple(2 if c=='w'else int(c)for c in 'w10100100101')
  rot=[seed[i:]+seed[:i]for i in range(12)]
  parent=span([sum(((x&1)<<i)|((x>>1)<<(i+12))
                   for i,x in enumerate(row))for row in rot])
  D=set()
  for v in parent:
   if (v&1)or((v>>12)&1):continue
   row=[((v>>i)&1)|(((v>>(i+12))&1)<<1)for i in range(2,12)]
   D.add(sum(((x&1)<<i)|((x>>1)<<(i+10))
             for i,x in enumerate(row)))
  result=deep_holes(basis(sorted(D)))
  assert result['distinct_C_cosets_min_distance_at_least_4']==3
  print('ACTUAL DODECACODE-DERIVED C10 d5 child:',result)
  print('EXACT FOUR-DEEP-HOLE NECESSARY GATE CONTROLS PASS')
