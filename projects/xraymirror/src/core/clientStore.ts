import type { DetectorSettings, RuleDefinition } from './types';

const SETTINGS_KEY = 'xraymirror.settings.v1';

export interface StoredSettings {
  detectors: DetectorSettings;
  rules: RuleDefinition[];
  modelCache: {
    mode: 'auto' | 'local-only' | 'remote-only';
    note: string;
  };
  anatomy: {
    opacity: number;
    lens: boolean;
    labels: boolean;
    layers: Record<string, boolean>;
  };
  paint: {
    /** Held fist (~0.9 s) clears the canvas. Off by default: destructive. */
    clearWithFist: boolean;
  };
  privacy: {
    storeRawMedia: boolean;
    anonymizeExports: boolean;
  };
}

export function loadSettings(fallback: StoredSettings): StoredSettings {
  try {
    const raw = localStorage.getItem(SETTINGS_KEY);
    if (!raw) return fallback;
    const parsed = JSON.parse(raw) as Partial<StoredSettings>;
    return {
      ...fallback,
      ...parsed,
      detectors: { ...fallback.detectors, ...(parsed.detectors ?? {}) },
      rules: Array.isArray(parsed.rules) ? parsed.rules : fallback.rules,
      anatomy: { ...fallback.anatomy, ...(parsed.anatomy ?? {}) },
      paint: { ...fallback.paint, ...(parsed.paint ?? {}) },
      privacy: { ...fallback.privacy, ...(parsed.privacy ?? {}) },
      modelCache: { ...fallback.modelCache, ...(parsed.modelCache ?? {}) },
    };
  } catch {
    return fallback;
  }
}

export function saveSettings(settings: StoredSettings): void {
  try {
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
  } catch {
    // Quota or private mode: never break the live session for settings persistence.
  }
}

export function downloadText(filename: string, content: string, mime = 'application/json'): void {
  const blob = new Blob([content], { type: `${mime};charset=utf-8` });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  setTimeout(() => URL.revokeObjectURL(url), 1500);
}
