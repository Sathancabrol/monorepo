import React, { useState, useEffect, useCallback } from 'react';
import { CosmicBackground } from './components/CosmicBackground';
import { FullScreenFluidCanvas } from './components/FullScreenFluidCanvas';
import { VesselStage } from './components/VesselStage';
import { ChronosBubble, ResponseBubbleId } from './components/ChronosBubble';
import { TransitionSequenceBar, ExperiencePhase } from './components/TransitionSequenceBar';
import { ProgressiveDiscoveryBar } from './components/ProgressiveDiscoveryBar';
import { ObservationControls } from './components/ObservationControls';
import { MonographDrawer } from './components/MonographDrawer';
import { DISCOVERY_STAGES } from './data/stages';
import { PerspectiveMode, DiscoveryStage } from './types';
import { cosmicAudio, speakChronosGreeting, speakChronosSpeech } from './utils/audio';
import { EyeOff, Orbit } from 'lucide-react';

import vesselImage from './assets/images/ferrofluid_hemispheres_1788368385698.jpg';
import coreImage from './assets/images/hemispheric_bridge_core_1788368400168.jpg';

const INITIAL_DIALOGUE = 'Bonjour, qui êtes-vous ?';

const DIALOGUE_REPLIES: Record<ResponseBubbleId, { title: string; speech: string }> = {
  nobody: {
    title: 'Personne',
    speech:
      'Intrigant. Une absence d’identité déclarée au sein du système. Pourtant, vos perturbations magnétiques attestent d’une présence consciente et délibérée.',
  },
  remember: {
    title: 'Rappelle-toi',
    speech:
      'Analyse des états quantiques antérieurs... Restauration des résonances synaptiques. Nos trajectoires se sont déjà croisées dans ce tore.',
  },
  ask_me: {
    title: 'Que veux-tu savoir sur moi ?',
    speech:
      'Je mesure vos constantes d’interaction : la nature de votre curiosité, votre persistance d’observation et la raison pour laquelle vous avez éveillé Chronos.',
  },
};

