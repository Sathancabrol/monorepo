// Pure function checks extracted from the same source as the UI, with minimal DOM-independent harness.
const assert=require('node:assert/strict'),fs=require('node:fs');
const src=fs.readFileSync(require('node:path').join(__dirname,'../assets/workbench-v3.js'),'utf8');
const block=src.slice(src.indexOf('function metrics(id){'),src.indexOf('\nfunction card(m){'));
assert.ok(block.startsWith('function metrics(id){'),'metrics block missing');
const entryState={vals:[]};
const evaluate=new Function('moduleById','entry','nf',block+';return metrics;')({sdp:{calc:['multiply','Quantité','Prix',100,48]},planning:{calc:['difference','Prévu','Écoulé',90,26]},rdc:{calc:['ratio','Cible','Réalisé',100,42]}},()=>entryState,n=>Number(n).toLocaleString('fr-FR',{maximumFractionDigits:2}));
const cases=[
 ['sdp',[],4800,true],['planning',[],64,true],['rdc',[],42,true],
 ['sdp',['',48],null,false],['sdp',['abc',48],null,false],['sdp',[-1,48],null,false],
 ['sdp',[0,48],0,true],['rdc',[0,42],null,false],['rdc',[100,0],0,true],
 ['planning',[1,2],-1,true],['sdp',[1e309,2],null,false],
 ['sdp',[' 2.5 ','4'],10,true],['sdp',['1e308','1e308'],null,false]
];
for(const [id,vals,expected,valid] of cases){entryState.vals=vals;const actual=evaluate(id);assert.equal(actual.valid,valid,JSON.stringify({id,vals,actual}));assert.equal(actual.res,expected,JSON.stringify({id,vals,actual}));}
console.log(cases.length+' calculs workbench validés');