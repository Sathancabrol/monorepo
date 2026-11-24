/* BTP Studio / Project Workspace — local-first WBS, Gantt, costs and records. */
(function(){
"use strict";
const core=window.BTPProjectCore;
if(!core){document.body.textContent="Le moteur de calcul du projet ne s'est pas chargé.";return}
const STORE="btp_project_workspace_v1",ACTIVE="btp_project_active_v1";
const el=id=>document.getElementById(id);
const esc=s=>String(s==null?"":s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const euro=n=>Number(n).toLocaleString("fr-FR",{style:"currency",currency:"EUR"});
const fmt=(n,d=2)=>Number(n).toLocaleString("fr-FR",{maximumFractionDigits:d});
const today=()=>new Date().toISOString().slice(0,10);
let projects=[],activeId="",editingId="",modalMode="new",seq=0,storageBlocked=false;
const newId=prefix=>prefix+"-"+Date.now().toString(36)+"-"+(++seq).toString(36);
function active(){return projects.find(p=>p.id===activeId)||projects[0]}
function error(s,id="formError"){el(id).textContent=s}
function store(){if(storageBlocked){alert("Stockage protégé : données illisibles. Exportez le JSON avant toute intervention. Les modifications restent en mémoire.");return}try{localStorage.setItem(STORE,JSON.stringify({schema:"btp-workspace-collection-v1",projects}));localStorage.setItem(ACTIVE,activeId)}catch(e){error("Stockage indisponible : utiliser Export JSON.")}}
function load(){
 let stored=null;
 try{
  stored=localStorage.getItem(STORE);
  const v=JSON.parse(stored||"null");
  if(stored!==null){
   if(!v||v.schema!=="btp-workspace-collection-v1"||!Array.isArray(v.projects)||!v.projects.length||v.projects.length>100)throw Error("Collection invalide");
   const next=v.projects.map(core.project);
   if(new Set(next.map(p=>p.id)).size!==next.length)throw Error("Identifiants de projets dupliqués");
   next.forEach(core.schedule);
   projects=next;
  }
  activeId=localStorage.getItem(ACTIVE)||"";
 }catch(e){
  // Never replace unreadable user data with a demonstration.
  if(!projects.length)projects=[core.sample()];
  activeId=projects.some(p=>p.id===activeId)?activeId:projects[0].id;
  storageBlocked=true;
  return;
 }
 storageBlocked=false;
 if(!projects.length){projects=[core.sample()];activeId=projects[0].id;store()}
 if(!projects.some(p=>p.id===activeId))activeId=projects[0].id;
}
function saveFile(name,body,type){const url=URL.createObjectURL(new Blob([body],{type})),a=document.createElement("a");a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),3000)}
function csv(v){let s=String(v==null?"":v);if(/^[=+\-@\t\r]/.test(s))s="'"+s;return '"'+s.replace(/"/g,'""')+'"'}
function listProjects(){
 el("projectList").innerHTML=projects.map(p=>'<button class="project-item '+(p.id===activeId?"active":"")+'" data-project="'+esc(p.id)+'"><strong>'+esc(p.title)+'</strong><small>'+esc(p.client||"Sans client")+'</small><span class="pill">'+(p.dataType==="demonstration"?"EXEMPLE":p.dataType==="imported"?"IMPORT":"UTILISATEUR")+'</span></button>').join("");
}
function warnings(model){
 const w=model.warnings.slice();
 if(storageBlocked)w.unshift("Stockage local illisible : sauvegarde bloquée pour préserver les données originales. Les modifications restent en mémoire.");
 if(model.project.dataType==="demonstration")w.unshift("Projet de démonstration : données, durées et coûts fictifs.");
 if(!model.project.client)w.push("Maître d’ouvrage non renseigné.");
 el("warnings").innerHTML=w.length?w.map(t=>'<p>'+esc(t)+'</p>').join(""):'<p class="ok">Aucune incohérence simple détectée. Validation humaine toujours indispensable.</p>';
}
function table(rows){
 el("taskTable").innerHTML=rows.length?rows.map(t=>
 '<tr><td><strong>'+esc(t.name)+'</strong><small>'+esc(t.group)+' · ID '+esc(t.id)+(t.depends.length?' · après '+esc(t.depends.join(", ")):"")+'</small></td>'+
 '<td>'+fmt(t.quantity)+' '+esc(t.unit)+'</td><td>'+fmt(t.doneQuantity)+' '+esc(t.unit)+'</td>'+
 '<td>'+fmt(t.dailyRate)+'/j</td><td>'+t.durationDays+' j</td><td>'+esc(t.start)+'</td><td>'+esc(t.endInclusive)+'</td>'+
 '<td>'+euro(t.plannedCost)+'</td><td><button class="row-button" data-edit="'+esc(t.id)+'">Modifier</button></td></tr>').join(""):
 '<tr><td colspan="9" style="padding:26px;text-align:center">Aucune tâche dans ce chantier. Ajoute un poste pour générer le Gantt.</td></tr>';
}
function dayDiff(from,to){return (Date.parse(to+"T00:00:00Z")-Date.parse(from+"T00:00:00Z"))/86400000}
function gantt(model){
 const rows=model.tasks,period=Math.max(1,model.summary.calendarDays),start=model.project.startDate;
 if(!rows.length){el("gantt").innerHTML='<p class="muted">Le Gantt sera généré avec la première tâche.</p>';return}
 let out='<div class="gantt-inner"><div class="gantt-head"><span>Début : '+esc(start)+'</span><span>Fin : '+esc(core.addDays(model.summary.endExclusive,-1))+'</span></div>';
 rows.forEach(t=>{
 const left=Math.max(0,dayDiff(start,t.start)/period*100),width=Math.min(100-left,t.durationDays/period*100);
 const done=t.quantity>0?Math.max(0,Math.min(100,t.doneQuantity/t.quantity*100)):0;
 out+='<div class="gantt-row"><div class="gantt-label">'+esc(t.name)+'<small>'+esc(t.id)+' · '+t.durationDays+' jours</small></div>'+
 '<div class="gantt-track"><div class="gantt-bar" style="left:'+left+'%;width:'+width+'%" title="'+esc(t.name)+' — '+esc(t.start)+' au '+esc(t.endInclusive)+'"><i style="width:'+done+'%"></i></div></div></div>';
 });
 el("gantt").innerHTML=out+"</div>";
}
function render(){
 const model=core.schedule(active()),p=model.project,m=model.summary;
 el("projectType").textContent=p.dataType==="demonstration"?"EXEMPLE PÉDAGOGIQUE":p.dataType==="imported"?"PROJET IMPORTÉ · À VÉRIFIER":"PROJET UTILISATEUR";
 el("projectTitle").textContent=p.title;el("projectDetail").textContent=[p.client||"Client non renseigné",p.city||"Localisation non renseignée","Début : "+p.startDate,p.tasks.length+" tâches"].join(" · ");
 el("plannedCost").textContent=euro(m.plannedCost);el("earnedValue").textContent=euro(m.theoreticalRealizedValue);
 el("progress").textContent=fmt(m.valueProgressPct,1)+" %";el("calendarDays").textContent=m.calendarDays+" j";
 el("summaryFooter").innerHTML='<span>Heures équipe estimées : <strong>'+fmt(m.plannedCrewHours,0)+' h</strong></span><span>Coût constaté renseigné : <strong>'+(m.actualCost===null?"Non renseigné":euro(m.actualCost))+'</strong> ('+m.actualCostCoverage+' tâches)</span>';
 listProjects();warnings(model);table(model.tasks);gantt(model);
}
function resetEditor(){
 editingId="";el("taskForm").reset();el("editorTitle").textContent="Nouvelle activité";el("editorSubtitle").textContent="Hypothèses de quantité, rendement et moyens.";
 el("taskQuantity").value="100";el("taskUnit").value="m²";el("taskDone").value="0";el("taskCost").value="0";el("taskDailyRate").value="50";el("taskCrew").value="3";el("taskDependencies").value="";el("taskActualCost").value="";el("taskNotes").value="";el("taskDays").value="";el("taskConstraint").value="";el("deleteTask").disabled=true;error("");
}
function editTask(id){
 const t=active().tasks.find(x=>x.id===id);if(!t)return;editingId=id;
 try{localStorage.setItem("btp_project_active_task_v1",id)}catch(e){}
 el("editorTitle").textContent="Modifier "+id;el("editorSubtitle").textContent="Recalcul automatique des dépendances après enregistrement.";
 for(const [key,val] of Object.entries({taskName:t.name,taskGroup:t.group,taskQuantity:t.quantity,taskUnit:t.unit,taskDone:t.doneQuantity,taskCost:t.unitCost,taskDailyRate:t.dailyRate,taskCrew:t.crew,taskDays:t.daysOverride||"",taskConstraint:t.startConstraint||"",taskDependencies:t.depends.join(", "),taskActualCost:t.costActual===null?"":t.costActual,taskNotes:t.notes}))el(key).value=val;
 el("deleteTask").disabled=false;error("");el("taskName").focus();
}
const val=id=>el(id).value;
const optional=id=>val(id).trim()===""?null:Number(val(id));
function submitTask(event){
 event.preventDefault();error("");
 try{
 const id=editingId||newId("t"),raw={id,name:val("taskName"),group:val("taskGroup"),unit:val("taskUnit"),quantity:val("taskQuantity"),doneQuantity:val("taskDone"),unitCost:val("taskCost"),dailyRate:val("taskDailyRate"),crew:val("taskCrew"),depends:val("taskDependencies").split(",").map(x=>x.trim()).filter(Boolean),notes:val("taskNotes"),costActual:optional("taskActualCost"),daysOverride:optional("taskDays"),startConstraint:val("taskConstraint")||undefined};
 const next=core.putTask(active(),raw);core.schedule(next);projects[projects.findIndex(x=>x.id===activeId)]=next;store();render();editTask(id);
 }catch(e){error(e.message)}
}
function removeTask(){
 if(!editingId)return;const id=editingId;if(!confirm("Supprimer la tâche "+id+" ?"))return;
 try{const next=core.deleteTask(active(),id);projects[projects.findIndex(x=>x.id===activeId)]=next;store();resetEditor();render()}catch(e){error(e.message)}
}
function selectProject(id){if(!projects.some(p=>p.id===id))return;activeId=id;store();resetEditor();render()}
function openProjectDialog(mode){
 modalMode=mode;const p=active();error("","projectError");
 el("projectModalTitle").textContent=mode==="edit"?"Modifier le chantier":"Créer un nouveau chantier";
 el("projectName").value=mode==="edit"?p.title:"";el("projectClient").value=mode==="edit"?p.client:"";el("projectCity").value=mode==="edit"?p.city:"";
 el("projectStart").value=mode==="edit"?p.startDate:today();el("projectDialog").showModal();
}
function submitProject(event){
 event.preventDefault();error("","projectError");
 try{
 let raw;if(modalMode==="edit"){raw={...active(),title:val("projectName"),client:val("projectClient"),city:val("projectCity"),startDate:val("projectStart")}}
 else raw={schema:core.SCHEMA,id:newId("chantier"),title:val("projectName"),client:val("projectClient"),city:val("projectCity"),startDate:val("projectStart"),dataType:"user",notes:"",tasks:[]};
 const p=core.project(raw);core.schedule(p);if(modalMode==="edit")projects[projects.findIndex(x=>x.id===activeId)]=p;else{projects.push(p);activeId=p.id;resetEditor()}
 store();el("projectDialog").close();render();
 }catch(e){error(e.message,"projectError")}
}
function removeProject(){
 if(projects.length===1){alert("Crée un autre projet avant de supprimer le dernier dossier.");return}
 if(!confirm("Supprimer le chantier dans ce navigateur ? Pense à exporter son JSON."))return;
 projects=projects.filter(x=>x.id!==activeId);activeId=projects[0].id;resetEditor();store();render();
}
function exportJSON(){
 const p=active();saveFile("btp-"+p.id+".json",JSON.stringify({...p,exportedAt:new Date().toISOString(),warning:"Informations indicatives, non certifiées."},null,2),"application/json");
}
function exportCSV(){
 const rows=core.schedule(active()).tasks,head=["ID","Désignation","Phase","Unité","Quantité prévue","Quantité réalisée","Prix unitaire hypothétique","Rendement quotidien","Équipe","Début","Fin","Jours","Coût prévisionnel","Prédécesseurs"];
 const lines=[head.map(csv).join(";")];
 for(const t of rows)lines.push([t.id,t.name,t.group,t.unit,t.quantity,t.doneQuantity,t.unitCost,t.dailyRate,t.crew,t.start,t.endInclusive,t.durationDays,t.plannedCost,t.depends.join(",")].map(csv).join(";"));
 saveFile("btp-metrés-"+activeId+".csv","\uFEFF"+lines.join("\r\n"),"text/csv;charset=utf-8");
}
function importFile(file){
 if(!file)return;if(file.size>2000000){alert("Fichier limité à 2 Mo.");return}
 const reader=new FileReader();
 reader.onload=function(){
 try{
 const raw=JSON.parse(String(reader.result)),p=core.project({...raw,dataType:raw.dataType==="demonstration"?"demonstration":"imported"});core.schedule(p);
 if(projects.length>=100)throw Error("Limite de 100 projets atteinte");
 if(projects.some(x=>x.id===p.id)){if(!confirm("Cet identifiant existe déjà. Créer une copie ?"))return;p.id=newId("import");core.project(p)}
 projects.push(p);activeId=p.id;resetEditor();store();render();
 }catch(e){alert("Import refusé : "+e.message)}
 };
 reader.onerror=()=>alert("Fichier illisible");reader.readAsText(file);
}
function bind(){
 el("projectList").addEventListener("click",e=>{const b=e.target.closest("[data-project]");if(b)selectProject(b.dataset.project)});
 el("taskTable").addEventListener("click",e=>{const b=e.target.closest("[data-edit]");if(b)editTask(b.dataset.edit)});
 el("taskForm").addEventListener("submit",submitTask);
 el("addTask").onclick=()=>{resetEditor();el("taskName").focus()};
 el("cancelEdit").onclick=resetEditor;el("deleteTask").onclick=removeTask;
 el("newProject").onclick=()=>openProjectDialog("new");el("editProject").onclick=()=>openProjectDialog("edit");
 el("projectForm").addEventListener("submit",submitProject);
 el("closeDialog").onclick=()=>el("projectDialog").close();el("cancelDialog").onclick=()=>el("projectDialog").close();
 el("deleteProject").onclick=removeProject;el("exportProject").onclick=exportJSON;el("exportCSV").onclick=exportCSV;
 el("importProject").onclick=()=>el("fileImport").click();
 el("fileImport").onchange=e=>{importFile(e.target.files[0]);e.target.value=""};
 window.addEventListener("storage",e=>{if(e.key===STORE||e.key===ACTIVE){load();resetEditor();render()}});
}
load();resetEditor();bind();render();
})();