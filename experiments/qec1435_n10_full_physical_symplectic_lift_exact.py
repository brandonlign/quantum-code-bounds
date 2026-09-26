#!/usr/bin/env python3
"""Exact 14-site physical symplectic-lift decision for ONE genuine F2-additive
ten-site code C with |C|=1024, d>=5 and symplectic hull dimension 4.

Enumerates all 1,451,520 ordered symplectic bases of the real four-site
ZZZZ centralizer quotient. A surviving lift is independently checked
against all 131,072 real fourteen-qubit centralizer labels.
Python >=3.10, standard library only.
"""
import argparse,json
from collections import Counter
N=10; MASK=(1<<N)-1
MUL=((0,0,0,0),(0,1,2,3),(0,2,3,1),(0,3,1,2))
EXAMPLE=('1111000011','0000111111','3100121020','0010212010','1001321000')
def wt(v,n=N):
 m=(1<<n)-1
 return ((v&m)|(v>>n)).bit_count()
def sym(a,b,n=N):
 m=(1<<n)-1
 return (((a&m)&(b>>n)).bit_count()+((b&m)&(a>>n)).bit_count())&1
def basis(vectors):
 piv={};out=[]
 for v in vectors:
  w=v
  while w:
   j=w.bit_length()-1
   if j in piv:w^=piv[j]
   else:piv[j]=w;out.append(v);break
 return out
def nullspace(rows,n):
 a=list(rows);piv=[];r=0
 for j in range(n):
  k=next((k for k in range(r,len(a))if a[k]>>j&1),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r]
  for k in range(len(a)):
   if k!=r and a[k]>>j&1:a[k]^=a[r]
  piv.append(j);r+=1
 out=[]
 for j in range(n):
  if j in piv:continue
  v=1<<j
  for i,p in enumerate(piv):
   if a[i]>>j&1:v|=1<<p
  out.append(v)
 return out
def perp(g,n=N):
 m=(1<<n)-1
 return nullspace([((v>>n)&m)|((v&m)<<n)for v in g],2*n)
def span(g):
 a=[0]
 for v in g:a +=[v^x for x in a]
 return a
def gf4example():
 result=[]
 for line in EXAMPLE:
  row=list(map(int,line))
  for a in (1,2):
   vals=[MUL[a][c]for c in row]
   result.append(sum(((v&1)<<i)|((v>>1)<<(i+N))
                     for i,v in enumerate(vals)))
 return result
def sympl_basis(P):
 a=P[:];out=[];rad=[]
 while a:
  x=a.pop(0)
  j=next((j for j,y in enumerate(a)if sym(x,y)),None)
  if j is None:rad.append(x);continue
  y=a.pop(j)
  a=[v^(x if sym(v,y) else 0)^(y if sym(v,x)else 0)for v in a]
  out +=[x,y]
 assert len(basis(out+rad))==len(P)
 assert all(sym(out[i],out[j])==int((i^1)==j)
            for i in range(len(out))for j in range(len(out)))
 return out,rad
def make_prefix():
 p=0xf0
 R=sorted({min(v,v^p)for v in range(256)if (v&15).bit_count()%2==0})
 assert len(R)==64
 cost={v:min(wt(v,4),wt(v^p,4))for v in R}
 assert Counter(cost.values())=={0:1,1:4,2:27,3:24,4:8}
 return R,cost,p
