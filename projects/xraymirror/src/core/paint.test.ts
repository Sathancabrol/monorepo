import { describe, expect, it } from 'vitest';
import { PaintModel } from './paint';

describe('paint model', () => {
  it('draws, ignores micro-movements and exports SVG', () => {
    const model = new PaintModel();
    model.begin({ x: 0.1, y: 0.2 }, '#5ff', 0.004);
    model.append({ x: 0.1, y: 0.2 });
    model.append({ x: 0.5, y: 0.6 });
    model.end();
    expect(model.strokes[0].points).toHaveLength(2);
    const svg = model.toSvg();
    expect(svg).toContain('<svg');
    expect(svg).toContain('stroke="#5ff"');
  });

  it('undoes and clears strokes', () => {
    const model = new PaintModel();
    model.begin({ x: 0, y: 0 }, '#fff', 0.004);
    model.append({ x: 1, y: 1 });
    model.end();
    model.undo();
    expect(model.strokes).toHaveLength(0);
    model.begin({ x: 0, y: 0 }, '#fff', 0.004);
    model.clear();
    expect(model.strokes).toHaveLength(0);
  });
});
