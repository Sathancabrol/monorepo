import { Workflow, Zap } from 'lucide-react';
import { Card, Toggle } from '../components';
import type { StudioState } from '../useStudio';
import type { RuleDefinition } from '../../core/types';

export function RulesPanel({
  state,
  onUpdate,
}: {
  state: StudioState;
  onUpdate: (ruleId: string, patch: Partial<RuleDefinition>) => void;
}) {
  const fired = state.events.filter((event) => event.type === 'rule.fired').slice(-6).reverse();
  return (
    <>
      <Card title="Moteur de règles" icon={<Workflow size={14} color="var(--accent)" />} subtitle="Quand → Conditions → Action, exécuté localement">
        <div className="list">
          {state.settings.rules.map((rule) => (
            <div className="rule" key={rule.id}>
              <div className="head">
                <Zap size={13} color={rule.enabled ? 'var(--accent)' : 'var(--muted)'} />
                <div className="grow">{rule.name}</div>
                <button className={`switch ${rule.enabled ? 'on' : ''}`} onClick={() => onUpdate(rule.id, { enabled: !rule.enabled })} aria-label={`Activer ${rule.name}`} />
              </div>
              <div className="plugin-meta">
                <span className="tag">{rule.trigger}{rule.matchLabel ? ` = ${rule.matchLabel}` : ''}</span>
                <span className="tag">≥ {Math.round(rule.minConfidence * 100)} %</span>
                <span className="tag">cooldown {rule.cooldownMs} ms</span>
                <span className="tag">{rule.action.type}</span>
              </div>
            </div>
          ))}
        </div>
        <div className="note" style={{ marginTop: 9 }}>
          Les actions disponibles ici sont volontairement limitées : toast, bascule de couches, effacement du dessin. Aucun script arbitraire n’est exécuté depuis une règle.
        </div>
      </Card>

      <Card title="Déclenchements récents" icon={<Zap size={14} color="var(--warn)" />} subtitle={`${fired.length} affichés`}>
        {fired.length === 0 ? (
          <div className="empty">Aucune règle déclenchée pour l’instant.</div>
        ) : (
          <div className="list">
            {fired.map((event) => (
              <div className="row" key={event.id}>
                <Zap size={12} color="var(--warn)" />
                <div className="grow">
                  <div className="t">{event.label}</div>
                  <div className="s">{String(event.attributes.action ?? '')} · {new Date(event.timestamp).toLocaleTimeString('fr-FR', { hour12: false })}</div>
                </div>
              </div>
            ))}
          </div>
        )}
        <div className="note" style={{ marginTop: 9 }}>
          Règle par défaut : un claquement (confiance ≥ 55 %) inverse les couches anatomiques, avec anti-rebond de 1,2 s.
        </div>
      </Card>
    </>
  );
}