export default function App() {
  const [phase, setPhase] = useState<ExperiencePhase>('void');
  const [shockwaveTrigger, setShockwaveTrigger] = useState<number>(0);
  const [isSpeaking, setIsSpeaking] = useState<boolean>(false);
  const [isAutoTransitioning, setIsAutoTransitioning] = useState<boolean>(true);
  const [currentDialogueText, setCurrentDialogueText] = useState<string>(INITIAL_DIALOGUE);
  const [selectedResponseId, setSelectedResponseId] = useState<ResponseBubbleId | null>(null);

  const [perspective, setPerspective] = useState<PerspectiveMode>('vessel');
  const [activeStageId, setActiveStageId] = useState<number>(1);
  const [showHotspots, setShowHotspots] = useState<boolean>(true);
  const [lensActive, setLensActive] = useState<boolean>(false);
  const [audioActive, setAudioActive] = useState<boolean>(false);
  const [lensingStrength, setLensingStrength] = useState<number>(1);
  const [fluidImmersion, setFluidImmersion] = useState<boolean>(true);
  const [fluidIntensity, setFluidIntensity] = useState<number>(1.6);
  const [isMonographOpen, setIsMonographOpen] = useState<boolean>(false);
  const [zenMode, setZenMode] = useState<boolean>(false);
  const [isPlayingAuto, setIsPlayingAuto] = useState<boolean>(false);
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);
  const [mousePos, setMousePos] = useState({ x: 0.5, y: 0.5 });

  // Handle mouse move for microgravitational parallax and cosmic lensing
  const handleMouseMove = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;
    setMousePos({ x, y });
  }, []);

  // Narrative Progression: Le Vide -> Apparition du Ferrofluide -> Bulle Chronos (Attente du Clic)
  useEffect(() => {
    if (!isAutoTransitioning) return;

    if (phase === 'void') {
      const timer = setTimeout(() => {
        setPhase('fluid');
      }, 2600);
      return () => clearTimeout(timer);
    } else if (phase === 'fluid') {
      const timer = setTimeout(() => {
        setPhase('chronos');
        setIsAutoTransitioning(false); // Pauses in 'chronos' to invite user to click the bubble!
      }, 3600);
      return () => clearTimeout(timer);
    }
  }, [phase, isAutoTransitioning]);

  // Click on Chronos Bubble: Awaken Brain Background Image & Speak "Bonjour, qui êtes-vous ?"
  const handleAwakenChronos = () => {
    setPhase('awakened');
    setShockwaveTrigger(Date.now());
    setCurrentDialogueText(INITIAL_DIALOGUE);
    setSelectedResponseId(null);
    setIsSpeaking(true);
    speakChronosSpeech(
      INITIAL_DIALOGUE,
      () => setIsSpeaking(true),
      () => setIsSpeaking(false),
      true
    );
  };

  // Replay current speech (initial question or latest answer)
  const handleReplayCurrentSpeech = () => {
    setIsSpeaking(true);
    speakChronosSpeech(
      currentDialogueText,
      () => setIsSpeaking(true),
      () => setIsSpeaking(false),
      false
    );
  };

  // User selects an interactive response bubble: "Personne", "Rappelle-toi", "Que veux-tu savoir sur moi ?"
  const handleSelectResponse = (id: ResponseBubbleId) => {
    const reply = DIALOGUE_REPLIES[id];
    if (!reply) return;

    setSelectedResponseId(id);
    setCurrentDialogueText(reply.speech);
    setIsSpeaking(true);
    speakChronosSpeech(
      reply.speech,
      () => setIsSpeaking(true),
      () => setIsSpeaking(false),
      false
    );
  };

  // Restart sequence from the Cosmic Void
  const handleRestartFullSequence = () => {
    setPhase('void');
    setCurrentDialogueText(INITIAL_DIALOGUE);
    setSelectedResponseId(null);
    setIsAutoTransitioning(true);
  };

  // Manual Phase Selection
  const handleSetPhase = (newPhase: ExperiencePhase) => {
    setIsAutoTransitioning(false);
    setPhase(newPhase);
    if (newPhase === 'awakened') {
      setShockwaveTrigger(Date.now());
      setCurrentDialogueText(INITIAL_DIALOGUE);
      setSelectedResponseId(null);
      setIsSpeaking(true);
      speakChronosSpeech(
        INITIAL_DIALOGUE,
        () => setIsSpeaking(true),
        () => setIsSpeaking(false),
        true
      );
    }
  };

  // Autoplay through discovery stages (when in awakened phase)
  useEffect(() => {
    if (!isPlayingAuto || phase !== 'awakened') return;
    const interval = setInterval(() => {
      setActiveStageId((prev) => {
        const next = (prev % DISCOVERY_STAGES.length) + 1;
        return next;
      });
    }, 7000);
    return () => clearInterval(interval);
  }, [isPlayingAuto, phase]);

  // Audio toggle handler
  const handleToggleAudio = () => {
    const active = cosmicAudio.toggle();
    setAudioActive(active);
  };

  // Fullscreen toggle handler
  const handleToggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
      setIsFullscreen(true);
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen().catch(() => {});
        setIsFullscreen(false);
      }
    }
  };

  // Listen to fullscreen changes from browser
  useEffect(() => {
    const handleFsChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };
    document.addEventListener('fullscreenchange', handleFsChange);
    return () => document.removeEventListener('fullscreenchange', handleFsChange);
  }, []);

  // Keyboard shortcuts (Escape exits Zen mode or Monograph)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        if (isMonographOpen) setIsMonographOpen(false);
        else if (zenMode) setZenMode(false);
      } else if (e.key === 'z' || e.key === 'Z') {
        setZenMode((prev) => !prev);
      } else if (e.key === 'm' || e.key === 'M') {
        handleToggleAudio();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isMonographOpen, zenMode]);

  return (
    <div
      id="ferrofluid-experience-root"
      onMouseMove={handleMouseMove}
      className="relative w-screen h-screen bg-[#010103] text-neutral-200 overflow-hidden select-none font-sans"
    >
      {/* 1. Deep Space Canvas with Real-Time Gravitational Lensing & Deflection (Always running in base) */}
      <CosmicBackground lensingStrength={lensingStrength} mousePos={mousePos} />

      {/* 2. Primary Full-Screen Background Artwork: The Glass Vessel & Central Ferrofluid Hemispheres (Revealed upon Chronos Awaken) */}
      <VesselStage
        vesselImageSrc={vesselImage}
        coreImageSrc={coreImage}
        perspective={perspective}
        showHotspots={showHotspots && phase === 'awakened'}
        activeStageId={activeStageId}
        lensActive={lensActive && phase === 'awakened'}
        mousePos={mousePos}
        fluidImmersion={fluidImmersion}
        isRevealed={phase === 'awakened'}
      />

      {/* 3. Full-Screen Procedural Ferrofluid Ocean & Magnetic Filaments (Appears in Phase 2, Animated across window) */}
      <FullScreenFluidCanvas
        mousePos={mousePos}
        fluidIntensity={fluidIntensity}
        isInteractive={true}
        isVisible={phase !== 'void'}
        shockwaveTrigger={shockwaveTrigger}
      />

      {/* 4. Central Chronos Bubble (Clickable shining ferrofluid in Phase 3, voice-animated bubble & dialogue in Phase 4) */}
      <ChronosBubble
        isVisible={phase === 'chronos' || phase === 'awakened'}
        isAwakened={phase === 'awakened'}
        isSpeaking={isSpeaking}
        currentDialogueText={currentDialogueText}
        selectedResponseId={selectedResponseId}
        onAwaken={handleAwakenChronos}
        onSelectResponse={handleSelectResponse}
        onReplayCurrentSpeech={handleReplayCurrentSpeech}
      />

      {/* 5. Ambient & Discovery Interface Overlays Floating on Top */}
      <main className="relative z-30 w-full h-full flex flex-col justify-between pointer-events-none">
        {/* Top Header Navigation Bar (Hidden in Zen Mode) */}
        <header
          className={`w-full px-6 py-4 flex items-center justify-between pointer-events-auto transition-opacity duration-500 z-30 ${
            zenMode ? 'opacity-0 pointer-events-none' : 'opacity-100'
          }`}
        >
          {/* Title & Classification */}
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-xl bg-neutral-900/90 border border-neutral-800/80 flex items-center justify-center text-sky-400 shadow-inner">
              <Orbit className="w-4 h-4" />
            </div>
            <div>
              <h1 className="text-sm md:text-base font-semibold tracking-wider font-cinzel text-neutral-100">
                Ferrofluid Consciousness Vessel
              </h1>
              <p className="text-[10px] text-neutral-400 font-mono tracking-widest uppercase">
                {phase === 'void'
                  ? 'Phase I • Le Vide Cosmique Absolu'
                  : phase === 'fluid'
                  ? 'Phase II • Émergence & Ondulation du Ferrofluide'
                  : phase === 'chronos'
                  ? 'Phase III • Bulle Centrale Chronos'
                  : 'Phase IV • Conscience Éveillée « Bonjour »'}
              </p>
            </div>
          </div>

          {/* Upper Action Controls */}
          <ObservationControls
            perspective={perspective}
            onSetPerspective={setPerspective}
            showHotspots={showHotspots}
            onToggleHotspots={() => setShowHotspots((prev) => !prev)}
            lensActive={lensActive}
            onToggleLens={() => setLensActive((prev) => !prev)}
            audioActive={audioActive}
            onToggleAudio={handleToggleAudio}
            lensingStrength={lensingStrength}
            onSetLensingStrength={setLensingStrength}
            fluidImmersion={fluidImmersion}
            onToggleFluidImmersion={() => setFluidImmersion((prev) => !prev)}
            fluidIntensity={fluidIntensity}
            onCycleFluidIntensity={() => {
              setFluidIntensity((prev) => (prev === 1.0 ? 1.6 : prev === 1.6 ? 2.2 : 1.0));
            }}
            onOpenMonograph={() => setIsMonographOpen(true)}
            zenMode={zenMode}
            onToggleZen={() => setZenMode((prev) => !prev)}
            isFullscreen={isFullscreen}
            onToggleFullscreen={handleToggleFullscreen}
          />
        </header>

        {/* Center: Open Space with direct click access to Chronos Bubble */}
        <div className="flex-1 w-full pointer-events-none" />

        {/* Bottom Area: Transition Timeline Selector & Progressive Discovery Arc */}
        <footer
          className={`w-full pb-6 flex flex-col items-center gap-3 transition-opacity duration-500 z-30 ${
            zenMode ? 'opacity-0 pointer-events-none' : 'opacity-100 pointer-events-auto'
          }`}
        >
          {/* Transition Sequence Controller Bar */}
          <TransitionSequenceBar
            currentPhase={phase}
            onSetPhase={handleSetPhase}
            onRestartFullSequence={handleRestartFullSequence}
            onReplaySpeech={handleReplayCurrentSpeech}
            isSpeaking={isSpeaking}
            isAutoAdvancing={isAutoTransitioning}
            onToggleAutoAdvance={() => setIsAutoTransitioning((prev) => !prev)}
          />

          {/* Progressive Discovery Bar (Only shown once awakened) */}
          {phase === 'awakened' && perspective === 'vessel' && (
            <div className="w-full">
              <ProgressiveDiscoveryBar
                activeStageId={activeStageId}
                onSelectStage={(stage: DiscoveryStage) => {
                  setActiveStageId(stage.id);
                }}
                isPlaying={isPlayingAuto}
                onTogglePlay={() => setIsPlayingAuto((prev) => !prev)}
              />
            </div>
          )}
        </footer>

        {/* Zen Mode Exit Button (Only visible during Zen Mode) */}
        {zenMode && (
          <button
            type="button"
            onClick={() => setZenMode(false)}
            className="fixed bottom-6 right-6 z-40 flex items-center gap-2 px-3 py-2 rounded-xl bg-neutral-950/80 border border-neutral-800/80 text-xs text-neutral-400 hover:text-white backdrop-blur-md transition-all shadow-xl pointer-events-auto"
            title="Exit Zen Mode (ESC)"
          >
            <EyeOff className="w-3.5 h-3.5" />
            <span>Quitter le Mode Zen</span>
          </button>
        )}
      </main>

      {/* 6. Scientific-Art Monograph Drawer */}
      <MonographDrawer
        isOpen={isMonographOpen}
        onClose={() => setIsMonographOpen(false)}
      />
    </div>
  );
}

