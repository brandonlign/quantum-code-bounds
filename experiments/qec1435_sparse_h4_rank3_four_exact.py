#!/usr/bin/env python3
"""Exact original-physical exclusions for four sparse rank-three H4=3 cases.

No optimizer at replay: rebuild each physical 3-Z-check normalizer's R-cosets,
split MacWilliams / affine-shadow NECESSARY models and integer Farkas identities.
Does NOT exclude disjoint H4=3 checks or the H4=1 case.
"""
from collections import Counter
from math import comb

SETS = {
 'triangle':((0,1,2,3),(3,4,5,6),(2,4,7,8)),
 'common':((0,1,2,3),(3,4,5,6),(3,7,8,9)),
 'two':((0,1,2,3),(3,4,5,6),(6,7,8,9)),
 'one':((0,1,2,3),(3,4,5,6),(7,8,9,10)),
}
CERT = {
 'triangle': {'L':{72:102351,73:29991,78:33531,121:4128,122:1100,124:184,127:5672,129:700,132:4160,134:202,139:1732,144:2248},'NU':{0:-422449152,1:136242,2:58332,3:44008,4:15462,5:7538,6:35628,7:23548,8:8310,9:4478,10:120649,11:34191,12:3446,13:36663,14:1400,15:1382,16:18984960,17:-181309440,18:51394560,19:-38762496},'bound':86470656,'classes':40,'columns':240,'positive':151},
 'common': {'L':{61:10645,65:15264,70:5638,110:1000,111:1544,112:668,113:376,115:544,116:572,120:616,122:12,126:122,130:272},'NU':{0:-61333504,1:19640,2:8910,3:6566,4:2444,5:1292,6:5204,7:14413,8:1494,9:810,10:17660,11:690,12:490,13:6046,14:246,15:136,16:4026368,17:-12394496,18:9875456,19:-3350528},'bound':9031680,'classes':27,'columns':135,'positive':83},
 'two': {'L':{60:6694,61:28701,65:38922,66:10950,70:17023,111:5274,112:1188,113:726,115:1644,116:1197,118:9,120:1188,126:363,130:726},'NU':{0:-179294208,1:62919,2:26424,3:19800,4:6963,5:3351,6:22708,7:40851,8:4395,9:2235,10:46788,11:13167,12:1509,13:18178,14:783,15:429,16:9984000,17:-53784576,18:25786368,19:-9394176},'bound':20484096,'classes':60,'columns':300,'positive':205},
 'one': {'L':{52:36,53:116,54:32,56:152,57:32,60:57,96:84,97:16,98:28,101:20,104:24,106:4,109:4,112:6},'NU':{0:-847872,1:348,2:184,3:120,4:36,5:156,6:200,7:60,8:12,9:212,10:52,11:12,12:69,13:8,14:6,15:24576,16:-589824,17:139264,18:-172032},'bound':61440,'classes':74,'columns':296,'positive':157},
}

def poly(n,w):
 p=[1]
 for multiplier in [3]*(n-w)+[-1]*w:
  q=[0]*(len(p)+1)
  for j,v in enumerate(p):
   q[j]+=v
   q[j+1]+=multiplier*v
  p=q
 return p

def kw(n):
 out=[[sum((-1)**r*3**(j-r)*comb(w,r)*comb(n-w,j-r)
      for r in range(max(0,j-(n-w)),min(j,w)+1))
      for w in range(n+1)] for j in range(n+1)]
 for w in range(n+1):
  assert [out[j][w] for j in range(n+1)]==poly(n,w)
 return out

