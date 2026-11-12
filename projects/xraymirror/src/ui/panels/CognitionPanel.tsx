import { useRef, useState } from 'react';
import { Brain, Flag, Timer, Trophy } from 'lucide-react';
import { Card } from '../components';
import { downloadText } from '../../core/clientStore';

interface Reaction {
  at: number;
  ms: number;
}

interface MemoryRun {
  at: number;
  score: number;
  best: number;
}

const GRID = 16;

export function CognitionPanel({ onToast }: { onToast: (message: string, tone?: 'info' | 'ok') => void }) {
  const [phase, setPhase] = useState<'idle' | 'waiting' | 'go' | 'done'>('idle');
  const [reactions, setReactions] = useState<Reaction[]>([]);
  const goAt = useRef(0);
  const timeout = useRef<number | null>(null);

  const [sequence, setSequence] = useState<number[]>([]);
  const [input, setInput] = useState<number[]>([]);
  const [memoryRuns, setMemoryRuns] = useState<MemoryRun[]>([]);
  const [score, setScore] = useState(0);

  const startReaction = () => {
    setPhase('waiting');
    const delay = 1100 + Math.random() * 1800;
    timeout.current = window.setTimeout(() => {
      goAt.current = performance.now();
      setPhase('go');
    }, delay);
  };

  const hit = () => {
    if (phase === 'waiting') {
      if (timeout.current) window.clearTimeout(timeout.current);
      setPhase('idle');
      onToast('Trop tôt — essai annulé', 'info');
      return;
    }
    if (phase !== 'go') return;
    const ms = Math.round(performance.now() - goAt.current);
    setReactions((current) => [...current.slice(-7), { at: Date.now(), ms }]);
    setPhase('done');
  };

  const startMemory = () => {
    const next = Array.from({ length: 4 }, () => Math.floor(Math.random() * GRID));
    setSequence([...new Set(next)]);
    setInput([]);
    setScore(0);
  };

  const press = (index: number) => {
    if (sequence.includes(index)) {
      if (input.includes(index)) return;
      const next = [...input, index];
      setInput(next);
      setScore(next.length);
      if (next.length === sequence.length) {
        setMemoryRuns((current) => [...current.slice(-5), { at: Date.now(), score: sequence.length, best: sequence.length }]);
        onToast('Séquence complète ✓', 'ok');
        window.setTimeout(startMemory, 900);
      }
    } else if (sequence.length) {
      setInput([]);
      setScore(0);
      onToast('Mauvaise case — séquence réinitialisée', 'info');
    }
  };

  const best = reactions.length ? Math.min(...reactions.map((entry) => entry.ms)) : 0;
  const average = reactions.length ? Math.round(reactions.reduce((sum, entry) => sum + entry.ms, 0) / reactions.length) : 0;

  return (
    <>
      <Card title="Temps de réaction" icon={<Timer size={14} color="var(--accent)" />} subtitle="Mesure de performance, pas d’état mental">
        <div className="cognition">
          <button
            className={`target ${phase === 'go' ? 'go' : ''}`}
            style={{ border: '1px dashed rgba(89,242,200,.35)', height: 120, borderRadius: 12, background: phase === 'go' ? 'rgba(89,242,200,.25)' : '#071512', color: phase === 'go' ? 'var(--accent)' : 'var(--muted)', fontSize: 13 }}
            onClick={phase === 'go' ? hit : startReaction}
          >
            {phase === 'idle' && 'Démarrer — clique quand la zone devient verte'}
            {phase === 'waiting' && 'Attends…'}
            {phase === 'go' && 'CLIQUE !'}
            {phase === 'done' && `Dernier essai : ${reactions.at(-1)?.ms} ms — reclique pour recommencer`}
          </button>
          {phase === 'waiting' && <button className="btn" onClick={hit}>Annuler</button>}
          {phase === 'go' && <button className="btn primary" onClick={hit}>Clic</button>}
        </div>
        <div className="metrics-grid" style={{ marginTop: 9 }}>
          <div className="metric"><div className="k">Meilleur</div><div className="v">{best || '—'}<small>ms</small></div></div>
          <div className="metric"><div className="k">Moyenne</div><div className="v">{average || '—'}<small>ms</small></div></div>
        </div>
        <div className="note warn" style={{ marginTop: 9 }}>Le temps de réaction dépend aussi de l’écran, de la souris et de la fatigue. Aucun diagnostic, aucun classement clinique.</div>
      </Card>

      <Card title="Mémoire spatiale" icon={<Brain size={14} color="var(--accent-2)" />} subtitle={`${sequence.length} cibles à retrouver`} actions={<button className="btn small" onClick={startMemory}><Flag size={12} /> Nouvelle</button>}>
        <div className="grid-target">
          {Array.from({ length: GRID }).map((_, index) => {
            const revealed = sequence.includes(index);
            const selected = input.includes(index);
            return (
              <button key={index} onClick={() => press(index)} style={{ borderColor: selected ? 'var(--accent)' : undefined, background: selected ? 'rgba(89,242,200,.15)' : undefined, color: selected ? 'var(--accent)' : undefined }}>
                {selected ? '✓' : revealed && input.length === 0 ? '·' : ''}
              </button>
            );
          })}
        </div>
        <div className="metrics-grid" style={{ marginTop: 9 }}>
          <div className="metric"><div className="k">Cette séquence</div><div className="v">{score}<small>/{sequence.length || 4}</small></div></div>
          <div className="metric"><div className="k">Séquences</div><div className="v">{memoryRuns.length}</div></div>
        </div>
      </Card>

      <Card title="Journal" icon={<Trophy size={14} color="var(--warn)" />} actions={
        <button className="btn small ghost" onClick={() => downloadText(`xraymirror-cognition-${Date.now()}.json`, JSON.stringify({ reactions, memoryRuns }, null, 2))}>Export</button>
      }>
        {reactions.length === 0 && memoryRuns.length === 0 ? (
          <div className="empty">Aucun essai enregistré.</div>
        ) : (
          <div className="list">
            {reactions.map((entry) => (
              <div className="row" key={`r-${entry.at}`}><Timer size={12} color="var(--accent)" /><div className="grow"><div className="t">Réaction</div><div className="s">{new Date(entry.at).toLocaleTimeString('fr-FR', { hour12: false })}</div></div><span className="tag">{entry.ms} ms</span></div>
            ))}
            {memoryRuns.map((entry) => (
              <div className="row" key={`m-${entry.at}`}><Brain size={12} color="var(--accent-2)" /><div className="grow"><div className="t">Mémoire</div><div className="s">{new Date(entry.at).toLocaleTimeString('fr-FR', { hour12: false })}</div></div><span className="tag">{entry.score}/{entry.best}</span></div>
            ))}
          </div>
        )}
      </Card>
    </>
  );
}
