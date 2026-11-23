/* BTP Studio v4 — real local registers, not fabricated delivery/weather attestations. */
(function(){
"use strict";
const KEY="btp_local_records_v4",PRJ="btp_project_active_v1";
const $=id=>document.getElementById(id);
const fmt=(v,d=2)=>Number(v).toLocaleString("fr-FR",{maximumFractionDigits:d});
const today=()=>new Date().toISOString().slice(0,10);
const safe=s=>String(s??"").slice(0,250);
const csv=x=>{let v=String(x??"");if(/^[=+\-@\t\r]/.test(v))v="'"+v;return '"'+v.replace(/"/g,'""')+'"'};
let collection={};
try{const v=JSON.parse(localStorage.getItem(KEY)||"{}");if(v&&typeof v==="object"&&!Array.isArray(v))collection=v}catch(e){}
function project(){try{return localStorage.getItem(PRJ)||"sans-dossier"}catch(e){return "sans-dossier"}}
function current(name){const p=project();const r=collection[p]||{};return Array.isArray(r[name])?r[name]:[]}
function save(name,rows){if(rows.length>5000)throw Error("Limite de 5 000 lignes par registre");const p=project();if(!collection[p])collection[p]={};collection[p][name]=rows;localStorage.setItem(KEY,JSON.stringify(collection))}
function text(id,value){const node=$(id);if(node)node.textContent=value}
function close(name){if(typeof window.closeModal==="function")window.closeModal(name);else $(name)?.classList.remove("active")}
function open(name){if(typeof window.openModal==="function")window.openModal(name);else $(name)?.classList.add("active")}
function csvFile(name,cols,rows){
 const header=cols.map(x=>x[1]),body=rows.map(r=>cols.map(x=>r[x[0]]).map(csv).join(";"));
 const result="\uFEFF"+[header.map(csv).join(";"),...body].join("\r\n");
 const url=URL.createObjectURL(new Blob([result],{type:"text/csv;charset=utf-8"})),a=document.createElement("a");
 a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),3000);
}
function renderTable(id,rows,mapper){
 const tbody=$(id);if(!tbody)return;tbody.replaceChildren();
 if(!rows.length){const tr=document.createElement("tr"),td=document.createElement("td");td.colSpan=10;td.textContent="Aucune saisie locale. Les anciennes valeurs fictives ne sont pas comptabilisées.";td.style.cssText="padding:16px;color:#b5c9c1;text-align:center";tr.appendChild(td);tbody.appendChild(tr);return}
 for(const record of rows){const tr=document.createElement("tr");for(const cell of mapper(record)){const td=document.createElement("td");td.textContent=String(cell??"");td.style.cssText="padding:8px 10px;border-bottom:1px solid #405057";tr.appendChild(td)}tbody.appendChild(tr)}
}
function renderLivraisons(){
 const rows=current("livraisons");
 renderTable("rdc-livraisons-table-body",rows,r=>[r.num,r.date,r.supplier,r.material,r.truck,fmt(r.quantity)+" t",r.temperature==null?"—":fmt(r.temperature)+" °C",r.projectLabel||"Projet actif","Saisie locale · non vérifiée"]);
 const enrobes=rows.filter(x=>/BBSG|BBME|enrob/i.test(x.material)).reduce((a,x)=>a+x.quantity,0);
 const gnt=rows.filter(x=>/GNT|grave/i.test(x.material)).reduce((a,x)=>a+x.quantity,0);
 text("kpi-livraison-enrobes",fmt(enrobes)+" t (saisie)");
 text("kpi-livraison-gnt",fmt(gnt)+" t (saisie)");
 text("kpi-livraison-beton","Non mesuré en m³");
 text("kpi-livraison-rendement","Non calculé : surface inconnue");
}
function renderIntemperies(){
 const rows=current("intemperies");
 renderTable("planning-intemperies-table-body",rows,r=>[r.date,r.type,r.measure||"Non documentée",r.tasks||"À préciser","Non déterminé","À faire valider"]);
 text("kpi-intemperies-jours",rows.length+" constat(s) locaux");
 text("kpi-intemperies-depassement","À instruire selon CCAP");
 text("kpi-intemperies-nouvelle-date","Non déterminée");
}
function initForms(){
 const f=$("form-add-intemperie");
 if(f&&!$("new-intemp-extra")){
  const div=document.createElement("div");div.id="new-intemp-extra";div.style.cssText="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:9px";
  const fields=[["new-intemp-measure","Mesure observée (unité, lieu)","Ex. 18 mm mesurés à ..."],["new-intemp-source","Source / justificatif","Ex. relevé météo daté"],["new-intemp-tasks","Travaux réellement bloqués","Ex. terrassement, secteur A"],["new-intemp-note","Observations","Éléments à faire viser"]];
  fields.forEach(([id,label,placeholder])=>{const box=document.createElement("label");box.style.cssText="font-size:11px;color:#c4d7d1";box.textContent=label;const input=document.createElement("input");input.id=id;input.className="input-field";input.type="text";input.maxLength=250;input.placeholder=placeholder;input.style.cssText="display:block;width:100%;margin-top:4px";box.appendChild(input);div.appendChild(box)});
  const submit=f.querySelector('button[type="submit"]');if(submit)submit.parentElement.before(div);else f.appendChild(div);
  const p=document.createElement("p");p.textContent="Une saisie n'ouvre aucun droit automatique à prolongation ou indemnisation. Vérification des seuils, clauses du marché et accord du maître d'œuvre obligatoires.";p.style.cssText="font-size:11px;color:#f0c08a;margin:10px 0";div.after(p);
 }
}
window.openAddLivraisonModal=function(){
 if($("new-bl-date")&&!$("new-bl-date").value)$("new-bl-date").value=new Date().toISOString().slice(0,16);
 open("modal-add-livraison");
};
window.saveNewLivraison=function(e){
 if(e&&e.preventDefault)e.preventDefault();
 const num=safe($("new-bl-num")?.value).trim(),date=$("new-bl-date")?.value||"",quantity=Number($("new-bl-qte")?.value);
 if(!num||!date||!Number.isFinite(quantity)||quantity<=0||quantity>5000){alert("Bon, date et quantité positive (0 à 5000 t) requis.");return}
 const rows=current("livraisons");
 if(rows.some(r=>r.num===num)){alert("Ce numéro de bon figure déjà dans ce dossier.");return}
 const tStr=$("new-bl-temp")?.value||"";
 const temperature=tStr===""?null:Number(tStr);
 if(temperature!==null&&(!Number.isFinite(temperature)||temperature< -50||temperature>350)){alert("Température hors plage de saisie.");return}
 try{
  rows.push({num,date,supplier:safe($("new-bl-fournisseur")?.value),material:safe($("new-bl-materiau")?.value),
   truck:safe($("new-bl-camion")?.value),quantity,temperature,projectLabel:project(),savedAt:new Date().toISOString()});
  save("livraisons",rows);renderLivraisons();close("modal-add-livraison");$("form-add-livraison")?.reset();
 }catch(err){alert("Enregistrement impossible : "+err.message)}
};
window.exportLivraisonsCSV=function(){
 const cols=[["num","N° BL"],["date","Date"],["supplier","Fournisseur"],["material","Matériau"],["truck","Camion"],["quantity","Quantité (t)"],["temperature","Température (°C)"],["projectLabel","Dossier"],["savedAt","Saisie locale horodatée"]];
 csvFile("btp-livraisons-"+project()+".csv",cols,current("livraisons"));
};
window.openAddIntemperieModal=function(){
 initForms();if($("new-intemp-date"))$("new-intemp-date").value=today();open("modal-add-intemperie");
};
window.saveNewIntemperie=function(e){
 if(e&&e.preventDefault)e.preventDefault();
 const date=$("new-intemp-date")?.value||"",type=safe($("new-intemp-type")?.value);
 if(!/^\d{4}-\d{2}-\d{2}$/.test(date)||!type){alert("Date et phénomène requis.");return}
 const rows=current("intemperies");
 if(rows.some(r=>r.date===date&&r.type===type)){alert("Constat déjà enregistré pour cette date et ce phénomène.");return}
 try{
 rows.push({date,type,measure:safe($("new-intemp-measure")?.value),source:safe($("new-intemp-source")?.value),
   tasks:safe($("new-intemp-tasks")?.value),note:safe($("new-intemp-note")?.value),projectLabel:project(),
   savedAt:new Date().toISOString(),status:"Constat local · non instruit"});
 save("intemperies",rows);renderIntemperies();close("modal-add-intemperie");$("form-add-intemperie")?.reset();
 }catch(err){alert("Enregistrement impossible : "+err.message)}
};
window.exportIntemperiesCSV=function(){
 const cols=[["date","Date"],["type","Phénomène"],["measure","Mesure"],["source","Justificatif"],["tasks","Tâches"],["note","Observations"],["projectLabel","Dossier"],["status","Statut"],["savedAt","Date saisie"]];
 csvFile("btp-intemperies-"+project()+".csv",cols,current("intemperies"));
};
function init(){
 initForms();renderLivraisons();renderIntemperies();
 window.addEventListener("storage",e=>{if(e.key===KEY||e.key===PRJ){if(e.key===KEY){try{collection=JSON.parse(e.newValue||"{}")}catch(_){}}
 renderLivraisons();renderIntemperies()}});
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();