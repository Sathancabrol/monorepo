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
