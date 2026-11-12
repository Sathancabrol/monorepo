import { describe, expect, it } from 'vitest';
import { classifyGesture, GestureStabilizer, pinchRatio } from './gestures';

function hand(options: {
  thumb?: [number, number];
  index?: [number, number];
  extended?: number[];
}) {
  const points = Array.from({ length: 21 }, () => ({ x: 0.5, y: 0.6 }));
  points[0] = { x: 0.5, y: 0.8 }; // wrist
  points[9] = { x: 0.5, y: 0.5 }; // middle MCP, hand size = 0.3
  points[3] = { x: 0.38, y: 0.7 };
  points[4] = options.thumb ? { x: options.thumb[0], y: options.thumb[1] } : { x: 0.36, y: 0.68 };
  points[8] = options.index ? { x: options.index[0], y: options.index[1] } : { x: 0.68, y: 0.7 };
  // PIP joints sit between wrist and tips; tips are far when "extended"
  const tips = [8, 12, 16, 20];
  const pips = [6, 10, 14, 18];
  tips.forEach((tip, index) => {
    const isExtended = options.extended?.includes(tip);
    points[pips[index]] = { x: 0.5 + index * 0.01, y: 0.54 };
    points[tip] = isExtended ? { x: 0.5 + index * 0.01, y: 0.35 } : { x: 0.5 + index * 0.01, y: 0.68 };
  });
  return points;
}

describe('gesture classifier', () => {
  it('classifies a pinch when thumb and index tips are close', () => {
    // Thumb tip and index tip are close *and* both sit away from the wrist.
    const points = hand({ thumb: [0.56, 0.36], index: [0.57, 0.35], extended: [8] });
    points[3] = { x: 0.5, y: 0.55 };
    const result = classifyGesture(points);
    expect(result.gesture).toBe('pincement');
    expect(result.pinchRatio).toBeLessThan(0.32);
  });

  it('classifies an open palm', () => {
    const result = classifyGesture(hand({ thumb: [0.3, 0.5], index: [0.7, 0.4], extended: [8, 12, 16, 20] }));
    expect(result.gesture).toBe('paume');
  });

  it('classifies a fist when no finger is extended', () => {
    // Build a closed hand: every tip/thumb is close to the wrist.
    const points = hand({});
    const tips = [8, 12, 16, 20];
    const pips = [6, 10, 14, 18];
    tips.forEach((_, index) => {
      points[tips[index]] = { x: 0.5 + index * 0.01, y: 0.76 };
      points[pips[index]] = { x: 0.5 + index * 0.01, y: 0.6 };
    });
    // Keep thumb tip far from the index tip so the closed hand is not a pinch.
    points[4] = { x: 0.36, y: 0.66 };
    points[3] = { x: 0.4, y: 0.62 };
    expect(classifyGesture(points).gesture).toBe('poing');
  });

  it('returns infinity without landmarks', () => {
    expect(pinchRatio([])).toBe(Number.POSITIVE_INFINITY);
  });
});

describe('gesture stabilizer', () => {
  it('requires two consecutive samples before accepting a gesture', () => {
    const stabilizer = new GestureStabilizer();
    const sample = { gesture: 'poing' as const, confidence: 1, pinchRatio: 1, extendedFingers: 0 };
    expect(stabilizer.update(sample).gesture).toBe('inconnu');
    expect(stabilizer.update(sample)).toEqual({ gesture: 'poing', changed: true });
    expect(stabilizer.update(sample).changed).toBe(false);
  });
});
