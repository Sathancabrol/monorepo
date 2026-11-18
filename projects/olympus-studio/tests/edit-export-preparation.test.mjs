import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

// Guard against the asynchronous media-loading race: a user may replace the
// soundtrack while IndexedDB or AudioContext is still being prepared.
const app = readFileSync(new URL('../src/app.js', import.meta.url), 'utf8');
const exportBody = app.slice(app.indexOf('async function exportEditorWebM('), app.indexOf('\nfunction draw(){'));
test('EDIT export serializes concurrent preparation and recording', () => {
  assert.match(exportBody, /editorExportPreparing\|\|editorRecorder\?\.state==='recording'/);
  assert.match(exportBody, /editorExportPreparing=true/);
  assert.match(exportBody, /finally\s*\{\s*editorExportPreparing=false/);
});
test('EDIT export revalidates audio after each asynchronous boundary', () => {
  assert.match(exportBody, /const requestedAudio=state\.editAudioTrack\?\{\.\.\.state\.editAudioTrack\}:null/);
  const checks = exportBody.match(/JSON\.stringify\(state\.editAudioTrack\)!==JSON\.stringify\(requestedAudio\)/g) || [];
  assert.ok(checks.length >= 3, 'must revalidate after load, graph setup and before recorder start');
  assert.match(exportBody, /loadEditAsset\(requestedAudio\.assetId\)/);
  assert.match(exportBody, /attachAudioToEditorCapture\(stream,audio,requestedAudio\.volume\)/);
});
