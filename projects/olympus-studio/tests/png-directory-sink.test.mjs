import test from 'node:test';
import assert from 'node:assert/strict';
import { createPngDirectorySink } from '../src/png-directory-sink.js';

const png = new Blob(['png'], { type: 'image/png' });
function directory(existing = []) {
  const files = new Set(existing), writes = [];
  return {
    files, writes,
    async getFileHandle(name, { create } = {}) {
      if (!files.has(name) && !create) {
        const error = new Error('missing'); error.name = 'NotFoundError'; throw error;
      }
      if (create) files.add(name);
      return { async createWritable() {
        return { async write(data) { writes.push([name, data]); },
          async close() {}, async abort() {} };
      } };
    }
  };
}
test('explicit directory sink writes ordered PNGs without overwrite', async () => {
  const dir = directory(), sink = createPngDirectorySink(dir);
  await sink({ filename:'000001.png', index:0, png });
  await sink({ filename:'000002.png', index:1, png });
  assert.deepEqual(dir.writes.map(x => x[0]), ['000001.png','000002.png']);
});
test('rejects existing file before opening writable stream', async () => {
  const dir = directory(['000001.png']), sink = createPngDirectorySink(dir);
  await assert.rejects(sink({ filename:'000001.png', index:0, png }), /already exists/);
  assert.equal(dir.writes.length, 0);
});
test('rejects path traversal, out of order, invalid PNG and limits', async () => {
  const dir = directory(), sink = createPngDirectorySink(dir, { maxFrames:1 });
  await assert.rejects(sink({ filename:'../evil.png', index:0, png }), /sequential/);
  await assert.rejects(sink({ filename:'000001.png', index:0, png:new Blob(['x']) }), /PNG Blob/);
  await sink({ filename:'000001.png', index:0, png });
  await assert.rejects(sink({ filename:'000002.png', index:1, png }), /limit/);
  assert.equal(dir.writes.length, 1);
});
test('permission errors propagate without creating output', async () => {
  const denied = { async getFileHandle() { const e = new Error('denied'); e.name='NotAllowedError'; throw e; } };
  await assert.rejects(createPngDirectorySink(denied)({ filename:'000001.png', index:0, png }), /denied/);
});
