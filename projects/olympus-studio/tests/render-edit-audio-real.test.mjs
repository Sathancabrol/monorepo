// Real FFmpeg regression: verify EDIT trim, offset, gain, duration in decoded PCM.
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {mkdtemp,readFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {renderAudio} from '../scripts/render-edit-audio.mjs';

const run=(bin,args)=>spawnSync(bin,args,{encoding:'utf8',timeout:30000});
const ffmpegReady=run('ffmpeg',['-version']).status===0 && run('ffprobe',['-version']).status===0;
function rms(pcm,from,to){
  const start=Math.floor(from*48000)*4, end=Math.floor(to*48000)*4;
  let sum=0,count=0;
  for(let i=start;i+1<Math.min(end,pcm.length);i+=2){
    const x=pcm.readInt16LE(i)/32768;sum+=x*x;count++;
  }
  return Math.sqrt(sum/Math.max(count,1));
}
test('FFmpeg real render: IN, delay, gain and exact PCM duration', {skip:!ffmpegReady}, async()=>{
  const dir=await mkdtemp(join(tmpdir(),'olympus-edit-audio-'));
  try{
    const src=join(dir,'source.wav'),out=join(dir,'render.wav'),raw=join(dir,'render.raw');
    let p=run('ffmpeg',['-nostdin','-hide_banner','-loglevel','error','-f','lavfi','-i','sine=frequency=440:duration=1.5:sample_rate=48000','-c:a','pcm_s16le','-y',src]);
    assert.equal(p.status,0,p.stderr);
    await renderAudio(src,out,{assetId:'fixture',inPoint:0.3,offset:0.25,volume:0.4},2);
    p=run('ffprobe',['-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',out]);
    assert.equal(p.status,0,p.stderr);
    assert.ok(Math.abs(Number(p.stdout.trim())-2)<0.02,'duration: '+p.stdout);
    p=run('ffmpeg',['-nostdin','-hide_banner','-loglevel','error','-i',out,'-f','s16le','-ac','2','-ar','48000','-y',raw]);
    assert.equal(p.status,0,p.stderr);
    const data=await readFile(raw);
    assert.equal(data.length,2*48000*2*2,'2 seconds stereo 16-bit');
    const before=rms(data,0.03,0.20),active=rms(data,0.40,0.65),after=rms(data,1.65,1.9);
    assert.ok(before<0.0002,'silence before offset: '+before);
    assert.ok(active>0.005&&active<0.06,'gain .4 must remain audible but attenuated: '+active);
    assert.ok(after<0.0002,'silence after source ends: '+after);
    console.log(JSON.stringify({duration:2,before,active,after}));
  }finally{await rm(dir,{recursive:true,force:true});}
});
