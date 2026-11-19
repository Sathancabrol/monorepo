// Offline EDIT export bridge: apply the timeline audio contract and mux it with an existing video-only file.
// Video timing is inherited from the source. This does NOT repair dropped MediaRecorder frames.
// Usage: node scripts/render-edit-av.mjs video.webm audio.wav track.json durationSeconds output.webm
import {spawn} from 'node:child_process';
import {readFile, mkdtemp, rm, stat} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join, resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {renderAudio} from './render-edit-audio.mjs';

async function run(bin,args){
  return new Promise((ok,fail)=>{
    const child=spawn(bin,args,{shell:false,stdio:['ignore','ignore','pipe']});
    let err='';
    child.stderr.on('data',chunk=>{err=(err+chunk.toString()).slice(-4096);});
    child.once('error',fail);
    child.once('close',code=>code===0?ok():fail(new Error(bin+' exit '+code+': '+err)));
  });
}
async function exists(path){try{await stat(path);return true;}catch(e){if(e.code==='ENOENT')return false;throw e;}}
export async function renderEditAV(video,audio,track,duration,output,{ffmpeg='ffmpeg',ffprobe='ffprobe'}={}){
  const paths=[video,audio,output];
  if(paths.some(p=>typeof p!=='string'||!p.trim()))throw Error('Chemin manquant');
  const [v,a,o]=paths.map(p=>resolve(p));
  if(new Set([v,a,o]).size!==3||!o.toLowerCase().endsWith('.webm'))throw Error('Entrées/sortie invalides');
  if(!await exists(v)||!await exists(a)||await exists(o))throw Error('Source absente ou sortie existante');
  const seconds=Number(duration);
  if(!Number.isFinite(seconds)||seconds<=0||seconds>120)throw Error('Durée EDIT invalide');
  const dir=await mkdtemp(join(tmpdir(),'olympus-av-'));
  const wav=join(dir,'timeline.wav');
  let outputCreated=false;
  try{
    await renderAudio(a,wav,track,seconds,{binary:ffmpeg});
    // Re-encode the source video to VP9 and the timeline WAV to Opus. No shell or network.
    await run(ffmpeg,['-nostdin','-hide_banner','-loglevel','error','-n','-i',v,'-i',wav,
      '-map','0:v:0','-map','1:a:0','-t',String(seconds),'-c:v','libvpx-vp9',
      '-deadline','realtime','-cpu-used','5','-c:a','libopus','-b:a','128k',o]);
    outputCreated=true;
    const chunks=[];
    const probe=spawn(ffprobe,['-v','error','-show_entries','stream=codec_type,codec_name','-of','json',o],{shell:false,stdio:['ignore','pipe','pipe']});
    for await(const chunk of probe.stdout)chunks.push(chunk);
    const exit=await new Promise((ok,fail)=>{probe.once('error',fail);probe.once('close',ok);});
    if(exit!==0)throw Error('FFprobe a échoué');
    const streams=JSON.parse(Buffer.concat(chunks).toString()).streams||[];
    if(!streams.some(s=>s.codec_type==='video'&&s.codec_name==='vp9')||
       !streams.some(s=>s.codec_type==='audio'&&s.codec_name==='opus'))throw Error('Codecs de sortie invalides');
    return o;
  }catch(error){
    // Only delete the output if this invocation created it; never remove a pre-existing file.
    if(outputCreated)await rm(o,{force:true});
    throw error;
  }finally{await rm(dir,{recursive:true,force:true});}
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){
  const [video,audio,config,duration,output]=process.argv.slice(2);
  if(!video||!audio||!config||!duration||!output){console.error('Usage: node scripts/render-edit-av.mjs video.webm audio.wav track.json durationSeconds output.webm');process.exitCode=2;}
  else try{await renderEditAV(video,audio,JSON.parse(await readFile(config,'utf8')),duration,output);console.log('WebM EDIT : '+output);}
  catch(e){console.error(e.message);process.exitCode=1;}
}
