import { Bone, Layers3, Ruler, ScanEye } from 'lucide-react';
import { Card, Toggle } from '../components';
import { ANATOMY_LAYERS, buildSkeletalAnchors, coverageFromBones, formatCoverage } from '../../core/anatomy';
import type { StudioState } from '../useStudio';

export function AnatomyPanel({
  state,
  onChange,
}: {
  state: StudioState;
  onChange: (updater: (current: StudioState['settings']) => StudioState['settings']) => void;
}) {
  const bones = state.snapshot.pose.length ? buildSkeletalAnchors(state.snapshot.pose) : [];
  const coverage = coverageFromBones(bones);
  const layers = state.settings.anatomy.layers;

  return (
    <>
      <Card title="Couches anatomiques" icon={<Layers3 size={14} color="var(--accent)" />} subtitle="Schématique, éducatif, non clinique">
        <div className="anatomy-list">
          {ANATOMY_LAYERS.map((layer) => (
            <label className="anatomy-layer" key={layer.id}>
              <input
                type="checkbox"
                checked={Boolean(layers[layer.id])}
                onChange={() =>
                  onChange((current) => ({
                    ...current,
                    anatomy: {
                      ...current.anatomy,
                      layers: { ...current.anatomy.layers, [layer.id]: !current.anatomy.layers[layer.id] },
                    },
                  }))
                }
              />
              <span className="swatch" style={{ background: layer.color }} />
              {layer.label}
            </label>
          ))}
        </div>
        <Toggle
          label="Étiquettes"
          checked={state.settings.anatomy.labels}
          onChange={() =>
            onChange((current) => ({
              ...current,
              anatomy: { ...current.anatomy, labels: !current.anatomy.labels },
            }))
          }
        />
        <Toggle
          label="Mode lentille X-Ray"
          hint="Réduit l’opacité des couches actives"
          checked={state.settings.anatomy.lens}
          onChange={() =>
            onChange((current) => ({
              ...current,
              anatomy: { ...current.anatomy, lens: !current.anatomy.lens },
            }))
          }
        />
        <div className="field" style={{ marginTop: 8 }}>
          <label>Opacité · {Math.round(state.settings.anatomy.opacity * 100)} %</label>
          <input
            type="range"
            min={0.15}
            max={1}
            step={0.01}
            value={state.settings.anatomy.opacity}
            onChange={(event) =>
              onChange((current) => ({
                ...current,
                anatomy: { ...current.anatomy, opacity: Number(event.target.value) },
              }))
            }
          />
        </div>
      </Card>

      <Card title="Couverture des ancrages" icon={<Ruler size={14} color="var(--accent-2)" />} subtitle={formatCoverage(coverage)}>
        <div className="progress" style={{ marginBottom: 8 }}>
          <span style={{ width: `${coverage.ratio * 100}%` }} />
        </div>
        <div className="list">
          {bones.slice(0, 9).map((bone) => (
            <div className="row" key={bone.id}>
              <Bone size={12} color={bone.system === 'organes' ? 'var(--ok)' : 'var(--accent)'} />
              <div className="grow"><div className="t">{bone.label}</div><div className="s">{bone.id}</div></div>
              <span className={`status-dot ${layers[bone.system] ? 'ready' : ''}`} />
            </div>
          ))}
        </div>
        <div className="note warn" style={{ marginTop: 9 }}>
          Repères anatomiques approximatifs dérivés de la pose 2D. Ils ne mesurent ni une pathologie ni une structure réelle du corps. Aucun maillage Écorché/BodyParts3D n’est embarqué ici.
        </div>
      </Card>

      <Card title="Lentille & précision" icon={<ScanEye size={14} color="var(--warn)" />}>
        <div className="metrics-grid">
          <div className="metric"><div className="k">Ancrages visibles</div><div className="v">{coverage.visible}<small>/{coverage.total}</small></div></div>
          <div className="metric"><div className="k">Pose</div><div className="v">{state.snapshot.pose.length ? 'suivie' : 'absente'}</div></div>
          <div className="metric"><div className="k">Couche os</div><div className="v">{layers.skeleton ? 'oui' : 'non'}</div></div>
          <div className="metric"><div className="k">Couche organes</div><div className="v">{layers.organs ? 'oui' : 'non'}</div></div>
        </div>
      </Card>
    </>
  );
}
