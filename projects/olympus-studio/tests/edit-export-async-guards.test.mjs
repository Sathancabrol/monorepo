import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

// Regression guard: both asynchronous media-loading handlers must recheck
// export state after their await, before they mutate the storyboard.
const source = readFileSync(new URL('../src/app.js', import.meta.url), 'utf8');
function handler(start, end) {
  const begin = source.indexOf(start);
  assert.ok(begin >= 0, 'handler missing: ' + start);
  const finish = source.indexOf(end, begin);
  assert.ok(finish > begin, 'handler boundary missing: ' + end);
  return source.slice(begin, finish);
}
test('async audio assignment rechecks export state after media loading', () => {
  const body = handler('assign.onclick=async()=>{', 'audioPanel.append(audioSelect,assign)');
  const awaited = body.indexOf('await loadEditAsset(asset.id)');
  const guard = body.indexOf("editorRecorder?.state==='recording'", awaited);
  const mutation = body.indexOf('state.editAudioTrack=validateEditAudioTrack');
  assert.ok(awaited >= 0 && guard > awaited && mutation > guard);
});
test('async video clip creation rechecks export state after metadata loading', () => {
  const body = handler('add.onclick=async()=>{', 'wrap.append(select,add)');
  const awaited = body.indexOf('await ensureVideoDuration(asset.id,media)');
  const guard = body.indexOf("editorRecorder?.state==='recording'", awaited);
  const mutation = body.indexOf('state.clips.push');
  assert.ok(awaited >= 0 && guard > awaited && mutation > guard);
});

test('all EDIT recording mutation guards also cover asynchronous preparation', () => {
  const recordingGuard = "if(editorRecorder?.state==='recording')";
  assert.equal(source.includes(recordingGuard), false, 'unguarded recording-only mutation remains');
  const combined = "if(editorExportPreparing||editorRecorder?.state==='recording')";
  assert.ok(source.split(combined).length - 1 >= 10, 'expected EDIT mutation guards');
});
test('async asset assignment checks preparation lock after await', () => {
  for (const [start, end, mutation] of [
    ['assign.onclick=async()=>{', 'audioPanel.append(audioSelect,assign)', 'state.editAudioTrack=validateEditAudioTrack'],
    ['add.onclick=async()=>{', 'wrap.append(select,add)', 'state.clips.push'],
  ]) {
    const body = handler(start, end);
    const awaitIndex = body.indexOf('await loadEditAsset(asset.id)');
    const lockIndex = body.indexOf("if(editorExportPreparing||editorRecorder?.state==='recording')", awaitIndex);
    const mutationIndex = body.indexOf(mutation);
    assert.ok(awaitIndex >= 0 && lockIndex > awaitIndex && mutationIndex > lockIndex, start);
  }
});
