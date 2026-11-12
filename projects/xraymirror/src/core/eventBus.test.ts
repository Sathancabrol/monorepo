import { describe, expect, it, vi } from 'vitest';
import { EventBus } from './eventBus';

describe('event bus', () => {
  it('adds ids, timestamps and attributes', () => {
    const bus = new EventBus();
    const event = bus.emit({ type: 'system.metric', source: 'test', attributes: { fps: 30 } });
    expect(event.id).toMatch(/^evt_/);
    expect(event.timestamp).toBeGreaterThan(0);
    expect(event.attributes.fps).toBe(30);
  });

  it('notifies subscribers and supports unsubscription', () => {
    const bus = new EventBus();
    const listener = vi.fn();
    const unsubscribe = bus.subscribe(listener);
    bus.emit({ type: 'session.state', source: 'test', attributes: {} });
    unsubscribe();
    bus.emit({ type: 'session.state', source: 'test', attributes: {} });
    expect(listener).toHaveBeenCalledTimes(1);
  });

  it('bounds memory and exports JSONL', () => {
    const bus = new EventBus(50);
    for (let index = 0; index < 80; index += 1) {
      bus.emit({ type: 'system.metric', source: 'test', attributes: { index } });
    }
    expect(bus.all()).toHaveLength(50);
    expect(bus.exportJsonLines().split('\n')).toHaveLength(50);
  });

  it('filters by type', () => {
    const bus = new EventBus();
    bus.emit({ type: 'face.detected', source: 'test', attributes: {} });
    bus.emit({ type: 'sound.detected', source: 'test', attributes: {} });
    expect(bus.byType('sound.detected')).toHaveLength(1);
    expect(bus.recent(10, ['face.detected'])).toHaveLength(1);
  });
});
