// File System Access API sink for the deterministic EDIT PNG renderer.
// The caller must obtain a user-chosen directory handle via showDirectoryPicker.
// No implicit filesystem access, no overwrites, and no deletion on failure.
const PNG_NAME = /^\d{6}\.png$/;

export function createPngDirectorySink(directory, { maxFrames = 7200 } = {}) {
  if (!directory || typeof directory.getFileHandle !== 'function')
    throw new TypeError('User-selected directory handle required');
  if (!Number.isInteger(maxFrames) || maxFrames < 1 || maxFrames > 7200)
    throw new RangeError('Invalid frame limit');
  let next = 1;
  return async function writeFrame({ filename, index, png }) {
    const expected = String(next).padStart(6, '0') + '.png';
    if (!PNG_NAME.test(filename) || filename !== expected || index !== next - 1)
      throw new Error('PNG frames must be sequential and start at 000001.png');
    if (next > maxFrames) throw new RangeError('Frame limit exceeded');
    if (!(png instanceof Blob) || png.type !== 'image/png' || png.size === 0)
      throw new TypeError('Nonempty PNG Blob required');
    // Check without create first; a pre-existing file must never be truncated.
    try {
      await directory.getFileHandle(filename, { create: false });
    } catch (error) {
      if (error?.name !== 'NotFoundError') throw error;
      const handle = await directory.getFileHandle(filename, { create: true });
      const writable = await handle.createWritable({ keepExistingData: false });
      try {
        await writable.write(png);
        await writable.close();
      } catch (writeError) {
        try { await writable.abort(); } catch { /* preserve original failure */ }
        throw writeError;
      }
      next++;
      return;
    }
    throw new Error('Output file already exists: ' + filename);
  };
}
