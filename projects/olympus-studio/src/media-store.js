// OLYMPUS Studio — persistent, local-only media library.
// Stores original Blob objects in IndexedDB and re-links scenes by stable IDs.
// No network access; the browser owns quotas and may evict local data.
export const MEDIA_DB_NAME = 'olympus-studio-assets';
export const MEDIA_DB_VERSION = 3;
export const PORTABLE_LIMIT = 45 * 1024 * 1024;

export function openMediaDB(indexedDBAPI = globalThis.indexedDB) {
  if (!indexedDBAPI) return Promise.reject(new Error('IndexedDB non disponible'));
  return new Promise((resolve, reject) => {
    const request = indexedDBAPI.open(MEDIA_DB_NAME, MEDIA_DB_VERSION);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains('assets')) db.createObjectStore('assets', { keyPath: 'id' });
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error || new Error('Ouverture IndexedDB impossible'));
  });
}

export function storeRequest(db, mode, action) {
  return new Promise((resolve, reject) => {
    const tx = db.transaction('assets', mode);
    const request = action(tx.objectStore('assets'));
    let value;
    request.onsuccess = () => { value = request.result; };
    tx.oncomplete = () => resolve(value);
    tx.onabort = () => reject(tx.error || new Error('Transaction annulée'));
    tx.onerror = () => reject(tx.error || new Error('Erreur de stockage local'));
  });
}

export function putMedia(db, media) {
  if (!media?.id || !media?.blob || !(media.blob instanceof Blob)) throw new Error('Média invalide');
  const record = { id: String(media.id), name: String(media.name || 'Média'), type: String(media.type || media.blob.type || 'application/octet-stream'), size: media.blob.size, blob: media.blob };
  return storeRequest(db, 'readwrite', store => store.put(record));
}
export function getMedia(db, id) { return storeRequest(db, 'readonly', store => store.get(id)); }
export function listMedia(db) { return storeRequest(db, 'readonly', store => store.getAll()); }
export function deleteMedia(db, id) { return storeRequest(db, 'readwrite', store => store.delete(id)); }

function b64(bytes) {
  const blocks = [];
  for (let i = 0; i < bytes.length; i += 49152) {
    blocks.push(btoa(String.fromCharCode(...bytes.subarray(i, i + 49152))));
  }
  return blocks.join('');
}

function bytesFromB64(data) {
  if (typeof data !== 'string' || !/^[A-Za-z0-9+/]*={0,2}$/.test(data) || data.length % 4 !== 0) throw new Error('Média portable base64 invalide');
  const output = new Uint8Array(Math.floor(data.length / 4) * 3 - (data.endsWith('==') ? 2 : data.endsWith('=') ? 1 : 0));
  for (let i = 0, offset = 0; i < data.length; i += 65536) {
    const chunk = atob(data.slice(i, i + 65536));
    for (let j = 0; j < chunk.length; j++) output[offset++] = chunk.charCodeAt(j);
  }
  return output;
}

export async function exportPortableAssets(records, maxBytes = PORTABLE_LIMIT) {
  if (!Array.isArray(records)) throw new Error('Liste de médias invalide');
  const total = records.reduce((sum, r) => sum + (r?.blob?.size ?? 0), 0);
  if (total > maxBytes) throw new Error('Projet portable limité à ' + Math.round(maxBytes / 1048576) + ' Mo de médias');
  const exported = [];
  for (const record of records) {
    if (!record || !(record.blob instanceof Blob)) continue;
    const bytes = new Uint8Array(await record.blob.arrayBuffer());
    exported.push({ id: String(record.id), name: String(record.name), type: String(record.type || record.blob.type || 'application/octet-stream'), size: bytes.length, data_b64: b64(bytes) });
  }
  return exported;
}

export function importPortableAsset(asset, maxBytes = PORTABLE_LIMIT) {
  if (!asset || typeof asset.id !== 'string' || typeof asset.name !== 'string' || typeof asset.data_b64 !== 'string') throw new Error('Entrée de média portable invalide');
  if (asset.data_b64.length > Math.ceil(maxBytes / 3) * 4 + 4) throw new Error('Média portable trop volumineux');
  const bytes = bytesFromB64(asset.data_b64);
  if (bytes.length > maxBytes || (Number.isInteger(asset.size) && bytes.length !== asset.size)) throw new Error('Taille du média portable incohérente');
  const type = typeof asset.type === 'string' && asset.type.length < 128 ? asset.type : 'application/octet-stream';
  return { id: asset.id, name: asset.name, type, size: bytes.length, blob: new Blob([bytes], { type }) };
}

export function mediaLayerUsable(record, layer) {
  if (!record || !layer) return false;
  return record.id === layer.id && typeof record.type === 'string' && (layer.type === 'image' && record.type.startsWith('image/') || layer.type === 'video' && record.type.startsWith('video/'));
}
