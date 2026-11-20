import {test} from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {mkdtemp,mkdir,readFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {renderSequenceAV} from '../scripts/render-edit-sequence-av.mjs';
const run=(bin,args)=>spawnSync(bin,args,{encoding:'utf8',timeout:90000});
const ready=run('ffmpeg',['-version']).status===0&&run('ffprobe',['-version']).status===0;
test('numbered PNG sequence and timeline WAV yield VP9/Opus WebM without overwriting inputs', {skip:!ready},async()=>{
 const root=await mkdtemp(join(tmpdir(),'olympus-seq-av-test-'));
 try{
  const frames=join(root,'frames');await mkdir(frames);
  for(let i=1;i<=4;i++){
   const path=join(frames,String(i).padStart(6,'0')+'.png');
   const p=run('ffmpeg',['-nostdin','-hide_banner','-loglevel','error','-f','lavfi','-i','color=c=blue:s=64x64','-frames:v','1','-update','1','-y',path]);
   assert.equal(p.status,0,p.stderr);
  }
  const audio=join(root,'tone.wav'),out=join(root,'final.webm');
  const p=run('ffmpeg',['-nostdin','-hide_banner','-loglevel','error','-f','lavfi','-i','sine=frequency=440:duration=0.8','-y',audio]);
  assert.equal(p.status,0,p.stderr);
  const before=await readFile(audio);
  const track={assetId:'fixture',inPoint:0.1,offset:0.2,volume:0.5};
  const result=await renderSequenceAV(frames,4,1,audio,track,out);
  assert.equal(result.frames,4);
  const probe=run('ffprobe',['-v','error','-count_frames','-show_entries','stream=codec_type,codec_name,nb_read_frames','-show_entries','format=duration','-of','json',out]);
  assert.equal(probe.status,0,probe.stderr);
  const data=JSON.parse(probe.stdout);
  assert.ok(data.streams.some(s=>s.codec_type==='video'&&s.codec_name==='vp9'&&Number(s.nb_read_frames)===4));
  assert.ok(data.streams.some(s=>s.codec_type==='audio'&&s.codec_name==='opus'));
  assert.ok(Math.abs(Number(data.format.duration)-1)<0.2);
  assert.deepEqual(await readFile(audio),before);
  const saved=await readFile(out);
  await assert.rejects(renderSequenceAV(frames,4,1,audio,track,out),/Sortie existante/);
  assert.deepEqual(await readFile(out),saved);
 }finally{await rm(root,{recursive:true,force:true});}
});
test('sequence bridge rejects invalid duration and output paths before invoking tools',async()=>{
 await assert.rejects(renderSequenceAV('frames',30,121,'audio.wav',{},'out.webm'),/Durée/);
 await assert.rejects(renderSequenceAV('frames',4,1,'audio.wav',{},'out.mp4'),/Chemins invalides/);
});
