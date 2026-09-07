import React from 'react';
import { DISCOVERY_STAGES } from '../data/stages';
import { DiscoveryStage } from '../types';
import { ChevronRight, ChevronLeft, Play, Pause, Sparkles } from 'lucide-react';

interface ProgressiveDiscoveryBarProps {
  activeStageId: number;
  onSelectStage: (stage: DiscoveryStage) => void;
  isPlaying: boolean;
  onTogglePlay: () => void;
}

export const ProgressiveDiscoveryBar: React.FC<ProgressiveDiscoveryBarProps> = ({
  activeStageId,
  onSelectStage,
  isPlaying,
  onTogglePlay,
}) => {
  const currentStage = DISCOVERY_STAGES.find((s) => s.id === activeStageId) || DISCOVERY_STAGES[0];

  const handleNext = () => {
    const nextIdx = (currentStage.id % DISCOVERY_STAGES.length) + 1;
    const nextStage = DISCOVERY_STAGES.find((s) => s.id === nextIdx) || DISCOVERY_STAGES[0];
    onSelectStage(nextStage);
  };

  const handlePrev = () => {
    const prevIdx = currentStage.id === 1 ? DISCOVERY_STAGES.length : currentStage.id - 1;
    const prevStage = DISCOVERY_STAGES.find((s) => s.id === prevIdx) || DISCOVERY_STAGES[0];
    onSelectStage(prevStage);
  };

  return (
    <div
      id="progressive-discovery-controller"
      className="w-full max-w-3xl mx-auto px-4 pointer-events-auto"
    >
      <div className="bg-neutral-950/80 backdrop-blur-xl border border-neutral-800/80 rounded-2xl p-4 shadow-2xl transition-all duration-300">
        {/* Step Indicator Header */}
        <div className="flex items-center justify-between mb-3 border-b border-neutral-900 pb-3">
          <div className="flex items-center gap-2">
            <span className="text-[10px] uppercase font-mono tracking-widest text-neutral-400 bg-neutral-900/90 px-2 py-0.5 rounded border border-neutral-800">
              Observation Arc {currentStage.phase} of V
            </span>
            <span className="text-xs text-neutral-400 font-medium">
              Progressive Revelation
            </span>
          </div>

          {/* Player controls */}
          <div className="flex items-center gap-1.5">
            <button
              type="button"
              onClick={onTogglePlay}
              className={`flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-medium border transition-colors ${
                isPlaying
                  ? 'bg-sky-950/60 border-sky-700/60 text-sky-300'
                  : 'bg-neutral-900/80 border-neutral-800 text-neutral-400 hover:text-neutral-200'
              }`}
              title={isPlaying ? 'Pause Guided Discovery' : 'Autoplay Progressive Discovery'}
            >
              {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
              <span className="text-[11px]">{isPlaying ? 'Cycle Active' : 'Auto Flow'}</span>
            </button>

            <button
              type="button"
              onClick={handlePrev}
              className="p-1.5 rounded-lg bg-neutral-900/80 hover:bg-neutral-800 border border-neutral-800 text-neutral-300 hover:text-white transition-colors"
              title="Previous Discovery"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              type="button"
              onClick={handleNext}
              className="p-1.5 rounded-lg bg-neutral-900/80 hover:bg-neutral-800 border border-neutral-800 text-neutral-300 hover:text-white transition-colors"
              title="Next Discovery"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* 5-Stage Stepper Buttons */}
        <div className="grid grid-cols-5 gap-2 mb-3">
          {DISCOVERY_STAGES.map((stage) => {
            const isActive = stage.id === activeStageId;
            return (
              <button
                key={stage.id}
                type="button"
                onClick={() => onSelectStage(stage)}
                className={`group flex flex-col items-start p-2 rounded-xl text-left border transition-all duration-300 ${
                  isActive
                    ? 'bg-neutral-900/90 border-neutral-700 shadow-md ring-1 ring-neutral-700/50'
                    : 'bg-neutral-950/40 border-neutral-900 hover:border-neutral-800 hover:bg-neutral-900/40'
                }`}
              >
                <div className="flex items-center justify-between w-full mb-1">
                  <span
                    className={`text-[9px] font-mono uppercase tracking-wider ${
                      isActive ? 'text-sky-400 font-semibold' : 'text-neutral-500'
                    }`}
                  >
                    Phase {stage.phase}
                  </span>
                  {stage.id === 5 && (
                    <span className="w-1.5 h-1.5 rounded-full bg-sky-400 shadow-[0_0_6px_#38bdf8]" />
                  )}
                </div>
                <span
                  className={`text-[11px] leading-tight font-medium line-clamp-1 transition-colors ${
                    isActive ? 'text-neutral-100' : 'text-neutral-400 group-hover:text-neutral-300'
                  }`}
                >
                  {stage.title.replace('The ', '')}
                </span>
              </button>
            );
          })}
        </div>

        {/* Active Stage Narrative Card */}
        <div className="bg-neutral-900/40 border border-neutral-800/50 rounded-xl p-3">
          <div className="flex items-baseline justify-between gap-2 mb-1">
            <h3 className="text-sm font-semibold text-neutral-100 font-cinzel tracking-wide">
              {currentStage.title}
            </h3>
            <span className="text-[11px] text-neutral-400 font-mono tracking-tight">
              {currentStage.subtitle}
            </span>
          </div>
          <p className="text-xs text-neutral-300 leading-relaxed">
            {currentStage.description}
          </p>
        </div>
      </div>
    </div>
  );
};
