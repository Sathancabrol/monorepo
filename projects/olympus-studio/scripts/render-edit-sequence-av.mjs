// Deterministic offline EDIT pipeline: numbered PNG frames -> VP9 -> timeline audio -> Opus WebM.
// Usage: node scripts/render-edit-sequence-av.mjs framesDir fps duration audio.wav track.json output.webm
import {mkdtemp,rm,readFile,stat} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {framePlan,renderFrames} from './render-edit-frames.mjs';
import {renderEditAV} from './render-edit-av.mjs';

export async function renderSequenceAV(framesDir,fps,duration,audio,track,output,options={}){
  const plan=framePlan(fps,duration);
  for(const value of [framesDir,audio,output])if(typeof value!=='string'||!value.trim())throw Error('Chemin manquant');
  const paths=[resolve(framesDir),resolve(audio),resolve(output)];
  if(new Set(paths).size!==3||!paths[2].toLowerCase().endsWith('.webm'))throw Error('Chemins invalides');
  try{await stat(paths[2]);throw Error('Sortie existante');}
  catch(e){if(e.code!=='ENOENT')throw e;}
  const temp=await mkdtemp(join(tmpdir(),'olympus-sequence-av-'));
  try{
    const video=join(temp,'silent.webm');
    await renderFrames(paths[0],plan.rate,plan.duration,video,{ffmpeg:options.ffmpeg});
    await renderEditAV(video,paths[1],track,plan.duration,paths[2],options);
    return {output:paths[2],fps:plan.rate,frames:plan.count,duration:plan.duration};
  }finally{await rm(temp,{recursive:true,force:true});}
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){
  const [frames,fps,duration,audio,trackPath,output]=process.argv.slice(2);
  try{
    if(!trackPath)throw Error('Usage: framesDir fps duration audio.wav track.json output.webm');
    const track=JSON.parse(await readFile(trackPath,'utf8'));
    console.log(JSON.stringify(await renderSequenceAV(frames,fps,duration,audio,track,output)));
  }catch(e){console.error(e.message);process.exitCode=1;}
}
