/**
 * One Euro filter — adaptive low-pass filtering for noisy interactive signals.
 * Reference: Casiez, Roussel & Vogel (CHI 2012).
 */
export class OneEuroFilter {
  private xPrev: number | null = null;
  private dxPrev = 0;
  private tPrev: number | null = null;

  constructor(
    private minCutoff = 1.2,
    private beta = 0.02,
    private dCutoff = 1.0,
  ) {}

  private static alpha(cutoff: number, dt: number): number {
    const tau = 1 / (2 * Math.PI * cutoff);
    return 1 / (1 + tau / dt);
  }

  reset(): void {
    this.xPrev = null;
    this.dxPrev = 0;
    this.tPrev = null;
  }

  filter(value: number, timestampMs = performance.now()): number {
    if (!Number.isFinite(value)) return this.xPrev ?? 0;
    if (this.xPrev === null || this.tPrev === null) {
      this.xPrev = value;
      this.tPrev = timestampMs;
      return value;
    }
    const dt = Math.max(1, timestampMs - this.tPrev) / 1000;
    this.tPrev = timestampMs;

    const dx = (value - this.xPrev) / dt;
    const aD = OneEuroFilter.alpha(this.dCutoff, dt);
    this.dxPrev = aD * dx + (1 - aD) * this.dxPrev;

    const cutoff = this.minCutoff + this.beta * Math.abs(this.dxPrev);
    const a = OneEuroFilter.alpha(cutoff, dt);
    this.xPrev = a * value + (1 - a) * this.xPrev;
    return this.xPrev;
  }
}

export class Vec2Filter {
  readonly x: OneEuroFilter;
  readonly y: OneEuroFilter;

  constructor(minCutoff = 1.4, beta = 0.012) {
    this.x = new OneEuroFilter(minCutoff, beta);
    this.y = new OneEuroFilter(minCutoff, beta);
  }

  filter(x: number, y: number, timestampMs?: number): { x: number; y: number } {
    return {
      x: this.x.filter(x, timestampMs),
      y: this.y.filter(y, timestampMs),
    };
  }

  reset(): void {
    this.x.reset();
    this.y.reset();
  }
}

/** MediaPipe pose landmark indexes used by anatomy anchors. */
export const POSE = {
  nose: 0,
  leftShoulder: 11,
  rightShoulder: 12,
  leftElbow: 13,
  rightElbow: 14,
  leftWrist: 15,
  rightWrist: 16,
  leftHip: 23,
  rightHip: 24,
  leftKnee: 25,
  rightKnee: 26,
  leftAnkle: 27,
  rightAnkle: 28,
} as const;

export interface NormalizedPoint {
  x: number;
  y: number;
  z?: number;
  /** MediaPipe landmark visibility when provided (0..1). */
  visibility?: number;
}

export function midpoint(a: NormalizedPoint, b: NormalizedPoint): NormalizedPoint {
  return {
    x: (a.x + b.x) / 2,
    y: (a.y + b.y) / 2,
    z: ((a.z ?? 0) + (b.z ?? 0)) / 2,
    visibility: Math.min(a.visibility ?? 1, b.visibility ?? 1),
  };
}

/** Approximate pixel scale from shoulder span; guards against zero spans. */
export function shoulderSpan(points: NormalizedPoint[], width: number): number {
  const left = points[POSE.leftShoulder];
  const right = points[POSE.rightShoulder];
  if (!left || !right) return 0;
  return Math.abs(left.x - right.x) * width;
}

export function clamp01(value: number): number {
  return Math.max(0, Math.min(1, value));
}
