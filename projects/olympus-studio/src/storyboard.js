// OLYMPUS Studio — minimal non-destructive sequential editor model.
// Rendering and media loading are handled by the browser shell, not this module.
export function clipDuration(clip) {
  if (!clip || typeof clip !== 'object') return 0;
  if (clip.kind === 'video') {
    const start = Math.max(0, Number(clip.inPoint) || 0);
    const end = Number(clip.outPoint);
    if (Number.isFinite(end) && end > start) return Math.min(36000, end - start);
  }
  const time = Number(clip.duration);
  return Number.isFinite(time) ? Math.min(36000,Math.max(0.1,time)) : 5;
}

export function storyboardDuration(clips) {
  return (Array.isArray(clips)?clips:[]).reduce((sum,clip)=>sum+clipDuration(clip),0);
}

export function locateClip(clips, time) {
  if (!Array.isArray(clips) || !clips.length) return null;
  const total = storyboardDuration(clips);
  if (!Number.isFinite(time) || time < 0 || time >= total) return null;
  let start=0;
  for (const [index,clip] of clips.entries()) {
    const duration=clipDuration(clip);
    if (time < start+duration) return {index,clip,start,end:start+duration,localTime:time-start,sourceTime:Math.max(0,Number(clip.inPoint)||0)+(time-start)};
    start+=duration;
  }
  return null;
}

export function moveClip(clips, index, offset) {
  if (!Array.isArray(clips)) return [];
  const arr=clips.slice(), target=index+offset;
  if (!Number.isInteger(index) || !Number.isInteger(offset) || index<0 || index>=arr.length || target<0 || target>=arr.length) return arr;
  const [item]=arr.splice(index,1);
  arr.splice(target,0,item);
  return arr;
}

export function validateClip(clip) {
  if (!clip || typeof clip.id!=='string' || typeof clip.assetId!=='string' || !['image','video'].includes(clip.kind)) throw new Error('Clip de montage invalide');
  const d=clipDuration(clip);
  if (!Number.isFinite(d) || d<=0) throw new Error('Durée du clip invalide');
  return {id:clip.id,assetId:clip.assetId,kind:clip.kind,name:String(clip.name||'Clip'),title:String(clip.title||''),duration:d,inPoint:Math.max(0,Number(clip.inPoint)||0),outPoint:clip.kind==='video'?Math.max(0,Number(clip.inPoint)||0)+d:0};
}

export function referencedAssetIds(scenes, clips, audioTrack = null) {
 const mediaLayers = (Array.isArray(scenes)?scenes:[]).flatMap(scene=>(scene.layers||[]).filter(layer=>layer.type==='image'||layer.type==='video').map(layer=>layer.assetId||layer.id));
 const clipAssets=(Array.isArray(clips)?clips:[]).map(clip=>clip.assetId);
 return [...new Set([...mediaLayers,...clipAssets,audioTrack?.assetId].filter(Boolean))];
}

// Edition non destructive : seule la plage source change, jamais le média original.
// Minimum 0,1 seconde, pas de valeur infinie, durée maximale de 10 h.
export function trimVideoClip(clip, inPoint, outPoint) {
  if (!clip || clip.kind !== 'video') throw new Error('Découpe réservée aux vidéos');
  const start=Number(inPoint), end=Number(outPoint);
  if (!Number.isFinite(start) || !Number.isFinite(end) || start<0 || end-start<0.1-1e-7 || end-start>36000)
    throw new Error('Plage IN/OUT invalide (0,1 s minimum, 10 h maximum)');
  return {...clip,inPoint:start,outPoint:end,duration:end-start};
}

// Les deux segments partagent la même source vidéo mais portent des identifiants
// différents : renommer/supprimer l'un ne modifie pas l'autre.
export function splitVideoClip(clip, atLocalTime, rightId) {
  if (!clip || clip.kind !== 'video') throw new Error('Division réservée aux vidéos');
  if (typeof rightId !== 'string' || !rightId || rightId === clip.id) throw new Error('Identifiant de segment invalide');
  const duration=clipDuration(clip);
  const at=Number(atLocalTime);
  if (!Number.isFinite(at) || at<0.1-1e-7 || duration-at<0.1-1e-7)
    throw new Error('Point de coupe trop proche du bord (0,1 s minimum)');
  const start=Number(clip.inPoint)||0;
  return [
    trimVideoClip(clip,start,start+at),
    trimVideoClip({...clip,id:rightId},start+at,start+duration),
  ];
}

// Découpe au temps du projet (timeline globale), pas au temps du fichier source.
export function splitStoryboardAt(clips, projectTime, rightId) {
  const located=locateClip(clips,projectTime);
  if (!located) throw new Error('Aucun clip au curseur');
  const [left,right]=splitVideoClip(located.clip,located.localTime,rightId);
  return [...clips.slice(0,located.index),left,right,...clips.slice(located.index+1)];
}
