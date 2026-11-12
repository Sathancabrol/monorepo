import { clipDuration, storyboardDuration, locateClip, moveClip, validateClip, referencedAssetIds, trimVideoClip, splitStoryboardAt } from './storyboard.js';
import { migrateV03Project } from './v03-migration.js';
import { parseSRT, formatSRT, exportMeetingNotes } from './meeting-utils.js';
import { openMediaDB, putMedia, getMedia, listMedia, exportPortableAssets, importPortableAsset, mediaLayerUsable } from './media-store.js';
const $=id=>document.getElementById(id);
const C=$('stage'),ctx=C.getContext('2d');
const spaces=[
  ['LIVE','◉','Réalisation et enregistrement en direct'],
  ['EDIT','▤','Montage et chronologie'],
  ['GENERATE','✦','Génération image et vidéo locale'],
  ['XR','⬡','Motion capture, objets et avatars'],
  ['AUDIO','♫','Mixage et analyse audio'],
  ['MEETING','◷','Réunions, sous-titres et concepts'],
  ['CAPTURE','◎','Capture spatiale sans LiDAR'],
  ['CINEMA','▣','Caméras, lumière et VFX'],
  ['AUTOMATE','⌘','Workflows et orchestration Chronos'],
  ['GRAPHICS','◇','Infographies et animations'],
  ['LIBRARY','▦','Médias et modèles locaux'],
  ['CONTROL','⚙','État des moteurs et matériel']
];
const newId=()=>Math.random().toString(36).slice(2,11);
const baseScenes=()=>[{id:newId(),name:'Scène principale',layers:[{id:newId(),type:'text',name:'Titre',value:'OLYMPUS STUDIO',x:.12,y:.43,w:.74,h:.18,size:66,color:'#ffffff',visible:true},{id:newId(),type:'rect',name:'Accent',x:.12,y:.64,w:.24,h:.015,color:'#27c8c0',visible:true}]},{id:newId(),name:'Présentation',layers:[{id:newId(),type:'text',name:'Présentation',value:'Réunion augmentée',x:.09,y:.12,w:.82,h:.16,size:55,color:'#ffffff',visible:true}]}];
const state={space:'LIVE',projectName:'Production sans titre',scenes:baseScenes(),activeScene:null,selected:null,transcript:[],assets:[],clips:[],editTime:0,editPlaying:false,editLast:0,captionsVisible:false,legacyV03:null,recording:false};
const runtime=new Map();let webcamStream=null;let webcamVideo=null;let microphoneStream=null;let screenStream=null;let screenVideo=null;let recorder=null;let chunks=[];let recStarted=0;let lastCanvas=0;let obsOutput=false;let lastObsFrame=0;let sendingObs=false;let lastComfyJob=null;
state.activeScene=state.scenes[0].id;
const dbReady = openMediaDB().catch(() => null);
const editMedia = new Map();let editorRecorder=null;
const createdMediaURLs = new Set();
function releaseMediaURLs(){for(const url of createdMediaURLs)URL.revokeObjectURL(url);createdMediaURLs.clear();}
function localMediaURL(blob){const url=URL.createObjectURL(blob);createdMediaURLs.add(url);return url;}
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const scene=()=>state.scenes.find(s=>s.id===state.activeScene)||state.scenes[0];
const selected=()=>scene().layers.find(l=>l.id===state.selected);
function status(t){$('status').textContent=t;}
function dl(name,blob){const a=document.createElement('a');const u=URL.createObjectURL(blob);a.href=u;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),10000);}
function addLayer(layer){layer.id=newId();layer.visible=true;scene().layers.push(layer);state.selected=layer.id;sync();return layer;}
function setSpace(key){if(key!=='EDIT'){state.editPlaying=false;if(editorRecorder?.state==='recording'){editorRecorder.stop();status('Export storyboard interrompu par changement d’espace');}}state.space=key;const item=spaces.find(s=>s[0]===key);$('spaceTitle').textContent=item[0];$('spaceDesc').textContent=item[2];document.querySelectorAll('[data-space]').forEach(b=>b.classList.toggle('active',b.dataset.space===key));panel();sync();}
function makeNav(){const root=$('navItems');spaces.forEach(([key,icon,label])=>{const b=document.createElement('button');b.dataset.space=key;b.innerHTML='<b aria-hidden="true">'+esc(icon)+'</b><span>'+key+'</span>';b.title=label;b.onclick=()=>setSpace(key);root.append(b);});}
function sync(){
 $('stageLabel').textContent=scene().name+' · 1280 × 720';
 const list=$('scenes');list.innerHTML='';
 state.scenes.forEach(s=>{
  const d=document.createElement('div');d.className='scene'+(s.id===state.activeScene?' active':'');
  const n=document.createElement('span');n.className='name';n.textContent=s.name;n.title='Activer cette scène';n.onclick=()=>{state.activeScene=s.id;state.selected=null;sync();};
  const rename=document.createElement('button');rename.textContent='✎';rename.title='Renommer';rename.onclick=()=>{const v=prompt('Nom de la scène',s.name);if(v&&v.trim()){s.name=v.trim();sync();}};
  d.append(n,rename);list.append(d);
 });
 const layers=$('layers');layers.innerHTML='';
 [...scene().layers].reverse().forEach(l=>{
  const d=document.createElement('div');d.className='layer-row'+(l.id===state.selected?' active':'');
  const toggle=document.createElement('input');toggle.type='checkbox';toggle.className='check';toggle.checked=l.visible;toggle.title='Afficher ou masquer';toggle.onchange=()=>{l.visible=toggle.checked;};
  const name=document.createElement('span');name.className='name';name.textContent=l.name;name.title=l.type;name.onclick=()=>{state.selected=l.id;sync();};
  const rm=document.createElement('button');rm.textContent='×';rm.title='Supprimer';rm.onclick=()=>{scene().layers=scene().layers.filter(x=>x!==l);runtime.delete(l.id);if(state.selected===l.id)state.selected=null;sync();};
  d.append(toggle,name,rm);layers.append(d);
 });
 const box=$('properties');box.innerHTML='';const l=selected();
 if(!l){box.className='muted';box.textContent='Sélectionne un calque dans la liste.';}else{
  box.className='';['name','x','y','w','h','color'].forEach(prop=>{
   if(!(prop in l))return;
   const div=document.createElement('div');div.className='field';
   const label=document.createElement('label');label.textContent=({name:'Nom',x:'Position X (0–1)',y:'Position Y (0–1)',w:'Largeur (0–1)',h:'Hauteur (0–1)',color:'Couleur'})[prop]||prop;
   const input=document.createElement('input');input.value=l[prop];input.type=['x','y','w','h'].includes(prop)?'number':prop==='color'?'color':'text';if(input.type==='number'){input.min='0';input.max='1';input.step='.01';}
   input.onchange=()=>{l[prop]=input.type==='number'?Math.min(1,Math.max(0,Number(input.value))):input.value;sync();};div.append(label,input);box.append(div);
  });
  if(l.type==='text'){const div=document.createElement('div');div.className='field';const label=document.createElement('label');label.textContent='Texte';const input=document.createElement('input');input.value=l.value;input.onchange=()=>{l.value=input.value;};div.append(label,input);box.append(div);}
  const top=document.createElement('button');top.textContent='Monter le calque';top.onclick=()=>{const a=scene().layers,i=a.indexOf(l);if(i<a.length-1){[a[i],a[i+1]]=[a[i+1],a[i]];sync();}};box.append(top);
 }
 renderTimeline();
}
function renderTimeline(){
 const el=$('timeline');el.innerHTML='';scene().layers.forEach(l=>{const tr=document.createElement('div');tr.className='track';const name=document.createElement('b');name.textContent=l.name;const bar=document.createElement('div');bar.className='bar';bar.style.opacity=l.visible?1:.22;bar.title='Calque de composition — pas encore un clip montable';tr.append(name,bar);el.append(tr);});
}
async function loadEditAsset(assetId){
 if(editMedia.has(assetId))return editMedia.get(assetId);
 const db=await dbReady;
 let record=db?await getMedia(db,assetId):null;
 if(!record){
  const available=runtime.get(assetId);
  if(available){editMedia.set(assetId,available);return available;}
  return null;
 }
 const url=localMediaURL(record.blob);
 let element;
 if(record.type.startsWith('image/')){
  element=new Image();element.src=url;
  await new Promise(resolve=>{element.onload=resolve;element.onerror=resolve;});
 }else if(record.type.startsWith('video/')){
  element=document.createElement('video');element.src=url;element.muted=true;element.preload='auto';element.playsInline=true;
 }else return null;
 editMedia.set(assetId,element);return element;
}
function editClock(seconds){
 const total=Math.max(0,Math.floor(seconds));
 return String(Math.floor(total/60)).padStart(2,'0')+':'+String(total%60).padStart(2,'0');
}
function drawEditor(now){
 const canvas=$('editPreview');if(!canvas){state.editLast=now;return;}
 const context=canvas.getContext('2d'), total=storyboardDuration(state.clips);
 if(state.editPlaying && state.editLast)state.editTime+=(now-state.editLast)/1000;
 state.editLast=now;
 if(total>0&&state.editTime>=total){state.editTime=total;state.editPlaying=false;if(editorRecorder?.state==='recording')editorRecorder.stop();}
 context.fillStyle='#081421';context.fillRect(0,0,canvas.width,canvas.height);
 const found=locateClip(state.clips,Math.min(state.editTime,Math.max(0,total-0.0001)));
 if(found){
  const source=editMedia.get(found.clip.assetId);
  if(source){
   try{
    if(found.clip.kind==='video'){
     const target=found.sourceTime;
     if(Math.abs(source.currentTime-target)>0.28 && Number.isFinite(target))source.currentTime=target;
     if(state.editPlaying&&source.paused)source.play().catch(()=>{});
     if(!state.editPlaying&&!source.paused)source.pause();
     if(source.readyState>=2)context.drawImage(source,0,0,canvas.width,canvas.height);
    }else if(source.complete&&source.naturalWidth)context.drawImage(source,0,0,canvas.width,canvas.height);
   }catch{}
  }
  if(found.clip.title){context.fillStyle='rgba(0,0,0,.65)';context.fillRect(20,canvas.height-95,canvas.width-40,65);context.font='bold 38px Segoe UI,Arial';context.fillStyle='#fff';context.fillText(found.clip.title,34,canvas.height-55,canvas.width-80);}
 }else{
  context.fillStyle='#8ca4c0';context.textAlign='center';context.font='27px Segoe UI,Arial';context.fillText('Ajouter un média à la timeline',canvas.width/2,canvas.height/2);context.textAlign='left';
 }
 const seek=$('editSeek');if(seek&&document.activeElement!==seek){seek.max=String(Math.max(0.1,total));seek.value=String(Math.min(state.editTime,total));}
 const clock=$('editClock');if(clock)clock.textContent=editClock(state.editTime)+' / '+editClock(total);
 const play=$('editPlay');if(play)play.textContent=state.editPlaying?'Pause':'Lecture';
}
function exportEditorWebM(){
 const canvas=$('editPreview'),total=storyboardDuration(state.clips);
 if(!canvas||!total)return status('Aucun clip à exporter');
 if(total>120)return status('Export de démonstration limité à 120 secondes');
 if(editorRecorder?.state==='recording')return status('Un export est déjà en cours');
 try{
  state.editTime=0;state.editLast=0;state.editPlaying=true;
  const stream=canvas.captureStream(24);
  const mime=['video/webm;codecs=vp8','video/webm'].find(x=>MediaRecorder.isTypeSupported(x));
  editorRecorder=new MediaRecorder(stream,mime?{mimeType:mime}:undefined);
  const chunks=[];
  editorRecorder.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};
  editorRecorder.onstop=()=>{
   stream.getTracks().forEach(t=>t.stop());state.editPlaying=false;
   dl('olympus-storyboard-'+Date.now()+'.webm',new Blob(chunks,{type:editorRecorder.mimeType||'video/webm'}));
   status('Storyboard WebM exporté sans audio — rendu en temps réel');
  };
  editorRecorder.start(1000);
  status('Export storyboard en cours — garder EDIT visible (vidéo seule)');
 }catch(e){state.editPlaying=false;status('Export storyboard impossible : '+e.message);}
}
function draw(){
 ctx.fillStyle='#0b1725';ctx.fillRect(0,0,C.width,C.height);
 const grd=ctx.createLinearGradient(0,0,C.width,C.height);grd.addColorStop(0,'#0b1725');grd.addColorStop(1,'#153d55');ctx.fillStyle=grd;ctx.fillRect(0,0,C.width,C.height);
 ctx.strokeStyle='rgba(255,255,255,.055)';ctx.lineWidth=1;for(let i=0;i<C.width;i+=80){ctx.beginPath();ctx.moveTo(i,0);ctx.lineTo(i,C.height);ctx.stroke();}for(let i=0;i<C.height;i+=80){ctx.beginPath();ctx.moveTo(0,i);ctx.lineTo(C.width,i);ctx.stroke();}
 scene().layers.forEach(l=>{if(!l.visible)return;const x=l.x*C.width,y=l.y*C.height,w=l.w*C.width,h=l.h*C.height;
  try{
   if(l.type==='rect'){ctx.fillStyle=l.color||'#23cfc2';ctx.fillRect(x,y,w,h);}
   else if(l.type==='text'){ctx.font='600 '+(l.size||44)+'px Segoe UI,Arial,sans-serif';ctx.fillStyle=l.color||'#fff';ctx.textBaseline='middle';ctx.fillText(l.value||'',x,y+h/2,w);}
   else if(l.type==='image'||l.type==='video'||l.type==='webcam'||l.type==='screen'){const media=l.type==='webcam'?webcamVideo:l.type==='screen'?screenVideo:runtime.get(l.id);if(media&&((l.type==='image'&&media.complete)||(l.type!=='image'&&media.readyState>=2)))ctx.drawImage(media,x,y,w,h);else {ctx.strokeStyle='#7894af';ctx.strokeRect(x,y,w,h);ctx.fillStyle='#a9bdcf';ctx.font='22px Segoe UI';ctx.fillText(l.name+' · fichier à relier',x+12,y+35,w-24);}}
  }catch{}
  if(l.id===state.selected){ctx.strokeStyle='#42e8df';ctx.lineWidth=3;ctx.strokeRect(x,y,w,h);}
 });
 const last=state.transcript[state.transcript.length-1];if(last&&state.captionsVisible===true){ctx.fillStyle='rgba(0,0,0,.76)';ctx.fillRect(140,630,1000,57);ctx.fillStyle='#fff';ctx.font='26px Segoe UI';ctx.textAlign='center';ctx.fillText((last.speaker+': '+last.text).slice(0,85),640,666,950);ctx.textAlign='left';}
}
function loop(t){if(t-lastCanvas>=32){draw();drawEditor(t);lastCanvas=t;}if(obsOutput&&t-lastObsFrame>=150&&!sendingObs){lastObsFrame=t;sendingObs=true;C.toBlob(async b=>{try{if(b)await fetch('/api/frame',{method:'POST',headers:{'Content-Type':'image/jpeg'},body:b});}catch(e){status('Sortie OBS indisponible : '+e.message);}finally{sendingObs=false;}},'image/jpeg',.66);}requestAnimationFrame(loop);}
function projectPayload(){
 const safe=state.scenes.map(s=>({id:s.id,name:s.name,layers:s.layers.map(l=>({...l,source:undefined}))}));
 return {format:'olympus-studio-project',schema:2,projectName:state.projectName,activeScene:state.activeScene,scenes:safe,transcript:state.transcript,clips:state.clips,legacyV03:state.legacyV03,warning:'Les références média utilisent IndexedDB pour cette origine du navigateur; utilise Portable pour changer de PC.'};
}
function saveProject(){
 dl('olympus-project-'+Date.now()+'.json',new Blob([JSON.stringify(projectPayload(),null,2)],{type:'application/json'}));
 status('Projet JSON exporté — les médias restent dans le coffre local du navigateur');
}
async function savePortableProject(){
 const button=$('btnPortable');button.disabled=true;
 try{
  const db=await dbReady;
  const refs=referencedAssetIds(state.scenes,state.clips);
  if(refs.length&&!db)throw Error('IndexedDB indisponible; impossible de créer une archive complète');
  const records=[];
  for(const id of refs){const record=await getMedia(db,id);if(!record)throw Error('Média absent du coffre : '+id);records.push(record);}
  const embeddedAssets=await exportPortableAssets(records);
  const payload={...projectPayload(),portable:true,embeddedAssets};
  dl('olympus-portable-'+Date.now()+'.json',new Blob([JSON.stringify(payload)],{type:'application/json'}));
  status('Projet portable exporté : '+embeddedAssets.length+' média(s) intégré(s)');
 }catch(e){status('Export portable impossible : '+e.message);}
 finally{button.disabled=false;}
}
async function restoreLayerMedia(){
 const db=await dbReady;if(!db)return;
 const references=new Map();
 for(const sc of state.scenes)for(const layer of sc.layers)
  if(layer.type==='image'||layer.type==='video')references.set(layer.id,layer);
 for(const [id,layer] of references){
  try{
   const record=await getMedia(db,layer.assetId||id);
   if(!mediaLayerUsable(record,layer))continue;
   const url=localMediaURL(record.blob);
   let media;
   if(layer.type==='image'){media=new Image();media.src=url;await new Promise(resolve=>{media.onload=resolve;media.onerror=resolve;});}
   else {media=document.createElement('video');media.src=url;media.loop=true;media.muted=true;media.playsInline=true;media.autoplay=true;media.play().catch(()=>{});}
   runtime.set(id,media);
  }catch(e){status('Reliaison média : '+e.message);}
 }
}
async function initMediaLibrary(){
 try{
  const db=await dbReady;
  if(!db){status('IndexedDB indisponible; médias non persistants');return;}
  const records=await listMedia(db);
  state.assets=records.map(r=>({id:r.id,name:r.name,type:r.type,size:r.size}));
  await restoreLayerMedia();sync();panel();
 }catch(e){status('Coffre de médias indisponible : '+e.message);}
}
async function loadProject(file){
 try{let data=JSON.parse(await file.text());if(data.app==='OLYMPUS Studio'&&String(data.version)==='0.3')data=migrateV03Project(data);if(data.format!=='olympus-studio-project'||!Array.isArray(data.scenes)||!data.scenes.length)throw Error('Format incompatible');
  const db=await dbReady;
  if(Array.isArray(data.embeddedAssets)&&data.embeddedAssets.length){
   if(!db)throw Error('IndexedDB requis pour importer les médias portables');
   const decoded=data.embeddedAssets.map(asset=>importPortableAsset(asset));
   const total=decoded.reduce((sum,r)=>sum+r.size,0);
   if(total>45*1024*1024)throw Error('Import portable trop volumineux');
   for(const record of decoded)await putMedia(db,record);
  }
  state.projectName=String(data.projectName||'Projet');$('projectName').value=state.projectName;
  state.scenes=data.scenes.filter(s=>Array.isArray(s.layers)).map(s=>({id:s.id||newId(),name:String(s.name||'Scène'),layers:s.layers.map(l=>({...l,id:l.id||newId(),visible:l.visible!==false}))}));
  if(!state.scenes.length)throw Error('Aucune scène valide');
  state.activeScene=state.scenes.find(s=>s.id===data.activeScene)?.id||state.scenes[0].id;state.selected=null;state.transcript=Array.isArray(data.transcript)?data.transcript:[];state.captionsVisible=false;state.legacyV03=data.legacyV03||null;
  const legacyClips=data.legacyV03?.edit?.clips;
  const candidates=Array.isArray(data.clips)?data.clips:Array.isArray(legacyClips)?legacyClips:[];
  state.clips=candidates.slice(0,1000).flatMap(c=>{try{return [validateClip(c)];}catch{return [];}});
  state.editTime=0;state.editPlaying=false;editMedia.clear();
  runtime.clear();releaseMediaURLs();await initMediaLibrary();sync();panel();
  status('Projet chargé : calques reliés aux médias IndexedDB existants ('+(data.embeddedAssets?.length||0)+' intégrés)');
 }catch(e){status('Échec import : '+e.message);}
}
async function addFiles(files){
 const db=await dbReady;
 let imported=0,failures=0;
 for(const file of files){
  const type=file.type.startsWith('image/')?'image':file.type.startsWith('video/')?'video':null;
  if(!type)continue;
  const layer=addLayer({type,name:file.name,sourceName:file.name,x:.15,y:.15,w:.7,h:.65});
  if(db){try{await putMedia(db,{id:layer.id,name:file.name,type:file.type,blob:file});}catch{failures++;}}
  else failures++;
  const url=localMediaURL(file);let media;
  if(type==='image'){media=new Image();media.src=url;await new Promise(resolve=>{media.onload=resolve;media.onerror=resolve;});}
  else{media=document.createElement('video');media.src=url;media.muted=true;media.loop=true;media.playsInline=true;media.autoplay=true;media.play().catch(()=>{});}
  runtime.set(layer.id,media);
  state.assets.push({name:file.name,type:file.type,id:layer.id,size:file.size});
  imported++;
 }
 sync();panel();status(imported+' média(s) importé(s)'+(failures?' · '+failures+' sans sauvegarde persistante':' · sauvegardés dans IndexedDB'));
}
async function camera(){
 if(webcamStream){webcamStream.getTracks().forEach(t=>t.stop());webcamStream=null;webcamVideo=null;status('Webcam arrêtée');return;}
 try{webcamStream=await navigator.mediaDevices.getUserMedia({video:{width:1280,height:720},audio:false});webcamVideo=document.createElement('video');webcamVideo.srcObject=webcamStream;webcamVideo.muted=true;webcamVideo.playsInline=true;await webcamVideo.play();addLayer({type:'webcam',name:'Webcam locale',x:.15,y:.1,w:.7,h:.75});status('Webcam autorisée par le navigateur');}catch(e){status('Webcam indisponible ou refusée : '+e.message);}
}
async function microphone(){
 if(microphoneStream){microphoneStream.getTracks().forEach(track=>track.stop());microphoneStream=null;$('btnMicrophone').textContent='+ Micro';status('Microphone arrêté');return;}
 try{
  microphoneStream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true},video:false});
  $('btnMicrophone').textContent='■ Micro';status('Microphone autorisé; sera inclus au prochain enregistrement WebM');
 }catch(e){status('Microphone indisponible ou refusé : '+e.message);}
}
async function captureScreen(){
 if(screenStream){screenStream.getTracks().forEach(t=>t.stop());screenStream=null;screenVideo=null;$('btnScreen').textContent='+ Écran';status('Partage d’écran arrêté');return;}
 try{
  if(!navigator.mediaDevices?.getDisplayMedia)throw Error('Partage d’écran non pris en charge par ce navigateur');
  screenStream=await navigator.mediaDevices.getDisplayMedia({video:{frameRate:30},audio:true});
  screenVideo=document.createElement('video');screenVideo.srcObject=screenStream;screenVideo.muted=true;screenVideo.playsInline=true;
  await screenVideo.play();
  const track=screenStream.getVideoTracks()[0];
  track?.addEventListener('ended',()=>{screenStream=null;screenVideo=null;$('btnScreen').textContent='+ Écran';status('Partage d’écran terminé');},{once:true});
  addLayer({type:'screen',name:'Écran / fenêtre capturée',x:.1,y:.1,w:.8,h:.8});
  $('btnScreen').textContent='■ Écran';
  status('Partage d’écran actif; son de l’onglet inclus uniquement si le navigateur le fournit');
 }catch(e){if(screenStream)screenStream.getTracks().forEach(t=>t.stop());screenStream=null;screenVideo=null;status('Capture écran impossible : '+e.message);}
}
function png(){C.toBlob(b=>{if(b)dl('olympus-'+Date.now()+'.png',b)},'image/png');}
function record(){const button=$('btnRecord');
 if(recorder&&recorder.state==='recording'){recorder.stop();return;}
 let stream=null;let mixContext=null;
 try{
  stream=C.captureStream(24);
  const sources=[microphoneStream,screenStream].filter(Boolean).flatMap(s=>s.getAudioTracks()).filter(t=>t.readyState==='live');
  if(sources.length===1)stream.addTrack(sources[0].clone());
  if(sources.length>1){
   const Context=window.AudioContext||window.webkitAudioContext;
   if(!Context)throw Error('Mixage audio non pris en charge');
   mixContext=new Context();const target=mixContext.createMediaStreamDestination();
   for(const track of sources)mixContext.createMediaStreamSource(new MediaStream([track])).connect(target);
   stream.addTrack(target.stream.getAudioTracks()[0].clone());
  }
  const withAudio=stream.getAudioTracks().length>0;
  const formats=withAudio?['video/webm;codecs=vp9,opus','video/webm;codecs=vp8,opus','video/webm']:['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm'];
  const mime=formats.find(t=>MediaRecorder.isTypeSupported(t));
  recorder=new MediaRecorder(stream,mime?{mimeType:mime}:undefined);chunks=[];recStarted=Date.now();
  recorder.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};
  recorder.onstop=()=>{const blob=new Blob(chunks,{type:recorder.mimeType||'video/webm'});dl('olympus-live-'+Date.now()+'.webm',blob);stream.getTracks().forEach(t=>t.stop());mixContext?.close();button.textContent='● WebM';state.recording=false;status(withAudio?'WebM téléchargé (vidéo et audio autorisé)':'WebM téléchargé (vidéo seule; activer Micro ou partage audio)');};
  recorder.start(1000);state.recording=true;button.textContent='■ Arrêter';status(withAudio?'Enregistrement WebM vidéo + audio autorisé':'Enregistrement WebM vidéo seule');
 }catch(e){stream?.getTracks().forEach(t=>t.stop());mixContext?.close();status('Enregistrement impossible : '+e.message);}
}
function srtTime(s){const ms=Math.max(0,Math.round(s*1000)),h=Math.floor(ms/3600000),m=Math.floor(ms%3600000/60000),sec=Math.floor(ms%60000/1000),r=ms%1000;return [h,m,sec].map(n=>String(n).padStart(2,'0')).join(':')+','+String(r).padStart(3,'0');}
function downloadSRT(){dl('reunion.srt',new Blob([formatSRT(state.transcript)],{type:'text/plain'}));}
async function health(){try{const r=await fetch('/api/health');const x=await r.json();$('engineStatus').textContent='OBS '+(x.services.obs.reachable?'visible':'absent')+' · ComfyUI '+(x.services.comfyui.reachable?'visible':'absent')+' · XR non connecté';status('Diagnostic local effectué — visible ne signifie pas connecté');return x;}catch(e){status('Diagnostic non disponible : '+e.message);return null;}}
const card=(name,detail)=>'<div class="mini-card"><h3>'+esc(name)+'</h3><p>'+esc(detail)+'</p></div>';
function panel(){
 const el=$('workspacePanel');el.innerHTML='';const h=document.createElement('h2');h.textContent=state.space+' · atelier';el.append(h);
 const wrap=document.createElement('div');wrap.className='actions';el.append(wrap);
 if(state.space==='LIVE'){const info=document.createElement('p');info.className='notice';info.textContent='La composition Canvas fonctionne localement. La régie OBS WebSocket se trouve à droite (à connecter à OBS installé). La sortie MJPEG reste vidéo seule; l’audio multipiste OBS natif reste externe.';el.append(info);const cards=document.createElement('div');cards.className='cards';cards.innerHTML=card('Écran / webcams','Webcam, écran et microphone disponibles sur autorisation, depuis la barre d’outils.')+card('OBS externe','Source navigateur sur /obs après activation du bouton « Sortie OBS », sans audio; vidéo MJPEG limitée par la machine.')+card('Enregistrement','WebM du Canvas avec piste microphone ou audio partagé si disponible; PNG du plan courant. OBS reste externe.');el.append(cards);}
 else if(state.space==='EDIT'){
  const header=document.createElement('p');header.className='notice';
  header.textContent='Montage séquentiel non destructif : points IN/OUT, coupe au curseur, titres, réordonnancement et export WebM muet. Audio et transitions multipistes à intégrer.';
  el.append(header);
  const preview=document.createElement('canvas');preview.id='editPreview';preview.width=1280;preview.height=720;preview.style.width='100%';preview.style.maxHeight='360px';preview.style.background='#071422';preview.style.borderRadius='8px';el.append(preview);
  const controls=document.createElement('div');controls.className='actions';el.append(controls);
  const play=document.createElement('button');play.id='editPlay';play.textContent=state.editPlaying?'Pause':'Lecture';
  play.onclick=()=>{if(!state.clips.length)return status('Ajouter un clip');if(state.editTime>=storyboardDuration(state.clips))state.editTime=0;state.editPlaying=!state.editPlaying;state.editLast=0;};
  const seek=document.createElement('input');seek.id='editSeek';seek.type='range';seek.min='0';seek.max=String(Math.max(0.1,storyboardDuration(state.clips)));seek.step='.05';seek.value=String(state.editTime);seek.style.flex='1';
  seek.oninput=()=>{state.editTime=Number(seek.value);state.editPlaying=false;state.editLast=0;};
  const clock=document.createElement('span');clock.id='editClock';clock.className='muted';clock.textContent=editClock(state.editTime);
  const exportButton=document.createElement('button');exportButton.textContent='Exporter WebM (sans audio)';exportButton.onclick=exportEditorWebM;
  const cutButton=document.createElement('button');cutButton.textContent='Diviser au curseur';
  cutButton.title='Scinder une vidéo en deux segments à la position courante de la timeline';
  cutButton.onclick=()=>{
   if(editorRecorder?.state==='recording')return status('Arrêter export EDIT avant une modification');
   try{
    state.clips=splitStoryboardAt(state.clips,state.editTime,newId());
    state.editPlaying=false;state.editLast=0;panel();sync();
    status('Clip vidéo divisé au curseur, source inchangée');
   }catch(e){status('Division impossible : '+e.message);}
  };
  controls.append(play,seek,clock,cutButton,exportButton);
  const select=document.createElement('select');select.setAttribute('aria-label','Choisir un média du coffre');
  const eligible=state.assets.filter(a=>String(a.type).startsWith('image/')||String(a.type).startsWith('video/'));
  for(const asset of eligible){const option=document.createElement('option');option.value=asset.id;option.textContent=asset.name;select.append(option);}
  const add=document.createElement('button');add.textContent='+ Clip';add.disabled=!eligible.length;
  add.onclick=()=>{
   const asset=state.assets.find(a=>a.id===select.value);if(!asset)return;
   const kind=asset.type.startsWith('video/')?'video':'image';
   state.clips.push(validateClip({id:newId(),assetId:asset.id,name:asset.name,kind,duration:5,inPoint:0}));
   loadEditAsset(asset.id).catch(error=>status('Prévisualisation média : '+error.message));
   state.editTime=0;state.editPlaying=false;panel();sync();status('Clip ajouté à la timeline');
  };
  wrap.append(select,add);
  const count=document.createElement('p');count.className='muted';
  count.textContent=state.clips.length+' clip(s) · '+editClock(storyboardDuration(state.clips))+' · projet sauvegardable';
  el.append(count);
  state.clips.forEach((clip,index)=>{
   const row=document.createElement('div');row.className='layer-row';row.style.flexWrap='wrap';row.style.gap='6px';
   const info=document.createElement('span');info.className='name';info.textContent=(index+1)+'. '+clip.name+' · '+clip.kind;
   const duration=document.createElement('input');duration.type='number';duration.min='0.1';duration.max='3600';duration.step='0.1';duration.style.width='75px';
   duration.title='Durée en secondes';duration.value=String(clipDuration(clip));
   duration.onchange=()=>{
    const n=Number(duration.value);if(!Number.isFinite(n)||n<.1||n>3600)return;
    clip.duration=n;if(clip.kind==='video')clip.outPoint=(Number(clip.inPoint)||0)+n;
    state.editPlaying=false;panel();
   };
   if(clip.kind==='video'){
    const inputTime=(caption,value,callback)=>{
     const wrapper=document.createElement('label');wrapper.className='muted';wrapper.textContent=caption+' ';
     const control=document.createElement('input');control.type='number';control.min='0';control.step='0.1';control.style.width='82px';control.value=String(value);
     control.setAttribute('aria-label',caption+' du clip '+(index+1));
     control.onchange=callback;wrapper.append(control);return wrapper;
    };
    const updateTrim=(start,end)=>{
     if(editorRecorder?.state==='recording')return status('Arrêter export EDIT avant une modification');
     try{
      state.clips[index]=trimVideoClip(clip,start,end);
      state.editPlaying=false;state.editLast=0;
      state.editTime=Math.min(state.editTime,Math.max(0,storyboardDuration(state.clips)-0.001));
      panel();sync();status('Plage source IN/OUT modifiée sans modifier le fichier');
     }catch(e){status('Plage refusée : '+e.message);panel();}
    };
    row.append(inputTime('IN (s)',clip.inPoint,()=>updateTrim(Number(row.querySelector('[aria-label="IN (s) du clip '+(index+1)+'"]').value),Number(clip.outPoint))));
    row.append(inputTime('OUT (s)',clip.outPoint,()=>updateTrim(Number(clip.inPoint),Number(row.querySelector('[aria-label="OUT (s) du clip '+(index+1)+'"]').value))));
   }
   const title=document.createElement('input');title.type='text';title.placeholder='Titre incrusté';title.value=clip.title||'';title.style.flex='1';
   title.onchange=()=>{clip.title=title.value;};
   const up=document.createElement('button');up.textContent='↑';up.title='Monter';up.onclick=()=>{state.clips=moveClip(state.clips,index,-1);panel();};
   const down=document.createElement('button');down.textContent='↓';down.title='Descendre';down.onclick=()=>{state.clips=moveClip(state.clips,index,1);panel();};
   const remove=document.createElement('button');remove.textContent='×';remove.title='Retirer le clip';remove.onclick=()=>{state.clips.splice(index,1);state.editTime=0;panel();};
   row.append(info,duration,title,up,down,remove);el.append(row);
   loadEditAsset(clip.assetId).catch(()=>{});
  });
  if(!state.clips.length){const msg=document.createElement('p');msg.className='muted';msg.textContent='Ajoute une image ou une vidéo par + Média, puis sélectionne-la ici.';el.append(msg);}
 }
 else if(state.space==='MEETING'){
  const speaker=document.createElement('input');speaker.placeholder='Intervenant';speaker.value='Intervenant 1';
  const line=document.createElement('input');line.placeholder='Phrase / transcription manuelle';line.setAttribute('aria-label','Texte de la transcription');
  const add=document.createElement('button');add.textContent='+ Segment';
  add.onclick=()=>{if(!line.value.trim())return;state.transcript.push({speaker:speaker.value||'Inconnu',text:line.value.trim(),t:Math.floor(performance.now()/1000),verified:false});line.value='';panel();status('Segment ajouté à la réunion');};
  const exportBtn=document.createElement('button');exportBtn.textContent='Exporter SRT';exportBtn.onclick=downloadSRT;
  const exportNotes=document.createElement('button');exportNotes.textContent='Compte rendu Markdown';exportNotes.onclick=()=>dl('reunion-notes.md',new Blob([exportMeetingNotes(state.transcript)],{type:'text/markdown'}));
  const importLabel=document.createElement('label');importLabel.className='file-button';importLabel.textContent='Importer SRT';
  const input=document.createElement('input');input.type='file';input.accept='.srt,text/plain';input.hidden=true;
  input.onchange=async()=>{try{
    const file=input.files?.[0];if(!file)return;
    const imported=parseSRT(await file.text());if(!imported.length)throw Error('Aucun segment valide');
    state.transcript.push(...imported);state.transcript.sort((a,b)=>a.t-b.t);panel();status(imported.length+' segments SRT importés (non vérifiés)');
  }catch(error){status('Import SRT : '+error.message);}};
  importLabel.append(input);wrap.append(speaker,line,add,importLabel,exportBtn,exportNotes);
  const captionLabel=document.createElement('label');captionLabel.className='notice';
  const check=document.createElement('input');check.type='checkbox';check.checked=state.captionsVisible;
  check.onchange=()=>{state.captionsVisible=check.checked;status(check.checked?'Sous-titres visibles dans le flux public':'Sous-titres retirés du flux public');};
  captionLabel.append(check,document.createTextNode(' Afficher explicitement les sous-titres sur le flux public'));
  el.append(captionLabel);
  const info=document.createElement('p');info.className='notice';info.textContent='Import, saisie et export locaux. Les sous-titres sont PRIVÉS par défaut et non analysés automatiquement. Transcription et traduction IA restent à intégrer.';el.append(info);
  state.transcript.slice(-7).forEach(item=>{const div=document.createElement('div');div.className='transcript';div.innerHTML='<span class="speaker">'+esc(item.speaker)+'</span><span>'+esc(item.text)+'</span><small>'+esc(srtTime(item.t))+'</small>';el.append(div);});
 }
 else if(state.space==='GENERATE'){
  const info=document.createElement('p');info.className='notice';info.textContent='Relais local vers ComfyUI, port 8188. Importer un workflow API JSON contenant des noeuds. Aucun modèle n’est inclus; génération non temps réel.';el.append(info);
  const input=document.createElement('textarea');input.id='workflow';input.placeholder='{"3":{"class_type":"...","inputs":{...}}}';input.setAttribute('aria-label','Workflow ComfyUI API JSON');el.append(input);
  const send=document.createElement('button');send.textContent='Envoyer à ComfyUI local';
  const check=document.createElement('button');check.textContent='Vérifier le dernier job';check.disabled=!lastComfyJob;
  const result=document.createElement('pre');result.className='muted';result.style.whiteSpace='pre-wrap';result.style.overflowWrap='anywhere';
  result.textContent=lastComfyJob?'Dernier job : '+lastComfyJob+' (état non vérifié)':'Aucun job soumis dans cette session.';
  send.onclick=async()=>{try{
    const prompt=JSON.parse(input.value);
    const r=await fetch('/api/comfy/queue',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt})});
    const data=await r.json();
    if(r.ok&&data.prompt_id){lastComfyJob=String(data.prompt_id);check.disabled=false;result.textContent='Job '+lastComfyJob+' en file — cliquer sur Vérifier.';}
    status(r.ok?'Job ComfyUI : '+(data.prompt_id||'en file'):'ComfyUI : '+(data.error||'échec'));
  }catch(e){status('Erreur génération : '+e.message);}};
  check.onclick=async()=>{
    if(!lastComfyJob)return;
    check.disabled=true;
    result.textContent='Recherche du résultat ComfyUI…';
    try{
      const r=await fetch('/api/comfy/job?prompt_id='+encodeURIComponent(lastComfyJob));
      const data=await r.json();
      if(!r.ok)throw Error(data.error||'Erreur ComfyUI');
      const names=(data.outputs||[]).map(item=>item.kind+' : '+item.filename);
      result.textContent='Job : '+data.prompt_id+'\nÉtat : '+data.status+'\nFichiers produits : '+names.length+(names.length?'\n'+names.join('\n'):'');
      status(data.status==='completed'?'Génération terminée, fichiers sur ComfyUI local':'Suivi ComfyUI : '+data.status);
    }catch(e){result.textContent='Suivi impossible : '+e.message;}
    finally{check.disabled=false;}
  };
  wrap.append(send,check);el.append(result);
 }
 else if(state.space==='XR'){
  const intro=document.createElement('p');intro.className='notice';intro.textContent='Importer un événement X-Ray au format {"type":"detections","items":[{"label":"main","x":0.1,"y":0.2,"w":0.2,"h":0.3}]}. Démo d’overlays seulement.';el.append(intro);
  const input=document.createElement('textarea');input.placeholder='{"type":"detections","items":[]}';input.setAttribute('aria-label','Événement XR JSON');el.append(input);
  const add=document.createElement('button');add.textContent='Importer détections';add.onclick=()=>{try{const obj=JSON.parse(input.value);if(obj.type!=='detections'||!Array.isArray(obj.items))throw Error('Type attendu : detections');for(const d of obj.items.slice(0,30)){addLayer({type:'rect',name:'XR · '+String(d.label||'objet'),x:Math.max(0,Number(d.x)||0),y:Math.max(0,Number(d.y)||0),w:Math.min(1,Number(d.w)||.1),h:Math.min(1,Number(d.h)||.1),color:'#42e8df'});}status('Événement XR importé en overlays 2D (test manuel)');}catch(e){status('Événement invalide : '+e.message);}};wrap.append(add);
  const gesture=document.createElement('button');gesture.textContent='Simuler claquement de doigts';gesture.onclick=()=>{scene().layers.filter(l=>l.name.startsWith('XR ·')).forEach(l=>l.visible=!l.visible);sync();status('Geste simulé : couches XR basculées');};wrap.append(gesture);
 }
 else if(state.space==='CONTROL'){
  const button=document.createElement('button');button.textContent='Actualiser diagnostic';const pre=document.createElement('pre');pre.className='muted';pre.textContent='Vérifie seulement les ports locaux : pas de contrôle OBS ni de test des modèles.';button.onclick=async()=>{pre.textContent=JSON.stringify(await health(),null,2);};wrap.append(button);el.append(pre);
 }
 else if(state.space==='LIBRARY'){
  const info=document.createElement('p');info.className='notice';info.textContent='Bibliothèque de session. Les fichiers ne sont pas sauvegardés dans le JSON; conserver les originaux.';el.append(info);
  const cards=document.createElement('div');cards.className='cards';cards.innerHTML=state.assets.map(a=>card(a.name,Math.round(a.size/1024)+' Ko · '+a.type)).join('')||card('Bibliothèque vide','Ajoute une image ou vidéo par + Média.');el.append(cards);
 }
 else{
  const modules={EDIT:[['Montage multipiste','À auditer : FreeCut MIT / OpenReelio MIT.'],['Composition LIVE','Les calques ci-dessus peuvent déjà être préparés.']],AUDIO:[['Routage','Sources système et micro séparées — non implémenté.'],['ASR','Sherpa-ONNX / WhisperLiveKit à raccorder.']],CAPTURE:[['Profondeur monoculaire','Estimation ≠ géométrie métrique.'],['Photogrammétrie','COLMAP / SuperSplat : export et tests à faire.']],CINEMA:[['Caméras 3D','Connecteur Blender / Watchtower à développer.'],['Animations','Personnages et trajectoires persistantes à développer.']],AUTOMATE:[['Chronos','Contrat événement/action, autorisations et audit à implémenter.'],['Workflows','Moteur de graphes à choisir avant intégration.']],GRAPHICS:[['Graphiques','Titres statiques disponibles ; motion design non relié.'],['Schémas','Mermaid / Motion Canvas à évaluer.']]};
  const cards=document.createElement('div');cards.className='cards';cards.innerHTML=(modules[state.space]||[]).map(v=>card(v[0],v[1])).join('');el.append(cards);
 }
}
makeNav();sync();setSpace('LIVE');
$('projectName').onchange=e=>{state.projectName=e.target.value||'Projet';};
$('btnNewScene').onclick=()=>{const s={id:newId(),name:'Scène '+(state.scenes.length+1),layers:[]};state.scenes.push(s);state.activeScene=s.id;state.selected=null;sync();status('Nouvelle scène');};
$('btnSave').onclick=saveProject;$('btnPortable').onclick=savePortableProject;$('fileProject').onchange=e=>{if(e.target.files[0])loadProject(e.target.files[0]);};
$('fileMedia').onchange=e=>addFiles([...e.target.files]);
document.querySelectorAll('[data-add]').forEach(b=>b.onclick=()=>{if(b.dataset.add==='text')addLayer({type:'text',name:'Texte',value:'Nouveau texte',x:.2,y:.2,w:.6,h:.12,size:48,color:'#ffffff'});else addLayer({type:'rect',name:'Forme',x:.2,y:.2,w:.3,h:.2,color:'#28c8bf'});});
$('btnCamera').onclick=camera;$('btnMicrophone').onclick=microphone;$('btnScreen').onclick=captureScreen;$('btnPNG').onclick=png;$('btnRecord').onclick=record;$('btnHealth').onclick=health;$('btnObsOutput').onclick=()=>{obsOutput=!obsOutput;$('btnObsOutput').classList.toggle('active',obsOutput);$('btnObsOutput').textContent=obsOutput?'■ Stop OBS':'Sortie OBS';status(obsOutput?'Sortie MJPEG active : ajouter Source navigateur http://127.0.0.1:8787/obs dans OBS · vidéo seule':'Sortie OBS arrêtée');};
C.addEventListener('pointerdown',e=>{const rect=C.getBoundingClientRect(),x=(e.clientX-rect.left)/rect.width,y=(e.clientY-rect.top)/rect.height;const hit=[...scene().layers].reverse().find(l=>l.visible&&x>=l.x&&x<=l.x+l.w&&y>=l.y&&y<=l.y+l.h);state.selected=hit?.id||null;sync();});
requestAnimationFrame(loop);
initMediaLibrary();
window.addEventListener('beforeunload',()=>{if(webcamStream)webcamStream.getTracks().forEach(t=>t.stop());if(microphoneStream)microphoneStream.getTracks().forEach(t=>t.stop());if(screenStream)screenStream.getTracks().forEach(t=>t.stop());releaseMediaURLs();});
health();
