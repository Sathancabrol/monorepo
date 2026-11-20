// Pure, non-executing bridge from the EDIT audio contract to the local FFmpeg CLI.
// Paths are deliberate placeholders: browser media never becomes an arbitrary disk path.
import { validateEditAudioTrack } from './edit-audio.js';

export function editFfmpegPlan(track, duration) {
  if (!Number.isFinite(duration) || duration <= 0 || duration > 120) {
    throw new Error('Durée du montage invalide pour FFmpeg');
  }
  const seconds = duration.toFixed(6);
  const mux = 'python tools/ffmpeg_mux_fallback.py --frames-dir "CHEMIN_DOSSIER_PNG" --fps 24 --audio "audio_prepare.wav" --output "montage.webm" --av-report --max-end-delta 0.2';
  if (!track || track.enabled === false) {
    return {
      audio: false,
      prepare: null,
      mux: mux.replace(' --audio "audio_prepare.wav"', ''),
      warning: 'Aucune piste audio active : sortie vidéo sans son.',
    };
  }
  const t = validateEditAudioTrack(track);
  return {
    audio: true,
    prepare: 'python tools/prepare_edit_audio.py --source "CHEMIN_AUDIO_SOURCE" --output "audio_prepare.wav"'
      + ' --offset ' + t.offset.toFixed(6)
      + ' --in-point ' + t.inPoint.toFixed(6)
      + ' --volume ' + t.volume.toFixed(6)
      + ' --duration ' + seconds,
    mux,
    warning: 'Exporter la source audio de LIBRARY puis renseigner son chemin local. Vérifier le WAV préparé avant le mux. Aucun fichier source modifié.',
  };
}
