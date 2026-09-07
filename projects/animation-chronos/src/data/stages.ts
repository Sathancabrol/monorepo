import { DiscoveryStage, Hotspot } from '../types';

export const DISCOVERY_STAGES: DiscoveryStage[] = [
  {
    id: 1,
    phase: 'I',
    title: 'The Transparent Ovoid Vessel',
    subtitle: 'Flawless Geoid Glass & Microgravitational Equilibrium',
    description:
      'A single organic, subtly asymmetric egg-shaped geoid vessel floating in absolute weightlessness. Free of any pedestal, floor, or visible support. The optical surface exhibits physically accurate caustics, internal reflections, and a faint rim illuminated by distant cosmic radiation.',
    focusPoint: { x: 50, y: 50, zoom: 1.0 },
    visualHighlight: 'glass',
  },
  {
    id: 2,
    phase: 'II',
    title: 'Obsidian Ferrofluid Mass',
    subtitle: 'Viscous Metallic Liquid in Microgravity',
    description:
      'Suspended evenly throughout the vessel volume without sedimentation. Highly viscous, metallic, and obsidian-black with restrained dark violet and deep indigo undertones. Magnetic surface tension binds the fluid into swollen lobes and liquid bridges.',
    focusPoint: { x: 48, y: 52, zoom: 1.25 },
    visualHighlight: 'ferrofluid',
  },
  {
    id: 3,
    phase: 'III',
    title: 'Interconnected Magnetic Network',
    subtitle: 'Continuous Tendrils & Micro Bubbles',
    description:
      'Every secondary ferrofluid mass remains physically unified through ultra-thin, continuous liquid filaments—strictly devoid of isolated droplets. Spherical transparent air bubbles drift in microgravity, refracting the black fluid filaments around them.',
    focusPoint: { x: 52, y: 44, zoom: 1.55 },
    visualHighlight: 'filaments',
  },
  {
    id: 4,
    phase: 'IV',
    title: 'The Bilateral Hemispheres',
    subtitle: 'Two Uneven Masses & Longitudinal Fissure',
    description:
      'Liquid membranes stretching and slowly undulating under surface tension. Two large, uneven interconnected masses form an organic bilateral topology separated by a visible longitudinal fissure—strictly avoiding any radial or wheel-like symmetry.',
    focusPoint: { x: 50, y: 48, zoom: 1.9 },
    visualHighlight: 'brain',
  },
  {
    id: 5,
    phase: 'V',
    title: 'The Central Bridge Glow',
    subtitle: 'Narrow Organic Bridge & Softly Diffused Cold White-Blue Light',
    description:
      'Connecting the two uneven hemispheres across the fissure is a narrow liquid bridge carrying a faint cold white-blue glow, softly diffused into the surrounding dark violet ferrofluid without harsh point-sources or radiating spokes.',
    focusPoint: { x: 49.5, y: 49.2, zoom: 2.7 },
    visualHighlight: 'core',
  },
];

export const VESSEL_HOTSPOTS: Hotspot[] = [
  {
    id: 'core-light',
    title: 'Diffused Central Bridge',
    classification: 'Diffused Inter-Hemispheric Bridge',
    x: 49.6,
    y: 49.5,
    description: 'A faint cold white-blue glow softly diffused into the obsidian fluid across the narrow inter-lobar bridge.',
    detail: 'Non-radial soft diffusion across the central groove separating the two asymmetric cerebral masses.',
    stageId: 5,
  },
  {
    id: 'left-cerebral-lobe',
    title: 'Asymmetric Left Cerebral Mass',
    classification: 'Ferrofluid Lobe A',
    x: 42.0,
    y: 45.0,
    description: 'Convoluted magnetic fluid fold mimicking cerebral cortex sulci.',
    detail: 'Higher density ferrofluid mass with subtle embedded cosmic dust motes and micro-vortex spirals.',
    stageId: 4,
  },
  {
    id: 'right-cerebral-lobe',
    title: 'Asymmetric Right Cerebral Mass',
    classification: 'Ferrofluid Lobe B',
    x: 58.0,
    y: 47.0,
    description: 'Opposing cerebral lobe with looser organic curvature and thinner boundary membranes.',
    detail: 'Demonstrates authentic physical asymmetry rather than synthetic mirrored CAD geometry.',
    stageId: 4,
  },
  {
    id: 'magnetic-filaments',
    title: 'Continuous Liquid Bridges',
    classification: 'Capillary Tendrils',
    x: 51.0,
    y: 36.0,
    description: 'Ultra-thin branching filaments maintaining physical mass continuity.',
    detail: 'Governed by magnetic field lines and surface tension; ensures no severed or floating orphan droplets exist.',
    stageId: 3,
  },
  {
    id: 'refraction-bubble',
    title: 'Transparent Micro-Cavity',
    classification: 'Spherical Gas Void',
    x: 39.5,
    y: 56.0,
    description: 'Spherical air inclusion refracting the obsidian liquid behind it.',
    detail: 'True double-surface Fresnel reflection with distinct boundary caustics distinguishing it from fluid voids.',
    stageId: 3,
  },
  {
    id: 'geoid-glass-rim',
    title: 'Flawless Geoid Glass Boundary',
    classification: 'Optical Enclosure',
    x: 68.0,
    y: 38.0,
    description: 'Subtly asymmetric egg-shaped glass vessel rim illuminated by distant cosmic light.',
    detail: 'Index of refraction (n ≈ 1.52) yielding gentle internal caustics without geometric aberration.',
    stageId: 1,
  },
];
