import { useEffect, useState } from 'react';
import { Download, Eraser, Paintbrush, Trash2, Undo2 } from 'lucide-react';
import { Card, Toggle } from '../components';
import type { StudioState } from '../useStudio';
import { downloadText } from '../../core/clientStore';
import type { PaintModel } from '../../core/paint';

const COLORS = ['#59f2c8', '#7cc7ff', '#ffd479', '#ff6f7f', '#c6a7ff', '#ffffff'];

export function PaintPanel({
  paint,
  state,
  onChange,
}: {
  paint: PaintModel;
  state: StudioState;
  onChange: (updater: (current: StudioState['settings']) => StudioState['settings']) => void;
}) {
  const [size, setSize] = useState(paint.width);
  const [color, setColor] = useState(paint.color);
  useEffect(() => {
    paint.setStyle(color, size);
  }, [paint, color, size]);

  const pinch = state.snapshot.hands.find((hand) => hand.gesture.gesture === 'pincement');
  const fist = state.snapshot.hands.some((hand) => hand.gesture.gesture === 'poing');

  return (
    <>
      <Card title="AirPaint" icon={<Paintbrush size={14} color="var(--accent)" />} subtitle="Pincement = dessiner · poing = effacer">
        <div className="metrics-grid" style={{ marginBottom: 10 }}>
          <div className="metric">
            <div className="k">Geste</div>
            <div className="v" style={{ fontSize: 14 }}>{pinch ? 'pincement' : fist ? 'poing' : 'neutre'}</div>
          </div>
          <div className="metric">
            <div className="k">Traits</div>
            <div className="v">{paint.strokes.length}</div>
          </div>
        </div>
        <div className="field">
          <label>Couleur</label>
          <div style={{ display: 'flex', gap: 6 }}>
            {COLORS.map((value) => (
              <button
                key={value}
                onClick={() => setColor(value)}
                aria-label={`Couleur ${value}`}
                style={{
                  width: 24, height: 24, borderRadius: 7, cursor: 'pointer',
                  background: value, border: color === value ? '2px solid #fff' : '1px solid rgba(255,255,255,.2)',
                }}
              />
            ))}
          </div>
        </div>
        <div className="field" style={{ marginTop: 8 }}>
          <label>Épaisseur · {(size * 1000).toFixed(0)}</label>
          <input type="range" min={0.002} max={0.016} step={0.001} value={size} onChange={(event) => setSize(Number(event.target.value))} />
        </div>
        <div className="inline" style={{ marginTop: 9 }}>
          <button className="btn" onClick={() => paint.undo()}><Undo2 size={13} /> Annuler</button>
          <button className="btn danger" onClick={() => paint.clear()}><Trash2 size={13} /> Effacer</button>
        </div>
        <div className="inline" style={{ marginTop: 6 }}>
          <button className="btn" onClick={() => downloadText(`airpaint-${Date.now()}.svg`, paint.toSvg(), 'image/svg+xml')}><Download size={13} /> Export SVG</button>
        </div>
        <div className="note" style={{ marginTop: 9 }}>
          Le tracé est ancré sur les coordonnées caméra. Les paramètres de couleur et d’épaisseur s’appliquent aux nouveaux traits ; le dessin réel se fait au pincement dans le viewport.
        </div>
      </Card>

      <Card title="Contrôles" icon={<Eraser size={14} color="var(--warn)" />} subtitle="Sans modèle supplémentaire">
        <div className="list">
          <div className="row"><div className="grow"><div className="t">Pincement</div><div className="s">démarre / termine le trait</div></div><span className={`status-dot ${pinch ? 'ready' : ''}`} /></div>
        </div>
        <Toggle
          label="Effacer avec un poing tenu"
          hint="Action destructive — désactivée par défaut"
          checked={state.settings.paint.clearWithFist}
          onChange={() =>
            onChange((current) => ({
              ...current,
              paint: { ...current.paint, clearWithFist: !current.paint.clearWithFist },
            }))
          }
        />
        {state.settings.paint.clearWithFist && (
          <div className="note warn" style={{ marginTop: 8 }}>
            Maintiens le poing environ 0,9 s pour vider le calque. Le geste doit être stable pour éviter les faux positifs.
            {fist && <span> Poing détecté.</span>}
          </div>
        )}
        <div className="note" style={{ marginTop: 8 }}>
          L’export SVG utilise un viewBox 1000×1000 ; le viewport affiche les traits en coordonnées caméra.
        </div>
      </Card>
    </>
  );
}
