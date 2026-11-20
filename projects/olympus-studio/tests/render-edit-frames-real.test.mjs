import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,rm,readFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {spawnSync} from 'node:child_process';
import {framePlan,renderFrames} from '../scripts/render-edit-frames.mjs';
const has=b=>spawnSync(b,['-version'],{stdio:'ignore'}).status===0;
test('frame plan validates finite bounded cadence and duration',()=>{
  assert.deepEqual(framePlan(10,1.2),{rate:10,count:12,duration:1.2});
  for(const [fps,duration] of [[0,1],[61,1],[30,0],[30,121],['x',1],[30,Infinity]])
    assert.throws(()=>framePlan(fps,duration));
});
test('numbered PNG frames produce deterministic VP9 duration, without overwrite', {skip:!has('ffmpeg')||!has('ffprobe')},async()=>{
  const root=await mkdtemp(join(tmpdir(),'olympus-frames-test-'));
  try{
    const frames=join(root,'frames');await mkdir(frames);
    const output=join(root,'out.webm');
    await assert.rejects(renderFrames(frames,4,1,output),/Séquence PNG/);
    for(let i=1;i<=4;i++){
      const name=join(frames,String(i).padStart(6,'0')+'.png');
      const p=spawnSync('ffmpeg',['-hide_banner','-loglevel','error','-f','lavfi','-i','color=c=blue:s=64x64','-frames:v','1','-update','1','-y',name]);
      assert.equal(p.status,0,p.stderr?.toString());
    }
    const rendered=await renderFrames(frames,4,1,output);
    assert.equal(rendered.count,4);
    const probe=spawnSync('ffprobe',['-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=codec_name,nb_read_frames,duration','-show_entries','format=duration','-of','json',output],{encoding:'utf8'});
    assert.equal(probe.status,0,probe.stderr);
    const data=JSON.parse(probe.stdout);
    assert.equal(data.streams[0].codec_name,'vp9');
    assert.equal(Number(data.streams[0].nb_read_frames),4);
    assert.ok(Math.abs(Number(data.format.duration)-1)<0.15);
    const original=await readFile(output);
    await assert.rejects(renderFrames(frames,4,1,output),/FFmpeg/);
    assert.deepEqual(await readFile(output),original);
  }finally{await rm(root,{recursive:true,force:true});}
});
