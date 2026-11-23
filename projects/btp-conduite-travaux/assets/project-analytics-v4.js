/* Cross-module project facts derived from the validated local project engine.
 * The historical dashboard remains a demo; this panel never implies live data. */
(function(){
"use strict";
const core=window.BTPProjectCore,STORAGE="btp_project_workspace_v1",ACTIVE="btp_project_active_v1";if(!core)return;
const definitions={
 company:{title:"Coûts du chantier actif",columns:["name","plannedCost","realizedValue"]},
 planning:{title:"Planning du dossier actif",columns:["name","start","endInclusive"]},
 sdp:{title:"Déboursés unitaires et métrés",columns:["name","quantity","unitCost","plannedCost"]},
 hr:{title:"Ressources humaines prévues",columns:["name","crew","estimatedCrewHours"]},
 procurement:{title:"Besoins à préparer",columns:["name","quantity","unit"]},
 benchmark:{title:"Références internes de prix",columns:["name","unitCost","unit"]},
 safety:{title:"Contrôles déclaratifs",columns:["name","verification","start"]},
 simulator:{title:"Quantités liées au dossier",columns:["name","quantity","unit"]},
 rdc:{title:"Quantités prévues / réalisées",columns:["name","quantity","doneQuantity"]},
 docs:{title:"Contrôles / documents attendus",columns:["name","verification","group"]},
 archives:{title:"Travaux et pièces attendues",columns:["name","verification","group"]}
};
const labels={name:"Activité",plannedCost:"Prévu (€)",realizedValue:"Valorisé (€)",start:"Début",endInclusive:"Fin",quantity:"Quantité",doneQuantity:"Réalisé",unitCost:"PU indicatif (€)",unit:"Unité",crew:"Équipe",estimatedCrewHours:"Heures équipe",verification:"Contrôle",group:"Phase"};
const $=id=>document.getElementById(id),fmt=n=>Number(n).toLocaleString("fr-FR",{maximumFractionDigits:2});
const euro=n=>Number(n).toLocaleString("fr-FR",{style:"currency",currency:"EUR"});
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function state(){try{
 const json=JSON.parse(localStorage.getItem(STORAGE)||"{}"),id=localStorage.getItem(ACTIVE);
 const project=json.projects?.find(p=>p.id===id)||json.projects?.[0];
 return project?core.schedule(project):null
}catch(e){return {error:e.message}}}
function textFor(row,key){
 const v=row[key];if(["plannedCost","realizedValue","unitCost"].includes(key))return euro(v);
 if(["quantity","doneQuantity"].includes(key))return fmt(v);
 if(key==="estimatedCrewHours")return fmt(v)+" h";
 return String(v??"—")
}
function render(){
 const model=state();
 for(const [id,cfg] of Object.entries(definitions)){
  const host=$("btp-project-live-"+id);if(!host)continue;
  if(!model||model.error){host.innerHTML='<strong>'+esc(cfg.title)+'</strong><p>Pas de dossier exploitable : '+esc(model?.error||"ouvrir la Gestion des chantiers")+'</p><a href="chantier-studio.html">Accéder au dossier</a>';continue}
  const p=model.project,s=model.summary,demo=p.dataType==="demonstration",phase=demo?"EXEMPLE":p.dataType==="imported"?"IMPORT NON VÉRIFIÉ":"SAISIE UTILISATEUR";
  const kpis=[["Déboursé théorique",euro(s.plannedCost)],["Valorisé théorique",euro(s.theoreticalRealizedValue)],["Avancement valorisé",fmt(s.valueProgressPct)+" %"],["Durée calendaire",s.calendarDays+" j"]];
  if(id==="hr"){kpis[0]=["Heures d'équipe prévues",fmt(s.plannedCrewHours)+" h"];kpis[1]=["Tâches",String(model.tasks.length)]}
  if(id==="planning"){kpis[0]=["Début",p.startDate];kpis[1]=["Fin prévue (exclue)",s.endExclusive]}
  const table='<table class="btp-project-live-table"><thead><tr>'+cfg.columns.map(k=>'<th>'+esc(labels[k]||k)+'</th>').join("")+'</tr></thead><tbody>'+
   (model.tasks.length?model.tasks.slice(0,30).map(t=>'<tr>'+cfg.columns.map(k=>'<td>'+esc(textFor(t,k))+'</td>').join("")+'</tr>').join(""):'<tr><td colspan="'+cfg.columns.length+'">Aucune tâche</td></tr>')+'</tbody></table>';
  host.innerHTML='<div class="btp-project-live-top"><div><small>PROJET ACTIF · '+esc(phase)+'</small><h3>'+esc(cfg.title)+'</h3><p>'+esc(p.title)+' — quantités et dates calculées localement</p></div><a href="chantier-studio.html">Modifier le dossier ↗</a></div>'+
  '<div class="btp-project-live-kpis">'+kpis.map(k=>'<div><small>'+esc(k[0])+'</small><strong>'+esc(k[1])+'</strong></div>').join("")+'</div>'+
  '<div class="btp-project-live-scroll">'+table+'</div><p class="btp-project-live-warning">Hypothèses : ce tableau vient du dossier local. Les anciens indicateurs du module qui suivent peuvent être fictifs ; aucune conformité ou dépense réelle ne peut être inférée automatiquement.</p>';
 }
}
function init(){
 const style=document.createElement("style");
 style.textContent=[
 ".btp-project-live{border:1px solid #688e7c88;border-radius:13px;padding:15px;margin:0 0 16px;background:linear-gradient(140deg,#1d393c,#11272d);color:#e6f4e8}",
 ".btp-project-live-top{display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap}",
 ".btp-project-live-top small{font-size:10px;letter-spacing:.12em;font-weight:850;color:#b9e987}",
 ".btp-project-live-top h3{font-size:17px;margin:5px 0;color:#f2fff0}",
 ".btp-project-live-top p{color:#b6d0c2;font-size:11px;margin:0}",
 ".btp-project-live-top a{font-size:11px;font-weight:800;padding:8px 11px;border-radius:7px;background:#bce985;color:#1b2d20;text-decoration:none}",
 ".btp-project-live-kpis{display:flex;gap:9px;flex-wrap:wrap;margin:13px 0}",
 ".btp-project-live-kpis>div{min-width:125px;background:#12282b;border:1px solid #50776a8a;border-radius:9px;padding:9px 12px}",
 ".btp-project-live-kpis small{display:block;font-size:9px;color:#bbd1c1;text-transform:uppercase}",
 ".btp-project-live-kpis strong{font-size:17px;color:#eaffeb}",
 ".btp-project-live-scroll{overflow:auto;max-height:235px}",
 ".btp-project-live-table{border-collapse:collapse;width:100%;font-size:11px}",
 ".btp-project-live-table th,.btp-project-live-table td{padding:7px 9px;border-bottom:1px solid #6b8b7440;text-align:left}",
 ".btp-project-live-warning{font-size:10px;color:#dfc496;margin:10px 0 0}"
 ].join("");document.head.appendChild(style);
 for(const id of Object.keys(definitions)){const tab=$("tab-"+id);if(!tab)continue;
  const panel=document.createElement("section");panel.className="btp-project-live";panel.id="btp-project-live-"+id;
  const anchor=tab.querySelector(".btp-context")||tab.querySelector(".btp-wb-hub");if(anchor)anchor.insertAdjacentElement("afterend",panel);else tab.insertBefore(panel,tab.firstChild);
 }
 render();
 window.addEventListener("storage",e=>{if(e.key===STORAGE||e.key===ACTIVE)render()});
 document.addEventListener("change",e=>{if(e.target.closest(".btp-context"))setTimeout(render,0)});
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();