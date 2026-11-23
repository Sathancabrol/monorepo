/* BTP Studio — restores missing existing controls without faking external integrations. */
(function(){
"use strict";
const el=id=>document.getElementById(id);
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const briefings={
 aipr_gaz_elec:{title:"Réseaux enterrés : briefing préalable",points:["Examiner les récépissés DT/DICT et les plans applicables","Identifier les réseaux et la précision des données disponibles","Effectuer marquage-piquetage et adapter les méthodes d'approche","Définir arrêts et contrôles avant intervention à proximité des ouvrages","Stopper et alerter selon consignes en cas de doute ou d'endommagement"]},
 blindage_tranchee:{title:"Fouilles : stabilité et protections",points:["Évaluer sols, eau, voisinage et vibrations avant terrassement","Choisir blindage ou talutage avec dimensionnement compétent","Contrôler accès, circulation, charges en rive et évacuation","Inspecter protections après intempéries et modifications de la fouille","Ne jamais exposer les personnels à une tranchée non sécurisée"]},
 engins_pietons:{title:"Coactivité entre engins et piétons",points:["Définir plan de circulation et zones interdites","Vérifier angle mort, signaleur et communication","Séparer flux piétons et engins par protections adaptées","Contrôler marches arrière, visibilité et éclairage","Suspendre la manœuvre si un tiers pénètre dans l'emprise"]},
 elinguage_levage:{title:"Levage et manutentions",points:["Contrôler adéquation engin, portée, charge et CMU des accessoires","Vérifier contrôles et état des élingues","Désigner chef de manœuvre et signaux","Installer balisage, interdire le passage sous charge","Consigner une anomalie et interrompre l'opération si risque"]},
 enrobes_brulures:{title:"Enrobés chauds : risques thermiques",points:["Rappeler températures, exposition et EPI adaptés","Organiser circulation camions-finisseur-compacteurs","Éviter contact cutané avec enrobés et produits chauds","Prévoir premiers secours, eau et consignes accident","Surveiller fumées, fatigue thermique et conditions météo"]}
};
function safeOpen(id){if(typeof window.openModal==="function")window.openModal(id);else el(id)?.classList.add("active")}
window.openSafetyQuarterHourModal=function(){safeOpen("modal-safety-quarter-hour");window.loadSafetyBriefingContent()};
window.loadSafetyBriefingContent=function(){
 const key=el("safety-theme-select")?.value||"aipr_gaz_elec",b=briefings[key]||briefings.aipr_gaz_elec,node=el("safety-briefing-content");
 if(!node)return;
 node.innerHTML='<h3 style="font-size:16px;margin:3px 0 10px;color:#c3efab">'+esc(b.title)+'</h3>'+
 '<p style="font-size:12px;color:#e9c799">Fiche pédagogique non exhaustive : à adapter au chantier, aux prescriptions officielles et aux évaluations de risques. Ne vaut ni attestation ni visa.</p>'+
 '<ol style="padding-left:21px;font-size:13px;line-height:1.8">'+b.points.map(x=>'<li>'+esc(x)+'</li>').join("")+'</ol>'+
 '<p style="font-size:11px;color:#b8cec4">Faire dater et valider la formation / le quart d’heure sécurité par un responsable ; aucun point n’est réputé contrôlé automatiquement.</p>';
};
window.printSafetyBriefing=function(){
 window.loadSafetyBriefingContent();
 const selected=briefings[el("safety-theme-select")?.value]||briefings.aipr_gaz_elec;
 const win=window.open("","_blank");
 if(!win){alert("Impression bloquée par le navigateur. Autoriser les fenêtres surgissantes pour cette action.");return}
 const body='<h1>'+esc(selected.title)+'</h1><p>Support pédagogique à adapter — non certifié.</p><ol>'+selected.points.map(x=>'<li>'+esc(x)+'</li>').join("")+'</ol><p>Chantier : ____________________ Date : _____________ Animateur : ______________</p><p>Participants / émargement : _________________________</p><p>Mesures et commentaires : ________________________________________</p>';
 win.document.open();win.document.write('<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Fiche sécurité — BROUILLON</title><style>body{font:15px/1.6 system-ui;max-width:850px;padding:40px;margin:auto;color:#111}li{margin:12px 0}p{margin:18px 0}</style></head><body>'+body+'</body></html>');win.document.close();win.focus();win.print();
};
let playback=null,phase=0;
window.togglePlay4DSimulation=function(){
 const btn=el("btn-play-4d-sim");
 if(playback){clearInterval(playback);playback=null;if(btn)btn.textContent="▶ Simulation 4D";return}
 if(typeof window.setSimPhase!=="function"){alert("La simulation de phasage n'est pas disponible.");return}
 if(typeof window.setSimulatorViewMode==="function")window.setSimulatorViewMode("3d");
 phase=0;
 const advance=()=>{phase=(phase%6)+1;window.setSimPhase(phase);if(btn)btn.textContent="⏸ Pause 4D — phase "+phase+"/6"};
 advance();playback=setInterval(advance,1800);
};
document.addEventListener("visibilitychange",()=>{if(document.hidden&&playback)window.togglePlay4DSimulation()});
if(typeof window.renderWatchtowerMaps!=="function"&&typeof window.renderLeafletDICTNetworks==="function"){
 window.renderWatchtowerMaps=window.renderLeafletDICTNetworks;
}
window.sortBenchmarkTable=function(column){
 const body=el("benchmark-table-body");if(!body)return;
 const mapping={code:0,designation:1,unit:2,cost_internal:3,pv_internal:4,ref_dce_barbazan:5,ref_dce_aurouer:6,fntp_regional_avg:7,variance_pct:8};
 const col=mapping[column];if(col==null)return;
 const ascending=body.dataset.sortKey!==column||body.dataset.sortOrder!=="asc";
 const rows=Array.from(body.querySelectorAll("tr"));
 rows.sort((a,b)=>{
  const a0=a.children[col]?.textContent.trim()||"",b0=b.children[col]?.textContent.trim()||"";
  const num=s=>{const cleaned=s.replace(/[\s€%\u00a0]/g,"").replace(",",".");return /^[+-]?\d+(?:\.\d+)?$/.test(cleaned)?Number(cleaned):null};
  const n1=num(a0),n2=num(b0),cmp=n1!==null&&n2!==null?n1-n2:a0.localeCompare(b0,"fr",{numeric:true});
  return ascending?cmp:-cmp
 });
 body.replaceChildren(...rows);body.dataset.sortKey=column;body.dataset.sortOrder=ascending?"asc":"desc";
};
window.updateRolePreview=function(role){
 const target=el("role-preview")||el("account-role-preview");
 const text={direction:"Direction : indicateurs portefeuille, trésorerie et risques.",conduite:"Conduite de travaux : planning, ressources et opérations.",compagnon:"Compagnon : interface terrain et comptes rendus."}[role]||"Rôle à confirmer.";
 if(target)target.textContent=text;
};
let currentCamera=0,knownCameras=[];
window.updateCameraFeedView=async function(){
 const status=el("camera-source-hud"),video=el("rdc-webcam-video");
 if(!video||!navigator.mediaDevices?.getUserMedia){if(status)status.textContent="Caméra locale indisponible dans ce navigateur";return}
 try{
  // User interaction only: never open a camera without a click.
  const initial=video.srcObject||await navigator.mediaDevices.getUserMedia({video:true});
  if(!knownCameras.length)knownCameras=(await navigator.mediaDevices.enumerateDevices()).filter(d=>d.kind==="videoinput");
  if(knownCameras.length<2){video.srcObject=initial;if(status)status.textContent="Une seule caméra locale détectée — aucun autre angle disponible";return}
  currentCamera=(currentCamera+1)%knownCameras.length;
  const stream=await navigator.mediaDevices.getUserMedia({video:{deviceId:{exact:knownCameras[currentCamera].deviceId}}});
  if(video.srcObject&&video.srcObject!==stream)video.srcObject.getTracks().forEach(t=>t.stop());
  video.srcObject=stream;await video.play();
  if(status)status.textContent="WEBCAM LOCALE : "+(knownCameras[currentCamera].label||"caméra "+(currentCamera+1));
 }catch(e){if(status)status.textContent="Changement de caméra impossible : "+e.message}
};
function init(){if(el("safety-briefing-content"))window.loadSafetyBriefingContent()}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();