def normalizer_patterns(sets):
 u=max(max(row) for row in sets)+1
 gens=[sum(1<<j for j in row) for row in sets]
 R=sorted({a^b^c for a in (0,gens[0])
                    for b in (0,gens[1]) for c in (0,gens[2])})
 assert len(R)==8
 reps=sorted({min(z^r for r in R) for z in range(1<<u)})
 xs=[x for x in range(1<<u)
     if all(((x&g).bit_count()&1)==0 for g in gens)]
 assert len(xs)==len(reps)==(1<<(u-3))
 patterns=Counter()
 for x in xs:
  for z in reps:
   hist=[0]*(u+1)
   for r in R:hist[(x|(z^r)).bit_count()]+=1
   patterns[tuple(hist)]+=1
 assert sum(patterns.values())==(1<<(2*u-6))
 assert all(sum(p)==8 for p in patterns)
 return u,patterns

def verify(name):
 u,patterns=normalizer_patterns(SETS[name])
 f=14-u
 pats=sorted(patterns)
 ncell=(u+1)*(f+1)
 nvar=len(pats)*(f+1)
 cert=CERT[name]
 assert len(pats)==cert['classes'] and nvar==cert['columns']
 def idx(a,b):return a*(f+1)+b
 H=[[0]*nvar for _ in range(ncell)]
 for k,pat in enumerate(pats):
  for b in range(f+1):
   col=k*(f+1)+b
   for a,mul in enumerate(pat):H[idx(a,b)][col]=mul
 Ku,Kf=kw(u),kw(f)
 T=[[0]*nvar for _ in range(ncell)]
 SH=[[0]*nvar for _ in range(ncell)]
 for a in range(u+1):
  for b in range(f+1):
   dest=idx(a,b)
   for i in range(u+1):
    for j in range(f+1):
     scalar=Ku[a][i]*Kf[b][j]
     signed=-scalar if (i+j)%2 else scalar
     src=H[idx(i,j)]
     if not any(src):continue
     for col,v in enumerate(src):
      if v:
       T[dest][col]+=scalar*v
       SH[dest][col]+=signed*v
 E=[H[0][:],[sum(row[j] for row in H) for j in range(nvar)]]
 rhs=[1,2048]
 for a in range(u+1):
  for b in range(f+1):
   if 1<=a+b<=4:
    k=idx(a,b)
    E.append([T[k][col]-2048*H[k][col] for col in range(nvar)])
    rhs.append(0)
 E.append([sum(H[idx(a,4-a)][col] for a in range(u+1)
               if 0<=4-a<=f) for col in range(nvar)])
 rhs.append(3)
 for w in (1,2,3):
  E.append([sum(H[idx(a,w-a)][col] for a in range(u+1)
                if 0<=w-a<=f) for col in range(nvar)])
  rhs.append(0)
 G=[[2048*H[i][col]-T[i][col] for col in range(nvar)]
    for i in range(ncell)]
 G.extend([[-T[i][col] for col in range(nvar)] for i in range(ncell)])
 G.extend([[-SH[i][col] for col in range(nvar)] for i in range(ncell)])
 lam,nu=cert['L'],cert['NU']
 assert len(G)==3*ncell and len(E)==len(rhs)
 assert len(E)==(19 if name=='one' else 20)
 assert all(0<=i<len(G) and mul>0 for i,mul in lam.items())
 assert all(0<=i<len(E) for i in nu)
 constant=sum(mul*rhs[i] for i,mul in nu.items())
 assert constant==-cert['bound']
 positives=0
 for col in range(nvar):
  remainder=(sum(mul*G[i][col] for i,mul in lam.items())
             +sum(mul*E[i][col] for i,mul in nu.items()))
  assert remainder>=0,(name,col,remainder)
  positives+=remainder>0
 assert positives==cert['positive']
 print('EXACT PASS',name,'prefix',u,'+',f,'classes',len(pats),
       'columns',nvar,'lambda',len(lam),'constant',constant,
       'positive residuals',positives)

if __name__=='__main__':
 for name in SETS:verify(name)
 print('FOUR EXACT OVERLAPPING H4=3 NO-GOS; disjoint geometry is checked by the separate 648-column verifier.')
 print('The H4=1 branch is handled by the graph/lift closure in the nonexistence manuscript.')
