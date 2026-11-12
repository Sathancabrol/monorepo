import type { NormalizedPoint } from './filters';

export interface Stroke {
  id: string;
  color: string;
  width: number;
  points: NormalizedPoint[];
}

export class PaintModel {
  strokes: Stroke[] = [];
  color = '#59f2c8';
  width = 0.004;
  private active: Stroke | null = null;
  private counter = 0;

  setStyle(color: string, width: number): void {
    this.color = color;
    this.width = width;
  }

  begin(point: NormalizedPoint, color = this.color, width = this.width): Stroke {
    const stroke: Stroke = {
      id: `stroke_${Date.now().toString(36)}_${this.counter++}`,
      color,
      width,
      points: [{ ...point }],
    };
    this.strokes.push(stroke);
    this.active = stroke;
    return stroke;
  }

  append(point: NormalizedPoint): void {
    if (!this.active) return;
    const last = this.active.points.at(-1);
    if (last && Math.hypot(last.x - point.x, last.y - point.y) < 0.0025) return;
    this.active.points.push({ ...point });
  }

  end(): void {
    this.active = null;
  }

  get isDrawing(): boolean {
    return this.active !== null;
  }

  clear(): void {
    this.strokes = [];
    this.active = null;
  }

  undo(): void {
    this.strokes.pop();
    this.active = null;
  }

  /** Minimal deterministic SVG export in a 1000x1000 viewbox. */
  toSvg(): string {
    const paths = this.strokes
      .filter((stroke) => stroke.points.length > 1)
      .map((stroke) => {
        const commands = stroke.points
          .map((point, index) => `${index === 0 ? 'M' : 'L'}${(point.x * 1000).toFixed(1)} ${(point.y * 1000).toFixed(1)}`)
          .join(' ');
        return `<path d="${commands}" fill="none" stroke="${stroke.color}" stroke-width="${(stroke.width * 1000).toFixed(1)}" stroke-linecap="round" stroke-linejoin="round"/>`;
      })
      .join('');
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">${paths}</svg>`;
  }
}
