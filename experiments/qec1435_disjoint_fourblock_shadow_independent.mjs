#!/usr/bin/env node
/**
 * Independent JavaScript replay of the full 648-column original-physical
 * 4+4+4+2 shadow Farkas certificate. No imports of Python, no floating point
 * LP solver, and no call to the first verifier.
 *
 * This validates the DISJOINT-H4=3 branch only. Global uniqueness also
 * depends on separate H4 parity, 4 overlapping triple geometries, and
 * double-H4 subgroup no-gos.
 */
import { readFileSync } from "node:fs";
const D=JSON.parse(readFileSync(
  new URL("./qec1435_disjoint_fourblock_exact_dual.json",import.meta.url),
  "utf8"
));
const pc=n=>{let v=0;while(n){n&=n-1;v++}return v};
function krawByPolynomial(n){
  return Array.from({length:n+1},(_,j)=>
    Array.from({length:n+1},(_,w)=>{
      let p=[1];
      for(let t=0;t<n;t++){
        const slope=t<n-w?3:-1;
        const q=Array(p.length+1).fill(0);
        for(let i=0;i<p.length;i++){
          q[i]+=p[i];q[i+1]+=slope*p[i];
        }
        p=q;
      }
      return p[j];
    })
  );
}
const groups=new Map();
for(let x=0;x<16;x++){
  if(pc(x)%2)continue;
  for(let z=0;z<16;z++){
    if(z>(z^15))continue;
    const a=Array(5).fill(0);
    a[pc(x|z)]++;a[pc(x|(z^15))]++;
    const key=a.join(",");
    groups.set(key,(groups.get(key)||0)+1);
  }
}
const patterns=[...groups].map(([k,v])=>({a:k.split(",").map(Number),count:v}))
  .sort((u,v)=>{for(let i=0;i<5;i++)if(u.a[i]!==v.a[i])
    return u.a[i]-v.a[i];return 0;});
if(patterns.length!==6||patterns.reduce((s,p)=>s+p.count,0)!==64)
  throw Error("64 original-physical block cosets");
const K4=krawByPolynomial(4),K2=krawByPolynomial(2);
const cells=[];
for(let a=0;a<5;a++)
  for(let b=0;b<5;b++)
    for(let c=0;c<5;c++)
      for(let z=0;z<3;z++)cells.push([a,b,c,z]);
const low=cells.filter(c=>{const w=c.reduce((s,x)=>s+x,0);
  return w>0&&w<=4;});
if(cells.length!==375||low.length!==64)
  throw Error("4+4+4+2 split cell count");
const T=patterns.map(({a})=>Array.from({length:5},(_,j)=>
  a.reduce((s,v,w)=>s+v*K4[j][w],0)));
const SH=patterns.map(({a})=>Array.from({length:5},(_,j)=>
  a.reduce((s,v,w)=>s+v*(w&1?-1:1)*K4[j][w],0)));
const nu=Object.entries(D.NU).map(([k,v])=>[+k,v]);
const lambda=Object.entries(D.L).map(([k,v])=>[+k,v]);
if(nu.length!==68||lambda.length!==43||lambda.some(([j,v])=>v<=0))
  throw Error("Farkas multiplier constraints");
const constant=2048*D.NU["0"]+2048**2*D.NU["1"]+
               3*2048*D.NU["69"];
let pos=0,zero=0,neg=0,min=Infinity;
for(let i=0;i<6;i++)
 for(let j=0;j<6;j++)
  for(let k=0;k<6;k++)
   for(let b=0;b<3;b++){
    const block=[patterns[i].a,patterns[j].a,patterns[k].a];
    const H=cell=>cell[3]===b?
      block[0][cell[0]]*block[1][cell[1]]*block[2][cell[2]]:0;
    const C=cell=>T[i][cell[0]]*T[j][cell[1]]*
      T[k][cell[2]]*K2[cell[3]][b];
    const V=cell=>SH[i][cell[0]]*SH[j][cell[1]]*
      SH[k][cell[2]]*K2[cell[3]][b]*(b&1?-1:1);
    const E=Array(70).fill(0);
    E[0]=2048*H([0,0,0,0]);
    E[1]=2048*8;
    for(let t=0;t<64;t++)E[t+2]=C(low[t])-2048*H(low[t]);
    for(let w=1;w<=4;w++)
      E[65+w]=2048*cells
        .filter(c=>c.reduce((s,x)=>s+x,0)===w)
        .reduce((s,c)=>s+H(c),0);
    const rem=nu.reduce((s,[q,v])=>s+v*E[q],0)-
      lambda.reduce((s,[q,v])=>s+v*V(cells[q-750]),0);
    if(!Number.isSafeInteger(rem))throw Error("unsafe numeric precision");
    if(rem>0)pos++;
    else if(rem===0)zero++;
    else neg++;
    min=Math.min(min,rem);
   }
if(!(pos===403&&zero===245&&neg===0&&min===0&&
     constant===-125829120))
  throw Error("disjoint H4=3 proof identity mismatch: "+
    JSON.stringify({pos,zero,neg,min,constant}));
console.log("INDEPENDENT JS PHYSICAL DISJOINT H4=3 FARKAS PASS");
console.log("64 four-site real Pauli cosets; six block-weight patterns");
console.log("648/648 exact physical original-four-block columns");
console.log("403 positive, 245 zero, NO negative coefficients");
console.log("rhs contradiction",constant);
console.log("LIMIT: other H4=3 supports and parent parity are separate proofs.");
