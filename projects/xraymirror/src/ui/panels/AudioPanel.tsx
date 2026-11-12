import { AudioWaveform, Mic, Volume2 } from 'lucide-react';
import { Card, Toggle } from '../components';
import type { StudioState } from '../useStudio';

export function AudioPanel({ state, onToggle }: { state: StudioState; onToggle: () => void }) {
  const lastSounds = state.events.filter((event) => event.type === 'sound.detected').slice(-6).reverse();
  const sounds = state.events.filter((event) => event.type === 'sound.detected').length;
  return (
    <>
      <Card title="Micro & événements sonores" icon={<Mic size={14} color="var(--accent)" />} subtitle="Aucun flux audio n’est envoyé au réseau">
        <Toggle label="Activer le microphone" hint="Nécessite de relancer la caméra" checked={state.settings.detectors.audio} onChange={onToggle} disabled={state.running} />
        <div className="field" style={{ marginTop: 8 }}>
          <label>Niveau · {state.microphone === 'granted' ? 'en direct' : 'inactif'}</label>
          <div className="sound-meter">
            {state.audioLevels.map((level, index) => (
              <span key={index} style={{ height: `${Math.max(3, level * 24)}px` }} />
            ))}
          </div>
        </div>
        <div className="metrics-grid" style={{ marginTop: 9 }}>
          <div className="metric"><div className="k">Événements son</div><div className="v">{sounds}</div></div>
          <div className="metric"><div className="k">Micro</div><div className="v" style={{ fontSize: 13 }}>{state.microphone}</div></div>
        </div>
      </Card>

      <Card title="Derniers transitoires" icon={<Volume2 size={14} color="var(--warn)" />} subtitle="Détection amplitude locale, pas de transcription">
        <div className="list">
          {lastSounds.length === 0 && <div className="empty"><AudioWaveform size={18} style={{ opacity: 0.5, marginBottom: 6 }} /><div>Aucun événement. Claque des mains près du micro.</div></div>}
          {lastSounds.map((event) => (
            <div className="row" key={event.id}>
              <AudioWaveform size={12} color="var(--warn)" />
              <div className="grow">
                <div className="t">{event.label ?? 'transitoire'}</div>
                <div className="s">{new Date(event.timestamp).toLocaleTimeString('fr-FR', { hour12: false })} · {Math.round((event.confidence ?? 0) * 100)} %</div>
              </div>
              <span className="status-dot warn" />
            </div>
          ))}
        </div>
        <div className="note warn" style={{ marginTop: 9 }}>
          Ce module détecte surtout les attaques courtes de type claquement. Cette version ne contient pas de classifieur YAMNet/BEATs et ne prétend pas identifier tous les sons.
        </div>
      </Card>
    </>
  );
}
