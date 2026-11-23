/* BTP Studio 3D -> Dossier : explicit, reversible through project JSON backups, user-confirmed estimates only. */
(function(){
"use strict";
const core=window.BTPProjectCore,api=window.BTPAtelier3D;
if(!core||!api)return;
const STORE="btp_project_workspace_v1",ACTIVE="btp_project_active_v1";
const esc=v=>String(v==null?"":v).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const fmt=n=>Number(n).toLocaleString("fr-FR",{maximumFractionDigits:3});
let metric="m³";
function read(){
 try{
  const source=JSON.parse(localStorage.getItem(STORE)||"null");
  if(!source||source.schema!=="btp-workspace-collection-v1"||!Array.isArray(source.projects))return null;
  const id=localStorage.getItem(ACTIVE)||"",p=source.projects.find(v=>v.id===id)||source.projects[0];
  return p?{source,project:core.project(p)}:null;
 }catch(e){return null}
}
const holder=document.createElement("section");holder.id="btp-atelier-link";holder.style.cssText="border-top:1px solid #42645d;margin-top:17px;padding-top:14px;color:#d9ebdf";
holder.innerHTML='<div class="groupTitle" style="margin-bottom:8px">Lien avec le chantier actif</div>'+
 '<div class="note" id="b3d-caption" style="margin-bottom:8px">Import des métrés prévu avec confirmation utilisateur.</div>'+
 '<div class="field"><div class="fieldtop"><label for="b3d-metric">Grandeur à comparer</label></div><select id="b3d-metric" style="width:100%;padding:8px;background:#102127;color:#f0fff0;border:1px solid #48695a;border-radius:8px"><option value="m³">Volume (m³)</option><option value="m²">Surface d’emprise (m²)</option></select></div>'+
 '<div class="field"><div class="fieldtop"><label for="b3d-task">Tâche projet cible</label></div><select id="b3d-task" style="width:100%;padding:8px;background:#102127;color:#f0fff0;border:1px solid #48695a;border-radius:8px"></select></div>'+
 '<div id="b3d-compare" class="results" aria-live="polite" style="margin:10px 0">Sélectionner une tâche compatible.</div>'+
 '<div class="btnrow"><button id="b3d-apply" class="btn primary" type="button">Reporter le métré prévu</button><a href="chantier-studio.html" class="btn ghost" style="text-decoration:none;text-align:center">Dossier ↗</a></div>'+
 '<div id="b3d-message" class="footnote" role="status" aria-live="polite" style="margin-top:9px"></div>'+
 '<div class="warning" style="margin-top:10px">Opération manuelle : remplace uniquement la quantité prévisionnelle sélectionnée. Ne modifie ni quantité réalisée ni coût réel. Contrôler géométrie, unités, hypothèses et pièces contractuelles.</div>';
const inspector=document.querySelector(".inspector .bodypad");if(!inspector)return;inspector.appendChild(holder);
const $=id=>document.getElementById(id);
const matching=()=>{
 const found=read();return found?found.project.tasks.filter(t=>t.unit===metric):[]
};
function quantity(){
 const q=api.getQuantities();
 return metric==="m³"?q.volume:q.area;
}
function refresh(){
 const found=read(),selected=$("b3d-task").value;
 $("b3d-caption").textContent=found?"Dossier : "+found.project.title+" ("+(found.project.dataType==="demonstration"?"EXEMPLE":found.project.dataType==="imported"?"IMPORT":"UTILISATEUR")+")":"Aucun dossier trouvé. Ouvre d’abord « Dossier chantier ».";
 const tasks=matching();
 $("b3d-task").innerHTML=tasks.length?tasks.map(t=>'<option value="'+esc(t.id)+'" '+(t.id===selected?"selected":"")+'>'+esc(t.name)+' · '+fmt(t.quantity)+' '+esc(t.unit)+'</option>').join(""):'<option value="">Aucune tâche en '+metric+'</option>';
 const selectedTask=tasks.find(t=>t.id===$("b3d-task").value);
 const q=quantity();
 if(selectedTask){
  const diff=q-selectedTask.quantity;
  $("b3d-compare").innerHTML='<strong>Modèle : '+fmt(q)+' '+metric+'</strong><br>Prévu dans la tâche : '+fmt(selectedTask.quantity)+' '+metric+
  '<br>Écart estimatif : '+(diff>=0?"+":"")+fmt(diff)+' '+metric;
 }else $("b3d-compare").textContent="Créer une tâche de même unité dans le dossier actif.";
 $("b3d-apply").disabled=!found||!selectedTask||!Number.isFinite(q)||q<0;
}
$("b3d-metric").addEventListener("change",e=>{metric=e.target.value;refresh()});
$("b3d-task").addEventListener("change",refresh);
$("b3d-apply").addEventListener("click",()=>{
 const found=read(),taskId=$("b3d-task").value;if(!found)return;
 const q=quantity(),task=found.project.tasks.find(t=>t.id===taskId&&t.unit===metric);
 if(!task||!Number.isFinite(q)||q<0)return;
 const value=Math.round(q*1000)/1000;
 if(!confirm('Remplacer le métré prévisionnel de « '+task.name+' » : '+fmt(task.quantity)+' '+metric+' → '+fmt(value)+' '+metric+' ?\n\nLe calcul 3D est indicatif. Le réalisé et les contrôles restent inchangés.'))return;
 try{
  const updated={...task,quantity:value,verification:"À vérifier"};
  const p=core.putTask(found.project,updated);core.schedule(p);
  const i=found.source.projects.findIndex(v=>v.id===found.project.id);
  if(i<0)throw Error("Projet non trouvé");
  found.source.projects[i]=p;
  localStorage.setItem(STORE,JSON.stringify(found.source));
  $("b3d-message").textContent="Métré prévisionnel reporté et marqué « à vérifier ». Ouvre le dossier pour contrôler le planning et le déboursé.";
  refresh();
 }catch(e){$("b3d-message").textContent="Report refusé : "+e.message}
});
document.addEventListener("btp3d:changed",refresh);
window.addEventListener("storage",e=>{if(e.key===STORE||e.key===ACTIVE)refresh()});
refresh();
})();