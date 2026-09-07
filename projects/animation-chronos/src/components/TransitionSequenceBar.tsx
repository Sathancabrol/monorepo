import React from 'react';
import { Play, RotateCcw, Volume2, Sparkles, CircleDot, Orbit, Brain } from 'lucide-react';

export type ExperiencePhase = 'void' | 'fluid' | 'chronos' | 'awakened';

interface TransitionSequenceBarProps {
  currentPhase: ExperiencePhase;
  onSetPhase: (phase: ExperiencePhase) => void;
  onRestartFullSequence: () => void;
  onReplaySpeech: () => void;
  isSpeaking: boolean;
  isAutoAdvancing: boolean;
  onToggleAutoAdvance: () => void;
}

export const TransitionSequenceBar: React.FC<TransitionSequenceBarProps> = ({
  currentPhase,
  onSetPhase,
  onRestartFullSequence,
  onReplaySpeech,
  isSpeaking,
  isAutoAdvancing,
  onToggleAutoAdvance,
}) => {
  const steps: { id: ExperiencePhase; label: string; icon: React.ReactNode; desc: string }[] = [
    {
      id: 'void',
      label: '1. Le Vide',
      icon: <CircleDot className="w-3.5 h-3.5" />,
      desc: 'Espace pur & trou noir',
    },
    {
      id: 'fluid',
      label: '2. Ferrofluide',
      icon: <Orbit className="w-3.5 h-3.5" />,
      desc: 'Apparition & filaments',
    },
    {
      id: 'chronos',
      label: '3. Bulle Chronos',
      icon: <Sparkles className="w-3.5 h-3.5" />,
      desc: 'Noyau temporel central',
    },
    {
      id: 'awakened',
      label: '4. Parole AI & Dialogue',
      icon: <Brain className="w-3.5 h-3.5" />,
      desc: 'Bulle ferrofluide vocale & réponses',
    },
  ];

  return (
    <div className="flex flex-col items-center gap-2 pointer-events-auto">
      {/* Step Pills Navigation */}
      <div className="flex items-center gap-1.5 p-1.5 rounded-2xl bg-neutral-950/80 border border-neutral-800/80 backdrop-blur-xl shadow-2xl">
        {steps.map((step) => {
          const isActive = currentPhase === step.id;
          return (
            <button
              key={step.id}
              type="button"
              onClick={() => onSetPhase(step.id)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-mono transition-all cursor-pointer select-none ${
                isActive
                  ? 'bg-sky-500/20 text-sky-200 border border-sky-400/40 shadow-[0_0_15px_rgba(56,189,248,0.2)]'
                  : 'text-neutral-400 hover:text-neutral-200 hover:bg-neutral-900/60 border border-transparent'
              }`}
            >
              <span className={isActive ? 'text-sky-400' : 'text-neutral-500'}>
                {step.icon}
              </span>
              <span className="font-medium">{step.label}</span>
            </button>
          );
        })}

        <div className="w-[1px] h-5 bg-neutral-800 mx-1" />

        {/* Replay Full Sequence */}
        <button
          type="button"
          onClick={onRestartFullSequence}
          title="Rejouer la transition depuis le Vide"
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-neutral-900/80 hover:bg-neutral-800 text-xs font-mono text-neutral-300 hover:text-white border border-neutral-800 transition-all cursor-pointer"
        >
          <RotateCcw className="w-3 h-3 text-sky-400" />
          <span>Rejouer</span>
        </button>

        {/* Speak Bonjour button */}
        {currentPhase === 'awakened' && (
          <button
            type="button"
            onClick={onReplaySpeech}
            title="Faire reparler Chronos"
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-mono border transition-all cursor-pointer ${
              isSpeaking
                ? 'bg-sky-500/30 text-white border-sky-400 shadow-[0_0_15px_rgba(56,189,248,0.4)]'
                : 'bg-neutral-900/80 hover:bg-neutral-800 text-sky-300 border-sky-500/30'
            }`}
          >
            <Volume2 className={`w-3 h-3 ${isSpeaking ? 'animate-bounce text-sky-300' : ''}`} />
            <span>« Bonjour »</span>
          </button>
        )}
      </div>
    </div>
  );
};
