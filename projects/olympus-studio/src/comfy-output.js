// ComfyUI output gateway: no arbitrary URL, path, host or filesystem access.
// Only files enumerated in a completed job's /history may be retrieved.
export const MAX_COMFY_BYTES = 25 * 1024 * 1024;
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const MIME = {png:'image/png',jpg:'image/jpeg',jpeg:'image/jpeg',webp:'image/webp',gif:'image/gif',webm:'video/webm',mp4:'video/mp4',wav:'audio/wav',mp3:'audio/mpeg',ogg:'audio/ogg'};
export function selectComfyOutput(history,id,index){
 if(!UUID.test(id))throw Error('Identifiant de job invalide');
 if(!Number.isSafeInteger(index)||index<0||index>=250)throw Error('Index de sortie invalide');
 const job=history?.[id];
 if(!job||job.status?.completed!==true||job.status?.status_str==='error')throw Error('Job non terminé');
 const outputs=[];
 for(const value of Object.values(job.outputs||{})){
  for(const kind of ['images','videos','gifs','audio']){
   if(!Array.isArray(value?.[kind]))continue;
   for(const item of value[kind]){
    if(item&&typeof item.filename==='string')outputs.push(item);
   }
  }
 }
 const item=outputs[index];
 if(!item)throw Error('Sortie introuvable');
 const filename=item.filename,subfolder=item.subfolder??'',type=item.type??'output';
 if(!/^[^\\/\x00-\x1f]{1,180}$/.test(filename)||filename==='.'||filename==='..'||filename.includes('..'))throw Error('Nom de fichier interdit');
 if(typeof subfolder!=='string'||subfolder.length>180||subfolder.startsWith('/')||subfolder.includes('\\')||subfolder.split('/').some(s=>s==='.'||s==='..'||!s||/[\x00-\x1f]/.test(s)))throw Error('Sous-dossier interdit');
 if(type!=='output')throw Error('Seules les sorties finales sont autorisées');
 const ext=filename.split('.').pop().toLowerCase(),mime=MIME[ext];
 if(!mime)throw Error('Format de sortie non autorisé');
 return {filename,subfolder,type,mime};
}
export function validComfyBytes(bytes,mime){
 if(!bytes||bytes.length===0||bytes.length>MAX_COMFY_BYTES)return false;
 const prefix=(...b)=>b.every((v,i)=>bytes[i]===v);
 if(mime==='image/png')return prefix(137,80,78,71,13,10,26,10);
 if(mime==='image/jpeg')return prefix(255,216,255);
 if(mime==='image/webp')return bytes.length>12&&String.fromCharCode(...bytes.subarray(0,4))==='RIFF'&&String.fromCharCode(...bytes.subarray(8,12))==='WEBP';
 if(mime==='image/gif')return prefix(71,73,70,56);
 if(mime==='video/webm')return prefix(26,69,223,163);
 if(mime==='video/mp4')return bytes.length>12&&String.fromCharCode(...bytes.subarray(4,8))==='ftyp';
 if(mime==='audio/wav')return bytes.length>12&&String.fromCharCode(...bytes.subarray(0,4))==='RIFF'&&String.fromCharCode(...bytes.subarray(8,12))==='WAVE';
 if(mime==='audio/ogg')return prefix(79,103,103,83);
 if(mime==='audio/mpeg')return prefix(73,68,51)||bytes[0]===255&&(bytes[1]&224)===224;
 return false;
}
