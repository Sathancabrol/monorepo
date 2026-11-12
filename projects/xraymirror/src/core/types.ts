/** Shared types for the Studio core. Keep this module dependency-free (also used by tests). */

export type Runtime = 'browser' | 'python' | 'native';
export type Permission = 'camera' | 'microphone' | 'network' | 'storage' | 'biometrics';

export type PluginCategory =
  | 'perception'
  | 'audio'
  | 'anatomy'
  | 'creator'
  | 'nutrition'
  | 'education'
  | 'system';

export type PluginStatus = 'core' | 'ready' | 'preview' | 'planned';

export interface PluginManifest {
  id: string;
  name: string;
  version: string;
  description: string;
  category: PluginCategory;
  status: PluginStatus;
  runtime: Runtime;
  inputs: Array<'video' | 'audio' | 'events' | 'manual'>;
  outputs: Array<'events' | 'overlay' | 'panel' | 'export'>;
  permissions: Permission[];
  network: boolean;
  gpu: { required: boolean; exclusive: boolean; vramMb: number };
  models: string[];
  cadenceHz: number;
}

export type EventType =
  | 'face.detected'
  | 'face.blink'
  | 'face.expressions'
  | 'hand.detected'
  | 'hand.gesture'
  | 'pinch.state'
  | 'pose.detected'
  | 'object.detected'
  | 'barcode.detected'
  | 'sound.detected'
  | 'audio.level'
  | 'session.state'
  | 'rule.fired'
  | 'system.metric';

export interface GeometryPoint {
  x: number;
  y: number;
  z?: number;
}

export interface EventGeometry {
  box?: { x: number; y: number; width: number; height: number };
  points?: GeometryPoint[];
  value?: number;
}

export interface StudioEvent<T = Record<string, unknown>> {
  id: string;
  timestamp: number;
  type: EventType | string;
  source: string;
  subjectId?: string;
  label?: string;
  confidence?: number;
  geometry?: EventGeometry;
  attributes: T;
  model?: { name: string; version: string };
}

export type EventDraft<T = Record<string, unknown>> = Omit<StudioEvent<T>, 'id' | 'timestamp'> & {
  timestamp?: number;
};

export interface ModuleMetric {
  fps: number;
  latencyMs: number;
  lastError: string | null;
}

export type ModuleMetrics = Record<string, ModuleMetric>;

export type ModuleId = 'face' | 'hands' | 'pose' | 'objects' | 'gestures' | 'audio';

export interface DetectorSettings {
  face: boolean;
  hands: boolean;
  pose: boolean;
  objects: boolean;
  audio: boolean;
  gestures: boolean;
}

export interface FrameCtx {
  video: HTMLVideoElement;
  bounds: { width: number; height: number };
  timestampMs: number;
}

/** An inference loop driven by the media engine. */
export interface DetectorModule {
  id: ModuleId;
  label: string;
  cadenceMs: number;
  requires?: 'camera' | 'microphone';
  warmup?: () => Promise<void>;
  process?: (ctx: FrameCtx) => Promise<void> | void;
  /** Audio modules run outside the video loop and use their own lifecycle. */
  start?: () => Promise<void>;
  stop?: () => void;
  status: () => string;
}

export interface RuleAction {
  type: 'show-toast' | 'toggle-layer' | 'start-recording' | 'stop-recording' | 'clear-paint';
  payload?: Record<string, string | number | boolean>;
}

export interface RuleDefinition {
  id: string;
  name: string;
  enabled: boolean;
  trigger: string;
  matchLabel?: string;
  minConfidence: number;
  cooldownMs: number;
  action: RuleAction;
}

export interface RuleFiring {
  ruleId: string;
  at: number;
  eventId: string;
}
