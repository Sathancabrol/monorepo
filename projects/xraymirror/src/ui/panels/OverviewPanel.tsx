import { useMemo } from 'react';
import { Activity, Aperture, Bone, Boxes, Brain, Barcode, AudioWaveform, Download, Paintbrush, ScanFace, ShieldCheck } from 'lucide-react';
import { Card } from '../components';
import type { StudioState } from '../useStudio';
import { PLUGIN_CATALOG } from '../../core/pluginCatalog';
import { downloadText } from '../../core/clientStore';
import { formatCoverage, buildSkeletalAnchors, coverageFromBones } from '../../core/anatomy';

export function OverviewPanel({ state, getExport, onGrab }: { state: StudioState; getExport: () => string; onGrab: () => void }) {
  const counts = useMemo(() => {
    const types = ['face.detected', 'hand.detected', 'pose.detected', 'object.detected', 'sound.detected', 'hand.gesture'];
    return types.map((type) => ({ type, count: state.events.filter((event) => event.type === type).length }));
  }, [state.events]);

  const bones = state.snapshot.pose.length ? buildSkeletalAnchors(state.snapshot.pose) : [];
  const coverage = coverageFromBones(bones);
  const ready = PLUGIN_CATALOG.filter((plugin) => plugin.status === 'ready' || plugin.status === 'core').length;
  const planned = PLUGIN_CATALOG.filter((plugin) => plugin.status === 'planned').length;

  return (
    <>
      <Card title="Socle Studio" icon={<Aperture size={14} color="var(--accent)" />} subtitle="État réel du prototype, sans pourcentage d’achèvement inventé">
        <div className="metrics-grid">
          <div className="metric"><div className="k">Plugins prêts</div><div className="v">{ready}<small>/{PLUGIN_CATALOG.length}</small></div></div>
          <div className="metric"><div className="k">Prévus</div><div className="v">{planned}</div></div>
          <div className="metric"><div className="k">Événements</div><div className="v">{state.events.length}</div></div>
          <div className="metric"><div className="k">Rendu</div><div className="v">{state.fps}<small>fps</small></div></div>
        </div>
        <div className="inline" style={{ marginTop: 9 }}>
          <button className="btn" onClick={onGrab}><Download size={13} /> Capture PNG</button>
          <button className="btn" onClick={() => downloadText(`xraymirror-events-${Date.now()}.jsonl`, getExport(), 'application/x-ndjson')}><Activity size={13} /> Export JSONL</button>
        </div>
        <div className="note" style={{ marginTop: 9 }}>
          Ce dossier est une base autonome v0.7 expérimentale. Il ne remplace pas les checkpoints v0.6.0 testés par Hermes et ne prétend pas restaurer les 634 structures Écorché.
        </div>
      </Card>

      <Card title="Détections cumulées" icon={<Activity size={14} color="var(--accent-2)" />}>
        <div className="bars">
          {counts.map((entry) => {
            const max = Math.max(1, ...counts.map((item) => item.count));
            return (
              <div className="bar-row" key={entry.type}>
                <span>{entry.type.replace('.detected', '')}</span>
                <div className="track"><span style={{ width: `${(entry.count / max) * 100}%` }} /></div>
                <span className="val">{entry.count}</span>
              </div>
            );
          })}
        </div>
      </Card>

      <Card title="Accès rapides" icon={<Boxes size={14} color="var(--accent)" />}>
        <div className="list">
          <div className="row"><ScanFace size={13} color="var(--accent)" /><div className="grow"><div className="t">Visage</div><div className="s">{state.snapshot.face.length ? `${state.snapshot.face.length} points` : 'aucun visage'}</div></div></div>
          <div className="row"><Paintbrush size={13} color="var(--accent-2)" /><div className="grow"><div className="t">AirPaint</div><div className="s">pincement pour tracer</div></div></div>
          <div className="row"><Bone size={13} color="var(--accent)" /><div className="grow"><div className="t">Anatomie</div><div className="s">{state.snapshot.pose.length ? formatCoverage(coverage) : 'pose requise'}</div></div></div>
          <div className="row"><Barcode size={13} color="var(--accent-2)" /><div className="grow"><div className="t">Nutrition</div><div className="s">Open Food Facts à la demande</div></div></div>
          <div className="row"><AudioWaveform size={13} color="var(--warn)" /><div className="grow"><div className="t">Sons</div><div className="s">{state.microphone}</div></div></div>
          <div className="row"><Brain size={13} color="var(--accent)" /><div className="grow"><div className="t">Cognition</div><div className="s">exercices expérimentaux</div></div></div>
          <div className="row"><ShieldCheck size={13} color="var(--ok)" /><div className="grow"><div className="t">Confidentialité</div><div className="s">aucune vidéo transmise</div></div></div>
        </div>
      </Card>
    </>
  );
}
