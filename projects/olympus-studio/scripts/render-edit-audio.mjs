// Deterministic offline EDIT audio render. No shell interpolation or source mutation.
// Usage: node scripts/render-edit-audio.mjs source.wav output.wav track.json durationSeconds
import {spawn} from 'node:child_process';
import {readFile} from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
import {validateEditAudioTrack} from '../src/edit-audio.js';

export function renderAudioArgs(input,output,track,duration) {
  const t=validateEditAudioTrack(track);
  const seconds=Number(duration);
  if(!Number.isFinite(seconds)||seconds<=0||seconds>120)throw Error('Durée EDIT invalide (0–120 s)');
  if(typeof input!=='string'||!input.trim()||typeof output!=='string'||!output.trim()||input===output)throw Error('Chemins audio invalides');
  const n=x=>Number(x).toFixed(6);
  // Work in a fixed 48 kHz sample domain: timestamp-based atrim after adelay/apad
  // can truncate the WAV (observed 1.792667 s instead of 2.000000 s).
  const samples=Math.round(seconds*48000);
  // Source IN, timeline delay, volume, then pad/trim to the exact EDIT length.
  const filter='[0:a]atrim=start='+n(t.inPoint)+',asetpts=PTS-STARTPTS,volume='+n(t.enabled?t.volume:0)+',adelay='+Math.round(t.offset*1000)+':all=1,aresample=48000,apad=whole_len='+samples+',atrim=end_sample='+samples+',asetpts=PTS-STARTPTS[out]';
  return ['-nostdin','-hide_banner','-loglevel','error','-i',input,'-filter_complex',filter,'-map','[out]','-ar','48000','-ac','2','-c:a','pcm_s16le','-n',output];
}
export async function renderAudio(input,output,track,duration,{binary='ffmpeg'}={}){
  const args=renderAudioArgs(input,output,track,duration);
  return await new Promise((resolve,reject)=>{
    const child=spawn(binary,args,{shell:false,stdio:['ignore','ignore','pipe']});
    let error='';child.stderr.on('data',c=>{error=(error+c.toString()).slice(-4096);});
    child.on('error',reject);
    child.on('close',code=>code===0?resolve(output):reject(Error('FFmpeg a échoué ('+code+'): '+error)));
  });
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
  const [input,output,config,duration]=process.argv.slice(2);
  if(!input||!output||!config||!duration){console.error('Usage: node scripts/render-edit-audio.mjs input.wav output.wav track.json durationSeconds');process.exitCode=2;}
  else try{await renderAudio(input,output,JSON.parse(await readFile(config,'utf8')),duration);console.log('Audio EDIT rendu : '+output);}
  catch(e){console.error(e.message);process.exitCode=1;}
}
