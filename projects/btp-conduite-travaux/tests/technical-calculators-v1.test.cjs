"use strict";
const assert=require("node:assert/strict");
const {hydraulic,basin,electrical,lighting}=require("../assets/technical-calculators-v1.js");
let n=0;function check(name,fn){fn();n++;console.log("PASS",name);}
const approx=(a,b,tol=1e-8)=>assert.ok(Math.abs(a-b)<tol, a+" != "+b);
check("Manning full circular pipe",()=>{const r=hydraulic({k:100,diameterMm:300,slopePct:1,fillPct:100});approx(r.qFullLs,r.qLs,1e-7);approx(r.areaM2,Math.PI*.3*.3/4);});
check("Manning half-filled area",()=>{const r=hydraulic({k:100,diameterMm:300,slopePct:1,fillPct:50});approx(r.areaM2,Math.PI*.3*.3/8);approx(r.velocityMs,hydraulic({k:100,diameterMm:300,slopePct:1,fillPct:100}).velocityMs);});
check("Hydraulic rejects empty",()=>assert.throws(()=>hydraulic({k:"",diameterMm:300,slopePct:1,fillPct:50})));
check("Hydraulic rejects fill >100",()=>assert.throws(()=>hydraulic({k:100,diameterMm:300,slopePct:1,fillPct:120})));
check("Basin gross runoff",()=>{const r=basin({areaHa:2.5,runoff:.5,rainMm:45,outflowLsHa:2});approx(r.grossRunoffM3,562.5);approx(r.outflowLs,5);assert.equal(r.orificeMm,null);});
check("Basin rejects negative outflow",()=>assert.throws(()=>basin({areaHa:1,runoff:.5,rainMm:30,outflowLsHa:-1})));
check("Electric mono 1800W 250m 6mm2",()=>{const r=electrical({phase:"mono",metal:"cuivre",powerW:1800,lengthM:250,sectionMm2:6});approx(r.currentA,1800/230);approx(r.dropV,2*.0225*250*(1800/230)/6);});
check("Electric tri current",()=>{const r=electrical({phase:"tri",metal:"alu",powerW:4000,lengthM:100,sectionMm2:10});approx(r.currentA,4000/(Math.sqrt(3)*400));});
check("Electric rejects zero section",()=>assert.throws(()=>electrical({phase:"mono",metal:"cuivre",powerW:1000,lengthM:10,sectionMm2:0})));
check("Lighting does not invent lux",()=>{const r=lighting({heightM:6,spacingM:25});assert.equal(r.estimatedLux,null);approx(r.ratio,25/6);});
console.log(n+" tests passed");
