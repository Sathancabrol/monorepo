import type { EventBus } from './eventBus';
import { classifyGesture, type GestureResult } from './gestures';
import { toPoints, type MediaPipeEngine } from './mediapipe';
import type { DetectorSettings } from './types';

export interface PerceptionSnapshot {
  face: ReturnType<typeof toPoints>;
  hands: Array<{ points: ReturnType<typeof toPoints>; handedness: string; gesture: GestureResult }>;
  pose: ReturnType<typeof toPoints>;
  objects: Array<{ box: { x: number; y: number; width: number; height: number }; label: string; confidence: number }>;
  updatedAt: number;
}

/** Cadences are targets, not guarantees: each engine runs only when the loop is free. */
export const FACE_HZ = 24;
export const HANDS_HZ = 24;
export const POSE_HZ = 16;
export const OBJECTS_HZ = 6;
export const GESTURES_HZ = 12;

export function emptySnapshot(): PerceptionSnapshot {
  return { face: [], hands: [], pose: [], objects: [], updatedAt: 0 };
}

/**
 * Runs MediaPipe tasks over a shared video element. Each task has its own
 * cadence so light face/hand tracking can run while heavy detection stays slow.
 */
export class PerceptionLoop {
  private raf = 0;
  private running = false;
  private lastRuns: Record<string, number> = {};
  private lastVideoTime = -1;
  private busy = false;
  private lastExpression = { smile: 0, blink: 0 };
  private snapshot: PerceptionSnapshot = emptySnapshot();
  readonly timings: Record<string, number> = {};
  readonly errors: string[] = [];
  private samples: Record<string, number[]> = {};

  /** p50/p95 over a bounded rolling window (120 samples per engine). */
  summary(): Record<string, { p50: number; p95: number; samples: number }> {
    const output: Record<string, { p50: number; p95: number; samples: number }> = {};
    for (const [engine, values] of Object.entries(this.samples)) {
      if (!values.length) continue;
      const sorted = [...values].sort((a, b) => a - b);
      const at = (quantile: number) => sorted[Math.min(sorted.length - 1, Math.floor(quantile * sorted.length))];
      output[engine] = {
        p50: Math.round(at(0.5) * 10) / 10,
        p95: Math.round(at(0.95) * 10) / 10,
        samples: sorted.length,
      };
    }
    return output;
  }

  private record(engine: string, ms: number): void {
    const list = this.samples[engine] ?? [];
    list.push(ms);
    if (list.length > 120) list.shift();
    this.samples[engine] = list;
  }

  constructor(
    private readonly video: HTMLVideoElement,
    private readonly engine: MediaPipeEngine,
    private readonly bus: EventBus,
    private onSnapshot: (snapshot: PerceptionSnapshot) => void,
  ) {}

  start(): void {
    if (this.running) return;
    this.running = true;
    const tick = () => {
      if (!this.running) return;
      void this.process();
      this.raf = requestAnimationFrame(tick);
    };
    this.raf = requestAnimationFrame(tick);
  }

  stop(): void {
    this.running = false;
    cancelAnimationFrame(this.raf);
  }

  get current(): PerceptionSnapshot {
    return this.snapshot;
  }

  private async process(): Promise<void> {
    if (this.busy || !this.running) return;
    const video = this.video;
    if (!video || video.readyState < 2 || video.videoWidth === 0) return;
    // Avoid duplicated inference for the same painted frame.
    if (video.currentTime === this.lastVideoTime) return;
    this.lastVideoTime = video.currentTime;
    this.busy = true;
    try {
      await this.runTasks();
    } catch (error) {
      this.errors.push(String(error));
    } finally {
      this.busy = false;
    }
  }

  private due(kind: string, cadenceHz: number, now: number): boolean {
    const interval = cadenceHz > 0 ? 1000 / cadenceHz : Infinity;
    const last = this.lastRuns[kind] ?? 0;
    if (now - last < interval) return false;
    this.lastRuns[kind] = now;
    return true;
  }

