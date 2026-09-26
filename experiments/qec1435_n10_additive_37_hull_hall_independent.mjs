#!/usr/bin/env node
"use strict";
/* Recompute hull dimensions and coset-capacity bounds for the 37 saved
 * length-ten additive codes using JavaScript.
 */
import { readFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
const GENS=join(dirname(fileURLToPath(import.meta.url)),
  "qec1435_n10_additive_37_generators_xy.json");
const M=(1<<10)-1;
function pop(x){let n=0;for(;x;x&=x-1)n++;return n;}
function rank(a){const piv=new Map();let n=0;for(let v of a){while(v){const j=31-Math.clz32(v);if(piv.has(j))v^=piv.get(j);else{piv.set(j,v);n++;break;}}}return n;}
function kernel(rows,n){const a=rows.slice(),p=[];let r=0;for(let j=0;j<n;j++){let k=r;while(k<a.length&&!((a[k]>>>j)&1))k++;if(k==a.length)continue;[a[r],a[k]]=[a[k],a[r]];for(let i=0;i<a.length;i++)if(i!=r&&((a[i]>>>j)&1))a[i]^=a[r];p.push(j);r++;}const ans=[];for(let j=0;j<n;j++){if(p.includes(j))continue;let v=1<<j;for(let i=0;i<r;i++)if((a[i]>>>j)&1)v|=1<<p[i];if(rows.some(row=>pop(row&v)&1))throw Error("binary nullspace residual");ans.push(v);}return ans;}
function span(g){const out=[0];for(const v of g){const len=out.length;for(let i=0;i<len;i++)out.push(out[i]^v);}return out;}
function phys(v,n=10){const mask=(1<<n)-1;return pop((v&mask)|(v>>>n));}
function sym(a,b){return pop(((a&M)&(b>>>10))^((a>>>10)&(b&M)))&1;}
function fourPrefix(){const s=new Set(),cost={};const p=0xf0;for(let v=0;v<256;v++){if(pop(v&15)&1)continue;s.add(Math.min(v,v^p));}if(s.size!==64)throw Error("prefix quotient not 64");for(const v of s){const c=Math.min(phys(v,4),phys(v^p,4));cost[c]=(cost[c]||0)+1;}if(JSON.stringify([0,1,2,3,4].map(k=>cost[k]||0))!==JSON.stringify([1,4,27,24,8]))throw Error("prefix capacity incorrect");return cost;}
function auditOne(g,i){if(g.length!==10||g.some(x=>!Number.isInteger(x)||x<0||x>=1<<20)||rank(g)!==10)throw Error("bad candidate "+i);const C=span(g);if(new Set(C).size!==1024)throw Error("bad cardinality");const d=Math.min(...C.slice(1).map(x=>phys(x)));if(d!==5)throw Error("bad distance");const gram=g.map(a=>g.reduce((sum,b,j)=>sum|(sym(a,b)<<j),0));const hcoeff=kernel(gram,10);const h=hcoeff.map(mask=>g.reduce((v,x,j)=>v^(((mask>>>j)&1)?x:0),0));const hd=h.length;if(rank(h)!==hd)throw Error("hull inconsistency");
const record={class:i+1,distance:d,hull:hd};
if(hd!==4)return record;
const Hperp=kernel(h.map(v=>((v>>>10)&M)|((v&M)<<10)),20);
if(Hperp.length!==16)throw Error("hull-perp dimension");const ext=g.slice(),Q=[];
for(const v of Hperp){if(rank([...ext,v])>ext.length){ext.push(v);Q.push(v);}}
if(Q.length!==6)throw Error("quotient dimension");const D=span(Q),hist={};for(const v of D){let low=11;for(const c of C){const w=phys(v^c);if(w<low)low=w;if(low===0)break;}hist[low]=(hist[low]||0)+1;}if(hist[0]!==1||Object.values(hist).reduce((a,b)=>a+b,0)!==64)throw Error("cosets are not distinct");
const n1=hist[1]||0,n2=n1+(hist[2]||0),n3=n2+(hist[3]||0);
record.cosetMinima=hist;record.capacities={n1,n2,n3};record.excluded=n1>8||n2>32||n3>59;
if(!record.excluded)throw Error("SURVIVING CLASS: "+(i+1));
return record;}
function main(){const inputs=JSON.parse(readFileSync(GENS,"utf8"));if(inputs.length!==37)throw Error("not 37 inputs");
const prefix=fourPrefix(),rows=inputs.map(auditOne),hulls={};for(const x of rows)hulls[x.hull]=(hulls[x.hull]||0)+1;
if(JSON.stringify([0,2,4,6,8].map(k=>hulls[k]||0))!==JSON.stringify([7,14,12,2,2]))throw Error("unexpected hull counts");
const h4=rows.filter(x=>x.hull===4);if(h4.length!==12||h4.some(x=>!x.excluded||x.capacities.n3<62||x.capacities.n3>63))throw Error("hull4 closure failed");
console.log(JSON.stringify({source:basename(GENS),prefixCost:prefix,candidates:rows.length,hulls,hull4:h4},null,2));
}
main();
