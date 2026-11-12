export interface PixelBox {
  x: number;
  y: number;
  width: number;
  height: number;
}

export function faceBoxFromPoints(
  points: Array<{ x: number; y: number }>,
  videoWidth: number,
  videoHeight: number,
): PixelBox | null {
  if (points.length === 0) return null;
  const minX = Math.min(...points.map((point) => point.x)) * videoWidth;
  const maxX = Math.max(...points.map((point) => point.x)) * videoWidth;
  const minY = Math.min(...points.map((point) => point.y)) * videoHeight;
  const maxY = Math.max(...points.map((point) => point.y)) * videoHeight;
  return { x: minX, y: minY, width: maxX - minX, height: maxY - minY };
}

export function expandBox(box: PixelBox, ratio: number): PixelBox {
  const padX = box.width * ratio;
  const padY = box.height * ratio;
  return { x: box.x - padX, y: box.y - padY, width: box.width + padX * 2, height: box.height + padY * 2 };
}

export function clampBox(box: PixelBox, width: number, height: number): PixelBox {
  const x = Math.max(0, Math.min(width, box.x));
  const y = Math.max(0, Math.min(height, box.y));
  return {
    x,
    y,
    width: Math.max(0, Math.min(width - x, box.width)),
    height: Math.max(0, Math.min(height - y, box.height)),
  };
}
