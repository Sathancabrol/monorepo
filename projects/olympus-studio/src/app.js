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
const state={space:'LIVE',projectName:'Production sans titre',scenes:baseScenes(),activeScene:null,selected:null,transcript:[],assets:[],recording:false};
const runtime=new Map();let webcamStream=null;let webcamVideo=null;let microphoneStream=null;let screenStream=null;let screenVideo=null;let recorder=null;let chunks=[];let recStarted=0;let lastCanvas=0;let obsOutput=false;let lastObsFrame=0;let sendingObs=false;let lastComfyJob=null;
state.activeScene=state.scenes[0].id;
const dbReady = openMediaDB().catch(() => null);
const createdMediaURLs = new Set();
function releaseMediaURLs(){for(const url of createdMediaURLs)URL.revokeObjectURL(url);createdMediaURLs.clear();}
function localMediaURL(blob){const url=URL.createObjectURL(blob);createdMediaURLs.add(url);return url;}
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const scene=()=>state.scenes.find(s=>s.id===state.activeScene)||state.scenes[0];
const selected=()=>scene().layers.find(l=>l.id===state.selected);
function status(t){$('status').textContent=t;}
function dl(name,blob){const a=document.createElement('a');const u=URL.createObjectURL(blob);a.href=u;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),10000);}
function addLayer(layer){layer.id=newId();layer.visible=true;scene().layers.push(layer);state.selected=layer.id;sync();return layer;}
function setSpace(key){state.space=key;const item=spaces.find(s=>s[0]===key);$('spaceTitle').textContent=item[0];$('spaceDesc').textContent=item[2];document.querySelectorAll('[data-space]').forEach(b=>b.classList.toggle('active',b.dataset.space===key));panel();sync();}
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
 const last=state.transcript[state.transcript.length-1];if(last&&state.space==='MEETING'){ctx.fillStyle='rgba(0,0,0,.76)';ctx.fillRect(140,630,1000,57);ctx.fillStyle='#fff';ctx.font='26px Segoe UI';ctx.textAlign='center';ctx.fillText((last.speaker+': '+last.text).slice(0,85),640,666,950);ctx.textAlign='left';}
}
function loop(t){if(t-lastCanvas>=32){draw();lastCanvas=t;}if(obsOutput&&t-lastObsFrame>=150&&!sendingObs){lastObsFrame=t;sendingObs=true;C.toBlob(async b=>{try{if(b)await fetch('/api/frame',{method:'POST',headers:{'Content-Type':'image/jpeg'},body:b});}catch(e){status('Sortie OBS indisponible : '+e.message);}finally{sendingObs=false;}},'image/jpeg',.66);}requestAnimationFrame(loop);
initMediaLibrary();}
function projectPayload(){
 const safe=state.scenes.map(s=>({id:s.id,name:s.name,layers:s.layers.map(l=>({...l,source:undefined}))}));
 return {format:'olympus-studio-project',schema:2,projectName:state.projectName,activeScene:state.activeScene,scenes:safe,transcript:state.transcript,warning:'Les références média utilisent IndexedDB pour cette origine du navigateur; utilise Portable pour changer de PC.'};
}
function saveProject(){
 dl('olympus-project-'+Date.now()+'.json',new Blob([JSON.stringify(projectPayload(),null,2)],{type:'application/json'}));
 status('Projet JSON exporté — les médias restent dans le coffre local du navigateur');
}
async function savePortableProject(){
 const button=$('btnPortable');button.disabled=true;
 try{
  const db=await dbReady;
  const refs=[...new Set(state.scenes.flatMap(s=>s.layers.filter(l=>l.type==='image'||l.type==='video').map(l=>l.id)))];
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
   const record=await getMedia(db,id);
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
 try{const data=JSON.parse(await file.text());if(data.format!=='olympus-studio-project'||!Array.isArray(data.scenes)||!data.scenes.length)throw Error('Format incompatible');
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
  state.activeScene=state.scenes.find(s=>s.id===data.activeScene)?.id||state.scenes[0].id;state.selected=null;state.transcript=Array.isArray(data.transcript)?data.transcript:[];
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
function downloadSRT(){const body=state.transcript.map((x,i)=>String(i+1)+'\n'+srtTime(x.t)+' --> '+srtTime(x.t+3)+'\n'+x.speaker+': '+x.text+'\n').join('\n');dl('reunion.srt',new Blob([body],{type:'text/plain'}));}
async function health(){try{const r=await fetch('/api/health');const x=await r.json();$('engineStatus').textContent='OBS '+(x.services.obs.reachable?'visible':'absent')+' · ComfyUI '+(x.services.comfyui.reachable?'visible':'absent')+' · XR non connecté';status('Diagnostic local effectué — visible ne signifie pas connecté');return x;}catch(e){status('Diagnostic non disponible : '+e.message);return null;}}
const card=(name,detail)=>'<div class="mini-card"><h3>'+esc(name)+'</h3><p>'+esc(detail)+'</p></div>';
function panel(){
 const el=$('workspacePanel');el.innerHTML='';const h=document.createElement('h2');h.textContent=state.space+' · atelier';el.append(h);
 const wrap=document.createElement('div');wrap.className='actions';el.append(wrap);
 if(state.space==='LIVE'){const info=document.createElement('p');info.className='notice';info.textContent='La composition Canvas fonctionne localement. La régie OBS WebSocket se trouve à droite (à connecter à OBS installé). La sortie MJPEG reste vidéo seule; l’audio multipiste OBS natif reste externe.';el.append(info);const cards=document.createElement('div');cards.className='cards';cards.innerHTML=card('Écran / webcams','Webcam, écran et microphone disponibles sur autorisation, depuis la barre d’outils.')+card('OBS externe','Source navigateur sur /obs après activation du bouton « Sortie OBS », sans audio; vidéo MJPEG limitée par la machine.')+card('Enregistrement','WebM du Canvas avec piste microphone ou audio partagé si disponible; PNG du plan courant. OBS reste externe.');el.append(cards);}
 else if(state.space==='MEETING'){
  const speaker=document.createElement('input');speaker.placeholder='Intervenant';speaker.value='Intervenant 1';const line=document.createElement('input');line.placeholder='Phrase / transcription manuelle';line.setAttribute('aria-label','Texte de la transcription');const add=document.createElement('button');add.textContent='+ Segment';add.onclick=()=>{if(!line.value.trim())return;state.transcript.push({speaker:speaker.value||'Inconnu',text:line.value.trim(),t:Math.floor(performance.now()/1000)});line.value='';panel();status('Segment ajouté à la réunion');};const exportBtn=document.createElement('button');exportBtn.textContent='Exporter SRT';exportBtn.onclick=downloadSRT;wrap.append(speaker,line,add,exportBtn);
  const info=document.createElement('p');info.className='notice';info.textContent='Saisie manuelle seulement. Transcription, traduction et diarisation automatiques restent à intégrer; informer les participants avant enregistrement.';el.append(info);
  state.transcript.slice(-7).forEach(s=>{const div=document.createElement('div');div.className='transcript';div.innerHTML='<span class="speaker">'+esc(s.speaker)+'</span><span>'+esc(s.text)+'</span><small>'+esc(srtTime(s.t))+'</small>';el.append(div);});
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
window.addEventListener('beforeunload',()=>{if(webcamStream)webcamStream.getTracks().forEach(t=>t.stop());if(microphoneStream)microphoneStream.getTracks().forEach(t=>t.stop());if(screenStream)screenStream.getTracks().forEach(t=>t.stop());releaseMediaURLs();});
health();
