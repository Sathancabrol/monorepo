import type { EventDraft, StudioEvent } from './types';

let sequence = 0;

/**
 * Deterministic-enough unique id. crypto.randomUUID is not available in every
 * test environment, hence the fallback.
 */
export function createId(prefix = 'evt'): string {
  sequence = (sequence + 1) % 1_000_000;
  const random = Math.random().toString(36).slice(2, 8);
  return `${prefix}_${Date.now().toString(36)}_${sequence.toString(36)}_${random}`;
}

export class EventBus {
  private events: StudioEvent[] = [];
  private listeners = new Set<(event: StudioEvent) => void>();
  private readonly capacity: number;

  constructor(capacity = 4000) {
    this.capacity = Math.max(50, capacity);
  }

  emit<T>(draft: EventDraft<T>): StudioEvent<T> {
    const event: StudioEvent<T> = {
      ...draft,
      id: createId(),
      timestamp: draft.timestamp ?? Date.now(),
      attributes: (draft.attributes ?? {}) as T,
    };
    this.events.push(event as StudioEvent);
    if (this.events.length > this.capacity) {
      this.events.splice(0, this.events.length - this.capacity);
    }
    for (const listener of this.listeners) {
      try {
        listener(event as StudioEvent);
      } catch (error) {
        console.error('[event-bus] listener failed', error);
      }
    }
    return event;
  }

  subscribe(listener: (event: StudioEvent) => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  recent(limit = 80, types?: string[]): StudioEvent[] {
    const filtered = types?.length
      ? this.events.filter((event) => types.includes(event.type))
      : this.events;
    return filtered.slice(-Math.max(1, limit));
  }

  byType(type: string, limit = 50): StudioEvent[] {
    return this.events.filter((event) => event.type === type).slice(-limit);
  }

  all(): readonly StudioEvent[] {
    return this.events;
  }

  count(type?: string): number {
    return type ? this.events.filter((event) => event.type === type).length : this.events.length;
  }

  exportJsonLines(): string {
    return this.events.map((event) => JSON.stringify(event)).join('\n');
  }

  clear(): void {
    this.events = [];
  }
}
