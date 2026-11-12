import { describe, expect, it } from 'vitest';
import { buildSkeletalAnchors, coverageFromBones, boneProgress, isBoneVisible } from './anatomy';

function makePose() {
  const points: Array<{ x: number; y: number; z: number; visibility?: number }> = Array.from(
    { length: 33 },
    (_, index) => ({ x: 0.45 + (index % 3) * 0.05, y: 0.2 + (index / 33) * 0.6, z: 0 }),
  );
  points[0] = { x: 0.5, y: 0.1, z: 0 };
  points[11] = { x: 0.42, y: 0.3, z: 0 };
  points[12] = { x: 0.58, y: 0.3, z: 0 };
  points[13] = { x: 0.36, y: 0.42, z: 0 };
  points[14] = { x: 0.64, y: 0.42, z: 0 };
  points[15] = { x: 0.32, y: 0.54, z: 0 };
  points[16] = { x: 0.68, y: 0.54, z: 0 };
  points[23] = { x: 0.45, y: 0.58, z: 0 };
  points[24] = { x: 0.55, y: 0.58, z: 0 };
  points[25] = { x: 0.43, y: 0.75, z: 0 };
  points[26] = { x: 0.57, y: 0.75, z: 0 };
  points[27] = { x: 0.42, y: 0.92, z: 0 };
  points[28] = { x: 0.58, y: 0.92, z: 0 };
  return points;
}

describe('anatomy anchors', () => {
  it('builds the expected schematic skeleton and coverage', () => {
    const bones = buildSkeletalAnchors(makePose());
    expect(bones.length).toBeGreaterThanOrEqual(13);
    expect(bones.map((bone) => bone.id)).toContain('femur.l');
    expect(bones.every((bone) => Number.isFinite(bone.a.x) && Number.isFinite(bone.b.y))).toBe(true);
    expect(coverageFromBones(bones).ratio).toBe(1);
  });

  it('interpolates a bone at t=0.5 without mutating the source', () => {
    const bone = buildSkeletalAnchors(makePose())[0];
    const middle = boneProgress(bone, 0.5);
    expect(middle.x).toBeCloseTo((bone.a.x + bone.b.x) / 2);
    expect(bone.a.x).toBe(bone.a.x);
  });

  it('returns no anchors when the pose is incomplete', () => {
    expect(buildSkeletalAnchors([{ x: 0, y: 0 }])).toEqual([]);
  });
});

describe('anatomy visibility', () => {
  it('counts only anchors whose endpoints are actually visible', () => {
    const pose = makePose();
    // Hide left knee and left ankle: femur.l / tibia.l must not count as visible.
    pose[25] = { x: 0.43, y: 0.75, z: 0, visibility: 0.05 };
    pose[27] = { x: 0.42, y: 0.92, z: 0, visibility: 0.05 };
    const coverage = coverageFromBones(buildSkeletalAnchors(pose));
    expect(coverage.withPoseAnchor).toBeGreaterThanOrEqual(coverage.visible);
    expect(coverage.visible).toBeLessThan(coverage.total);
    expect(coverage.ratio).toBeLessThan(1);
  });

  it('treats missing visibility as visible (backward compatible)', () => {
    const coverage = coverageFromBones(buildSkeletalAnchors(makePose()));
    expect(coverage.visible).toBe(coverage.total);
  });
});
