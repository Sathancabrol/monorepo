import { describe, expect, it } from 'vitest';
import { MODEL_CATALOG } from './modelManager';
import { PLUGIN_CATALOG } from './pluginCatalog';

describe('plugin catalog', () => {
  it('has unique ids and explicit permissions', () => {
    const ids = PLUGIN_CATALOG.map((plugin) => plugin.id);
    expect(new Set(ids).size).toBe(ids.length);
    for (const plugin of PLUGIN_CATALOG) {
      expect(plugin.version).toMatch(/^\d+\.\d+\.\d+/);
      expect(Array.isArray(plugin.permissions)).toBe(true);
    }
  });

  it('references only known models', () => {
    const known = new Set(MODEL_CATALOG.map((model) => model.id));
    for (const plugin of PLUGIN_CATALOG) {
      for (const model of plugin.models) expect(known.has(model)).toBe(true);
    }
  });

  it('does not claim planned plugins are ready', () => {
    for (const plugin of PLUGIN_CATALOG.filter((entry) => entry.id.startsWith('planned.'))) {
      expect(plugin.status).toBe('planned');
    }
  });
});
