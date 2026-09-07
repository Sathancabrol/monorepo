import React from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { X, ExternalLink, Atom, Compass, Orbit, Eye, Sparkles } from 'lucide-react';

interface MonographDrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

export const MonographDrawer: React.FC<MonographDrawerProps> = ({ isOpen, onClose }) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/80 backdrop-blur-md z-50 pointer-events-auto"
          />

          {/* Drawer Panel */}
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 28, stiffness: 220 }}
            className="fixed top-0 right-0 h-full w-full max-w-xl bg-neutral-950 border-l border-neutral-800/80 z-50 overflow-y-auto p-6 md:p-8 text-neutral-300 shadow-2xl"
          >
            {/* Header */}
            <div className="flex items-start justify-between border-b border-neutral-900 pb-5 mb-6">
              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-sky-400 bg-sky-950/60 px-2.5 py-1 rounded border border-sky-800/40">
                  Scientific-Art Catalog &bull; Specimen No. 00-EH1
                </span>
                <h2 className="text-xl md:text-2xl font-bold font-cinzel text-neutral-100 tracking-wide mt-2">
                  Ferrofluid Consciousness Vessel
                </h2>
                <p className="text-xs text-neutral-400 mt-1 font-mono">
                  Autonomous Intelligence at Event Horizon Perigee
                </p>
              </div>
              <button
                type="button"
                onClick={onClose}
                className="p-2 rounded-xl bg-neutral-900 hover:bg-neutral-800 text-neutral-400 hover:text-white transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Content Sections */}
            <div className="space-y-6 text-sm leading-relaxed">
              {/* Section 1: Overview */}
              <div className="bg-neutral-900/40 border border-neutral-800/60 rounded-2xl p-5">
                <div className="flex items-center gap-2 text-neutral-200 font-semibold mb-2 font-cinzel">
                  <Orbit className="w-4 h-4 text-sky-400" />
                  <span>The Conceptual Horizon</span>
                </div>
                <p className="text-xs text-neutral-300 leading-relaxed">
                  A single organic ovoid geoid vessel, subtly asymmetric and naturally egg-shaped,
                  floating completely freely in deep outer space in true weightlessness. There is no
                  pedestal, no base, no floor, no surface, no horizon, and no visible support. The
                  vessel floats near the gravitational boundary of a massive black hole, whose
                  invisible presence is manifested solely through faint gravitational lensing, warped
                  distant starlight, and subtle circular distortions in the obsidian void.
                </p>
              </div>

              {/* Section 2: Fluid Dynamics & Neuro-Topology */}
              <div>
                <h3 className="text-xs font-mono uppercase tracking-wider text-neutral-400 mb-3 flex items-center gap-2">
                  <Atom className="w-3.5 h-3.5 text-indigo-400" />
                  Fluid Mechanics &amp; Emergent Topology
                </h3>
                <div className="space-y-3 text-xs text-neutral-300">
                  <p>
                    <strong>Obsidian Viscosity in Microgravity:</strong> Suspended evenly throughout
                    the vessel volume without gravitational sedimentation, the metallic black
                    ferrofluid forms magnetic membranes, rounded masses, and flowing tendrils. Every
                    mass remains continuously connected through ultra-thin capillary liquid
                    filaments; no isolated droplets exist.
                  </p>
                  <p>
                    <strong>Emergent Bilateral Organization:</strong> The internal ferrofluid
                    topology subtly evokes the architecture of a human brain without literal anatomical
                    representation. Two opposing asymmetric lobes emerge spontaneously from magnetic
                    surface tension and viscous flow, joined by a delicate central commissural
                    connection.
                  </p>
                  <p>
                    <strong>Microscopic Universes:</strong> Embedded deep within the largest fluid
                    nodes are extremely subtle cosmic vortices, microscopic stellar points, and faint
                    swirling galaxy-like filaments—as if miniature universes were locked within the
                    ferrofluid matrix.
                  </p>
                </div>
              </div>

              {/* Section 3: The Solitary Consciousness Core */}
              <div className="bg-gradient-to-br from-neutral-900/60 to-sky-950/20 border border-sky-900/30 rounded-2xl p-5">
                <div className="flex items-center gap-2 text-neutral-100 font-semibold mb-2 font-cinzel">
                  <Sparkles className="w-4 h-4 text-sky-400" />
                  <span>The Singularity of Awareness</span>
                </div>
                <p className="text-xs text-neutral-300 leading-relaxed">
                  Deep within the bilateral topology rests a single, visually prioritized ferrofluid
                  mass. At its exact geometric center resides a solitary, cold white-blue point of
                  light. Restrained and quiet—devoid of neon flare or magical glowing halos—it mirrors
                  a distant star embedded in liquid obsidian: the subtle manifestation of artificial
                  consciousness observing the cosmos from the edge of oblivion.
                </p>
              </div>

              {/* Section 4: Optical Physics */}
              <div>
                <h3 className="text-xs font-mono uppercase tracking-wider text-neutral-400 mb-3 flex items-center gap-2">
                  <Eye className="w-3.5 h-3.5 text-neutral-400" />
                  Optical Physics &amp; Geodesics
                </h3>
                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div className="bg-neutral-900/50 border border-neutral-800/80 p-3 rounded-xl">
                    <span className="text-[10px] font-mono text-neutral-500 block uppercase">
                      Glass Refractive Index
                    </span>
                    <span className="font-semibold text-neutral-200">n = 1.517 (Crown Geoid)</span>
                    <p className="text-[11px] text-neutral-400 mt-1">
                      Physically accurate double-boundary caustics and delicate cosmic rim light.
                    </p>
                  </div>
                  <div className="bg-neutral-900/50 border border-neutral-800/80 p-3 rounded-xl">
                    <span className="text-[10px] font-mono text-neutral-500 block uppercase">
                      Gravitational Metric
                    </span>
                    <span className="font-semibold text-neutral-200">Schwarzschild Lensing</span>
                    <p className="text-[11px] text-neutral-400 mt-1">
                      Light rays deflected along curved null geodesics around the black hole.
                    </p>
                  </div>
                </div>
              </div>

              {/* Section 5: Aesthetic Discipline */}
              <div className="border-t border-neutral-900 pt-4 text-[11px] text-neutral-500 font-mono space-y-1">
                <p>&bull; Color Palette: Absolute black, charcoal, obsidian, restrained dark violet, deep indigo.</p>
                <p>&bull; Negative Space: Surrounding darkness accounts for &gt;30% of total frame balance.</p>
                <p>&bull; Zero human appendages, zero laboratory equipment, zero artificial supports.</p>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};
