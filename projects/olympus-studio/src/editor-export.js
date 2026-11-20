// Export EDIT : ne jamais présenter un WebM silencieux comme un export A/V.
// Le navigateur doit annoncer explicitement un conteneur avec codec audio Opus.
export function selectEditorWebMMime(audioRequested, isTypeSupported) {
  if (typeof isTypeSupported !== 'function') throw new TypeError('Détection MediaRecorder indisponible');
  const candidates = audioRequested
    ? ['video/webm;codecs=vp8,opus', 'video/webm;codecs=vp9,opus']
    : ['video/webm;codecs=vp8', 'video/webm;codecs=vp9', 'video/webm'];
  const mime = candidates.find(type => isTypeSupported(type));
  if (!mime) {
    throw new Error(audioRequested
      ? 'Export A/V indisponible : aucun encodeur WebM avec Opus compatible'
      : 'Export WebM indisponible : aucun encodeur vidéo compatible');
  }
  return mime;
}
