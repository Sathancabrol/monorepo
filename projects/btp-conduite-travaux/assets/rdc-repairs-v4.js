/* BTP Studio v4 — reliable local RDC reports and weekly crew timesheets.
 * Never synchronizes payroll or client data. Demo labels remain separate. */
(function(){
"use strict";
const PROJECT="btp_project_active_v1",PKEY="btp_rdc_records_v4",TKEY="btp_timesheets_v4";
const $=id=>document.getElementById(id);
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const csv=s=>{let v=String(s??"");if(/^[=+\-@\t\r]/.test(v))v="'"+v;return '"'+v.replace(/"/g,'""')+'"'};
const format=n=>Number(n).toLocaleString("fr-FR",{maximumFractionDigits:2});
const today=()=>new Date().toISOString().slice(0,10);
const id=()=>Date.now().toString(36)+"-"+Math.random().toString(36).slice(2,9);
function project(){try{return localStorage.getItem(PROJECT)||"sans-dossier"}catch(e){return "sans-dossier"}}
function read(key){try{const data=JSON.parse(localStorage.getItem(key)||"{}");return data&&typeof data==="object"&&!Array.isArray(data)?data:{}}catch(e){return {}}}
function collection(key){const items=read(key)[project()];return Array.isArray(items)?items:[]}
function put(key,list){if(list.length>3000)throw Error("Limite de stockage atteinte");const data=read(key);data[project()]=list;localStorage.setItem(key,JSON.stringify(data))}
function projectTitle(){
 try{const p=JSON.parse(localStorage.getItem("btp_project_workspace_v1")||"{}"),id=project();return p.projects?.find(v=>v.id===id)?.title||id}catch(e){return project()}
}
function dl(name,body,kind){
 const u=URL.createObjectURL(new Blob([body],{type:kind})),a=document.createElement("a");a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),3000)
}
function message(text){const el=$("btp-rdc-status");if(el)el.textContent=text}
function formRDC(){
 const date=$("rdc-date")?.value||"",chief=($("rdc-chief")?.value||"").trim().slice(0,150),
  work=($("rdc-desc")?.value||"").trim().slice(0,3000),
  hMO=Number($("rdc-heures-mo")?.value),hEng=Number($("rdc-heures-engins")?.value);
 if(!/^\d{4}-\d{2}-\d{2}$/.test(date)||!work)throw Error("La date et la description des travaux sont obligatoires.");
 if(!Number.isFinite(hMO)||!Number.isFinite(hEng)||hMO<0||hEng<0||hMO>10000||hEng>10000)throw Error("Heures invalides");
 return {date,chief:chief||"Non renseigné",work,hMO,hEng,project:project(),projectTitle:projectTitle()};
}
function renderRDC(){
 const root=$("rdc-entries-list");if(!root)return;
 const items=collection(PKEY).slice().sort((a,b)=>b.createdAt.localeCompare(a.createdAt));
 root.innerHTML='<div style="border:1px solid #476861;border-radius:10px;background:#182d30;padding:12px;margin:14px 0"><div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:9px"><div><strong style="color:#bce985">Rapports réellement enregistrés</strong><p style="font-size:11px;color:#b7cdc2">Enregistrements locaux du dossier : '+esc(projectTitle())+'. Pas de transmission ni de validation automatique.</p></div><button class="btn btn-secondary" id="btp-rdc-all-export">Exporter les rapports JSON</button></div>'+
 (items.length?'<div style="max-height:300px;overflow:auto">'+items.slice(0,40).map(r=>'<article style="border-top:1px solid #41645f;padding:9px 0"><div style="display:flex;justify-content:space-between;flex-wrap:wrap"><strong>'+esc(r.date)+' · '+esc(r.chief)+'</strong><button type="button" class="btn btn-secondary" data-rdc-remove="'+esc(r.id)+'">Retirer</button></div><p style="font-size:11px;margin:5px 0;color:#d9e7db">'+esc(r.work)+'</p><small style="color:#9fbab0">'+format(r.hMO)+' h équipe · '+format(r.hEng)+' h engins — saisie utilisateur</small></article>').join("")+'</div>':'<p style="font-size:11px;color:#adc4b9">Aucun rapport enregistré pour ce dossier.</p>')+
 '<p id="btp-rdc-status" role="status" style="font-size:11px;color:#c1e59e"></p></div>';
 $("btp-rdc-all-export").onclick=()=>dl("btp-rdc-"+project()+".json",JSON.stringify({schema:"btp-rdc-v4",project:project(),reports:collection(PKEY)},null,2),"application/json");
 root.querySelectorAll("[data-rdc-remove]").forEach(b=>b.onclick=()=>{
  if(!confirm("Supprimer ce rapport du navigateur ?"))return;
  try{put(PKEY,collection(PKEY).filter(r=>r.id!==b.dataset.rdcRemove));renderRDC()}catch(e){message("Erreur : "+e.message)}
 });
}
window.saveRdcEntry=function(){
 try{
  const record={id:id(),...formRDC(),createdAt:new Date().toISOString(),provenance:"saisie locale non vérifiée"};
  const entries=collection(PKEY);entries.push(record);put(PKEY,entries);renderRDC();message("Rapport enregistré localement. Pas de synchronisation paie/comptabilité ni de validation contractuelle.");
 }catch(e){alert("Rapport non enregistré : "+e.message)}
};
window.exportCurrentRDCV4=function(){
 let data;
 try{data=formRDC()}catch(e){alert(e.message);return}
 const win=window.open("","_blank");
 if(!win){alert("Fenêtre d'impression bloquée.");return}
 const html='<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>RDC — brouillon</title><style>body{font:14px/1.6 system-ui;color:#172322;padding:40px;max-width:800px;margin:auto}h1{color:#193b35}strong{color:#2b5046}.warn{padding:12px;background:#fef1d6;border:2px solid #bb8752}pre{white-space:pre-wrap;font:inherit}</style></head><body>'+
 '<div class="warn"><strong>BROUILLON · Saisie locale non vérifiée</strong> — Aucun visa, signature ni conformité automatique.</div>'+
 '<h1>Rapport journalier de chantier</h1><p><strong>Chantier :</strong> '+esc(data.projectTitle)+'</p><p><strong>Date :</strong> '+esc(data.date)+'</p>'+
 '<p><strong>Responsable :</strong> '+esc(data.chief)+'</p><p><strong>Heures main d’œuvre :</strong> '+format(data.hMO)+' h</p>'+
 '<p><strong>Heures engins :</strong> '+format(data.hEng)+' h</p><h2>Travaux exécutés</h2><pre>'+esc(data.work)+'</pre>'+
 '<p>Observations / anomalies : _____________________________________</p><p>Visa responsable : _____________________</p>'+
 '<p style="font-size:11px">Utiliser « Imprimer » puis « Enregistrer en PDF » dans le navigateur si souhaité. Cette page n’est pas un PDF signé.</p></body></html>';
 win.document.open();win.document.write(html);win.document.close();win.focus();win.print();
};
const hours=["lun","mar","mer","jeu","ven"];
function pointageForm(){
 const root=$("rdc-pointage-view");if(!root)return;
 root.innerHTML='<div class="card" style="padding:15px"><div style="color:#bce985;font-size:10px;text-transform:uppercase;font-weight:850;letter-spacing:.12em">Pointage utilisateur · saisies locales</div>'+
 '<h3>Feuille hebdomadaire nominative</h3><p style="font-size:11px;color:#bdcfc8">Créer des lignes puis enregistrer : aucune communication vers la paie, RH ou les organismes sociaux. Les six employés fictifs ne sont pas repris.</p>'+
 '<form id="btp-pointage-form" style="display:flex;gap:8px;flex-wrap:wrap;margin:12px 0">'+
 '<label>Semaine du <input id="p4-date" type="date" required></label><input id="p4-name" required maxlength="120" placeholder="Nom / matricule" aria-label="Nom ou matricule">'+
 '<input id="p4-role" maxlength="120" placeholder="Qualification" aria-label="Qualification">'+
 '<input id="p4-team" maxlength="100" placeholder="Équipe" aria-label="Équipe">'+
 '<label>Coût horaire € <input id="p4-rate" type="number" min="0" max="10000" step="any" value="0"></label>'+
 hours.map(d=>'<label>'+d.toUpperCase()+' <input id="p4-'+d+'" type="number" min="0" max="24" step=".25" value="0" style="width:65px"></label>').join("")+
 '<button class="btn btn-primary" type="submit">Enregistrer heures</button><button type="button" class="btn btn-secondary" id="p4-export">Exporter CSV</button></form>'+
 '<p id="p4-status" role="status" style="font-size:11px;color:#bce985"></p>'+
 '<div style="overflow:auto"><table style="min-width:800px;width:100%;font-size:11px"><thead><tr><th>Semaine</th><th>Nom</th><th>Qualification</th><th>Équipe</th><th>Heures</th><th>Coût théorique</th><th>Action</th></tr></thead><tbody id="p4-body"></tbody></table></div>'+
 '</div>';
 $("p4-date").value=today();$("btp-pointage-form").addEventListener("submit",savePointage);
 $("p4-export").onclick=()=>window.exportPointageCSV();renderPointage();
}
function savePointage(e){
 if(e)e.preventDefault();const date=$("p4-date").value,name=$("p4-name").value.trim().slice(0,120),rate=Number($("p4-rate").value);
 const qty=hours.map(d=>Number($("p4-"+d).value));
 if(!name||!date||!/^\d{4}-\d{2}-\d{2}$/.test(date)||!Number.isFinite(rate)||rate<0||rate>10000||
 qty.some(x=>!Number.isFinite(x)||x<0||x>24)){ $("p4-status").textContent="Renseigner une semaine, un nom et des heures valides.";return}
 try{
 const line={id:id(),date,name,role:$("p4-role").value.trim().slice(0,120),team:$("p4-team").value.trim().slice(0,100),rate,
 ...Object.fromEntries(hours.map((d,i)=>[d,qty[i]])),savedAt:new Date().toISOString(),provenance:"saisie locale"};
 const rows=collection(TKEY);rows.push(line);put(TKEY,rows);$("p4-status").textContent="Pointage conservé dans le navigateur (aucune paie mise à jour).";
 $("p4-name").value="";hours.forEach(d=>$("p4-"+d).value="0");renderPointage();
 }catch(err){$("p4-status").textContent=err.message}
}
function renderPointage(){
 const root=$("p4-body");if(!root)return;const data=collection(TKEY);
 root.innerHTML=data.map(r=>{const total=hours.reduce((acc,d)=>acc+Number(r[d]||0),0);return '<tr><td>'+esc(r.date)+'</td><td>'+esc(r.name)+'</td><td>'+esc(r.role)+'</td><td>'+esc(r.team)+'</td><td>'+format(total)+' h</td><td>'+format(total*r.rate)+' €</td><td><button type="button" class="btn btn-secondary" data-p4-remove="'+esc(r.id)+'">Supprimer</button></td></tr>'}).join("")||
 '<tr><td colspan="7" style="padding:14px;color:#bdcfc8;text-align:center">Aucune heure saisie.</td></tr>';
 root.querySelectorAll("[data-p4-remove]").forEach(b=>b.onclick=()=>{
  if(!confirm("Supprimer ce pointage local ?"))return;
  try{put(TKEY,collection(TKEY).filter(r=>r.id!==b.dataset.p4Remove));renderPointage()}catch(e){$("p4-status").textContent=e.message}
 });
}
window.saveCrewPointage=function(){const form=$("btp-pointage-form");if(form)form.requestSubmit();else alert("Ouvre d'abord le pointage terrain.")};
window.exportPointageCSV=function(){
 const fields=["date","name","role","team","rate","lun","mar","mer","jeu","ven","savedAt"],labels=["Semaine","Nom","Qualification","Équipe","THMO indicatif","Lun","Mar","Mer","Jeu","Ven","Date de saisie"];
 const data=collection(TKEY);
 const lines=[labels.map(csv).join(";"),...data.map(r=>fields.map(k=>csv(r[k])).join(";"))];
 dl("btp-pointage-local-"+project()+".csv","\uFEFF"+lines.join("\r\n"),"text/csv;charset=utf-8");
};
function init(){
 if(el("rdc-proj-select")){
  try{
   const p=JSON.parse(localStorage.getItem("btp_project_workspace_v1")||"{}").projects||[],sel=el("rdc-proj-select");
   sel.replaceChildren();
   for(const item of p){const o=document.createElement("option");o.value=item.id;o.textContent=item.title+(item.dataType==="demonstration"?" (EXEMPLE)":"");sel.appendChild(o)}
   sel.value=project();
  }catch(e){}
 }
 // Never prefill a real report with fictitious 2026 sample work.
 if(el("rdc-date"))el("rdc-date").value=today();
 if(el("rdc-chief")){el("rdc-chief").value="";el("rdc-chief").placeholder="Nom du responsable (saisie)"}
 if(el("rdc-desc"))el("rdc-desc").value="";
 if(el("rdc-heures-mo"))el("rdc-heures-mo").value="0";
 if(el("rdc-heures-engins"))el("rdc-heures-engins").value="0";
 renderRDC();pointageForm();
 window.addEventListener("storage",e=>{if([PKEY,TKEY,PROJECT].includes(e.key)){renderRDC();renderPointage()}});
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();