  private async runTasks(): Promise<void> {
    const now = performance.now();
    const timestamp = Math.round(now);
    const runtime = this.engine.runtime;
    const previous = this.snapshot;
    const next: PerceptionSnapshot = {
      ...previous,
      face: previous.face,
      hands: previous.hands,
      pose: previous.pose,
      objects: previous.objects,
    };
    let changed = false;

    if (runtime.face && this.due('face', FACE_HZ, now)) {
      const started = performance.now();
      const result = runtime.face.detectForVideo(this.video, timestamp);
      this.timings.face = performance.now() - started;
      this.record('face', this.timings.face);
      const points = toPoints(result.faceLandmarks?.[0]);
      next.face = points;
      changed = true;
      if (points.length) {
        const shapes = result.faceBlendshapes?.[0]?.categories ?? [];
        const pick = (name: string) => shapes.find((shape) => shape.categoryName === name)?.score ?? 0;
        const smile = (pick('mouthSmileLeft') + pick('mouthSmileRight')) / 2;
        const blink = Math.max(pick('eyeBlinkLeft'), pick('eyeBlinkRight'));
        this.bus.emit({
          type: 'face.detected',
          source: 'mediapipe.face',
          confidence: 0.96,
          timestamp: now,
          geometry: {
            box: {
              x: Math.min(...points.map((point) => point.x)),
              y: Math.min(...points.map((point) => point.y)),
              width:
                Math.max(...points.map((point) => point.x)) - Math.min(...points.map((point) => point.x)),
              height:
                Math.max(...points.map((point) => point.y)) - Math.min(...points.map((point) => point.y)),
            },
          },
          attributes: { landmarks: points.length, blendshapes: shapes.length },
          model: { name: 'face_landmarker', version: 'tasks-vision' },
        });
        if (smile > 0.45 && now - this.lastExpression.smile > 1200) {
          this.lastExpression.smile = now;
          this.bus.emit({
            type: 'face.expressions',
            source: 'mediapipe.face',
            label: 'sourire',
            confidence: smile,
            timestamp: now,
            attributes: { smile, blink },
          });
        }
        if (blink > 0.55 && now - this.lastExpression.blink > 600) {
          this.lastExpression.blink = now;
          this.bus.emit({
            type: 'face.blink',
            source: 'mediapipe.face',
            label: 'clignement',
            confidence: blink,
            timestamp: now,
            attributes: { blink },
          });
        }
      }
    }

    if (runtime.hands && this.due('hands', HANDS_HZ, now)) {
      const started = performance.now();
      const result = runtime.hands.detectForVideo(this.video, timestamp);
      this.timings.hands = performance.now() - started;
      this.record('hands', this.timings.hands);
      const hands = (result.landmarks ?? []).slice(0, 2).map((landmarks, index) => {
        const points = toPoints(landmarks);
        const handedness = result.handedness?.[index]?.[0]?.categoryName ?? `main-${index + 1}`;
        const gesture = classifyGesture(points);
        this.bus.emit({
          type: 'hand.detected',
          source: 'mediapipe.hands',
          subjectId: handedness,
          confidence: 0.94,
          timestamp: now,
          geometry: {
            points,
            box: {
              x: Math.min(...points.map((point) => point.x)),
              y: Math.min(...points.map((point) => point.y)),
              width:
                Math.max(...points.map((point) => point.x)) - Math.min(...points.map((point) => point.x)),
              height:
                Math.max(...points.map((point) => point.y)) - Math.min(...points.map((point) => point.y)),
            },
          },
          attributes: { index, gesture: gesture.gesture, pinchRatio: gesture.pinchRatio },
          model: { name: 'hand_landmarker', version: 'tasks-vision' },
        });
        if (gesture.gesture !== 'inconnu' && gesture.confidence >= 0.6) {
          this.bus.emit({
            type: 'hand.gesture',
            source: 'mediapipe.hands',
            subjectId: handedness,
            label: gesture.gesture,
            confidence: gesture.confidence,
            timestamp: now,
            attributes: { pinchRatio: gesture.pinchRatio, extendedFingers: gesture.extendedFingers },
          });
        }
        return { points, handedness, gesture };
      });
      next.hands = hands;
      changed = true;
    }

    if (runtime.pose && this.due('pose', POSE_HZ, now)) {
      const started = performance.now();
      const result = runtime.pose.detectForVideo(this.video, timestamp);
      this.timings.pose = performance.now() - started;
      this.record('pose', this.timings.pose);
      const points = toPoints(result.landmarks?.[0]);
      next.pose = points;
      changed = true;
      if (points.length) {
        this.bus.emit({
          type: 'pose.detected',
          source: 'mediapipe.pose',
          confidence: 0.92,
          timestamp: now,
          geometry: { points },
          attributes: { landmarks: points.length },
          model: { name: 'pose_landmarker_lite', version: 'tasks-vision' },
        });
      }
    }

    if (runtime.objects && this.due('objects', OBJECTS_HZ, now)) {
      const started = performance.now();
      const result = runtime.objects.detectForVideo(this.video, timestamp);
      this.timings.objects = performance.now() - started;
      this.record('objects', this.timings.objects);
      const objects = (result.detections ?? []).slice(0, 8).flatMap((detection) => {
        const category = detection.categories?.[0];
        if (!category || !detection.boundingBox) return [];
        const box = detection.boundingBox;
        const item = {
          box: { x: box.originX / this.video.videoWidth, y: box.originY / this.video.videoHeight, width: box.width / this.video.videoWidth, height: box.height / this.video.videoHeight },
          label: category.displayName || category.categoryName,
          confidence: category.score,
        };
        this.bus.emit({
          type: 'object.detected',
          source: 'mediapipe.objects',
          label: item.label,
          confidence: item.confidence,
          timestamp: now,
          geometry: { box: item.box },
          attributes: { category: category.categoryName },
          model: { name: 'efficientdet_lite0', version: 'tasks-vision' },
        });
        return [item];
      });
      next.objects = objects;
      changed = true;
    }

    if (runtime.gestures && this.due('gestures', GESTURES_HZ, now)) {
      const started = performance.now();
      const result = runtime.gestures.recognizeForVideo(this.video, timestamp);
      this.timings.gestures = performance.now() - started;
      this.record('gestures', this.timings.gestures);
      for (const categories of result.gestures ?? []) {
        const top = categories?.[0];
        if (top && top.score > 0.4) {
          this.bus.emit({
            type: 'hand.gesture',
            source: 'mediapipe.gestures',
            label: top.categoryName.toLowerCase(),
            confidence: top.score,
            timestamp: now,
            attributes: { classifier: 'mediapipe-gesture-recognizer' },
          });
        }
      }
    }

    if (changed) {
      next.updatedAt = now;
      this.snapshot = next;
      this.onSnapshot(next);
    }
  }
}
