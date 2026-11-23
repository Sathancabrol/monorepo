/* BTP 360: one cross-module workflow spanning the 23 existing routes.
   Planning dashboard only: does not claim works completion or regulatory approval. */
(function(){
"use strict";
const stages=[
 {id:"offer",name:"Offre & chiffrage",number:"01",desc:"Marché, prix, écarts, arbitrages",ids:["projects_hub","sdp","benchmark","company"]},
 {id:"prep",name:"Préparation",number:"02",desc:"Études, sécurité, achats, ressources",ids:["planning","schemas","safety","opbtp","procurement"]},
 {id:"means",name:"Moyens",number:"03",desc:"Dépôt, parc, matériels et équipes",ids:["depot","fleet","catalog","hr"]},
 {id:"execute",name:"Exécution",number:"04",desc:"Terrain, rapports, modèle et méthodes",ids:["compagnon_mobile","rdc","simulator","atelier_3d","fiches_taches"]},
 {id:"docs",name:"Contrôles & pièces",number:"05",desc:"Références, traçabilité, contrôles",ids:["docs","obsidian","ledger"]},
 {id:"receive",name:"Réception & clôture",number:"06",desc:"Archives, DOE et état final",ids:["archives","cockpit"]}
];
const labels={cockpit:"Cockpit",company:"Trésorerie",depot:"Dépôt",projects_hub:"Chantiers",planning:"Planning",simulator:"SIG",fleet:"Flotte",catalog:"Matériaux",hr:"Équipes",opbtp:"Balisage",safety:"AIPR/QSE",rdc:"Rapport RDC",compagnon_mobile:"Terrain",obsidian:"Connaissances",schemas:"Technique",sdp:"Prix/DQE",benchmark:"Benchmark",procurement:"Fournisseurs",ledger:"Journal d'audit",docs:"Normes",archives:"Archives/DOE",atelier_3d:"Atelier 3D",fiches_taches:"Fiches de tâches"};
const esc=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function load(){try{return JSON.parse(localStorage.getItem("btp_workbench_v3_20261123")||"{}")}catch(e){return {}}}
function countChecks(id){const obj=load()[id]||{},checks=Array.isArray(obj.checks)?obj.checks:[];return checks.filter(Boolean).length}
function init(){
 const cockpit=document.getElementById("tab-cockpit");if(!cockpit||document.getElementById("btp-flow"))return;
 const host=document.createElement("section");host.id="btp-flow";host.className="btp-flow";
 const workbench=cockpit.querySelector(".btp-wb-hub");if(workbench)workbench.insertAdjacentElement("afterend",host);else cockpit.insertBefore(host,cockpit.firstChild);
 host.addEventListener("click",function(e){const b=e.target.closest("button[data-btp-nav]");if(!b)return;const id=b.dataset.btpNav;if(typeof window.switchNav==="function")window.switchNav(id)});
 function render(){
 let html='<div class="btp-flow-head"><div><div class="btp-flow-title">Vue 360° · Cycle du chantier</div><h2>De l’appel d’offres à la réception</h2><p>Les six étapes traversent les 23 modules. Accède directement au prochain dossier à compléter.</p></div><div class="btp-wb-chip">Suivi personnel · pas de validation automatique</div></div><div class="btp-flow-grid">';
 for(const g of stages){
  const total=g.ids.length*4,done=g.ids.reduce((v,id)=>v+Math.min(4,countChecks(id)),0),rate=Math.round(done/total*100);
  const incomplete=g.ids.find(id=>countChecks(id)<4)||g.ids[0];
  html+='<button type="button" class="btp-flow-step" data-btp-nav="'+esc(incomplete)+'" title="Ouvrir '+esc(labels[incomplete])+'">'+
  '<span class="btp-flow-num"><span>ÉTAPE '+g.number+'</span><span>'+done+'/'+total+'</span></span><strong>'+esc(g.name)+'</strong><small>'+esc(g.desc)+'</small>'+
  '<span class="btp-flow-bar"><i style="width:'+rate+'%"></i></span></button>';
 }
 html+='</div><div class="btp-flow-modules">'+stages.flatMap(g=>g.ids.map(id=>'<button type="button" data-btp-nav="'+esc(id)+'">'+esc(labels[id])+'</button>')).join("")+'</div><div class="btp-flow-disclaimer">Progression basée sur les cases de suivi locales de chaque module, non sur l’exécution effective ou la conformité réglementaire du chantier.</div>';
 host.innerHTML=html;
 }
 render();
 document.addEventListener("change",e=>{if(e.target.matches("[data-wb-check]"))setTimeout(render,0)});
 document.addEventListener("click",e=>{if(e.target.matches('[data-wb-action="toggle"]'))setTimeout(render,0)});
 window.addEventListener("storage",e=>{if(e.key==="btp_workbench_v3_20261123")render()});
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();