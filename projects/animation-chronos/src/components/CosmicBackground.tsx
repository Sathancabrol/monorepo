import React, { useEffect, useRef } from 'react';

interface CosmicBackgroundProps {
  lensingStrength?: number;
  mousePos: { x: number; y: number };
}

interface Star {
  baseX: number;
  baseY: number;
  size: number;
  alpha: number;
  twinkleSpeed: number;
  color: string;
}

export const CosmicBackground: React.FC<CosmicBackgroundProps> = ({
  lensingStrength = 1.0,
  mousePos,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      initStars();
    };

    window.addEventListener('resize', handleResize);

    // Generate distant background stars (delicate, sparse, realistic cosmic deep field)
    let stars: Star[] = [];
    const initStars = () => {
      stars = [];
      const starCount = Math.floor((width * height) / 9000);
      for (let i = 0; i < starCount; i++) {
        const isColdBlue = Math.random() > 0.85;
        stars.push({
          baseX: Math.random() * width,
          baseY: Math.random() * height,
          size: Math.random() * 1.4 + 0.3,
          alpha: Math.random() * 0.7 + 0.2,
          twinkleSpeed: Math.random() * 0.02 + 0.005,
          color: isColdBlue ? 'rgba(215, 230, 255, ' : 'rgba(240, 240, 248, ',
        });
      }
    };
    initStars();

    let time = 0;

    const render = () => {
      time += 0.015;
      // True Obsidian Deep Space with faint cosmic dust undertones
      ctx.fillStyle = '#000002';
      ctx.fillRect(0, 0, width, height);

      // Subtle off-center gravitational influence anchor (black hole center, slightly offset in upper space)
      const bhX = width * 0.5 + (mousePos.x - 0.5) * 35;
      const bhY = height * 0.42 + (mousePos.y - 0.5) * 30;

      // 1. Black Hole Spacetime Distortion & Subtle Galaxy Dust Field
      const dustGrad = ctx.createRadialGradient(
        bhX,
        bhY,
        40,
        bhX,
        bhY,
        Math.max(width, height) * 0.7
      );
      dustGrad.addColorStop(0, 'rgba(0, 0, 1, 0.98)');
      dustGrad.addColorStop(0.2, 'rgba(12, 6, 22, 0.45)');
      dustGrad.addColorStop(0.45, 'rgba(20, 14, 38, 0.25)');
      dustGrad.addColorStop(0.75, 'rgba(6, 4, 16, 0.12)');
      dustGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');

      ctx.fillStyle = dustGrad;
      ctx.fillRect(0, 0, width, height);

      // 2. Gravitational Lensing Distortion Ring (Einstein Ring / Photon Sphere whisper)
      ctx.save();
      ctx.translate(bhX, bhY);
      
      // Outer faint gravitational warp ring
      const ringGrad = ctx.createRadialGradient(0, 0, 160, 0, 0, 320);
      ringGrad.addColorStop(0, 'rgba(0, 0, 0, 0.95)');
      ringGrad.addColorStop(0.48, 'rgba(40, 25, 75, 0.08)');
      ringGrad.addColorStop(0.52, 'rgba(160, 200, 255, 0.06)');
      ringGrad.addColorStop(0.56, 'rgba(30, 18, 55, 0.05)');
      ringGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');

      ctx.fillStyle = ringGrad;
      ctx.beginPath();
      ctx.arc(0, 0, 320, 0, Math.PI * 2);
      ctx.fill();

      // Black Hole Event Horizon Shadow (pure light-trapping darkness at the core)
      const shadowGrad = ctx.createRadialGradient(0, 0, 0, 0, 0, 140);
      shadowGrad.addColorStop(0, 'rgba(0, 0, 0, 1)');
      shadowGrad.addColorStop(0.8, 'rgba(0, 0, 2, 0.95)');
      shadowGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = shadowGrad;
      ctx.beginPath();
      ctx.arc(0, 0, 140, 0, Math.PI * 2);
      ctx.fill();

      ctx.restore();

      // 3. Render Stars with Real-Time Gravitational Lensing Deflection
      for (let i = 0; i < stars.length; i++) {
        const star = stars[i];
        const dx = star.baseX - bhX;
        const dy = star.baseY - bhY;
        const dist = Math.sqrt(dx * dx + dy * dy);

        // Gravitational deflection: light bends around mass (Schwarzschild light bending approximation)
        const deflectionFactor = (lensingStrength * 1600) / (dist + 70);
        const angle = Math.atan2(dy, dx);
        
        // Displaced star coordinates
        const curX = star.baseX + Math.cos(angle) * deflectionFactor;
        const curY = star.baseY + Math.sin(angle) * deflectionFactor;

        // Subtle twinkling
        const currentAlpha = star.alpha * (0.7 + 0.3 * Math.sin(time * 1.5 + i));

        // If star is close to the lensing ring, draw subtle curved light smear
        if (dist > 180 && dist < 420 && lensingStrength > 0.4) {
          const smearLen = (1 - Math.abs(dist - 300) / 120) * 4 * lensingStrength;
          const tangAngle = angle + Math.PI / 2;
          ctx.strokeStyle = `${star.color}${currentAlpha * 0.5})`;
          ctx.lineWidth = star.size * 0.8;
          ctx.beginPath();
          ctx.moveTo(curX - Math.cos(tangAngle) * smearLen, curY - Math.sin(tangAngle) * smearLen);
          ctx.lineTo(curX + Math.cos(tangAngle) * smearLen, curY + Math.sin(tangAngle) * smearLen);
          ctx.stroke();
        } else {
          ctx.fillStyle = `${star.color}${currentAlpha})`;
          ctx.beginPath();
          ctx.arc(curX, curY, star.size, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
    };
  }, [lensingStrength, mousePos]);

  return (
    <canvas
      id="cosmic-canvas"
      ref={canvasRef}
      className="absolute inset-0 w-full h-full pointer-events-none z-0"
    />
  );
};
