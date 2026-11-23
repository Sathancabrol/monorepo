/* BTP legacy UI repair — optional local-first handlers for missing actions.
   This module never claims contractual, safety or engineering certification. */
(function(root){
"use strict";
const doc=root.document;
const key="btp-studio-v2-registers-v1";
function read(){try{const x=JSON.parse(root.localStorage.getItem(key)||"{}");return {deliveries:Array.isArray(x.deliveries)?x.deliveries:[],weather:Array.isArray(x.weather)?x.weather:[]}}catch(_){return {deliveries:[],weather:[]}}}
function write(x){try{root.localStorage.setItem(key,JSON.stringify(x));return true}catch(_){root.alert("Enregistrement impossible : stockage local indisponible.");return false}}
function el(id){return doc.getElementById(id)}
function value(id){return (el(id)?.value||"").trim()}
function set(id,v){if(el(id))el(id).textContent=v}
function csv(name,header,rows){const quote=x=>{let v=String(x??"");if(/^[\s\uFEFF]*[=+@\-]/.test(v))v="\u0027"+v;return '"'+v.replace(/"/g,'""')+'"'};const body=[header,...rows].map(row=>row.map(quote).join(";")).join("\r\n");const url=root.URL.createObjectURL(new Blob(["\uFEFF"+body],{type:"text/csv;charset=utf-8"}));const a=doc.createElement("a");a.href=url;a.download=name;doc.body.appendChild(a);a.click();a.remove();root.URL.revokeObjectURL(url)}
function open(id){if(typeof root.openModal==="function")root.openModal(id);else el(id)?.classList.add("active")}
function close(id){if(typeof root.closeModal==="function")root.closeModal(id);else el(id)?.classList.remove("active")}
function validDate(x){if(!/^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2})?$/.test(x))return false;const [y,m,day]=x.slice(0,10).split("-").map(Number);const dt=new Date(Date.UTC(y,m-1,day));if(dt.getUTCFullYear()!==y||dt.getUTCMonth()!==m-1||dt.getUTCDate()!==day)return false;if(x.length>10){const h=Number(x.slice(11,13)),min=Number(x.slice(14,16));if(h>23||min>59)return false}return true}
function td(text){const c=doc.createElement("td");c.textContent=String(text??"");c.style.padding="6px 10px";return c}
function draw(id,records,fields){const target=el(id);if(!target)return;target.replaceChildren();records.forEach(r=>{const tr=doc.createElement("tr");fields.forEach(f=>tr.appendChild(td(r[f])));target.appendChild(tr)})}
function render(){const x=read();draw("rdc-livraisons-table-body",x.deliveries,["number","date","supplier","material","truck","quantity","temperature","site","status"]);draw("planning-intemperies-table-body",x.weather,["date","type","measurement","blocked","eligibility","validation"]);
const sum=needle=>x.deliveries.filter(d=>needle.test(d.material)).reduce((a,d)=>a+d.quantity,0);
set("kpi-livraison-enrobes",sum(/BBSG|BBME|enrob/i).toFixed(2)+" t");set("kpi-livraison-gnt",sum(/GNT/i).toFixed(2)+" t");
set("kpi-livraison-beton","Non renseigné");set("kpi-livraison-rendement","Non calculable sans surface réelle");
set("kpi-intemperies-jours",x.weather.length+" constat(s)");set("kpi-intemperies-depassement","À justifier selon CCAP");set("kpi-intemperies-nouvelle-date","À valider contractuellement");
}
root.openAddLivraisonModal=function(){open("modal-add-livraison")};
root.openAddIntemperieModal=function(){open("modal-add-intemperie")};
root.saveNewLivraison=function(e){e?.preventDefault();const rawQty=value("new-bl-qte"),q=rawQty===""?NaN:Number(rawQty);const date=value("new-bl-date"),number=value("new-bl-num");if(!number||!validDate(date)||!Number.isFinite(q)||q<=0||q>1000000){root.alert("Bon invalide : numéro, date et quantité strictement positive requis.");return}
const x=read();if(x.deliveries.some(d=>d.number===number)){root.alert("Numéro de bon déjà enregistré.");return}
x.deliveries.push({number,date,supplier:value("new-bl-fournisseur"),material:value("new-bl-materiau"),truck:value("new-bl-camion"),quantity:q,temperature:value("new-bl-temp"),site:"Non renseigné",status:"Saisie locale non vérifiée"});if(write(x)){close("modal-add-livraison");render()}};
root.saveNewIntemperie=function(e){e?.preventDefault();const date=value("new-intemp-date"),type=value("new-intemp-type");if(!validDate(date)||!type){root.alert("Date et phénomène requis.");return}const x=read();if(x.weather.some(d=>d.date===date&&d.type===type)){root.alert("Constat identique déjà saisi.");return}x.weather.push({date,type,measurement:"Non renseignée",blocked:"À documenter",eligibility:"Non déterminée",validation:"Non validé"});if(write(x)){close("modal-add-intemperie");render()}};
root.exportLivraisonsCSV=function(){const x=read();csv("btp-livraisons-local.csv",["Numéro","Date","Fournisseur","Matériau","Camion","Quantité (t)","Température (°C)","Chantier","Statut"],x.deliveries.map(d=>[d.number,d.date,d.supplier,d.material,d.truck,d.quantity,d.temperature,d.site,d.status]))};
root.exportIntemperiesCSV=function(){const x=read();csv("btp-intemperies-local.csv",["Date","Phénomène","Mesure","Travaux bloqués","Éligibilité","Validation"],x.weather.map(d=>[d.date,d.type,d.measurement,d.blocked,d.eligibility,d.validation]))};
if(doc.readyState==="loading")doc.addEventListener("DOMContentLoaded",render);else render();
root.BTPRegisterRepair={read,render};
})(window);
