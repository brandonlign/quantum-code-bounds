#!/usr/bin/env node
// Independent exact polynomial-product implementation; no Python or imports.
const n=14, modulus=4096, c=[1,-2,-6,-17,-95,-20,-24,1108,246];
function polyMultiply(a,b){
 const r=Array(a.length+b.length-1).fill(0n);
 for(let i=0;i<a.length;i++)for(let j=0;j<b.length;j++)r[i+j]+=a[i]*b[j];
 return r;
}
function kw(w){
 let p=[1n];
 for(let i=0;i<14-w;i++)p=polyMultiply(p,[1n,3n]);
 for(let i=0;i<w;i++)p=polyMultiply(p,[1n,-1n]);
 return p;
}
let residues=[];
for(let w=0;w<=14;w++){
 const k=kw(w);let a=BigInt(c[0]);
 for(let j=1;j<=4;j++)a+=BigInt(c[j])*k[j];
 for(let j=0;j<=3;j++)a+=BigInt(c[5+j])*BigInt(w%2?-1:1)*k[j];
 if(w>=1&&w<=4)a-=2048n*BigInt(c[w]);
 let rem=((a%4096n)+4096n)%4096n;
 if(rem!==BigInt(w===3||w===4?2048:0))throw Error('bad coefficient '+w+' '+rem);
 residues.push(Number(rem));
}
for(let j=0;j<=3;j++){
 if(((-2048n*BigInt(c[5+j]))%4096n)!==0n)throw Error('bad shadow '+j);
}
console.log('INDEPENDENT JS BIGINT PARITY CERTIFICATE PASS; 15/15 physical-weight coefficients');
console.log('residues modulo 4096:',JSON.stringify(residues));
console.log('H3+H4 odd, hence H4=1 or3 when H3=0 and H4<=3.');
