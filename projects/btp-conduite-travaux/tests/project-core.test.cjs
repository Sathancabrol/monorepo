"use strict";
const test=require("node:test");
const assert=require("node:assert/strict");
const core=require("../assets/project-core-v1.js");

test("exemple explicite de chantier fictif",()=>{
 const p=core.sample();
 assert.equal(p.schema,"btp-project-v1");
 assert.equal(p.dataType,"demonstration");
 assert.equal(p.tasks.length,6);
 assert.equal(p.tasks.find(t=>t.id==="t03").quantity,100*0.30);
});

test("plan, déboursé et heures équipe déterministes",()=>{
 const s=core.schedule(core.sample());
 assert.equal(s.summary.plannedCost,1830);
 assert.equal(s.summary.calendarDays,6);
 assert.equal(s.summary.plannedCrewHours,112);
 assert.equal(s.summary.theoreticalRealizedValue,0);
 assert.equal(s.summary.actualCost,null);
});

test("prédecesseurs imposent l'ordre de la planification",()=>{
 const s=core.schedule(core.sample());
 for(const t of s.tasks)for(const d of t.depends){
   assert.ok(s.tasks.find(x=>x.id===d).endExclusive<=t.start);
 }
});

test("réalisé = quantité réelle valorisée au PU estimé, jamais une dépense",()=>{
 const p=core.sample(),t=p.tasks.find(x=>x.id==="t03");
 t.doneQuantity=15;t.costActual=1000;
 const s=core.schedule(p);
 assert.equal(s.tasks.find(x=>x.id==="t03").realizedValue,270);
 assert.equal(s.summary.actualCost,1000);
 assert.equal(s.summary.actualCostCoverage,"1/6");
 assert.notEqual(s.summary.theoreticalRealizedValue,s.summary.actualCost);
});

test("volume et coût technique simplifié",()=>{
 const p=core.sample();
 const terr=p.tasks.find(t=>t.id==="t03");
 terr.quantity=100*.30;terr.unitCost=18;
 const s=core.schedule(p);
 assert.equal(s.tasks.find(t=>t.id==="t03").plannedCost,540);
});

test("date invalide refusée",()=>{
 assert.throws(()=>core.project({...core.sample(),startDate:"2026-02-30"}),/Date/);
});

test("prédécesseur absent refusé",()=>{
 assert.throws(()=>core.putTask(core.sample(),{id:"new",name:"Tâche",quantity:1,unit:"u",depends:["absent"]}),/Prédécesseur/);
});

test("cycle de dépendance refusé",()=>{
 const p=core.sample();p.tasks[0].depends=["t06"];
 assert.throws(()=>core.project(p),/Cycle/);
});

test("doublon ID refusé",()=>{
 const p=core.sample();p.tasks.push({...p.tasks[0]});
 assert.throws(()=>core.project(p),/dupliqué/);
});

test("règles de validité du rendement et des coûts",()=>{
 const t={id:"id",name:"activité",quantity:1,unit:"u",dailyRate:0};
 assert.throws(()=>core.task(t),/Rendement/);
 assert.throws(()=>core.task({...t,dailyRate:1,unitCost:-1}),/Déboursé/);
});

test("suppression d'une tâche avec dépendants empêchée",()=>{
 assert.throws(()=>core.deleteTask(core.sample(),"t01"),/prédécesseur/);
});

test("édition renvoie une nouvelle copie valide",()=>{
 const p=core.sample(),after=core.putTask(p,{...p.tasks[0],name:"Implantation revue"});
 assert.equal(p.tasks[0].name,"Implantation et piquetage");
 assert.equal(after.tasks[0].name,"Implantation revue");
});

test("dépassement de quantités signalé sans effacer la mesure",()=>{
 const p=core.sample();p.tasks[0].doneQuantity=125;
 const s=core.schedule(p);
 assert.equal(s.tasks[0].doneQuantity,125);
 assert.ok(s.warnings.some(w=>w.includes("supérieure")));
});

test("date de début contrainte peut décaler le planning",()=>{
 const p=core.sample();p.tasks[0].startConstraint="2027-01-20";
 const s=core.schedule(p);
 assert.equal(s.tasks[0].start,"2027-01-20");
 assert.equal(s.tasks[1].start,"2027-01-21");
});

test("calculs sans mutation de l'objet source",()=>{
 const p=core.sample(),before=JSON.stringify(p);
 core.schedule(p);
 assert.equal(JSON.stringify(p),before);
});

test("limite de 300 tâches et version de schéma",()=>{
 assert.throws(()=>core.project({...core.sample(),schema:"btp-project-v9"}),/Version/);
 const p=core.sample();p.tasks=Array.from({length:301},(_,i)=>({id:"x"+i,name:"test",quantity:1,unit:"u"}));
 assert.throws(()=>core.project(p),/Limite/);
});
