import { test } from 'node:test';
import assert from 'node:assert/strict';
import { selectEditorWebMMime } from '../src/editor-export.js';

test('Export audio exige un WebM explicitement compatible Opus', () => {
  const supports = x => ['video/webm', 'video/webm;codecs=vp8'].includes(x);
  assert.throws(() => selectEditorWebMMime(true, supports), /Opus/);
  assert.equal(selectEditorWebMMime(false, supports), 'video/webm;codecs=vp8');
});

test('Export audio sélectionne VP8+Opus puis VP9+Opus sans repli silencieux', () => {
  assert.equal(selectEditorWebMMime(true, x => x.includes('vp8,opus')), 'video/webm;codecs=vp8,opus');
  assert.equal(selectEditorWebMMime(true, x => x.includes('vp9,opus')), 'video/webm;codecs=vp9,opus');
  assert.throws(() => selectEditorWebMMime(true, () => false), /Opus/);
});

test('Aucun format vidéo pris en charge provoque une erreur explicite', () => {
  assert.throws(() => selectEditorWebMMime(false, () => false), /WebM/);
  assert.throws(() => selectEditorWebMMime(false, null), /MediaRecorder/);
});

test('Capture EDIT: marqueur change à chaque image, indépendamment du temps RAF', async () => {
  const { readFile } = await import('node:fs/promises');
  const source = await readFile(new URL('../src/app.js', import.meta.url), 'utf8');
  assert.match(source, /let editorCaptureFrame=0;/);
  assert.match(source, /const marker=\+\+editorCaptureFrame;/);
  assert.doesNotMatch(source, /const marker=Math\.floor\(now\/32\)%2;/);
  const nextMarker = (() => { let frame = 0; return () => ++frame; })();
  const repeatedTimestamp = [320, 320, 320, 320];
  assert.deepEqual(repeatedTimestamp.map(() => nextMarker()), [1, 2, 3, 4]);
});


test('EDIT termine la capture après avoir dessiné et demandé la dernière image', async () => {
  const { readFile } = await import('node:fs/promises');
  const source = await readFile(new URL('../src/app.js', import.meta.url), 'utf8');
  const draw = source.slice(source.indexOf('function drawEditor(now){'), source.indexOf('let editorExportPreparing=false;'));
  const end = draw.indexOf('const reachedEnd=total>0&&state.editTime>=total;');
  const frame = draw.lastIndexOf('editorVideoCaptureTrack?.requestFrame?.();');
  const stop = draw.indexOf("if(reachedEnd&&editorRecorder?.state==='recording'&&!editorExportFinalizing){");
  assert.ok(end>=0 && frame>end && stop>frame, 'stop doit suivre le dessin et la demande de trame finale');
  assert.doesNotMatch(draw.slice(0, frame), /editorRecorder\.stop\(\)/);
  assert.match(draw, /requestAnimationFrame\(\(\)=>\{/);
  assert.match(draw, /setTimeout\(\(\)=>\{if\(recorder\.state==='recording'\)recorder\.stop\(\);editorExportFinalizing=false;\},120\)/);
});
