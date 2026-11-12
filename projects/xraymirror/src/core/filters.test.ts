import { describe, expect, it } from 'vitest';
import { OneEuroFilter, Vec2Filter } from './filters';

describe('one euro filter', () => {
  it('passes the first sample through and reduces jitter', () => {
    const filter = new OneEuroFilter(1, 0.02);
    expect(filter.filter(10, 0)).toBe(10);
    const noisy = [10.4, 9.6, 10.3, 9.7, 10.2, 9.8];
    const output = noisy.map((value, index) => filter.filter(value, (index + 1) * 33));
    const variance = output.reduce((sum, value) => sum + Math.abs(value - 10), 0) / output.length;
    expect(variance).toBeLessThan(0.25);
  });

  it('rejects NaN and keeps the last value', () => {
    const filter = new OneEuroFilter();
    filter.filter(4, 0);
    filter.filter(5, 33);
    expect(filter.filter(Number.NaN, 66)).toBeCloseTo(4.21, 1);
  });

  it('filters both axes', () => {
    const filter = new Vec2Filter();
    const first = filter.filter(0.2, 0.8, 0);
    expect(first).toEqual({ x: 0.2, y: 0.8 });
    filter.reset();
    expect(filter.filter(0.7, 0.3, 10)).toEqual({ x: 0.7, y: 0.3 });
  });
});
