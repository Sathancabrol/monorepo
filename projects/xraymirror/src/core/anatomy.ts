import type { NormalizedPoint } from './filters';
import { midpoint } from './filters';
import { POSE } from './filters';

export type AnatomyLayer =
  | 'skeleton'
  | 'muscles'
  | 'nervous'
  | 'organs'
  | 'vessels'
  | 'labels';

export const ANATOMY_LAYERS: Array<{ id: AnatomyLayer; label: string; color: string }> = [
  { id: 'skeleton', label: 'Squelette', color: '#e8f6ff' },
  { id: 'muscles', label: 'Muscles', color: '#ff7c8a' },
  { id: 'nervous', label: 'Nerfs', color: '#ffd166' },
  { id: 'organs', label: 'Organes', color: '#8fe3a5' },
  { id: 'vessels', label: 'Vaisseaux', color: '#ff5c5c' },
  { id: 'labels', label: 'Étiquettes', color: '#9ad7ff' },
];

interface Bone {
  id: string;
  label: string;
  system: string;
  a: NormalizedPoint;
  b: NormalizedPoint;
}

function scaled(a: NormalizedPoint, b: NormalizedPoint, factor: number): NormalizedPoint {
  return {
    x: a.x + (b.x - a.x) * factor,
    y: a.y + (b.y - a.y) * factor,
    z: (a.z ?? 0) + ((b.z ?? 0) - (a.z ?? 0)) * factor,
  };
}

/**
 * Builds schematic long bones + torso anchors from 33 MediaPipe pose landmarks.
 * It is an educational overlay, explicitly not a clinical measurement.
 * Coordinates use normalized video space [0..1].
 */
export function buildSkeletalAnchors(points: NormalizedPoint[]): Bone[] {
  if (points.length < 29) return [];
  const p = (index: number) => ({
    x: points[index].x,
    y: points[index].y,
    z: points[index].z ?? 0,
    visibility: points[index].visibility,
  });

  const ls = p(POSE.leftShoulder);
  const rs = p(POSE.rightShoulder);
  const lh = p(POSE.leftHip);
  const rh = p(POSE.rightHip);
  const neck = scaled(midpoint(ls, rs), midpoint(lh, rh), 0.08);
  const pelvis = midpoint(lh, rh);
  // Visibility propagates through the synthetic points to the bones they feed.
  neck.visibility = Math.min(ls.visibility ?? 1, rs.visibility ?? 1);
  const spineMid = midpoint(neck, pelvis);

  const bones: Bone[] = [
    { id: 'skull', label: 'Crâne', system: 'skeleton', a: p(POSE.nose), b: neck },
    { id: 'clavicle.l', label: 'Clavicule G', system: 'skeleton', a: neck, b: ls },
    { id: 'clavicle.r', label: 'Clavicule D', system: 'skeleton', a: neck, b: rs },
    { id: 'humerus.l', label: 'Humérus G', system: 'skeleton', a: ls, b: p(POSE.leftElbow) },
    { id: 'humerus.r', label: 'Humérus D', system: 'skeleton', a: rs, b: p(POSE.rightElbow) },
    { id: 'radius.l', label: 'Radius G', system: 'skeleton', a: p(POSE.leftElbow), b: p(POSE.leftWrist) },
    { id: 'radius.r', label: 'Radius D', system: 'skeleton', a: p(POSE.rightElbow), b: p(POSE.rightWrist) },
    { id: 'spine', label: 'Colonne', system: 'skeleton', a: neck, b: pelvis },
    { id: 'sacrum', label: 'Sacrum', system: 'skeleton', a: pelvis, b: scaled(pelvis, p(POSE.leftKnee), 0.16) },
    { id: 'femur.l', label: 'Fémur G', system: 'skeleton', a: lh, b: p(POSE.leftKnee) },
    { id: 'femur.r', label: 'Fémur D', system: 'skeleton', a: rh, b: p(POSE.rightKnee) },
    { id: 'tibia.l', label: 'Tibia G', system: 'skeleton', a: p(POSE.leftKnee), b: p(POSE.leftAnkle) },
    { id: 'tibia.r', label: 'Tibia D', system: 'skeleton', a: p(POSE.rightKnee), b: p(POSE.rightAnkle) },
  ];

  // Extra anchors shown as anatomy points.
  bones.push({ id: 'abdomen', label: 'Abdomen', system: 'organs', a: spineMid, b: pelvis });
  bones.push({ id: 'thorax', label: 'Cage thoracique', system: 'organs', a: neck, b: spineMid });

  return bones;
}

export function boneProgress(bone: Bone, t: number): NormalizedPoint {
  return {
    x: bone.a.x + (bone.b.x - bone.a.x) * t,
    y: bone.a.y + (bone.b.y - bone.a.y) * t,
    z: (bone.a.z ?? 0) + ((bone.b.z ?? 0) - (bone.a.z ?? 0)) * t,
  };
}

export interface AnatomyCoverage {
  total: number;
  /** Anchors emitted from the pose, regardless of visibility. */
  withPoseAnchor: number;
  /** Anchors whose two endpoints are actually visible enough to trust. */
  visible: number;
  ratio: number;
}

const MIN_VISIBILITY = 0.35;
/** 13 long bones + thorax + abdomen schematic anchors. */
export const TOTAL_ANATOMY_ANCHORS = 15;

export function isBoneVisible(bone: Bone, minimum = MIN_VISIBILITY): boolean {
  return (bone.a.visibility ?? 1) >= minimum && (bone.b.visibility ?? 1) >= minimum;
}

export function coverageFromBones(bones: Bone[]): AnatomyCoverage {
  const total = TOTAL_ANATOMY_ANCHORS;
  const visible = bones.filter((bone) => isBoneVisible(bone)).length;
  return {
    total,
    withPoseAnchor: Math.min(total, bones.length),
    visible,
    ratio: Math.min(1, visible / total),
  };
}

export function formatCoverage(coverage: AnatomyCoverage): string {
  return `${coverage.visible}/${coverage.total} ancrages visibles · ${Math.round(coverage.ratio * 100)} %`;
}
