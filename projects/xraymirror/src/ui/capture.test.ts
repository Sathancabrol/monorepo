import { describe, expect, it } from 'vitest';
import { faceBoxFromPoints, expandBox, clampBox } from './capture';

describe('capture anonymisation geometry', () => {
  it('computes a padded face box in pixels', () => {
    const box = faceBoxFromPoints(
      [
        { x: 0.4, y: 0.2 },
        { x: 0.6, y: 0.4 },
      ],
      1280,
      720,
    );
    expect(box).toEqual({ x: 512, y: 144, width: 256, height: 144 });
  });

  it('returns null without landmarks', () => {
    expect(faceBoxFromPoints([], 1280, 720)).toBeNull();
  });

  it('expands and clamps a box inside the frame', () => {
    const expanded = expandBox({ x: 10, y: 10, width: 100, height: 100 }, 0.2);
    expect(expanded.width).toBeCloseTo(140);
    expect(clampBox({ x: -20, y: 700, width: 100, height: 100 }, 1280, 720)).toEqual({
      x: 0,
      y: 700,
      width: 100,
      height: 20,
    });
  });
});
