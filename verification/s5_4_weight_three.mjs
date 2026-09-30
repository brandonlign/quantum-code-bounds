#!/usr/bin/env node
"use strict";
// Second, non-Python verifier of the 3+11 weight-three split-shadow dual.
// Derives Krawtchouk tables via polynomial multiplication using JS BigInt.
const L={49:22,50:5,51:8,52:1,63:4,72:31,73:20,74:11,108:2,120:7,122:1,132:2};
const U={1:-11,2:32,3:12,4:10,5:2,6:40,9:4,11:20,12:12,13:40};
const R={3:8192,4:4096,16:4096,29:4096,35:4096};
const chk=(p,m)=>{if(!p)throw Error(m)};
const bits=x=>{let b=0;while(x){b+=x&1;x>>>=1;}return b};
const symp=(v,w,n)=>{let t=(1<<n)-1;return (bits((v&t)&(w>>n))+bits((w&t)&(v>>n)))&1};
const wt=(v,n)=>bits((v&((1<<n)-1))|(v>>n));
const p=7<<3,seen=new Set(),hist=new Map();
for(let v=0;v<64;v++){
 if(symp(v,p,3))continue;
 let twin=v^p,id=Math.min(v,twin);
 if(seen.has(id))continue;
 seen.add(id);
 let pat=Array.from({length:4},(_,k)=>Number(wt(v,3)===k)+Number(wt(twin,3)===k)).join(",");
 hist.set(pat,(hist.get(pat)||0)+1);
}
chk(seen.size===16&&hist.get("0,0,1,1")===12&&hist.get("0,1,1,0")===3&&hist.get("1,0,0,1")===1&&hist.size===3,"physical ZZZ coset failure");
const P=[[0,0,1,1],[0,1,1,0],[1,0,0,1]],S=2048n,N=36;
function poly(n,w){
 let a=[1n];
 for(let k=0;k<n;k++){
  const c=k<n-w?3n:-1n,next=Array(a.length+1).fill(0n);
  for(let j=0;j<a.length;j++){next[j]+=a[j];next[j+1]+=c*a[j]}
  a=next;
 }
 return a;
}
const transform=n=>{
 let a=Array.from({length:n+1},()=>Array(n+1).fill(0n));
 for(let w=0;w<=n;w++){let c=poly(n,w);for(let j=0;j<=n;j++)a[j][w]=c[j]}
 return a;
};
const A=transform(3),B=transform(11),H=Array.from({length:48},()=>Array(N).fill(0n));
for(let t=0;t<3;t++)for(let b=0;b<12;b++)for(let a=0;a<4;a++)H[12*a+b][12*t+b]=BigInt(P[t][a]);
const T=Array.from({length:48},()=>Array(N).fill(0n));
const SH=Array.from({length:48},()=>Array(N).fill(0n));
for(let a=0;a<4;a++)for(let b=0;b<12;b++)
for(let i=0;i<4;i++)for(let j=0;j<12;j++){
 let dest=12*a+b,src=12*i+j,k=A[a][i]*B[b][j],sig=(i+j)%2?-1n:1n;
 for(let v=0;v<N;v++){T[dest][v]+=k*H[src][v];SH[dest][v]+=sig*k*H[src][v]}
}
const E=[H[0].slice(),Array.from({length:N},(_,v)=>H.reduce((s,row)=>s+row[v],0n))],rhs=[1n,S];
for(let a=0;a<4;a++)for(let b=0;b<12;b++)if(a+b>0&&a+b<=4){
 let q=12*a+b;E.push(T[q].map((v,i)=>v-S*H[q][i]));rhs.push(0n)
}
const G=[];
for(let q=0;q<48;q++)G.push(T[q].map((v,i)=>S*H[q][i]-v));
for(let q=0;q<48;q++)G.push(T[q].map(v=>-v));
for(let q=0;q<48;q++)G.push(SH[q].map(v=>-v));
chk(E.length===15&&G.length===144,"bad matrix shape");
chk(Object.values(L).every(z=>z>0)&&Object.values(R).every(z=>z>0),"sign error");
let norm=0n;for(let [i,z] of Object.entries(U))norm+=BigInt(z)*rhs[Number(i)];
chk(norm===-22528n,"normalization mismatch");
for(let v=0;v<N;v++){
 let col=0n;
 for(let [i,z] of Object.entries(L))col+=BigInt(z)*G[Number(i)][v];
 for(let [i,z] of Object.entries(U))col+=BigInt(z)*E[Number(i)][v];
 chk(col===BigInt(R[v]||0),"certificate mismatch at column "+v);
}
if(typeof console!=="undefined")console.log("EXACT BIGINT PASS: 16 physical cosets, 36 identities, contradiction -22528");
