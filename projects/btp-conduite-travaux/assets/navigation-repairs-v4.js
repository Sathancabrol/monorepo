/* BTP Studio v4 — fixes broken navigation states without rewriting other working modules. */
(function(){
"use strict";
const $=id=>document.getElementById(id),escape=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const originalTech=window.setTechniqueViewMode;
const technicalExtra={hydraulique:"tech-hydraulique-view",gtr:"tech-gtr-view",bruckner:"tech-bruckner-view",reseauxsecs:"tech-reseauxsecs-view"};
if(typeof originalTech==="function"){
 window.setTechniqueViewMode=function(mode){
  const extra=Object.prototype.hasOwnProperty.call(technicalExtra,mode);
  if(extra){
   originalTech("formulas");
   const form=$("tech-formulas-view");if(form)form.style.display="none";
   ["tech-compactage-cut-view","tech-enrobes-2d-view","tech-tasksheet-view"].forEach(id=>{const n=$(id);if(n)n.style.display="none"});
  }else originalTech(mode);
  for(const [name,id] of Object.entries(technicalExtra)){const el=$(id);if(el)el.style.display=extra&&mode===name?"block":"none"}
  document.querySelectorAll(".tech-view-btn").forEach(b=>b.classList.remove("active"));
  const button=$("btn-tech-"+mode.replaceAll("_",""))||$("btn-tech-"+mode);
  if(button)button.classList.add("active");
  if(mode==="hydraulique"){window.updateHydrauliqueCalculation?.();window.updateBassinCalculation?.();}
  if(mode==="reseauxsecs"){window.updateElectriqueCalculation?.();window.updateEPCalculation?.();}
  if(mode==="bruckner")window.dispatchEvent(new Event("resize"));
 };
}
const originalPlan=window.setPlanningViewMode;
function activeProject(){try{
 const saved=JSON.parse(localStorage.getItem("btp_project_workspace_v1")||"{}"),projects=saved.projects||[];
 const id=localStorage.getItem("btp_project_active_v1")||"";return projects.find(p=>p.id===id)||projects[0]||null;
 }catch(e){return null}
}
let showingMonth=new Date().toISOString().slice(0,7);
function monthISO(y,m,d){return String(y)+"-"+String(m+1).padStart(2,"0")+"-"+String(d).padStart(2,"0")}
window.btpRenderMonthlyV4=function(){
 const holder=$("btp-month-v4");if(!holder)return;
 const y=Number(showingMonth.slice(0,4)),m=Number(showingMonth.slice(5,7))-1;
 if(!Number.isFinite(y)||!Number.isFinite(m)||m<0||m>11)return;
 const first=new Date(y,m,1),offset=(first.getDay()+6)%7;
 const days=new Date(y,m+1,0).getDate();
 const p=activeProject();let tasks=[];
 if(p&&window.BTPProjectCore){try{tasks=window.BTPProjectCore.schedule(p).tasks}catch(e){}}
 const mode=p?.dataType==="demonstration"?"EXEMPLE":p?"SAISIE LOCALE":"AUCUN DOSSIER";
 let html='<div style="padding:16px;border:1px solid #496864;background:#192d31;border-radius:11px"><div style="display:flex;gap:12px;justify-content:space-between;align-items:center;flex-wrap:wrap"><div><b style="color:#e9f6ed;font-size:15px">Agenda mensuel du dossier actif</b><p style="font-size:11px;color:#adc6bd">Prévision du modèle WBS : jours calendaires, sans jours fériés ni interruptions. '+mode+'</p></div><label style="color:#e3eedb">Mois <input id="btp-month-picker" type="month" value="'+showingMonth+'" style="margin-left:8px;background:#10252a;color:white;border:1px solid #48665c;padding:8px;border-radius:8px"></label></div>';
 html+='<div style="display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:5px;margin-top:13px">';
 for(const d of ["Lun","Mar","Mer","Jeu","Ven","Sam","Dim"])html+='<div style="font-size:10px;color:#b3d0c3;text-align:center;padding:6px">'+d+'</div>';
 for(let i=0;i<offset;i++)html+='<div></div>';
 for(let d=1;d<=days;d++){
  const date=monthISO(y,m,d),activities=tasks.filter(t=>t.start<=date&&t.endExclusive>date);
  html+='<div style="min-height:79px;border:1px solid #47615f;border-radius:8px;padding:7px;min-width:0"><b style="font-size:11px;color:#e9f6e8">'+d+'</b>'+
  activities.slice(0,3).map(t=>'<div title="'+escape(t.name)+'" style="font-size:9px;background:#2d5345;color:#e3f7e5;border-radius:3px;margin-top:4px;padding:3px 4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+escape(t.name)+'</div>').join("")+
  (activities.length>3?'<small style="color:#b9dfb5">+'+(activities.length-3)+' autres</small>':"")+'</div>';
 }
 html+='</div><p style="margin:14px 0 0;color:#aec9bd;font-size:11px">'+(p?escape(p.title)+" · "+tasks.length+" tâche(s) planifiée(s)":"Aucun dossier chargé : <a href='chantier-studio.html' style='color:#bce985'>créer un projet</a>")+'</p></div>';
 holder.innerHTML=html;
 $("btp-month-picker")?.addEventListener("change",e=>{if(/^\d{4}-\d{2}$/.test(e.target.value)){showingMonth=e.target.value;window.btpRenderMonthlyV4()}});
};
if(typeof originalPlan==="function"){
 window.setPlanningViewMode=function(mode){
  const intemp=$("planning-intemperies-view"),month=$("btp-month-v4"),agenda=$("planning-agenda-view"),gantt=$("planning-gantt-view");
  if(intemp)intemp.style.display=mode==="intemperies"?"block":"none";
  if(month)month.style.display=mode==="agenda_month"?"block":"none";
  if(mode==="agenda_month"||mode==="intemperies"){
   if(agenda)agenda.style.display="none";if(gantt)gantt.style.display="none";
  }else originalPlan(mode);
  if(mode==="agenda_month")window.btpRenderMonthlyV4();
  document.querySelectorAll(".planning-mode-btn").forEach(b=>b.classList.toggle("active",b.id==="btn-plan-"+mode));
 };
}
function init(){
 const v=$("tab-planning"),intemp=$("planning-intemperies-view"),gantt=$("planning-gantt-view");
 // The old nested template had the intempéries panel inside the Gantt container,
 // which is overwritten by renderPlanningGantt. Move it to preserve the form and data.
 if(intemp&&gantt&&gantt.contains(intemp))gantt.insertAdjacentElement("afterend",intemp);
 if(v&&!$("btp-month-v4")){
  const mon=document.createElement("div");mon.id="btp-month-v4";mon.style.display="none";const view=$("planning-agenda-view");if(view)view.insertAdjacentElement("afterend",mon);else v.appendChild(mon);
 }
 if(v&&!$("btn-plan-intemperies")){
  const anchor=$("btn-plan-gantt");if(anchor){const btn=document.createElement("button");btn.className="btn-secondary planning-mode-btn";btn.id="btn-plan-intemperies";btn.textContent="Intempéries & constats";btn.onclick=()=>window.setPlanningViewMode("intemperies");anchor.insertAdjacentElement("afterend",btn)}
 }
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();