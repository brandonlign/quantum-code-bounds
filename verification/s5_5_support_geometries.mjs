#!/usr/bin/env node
"use strict";
/*
Enumerate the five possible rank-three support geometries for three
weight-four stabilizer words and verify their pairwise products.

If two weight-four Pauli labels commute and their supports meet in t
original sites, with h different nonidentity labels in that intersection,
their product weight is 8-2t+h and h must be even.
*/
import assert from "node:assert/strict";
const expected=[
 {8:1},{6:1},{4:1,6:4},{2:1,4:12},{2:24,4:16}
];
function pairCensus(t){
  const results={};
  for(let code=0;code<3**t;code++){
    let x=code,changed=0;
    for(let k=0;k<t;k++){
      const symbol=x%3;x=Math.floor(x/3);
      if(symbol!==0)changed++;
    }
    if(t===4&&changed===0)continue; // identical Pauli word
    if(changed%2)continue; // original-physical anticommutation
    const productWeight=8-2*t+changed;
    results[productWeight]=(results[productWeight]??0)+1;
  }
  return results;
}
for(let t=0;t<=4;t++)
 assert.deepEqual(pairCensus(t),expected[t],`pairwise overlap ${t}`);

const TYPES=[
 ["disjoint",[[0,1,2,3],[4,5,6,7],[8,9,10,11]],12,[8,8,8],12],
 ["one-pair",[[0,1,2,3],[3,4,5,6],[7,8,9,10]],11,[6,8,8],10],
 ["two-pair",[[0,1,2,3],[3,4,5,6],[6,7,8,9]],10,[6,6,8],8],
 ["triangle",[[0,1,2,3],[3,4,5,6],[2,4,7,8]],9,[6,6,6],6],
 ["common",[[0,1,2,3],[3,4,5,6],[3,7,8,9]],10,[6,6,6],10],
];
const pop=x=>{let s=0;while(x){x&=x-1;s++}return s};
const combos=[[0,1],[0,2],[1,2]];
const seen=new Set();
for(const [name,sets,unionsize,pairweights,tripleweight] of TYPES){
  const masks=sets.map(a=>a.reduce((x,i)=>x|(1<<i),0));
  assert.equal(new Set(masks).size,3);
  assert.ok(sets.flat().every(i=>Number.isInteger(i)&&i>=0&&i<14));
  assert.ok(sets.every(a=>a.length===4&&new Set(a).size===4));
  const overlap=combos.map(([i,j])=>pop(masks[i]&masks[j]));
  assert.ok(overlap.every(x=>x<=1));
  assert.equal(pop(masks[0]|masks[1]|masks[2]),unionsize);
  const triple=pop(masks[0]&masks[1]&masks[2]);
  const signature=[...overlap].sort().join("")+";"+triple;
  assert.ok(!seen.has(signature));seen.add(signature);
  const actualPairWeights=combos.map(([i,j])=>pop(masks[i]^masks[j])).sort((a,b)=>a-b);
  assert.deepEqual(actualPairWeights,[...pairweights].sort((a,b)=>a-b));
  assert.equal(pop(masks[0]^masks[1]^masks[2]),tripleweight);
  const spanWeights=Array.from({length:7},(_,k)=>{
    let m=0;for(let i=0;i<3;i++)if((k+1)>>i&1)m^=masks[i];
    return pop(m);
  });
  assert.equal(spanWeights.filter(x=>x===4).length,3);
  assert.ok(spanWeights.every(x=>x>=4));
  console.log(name,JSON.stringify({signature,union:unionsize,spanWeights}));
}
assert.equal(seen.size,5);
console.log("PASS: all five normalized rank-three four-check support geometries");
console.log("PASS: distinct pair commuting overlap census, t=0..4");
