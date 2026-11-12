import { describe, expect, it } from 'vitest';
import { normalizeBarcode } from './nutrition';

describe('nutrition helpers', () => {
  it('normalizes typed barcodes', () => {
    expect(normalizeBarcode('3017620422003')).toBe('3017620422003');
    expect(normalizeBarcode(' 3017 620 422003 ')).toBe('3017620422003');
    expect(normalizeBarcode('abc')).toBe('');
    expect(normalizeBarcode('12345678901234567890')).toHaveLength(14);
  });
});
