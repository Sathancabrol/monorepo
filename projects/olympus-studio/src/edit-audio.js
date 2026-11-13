// OLYMPUS Studio — one non-destructive audio track for EDIT (S04).
// All positions use timeline seconds; source bytes never change.
export function validateEditAudioTrack(track) {
  if (!track || typeof track.assetId !== 'string' || !track.assetId.trim()) {
    throw new Error('Piste audio invalide : média manquant');
  }
  const offset = Number(track.offset ?? 0);
  const inPoint = Number(track.inPoint ?? 0);
  const volume = Number(track.volume ?? 1);
  if (!Number.isFinite(offset) || offset < 0 || offset > 36000) throw new Error('Départ audio invalide');
  if (!Number.isFinite(inPoint) || inPoint < 0 || inPoint > 36000) throw new Error('Point IN audio invalide');
  if (!Number.isFinite(volume) || volume < 0 || volume > 1) throw new Error('Volume audio invalide');
  return {
    assetId: track.assetId,
    name: String(track.name || 'Piste audio'),
    offset,
    inPoint,
    volume,
    enabled: track.enabled !== false,
  };
}

// Return source position only while the audio should be playing.
// Unknown source duration is represented by null, NOT a fabricated length.
export function audioAtTimeline(track, time, sourceDuration = null) {
  if (!track || track.enabled === false) return { active: false, sourceTime: 0 };
  const start = Number(track.offset);
  const sourceStart = Number(track.inPoint);
  const t = Number(time);
  if (![start, sourceStart, t].every(Number.isFinite) || t < start || start < 0 || sourceStart < 0) {
    return { active: false, sourceTime: 0 };
  }
  const sourceTime = sourceStart + t - start;
  const sourceEnd = Number(sourceDuration);
  if (sourceDuration !== null && Number.isFinite(sourceEnd) && sourceTime >= sourceEnd) {
    return { active: false, sourceTime };
  }
  return { active: true, sourceTime };
}
