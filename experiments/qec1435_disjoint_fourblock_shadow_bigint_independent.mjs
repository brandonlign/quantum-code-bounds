#!/usr/bin/env node
"use strict";
/* Independent BigInt replay of ORIGINAL-physical disjoint H4=3 no-go.
 * Literal four-site x,z Pauli cosets; original 4+4+4+2 split; polynomial
 * convolution Krawtchouk; exact 648-column integer dual. Node stdlib.
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";
const data=JSON.parse(readFileSync(join(dirname(fileURLToPath(import.meta.url)),
 "qec1435_disjoint_fourblock_exact_dual.json"),"utf8"));
const L=Object.entries(data.L).map(([i,v])=>[Number(i),BigInt(v)]);
const NU=Object.entries(data.NU).map(([i,v])=>[Number(i),BigInt(v)]);
assert.equal(L.length,43);assert.equal(NU.length,68);
function bits(x){let r=0;while(x){x&=x-1;r++}return r}
const pmap=new Map();
for(let x=0;x<16;x++){
 if(bits(x)%2)continue;
 for(let z=0;z<16;z++){
  if(z>(z^15))continue;
  let counts=[0,0,0,0,0];
  for(const zz of [0,15])counts[bits(x|(z^zz))]++;
  const key=counts.join(",");
  pmap.set(key,(pmap.get(key)||0)+1);
 }
}
assert.deepEqual([...pmap.entries()].sort(),[
 ["0,0,0,0,2",8],["0,0,0,2,0",24],["0,0,1,0,1",24],
 ["0,0,2,0,0",3],["0,1,0,1,0",4],["1,0,0,0,1",1]
].sort());
const patterns=[...pmap.keys()].sort().map(key=>key.split(",").map(Number));
assert.equal(patterns.length,6);
function convolution(slopes){
 let p=[1];
 for(const slope of slopes){
  const q=new Array(p.length+1).fill(0);
  for(let j=0;j<p.length;j++){
   q[j]+=p[j];q[j+1]+=slope*p[j];
  }
  p=q;
 }
 return p;
}
function Kraw(n){
 let K=Array.from({length:n+1},()=>new Array(n+1).fill(0));
 for(let w=0;w<=n;w++){
  const c=convolution([...Array(n-w).fill(3),...Array(w).fill(-1)]);
  for(let j=0;j<=n;j++)K[j][w]=c[j];
 }
 return K;
}
const K4=Kraw(4),K2=Kraw(2);
const tr=(p,signed)=>Array.from({length:5},(_,j)=>
 p.reduce((sum,v,w)=>sum+v*K4[j][w]*(signed&&(w&1)?-1:1),0));
const T=patterns.map(p=>tr(p,false)),S=patterns.map(p=>tr(p,true));
const cells=[],low=[];
for(let a=0;a<5;a++)for(let b=0;b<5;b++)
for(let c=0;c<5;c++)for(let d=0;d<3;d++){
 const row=[a,b,c,d];
 cells.push(row);
 if(a+b+c+d>=1&&a+b+c+d<=4)low.push(row);
}
assert.equal(cells.length,375);assert.equal(low.length,64);
let positive=0,zero=0;
for(let a=0;a<6;a++)for(let b=0;b<6;b++)
for(let c=0;c<6;c++)for(let d=0;d<3;d++){
 const pat1=patterns[a],pat2=patterns[b],pat3=patterns[c];
 const A=T[a],B=T[b],C=T[c],SA=S[a],SB=S[b],SC=S[c];
 const H=([i,j,k,l])=>l===d?pat1[i]*pat2[j]*pat3[k]:0;
 const transformed=([i,j,k,l],signed)=>
  BigInt((signed?SA:A)[i])*BigInt((signed?SB:B)[j])*
  BigInt((signed?SC:C)[k])*BigInt(K2[l][d])*
  BigInt(signed&&(d&1)?-1:1);
 const E=new Array(70).fill(0n);
 E[0]=2048n*BigInt(H([0,0,0,0]));
 E[1]=2048n*8n;
 for(let k=0;k<64;k++)
  E[2+k]=transformed(low[k],false)-2048n*BigInt(H(low[k]));
 for(let w=1;w<=4;w++){
  let count=0;
  for(const row of cells)
   if(row[0]+row[1]+row[2]+row[3]===w)count+=H(row);
  E[65+w]=2048n*BigInt(count);
 }
 let residual=NU.reduce((sum,[index,v])=>sum+v*E[index],0n);
 for(const [index,v] of L){
  assert(index>=750&&index<1125);
  residual-=v*transformed(cells[index-750],true);
 }
 assert(residual>=0n,"negative Farkas residual "+[a,b,c,d]);
 if(residual>0n)positive++;else zero++;
}
const rhs=NU.reduce((sum,[i,v])=>
 sum+v*(i===0?2048n:i===1?2048n**2n:i===69?2048n*3n:0n),0n);
assert.equal(positive,403);
assert.equal(zero,245);
assert.equal(rhs,-125829120n);
assert.equal(rhs,BigInt(data.constant));
console.log("INDEPENDENT EXACT ORIGINAL 4+4+4+2 SHADOW PASS");
console.log("64 literal <ZZZZ> cosets / 6 patterns per real block");
console.log("648 original-physical subgroup coset columns");
console.log("403 positive, 245 zero Farkas residuals; none negative");
console.log("68 equality and 43 physical shadow inequality multipliers");
console.log("exact contradiction: 0 <= c*y <= "+rhs.toString());
