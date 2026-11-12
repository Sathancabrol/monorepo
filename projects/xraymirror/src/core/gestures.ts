import type { NormalizedPoint } from './filters';

export type StaticGesture = 'pincement' | 'poing' | 'paume' | 'victoire' | 'pointage' | 'inconnu';

export interface GestureResult {
  gesture: StaticGesture;
  confidence: number;
  pinchRatio: number;
  extendedFingers: number;
}

const TIPS = [8, 12, 16, 20] as const;
const PIPS = [6, 10, 14, 18] as const;

export function distance2d(a: NormalizedPoint, b: NormalizedPoint): number {
  return Math.hypot(a.x - b.x, a.y - b.y);
}

export function pinchRatio(landmarks: NormalizedPoint[]): number {
  if (landmarks.length < 21) return Number.POSITIVE_INFINITY;
  const wrist = landmarks[0];
  const middleMcp = landmarks[9];
  const handSize = Math.max(1e-5, distance2d(wrist, middleMcp));
  return distance2d(landmarks[4], landmarks[8]) / handSize;
}

function isFingerExtended(
  landmarks: NormalizedPoint[],
  tipIndex: number,
  pipIndex: number,
): boolean {
  const wrist = landmarks[0];
  return distance2d(wrist, landmarks[tipIndex]) > distance2d(wrist, landmarks[pipIndex]) * 1.12;
}

function isThumbExtended(landmarks: NormalizedPoint[]): boolean {
  if (landmarks.length < 21) return false;
  const wrist = landmarks[0];
  return distance2d(wrist, landmarks[4]) > distance2d(wrist, landmarks[3]) * 1.06;
}

/**
 * Geometry-only classifier. It deliberately stays simple and predictable:
 * no model, no identity, no network. Confidence reflects finger-support margin.
 */
export function classifyGesture(landmarks: NormalizedPoint[]): GestureResult {
  if (landmarks.length < 21) {
    return { gesture: 'inconnu', confidence: 0, pinchRatio: Number.POSITIVE_INFINITY, extendedFingers: 0 };
  }
  const extended = TIPS.filter((tip, index) => isFingerExtended(landmarks, tip, PIPS[index]));
  const thumb = isThumbExtended(landmarks);
  const ratio = pinchRatio(landmarks);
  const count = extended.length;

  if (ratio < 0.32 && count <= 3) {
    return {
      gesture: 'pincement',
      confidence: Math.max(0.55, Math.min(0.99, 1 - ratio / 0.5)),
      pinchRatio: ratio,
      extendedFingers: count,
    };
  }

  if (count === 0 && !thumb) {
    return { gesture: 'poing', confidence: 0.86, pinchRatio: ratio, extendedFingers: count };
  }

  if (count === 4) {
    return { gesture: 'paume', confidence: 0.9, pinchRatio: ratio, extendedFingers: count };
  }

  const indexOnly = extended.length === 1 && extended[0] === 8;
  if (indexOnly) {
    return { gesture: 'pointage', confidence: 0.82, pinchRatio: ratio, extendedFingers: count };
  }

  const victory = extended.length === 2 && extended[0] === 8 && extended[1] === 12;
  if (victory) {
    return { gesture: 'victoire', confidence: 0.85, pinchRatio: ratio, extendedFingers: count };
  }

  return { gesture: 'inconnu', confidence: 0.4, pinchRatio: ratio, extendedFingers: count };
}

/** Requires the same gesture on consecutive samples before accepting it. */
export class GestureStabilizer {
  private candidate: StaticGesture = 'inconnu';
  private streak = 0;
  private accepted: StaticGesture = 'inconnu';

  update(result: GestureResult): { gesture: StaticGesture; changed: boolean } {
    if (result.gesture === this.candidate) {
      this.streak += 1;
    } else {
      this.candidate = result.gesture;
      this.streak = 1;
    }
    const changed = this.candidate !== this.accepted && this.streak >= 2;
    if (changed) this.accepted = this.candidate;
    return { gesture: this.accepted, changed };
  }

  reset(): void {
    this.candidate = 'inconnu';
    this.accepted = 'inconnu';
    this.streak = 0;
  }
}
