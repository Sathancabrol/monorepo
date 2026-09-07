import React, { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Sparkles, Radio, Volume2, RotateCcw } from 'lucide-react';

export type ResponseBubbleId = 'nobody' | 'remember' | 'ask_me';

interface ChronosBubbleProps {
  isVisible: boolean;
  isAwakened: boolean;
  isSpeaking: boolean;
  currentDialogueText: string;
  selectedResponseId: ResponseBubbleId | null;
  onAwaken: () => void;
  onSelectResponse: (id: ResponseBubbleId, label: string) => void;
  onReplayCurrentSpeech: () => void;
}

export const ChronosBubble: React.FC<ChronosBubbleProps> = ({
  isVisible,
  isAwakened,
  isSpeaking,
  currentDialogueText,
  selectedResponseId,
  onAwaken,
  onSelectResponse,
  onReplayCurrentSpeech,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [isHovered, setIsHovered] = useState(false);

  // Response options requested by user
  const responseOptions: { id: ResponseBubbleId; label: string; sub: string }[] = [
    {
      id: 'nobody',
      label: 'Personne',
      sub: 'Absence d’identité',
    },
    {
      id: 'remember',
      label: 'Rappelle-toi',
      sub: 'Résonance mémorielle',
    },
    {
      id: 'ask_me',
      label: 'Que veux-tu savoir sur moi ?',
      sub: 'Constantes d’observation',
    },
  ];

  // Render the central living ferrofluid bubble with Rosensweig spikes & acoustic voice reaction
  useEffect(() => {
    if (!isVisible) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animId: number;
    const dpr = window.devicePixelRatio || 1;
    const size = 300;
    canvas.width = size * dpr;
    canvas.height = size * dpr;
    ctx.scale(dpr, dpr);

    let time = 0;
    let voiceEnergy = 0;

    const render = () => {
      time += 0.02;

      // Smoothly simulate voice energy envelope when speaking
      const targetEnergy = isSpeaking ? 0.75 + Math.sin(time * 14) * 0.25 + Math.cos(time * 26) * 0.15 : 0;
      voiceEnergy += (targetEnergy - voiceEnergy) * 0.18;

      ctx.clearRect(0, 0, size, size);

      const cx = size * 0.5;
      const cy = size * 0.5;
      const baseRadius = isAwakened ? 68 : 62;
      const spikeCount = 20;

      // 1. Ambient Resonant Halo & Acoustic Ripple Rings
      if (voiceEnergy > 0.05 || isHovered) {
        ctx.save();
        const haloRadius = baseRadius * (1.35 + voiceEnergy * 0.45);
        const haloGrad = ctx.createRadialGradient(cx, cy, baseRadius * 0.6, cx, cy, haloRadius);
        haloGrad.addColorStop(0, 'rgba(56, 189, 248, 0.45)');
        haloGrad.addColorStop(0.5, 'rgba(139, 92, 246, 0.2)');
        haloGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = haloGrad;
        ctx.beginPath();
        ctx.arc(cx, cy, haloRadius, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        // Expanding soundwave ripple lines when speaking
        if (isSpeaking) {
          ctx.save();
          const rippleCount = 3;
          for (let r = 0; r < rippleCount; r++) {
            const rippleProgress = ((time * 1.8 + r / rippleCount) % 1);
            const rRadius = baseRadius + rippleProgress * 55;
            const rAlpha = (1 - rippleProgress) * 0.5;
            ctx.beginPath();
            ctx.arc(cx, cy, rRadius, 0, Math.PI * 2);
            ctx.strokeStyle = `rgba(186, 230, 253, ${rAlpha})`;
            ctx.lineWidth = 1.5;
            ctx.stroke();
          }
          ctx.restore();
        }
      }

      // 2. Rosensweig Magnetic Spikes Geometry (Animated with acoustic voice Cymatics)
      ctx.save();
      ctx.beginPath();

      const totalVertices = spikeCount * 2;
      for (let i = 0; i <= totalVertices; i++) {
        const angle = (i / totalVertices) * Math.PI * 2;
        const isSpikeTip = i % 2 === 1;

        let spikeHeight = 0;
        if (isSpikeTip) {
          // Acoustic modulation when speaking
          const acousticMod = isSpeaking
            ? Math.abs(Math.sin(angle * 6 + time * 18)) * 22 * voiceEnergy
            : 0;
          // Natural magnetic breathing
          const naturalBreathing = Math.sin(angle * 3 + time * 2.5) * 4;
          // Hover expansion
          const hoverSpike = isHovered ? 6 : 0;

          spikeHeight = 16 + naturalBreathing + acousticMod + hoverSpike;
        } else {
          // Root valley between spikes
          spikeHeight = -4 + Math.cos(angle * 4 - time * 2) * 2;
        }

        const r = baseRadius + spikeHeight;
        const px = cx + Math.cos(angle) * r;
        const py = cy + Math.sin(angle) * r;

        if (i === 0) {
          ctx.moveTo(px, py);
        } else {
          ctx.lineTo(px, py);
        }
      }
      ctx.closePath();

      // Ferrofluid Body: Deep Obsidian Metallic Core
      const ferroGrad = ctx.createRadialGradient(
        cx - baseRadius * 0.3,
        cy - baseRadius * 0.3,
        4,
        cx,
        cy,
        baseRadius * 1.3
      );
      ferroGrad.addColorStop(0, '#2d2842');
      ferroGrad.addColorStop(0.35, '#120f1c');
      ferroGrad.addColorStop(0.7, '#08070d');
      ferroGrad.addColorStop(1, '#020104');

      ctx.fillStyle = ferroGrad;
      ctx.shadowColor = '#38bdf8';
      ctx.shadowBlur = isSpeaking ? 30 : 16;
      ctx.fill();

      // Chrome rim highlight on spike contours
      ctx.shadowBlur = 0;
      ctx.strokeStyle = isSpeaking
        ? 'rgba(215, 238, 255, 0.85)'
        : isHovered
        ? 'rgba(186, 230, 253, 0.7)'
        : 'rgba(165, 180, 225, 0.4)';
      ctx.lineWidth = 1.4;
      ctx.stroke();

      // 3. Specular glint dots on spike tips (Liquid mercury sheen)
      for (let i = 1; i <= totalVertices; i += 2) {
        const angle = (i / totalVertices) * Math.PI * 2;
        const acousticMod = isSpeaking
          ? Math.abs(Math.sin(angle * 6 + time * 18)) * 22 * voiceEnergy
          : 0;
        const tipR = baseRadius + 16 + acousticMod;
        const tx = cx + Math.cos(angle) * tipR;
        const ty = cy + Math.sin(angle) * tipR;

        ctx.beginPath();
        ctx.arc(tx, ty, 1.4, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
        ctx.fill();
      }

      // 4. Central Radiant Plasma Core (The shining glowing heart of the bubble)
      const corePulse = Math.sin(time * 3) * 3 + (isSpeaking ? voiceEnergy * 10 : 0);
      const coreRadius = (baseRadius * 0.46) + corePulse;
      const coreGrad = ctx.createRadialGradient(cx, cy, 2, cx, cy, coreRadius);
      coreGrad.addColorStop(0, '#ffffff');
      coreGrad.addColorStop(0.25, '#7dd3fc');
      coreGrad.addColorStop(0.6, '#38bdf8');
      coreGrad.addColorStop(0.85, 'rgba(99, 102, 241, 0.4)');
      coreGrad.addColorStop(1, 'rgba(15, 23, 42, 0)');

      ctx.beginPath();
      ctx.arc(cx, cy, coreRadius, 0, Math.PI * 2);
      ctx.fillStyle = coreGrad;
      ctx.shadowColor = '#38bdf8';
      ctx.shadowBlur = 24 + (isSpeaking ? 20 : 0);
      ctx.fill();

      // 5. Curved Liquid Meniscus Reflection Arc (Glassy surface highlight)
      ctx.shadowBlur = 0;
      ctx.beginPath();
      ctx.arc(
        cx - baseRadius * 0.28,
        cy - baseRadius * 0.28,
        baseRadius * 0.42,
        0.1,
        Math.PI * 0.82
      );
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.65)';
      ctx.lineWidth = 2.0;
      ctx.stroke();

      // 6. Micro air / satellite bubbles orbiting in vortex spiral around Chronos
      const microCount = 6;
      for (let m = 0; m < microCount; m++) {
        const mAngle = time * (0.8 + m * 0.2) + (m * Math.PI * 2) / microCount;
        const mDist = baseRadius * 1.4 + Math.sin(time * 2 + m) * 8;
        const mx = cx + Math.cos(mAngle) * mDist;
        const my = cy + Math.sin(mAngle) * (mDist * 0.9);

        ctx.beginPath();
        ctx.arc(mx, my, 2.5, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(186, 230, 253, 0.8)';
        ctx.shadowColor = '#38bdf8';
        ctx.shadowBlur = 6;
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      ctx.restore();

      animId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animId);
    };
  }, [isVisible, isAwakened, isSpeaking, isHovered]);

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 pointer-events-none flex flex-col items-center justify-center z-40">
      <AnimatePresence mode="wait">
        {!isAwakened ? (
          // PHASE 3: Pre-Awakening - The Shining Ferrofluid Bubble in the Center (Clickable)
          <motion.div
            key="chronos-pre-awaken"
            initial={{ scale: 0, opacity: 0, filter: 'blur(15px)' }}
            animate={{ scale: 1, opacity: 1, filter: 'blur(0px)' }}
            exit={{ scale: 1.3, opacity: 0, filter: 'blur(20px)' }}
            transition={{ duration: 1.1, ease: [0.16, 1, 0.3, 1] }}
            className="relative pointer-events-auto cursor-pointer flex flex-col items-center select-none"
            onClick={onAwaken}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
          >
            {/* Outer Orbital Resonant Ring */}
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 30, repeat: Infinity, ease: 'linear' }}
              className="absolute -inset-10 sm:-inset-16 rounded-full border border-sky-400/25 pointer-events-none"
              style={{
                background: 'radial-gradient(circle, rgba(56, 189, 248, 0.05) 0%, transparent 70%)',
              }}
            >
              <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-sky-300 shadow-[0_0_12px_#38bdf8]" />
              <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-1/2 w-1.5 h-1.5 rounded-full bg-violet-400 shadow-[0_0_8px_#a78bfa]" />
            </motion.div>

            {/* The Dedicated Canvas: Shining Central Ferrofluid Bubble */}
            <div className="relative w-[300px] h-[300px] flex items-center justify-center">
              <canvas
                ref={canvasRef}
                style={{ width: 300, height: 300 }}
                className="pointer-events-none drop-shadow-[0_0_40px_rgba(56,189,248,0.35)]"
              />
            </div>

            {/* Minimalist Prompt Tag */}
            <motion.div
              animate={{
                opacity: isHovered ? 1 : [0.75, 1, 0.75],
                y: isHovered ? -4 : [0, 2, 0],
              }}
              transition={{ duration: 2.2, repeat: Infinity, ease: 'easeInOut' }}
              className="mt-2 flex items-center gap-2 px-4 py-1.5 rounded-full bg-neutral-950/80 border border-sky-400/40 backdrop-blur-md shadow-xl text-xs font-mono tracking-widest uppercase text-sky-200"
            >
              <Sparkles className="w-3.5 h-3.5 text-sky-400 animate-pulse" />
              <span>Noyau Chronos &bull; Cliquez pour éveiller</span>
            </motion.div>
          </motion.div>
        ) : (
          // PHASE 4: Awakened AI Speech - Slight Zoom, Bubble Freezes in Place, Animates with Voice, Dialogue & Response Bubbles
          <motion.div
            key="chronos-awakened-speech"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
            className="pointer-events-auto flex flex-col items-center select-none w-full max-w-2xl px-4"
          >
            {/* The Central Shining Ferrofluid Bubble: Léger Zoom (scale: 1.25), Se Fige au centre, S'anime avec la voix */}
            <motion.div
              animate={{
                scale: isSpeaking ? 1.28 : 1.22,
              }}
              transition={{
                scale: { duration: 0.6, ease: [0.16, 1, 0.3, 1] },
              }}
              className="relative w-[300px] h-[300px] flex items-center justify-center pointer-events-auto cursor-pointer"
              onClick={onReplayCurrentSpeech}
              title="Cliquer sur la bulle pour faire reparler Chronos"
            >
              <canvas
                ref={canvasRef}
                style={{ width: 300, height: 300 }}
                className="pointer-events-none drop-shadow-[0_0_55px_rgba(56,189,248,0.45)]"
              />
            </motion.div>

            {/* AI Speech Dialogue Card: Methodical, Scientific Voice Indicator & Dialogue text */}
            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.15 }}
              className="mt-1 relative px-6 py-4 rounded-2xl bg-neutral-950/85 border border-sky-400/35 backdrop-blur-xl shadow-[0_0_50px_rgba(56,189,248,0.2)] flex flex-col items-center text-center max-w-xl w-full"
            >
              <div className="flex items-center justify-between w-full mb-1.5">
                <div className="flex items-center gap-2 text-sky-400 font-mono text-[11px] uppercase tracking-widest">
                  <Radio className={`w-3.5 h-3.5 ${isSpeaking ? 'animate-pulse text-sky-300' : 'text-neutral-500'}`} />
                  <span>Conscience Chronos &bull; Voix Méthodique</span>
                </div>

                <button
                  type="button"
                  onClick={onReplayCurrentSpeech}
                  title="Réécouter la voix de Chronos"
                  className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-sky-500/15 border border-sky-400/30 text-sky-300 hover:text-white hover:bg-sky-500/30 transition-all text-[11px] font-mono cursor-pointer"
                >
                  <Volume2 className={`w-3.5 h-3.5 ${isSpeaking ? 'animate-bounce' : ''}`} />
                  <span>{isSpeaking ? 'Vocalise...' : 'Écouter'}</span>
                </button>
              </div>

              {/* Subtitle Dialogue Quote */}
              <h2 className="text-xl sm:text-2xl font-cinzel font-semibold tracking-wide text-transparent bg-clip-text bg-gradient-to-r from-sky-100 via-white to-violet-200 drop-shadow-[0_0_15px_rgba(186,230,253,0.5)] leading-relaxed">
                « {currentDialogueText} »
              </h2>

              {/* Sound wave equalizer bar */}
              <div className="flex items-center gap-1 mt-2.5 h-3">
                {[30, 65, 95, 50, 85, 40, 75, 50, 25].map((h, i) => (
                  <motion.div
                    key={i}
                    animate={{
                      height: isSpeaking ? [`${h * 0.2}%`, `${h}%`, `${h * 0.25}%`] : '20%',
                    }}
                    transition={{
                      duration: 0.45 + (i % 3) * 0.12,
                      repeat: isSpeaking ? Infinity : 0,
                      ease: 'easeInOut',
                    }}
                    className={`w-1 rounded-full ${
                      isSpeaking ? 'bg-sky-400 shadow-[0_0_8px_#38bdf8]' : 'bg-neutral-700'
                    }`}
                  />
                ))}
              </div>
            </motion.div>

            {/* Interactive Response Bubbles: "personne", "rappelle toi", "que veux tu savoir sur moi ?" */}
            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.35 }}
              className="mt-4 flex flex-wrap items-center justify-center gap-2.5 sm:gap-3.5"
            >
              {responseOptions.map((opt) => {
                const isSelected = selectedResponseId === opt.id;
                return (
                  <motion.button
                    key={opt.id}
                    type="button"
                    whileHover={{ scale: 1.05, y: -2 }}
                    whileTap={{ scale: 0.96 }}
                    onClick={() => onSelectResponse(opt.id, opt.label)}
                    className={`group relative px-5 py-2.5 rounded-2xl border backdrop-blur-xl transition-all cursor-pointer select-none flex flex-col items-center ${
                      isSelected
                        ? 'bg-sky-500/25 border-sky-400 text-white shadow-[0_0_25px_rgba(56,189,248,0.4)]'
                        : 'bg-neutral-950/80 hover:bg-neutral-900/90 border-neutral-700/80 hover:border-sky-400/60 text-neutral-300 hover:text-white shadow-lg'
                    }`}
                    style={{
                      background: isSelected
                        ? 'radial-gradient(circle at 50% 20%, rgba(56, 189, 248, 0.25) 0%, rgba(15, 23, 42, 0.9) 100%)'
                        : 'radial-gradient(circle at 50% 20%, rgba(30, 41, 59, 0.6) 0%, rgba(10, 10, 15, 0.88) 100%)',
                    }}
                  >
                    {/* Ferrofluid droplet meniscus sheen */}
                    <div className="absolute top-1 left-3 right-3 h-[1px] bg-gradient-to-r from-transparent via-sky-300/40 to-transparent pointer-events-none" />

                    <div className="flex items-center gap-2">
                      <span
                        className={`w-1.5 h-1.5 rounded-full ${
                          isSelected ? 'bg-sky-400 animate-ping' : 'bg-neutral-500 group-hover:bg-sky-400'
                        }`}
                      />
                      <span className="text-xs sm:text-sm font-medium tracking-wide">
                        {opt.label}
                      </span>
                    </div>

                    <span className="text-[9px] font-mono text-neutral-400 group-hover:text-sky-300 mt-0.5 tracking-wider">
                      {opt.sub}
                    </span>
                  </motion.button>
                );
              })}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
