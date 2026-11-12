import { Download, ShieldCheck, SlidersHorizontal, Trash2 } from 'lucide-react';
import { Card, Toggle } from '../components';
import type { StudioState } from '../useStudio';
import { downloadText } from '../../core/clientStore';

export function SettingsPanel({
  state,
  onChange,
  onToast,
}: {
  state: StudioState;
  onChange: (updater: (current: StudioState['settings']) => StudioState['settings']) => void;
  onToast: (message: string, tone?: 'info' | 'ok' | 'warn') => void;
}) {
  return (
    <>
      <Card title="Profil d’exécution" icon={<SlidersHorizontal size={14} color="var(--accent)" />} subtitle="Les valeurs sont sauvegardées dans ce navigateur">
        <div className="field">
          <label>Profil</label>
          <select
            value={state.settings.modelCache.mode}
            onChange={(event) =>
              onChange((current) => ({
                ...current,
                modelCache: { ...current.modelCache, mode: event.target.value as 'auto' | 'local-only' | 'remote-only' },
              }))
            }
          >
            <option value="auto">Auto — cache local puis distant</option>
            <option value="local-only">Local uniquement (offline)</option>
            <option value="remote-only">Distant uniquement</option>
          </select>
        </div>
        <div className="note" style={{ marginTop: 8 }}>
          <strong>Auto</strong> : cache local si présent, sinon URL épinglée. <strong>Local uniquement</strong> : échec explicite
          si un modèle manque, aucune requête distante. <strong>Distant uniquement</strong> : ignore le cache.
          Le mode est appliqué au prochain démarrage de la caméra.
        </div>
        <div className="inline" style={{ marginTop: 9 }}>
          <button
            className="btn"
            onClick={() => {
              onChange(() => ({ ...state.settings }));
              onToast('Réglages réappliqués', 'ok');
            }}
          >
            Réappliquer
          </button>
          <button
            className="btn"
            onClick={() => downloadText(`xraymirror-settings-${Date.now()}.json`, JSON.stringify(state.settings, null, 2))}
          >
            <Download size={13} /> Export
          </button>
        </div>
      </Card>

      <Card title="Confidentialité" icon={<ShieldCheck size={14} color="var(--ok)" />} subtitle="Par défaut : aucun stockage de flux brut">
        <Toggle
          label="Conserver les médias bruts"
          hint="Désactivé : captures seulement sur action"
          checked={state.settings.privacy.storeRawMedia}
          onChange={() => onChange((current) => ({ ...current, privacy: { ...current.privacy, storeRawMedia: !current.privacy.storeRawMedia } }))}
        />
        <Toggle
          label="Anonymiser les exports"
          hint="Floutage visage à l’export (prévu)"
          checked={state.settings.privacy.anonymizeExports}
          onChange={() => onChange((current) => ({ ...current, privacy: { ...current.privacy, anonymizeExports: !current.privacy.anonymizeExports } }))}
        />
        <div className="note" style={{ marginTop: 9 }}>
          Le floutage s’applique réellement aux captures PNG : les zones de visage détectées sont floutées avant
          l’export, jamais dans un second temps. Le streaming vidéo n’est pas exporté.
        </div>
        <button
          className="btn danger"
          style={{ marginTop: 9, width: '100%' }}
          onClick={() => {
            try {
              localStorage.removeItem('xraymirror.settings.v1');
              localStorage.removeItem('xraymirror.off.v1');
              onToast('Cache local des réglages et produits supprimé', 'ok');
            } catch {
              onToast('Suppression impossible dans ce navigateur', 'warn');
            }
          }}
        >
          <Trash2 size={13} /> Effacer les données locales
        </button>
      </Card>

      <Card title="Diagnostic" icon={<SlidersHorizontal size={14} color="var(--muted)" />}>
        <div className="list">
          {Object.entries(state.engineStatus).map(([engine, status]) => (
            <div className="row" key={engine}>
              <div className="grow"><div className="t">{engine}</div><div className="s">{status}</div></div>
              <span className={`status-dot ${status === 'prêt' ? 'ready' : status.startsWith('erreur') ? 'err' : 'preview'}`} style={status.startsWith('erreur') ? { background: 'var(--danger)' } : undefined} />
            </div>
          ))}
          {Object.keys(state.engineStatus).length === 0 && <div className="empty">Aucun moteur sollicité.</div>}
        </div>
        {state.error && <div className="note warn" style={{ marginTop: 8 }}>{state.error}</div>}
      </Card>
    </>
  );
}
