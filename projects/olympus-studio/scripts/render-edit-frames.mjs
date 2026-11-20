// Offline deterministic video from a contiguous PNG frame sequence. No MediaRecorder.
// Usage: node scripts/render-edit-frames.mjs framesDir fps durationSeconds output.webm
import {spawn} from 'node:child_process';
import {readdir,stat} from 'node:fs/promises';
import {existsSync} from 'node:fs';
import {resolve,join} from 'node:path';
import {pathToFileURL} from 'node:url';

export function framePlan(fps,duration){
  const rate=Number(fps),seconds=Number(duration);
  if(!Number.isInteger(rate)||rate<1||rate>60)throw Error('FPS invalide (1–60)');
  if(!Number.isFinite(seconds)||seconds<=0||seconds>120)throw Error('Durée invalide (0–120 s)');
  const count=Math.round(rate*seconds);
  if(count<1||Math.abs(count/rate-seconds)>1/rate/2+1e-9)throw Error('Durée non représentable');
  return {rate,count,duration:count/rate};
}
function run(binary,args){
  return new Promise((ok,fail)=>{
    const p=spawn(binary,args,{shell:false,stdio:['ignore','ignore','pipe']});
    let stderr='';
    p.stderr.on('data',b=>{stderr=(stderr+b.toString()).slice(-2048)});
    p.once('error',fail);
    p.once('close',code=>code===0?ok():fail(Error('FFmpeg ('+code+'): '+stderr)));
  });
}
export async function renderFrames(dir,fps,duration,output,{ffmpeg='ffmpeg'}={}){
  const plan=framePlan(fps,duration);
  if(typeof dir!=='string'||!dir.trim()||typeof output!=='string'||!output.trim())throw Error('Chemin manquant');
  const source=resolve(dir),target=resolve(output);
  if(!target.toLowerCase().endsWith('.webm')||target.startsWith(source+'/')||target.startsWith(source+'\\'))throw Error('Sortie invalide');
  if(existsSync(target))throw Error('FFmpeg: sortie existante, écrasement refusé');
  const names=await readdir(source);
  const expected=Array.from({length:plan.count},(_,i)=>String(i+1).padStart(6,'0')+'.png');
  const pngs=names.filter(n=>n.toLowerCase().endsWith('.png')).sort();
  if(pngs.length!==expected.length||pngs.some((n,i)=>n!==expected[i]))throw Error('Séquence PNG incomplète ou ambiguë');
  for(const name of expected)if(!(await stat(join(source,name))).isFile())throw Error('Frame non régulière');
  // -n protects pre-existing output; -frames:v bounds encoded frames.
  await run(ffmpeg,['-nostdin','-hide_banner','-loglevel','error','-n','-framerate',String(plan.rate),
    '-start_number','1','-i',join(source,'%06d.png'),'-frames:v',String(plan.count),
    '-an','-c:v','libvpx-vp9','-deadline','realtime','-cpu-used','5','-pix_fmt','yuv420p',target]);
  return {output:target,...plan};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){
  const [dir,fps,duration,output]=process.argv.slice(2);
  try{console.log(JSON.stringify(await renderFrames(dir,fps,duration,output)));}
  catch(e){console.error(e.message);process.exitCode=1;}
}
