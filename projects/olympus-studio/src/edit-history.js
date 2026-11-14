// EDIT history: bounded immutable snapshots of timeline metadata, never media bytes.
const clone = value => value == null ? null : JSON.parse(JSON.stringify(value));
export function snapshotEdit(clips, audioTrack) {
  if (!Array.isArray(clips)) throw new Error('Timeline invalide');
  return { clips: clone(clips), audioTrack: clone(audioTrack) };
}
export function createEditHistory(limit = 40) {
  if (!Number.isInteger(limit) || limit < 1 || limit > 200) throw new Error('Limite historique invalide');
  return { past: [], future: [], limit };
}
export function recordEdit(history, before, after) {
  const old = snapshotEdit(before.clips, before.audioTrack);
  const next = snapshotEdit(after.clips, after.audioTrack);
  if (JSON.stringify(old) === JSON.stringify(next)) return history;
  return { limit: history.limit, past: [...history.past, old].slice(-history.limit), future: [] };
}
export function undoEdit(history, current) {
  if (!history.past.length) return { history, snapshot: snapshotEdit(current.clips, current.audioTrack) };
  const snapshot = history.past[history.past.length - 1];
  return { snapshot: snapshotEdit(snapshot.clips, snapshot.audioTrack), history: {
    ...history, past: history.past.slice(0, -1), future: [...history.future, snapshotEdit(current.clips, current.audioTrack)].slice(-history.limit)
  }};
}
export function redoEdit(history, current) {
  if (!history.future.length) return { history, snapshot: snapshotEdit(current.clips, current.audioTrack) };
  const snapshot = history.future[history.future.length - 1];
  return { snapshot: snapshotEdit(snapshot.clips, snapshot.audioTrack), history: {
    ...history, past: [...history.past, snapshotEdit(current.clips, current.audioTrack)].slice(-history.limit), future: history.future.slice(0, -1)
  }};
}
