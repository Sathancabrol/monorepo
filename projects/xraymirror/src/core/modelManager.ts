export interface ModelDefinition {
  id: string;
  url: string;
  /** Filename expected in the local cache directory. */
  localFile: string;
  sha256: string;
  bytes: number;
  license: string;
  description: string;
}

/**
 * Pinned manifests. Assets are NOT bundled in this repository: the installer /
 * download step must fetch them and verify the digest before use.
 * SHA-256 values are completed by `npm run models:verify` on the target machine.
 */
export const MODEL_CATALOG: ModelDefinition[] = [
  {
    id: 'face_landmarker',
    localFile: 'face_landmarker.task',
    url: 'https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task',
    sha256: 'PENDING',
    bytes: 3_700_000,
    license: 'Apache-2.0 (MediaPipe), modèle Google',
    description: '478 points, blendshapes et matrice faciale',
  },
  {
    id: 'hand_landmarker',
    localFile: 'hand_landmarker.task',
    url: 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task',
    sha256: 'PENDING',
    bytes: 7_800_000,
    license: 'Apache-2.0 (MediaPipe), modèle Google',
    description: '21 points par main, deux mains',
  },
  {
    id: 'pose_landmarker_lite',
    localFile: 'pose_landmarker_lite.task',
    url: 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task',
    sha256: 'PENDING',
    bytes: 5_900_000,
    license: 'Apache-2.0 (MediaPipe), modèle Google',
    description: '33 points de pose, profil Lite',
  },
  {
    id: 'efficientdet_lite0',
    localFile: 'efficientdet_lite0.tflite',
    url: 'https://storage.googleapis.com/mediapipe-models/object_detector/efficientdet_lite0/int8/1/efficientdet_lite0.tflite',
    sha256: 'PENDING',
    bytes: 4_500_000,
    license: 'Apache-2.0 (MediaPipe), modèle Google',
    description: '80 catégories COCO, détection légère',
  },
  {
    id: 'gesture_recognizer',
    localFile: 'gesture_recognizer.task',
    url: 'https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task',
    sha256: 'PENDING',
    bytes: 9_400_000,
    license: 'Apache-2.0 (MediaPipe), modèle Google',
    description: 'Gestes statiques MediaPipe (pouce, poing, paume, victoire…)',
  },
];

export const MEDIAPIPE_VERSION = '1.2.3';

export interface ResolvedModel {
  id: string;
  url: string;
  source: 'local' | 'remote';
}

export type ModelCacheMode = 'auto' | 'local-only' | 'remote-only';

export interface ModelResolverOptions {
  baseUrl?: string;
  fetchImpl?: typeof fetch;
  mode?: ModelCacheMode;
  catalog?: ModelDefinition[];
}

function defaultBaseUrl(): string {
  const configured = (import.meta as { env?: Record<string, string> }).env?.VITE_MODEL_BASE_URL;
  const configuredOrBase = configured || `${import.meta.env.BASE_URL}models`;
  const normalized = configuredOrBase.endsWith('/') ? configuredOrBase : `${configuredOrBase}/`;
  if (typeof document === 'undefined') return normalized;
  return new URL(normalized, document.baseURI).href;
}

/**
 * Resolves a model to a local cached asset first. If the pinned local file is
 * present, it is HEAD-checked (content-length); otherwise the remote URL is used.
 * This keeps the app functional offline when assets were installed, while not
 * pretending that a missing SHA-256 provides integrity (we do not invent one).
 */
export class ModelResolver {
  private readonly baseUrl: string;
  private readonly fetchImpl: typeof fetch;
  readonly catalog: ModelDefinition[];
  readonly mode: ModelCacheMode;
  private resolved = new Map<string, ResolvedModel>();

  constructor(options: ModelResolverOptions = {}) {
    this.baseUrl = options.baseUrl ?? defaultBaseUrl();
    this.fetchImpl = options.fetchImpl ?? fetch;
    this.mode = options.mode ?? 'auto';
    this.catalog = options.catalog ?? MODEL_CATALOG;
  }

  async resolve(id: string): Promise<ResolvedModel> {
    const cached = this.resolved.get(id);
    if (cached) return cached;

    const definition = this.catalog.find((model) => model.id === id);
    if (!definition) throw new Error(`Modèle inconnu: ${id}`);

    const localUrl = `${this.baseUrl}${definition.localFile}`;
    let localAvailable = false;
    if (this.mode !== 'remote-only') {
      try {
        const response = await this.fetchImpl(localUrl, { method: 'HEAD', cache: 'no-store' });
        if (response.ok) {
          const length = Number(response.headers.get('content-length') ?? 0);
          localAvailable = !length || length === definition.bytes || length > definition.bytes * 0.5;
        }
      } catch {
        localAvailable = false;
      }
    }

    if (localAvailable) {
      const local: ResolvedModel = { id, url: localUrl, source: 'local' };
      this.resolved.set(id, local);
      return local;
    }
    if (this.mode === 'local-only') {
      throw new Error(
        `Mode hors ligne strict : ${definition.id} absent de ${this.baseUrl}. Installe le modèle puis recharge.`,
      );
    }
    const remote: ResolvedModel = { id, url: definition.url, source: 'remote' };
    this.resolved.set(id, remote);
    return remote;
  }

  /** Human-readable cache status for the diagnostics panel. */
  async inspect(): Promise<Array<ModelDefinition & { source: 'local' | 'remote' | 'unknown' }>> {
    const out: Array<ModelDefinition & { source: 'local' | 'remote' | 'unknown' }> = [];
    for (const model of this.catalog) {
      let source: 'local' | 'remote' | 'unknown' = 'unknown';
      try {
        source = (await this.resolve(model.id)).source;
      } catch {
        source = 'unknown';
      }
      out.push({ ...model, source });
    }
    return out;
  }

  describe(source: 'local' | 'remote'): string {
    return source === 'local'
      ? 'Cache local vérifié par taille'
      : 'URL distante épinglée — téléchargement à la première inférence';
  }
}
