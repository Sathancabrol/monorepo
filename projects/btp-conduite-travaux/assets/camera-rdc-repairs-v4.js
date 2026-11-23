/* BTP Studio v4 — real user-triggered RDC webcam capture.
 * Saves an actual PNG to local archive and a date/project reference, never invents geolocation. */
(function(){
"use strict";
const KEY="btp_rdc_photos_v4",PROJECT="btp_project_active_v1",el=id=>document.getElementById(id);
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","<":"&lt;",'>':"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function project(){try{return localStorage.getItem(PROJECT)||"sans-dossier"}catch(e){return "sans-dossier"}}
function records(){try{const x=JSON.parse(localStorage.getItem(KEY)||"{}");return x&&typeof x==="object"?x:{}}catch(e){return {}}}
function render(){
 const list=el("btp-rdc-photo-list");if(!list)return;const rows=records()[project()]||[];
 list.innerHTML=rows.length?rows.slice(-12).reverse().map(r=>
 '<li style="padding:7px 0;border-bottom:1px solid #355b53"><strong>'+esc(r.filename)+'</strong> · '+esc(r.reportDate||"Date non saisie")+
 ' <small>archivé localement le '+esc(r.time?.slice(0,16)||"")+'</small></li>').join(""):'<li>Aucune capture réelle enregistrée dans ce dossier.</li>';
}
function status(message){const n=el("btp-rdc-photo-status");if(n)n.textContent=message}
function stopVideo(stream){if(stream?.getTracks)stream.getTracks().forEach(t=>t.stop())}
window.snapPhotoAndAttach=window.capturePhotoForRDC=async function(){
 const video=el("rdc-webcam-video"),archive=window.BTPArchiveV4;
 if(!archive||!video){alert("Capture impossible : stockage local ou lecteur caméra absent.");return}
 if(!video.srcObject||video.readyState<2||!video.videoWidth||!video.videoHeight){
  status("Aucune image webcam active. Autorise la caméra et lance la prévisualisation avant capture.");
  alert("Impossible de capturer : aucune image vidéo active. Aucun fichier n'a été enregistré.");return
 }
 try{
  const canvas=document.createElement("canvas");canvas.width=video.videoWidth;canvas.height=video.videoHeight;
  if(canvas.width>4096||canvas.height>4096)throw Error("Image hors dimensions autorisées");
  canvas.getContext("2d").drawImage(video,0,0,canvas.width,canvas.height);
  const blob=await new Promise((resolve,reject)=>canvas.toBlob(x=>x?resolve(x):reject(Error("PNG non créé")),"image/png"));
  const stamp=new Date().toISOString(),filename="RDC-photo-"+stamp.replace(/[:.]/g,"-")+".png";
  const file=new File([blob],filename,{type:"image/png",lastModified:Date.now()});
  const saved=await archive.addFile(file);
  const all=records(),key=project();if(!Array.isArray(all[key]))all[key]=[];
  all[key].push({archiveId:saved.id,filename:saved.name,time:stamp,reportDate:el("rdc-date")?.value||"",project:key});
  all[key]=all[key].slice(-1000);localStorage.setItem(KEY,JSON.stringify(all));
  render();status("Photo PNG réelle enregistrée dans les archives locales et référencée au RDC. Aucune géolocalisation n'a été effectuée.");
  stopVideo(video.srcObject);video.srcObject=null;
  if(typeof window.closeModal==="function")window.closeModal("rdc-camera-modal");
 }catch(e){status("Capture ou sauvegarde impossible : "+e.message);alert("Photo non conservée : "+e.message)}
};
function init(){
 const tab=el("tab-rdc");if(!tab||el("btp-rdc-photo-panel"))return;
 const section=document.createElement("section");section.id="btp-rdc-photo-panel";
 section.style.cssText="padding:14px;margin:0 0 16px;border:1px solid #6b908577;border-radius:12px;background:#142b2e;color:#dfeee5";
 section.innerHTML='<div style="color:#bce985;text-transform:uppercase;font-size:10px;letter-spacing:.13em;font-weight:850">Preuves photo — dossier local</div>'+
 '<h3 style="font-size:16px;margin:3px 0">Captures RDC réellement enregistrées</h3><p style="font-size:11px;color:#b5cbc1">Après autorisation caméra, utiliser « Photo Chantier » puis « Capturer ». PNG conservé dans Archives locales (IndexedDB). Aucun service externe, GPS ou horodatage certifié.</p>'+
 '<ul id="btp-rdc-photo-list" style="list-style:none;padding:0;font-size:11px"></ul><p id="btp-rdc-photo-status" role="status" style="font-size:11px;color:#bce985"></p>';
 tab.insertBefore(section,tab.firstChild);render();
 window.addEventListener("storage",e=>{if(e.key===KEY||e.key===PROJECT)render()});
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();