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
  return {id:clip.id,assetId:clip.assetId,kind:clip.kind,name:String(clip.name||'Clip'),duration:d,inPoint:Math.max(0,Number(clip.inPoint)||0),outPoint:clip.kind==='video'?Math.max(0,Number(clip.inPoint)||0)+d:0};
}
