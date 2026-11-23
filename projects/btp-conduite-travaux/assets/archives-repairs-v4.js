/* BTP Studio v4 — local archival proof-of-concept using IndexedDB.
 * Saves original bytes without any upload. SHA-256 = integrity digest, NOT legal certification. */
(function(){
"use strict";
const DB="btp_local_archive_v4",VERSION=1,MAX_BYTES=20*1024*1024;
const $=id=>document.getElementById(id),esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function project(){try{return localStorage.getItem("btp_project_active_v1")||"sans-dossier"}catch(e){return "sans-dossier"}}
function openDb(){return new Promise((resolve,reject)=>{
 if(!window.indexedDB){reject(new Error("IndexedDB indisponible dans ce navigateur"));return}
 const request=indexedDB.open(DB,VERSION);
 request.onupgradeneeded=()=>{const db=request.result;if(!db.objectStoreNames.contains("meta"))db.createObjectStore("meta",{keyPath:"id"});if(!db.objectStoreNames.contains("files"))db.createObjectStore("files",{keyPath:"id"})};
 request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error||new Error("Ouverture impossible"));
})}
function requestResult(req){return new Promise((resolve,reject)=>{req.onsuccess=()=>resolve(req.result);req.onerror=()=>reject(req.error||new Error("Opération IndexedDB impossible"))})}
function txDone(tx){return new Promise((resolve,reject)=>{tx.oncomplete=()=>resolve();tx.onerror=()=>reject(tx.error||new Error("Transaction échouée"));tx.onabort=()=>reject(tx.error||new Error("Transaction annulée"))})}
async function metadata(){
 const db=await openDb();try{return await requestResult(db.transaction(["meta"],"readonly").objectStore("meta").getAll())}finally{db.close()}
}
function unique(){return typeof crypto!=="undefined"&&crypto.randomUUID?crypto.randomUUID():"archive-"+Date.now().toString(36)+"-"+Math.random().toString(36).slice(2)}
async function checksum(file){
 if(!crypto?.subtle?.digest)return null;
 const digest=await crypto.subtle.digest("SHA-256",await file.arrayBuffer());
 return Array.from(new Uint8Array(digest),b=>b.toString(16).padStart(2,"0")).join("")
}
async function addFile(file){
 if(!file)throw Error("Choisir un fichier");
 if(file.size===0||file.size>MAX_BYTES)throw Error("Fichier vide ou de plus de 20 Mo");
 const hash=await checksum(file).catch(()=>null),m={id:unique(),project:project(),name:file.name.slice(0,240),
  type:(file.type||"application/octet-stream").slice(0,100),size:file.size,sha256:hash,addedAt:new Date().toISOString(),source:"fichier choisi localement"};
 const db=await openDb();try{
  const tx=db.transaction(["meta","files"],"readwrite"),done=txDone(tx);
  tx.objectStore("meta").put(m);tx.objectStore("files").put({id:m.id,blob:file});
  await done;return m;
 }finally{db.close()}
}
async function download(id){
 const db=await openDb();try{
 const r=await requestResult(db.transaction(["files"],"readonly").objectStore("files").get(id));
 if(!r?.blob)throw Error("Fichier introuvable");
 const metas=await requestResult(db.transaction(["meta"],"readonly").objectStore("meta").get(id));
 const url=URL.createObjectURL(r.blob),a=document.createElement("a");a.href=url;a.download=metas?.name||"document";
 document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),3000);
 }finally{db.close()}
}
async function remove(id){
 const db=await openDb();try{const tx=db.transaction(["meta","files"],"readwrite"),done=txDone(tx);
 tx.objectStore("meta").delete(id);tx.objectStore("files").delete(id);await done;
 }finally{db.close()}
}
async function render(){
 const tbody=$("btp-v4-archive-body");if(!tbody)return;const status=$("btp-v4-archive-status");
 try{
  const entries=(await metadata()).filter(x=>x.project===project()).sort((a,b)=>b.addedAt.localeCompare(a.addedAt));
  tbody.innerHTML=entries.map(m=>'<tr><td>'+esc(m.name)+'</td><td>'+Number(m.size/1024).toLocaleString("fr-FR",{maximumFractionDigits:1})+' Ko</td><td>'+esc(m.addedAt.slice(0,16).replace("T"," "))+'</td>'+
  '<td><code style="font-size:10px">'+esc((m.sha256||"Non calculé").slice(0,16))+'</code></td><td><button class="btn btn-secondary" data-archive-get="'+esc(m.id)+'" type="button">Récupérer</button> <button class="btn btn-secondary" data-archive-del="'+esc(m.id)+'" type="button">Supprimer</button></td></tr>').join("")||
  '<tr><td colspan="5" style="text-align:center;padding:14px;color:#aec2bc">Aucune pièce enregistrée localement pour ce dossier.</td></tr>';
  if(status)status.textContent=entries.length+" document(s) conservé(s) dans ce navigateur. Pense à exporter des copies : le stockage du navigateur peut être effacé.";
 }catch(e){tbody.innerHTML="";if(status)status.textContent="Archives indisponibles : "+e.message}
}
window.BTPArchiveV4=Object.freeze({addFile:addFile,list:metadata,render:render});
window.openArchiveUploaderV4=function(){const input=$("btp-v4-archive-input");if(input)input.click();else alert("Outil d'archive non chargé");};
function init(){
 const tab=$("tab-archives");if(!tab||$("btp-v4-archive"))return;
 const section=document.createElement("section");section.id="btp-v4-archive";
 section.style.cssText="margin:0 0 17px;background:#15292d;border:1px solid #61847e88;border-radius:13px;padding:16px;color:#e3efe9";
 section.innerHTML='<div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:center"><div><div style="text-transform:uppercase;letter-spacing:.13em;color:#bce985;font-size:10px;font-weight:850">Archives locales · IndexedDB</div><h3 style="font-size:17px;margin:4px 0">Conserver de vraies pièces dans le navigateur</h3><p style="font-size:11px;color:#afc7bd">Aucun téléversement externe. Empreinte SHA-256 facultative — non équivalente à une signature ou un scellement légal.</p></div>'+
 '<div><button type="button" id="btp-v4-archive-add" class="btn btn-primary">Ajouter une pièce</button><input id="btp-v4-archive-input" type="file" hidden></div></div>'+
 '<div style="overflow:auto;margin-top:12px"><table style="width:100%;font-size:11px"><thead><tr><th>Fichier</th><th>Taille</th><th>Ajout UTC</th><th>SHA-256 (extrait)</th><th>Actions</th></tr></thead><tbody id="btp-v4-archive-body"></tbody></table></div>'+
 '<p id="btp-v4-archive-status" role="status" style="font-size:11px;color:#c0d5ca"></p>';
 tab.insertBefore(section,tab.firstChild);
 $("btp-v4-archive-add").addEventListener("click",()=>window.openArchiveUploaderV4());
 $("btp-v4-archive-input").addEventListener("change",async e=>{
  const file=e.target.files?.[0];e.target.value="";if(!file)return;
  const s=$("btp-v4-archive-status");s.textContent="Lecture et conservation locale du fichier…";
  try{await addFile(file);await render()}catch(err){s.textContent="Échec de sauvegarde : "+err.message}
 });
 $("btp-v4-archive-body").addEventListener("click",async e=>{
  const get=e.target.closest("[data-archive-get]"),del=e.target.closest("[data-archive-del]");
  if(get){try{await download(get.dataset.archiveGet)}catch(err){$("btp-v4-archive-status").textContent=err.message}}
  if(del&&confirm("Supprimer définitivement cette pièce du stockage local de ce navigateur ?")){
   try{await remove(del.dataset.archiveDel);await render()}catch(err){$("btp-v4-archive-status").textContent=err.message}
  }
 });
 window.addEventListener("storage",e=>{if(e.key==="btp_project_active_v1")render()});
 render();
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();