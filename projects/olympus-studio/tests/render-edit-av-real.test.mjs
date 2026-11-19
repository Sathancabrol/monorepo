import {test} from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {mkdtemp,readFile,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {renderEditAV} from '../scripts/render-edit-av.mjs';

const run=(bin,args)=>spawnSync(bin,args,{encoding:'utf8',timeout:90000});
const ready=run('ffmpeg',['-version']).status===0&&run('ffprobe',['-version']).status===0;
test('EDIT offline bridge produces VP9/Opus with timeline audio and preserves sources', {skip:!ready}, async()=>{
  const dir=await mkdtemp(join(tmpdir(),'olympus-av-bridge-test-'));
  try{
    const video=join(dir,'video.webm'),audio=join(dir,'audio.wav'),out=join(dir,'output.webm');
    let p=run('ffmpeg',['-nostdin','-hide_banner','-loglevel','error','-f','lavfi','-i','color=c=blue:s=160x90:r=15:d=2','-c:v','libvpx-vp9','-an','-y',video]);
    assert.equal(p.status,0,p.stderr);
    p=run('ffmpeg',['-nostdin','-hide_banner','-loglevel','error','-f','lavfi','-i','sine=frequency=440:duration=1.5','-c:a','pcm_s16le','-y',audio]);
    assert.equal(p.status,0,p.stderr);
    const before=[await readFile(video),await readFile(audio)];
    const track={assetId:'fixture',inPoint:0.2,offset:0.25,volume:0.4};
    assert.equal(await renderEditAV(video,audio,track,2,out),out);
    p=run('ffprobe',['-v','error','-show_streams','-of','json',out]);
    assert.equal(p.status,0,p.stderr);
    const streams=JSON.parse(p.stdout).streams;
    assert.ok(streams.some(s=>s.codec_type==='video'&&s.codec_name==='vp9'));
    assert.ok(streams.some(s=>s.codec_type==='audio'&&s.codec_name==='opus'));
    assert.deepEqual(await readFile(video),before[0]);
    assert.deepEqual(await readFile(audio),before[1]);
    await assert.rejects(renderEditAV(video,audio,track,2,out),/sortie existante/);
    assert.ok((await readFile(out)).length>100);
  }finally{await rm(dir,{recursive:true,force:true});}
});
test('EDIT bridge rejects invalid paths before running FFmpeg',async()=>{
  await assert.rejects(renderEditAV('same.webm','sound.wav',{assetId:'x'},2,'same.webm'),/invalides/);
});
