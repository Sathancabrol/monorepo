/* Run from projects/btp-conduite-travaux: node tests/project-core-v1.test.js
 * No network, no npm packages. Explicit calendar-day schedule; not a legal planning tool. */
"use strict";
const assert=require("node:assert/strict");
const core=require("../assets/project-core-v1.js");
let checks=0;
function ok(condition,message){assert.ok(condition,message);checks++}
function equal(a,b,message){assert.equal(a,b,message);checks++}
function rejects(fn,message){assert.throws(fn,undefined,message);checks++}
const p=core.sample();
const result=core.schedule(p);
equal(result.tasks.length,6,"six pedagogical tasks");
equal(result.summary.plannedCost,1830,"100 m2 sample planned direct cost");
equal(result.summary.calendarDays,6,"sequential schedule");
equal(result.summary.scheduleBasis,"calendar-days","basis explicitly declared");
const task=p.tasks[0];
rejects(()=>core.task({...task,quantity:""}),"empty quantity");
rejects(()=>core.task({...task,quantity:null}),"null quantity");
rejects(()=>core.task({...task,quantity:true}),"boolean quantity");
rejects(()=>core.task({...task,crew:1.5}),"fractional people");
rejects(()=>core.task({...task,daysOverride:2.3}),"fractional days");
const zero=core.schedule({...p,tasks:[{...task,quantity:0,depends:[]}]});
equal(zero.tasks[0].durationDays,0,"zero quantity does not automatically consume a day");
equal(zero.summary.calendarDays,0,"zero quantity produces no calendar span");
equal(zero.tasks[0].endInclusive,null,"zero-duration task has no inclusive end date");
ok(zero.warnings.some(x=>x.includes("quantité nulle")),"zero quantity is flagged");
const forced=core.schedule({...p,tasks:[{...task,quantity:0,daysOverride:2,depends:[]}]});
equal(forced.tasks[0].durationDays,2,"explicit mobilization is retained");
const dep=core.schedule({...p,tasks:[{...task,quantity:0,depends:[]},{...p.tasks[1],depends:[task.id]}]});
equal(dep.tasks[1].start,p.startDate,"successor of zero-duration task may start same day");
rejects(()=>core.project({...p,tasks:[{...task,depends:["missing"]}]}),"unknown predecessor");
rejects(()=>core.project({...p,tasks:[{...task,depends:["t02"]},{...p.tasks[1],depends:[task.id]}]}),"cycle");
rejects(()=>core.project({...p,tasks:[task,{...task}]}),"duplicate task id");
console.log("BTP Project Core v1: "+checks+" checks passed");
