/* Cross-module selected-project context; does NOT silently overwrite historical demo metrics. */
(function(){
"use strict";
const S="btp_project_workspace_v1",A="btp_project_active_v1";
const esc=v=>String(v==null?"":v).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function stored(){try{const r=JSON.parse(localStorage.getItem(S)||"null");return r&&r.schema==="btp-workspace-collection-v1"&&Array.isArray(r.projects)?r.projects:[]}catch(e){return []}}
function templates(){
 const p=stored(),id=localStorage.getItem(A)||"",target=p.find(x=>x.id===id)||p[0]||null;
 return {projects:p,active:target}
}
function add(){
 const state=templates(),tabs=document.querySelectorAll(".tab-panel");
 tabs.forEach(tab=>{
  if(tab.querySelector(":scope > .btp-context"))return;
  const bar=document.createElement("div");bar.className="btp-context";bar.dataset.contextFor=tab.id;
  const first=tab.querySelector(":scope > .btp-wb-hub");if(first)first.insertAdjacentElement("afterend",bar);else tab.insertBefore(bar,tab.firstChild);
 });
 update();
}
function update(){
 const data=templates();
 document.querySelectorAll(".btp-context").forEach(bar=>{
  const p=data.active;
  const options=data.projects.map(pr=>'<option value="'+esc(pr.id)+'" '+(p&&p.id===pr.id?"selected":"")+'>'+esc(pr.title)+'</option>').join("");
  bar.innerHTML='<label for="ctx-'+bar.dataset.contextFor+'">Dossier actif</label>'+
  (options?'<select id="ctx-'+bar.dataset.contextFor+'" aria-label="Choisir le dossier actif">'+options+'</select>':'<strong>Premier dossier à créer</strong>')+
  (p?'<span class="btp-context-tag '+(p.dataType==="demonstration"?"demo":"")+'">'+(p.dataType==="demonstration"?"EXEMPLE":p.dataType==="imported"?"IMPORT":"UTILISATEUR")+'</span>'+
  '<span>'+((Array.isArray(p.tasks)?p.tasks.length:0))+' tâches</span>':'')+
  '<span class="btp-context-note">Contexte partagé entre modules. Les tableaux historiques restent des démonstrations indépendantes tant qu’aucun lien métier n’est explicitement établi.</span>'+
  '<a href="chantier-studio.html">Ouvrir le dossier ↗</a>';
 });
}
function init(){
 add();
 document.addEventListener("change",e=>{
  if(!e.target.closest(".btp-context")||e.target.tagName!=="SELECT")return;
  const id=e.target.value;if(!stored().some(p=>p.id===id))return;
  try{localStorage.setItem(A,id)}catch(err){}update()
 });
 window.addEventListener("storage",e=>{if(e.key===S||e.key===A)update()});
 document.querySelectorAll(".tab-panel").forEach(tab=>{
  const observer=new MutationObserver(records=>{if(records.some(x=>Array.from(x.addedNodes).some(n=>n.nodeType===1&&n.classList?.contains("btp-wb-hub"))))add()});
  observer.observe(tab,{childList:true});
 });
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();