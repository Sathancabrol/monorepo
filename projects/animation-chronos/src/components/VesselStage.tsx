import React, { useRef, useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { PerspectiveMode, Hotspot } from '../types';
import { VESSEL_HOTSPOTS } from '../data/stages';
import { InspectionLens } from './InspectionLens';
import { Sparkles, Eye, Info, X } from 'lucide-react';

interface VesselStageProps {
  vesselImageSrc: string;
  coreImageSrc: string;
  perspective: PerspectiveMode;
  showHotspots: boolean;
  activeStageId: number;
  lensActive: boolean;
  mousePos: { x: number; y: number };
  fluidImmersion?: boolean;
  isRevealed?: boolean;
}

export const VesselStage: React.FC<VesselStageProps> = ({
  vesselImageSrc,
  coreImageSrc,
  perspective,
  showHotspots,
  activeStageId,
  lensActive,
  mousePos,
  fluidImmersion = true,
  isRevealed = true,
}) => {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [selectedHotspot, setSelectedHotspot] = useState<Hotspot | null>(null);

  // Filter hotspots for vessel perspective or stage relevance
  const activeHotspots = VESSEL_HOTSPOTS.filter(
    (h) => perspective === 'vessel' && (showHotspots || h.stageId === activeStageId)
  );

  // Parallax tilt calculation (-10px to +10px subtle shift)
  const tiltX = (mousePos.x - 0.5) * 16;
  const tiltY = (mousePos.y - 0.5) * 16;
  const rotateX = (mousePos.y - 0.5) * -4;
  const rotateY = (mousePos.x - 0.5) * 5;

  const currentImage = perspective === 'vessel' ? vesselImageSrc : coreImageSrc;

  return (
    <div
      id="vessel-stage-wrapper"
      className="fixed inset-0 w-full h-full flex items-center justify-center select-none overflow-hidden z-[1] pointer-events-auto"
    >
      {/* Microgravitational float animation container */}
      <motion.div
        animate={{
          y: [-7, 7, -7],
          rotate: [-0.2, 0.2, -0.2],
        }}
        transition={{
          duration: 16,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
        style={{
          transform: `perspective(1400px) translate3d(${tiltX}px, ${tiltY}px, 0px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`,
          transition: 'transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1)',
        }}
        className="relative w-full h-full flex items-center justify-center"
      >
        {/* The Entire Page as the Transparent Ovoid Glass Vessel Container */}
        <div
          ref={containerRef}
          id="vessel-artwork-container"
          className="relative w-full h-full overflow-hidden cursor-crosshair group"
        >
          {/* Main 3D Photorealistic Render as the Primary Full-Screen Background Image */}
          <AnimatePresence mode="wait">
            <motion.div
              key={`${perspective}-${isRevealed}`}
              initial={{ opacity: 0, scale: isRevealed ? 1.05 : 0.98 }}
              animate={{
                opacity: isRevealed ? 1 : 0,
                scale: 1,
              }}
              exit={{ opacity: 0, scale: 1.02 }}
              transition={{ duration: isRevealed ? 1.4 : 0.6, ease: [0.16, 1, 0.3, 1] }}
              className="absolute inset-0 w-full h-full"
            >
              <img
                src={currentImage}
                alt="Ferrofluid Consciousness Vessel in deep space microgravity"
                referrerPolicy="no-referrer"
                className={`w-full h-full select-none pointer-events-none transition-transform duration-1000 ${
                  perspective === 'vessel'
                    ? 'object-cover object-center scale-[1.05] sm:scale-100 md:scale-[1.03]'
                    : 'object-cover object-center scale-[1.12]'
                }`}
              />

              {/* Dynamic glass caustics & surface refraction reacting to mouse */}
              <div
                className="absolute inset-0 pointer-events-none mix-blend-screen opacity-35"
                style={{
                  background: `radial-gradient(circle at ${mousePos.x * 100}% ${
                    mousePos.y * 100
                  }%, rgba(190, 225, 255, 0.22) 0%, rgba(95, 75, 160, 0.06) 42%, transparent 70%)`,
                }}
              />
            </motion.div>
          </AnimatePresence>

          {/* Transparent Glass Vessel Perimeter Rim Lighting (The Entire Window is the Vessel Hull) */}
          <div className="absolute inset-0 pointer-events-none border border-white/10 shadow-[inset_0_0_90px_rgba(160,180,240,0.08),inset_0_0_30px_rgba(80,50,130,0.12)]">
            {/* Top & Bottom Curved Hull Rim Highlights */}
            <div className="absolute top-0 inset-x-0 h-[1px] bg-gradient-to-r from-transparent via-sky-300/30 to-transparent" />
            <div className="absolute bottom-0 inset-x-0 h-[1px] bg-gradient-to-r from-transparent via-violet-400/25 to-transparent" />
            
            {/* Ovoid Glass Vessel Corner Curvature Reflections */}
            <div className="absolute top-0 left-0 w-48 h-48 rounded-br-[100%] bg-gradient-to-br from-white/[0.04] to-transparent pointer-events-none" />
            <div className="absolute top-0 right-0 w-48 h-48 rounded-bl-[100%] bg-gradient-to-bl from-white/[0.04] to-transparent pointer-events-none" />
            <div className="absolute bottom-0 left-0 w-48 h-48 rounded-tr-[100%] bg-gradient-to-tr from-violet-400/[0.03] to-transparent pointer-events-none" />
            <div className="absolute bottom-0 right-0 w-48 h-48 rounded-tl-[100%] bg-gradient-to-tl from-sky-400/[0.03] to-transparent pointer-events-none" />
          </div>

          {/* Interactive Optical Inspection Loupe */}
          <InspectionLens
            imageSrc={currentImage}
            containerRef={containerRef}
            active={lensActive}
            zoomLevel={perspective === 'vessel' ? 2.5 : 3.2}
          />

          {/* Hotspot Interactive Markers (Only on Vessel Perspective) */}
          {perspective === 'vessel' && (
            <div className="absolute inset-0 pointer-events-auto">
              {activeHotspots.map((hotspot) => {
                const isCore = hotspot.id === 'core-light';
                const isSelected = selectedHotspot?.id === hotspot.id;

                return (
                  <div
                    key={hotspot.id}
                    id={`hotspot-${hotspot.id}`}
                    style={{
                      left: `${hotspot.x}%`,
                      top: `${hotspot.y}%`,
                    }}
                    className="absolute -translate-x-1/2 -translate-y-1/2 z-20 group/marker"
                  >
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        setSelectedHotspot(isSelected ? null : hotspot);
                      }}
                      className={`relative flex items-center justify-center p-1 rounded-full transition-all duration-300 focus:outline-none ${
                        isCore
                          ? 'w-7 h-7 bg-sky-400/20 hover:bg-sky-400/30'
                          : 'w-6 h-6 bg-white/10 hover:bg-white/20'
                      }`}
                      title={hotspot.title}
                    >
                      {/* Radiating pulse ring */}
                      <span
                        className={`absolute inset-0 rounded-full animate-ping opacity-60 ${
                          isCore ? 'bg-sky-400/40' : 'bg-neutral-300/20'
                        }`}
                      />
                      {/* Center dot */}
                      <span
                        className={`w-2 h-2 rounded-full transition-transform duration-300 ${
                          isSelected ? 'scale-125' : 'scale-100'
                        } ${
                          isCore
                            ? 'bg-sky-200 shadow-[0_0_8px_#38bdf8]'
                            : 'bg-neutral-300 shadow-[0_0_5px_rgba(255,255,255,0.8)]'
                        }`}
                      />
                    </button>

                    {/* Quick hover label when unselected */}
                    {!isSelected && (
                      <div className="pointer-events-none absolute left-full ml-2.5 top-1/2 -translate-y-1/2 opacity-0 group-hover/marker:opacity-100 transition-opacity duration-200 whitespace-nowrap bg-neutral-950/90 border border-neutral-800/80 px-2.5 py-1 rounded text-[11px] font-medium text-neutral-300 backdrop-blur-md shadow-lg">
                        {hotspot.title}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}

          {/* Selected Hotspot Detail Card Popover */}
          <AnimatePresence>
            {selectedHotspot && (
              <motion.div
                initial={{ opacity: 0, y: 10, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 10, scale: 0.95 }}
                transition={{ duration: 0.2 }}
                className="absolute bottom-4 left-4 right-4 z-30 bg-neutral-950/92 border border-neutral-800/90 rounded-xl p-4 backdrop-blur-xl shadow-2xl text-neutral-200"
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-[10px] uppercase font-mono tracking-widest text-sky-400/90 bg-sky-950/50 px-2 py-0.5 rounded border border-sky-800/40">
                        {selectedHotspot.classification}
                      </span>
                    </div>
                    <h4 className="text-sm font-semibold text-neutral-100 font-cinzel">
                      {selectedHotspot.title}
                    </h4>
                  </div>
                  <button
                    type="button"
                    onClick={() => setSelectedHotspot(null)}
                    className="p-1 rounded-md text-neutral-400 hover:text-neutral-100 hover:bg-neutral-800 transition-colors"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
                <p className="text-xs text-neutral-300 mt-2 leading-relaxed">
                  {selectedHotspot.description}
                </p>
                <p className="text-[11px] text-neutral-400 mt-1 leading-relaxed border-t border-neutral-900 pt-2 font-mono">
                  {selectedHotspot.detail}
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>

      {/* Micro-gravitational indicator coordinate tag */}
      <div className="absolute bottom-5 left-6 pointer-events-none hidden md:flex items-center gap-2 text-[10px] font-mono tracking-widest text-neutral-500 uppercase">
        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500/80 animate-pulse" />
        <span>Gravitational Equipotential: 0.000g | Schwarzschild Radius Margin: +4.82 AU</span>
      </div>
    </div>
  );
};
