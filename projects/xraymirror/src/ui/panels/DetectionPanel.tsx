import { Activity, Aperture, Boxes, Gauge, Hand, ScanFace } from 'lucide-react';
import { Card, Toggle } from '../components';
import type { StudioState } from '../useStudio';
import type { DetectorSettings } from '../../core/types';

const LABELS: Array<{ key: keyof DetectorSettings; label: string; hint: string }> = [
  { key: 'face', label: 'Visage & expressions', hint: '478 points, 52 blendshapes' },
  { key: 'hands', label: 'Mains', hint: '21 points/main + pincement' },
  { key: 'pose', label: 'Corps', hint: 'Pose 33 points, cadence réduite' },
  { key: 'objects', label: 'Objets COCO', hint: 'EfficientDet Lite0, 80 classes' },
  { key: 'gestures', label: 'Gestes MediaPipe', hint: 'Modèle supplémentaire, plus lourd' },
  { key: 'audio', label: 'Microphone & sons', hint: 'Niveau + transitoires locaux' },
];

export function DetectionPanel({
  state,
  onToggle,
}: {
  state: StudioState;
  onToggle: (key: keyof DetectorSettings) => void;
}) {
  const inference = Object.entries(state.latency);
  return (
    <>
      <Card title="Modules actifs" icon={<Aperture size={14} color="var(--accent)" />} subtitle="Activation au prochain démarrage">
        {LABELS.map((item) => (
          <Toggle
            key={item.key}
            label={item.label}
            hint={item.hint}
            checked={state.settings.detectors[item.key]}
            onChange={() => onToggle(item.key)}
            disabled={state.running && item.key !== 'audio'}
          />
        ))}
        {state.running && <div className="note" style={{ marginTop: 8 }}>Arrête la caméra pour modifier les moteurs, sauf le micro.</div>}
      </Card>

      <Card
        title="Latences par moteur"
        icon={<Gauge size={14} color="var(--accent-2)" />}
        subtitle="Temps observé, une seule inférence"
      >
        {inference.length === 0 ? (
          <div className="empty">Aucune mesure pour l’instant. Démarre la caméra.</div>
        ) : (
          <div className="bars">
            {inference.map(([kind, stats]) => (
              <div className="bar-row" key={kind}>
                <span>{kind}</span>
                <div className="track"><span style={{ width: `${Math.min(100, (stats.p95 / 80) * 100)}%` }} /></div>
                <span className="val">p95 {stats.p95} ms</span>
              </div>
            ))}
          </div>
        )}
        {inference.length > 0 && (
          <div className="note" style={{ marginTop: 8 }}>
            p50/p95 sur les 120 dernières inférences de chaque moteur — mesure réelle dans ce navigateur, pas un chiffre constructeur.
          </div>
        )}
        <div className="metrics-grid" style={{ marginTop: 10 }}>
          <div className="metric"><div className="k">Rendu</div><div className="v">{state.fps}<small>fps</small></div></div>
          <div className="metric"><div className="k">Inférence cumulée</div><div className="v">{state.inferenceMs}<small>ms</small></div></div>
          <div className="metric"><div className="k">Visage</div><div className="v">{state.snapshot.face.length >= 400 ? `${state.snapshot.face.length}` : '—'}<small>pts</small></div></div>
          <div className="metric"><div className="k">Mains</div><div className="v">{state.snapshot.hands.length}<small>/2</small></div></div>
        </div>
      </Card>

      <Card title="Provenance des données" icon={<Activity size={14} color="var(--warn)" />}>
        <div className="list">
          <div className="row"><ScanFace size={14} color="var(--accent)" /><div className="grow"><div className="t">Visage</div><div className="s">MediaPipe local (WASM/WebGL)</div></div><span className={`status-dot ${state.engineStatus.face === 'prêt' ? 'ready' : ''}`} /></div>
          <div className="row"><Hand size={14} color="var(--accent-2)" /><div className="grow"><div className="t">Mains</div><div className="s">MediaPipe local (WASM/WebGL)</div></div><span className={`status-dot ${state.engineStatus.hands === 'prêt' ? 'ready' : ''}`} /></div>
          <div className="row"><Boxes size={14} color="var(--warn)" /><div className="grow"><div className="t">Objets</div><div className="s">EfficientDet local, aucune image envoyée</div></div><span className={`status-dot ${state.engineStatus.objects === 'prêt' ? 'ready' : ''}`} /></div>
        </div>
        <div className="note" style={{ marginTop: 9 }}>
          Les modèles sont téléchargés à la première utilisation (URL épinglées) puis mis en cache par le navigateur. Le traitement vidéo reste local.
        </div>
      </Card>
    </>
  );
}
