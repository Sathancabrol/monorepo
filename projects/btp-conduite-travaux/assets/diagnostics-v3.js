/* BTP Studio diagnostic helper: structural audit, not a claim of validated business functionality. */
(function(){
"use strict";
const ids=["cockpit","company","depot","projects_hub","planning","simulator","fleet","catalog","hr","opbtp","safety","rdc","compagnon_mobile","obsidian","schemas","sdp","benchmark","procurement","ledger","docs","archives","atelier_3d","fiches_taches"];
const errors=[];let lastAudit=null;
window.addEventListener("error",e=>{errors.push({time:new Date().toISOString(),message:e.message||"Erreur JS",source:e.filename||"",line:e.lineno||0});if(errors.length>70)errors.shift()});
window.addEventListener("unhandledrejection",e=>{errors.push({time:new Date().toISOString(),message:String(e.reason).slice(0,300),source:"promise"});if(errors.length>70)errors.shift()});
const esc=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function run(){
 const all=document.querySelectorAll("[id]"),counts={};for(const e of all){counts[e.id]=(counts[e.id]||0)+1}
 const duplicates=Object.entries(counts).filter(x=>x[1]>1).map(x=>({id:x[0],count:x[1]}));
 const modules=ids.map(id=>{
 const p=document.getElementById("tab-"+id);
 const controls=p?p.querySelectorAll("button,input,select,textarea,canvas,iframe").length:0;
 const aid=p&&!!p.querySelector(".btp-wb-hub");
 const frames=p?Array.from(p.querySelectorAll("iframe")).map(f=>f.getAttribute("src")):[];
 const available=!!p&&!!p.querySelector(".btp-wb-hub");
 return {id,tab_exists:!!p,toolbox_present:aid,controls_visible_in_dom:controls,iframe_sources:frames,structural_status:available?"wired":"missing",functional_validation:"not_proven"};
 });
 lastAudit={schema:"btp-studio-structural-audit-v1",timestamp:new Date().toISOString(),total:ids.length,connected:modules.filter(x=>x.structural_status==="wired").length,modules,duplicate_dom_ids:duplicates,observed_errors:errors.slice(-30),warning:"Diagnostic de structure uniquement : ne garantit ni la validité métier, ni la fonction des boutons, ni la conformité du site."};
 return lastAudit;
}
function display(){
 const data=run();
 const div=document.getElementById("btp-diag-modal");div.classList.add("open");
 div.innerHTML='<div class="btp-wb-dialog" role="dialog" aria-modal="true" aria-label="Diagnostic des modules BTP">'+
 '<div style="display:flex;justify-content:space-between;align-items:center;gap:9px"><h2 class="btp-wb-dialog-title">Diagnostic des 23 modules</h2><button type="button" class="btp-wb-action" data-btp-diag="close">Fermer</button></div>'+
 '<p class="btp-wb-secondary">Contrôle de structure : '+data.connected+'/'+data.total+' panneaux connectés. Les calculs, interactions avancées et validations métier ne sont pas certifiés par ce contrôle.</p>'+
 '<div style="overflow:auto;max-height:55vh"><table style="width:100%;border-collapse:collapse;font-size:12px"><thead><tr><th style="text-align:left;padding:9px">Module</th><th>Panneau</th><th>Outils DOM</th><th>Atelier</th></tr></thead><tbody>'+
 data.modules.map(m=>'<tr style="border-top:1px solid #35535a"><td style="padding:9px">'+esc(m.id)+'</td><td style="text-align:center">'+(m.tab_exists?"Oui":"Non")+'</td><td style="text-align:center">'+m.controls_visible_in_dom+'</td><td style="text-align:center">'+(m.toolbox_present?"Oui":"Non")+'</td></tr>').join("")+
 '</tbody></table></div>'+
 '<div class="btp-wb-forced-note">Doublons ID signalés : '+data.duplicate_dom_ids.length+' · Erreurs JS interceptées depuis le chargement du diagnostic : '+data.observed_errors.length+'. L’absence d’erreur détectée n’est pas une validation des fonctionnalités.</div>'+
 '<div class="btp-wb-actions" style="margin-top:12px"><button type="button" class="btp-wb-action primary" data-btp-diag="export">Exporter diagnostic JSON</button><button type="button" class="btp-wb-action" data-btp-diag="again">Relancer le contrôle</button></div>'+
 '</div>';
}
function setup(){
 if(document.getElementById("btp-diag-modal"))return;
 const root=document.createElement("div");root.id="btp-diag-modal";root.className="btp-wb-modal";document.body.appendChild(root);
 const floating=document.querySelector(".btp-wb-float");if(floating){const btn=document.createElement("button");btn.textContent="Diagnostic 23";btn.title="Contrôler la structure de toutes les pages";btn.setAttribute("data-btp-diag","open");floating.insertBefore(btn,floating.firstChild)}
 document.addEventListener("click",function(e){const el=e.target.closest("[data-btp-diag]");if(!el)return;switch(el.dataset.btpDiag){case"open":case"again":display();break;case"close":root.classList.remove("open");break;case"export":if(!lastAudit)run();const blob=new Blob([JSON.stringify(lastAudit,null,2)],{type:"application/json"}),u=URL.createObjectURL(blob),a=document.createElement("a");a.href=u;a.download="btp-audit-23-modules.json";a.click();setTimeout(()=>URL.revokeObjectURL(u),3000);break;}});
 root.addEventListener("click",e=>{if(e.target===root)root.classList.remove("open")});
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",setup);else setup();
})();