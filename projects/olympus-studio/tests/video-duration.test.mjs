import { test } from 'node:test';
import assert from 'node:assert/strict';
import { finiteVideoDuration, readVideoDuration, initialClipDuration, trimWithinVideoDuration, setClipDuration } from '../src/video-duration.js';

class FakeVideo extends EventTarget {
  constructor(duration = NaN) {
    super();
    this.duration = duration;
  }
  setDuration(duration, event = 'loadedmetadata') {
    this.duration = duration;
    this.dispatchEvent(new Event(event));
  }
}

test('Durée source : refuse zéro, NaN, Infinity et accepte les secondes réelles', () => {
  assert.equal(finiteVideoDuration(13.75), 13.75);
  assert.equal(finiteVideoDuration('2.5'), 2.5);
  for (const value of [undefined, null, '', -5, 0, 0.09, NaN, Infinity, -Infinity]) {
    assert.equal(finiteVideoDuration(value), null);
  }
  assert.equal(initialClipDuration(2.4), 2.4);
  assert.equal(initialClipDuration(99), 5);
  assert.equal(initialClipDuration(null), 5);
});

test('Lecture immédiate des métadonnées déjà disponibles', async () => {
  assert.equal(await readVideoDuration(new FakeVideo(3.5), 50), 3.5);
  await assert.rejects(readVideoDuration(null), /invalide/);
});

test('Lecture asynchrone des métadonnées vidéo et réaction aux changements de durée', async () => {
  const video = new FakeVideo();
  const result = readVideoDuration(video, 150);
  queueMicrotask(() => video.setDuration(7.25));
  assert.equal(await result, 7.25);
  // Remove listeners after resolution: new duration does not alter the resolved value.
  video.setDuration(8.5, 'durationchange');
  assert.equal(await result, 7.25);

  const video2 = new FakeVideo();
  const result2 = readVideoDuration(video2, 150);
  queueMicrotask(() => video2.setDuration(4, 'durationchange'));
  assert.equal(await result2, 4);
});

test('Média illisible ou sans metadata : erreur explicite et délai borné', async () => {
  const broken = new FakeVideo();
  const p = readVideoDuration(broken, 100);
  queueMicrotask(() => broken.dispatchEvent(new Event('error')));
  await assert.rejects(p, /Impossible de lire/);

  await assert.rejects(readVideoDuration(new FakeVideo(), 15), /Durée vidéo inconnue/);
});

test('Contrôle IN/OUT : rejette les bornes au-delà du fichier source', () => {
  const clip = { id: 'clipA', assetId: 'media', kind: 'video', inPoint: 0, outPoint: 5, duration: 5 };
  const result = trimWithinVideoDuration(clip, 1.1, 2.5, 2.5);
  assert.equal(result.inPoint, 1.1);
  assert.equal(result.outPoint, 2.5);
  assert.equal(clip.outPoint, 5); // never mutate source
  assert.throws(() => trimWithinVideoDuration(clip, 1, 3, 2.5), /dépasse la durée source/);
  assert.throws(() => trimWithinVideoDuration(clip, 2, 2.05, 8), /invalide/);
  assert.throws(() => trimWithinVideoDuration(clip, 3, 2, null), /invalide/);
  assert.equal(trimWithinVideoDuration(clip, 1, 3, null).outPoint, 3);
});

test('Champ durée EDIT : ne peut pas contourner les bornes source et reste non destructif', () => {
  const video = { id: 'v', assetId: 'file', kind: 'video', inPoint: 1.5, outPoint: 4.5, duration: 3 };
  const changed = setClipDuration(video, 1.25, 3);
  assert.equal(changed.outPoint, 2.75);
  assert.equal(changed.inPoint, 1.5);
  assert.equal(video.outPoint, 4.5);
  assert.throws(() => setClipDuration(video, 3, 3), /dépasse la durée source/);
  assert.throws(() => setClipDuration(video, Infinity, 3), /invalide/);
  assert.throws(() => setClipDuration(video, 0.05, 3), /invalide/);
  assert.deepEqual(setClipDuration({ id:'i', kind:'image', duration:5 }, 8, null), { id:'i', kind:'image', duration:8 });
  assert.throws(() => setClipDuration({ kind:'audio' }, 2, null), /non pris en charge/);
});
