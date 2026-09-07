import React from 'react';
import { PerspectiveMode } from '../types';
import {
  Maximize2,
  Minimize2,
  Search,
  Volume2,
  VolumeX,
  Compass,
  BookOpen,
  Eye,
  Sliders,
  Layers,
  Sparkles,
  Waves,
  Droplets,
} from 'lucide-react';

interface ObservationControlsProps {
  perspective: PerspectiveMode;
  onSetPerspective: (p: PerspectiveMode) => void;
  showHotspots: boolean;
  onToggleHotspots: () => void;
  lensActive: boolean;
  onToggleLens: () => void;
  audioActive: boolean;
  onToggleAudio: () => void;
  lensingStrength: number;
  onSetLensingStrength: (val: number) => void;
  fluidImmersion: boolean;
  onToggleFluidImmersion: () => void;
  fluidIntensity: number;
  onCycleFluidIntensity: () => void;
  onOpenMonograph: () => void;
  zenMode: boolean;
  onToggleZen: () => void;
  isFullscreen: boolean;
  onToggleFullscreen: () => void;
}

export const ObservationControls: React.FC<ObservationControlsProps> = ({
  perspective,
  onSetPerspective,
  showHotspots,
  onToggleHotspots,
  lensActive,
  onToggleLens,
  audioActive,
  onToggleAudio,
  lensingStrength,
  onSetLensingStrength,
  fluidImmersion,
  onToggleFluidImmersion,
  fluidIntensity,
  onCycleFluidIntensity,
  onOpenMonograph,
  zenMode,
  onToggleZen,
  isFullscreen,
  onToggleFullscreen,
}) => {
  return (
    <div
      id="observation-controls-panel"
      className="flex items-center gap-2 pointer-events-auto bg-neutral-950/80 backdrop-blur-xl border border-neutral-800/80 rounded-2xl p-2 shadow-2xl"
    >
      {/* Perspective Mode Switcher */}
      <div className="flex items-center rounded-xl bg-neutral-900/90 p-1 border border-neutral-800/80">
        <button
          type="button"
          onClick={() => onSetPerspective('vessel')}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
            perspective === 'vessel'
              ? 'bg-neutral-800 text-neutral-100 shadow-sm'
              : 'text-neutral-400 hover:text-neutral-200'
          }`}
          title="Full Vessel Geoid Perspective"
        >
          <Compass className="w-3.5 h-3.5" />
          <span>Vaisseau</span>
        </button>
        <button
          type="button"
          onClick={() => onSetPerspective('core')}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
            perspective === 'core'
              ? 'bg-neutral-800 text-neutral-100 shadow-sm text-sky-300'
              : 'text-neutral-400 hover:text-neutral-200'
          }`}
          title="Macro Consciousness Core Perspective"
        >
          <Sparkles className="w-3.5 h-3.5 text-sky-400" />
          <span>Pont Conscience</span>
        </button>
      </div>

      <div className="w-[1px] h-6 bg-neutral-800 mx-1" />

      {/* Full Screen Fluid Ocean Immersion Toggle */}
      <button
        type="button"
        onClick={onToggleFluidImmersion}
        className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium border transition-colors ${
          fluidImmersion
            ? 'bg-indigo-950/70 border-indigo-700/70 text-indigo-200 shadow-[0_0_12px_rgba(99,102,241,0.25)]'
            : 'bg-neutral-900/60 border-neutral-800/80 text-neutral-400 hover:text-neutral-200 hover:bg-neutral-800/60'
        }`}
        title="Fluide Plein Écran & Fusion Spatiotemporelle"
      >
        <Waves className="w-3.5 h-3.5 text-indigo-400" />
        <span className="hidden sm:inline">Fluide Partout</span>
      </button>

      {/* Fluid Field Density Cycle */}
      <button
        type="button"
        onClick={onCycleFluidIntensity}
        className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl text-xs font-medium bg-neutral-900/60 border border-neutral-800/80 text-neutral-300 hover:text-neutral-100 transition-colors"
        title="Densité et Tension du Réseau Fluide"
      >
        <Droplets className="w-3.5 h-3.5 text-violet-400" />
        <span className="hidden md:inline">
          Densité: {fluidIntensity === 1 ? 'Normale' : fluidIntensity === 1.6 ? 'Élevée' : 'Océan'}
        </span>
      </button>

      {/* Optical Magnifier Loupe Toggle */}
      <button
        type="button"
        onClick={onToggleLens}
        className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium border transition-colors ${
          lensActive
            ? 'bg-sky-950/60 border-sky-700/60 text-sky-300'
            : 'bg-neutral-900/60 border-neutral-800/80 text-neutral-400 hover:text-neutral-200 hover:bg-neutral-800/60'
        }`}
        title="Interactive 2.5x Optical Magnifying Loupe"
      >
        <Search className="w-3.5 h-3.5" />
        <span className="hidden sm:inline">Loupe</span>
      </button>

      {/* Hotspots Toggle */}
      {perspective === 'vessel' && (
        <button
          type="button"
          onClick={onToggleHotspots}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium border transition-colors ${
            showHotspots
              ? 'bg-neutral-800 border-neutral-700 text-neutral-100'
              : 'bg-neutral-900/60 border-neutral-800/80 text-neutral-400 hover:text-neutral-200'
          }`}
          title="Toggle Physical Hotspots"
        >
          <Layers className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Repères</span>
        </button>
      )}

      {/* Gravitational Lensing Toggle */}
      <button
        type="button"
        onClick={() => {
          const next = lensingStrength === 1 ? 2 : lensingStrength === 2 ? 0 : 1;
          onSetLensingStrength(next);
        }}
        className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium border transition-colors ${
          lensingStrength > 0
            ? 'bg-neutral-800/80 border-neutral-700 text-neutral-200'
            : 'bg-neutral-900/60 border-neutral-800/80 text-neutral-500'
        }`}
        title="Toggle Event Horizon Gravitational Lensing Strength"
      >
        <Sliders className="w-3.5 h-3.5" />
        <span className="hidden md:inline">
          Lentille: {lensingStrength === 0 ? 'Off' : lensingStrength === 1 ? '1x' : '2x'}
        </span>
      </button>

      {/* Cosmic Audio Resonator */}
      <button
        type="button"
        onClick={onToggleAudio}
        className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium border transition-colors ${
          audioActive
            ? 'bg-indigo-950/60 border-indigo-700/60 text-indigo-300'
            : 'bg-neutral-900/60 border-neutral-800/80 text-neutral-400 hover:text-neutral-200'
        }`}
        title="Cosmic Event Horizon Synthesizer (Web Audio)"
      >
        {audioActive ? <Volume2 className="w-3.5 h-3.5" /> : <VolumeX className="w-3.5 h-3.5" />}
        <span className="hidden lg:inline">{audioActive ? 'Audio Actif' : 'Ambiance'}</span>
      </button>

      <div className="w-[1px] h-6 bg-neutral-800 mx-1" />

      {/* Scientific Monograph */}
      <button
        type="button"
        onClick={onOpenMonograph}
        className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium bg-neutral-900/80 hover:bg-neutral-800 border border-neutral-800 text-neutral-300 hover:text-neutral-100 transition-colors"
        title="Scientific & Artistic Monograph"
      >
        <BookOpen className="w-3.5 h-3.5 text-neutral-400" />
        <span className="hidden sm:inline">Monographie</span>
      </button>

      {/* Zen / Pure Artwork View */}
      <button
        type="button"
        onClick={onToggleZen}
        className="p-2 rounded-xl bg-neutral-900/80 hover:bg-neutral-800 border border-neutral-800 text-neutral-300 hover:text-neutral-100 transition-colors"
        title={zenMode ? 'Quitter le Mode Zen (ESC ou Clic)' : 'Mode Zen: Vue Fluide Intégrale'}
      >
        <Eye className="w-3.5 h-3.5" />
      </button>

      {/* Fullscreen Toggle */}
      <button
        type="button"
        onClick={onToggleFullscreen}
        className="p-2 rounded-xl bg-neutral-900/80 hover:bg-neutral-800 border border-neutral-800 text-neutral-300 hover:text-neutral-100 transition-colors"
        title={isFullscreen ? 'Quitter Plein Écran' : 'Plein Écran Navigateur'}
      >
        {isFullscreen ? <Minimize2 className="w-3.5 h-3.5" /> : <Maximize2 className="w-3.5 h-3.5" />}
      </button>
    </div>
  );
};
