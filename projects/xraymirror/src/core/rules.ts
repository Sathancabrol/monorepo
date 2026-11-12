import type { RuleDefinition, RuleFiring, StudioEvent } from './types';

/**
 * Small deterministic rule engine. It only reacts to already-produced events:
 * it cannot upload, execute arbitrary code or block the perception loop.
 */
export class RuleEngine {
  private lastFired = new Map<string, number>();

  constructor(
    private rules: RuleDefinition[],
    private onAction: (rule: RuleDefinition, event: StudioEvent) => void,
    private onFiring?: (firing: RuleFiring) => void,
  ) {}

  setRules(rules: RuleDefinition[]): void {
    this.rules = rules;
  }

  getRules(): readonly RuleDefinition[] {
    return this.rules;
  }

  evaluate(event: StudioEvent, now = Date.now()): RuleDefinition[] {
    const fired: RuleDefinition[] = [];
    for (const rule of this.rules) {
      if (!rule.enabled) continue;
      if (rule.trigger !== event.type) continue;
      if (rule.matchLabel && event.label !== rule.matchLabel) continue;
      if (typeof event.confidence === 'number' && event.confidence < rule.minConfidence) continue;

      const last = this.lastFired.get(rule.id) ?? 0;
      if (now - last < rule.cooldownMs) continue;

      this.lastFired.set(rule.id, now);
      fired.push(rule);
      this.onAction(rule, event);
      this.onFiring?.({ ruleId: rule.id, at: now, eventId: event.id });
    }
    return fired;
  }

  resetCooldowns(): void {
    this.lastFired.clear();
  }
}

export const DEFAULT_RULES: RuleDefinition[] = [
  {
    id: 'clap-anatomy',
    name: 'Claquement → couches anatomiques',
    enabled: true,
    trigger: 'sound.detected',
    matchLabel: 'claquement',
    minConfidence: 0.55,
    cooldownMs: 1200,
    action: { type: 'toggle-layer', payload: { layer: 'anatomy' } },
  },
  {
    id: 'smile-toast',
    name: 'Sourire → confirmation',
    enabled: false,
    trigger: 'face.expressions',
    matchLabel: 'sourire',
    minConfidence: 0.45,
    cooldownMs: 6000,
    action: {
      type: 'show-toast',
      payload: { message: 'Sourire détecté — expression visible, pas une émotion.' },
    },
  },
];
