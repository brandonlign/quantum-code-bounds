#!/usr/bin/env node
"use strict";
/* Independently reconstruct ALL FOUR overlapping rank-three H4=3
 * original-physical subgroup-model exact Farkas contradictions.
 * True ten-to-eleven-site prefix Pauli x|z cosets, direct polynomial
 * Krawtchouk convolution, 14-site genuine split and JS BigInt duals.
 * Imports ONLY integer multipliers and expected row/column totals from
 * the Python certificate source. It imports no Python computations.
 *
 * Node stdlib: node experiments/qec1435_sparse_h4_rank3_four_bigint_independent.mjs
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";
let txt=readFileSync(join(dirname(fileURLToPath(import.meta.url)),
 "qec1435_sparse_h4_rank3_four_exact.py"),"utf8");
let source=txt.split("CERT = ")[1].split("\n\ndef poly")[0];
source=source.replace(/'/g,'"')
 .replace(/([{,]\s*)(\d+)\s*:/g,'$1"$2":')
 .replace(/,\s*}/g,'}');
const CERT=JSON.parse(source);
const SETS={
 triangle:[[0,1,2,3],[3,4,5,6],[2,4,7,8]],
 common:[[0,1,2,3],[3,4,5,6],[3,7,8,9]],
 two:[[0,1,2,3],[3,4,5,6],[6,7,8,9]],
 one:[[0,1,2,3],[3,4,5,6],[7,8,9,10]],
};
function bits(x){let r=0;while(x){x&=x-1;r++}return r}
function kraw(n){
 const K=Array.from({length:n+1},()=>Array(n+1).fill(0));
 for(let w=0;w<=n;w++){
  let p=[1];
  for(const slope of [...Array(n-w).fill(3),...Array(w).fill(-1)]){
   const q=Array(p.length+1).fill(0);
   for(let j=0;j<p.length;j++){
    q[j]+=p[j];q[j+1]+=p[j]*slope;
   }
   p=q;
  }
  for(let j=0;j<=n;j++)K[j][w]=p[j];
 }
 return K;
}
const summary=[];
for(const [name,sets] of Object.entries(SETS)){
 const U=1+Math.max(...sets.flat()),F=14-U,mask=(1<<U)-1;
 const checks=sets.map(p=>p.reduce((x,i)=>x|(1<<i),0));
 let R=[0];
 for(const g of checks){
  const count=R.length;
  for(let i=0;i<count;i++)R.push(R[i]^g);
 }
 assert.equal(new Set(R).size,8);
 const reps=new Set();
 for(let z=0;z<=mask;z++)
  reps.add(Math.min(...R.map(t=>z^t)));
 const hist=new Map();
 for(let x=0;x<=mask;x++){
  if(checks.some(z=>bits(x&z)%2))continue;
  for(const z of reps){
   const pattern=Array(U+1).fill(0);
   for(const t of R)pattern[bits(x|(z^t))]++;
   const key=pattern.join(",");
   hist.set(key,(hist.get(key)||0)+1);
  }
 }
 const patterns=[...hist.keys()].map(key=>key.split(",").map(Number))
  .sort((a,b)=>{for(let i=0;i<a.length;i++)
   if(a[i]!==b[i])return a[i]-b[i];return 0});
 const KU=kraw(U),KF=kraw(F);
 const transform=(p,signed)=>Array.from({length:U+1},(_,j)=>
  p.reduce((sum,v,i)=>sum+v*KU[j][i]*(signed&&(i&1)?-1:1),0));
 const ordinary=patterns.map(p=>transform(p,false));
 const signed=patterns.map(p=>transform(p,true));
 const cells=[],low=[];
 for(let a=0;a<=U;a++)for(let b=0;b<=F;b++){
  const row=[a,b];
  cells.push(row);
  if(a+b>=1&&a+b<=4)low.push(row);
 }
 const ncell=cells.length,cert=CERT[name];
 const L=Object.entries(cert.L).map(([i,v])=>[Number(i),BigInt(v)]);
 const NU=Object.entries(cert.NU).map(([i,v])=>[Number(i),BigInt(v)]);
 assert.equal(patterns.length,cert.classes);
 assert.equal(patterns.length*(F+1),cert.columns);
 assert.equal(low.length+6,name==="one"?19:20);
 let positive=0,zero=0;
 for(let pi=0;pi<patterns.length;pi++)for(let suffix=0;suffix<=F;suffix++){
  const pat=patterns[pi],t=ordinary[pi],st=signed[pi];
  const H=([a,b])=>b===suffix?pat[a]:0;
  const T=([a,b])=>t[a]*KF[b][suffix];
  const SH=([a,b])=>st[a]*KF[b][suffix]*(suffix&1?-1:1);
  const E=[BigInt(H([0,0])),8n];
  for(const row of low)E.push(BigInt(T(row)-2048*H(row)));
  for(const weight of [4,1,2,3]){
   let count=0;
   for(const row of cells)
    if(row[0]+row[1]===weight)count+=H(row);
   E.push(BigInt(count));
  }
  assert.equal(E.length,name==="one"?19:20);
  let remainder=NU.reduce((s,[i,v])=>s+v*E[i],0n);
  for(const [i,v] of L){
   const kind=Math.floor(i/ncell),row=cells[i%ncell];
   const coeff=kind===0?2048*H(row)-T(row):
     kind===1?-T(row):-SH(row);
   assert(kind<=2);
   remainder+=v*BigInt(coeff);
  }
  assert(remainder>=0n,"negative residual "+name+" "+pi+" "+suffix);
  if(remainder>0n)positive++;else zero++;
 }
 const rhs=NU.reduce((s,[i,v])=>
  s+v*(i===0?1n:i===1?2048n:i===2+low.length?3n:0n),0n);
 assert.equal(rhs,-BigInt(cert.bound));
 assert.equal(positive,cert.positive);
 assert.equal(positive+zero,cert.columns);
 summary.push({name,prefix_sites:U,suffix_sites:F,
  physical_pattern_types:patterns.length,variables:cert.columns,
  positive,zero,dual_constant:rhs.toString()});
 console.log("INDEPENDENT BigInt H4=3 no-go",name,
  U+"+"+F,"original sites",cert.columns,"columns",
  "rhs="+rhs.toString(),"positive="+positive,"zero="+zero);
}
assert.equal(summary.length,4);
console.log("ALL FOUR ORIGINAL-SITE OVERLAPPING H4=3 CASES PASS");
