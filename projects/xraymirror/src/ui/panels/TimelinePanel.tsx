import { useMemo, useState } from 'react';
import { Download, Eraser, History, ListTree } from 'lucide-react';
import { Card } from '../components';
import type { StudioState } from '../useStudio';
import { downloadText } from '../../core/clientStore';

const FILTERS = [
  { id: 'all', label: 'Tout' },
  { id: 'face', label: 'Visage' },
  { id: 'hand', label: 'Mains' },
  { id: 'object', label: 'Objets' },
  { id: 'sound', label: 'Sons' },
  { id: 'pose', label: 'Corps' },
];

export function TimelinePanel({
  state,
  onClear,
  getExport,
}: {
  state: StudioState;
  onClear: () => void;
  getExport: () => string;
}) {
  const [filter, setFilter] = useState('all');
  const items = useMemo(() => {
    const list = [...state.events].reverse();
    if (filter === 'all') return list.slice(0, 90);
    return list.filter((event) => event.type.startsWith(filter)).slice(0, 90);
  }, [state.events, filter]);

  return (
    <Card
      title="Timeline d’événements"
      icon={<History size={14} color="var(--accent)" />}
      subtitle={`${state.events.length} événements en mémoire`}
      actions={
        <>
          <button className="btn small ghost" title="Exporter JSONL" onClick={() => downloadText(`xraymirror-events-${Date.now()}.jsonl`, getExport(), 'application/x-ndjson')}><Download size={12} /></button>
          <button className="btn small ghost" title="Effacer" onClick={onClear}><Eraser size={12} /></button>
        </>
      }
      bodyClassName=""
    >
      <div className="tabs" style={{ marginBottom: 6 }}>
        {FILTERS.map((entry) => (
          <button key={entry.id} className={filter === entry.id ? 'active' : ''} onClick={() => setFilter(entry.id)}>{entry.label}</button>
        ))}
      </div>
      <div className="feed scroll-panel" style={{ maxHeight: 430 }}>
        {items.length === 0 && (
          <div className="empty">
            <ListTree size={20} style={{ opacity: 0.5, marginBottom: 8 }} />
            <div>Aucun événement. Démarre la caméra ou le micro.</div>
          </div>
        )}
        {items.map((event) => (
          <div className="feed-item" key={event.id}>
            <span className={`dot ${event.type.startsWith('sound') ? 'warn' : event.type.startsWith('rule') ? 'err' : 'on'}`} />
            <div>
              <div className="name">
                {event.label ?? event.type}
                {typeof event.confidence === 'number' && (
                  <span className="badge" style={{ marginLeft: 6 }}>{Math.round(event.confidence * 100)}%</span>
                )}
              </div>
              <div className="meta">{event.source} · {event.type}</div>
            </div>
            <time>{new Date(event.timestamp).toLocaleTimeString('fr-FR', { hour12: false })}</time>
          </div>
        ))}
      </div>
    </Card>
  );
}
