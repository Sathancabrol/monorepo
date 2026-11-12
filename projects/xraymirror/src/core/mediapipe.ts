import {
  FaceLandmarker,
  FilesetResolver,
  GestureRecognizer,
  HandLandmarker,
  ObjectDetector,
  PoseLandmarker,
  type NormalizedLandmark,
} from '@mediapipe/tasks-vision';
import { MEDIAPIPE_VERSION, ModelResolver, type ModelCacheMode } from './modelManager';

export interface MediaPipeRuntime {
  face?: FaceLandmarker;
  hands?: HandLandmarker;
  pose?: PoseLandmarker;
  objects?: ObjectDetector;
  gestures?: GestureRecognizer;
}

let filesetPromise: Promise<Awaited<ReturnType<typeof FilesetResolver.forVisionTasks>>> | null = null;

function fileset() {
  if (!filesetPromise) {
    // Absolute URL matters: the loader is dynamically imported, and a relative
    // './mediapipe/...' path would resolve against assets/ instead of the app root.
    const wasmDir = new URL('mediapipe/wasm/', document.baseURI).href;
    filesetPromise = FilesetResolver.forVisionTasks(wasmDir).catch((error) => {
      // Do not cache a rejected promise: a transient network failure must be retryable.
      filesetPromise = null;
      throw error;
    });
  }
  return filesetPromise;
}

export type EngineKind = 'face' | 'hands' | 'pose' | 'objects' | 'gestures';

export class MediaPipeEngine {
  readonly runtime: MediaPipeRuntime = {};
  private readonly starting = new Map<EngineKind, Promise<void>>();
  readonly errors: string[] = [];
  private readonly modelResolver: ModelResolver;
  private delegate: 'GPU' | 'CPU';

  constructor(delegate: 'GPU' | 'CPU' = 'GPU', modelMode: ModelCacheMode = 'auto') {
    this.delegate = delegate;
    this.modelResolver = new ModelResolver({ mode: modelMode });
  }

  get version(): string {
    return MEDIAPIPE_VERSION;
  }

  async ensure(kind: EngineKind): Promise<void> {
    if (this.runtime[kind]) return;
    const inFlight = this.starting.get(kind);
    if (inFlight) return inFlight;

    const job = this.createWithFallback(kind).catch((error: unknown) => {
      this.errors.push(`${kind}: ${error instanceof Error ? error.message : String(error)}`);
      throw error;
    });
    this.starting.set(kind, job);
    try {
      await job;
    } finally {
      this.starting.delete(kind);
    }
  }

  private async createWithFallback(kind: EngineKind): Promise<void> {
    try {
      await this.create(kind);
    } catch (error) {
      if (this.delegate !== 'GPU') throw error;
      // Some integrated GPUs / browsers reject the WebGL delegate. Retry once
      // on CPU rather than killing the whole perception pipeline.
      this.errors.push(`${kind}: GPU indisponible, repli CPU (${String(error)})`);
      this.delegate = 'CPU';
      await this.create(kind);
    }
  }

  private async create(kind: EngineKind): Promise<void> {
    const vision = await fileset();
    switch (kind) {
      case 'face': {
        if (this.runtime.face) return;
        const model = await this.modelResolver.resolve('face_landmarker');
        this.runtime.face = await FaceLandmarker.createFromOptions(vision, {
          baseOptions: { modelAssetPath: model.url, delegate: this.delegate },
          numFaces: 1,
          outputFaceBlendshapes: true,
          outputFacialTransformationMatrixes: true,
          runningMode: 'VIDEO',
        });
        return;
      }
      case 'hands': {
        if (this.runtime.hands) return;
        const model = await this.modelResolver.resolve('hand_landmarker');
        this.runtime.hands = await HandLandmarker.createFromOptions(vision, {
          baseOptions: { modelAssetPath: model.url, delegate: this.delegate },
          runningMode: 'VIDEO',
          numHands: 2,
        });
        return;
      }
      case 'gestures': {
        if (this.runtime.gestures) return;
        const model = await this.modelResolver.resolve('gesture_recognizer');
        this.runtime.gestures = await GestureRecognizer.createFromOptions(vision, {
          baseOptions: { modelAssetPath: model.url, delegate: this.delegate },
          runningMode: 'VIDEO',
          numHands: 2,
        });
        return;
      }
      case 'pose': {
        if (this.runtime.pose) return;
        const model = await this.modelResolver.resolve('pose_landmarker_lite');
        this.runtime.pose = await PoseLandmarker.createFromOptions(vision, {
          baseOptions: { modelAssetPath: model.url, delegate: this.delegate },
          runningMode: 'VIDEO',
          numPoses: 1,
        });
        return;
      }
      case 'objects': {
        if (this.runtime.objects) return;
        const model = await this.modelResolver.resolve('efficientdet_lite0');
        this.runtime.objects = await ObjectDetector.createFromOptions(vision, {
          baseOptions: { modelAssetPath: model.url, delegate: this.delegate },
          runningMode: 'VIDEO',
          scoreThreshold: 0.35,
          maxResults: 6,
          displayNamesLocale: 'fr',
        });
        return;
      }
    }
  }

  get ready(): MediaPipeRuntime {
    return this.runtime;
  }

  close(): void {
    for (const key of Object.keys(this.runtime) as EngineKind[]) {
      const value = this.runtime[key];
      try {
        (value as { close?: () => void } | undefined)?.close?.();
      } catch {
        // Already closed.
      }
      delete this.runtime[key];
    }
  }
}

/** Converts MediaPipe landmarks into our plain normalized point shape. */
export function toPoints(landmarks: NormalizedLandmark[] | undefined) {
  return (landmarks ?? []).map((point) => ({ x: point.x, y: point.y, z: point.z, visibility: point.visibility }));
}
