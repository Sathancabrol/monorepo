import { describe, expect, it, vi } from 'vitest';
import { RuleEngine } from './rules';
import type { RuleDefinition, StudioEvent } from './types';

const rule: RuleDefinition = {
  id: 'test',
  name: 'Test',
  enabled: true,
  trigger: 'sound.detected',
  matchLabel: 'claquement',
  minConfidence: 0.5,
  cooldownMs: 1000,
  action: { type: 'toggle-layer', payload: { layer: 'anatomy' } },
};

function event(partial: Partial<StudioEvent> = {}): StudioEvent {
  return {
    id: 'e1',
    timestamp: 0,
    type: 'sound.detected',
    source: 'test',
    label: 'claquement',
    confidence: 0.9,
    attributes: {},
    ...partial,
  };
}

describe('rule engine', () => {
  it('fires on a matching event and respects the cooldown', () => {
    const action = vi.fn();
    const engine = new RuleEngine([rule], action);
    expect(engine.evaluate(event(), 10_000)).toHaveLength(1);
    expect(engine.evaluate(event({ id: 'e2' }), 10_500)).toHaveLength(0);
    expect(engine.evaluate(event({ id: 'e3' }), 11_100)).toHaveLength(1);
    expect(action).toHaveBeenCalledTimes(2);
  });

  it('ignores labels and low-confidence events', () => {
    const engine = new RuleEngine([rule], vi.fn());
    expect(engine.evaluate(event({ label: 'chien' }))).toHaveLength(0);
    expect(engine.evaluate(event({ confidence: 0.2 }))).toHaveLength(0);
  });

  it('ignores disabled rules', () => {
    const engine = new RuleEngine([{ ...rule, enabled: false }], vi.fn());
    expect(engine.evaluate(event())).toHaveLength(0);
  });
});
