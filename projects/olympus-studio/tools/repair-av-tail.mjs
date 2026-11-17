#!/usr/bin/env node
// Optional local repair of a MediaRecorder WebM whose video ends before audio.
// Requires existing FFmpeg + FFprobe; never overwrites the input.
import { spawnSync } from 'node:child_process';
import { resolve, extname } from 'node:path';
import { existsSync } from 'node:fs';

function run(command,args) {
 const result=spawnSync(command,args,{encoding:'utf8',timeout:120000,maxBuffer:32*1024*1024});
 if(result.error)throw result.error;
 if(result.status!==0)throw Error(command+' failed: '+(result.stderr||'').slice(-1200));
 return result.stdout;
}
export function plan(videoEnd,audioEnd) {
 if(!Number.isFinite(videoEnd)||!Number.isFinite(audioEnd)||videoEnd<=0||audioEnd<=0)throw Error('Invalid stream timestamps');
 const gap=audioEnd-videoEnd;
 if(gap<=0.05)return {needed:false,gap};
 if(gap>30)throw Error('Gap over 30s: inspect source manually');
 return {needed:true,gap,pad:gap.toFixed(3)};
}
export function streamEnd(stream) {
 const packets=stream.packets||[];
 let end=0;
 for(const p of packets){
  const pts=Number(p.pts_time),dur=Number(p.duration_time||0);
  if(Number.isFinite(pts))end=Math.max(end,pts+(Number.isFinite(dur)?dur:0));
 }
 return end;
}
function main(){
 const [inputArg,outputArg]=process.argv.slice(2);
 if(!inputArg||!outputArg)throw Error('Usage: node tools/repair-av-tail.mjs input.webm output.webm');
 const input=resolve(inputArg),output=resolve(outputArg);
 if(input===output)throw Error('Output must differ from input');
 if(!existsSync(input)||extname(input).toLowerCase()!=='.webm'||extname(output).toLowerCase()!=='.webm')throw Error('Input must exist and both paths must be .webm');
 if(existsSync(output))throw Error('Output already exists; refusing overwrite');
 const json=JSON.parse(run('ffprobe',['-v','error','-show_packets','-show_streams','-of','json',input]));
 const video=json.streams.find(s=>s.codec_type==='video'),audio=json.streams.find(s=>s.codec_type==='audio');
 if(!video||!audio)throw Error('Both video and audio streams are required');
 const packets=json.packets||[];
 const videoEnd=streamEnd({packets:packets.filter(p=>p.stream_index===video.index)});
 const audioEnd=streamEnd({packets:packets.filter(p=>p.stream_index===audio.index)});
 const p=plan(videoEnd,audioEnd);
 if(!p.needed)throw Error('No missing video tail detected; no repair performed');
 // Freeze the last frame to cover missing timestamps. Does not reconstruct motion.
 run('ffmpeg',['-hide_banner','-nostdin','-i',input,'-filter:v',`tpad=stop_mode=clone:stop_duration=${p.pad},fps=24`,'-c:v','libvpx','-b:v','1M','-c:a','libopus','-t',String(audioEnd),'-y',output]);
 process.stdout.write(JSON.stringify({input,output,videoEnd,audioEnd,paddedSeconds:p.gap,warning:'Frozen final frame; motion not recovered'})+'\n');
}
if(import.meta.url===new URL('file://'+process.argv[1]).href){
 try{main()}catch(e){console.error(e.message);process.exitCode=1}
}