def check_code(g):
 assert len(g)==10 and all(isinstance(v,int)and 0<=v<1<<20 for v in g)
 assert len(basis(g))==10
 C=span(g);assert len(C)==len(set(C))==1024
 d=min(wt(v)for v in C if v)
 if d<5:return {'status':'FAIL d(C)>=5','actual_d':d}
 P=perp(g);assert len(P)==10
 ps,rad=sympl_basis(P)
 assert len(ps)==6 and len(rad)==4
 gram=[sum(sym(a,b)<<j for j,b in enumerate(g))for a in g]
 hcoeff=nullspace(gram,10);H=[]
 for mask in hcoeff:
  h=0
  for j,v in enumerate(g):
   if mask>>j&1:h^=v
  H.append(h)
 assert len(H)==4 and len(basis(H))==4
 assert len(basis(rad+H))==4
 D=span(perp(H));assert len(D)==65536
 leaders=[15]*64;multiplicities=[0]*64
 for v in D:
  q=sum(sym(v,x)<<i for i,x in enumerate(ps))
  multiplicities[q]+=1
  leaders[q]=min(leaders[q],wt(v))
 assert multiplicities==[1024]*64 and leaders[0]==0
 prefix,cost,p=make_prefix()
 hist=Counter(leaders)
 halls=(sum(v<=1 for v in leaders[1:])<=8,
        sum(v<=2 for v in leaders[1:])<=32,
        sum(v<=3 for v in leaders[1:])<=59)
 summary={'distance':d,'hull_dim':4,'suffix_class_spectrum':dict(hist),
          'Hall_capacity':list(halls)}
 # The four one-site Z-prefix classes must pull back to an isotropic
 # affine four-deep-hole plane; the remaining three all-Z classes
 # require suffix distance >=3. This is strictly stronger than Hall.
 from qec1435_n10_lagrangian_affine_deep_hole_gate_exact import lagrangian_gate
 geometry=lagrangian_gate(leaders)
 summary['lagrangian_affine_hole_gate']=geometry['lagrangian_affine_hole_gate']
 summary['admissible_all_Z_lagrangian_patterns']=geometry['number_of_admissible_lagrangian_plane_pairs']
 if not all(halls):
  summary['status']='NO LIFT: EXACT 64-CLASS HALL NECESSITY'
  return summary
 if not geometry['lagrangian_affine_hole_gate']:
  summary['status']='NO LIFT: NO ISOTROPIC ALL-Z FOUR-DEEP-HOLE AFFINE PLANE'
  return summary
 seen=[0]*7;valid=[];terminals=0
 def recurse(ts):
  nonlocal terminals
  k=len(ts)
  if k and k%2==0:
   for q in range(1,1<<k):
    e=0
    for i in range(k):
     if q>>i&1:e^=ts[i^1]
    e=min(e,e^p)
    if leaders[q]+cost[e]<5:return False
  if k==6:
   terminals+=1;valid.append(ts[:]);return True
  for t in prefix:
   if not t:continue
   if any(sym(t,u,4)!=int((i^1)==k)
          for i,u in enumerate(ts)):continue
   seen[k+1]+=1
   if recurse(ts+[t]):return True
  return False
 found=recurse([])
 summary['nodes_seen_by_basis_length']=seen
 summary['full_symplectic_bases_satisfying_physical_weight']=len(valid)
 if not found:
  summary['status']='NO LIFT: ALL Sp(6,2) BASES EXCLUDED'
  assert seen[6]<=1451520
  return summary
 ts=valid[0]
 def join(a,b):
  return (a&15)|((b&MASK)<<4)|((a>>4)<<14)|((b>>10)<<18)
 sg=[join(p,0)]+[join(0,h)for h in H]
 sg +=[join(t,x)for t,x in zip(ts,ps)]
 assert len(sg)==11 and len(basis(sg))==11
 assert all(not sym(a,b,14)for a in sg for b in sg)
 S=set(span(sg));V=span(perp(sg,14))
 assert len(S)==2048 and len(V)==131072
 mind=min(wt(v,14)for v in V if v not in S)
 low=Counter(wt(v,14)for v in S if v and wt(v,14)<=4)
 summary['actual_d14']=mind
 summary['physical_stabilizer_low_weight']=dict(low)
 summary['stabilizer_generators_28bit']=sg
 summary['status']=('CONSTRUCTED EXACT [[14,3,>=5]]' if mind>=5 and low=={4:1}
                    else 'COUNTEREXAMPLE: lift test invalid or target premise mismatch')
 return summary
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 ap.add_argument('--generators',help='JSON list of ten 20-bit Pauli masks')
 args=ap.parse_args()
 g=json.load(open(args.generators))if args.generators else gf4example()
 res=check_code(g)
 if args.generators is None:
  assert res['suffix_class_spectrum']=={0:1,2:39,3:24},res
  assert res['Hall_capacity']==[True,False,False]
 print(json.dumps(res,indent=2,sort_keys=True))
