#!/usr/bin/env node
"use strict";
/*
Second-language, independently rebuilt EXACT six-site crossed-overlap subgroup
no-go. This JS source derives all physical prefix cosets and all signed
split-MacWilliams coefficients with BigInt; its immutable multipliers
must match the separate crossed-overlap Python verifier:
  qec1435_crossed_bell_sixsite_split_shadow_exact.py

 H=<ZZZZII, XXIIXX> has nonzero subgroup weights 4,4,6 on
two 2-site-overlapping pair supports. This script asserts
physical-normalizer coset geometry, 126 exact integer certificate
columns, 78 nonzero nonnegative residual coefficients, contradiction
-22212608. No numerical LP is executed for the replay.
*/
import assert from "node:assert/strict";
const W=6,F=8,MASK=63,SCALE=2048n;
const R=[0,51,15<<W,51^(15<<W)];
const PREFIX=[
 [0,1,0,1,0,2,0],
 [0,0,0,1,0,3,0],
 [0,0,0,0,4,0,0],
 [0,0,0,0,0,4,0],
 [0,0,0,2,0,2,0],
 [0,0,0,0,2,0,2],
 [0,0,0,0,3,0,1],
 [0,0,1,0,1,0,2],
 [0,0,0,0,1,0,3],
 [0,0,1,0,2,0,1],
 [0,0,2,0,1,0,1],
 [0,0,0,3,0,1,0],
 [0,0,1,0,3,0,0],
 [1,0,0,0,2,0,1],
];
const MULT=[4,48,16,32,32,32,40,8,16,16,2,4,5,1];
const LAM={54:888,127:8280,128:1614,135:5584,136:2839,
           138:337,144:2732,146:674,154:1455,162:1792,180:444};
const NU={0:-311595008,1:141300,2:49068,3:31368,4:8874,
          5:3996,6:34240,7:22408,8:5964,9:2878,10:16112,
          11:3054,12:1760,13:2808,14:1086,15:1300};
const pc=x=>{let n=0;while(x){x&=x-1;n++;}return n;};
const wt=v=>pc((v&MASK)|(v>>>W));
const sym=(v,w)=>(pc((v&MASK)&(w>>>W))+
                   pc((w&MASK)&(v>>>W)))&1;
for(let a of R)for(let b of R)assert.equal(sym(a,b),0);
assert.deepEqual(R.map(wt),[0,4,4,6]);

const hist=new Map();
let central=0,cosets=0;
for(let v=0;v<(1<<(2*W));v++){
 if(R.some(r=>sym(v,r)))continue;
 central++;
 const orbit=R.map(r=>v^r).sort((a,b)=>a-b);
 if(v!==orbit[0])continue;
 cosets++;
 const counts=Array(W+1).fill(0);
 for(let w of orbit)counts[wt(w)]++;
 const key=counts.join(",");
 hist.set(key,(hist.get(key)||0)+1);
}
assert.equal(central,1024);
assert.equal(cosets,256);
assert.equal(hist.size,14);
assert.equal(MULT.reduce((a,b)=>a+b,0),256);
for(let t=0;t<PREFIX.length;t++)
 assert.equal(hist.get(PREFIX[t].join(",")),MULT[t]);

function polynomial(n,w){
 let p=[1n];
 for(let k=0;k<n;k++){
  const factor=k<n-w?3n:-1n;
  const q=Array(p.length+1).fill(0n);
  for(let i=0;i<p.length;i++){
   q[i]+=p[i];q[i+1]+=factor*p[i];
  }
  p=q;
 }
 return p;
}
function transform(n){
 const K=Array.from({length:n+1},
  ()=>Array(n+1).fill(0n));
 for(let w=0;w<=n;w++){
  const p=polynomial(n,w);
  for(let j=0;j<=n;j++)K[j][w]=p[j];
 }
 return K;
}
const KW=transform(W),KF=transform(F);
const idx=(a,b)=>a*(F+1)+b;
const NCELL=(W+1)*(F+1),NVAR=PREFIX.length*(F+1);
assert.equal(NCELL,63);assert.equal(NVAR,126);
const H=Array.from({length:NCELL},()=>Array(NVAR).fill(0n));
for(let t=0;t<PREFIX.length;t++)
 for(let b=0;b<=F;b++)
  for(let a=0;a<=W;a++)
   H[idx(a,b)][t*(F+1)+b]=BigInt(PREFIX[t][a]);
const T=Array.from({length:NCELL},()=>Array(NVAR).fill(0n));
const SH=Array.from({length:NCELL},()=>Array(NVAR).fill(0n));
for(let a=0;a<=W;a++)for(let b=0;b<=F;b++)
 for(let i=0;i<=W;i++)for(let j=0;j<=F;j++){
  const dst=idx(a,b),src=idx(i,j),
   factor=KW[a][i]*KF[b][j],sign=(i+j)%2?-1n:1n;
  for(let v=0;v<NVAR;v++){
   T[dst][v]+=factor*H[src][v];
   SH[dst][v]+=sign*factor*H[src][v];
  }
 }
const E=[
 H[0].slice(),
 Array.from({length:NVAR},(_,v)=>H.reduce((z,row)=>z+row[v],0n))
],rhs=[1n,SCALE];
for(let a=0;a<=W;a++)for(let b=0;b<=F;b++){
 if(a+b<1||a+b>4)continue;
 const q=idx(a,b);
 E.push(T[q].map((z,v)=>z-SCALE*H[q][v]));
 rhs.push(0n);
}
assert.equal(E.length,16);
let normal=0n;
for(let [k,z] of Object.entries(NU))
 normal+=BigInt(z)*rhs[Number(k)];
assert.equal(normal,-22212608n);
let positive=0,max=0n;
for(let v=0;v<NVAR;v++){
 let residual=0n;
 for(let [i,z] of Object.entries(LAM)){
  const q=Number(i),weight=BigInt(z);
  const coeff=q<NCELL
    ?SCALE*H[q][v]-T[q][v]
    :q<2*NCELL?-T[q-NCELL][v]:-SH[q-2*NCELL][v];
  residual+=weight*coeff;
 }
 for(let [i,z] of Object.entries(NU))
  residual+=BigInt(z)*E[Number(i)][v];
 assert.ok(residual>=0n,"negative exact residual "+v+": "+residual);
 if(residual>0n)positive++;
 if(residual>max)max=residual;
}
assert.equal(positive,78);
assert.equal(max,280477696n);
if(typeof console!=="undefined"){
 console.log("EXACT BIGINT CROSSED-OVERLAP NO-GO PASS");
 console.log("1024 physical centralizer words, 256 cosets, 14 patterns;");
 console.log("126/126 dual columns, 78 positive residuals;");
 console.log("negative normalization",normal.toString());
}
