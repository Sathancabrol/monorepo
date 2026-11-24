/* BTP Studio - Project Core v1
 * Pure business calculations: no browser API, no network, no external dependencies.
 * All simulated prices/rates require human validation before contractual use. */
(function(root,factory){
  const api=factory();
  if(typeof module==="object"&&module.exports)module.exports=api;
  root.BTPProjectCore=api;
})(typeof globalThis!=="undefined"?globalThis:this,function(){
"use strict";
const SCHEMA="btp-project-v1";
const MAX_TASKS=300;
function invariant(ok,msg){if(!ok)throw new Error(msg)}
function finite(v,name,lo,hi){invariant(v!==null&&v!==undefined&&!(typeof v==="string"&&v.trim()===""),name+" : valeur obligatoire");invariant(typeof v==="number"||typeof v==="string",name+" : type numérique invalide");const x=Number(v);invariant((typeof v==="number"||typeof v==="string")&&Number.isFinite(x)&&x>=lo&&x<=hi,name+" : valeur hors limites");return x}
function str(v,name,max=180){const t=String(v==null?"":v).trim();invariant(t.length>0&&t.length<=max,name+" : texte manquant ou trop long");return t}
function iso(s){
 invariant(typeof s==="string"&&/^\d{4}-\d{2}-\d{2}$/.test(s),"Date invalide : AAAA-MM-JJ attendu");
 const ms=Date.parse(s+"T00:00:00Z");invariant(Number.isFinite(ms)&&new Date(ms).toISOString().slice(0,10)===s,"Date calendaire invalide");return ms
}
function addDays(date,number){return new Date(iso(date)+number*86400000).toISOString().slice(0,10)}
function chooseDay(a,b){return iso(a)>=iso(b)?a:b}
function task(raw){
 invariant(raw&&typeof raw==="object","Tâche absente");
 const t={
  id:str(raw.id,"Identifiant",90),name:str(raw.name,"Intitulé",180),
  unit:str(raw.unit||"u","Unité",24),
  quantity:finite(raw.quantity,"Quantité",0,1e8),
  doneQuantity:finite(raw.doneQuantity==null?0:raw.doneQuantity,"Quantité réalisée",0,1e8),
  unitCost:finite(raw.unitCost==null?0:raw.unitCost,"Déboursé unitaire indicatif",0,1e8),
  dailyRate:finite(raw.dailyRate==null?1:raw.dailyRate,"Rendement",.0001,1e8),
  crew:finite(raw.crew==null?1:raw.crew,"Équipe",1,200),
  depends:Array.isArray(raw.depends)?[...new Set(raw.depends.map(v=>str(v,"Prédécesseur",90)))]:[],
  group:String(raw.group||"Exécution").slice(0,90),
  notes:String(raw.notes||"").slice(0,2000),
  verification:String(raw.verification||"À vérifier").slice(0,120),
  costActual:raw.costActual==null?null:finite(raw.costActual,"Coût réel constaté",0,1e10)
 };
 if(raw.daysOverride!=null&&raw.daysOverride!=="")t.daysOverride=finite(raw.daysOverride,"Durée imposée",1,10000);
 invariant(Number.isInteger(t.crew),"Équipe : nombre entier requis");
 if(t.daysOverride!=null)invariant(Number.isInteger(t.daysOverride),"Durée imposée : nombre entier requis");
 if(raw.startConstraint!=null&&raw.startConstraint!==""){iso(raw.startConstraint);t.startConstraint=raw.startConstraint}
 invariant(!t.depends.includes(t.id),"Dépendance circulaire directe");
 return t
}
function project(raw){
 invariant(raw&&typeof raw==="object","Projet invalide");
 invariant(raw.schema==null||raw.schema===SCHEMA,"Version de projet non prise en charge");
 const p={
  schema:SCHEMA,
  id:str(raw.id,"Identifiant projet",90),
  title:str(raw.title,"Nom du chantier",180),
  client:String(raw.client||"").slice(0,180),
  city:String(raw.city||"").slice(0,180),
  startDate:String(raw.startDate||"2026-11-23"),
  dataType:raw.dataType==="demonstration"?"demonstration":raw.dataType==="imported"?"imported":"user",
  notes:String(raw.notes||"").slice(0,3000),
  tasks:[]
 };
 iso(p.startDate);
 invariant(Array.isArray(raw.tasks),"Liste de tâches absente");
 invariant(raw.tasks.length<=MAX_TASKS,"Limite de tâches dépassée");
 const seen=new Set();
 for(const r of raw.tasks){const t=task(r);invariant(!seen.has(t.id),"ID de tâche dupliqué : "+t.id);seen.add(t.id);p.tasks.push(t)}
 for(const t of p.tasks)for(const dep of t.depends)invariant(seen.has(dep),"Prédécesseur introuvable pour "+t.id+" : "+dep);
 // Require an acyclic task graph.
 const status=new Map(),byId=new Map(p.tasks.map(t=>[t.id,t]));
 function visit(id){if(status.get(id)===1)throw new Error("Cycle détecté : "+id);if(status.get(id)===2)return;status.set(id,1);for(const d of byId.get(id).depends)visit(d);status.set(id,2)}
 for(const t of p.tasks)visit(t.id);
 return p
}
function schedule(input){
 const p=project(input),byId=new Map(p.tasks.map(t=>[t.id,t])),memo=new Map();
 function compute(id){
  if(memo.has(id))return memo.get(id);
  // Zero-quantity tasks do not silently consume a full production day unless explicitly overridden.
  const t=byId.get(id),duration=t.daysOverride!=null?t.daysOverride:(t.quantity===0?0:Math.max(1,Math.ceil(t.quantity/t.dailyRate)));
  let start=t.startConstraint?chooseDay(p.startDate,t.startConstraint):p.startDate;
  for(const d of t.depends)start=chooseDay(start,compute(d).endExclusive);
  const endExclusive=addDays(start,duration);
  const row={...t,start,endExclusive,endInclusive:duration===0?null:addDays(endExclusive,-1),durationDays:duration,plannedCost:Math.round(t.quantity*t.unitCost*100)/100,realizedValue:Math.round(t.doneQuantity*t.unitCost*100)/100,estimatedCrewHours:duration*8*t.crew};
  memo.set(id,row);return row
 }
 const rows=p.tasks.map(t=>compute(t.id));
 const cost=rows.reduce((n,t)=>n+t.plannedCost,0),value=rows.reduce((n,t)=>n+t.realizedValue,0);
 const actualCost=rows.filter(t=>t.costActual!=null).reduce((n,t)=>n+t.costActual,0);
 const actualCostCount=rows.filter(t=>t.costActual!=null).length;
 const end=rows.reduce((max,t)=>chooseDay(max,t.endExclusive),p.startDate);
 const warnings=[];
 if(rows.some(t=>t.doneQuantity>t.quantity))warnings.push("Quantité réalisée supérieure à la quantité prévue : dépassement ou mise à jour du métré à vérifier");
 if(rows.some(t=>t.quantity===0))warnings.push("Tâche à quantité nulle : durée de production égale à zéro, vérifier si une mobilisation reste nécessaire");
 if(rows.some(t=>t.unitCost===0))warnings.push("Certains déboursés unitaires sont nuls ou non renseignés");
 if(rows.some(t=>t.verification!=="Validé"))warnings.push("Les contrôles et validations restent à effectuer");
 return {project:p,tasks:rows,summary:{
  plannedCost:Math.round(cost*100)/100,
  theoreticalRealizedValue:Math.round(value*100)/100,
  theoreticalBalance:Math.round((cost-value)*100)/100,
  actualCost:actualCostCount?Math.round(actualCost*100)/100:null,
  actualCostCoverage:actualCostCount+"/"+rows.length,
  valueProgressPct:cost>0?Math.round(value/cost*10000)/100:0,
  earliestDate:p.startDate,endExclusive:end,calendarDays:Math.round((iso(end)-iso(p.startDate))/86400000),
  plannedCrewHours:rows.reduce((n,t)=>n+t.estimatedCrewHours,0),
  scheduleBasis:"calendar-days", // Weekends, holidays, weather and shifts are NOT deducted.
  warningCount:warnings.length
 },warnings}
}
function sample(){
 return project({
 schema:SCHEMA,id:"demo-terrassement-100m2",title:"EXEMPLE — Terrassement 100 m²",client:"Démonstration pédagogique",city:"Lieu fictif",
 startDate:"2026-11-23",dataType:"demonstration",
 notes:"Tous les coûts et rendements sont des hypothèses. Aucun chantier réel n'est représenté.",
 tasks:[
  {id:"t01",group:"Préparation",name:"Implantation et piquetage",unit:"m²",quantity:100,doneQuantity:0,unitCost:1.8,dailyRate:350,crew:2},
  {id:"t02",group:"Exécution",name:"Décapage terre végétale (hypothèse 0,30 m)",unit:"m³",quantity:30,doneQuantity:0,unitCost:12,dailyRate:75,crew:3,depends:["t01"]},
  {id:"t03",group:"Exécution",name:"Terrassement terrain naturel",unit:"m³",quantity:30,doneQuantity:0,unitCost:18,dailyRate:65,crew:3,depends:["t02"]},
  {id:"t04",group:"Exécution",name:"Réglage du fond de forme",unit:"m²",quantity:100,doneQuantity:0,unitCost:3.5,dailyRate:250,crew:3,depends:["t03"]},
  {id:"t05",group:"Contrôles",name:"Contrôle géométrique et altimétrique",unit:"lot",quantity:1,doneQuantity:0,unitCost:100,dailyRate:1,crew:2,depends:["t04"]},
  {id:"t06",group:"Réception & DOE",name:"Rassembler rapports et preuves",unit:"dossier",quantity:1,doneQuantity:0,unitCost:300,dailyRate:1,crew:1,depends:["t05"]}
 ]})
}
function putTask(input,raw){
 const p=project(input),t=task(raw),i=p.tasks.findIndex(v=>v.id===t.id);
 if(i<0){invariant(p.tasks.length<MAX_TASKS,"Nombre maximum de tâches atteint");p.tasks.push(t)}else p.tasks[i]=t;
 return project(p)
}
function deleteTask(input,id){
 const p=project(input);invariant(!p.tasks.some(t=>t.depends.includes(id)),"Tâche utilisée comme prédécesseur, modifier les dépendances avant suppression");
 p.tasks=p.tasks.filter(t=>t.id!==id);return project(p)
}
return {SCHEMA,MAX_TASKS,project,task,schedule,sample,putTask,deleteTask,addDays};
});