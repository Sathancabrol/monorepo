import { useMemo, useState } from 'react';
import { Cpu, Puzzle, Search, ShieldCheck, Wifi, WifiOff } from 'lucide-react';
import { Card } from '../components';
import { PLUGIN_CATALOG, PLUGIN_CATEGORIES } from '../../core/pluginCatalog';

export function PluginsPanel({ onToast }: { onToast: (message: string, tone?: 'info' | 'warn' | 'ok') => void }) {
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState<string>('all');

  const filtered = useMemo(
    () =>
      PLUGIN_CATALOG.filter((plugin) => {
        if (category !== 'all' && plugin.category !== category) return false;
        if (!query) return true;
        const haystack = `${plugin.name} ${plugin.description} ${plugin.id}`.toLowerCase();
        return haystack.includes(query.toLowerCase());
      }),
    [query, category],
  );

  const installedCount = PLUGIN_CATALOG.filter((plugin) => plugin.status !== 'planned').length;
  const readyCount = PLUGIN_CATALOG.filter((plugin) => plugin.status === 'ready').length;

  return (
    <>
      <Card title="Centre de plugins" icon={<Puzzle size={14} color="var(--accent)" />} subtitle={`${installedCount} embarqués · ${readyCount} prêts · ${PLUGIN_CATALOG.length} au catalogue`}>
        <div className="search">
          <Search size={13} color="var(--muted)" />
          <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Filtrer…" />
        </div>
        <div className="tabs" style={{ marginTop: 8 }}>
          <button className={category === 'all' ? 'active' : ''} onClick={() => setCategory('all')}>Tout</button>
          {PLUGIN_CATEGORIES.filter((entry) => entry.id !== 'system').map((entry) => (
            <button key={entry.id} className={category === entry.id ? 'active' : ''} onClick={() => setCategory(entry.id)}>{entry.label}</button>
          ))}
        </div>
        <div className="plugin-grid" style={{ marginTop: 10 }}>
          {filtered.map((plugin) => {
            const planned = plugin.status === 'planned';
            return (
              <article className={`plugin-card ${!planned ? 'installed' : ''}`} key={plugin.id}>
                <div className="head">
                  <div className="grow">
                    <h4>{plugin.name}</h4>
                    <div className="s" style={{ color: 'var(--muted)', fontSize: 10 }}>{plugin.id} · v{plugin.version}</div>
                  </div>
                  <span className={`status-dot ${plugin.status}`} title={plugin.status} />
                </div>
                <div className="desc">{plugin.description}</div>
                <div className="plugin-meta">
                  <span className="tag">{plugin.category}</span>
                  <span className="tag">{plugin.runtime}</span>
                  {plugin.gpu.vramMb > 0 && <span className="tag gpu"><Cpu size={9} /> {plugin.gpu.vramMb} Mo</span>}
                  {plugin.network ? <span className="tag net"><Wifi size={9} /> réseau</span> : <span className="tag private"><WifiOff size={9} /> local</span>}
                  {plugin.permissions.map((permission) => <span className="tag" key={permission}>{permission}</span>)}
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span className="s" style={{ flex: 1, fontSize: 10, color: 'var(--muted)' }}>
                    {planned ? 'Non intégré au socle' : plugin.status === 'preview' ? 'Code présent, à valider' : 'Disponible dans cette version'}
                  </span>
                  <button
                    className="btn small ghost"
                    disabled={planned}
                    onClick={() =>
                      onToast(
                        planned
                          ? `${plugin.name} n’est pas encore intégré : aucune activation simulée.`
                          : `${plugin.name} se configure dans son panneau dédié (module réel, pas de bascule factice).`,
                        planned ? 'warn' : 'info',
                      )
                    }
                  >
                    {planned ? 'Prévu' : 'Ouvrir'}
                  </button>
                </div>
              </article>
            );
          })}
        </div>
        <div className="note" style={{ marginTop: 10 }}>
          <ShieldCheck size={11} style={{ verticalAlign: '-1px' }} /> Les modèles lourds (VLM, OCR natif) sont marqués <strong>prévus</strong> : aucun faux bouton « installé ». Chaque plugin déclare réseau, GPU, VRAM et permissions dans le manifeste.
        </div>
      </Card>
    </>
  );
}
