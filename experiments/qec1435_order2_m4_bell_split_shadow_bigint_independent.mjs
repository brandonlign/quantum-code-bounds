#!/usr/bin/env node
"use strict";
/* INDEPENDENT JS/BigInt verifier for ORIGINAL-physical 4+10 Bell
 * split-shadow certificate. The sparse immutable multipliers are copied
 * from the main Python certificate, but EVERY Krawtchouk coefficient,
 * original 55-cell transform, 39 equality rows, 165 inequality rows,
 * 55 column residuals and strict contradiction RHS are rebuilt here
 * using only integer polynomial multiplication and BigInt. No Python,
 * floating point, solver, import from primary checker, or external code
 * classification is needed.
 *
 * If a [[14,3,d>=5]] stabilizer contains original physical XXXX and
 * ZZZZ on SAME four sites, then its 4+10 physical split distribution
 * must satisfy Bell coset equations; full/split MacWilliams, distance
 * and affine shadow give the necessary inequalities below.
 */
import assert from "node:assert/strict";
const LAM={"5":6928035840,"14":188946432,"42":134061392,"43":2757441392,"46":1326542976,"64":70682880,"67":122972636160,"68":32876679168,"74":3464017920,"101":11431259136,"104":5888830464};
const NU={"1":-76298193,"4":-34682618340,"6":-15914513484,"7":-9992146944,"8":-28004724804,"10":6066470636,"11":-3695047552,"12":-2491478500,"13":1761058016,"14":622800644,"15":2437623040,"16":824048764,"17":3631687216,"18":339941692,"19":4082675968,"20":407953948,"21":3811805376,"22":713391828,"24":336437820,"25":91576037376,"26":65942304768,"27":17760964608,"28":9447321600,"34":5605410816,"35":2109901824,"36":6424178688,"37":3763183104,"38":153676431360};
const C={"5":31214958280704,"7":4192091504640,"22":174004044300288,"23":89818247725056,"24":86873034719232,"25":1031899447296,"26":12447287083008,"32":3095698341888,"33":225792497811456,"34":123473218240512,"35":56109532446720,"36":23314478137344,"37":4159844646912,"45":168801551253504,"46":30699008557056,"47":46757943705600,"54":644937154560};
const BOUND=320017816092672n;
const D=2048n,nvar=55,index=(a,b)=>11*a+b;
function polynomialKraw(n,target,source){
 let coefficients=[1n];
 for(let j=0;j<n-source;j++){
  const next=Array(coefficients.length+1).fill(0n);
  for(let k=0;k<coefficients.length;k++){
   next[k]+=coefficients[k];next[k+1]+=3n*coefficients[k];
  }
  coefficients=next;
 }
 for(let j=0;j<source;j++){
  const next=Array(coefficients.length+1).fill(0n);
  for(let k=0;k<coefficients.length;k++){
   next[k]+=coefficients[k];next[k+1]-=coefficients[k];
  }
  coefficients=next;
 }
 assert.equal(coefficients.length,n+1);
 return coefficients[target];
}
const K4=Array.from({length:5},(_,j)=>
 Array.from({length:5},(_,w)=>polynomialKraw(4,j,w)));
const K10=Array.from({length:11},(_,j)=>
 Array.from({length:11},(_,w)=>polynomialKraw(10,j,w)));
const T=Array.from({length:nvar},(_,r)=>{
 const a=Math.floor(r/11),b=r%11;
 return Array.from({length:nvar},(_,col)=>{
  const aa=Math.floor(col/11),bb=col%11;
  return K4[a][aa]*K10[b][bb];
 });
});
const sign=Array.from({length:nvar},(_,i)=>
  ((Math.floor(i/11)+i%11)&1)?-1n:1n);
const unit=j=>Array.from({length:nvar},(_,i)=>i===j?1n:0n);
const E=[],rhs=[],G=[];
function eq(row,value=0n){E.push(row);rhs.push(D*value);}
eq(unit(0).map(v=>D*v),1n);
eq(Array(nvar).fill(D),D);
eq(unit(1).map(v=>D*v));
for(let b=0;b<=10;b++){
 eq(unit(index(1,b)).map(v=>D*v));
 const row=Array(nvar).fill(0n);
 row[index(4,b)]=D;
 row[index(2,b)]=-D;
 row[index(0,b)]=-3n*D;
 eq(row);
}
for(let a=0;a<=4;a++)for(let b=0;b<=10;b++){
 const j=index(a,b),tr=T[j];
 if(a+b>0&&a+b<=4)
  eq(tr.map((v,i)=>v-(i===j?D:0n)));
 G.push(tr.map((v,i)=>(i===j?D:0n)-v));
 G.push(tr.map(v=>-v));
 G.push(tr.map((v,i)=>-sign[i]*v));
}
assert.equal(E.length,39);assert.equal(G.length,165);
assert.equal(Object.keys(LAM).length,11);
assert.equal(Object.keys(NU).length,28);
assert.equal(Object.keys(C).length,17);
assert.ok(Object.values(LAM).every(x=>x>0));
assert.ok(Object.values(C).every(x=>x>0));
const constant=Object.entries(NU).reduce((acc,[i,v])=>
 acc+BigInt(v)*rhs[Number(i)],0n);
assert.equal(constant,-BOUND);
let pos=0;
for(let col=0;col<nvar;col++){
 let q=0n;
 for(let [i,v]of Object.entries(LAM))
  q+=BigInt(v)*G[Number(i)][col];
 for(let [i,v]of Object.entries(NU))
  q+=BigInt(v)*E[Number(i)][col];
 const target=BigInt(C[col]||0);
 assert.equal(q,target,"Bell exact column "+col);
 assert.ok(q>=0n);if(q>0n)pos++;
}
assert.equal(pos,17);
console.log("PASS INDEPENDENT BIGINT ORIGINAL 4+10 BELL SPLIT-SHADOW");
console.log(JSON.stringify({physicalWeightCells:nvar,equalities:E.length,
 inequalities:G.length,positiveInequalityMultipliers:11,
 equalityMultipliers:28,positiveResidualCells:pos,
 negativeConstant:constant.toString(),independentKraw:"polynomial convolution"}));
