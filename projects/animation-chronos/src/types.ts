export type PerspectiveMode = 'vessel' | 'core';

export interface DiscoveryStage {
  id: number;
  phase: string;
  title: string;
  subtitle: string;
  description: string;
  focusPoint: { x: number; y: number; zoom: number }; // percentages
  visualHighlight?: 'glass' | 'ferrofluid' | 'filaments' | 'brain' | 'core';
}

export interface Hotspot {
  id: string;
  title: string;
  classification: string;
  x: number; // percentage
  y: number; // percentage
  description: string;
  detail: string;
  stageId: number;
}
