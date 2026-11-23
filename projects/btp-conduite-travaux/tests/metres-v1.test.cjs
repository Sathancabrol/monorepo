'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),m=require('../assets/metres-v1.cjs');
test('terrassement 100 m² x 0,30 m',()=>assert.equal(m.earthwork({area:100,depth:.3}),30));
test('tranchée trapézoïdale',()=>assert.deepEqual(m.trench({bottomWidth:2,depth:1,slope:1,length:20}),{topWidth:4,section:3,volume:60}));
test('chaussée 3 couches',()=>assert.deepEqual(m.pavement({area:100,layers:[{name:'GNT',thickness:.25},{name:'GB',thickness:.12},{name:'BBSG',thickness:.06}]}).map(x=>x.volume),[25,12,6]));
test('durée de production et aléas',()=>assert.deepEqual(m.duration({quantity:100,rate:20,setupDays:1,weatherDays:2}),{productionDays:5,totalDays:8}));
test('valeurs invalides',()=>{for(const x of [NaN,Infinity,-1,0,'100'])assert.throws(()=>m.earthwork({area:x,depth:.3}));assert.throws(()=>m.trench({bottomWidth:2,depth:1,slope:-1,length:20}));assert.throws(()=>m.pavement({area:100,layers:[]}));assert.throws(()=>m.duration({quantity:100,rate:0}));});
