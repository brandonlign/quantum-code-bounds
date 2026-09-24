#!/usr/bin/env node
"use strict";
/* Standalone SECOND-LANGUAGE original 2+12 weight-two stabilizer no-go.
 * Imports only immutable SPARSE integer multipliers copied from the
 * previous Python proof. Independently rebuilds all physical 2+12
 * polynomial Krawtchouk coefficients, 39 variables, 13 equality rows,
 * 130 inequality rows, 39 exact integer residuals and strict negative RHS.
 * No library, old G/E matrices, floats, Python, optimizer, external code
 * classification or hidden purity assumption.
 */
import assert from "node:assert/strict";
const LAM={"0":2662400,"12":24576,"18":319488,"21":36864,"54":253952,"57":2048,"63":14336,"91":143360,"93":409600,"95":43008,"96":49152,"98":14336,"99":77824};
const NU={"0":-5672960,"1":2157,"2":1437696,"3":872448,"4":227328,"5":92160,"6":118784,"7":364544,"8":43008,"9":38912};
const C={"1":2214592512,"2":301989888,"3":1220542464,"4":239075328,"5":327155712,"13":6006243328,"14":3028287488,"15":2092957696,"16":1052770304,"17":494927872,"18":188743680,"19":29360128,"27":2977955840,"28":1686110208,"29":813694976,"30":327155712,"31":109051904};
const BOUND=2571108352n;
const D=2048n,N=39,idx=(a,b)=>13*a+b;
function kw(n,j,w){
 let poly=[1n];
 for(let k=0;k<n-w;k++){
  const next=Array(poly.length+1).fill(0n);
  for(let h=0;h<poly.length;h++){
   next[h]+=poly[h];next[h+1]+=3n*poly[h];
  }
  poly=next;
 }
 for(let k=0;k<w;k++){
  const next=Array(poly.length+1).fill(0n);
  for(let h=0;h<poly.length;h++){
   next[h]+=poly[h];next[h+1]-=poly[h];
  }
  poly=next;
 }
 assert.equal(poly.length,n+1);
 return poly[j];
}
const K2=Array.from({length:3},(_,j)=>
 Array.from({length:3},(_,w)=>kw(2,j,w)));
const K12=Array.from({length:13},(_,j)=>
 Array.from({length:13},(_,w)=>kw(12,j,w)));
const T=Array.from({length:N},(_,i)=>
 Array.from({length:N},(_,k)=>K2[Math.floor(i/13)][Math.floor(k/13)]*
                                  K12[i%13][k%13]));
const sign=Array.from({length:N},(_,i)=>
  ((Math.floor(i/13)+i%13)&1)?-1n:1n);
const unit=i=>Array.from({length:N},(_,j)=>i===j?1n:0n);
const E=[],rhs=[],G=[];
E.push(unit(0).map(x=>D*x));rhs.push(D);
E.push(Array(N).fill(D));rhs.push(D*D);
for(let b=0;b<13;b++){
 const row=Array(N).fill(0n);
 row[idx(0,b)]=D;row[idx(2,b)]=-D;
 G.push(row);
}
for(let a=0;a<3;a++)for(let b=0;b<13;b++){
 const j=idx(a,b),tr=T[j];
 if(a+b>0&&a+b<=4){
  E.push(tr.map((x,i)=>x-(i===j?D:0n)));
  rhs.push(0n);
 }
 G.push(tr.map((x,i)=>(i===j?D:0n)-x));
 G.push(tr.map(x=>-x));
 G.push(tr.map((x,i)=>-sign[i]*x));
}
assert.equal(E.length,13);assert.equal(G.length,130);
assert.equal(Object.keys(LAM).length,13);
assert.equal(Object.keys(NU).length,10);
assert.equal(Object.keys(C).length,17);
assert.ok(Object.values(LAM).every(x=>x>0));
assert.ok(Object.values(C).every(x=>x>0));
const normalization=Object.entries(NU).reduce((s,[i,v])=>
 s+BigInt(v)*rhs[Number(i)],0n);
assert.equal(normalization,-BOUND);
let positive=0;
for(let col=0;col<N;col++){
 let value=0n;
 for(let [i,v] of Object.entries(LAM))
  value+=BigInt(v)*G[Number(i)][col];
 for(let [i,v] of Object.entries(NU))
  value+=BigInt(v)*E[Number(i)][col];
 assert.equal(value,BigInt(C[col]||0),"incorrect physical column "+col);
 assert.ok(value>=0n);
 if(value>0n)positive++;
}
assert.equal(positive,17);
console.log("PASS INDEPENDENT BIGINT ORIGINAL 2+12 SPLIT SHADOW");
console.log(JSON.stringify({physicalWeightCells:N,equalities:E.length,
 inequalities:G.length,positiveDualRows:13,equalityDualRows:10,
 positiveResidualCells:positive,contradiction:normalization.toString(),
 Krawtchouk:"independent polynomial convolution"}));
