#!/usr/bin/env node
/**
 * Independently replay the 37 STORED additive codes, without importing ANY
 * Python classification, hull, coset, or lifter functions.  Input file
 * generators are binary X bits 0..9 and Z bits 10..19.
 *
 * This validates every individual recorded code, its exact physical d=5,
 * binary trace-symplectic Gram radical, and every one of the 64 actual
 * suffix coset minima for every hull-four class. It deliberately does NOT
 * independently regenerate or certify nauty class COMPLETENESS; that
 * remains the separate lengthening-census/referee obligation.
 */
import { readFileSync } from "node:fs";

const N = 10, MASK = (1 << N) - 1;
const input = JSON.parse(readFileSync(
  new URL("./qec1435_n10_additive_37_generators_xy.json",import.meta.url),
  "utf8"
));
function parity(v) {
  let p = 0; while (v) { v &= v-1; p ^= 1; } return p;
}
function rank(values) {
  const piv = new Map();
  for (const v of values) {
    let x = v;
    while (x) {
      const j = 31 - Math.clz32(x);
      if (!piv.has(j)) { piv.set(j,x);break; }
      x ^= piv.get(j);
    }
  }
  return piv.size;
}
function nullspace(rows,n) {
  const A=rows.slice(),piv=[],out=[];
  let r=0;
  for(let j=0;j<n;j++){
    let k=r;
    while(k<A.length&&!((A[k]>>>j)&1))k++;
    if(k===A.length)continue;
    [A[r],A[k]]=[A[k],A[r]];
    for(let i=0;i<A.length;i++)
      if(i!==r&&((A[i]>>>j)&1))A[i]^=A[r];
    piv.push(j);r++;
  }
  for(let j=0;j<n;j++){
    if(piv.includes(j))continue;
    let v=1<<j;
    for(let i=0;i<r;i++)if((A[i]>>>j)&1)v|=1<<piv[i];
    if(rows.some(a=>parity(a&v)))throw Error("kernel failure");
    out.push(v);
  }
  return out;
}
function span(rows) {
  const out=[0];
  for(const row of rows){
    const old=out.length;
    for(let i=0;i<old;i++)out.push(out[i]^row);
  }
  return out;
}
function weight(v) {
  let x=(v&MASK)|(v>>>N),w=0;
  while(x){x&=x-1;w++;}
  return w;
}
function sym(a,b) {
  return parity(((a&MASK)&(b>>>N))^((a>>>N)&(b&MASK)));
}
function hullBasis(gens) {
  const gram=gens.map(a=>gens.reduce((bits,b,i)=>
    bits|(sym(a,b)<<i),0));
  return nullspace(gram,N).map(selector=>
    gens.reduce((bits,v,i)=>bits^(((selector>>>i)&1)?v:0),0));
}
function symplPerpBasis(gens) {
  return nullspace(gens.map(x=>
    ((x>>>N)&MASK)|((x&MASK)<<N)),2*N);
}
function cosetHistogram(G,H,C) {
  const dual=symplPerpBasis(H);
  if(dual.length!==16)throw Error("wrong 16D H perp");
  const independent=G.slice(),Q=[];
  for(const v of dual) {
    if(rank([...independent,v])>independent.length){
      independent.push(v);Q.push(v);
    }
  }
  if(Q.length!==6||independent.length!==16)
    throw Error("6D coset complement not found");
  const leaders={};
  for(const q of span(Q)){
    let minimum=11;
    for(const c of C){
      const wt=weight(q^c);
      if(wt<minimum)minimum=wt;
      if(minimum===0)break;
    }
    leaders[minimum]=(leaders[minimum]||0)+1;
  }
  return leaders;
}
const counts={},audit=[];
if(input.length!==37)throw Error("expected 37 input matrices");
for(let i=0;i<input.length;i++){
  const G=input[i];
  if(G.length!==10||G.some(x=>!Number.isInteger(x)||x<0||x>=1<<20))
    throw Error("invalid generator class "+(i+1));
  if(rank(G)!==10)throw Error("rank "+(i+1));
  const C=span(G);
  if(C.length!==1024||new Set(C).size!==1024)
    throw Error("size "+(i+1));
  if(Math.min(...C.slice(1).map(weight))!==5)
    throw Error("distance "+(i+1));
  const H=hullBasis(G),h=H.length;
  if(rank(H)!==h||H.some(x=>!C.includes(x))||
     H.some(x=>G.some(y=>sym(x,y))))
    throw Error("hull "+(i+1));
  counts[h]=(counts[h]||0)+1;
  if(h!==4)continue;
  const spectrum=cosetHistogram(G,H,C);
  const c1=(spectrum[1]||0),
        c2=c1+(spectrum[2]||0),
        c3=c2+(spectrum[3]||0);
  const passed=(c1<=8&&c2<=32&&c3<=59);
  if(passed)throw Error("HULL-4 SURVIVES: class "+(i+1));
  audit.push({class:i+1,spectrum,cumulative:[c1,c2,c3]});
}
if(JSON.stringify(counts)!==JSON.stringify({0:7,2:14,4:12,6:2,8:2}))
  throw Error("hull distribution differs");
if(audit.length!==12)throw Error("expected 12 hull-four candidates");
const expected={9:[0,39,63],12:[2,39,63],14:[0,39,63],
  15:[0,27,63],17:[2,39,63],20:[0,35,62],
  21:[2,39,63],22:[0,23,63],26:[0,35,62],
  34:[2,39,63],35:[2,39,63],37:[2,39,63]};
for(const row of audit)
  if(JSON.stringify(row.cumulative)!==JSON.stringify(expected[row.class]))
    throw Error("incorrect class "+row.class);
console.log("INDEPENDENT JS EXACT CHECK PASS: all 37 actual stored ten-site codebooks");
console.log("25 classes hull != 4; hull dimensions:",JSON.stringify(counts));
console.log("12/12 hull-four classes fail ORIGINAL-physical 8/32/59 Hall gate");
console.log("class: spectrum / cumulative [d<=1,d<=2,d<=3]");
for(const row of audit)
  console.log(row.class,JSON.stringify(row.spectrum),JSON.stringify(row.cumulative));
console.log("LIMIT: This independent JS codebook replayer does NOT itself certify");
console.log("that 37 is a COMPLETE equivalence-class enumeration.");
