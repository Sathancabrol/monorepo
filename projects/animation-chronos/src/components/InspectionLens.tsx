import React, { useState, useEffect } from 'react';

interface InspectionLensProps {
  imageSrc: string;
  containerRef: React.RefObject<HTMLDivElement | null>;
  active: boolean;
  zoomLevel?: number;
}

export const InspectionLens: React.FC<InspectionLensProps> = ({
  imageSrc,
  containerRef,
  active,
  zoomLevel = 2.4,
}) => {
  const [lensPos, setLensPos] = useState<{ x: number; y: number } | null>(null);
  const [bgPos, setBgPos] = useState({ x: 0, y: 0 });
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (!active) {
      setIsVisible(false);
      return;
    }

    const container = containerRef.current;
    if (!container) return;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      if (x < 0 || y < 0 || x > rect.width || y > rect.height) {
        setIsVisible(false);
        return;
      }

      setIsVisible(true);
      setLensPos({ x, y });

      // Calculate background position for zoom
      const bgX = (x / rect.width) * 100;
      const bgY = (y / rect.height) * 100;
      setBgPos({ x: bgX, y: bgY });
    };

    const handleMouseLeave = () => {
      setIsVisible(false);
    };

    container.addEventListener('mousemove', handleMouseMove);
    container.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      container.removeEventListener('mousemove', handleMouseMove);
      container.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, [active, containerRef]);

  if (!active || !isVisible || !lensPos) return null;

  const lensSize = 180;

  return (
    <div
      id="optical-inspection-lens"
      className="pointer-events-none absolute z-40 rounded-full border border-neutral-400/40 shadow-2xl overflow-hidden backdrop-blur-[1px]"
      style={{
        width: `${lensSize}px`,
        height: `${lensSize}px`,
        left: `${lensPos.x - lensSize / 2}px`,
        top: `${lensPos.y - lensSize / 2}px`,
        backgroundImage: `url(${imageSrc})`,
        backgroundSize: `${zoomLevel * 100}%`,
        backgroundPosition: `${bgPos.x}% ${bgPos.y}%`,
        boxShadow: '0 0 35px rgba(0,0,0,0.8), inset 0 0 25px rgba(255,255,255,0.08), 0 0 0 1px rgba(120,130,220,0.2)',
      }}
    >
      {/* Optical lens crosshair & chromatic refraction ring */}
      <div className="absolute inset-0 rounded-full border border-white/10 pointer-events-none" />
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        <div className="w-8 h-[1px] bg-sky-200/30" />
        <div className="h-8 w-[1px] bg-sky-200/30 absolute" />
        <div className="w-3 h-3 rounded-full border border-sky-300/40 absolute" />
      </div>
      <div className="absolute bottom-2 left-1/2 -translate-x-1/2 text-[9px] tracking-widest text-neutral-400 uppercase font-mono px-2 py-0.5 rounded bg-black/70 border border-white/10 backdrop-blur-md">
        {zoomLevel.toFixed(1)}x Optical
      </div>
    </div>
  );
};
