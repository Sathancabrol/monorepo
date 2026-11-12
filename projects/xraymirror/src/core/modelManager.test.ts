import { describe, expect, it, vi } from 'vitest';
import { ModelResolver, MODEL_CATALOG } from './modelManager';

function response(ok: boolean, headers: Record<string, string> = {}): Response {
  return { ok, headers: new Headers(headers) } as Response;
}

describe('model resolver', () => {
  it('uses a cached local file when present', async () => {
    const fetchImpl = vi.fn(async () => response(true, { 'content-length': String(MODEL_CATALOG[0].bytes) }));
    const resolver = new ModelResolver({ baseUrl: '/models/', fetchImpl });
    const resolved = await resolver.resolve(MODEL_CATALOG[0].id);
    expect(resolved.source).toBe('local');
    expect(resolved.url).toBe(`/models/${MODEL_CATALOG[0].localFile}`);
  });

  it('falls back to the pinned remote url when offline', async () => {
    const fetchImpl = vi.fn(async () => {
      throw new Error('offline');
    });
    const resolver = new ModelResolver({ baseUrl: '/models/', fetchImpl });
    const resolved = await resolver.resolve(MODEL_CATALOG[0].id);
    expect(resolved.source).toBe('remote');
    expect(resolved.url).toMatch(/^https:\/\//);
  });

  it('rejects unknown models', async () => {
    const resolver = new ModelResolver({ fetchImpl: vi.fn() });
    await expect(resolver.resolve('nope')).rejects.toThrow('Modèle inconnu');
  });

  it('memoizes resolutions', async () => {
    const fetchImpl = vi.fn(async () => response(false));
    const resolver = new ModelResolver({ fetchImpl });
    await resolver.resolve(MODEL_CATALOG[0].id);
    await resolver.resolve(MODEL_CATALOG[0].id);
    expect(fetchImpl).toHaveBeenCalledTimes(1);
  });
});

describe('cache modes', () => {
  it('fails explicitly in local-only mode instead of silently going remote', async () => {
    const fetchImpl = vi.fn(async () => response(false));
    const resolver = new ModelResolver({ baseUrl: '/models/', fetchImpl, mode: 'local-only' });
    await expect(resolver.resolve(MODEL_CATALOG[0].id)).rejects.toThrow(/hors ligne strict/);
  });

  it('skips the local HEAD request in remote-only mode', async () => {
    const fetchImpl = vi.fn(async () => response(true, { 'content-length': String(MODEL_CATALOG[0].bytes) }));
    const resolver = new ModelResolver({ fetchImpl, mode: 'remote-only' });
    const resolved = await resolver.resolve(MODEL_CATALOG[0].id);
    expect(resolved.source).toBe('remote');
    expect(fetchImpl).not.toHaveBeenCalled();
  });

  it('uses the local cache in auto mode when the HEAD check succeeds', async () => {
    const fetchImpl = vi.fn(async () => response(true, { 'content-length': String(MODEL_CATALOG[1].bytes) }));
    const resolver = new ModelResolver({ baseUrl: '/m/', fetchImpl, mode: 'auto' });
    expect((await resolver.resolve(MODEL_CATALOG[1].id)).url).toBe(`/m/${MODEL_CATALOG[1].localFile}`);
  });
});
