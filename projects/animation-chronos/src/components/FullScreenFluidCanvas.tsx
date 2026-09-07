import React, { useEffect, useRef } from 'react';

interface FluidNode {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  baseRadius: number;
  phase: number;
  speed: number;
  colorType: 'obsidian' | 'violet' | 'core';
  orbitAngle: number;
  orbitRadius: number;
  orbitSpeed: number;
  spikeCount: number;
}

interface Filament {
  fromNode: number;
  toNode: number;
  width: number;
  tension: number;
}

interface TyphoonBubble {
  angle: number;
  dist: number;
  speed: number;
  radialDrift: number;
  radius: number;
  alpha: number;
  wobble: number;
  type: 'air' | 'vacuum' | 'luminous';
}

interface FullScreenFluidCanvasProps {
  mousePos: { x: number; y: number };
  fluidIntensity?: number; // 0.5 to 2.0
  isInteractive?: boolean;
  isVisible?: boolean;
  shockwaveTrigger?: number;
}

export const FullScreenFluidCanvas: React.FC<FullScreenFluidCanvasProps> = ({
  mousePos,
  fluidIntensity = 1.0,
  isInteractive = true,
  isVisible = true,
  shockwaveTrigger = 0,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const mouseRef = useRef({ x: window.innerWidth * 0.5, y: window.innerHeight * 0.5, isDown: false });
  const shockwaveRef = useRef<{ active: boolean; radius: number; maxRadius: number; speed: number }>({
    active: false,
    radius: 0,
    maxRadius: 1000,
    speed: 24,
  });

  // Trigger radial shockwave when shockwaveTrigger changes
  useEffect(() => {
    if (shockwaveTrigger > 0) {
      shockwaveRef.current = {
        active: true,
        radius: 20,
        maxRadius: Math.max(window.innerWidth, window.innerHeight) * 1.2,
        speed: 32,
      };
    }
  }, [shockwaveTrigger]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animId: number;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      initNodes();
    };

    window.addEventListener('resize', handleResize);

    // Track mouse in canvas space
    const handleMouseMove = (e: MouseEvent) => {
      mouseRef.current.x = e.clientX;
      mouseRef.current.y = e.clientY;
    };
    const handleMouseDown = () => {
      mouseRef.current.isDown = true;
    };
    const handleMouseUp = () => {
      mouseRef.current.isDown = false;
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mousedown', handleMouseDown);
    window.addEventListener('mouseup', handleMouseUp);

    // Generate distributed fluid bodies and typhoon air bubbles across the entire screen
    let nodes: FluidNode[] = [];
    let filaments: Filament[] = [];
    let typhoonBubbles: TyphoonBubble[] = [];

    const initNodes = () => {
      nodes = [];
      filaments = [];
      typhoonBubbles = [];

      const cx = width * 0.5;
      const cy = height * 0.5;

      // 1. Central bilateral hub nodes (anchoring the vessel structure)
      nodes.push({
        x: cx - 40,
        y: cy - 10,
        vx: 0,
        vy: 0,
        radius: 65,
        baseRadius: 65,
        phase: 0,
        speed: 0.015,
        colorType: 'violet',
        orbitAngle: 0,
        orbitRadius: 40,
        orbitSpeed: 0.004,
        spikeCount: 8,
      });

      nodes.push({
        x: cx + 45,
        y: cy + 15,
        vx: 0,
        vy: 0,
        radius: 70,
        baseRadius: 70,
        phase: Math.PI,
        speed: 0.012,
        colorType: 'violet',
        orbitAngle: Math.PI,
        orbitRadius: 45,
        orbitSpeed: 0.004,
        spikeCount: 9,
      });

      // Central bridge node with soft blue luminescence
      nodes.push({
        x: cx,
        y: cy,
        vx: 0,
        vy: 0,
        radius: 35,
        baseRadius: 35,
        phase: 1.5,
        speed: 0.02,
        colorType: 'core',
        orbitAngle: 0.5,
        orbitRadius: 8,
        orbitSpeed: 0.006,
        spikeCount: 6,
      });

      // 2. Peripheral Screen-Filling Fluid Masses (Typhoon Spiral Orbit Distribution)
      const count = Math.max(16, Math.floor((width * height) / 40000));
      for (let i = 0; i < count; i++) {
        // Spiral logarithm distribution (Typhoon Arms)
        const armOffset = (i % 3) * ((Math.PI * 2) / 3);
        const spiralProgress = i / count;
        const angle = spiralProgress * Math.PI * 4 + armOffset;
        const dist = 70 + spiralProgress * (Math.min(width, height) * 0.48);

        const nx = cx + Math.cos(angle) * dist;
        const ny = cy + Math.sin(angle) * (dist * 0.88);
        const rad = Math.random() * 34 + 18;

        nodes.push({
          x: Math.max(25, Math.min(width - 25, nx)),
          y: Math.max(25, Math.min(height - 25, ny)),
          vx: (Math.random() - 0.5) * 0.2,
          vy: (Math.random() - 0.5) * 0.2,
          radius: rad,
          baseRadius: rad,
          phase: Math.random() * Math.PI * 2,
          speed: 0.01 + Math.random() * 0.018,
          colorType: Math.random() > 0.35 ? 'obsidian' : 'violet',
          orbitAngle: angle,
          orbitRadius: dist,
          orbitSpeed: 0.002 + (1 - dist / (width * 0.5)) * 0.005, // Faster near center (Keplerian vortex)
          spikeCount: Math.floor(Math.random() * 6) + 7,
        });
      }

      // 3. Typhoon Air Bubbles navigating in the magnetic cyclone spiral
      const bubbleCount = Math.max(30, Math.floor((width * height) / 28000));
      for (let b = 0; b < bubbleCount; b++) {
        const bDist = Math.random() * (Math.min(width, height) * 0.52) + 25;
        const bAngle = Math.random() * Math.PI * 2;
        typhoonBubbles.push({
          dist: bDist,
          angle: bAngle,
          speed: (0.006 + 0.018 / Math.sqrt(bDist * 0.1 + 1)) * (0.8 + Math.random() * 0.4),
          radialDrift: (Math.random() - 0.5) * 0.25,
          radius: Math.random() * 5.5 + 2.0,
          alpha: Math.random() * 0.6 + 0.35,
          wobble: Math.random() * Math.PI * 2,
          type: Math.random() > 0.75 ? 'luminous' : Math.random() > 0.4 ? 'air' : 'vacuum',
        });
      }

      // Build continuous filaments (viscous bridges) between nearby nodes
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const dx = nodes[i].x - nodes[j].x;
          const dy = nodes[i].y - nodes[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 260 && Math.random() > 0.35) {
            filaments.push({
              fromNode: i,
              toNode: j,
              width: Math.random() * 7 + 3,
              tension: 0.6 + Math.random() * 0.4,
            });
          }
        }
      }
    };

    initNodes();

    let time = 0;

    const render = () => {
      time += 0.016;

      ctx.clearRect(0, 0, width, height);

      const cx = width * 0.5;
      const cy = height * 0.5;
      const mx = mouseRef.current.x;
      const my = mouseRef.current.y;
      const isMouseDown = mouseRef.current.isDown;

      // 1. Update fluid node dynamics in Typhoon Spiral Vortex
      for (let i = 0; i < nodes.length; i++) {
        const node = nodes[i];
        node.phase += node.speed * fluidIntensity;

        // Pulsating volume breathing
        node.radius = node.baseRadius + Math.sin(node.phase) * (node.baseRadius * 0.15);

        // Typhoon angular spiral motion
        node.orbitAngle += node.orbitSpeed * fluidIntensity;
        // Inward/outward spiral oscillation
        const radialWobble = Math.sin(time * 0.8 + node.phase) * 12;
        const currentR = Math.max(15, node.orbitRadius + radialWobble);

        const targetX = cx + Math.cos(node.orbitAngle) * currentR;
        const targetY = cy + Math.sin(node.orbitAngle) * (currentR * 0.88);

        node.x += (targetX - node.x) * 0.015;
        node.y += (targetY - node.y) * 0.015;

        // Interactive magnetic attraction to cursor
        if (isInteractive) {
          const mdx = mx - node.x;
          const mdy = my - node.y;
          const mdist = Math.sqrt(mdx * mdx + mdy * mdy);

          if (mdist < 300) {
            const pull = (1 - mdist / 300) * (isMouseDown ? 4.5 : 2.0) * fluidIntensity;
            node.x += (mdx / mdist) * pull;
            node.y += (mdy / mdist) * pull;
            node.radius += (1 - mdist / 300) * 8;
          }
        }

        // Outward impulse from Chronos Awakening Shockwave
        if (shockwaveRef.current.active) {
          const cdx = node.x - cx;
          const cdy = node.y - cy;
          const cdist = Math.sqrt(cdx * cdx + cdy * cdy) || 1;
          const waveDist = Math.abs(cdist - shockwaveRef.current.radius);
          if (waveDist < 140) {
            const impulse = (1 - waveDist / 140) * 16;
            node.x += (cdx / cdist) * impulse;
            node.y += (cdy / cdist) * impulse;
            node.radius += (1 - waveDist / 140) * 12;
          }
        }
      }

      // Advance Shockwave
      if (shockwaveRef.current.active) {
        shockwaveRef.current.radius += shockwaveRef.current.speed;
        if (shockwaveRef.current.radius > shockwaveRef.current.maxRadius) {
          shockwaveRef.current.active = false;
        } else {
          ctx.save();
          ctx.beginPath();
          ctx.arc(cx, cy, shockwaveRef.current.radius, 0, Math.PI * 2);
          const shockAlpha = Math.max(0, 1 - shockwaveRef.current.radius / shockwaveRef.current.maxRadius);
          ctx.strokeStyle = `rgba(186, 230, 253, ${shockAlpha * 0.5})`;
          ctx.lineWidth = 4;
          ctx.shadowColor = '#38bdf8';
          ctx.shadowBlur = 25;
          ctx.stroke();
          ctx.restore();
        }
      }

      // 2. Render Typhoon Air Bubbles navigating along spiral streams
      ctx.save();
      for (let b = 0; b < typhoonBubbles.length; b++) {
        const bubble = typhoonBubbles[b];
        bubble.angle += bubble.speed * fluidIntensity;
        bubble.dist += bubble.radialDrift * fluidIntensity;

        // Loop boundaries within screen vortex
        if (bubble.dist < 20) bubble.dist = Math.min(width, height) * 0.5;
        if (bubble.dist > Math.min(width, height) * 0.55) bubble.dist = 30;

        bubble.wobble += 0.03;
        const bx = cx + Math.cos(bubble.angle) * bubble.dist + Math.sin(bubble.wobble) * 4;
        const by = cy + Math.sin(bubble.angle) * (bubble.dist * 0.88) + Math.cos(bubble.wobble) * 4;

        // Draw refractive bubble body
        ctx.beginPath();
        ctx.arc(bx, by, bubble.radius, 0, Math.PI * 2);

        if (bubble.type === 'luminous') {
          ctx.fillStyle = `rgba(186, 230, 253, ${bubble.alpha * 0.85})`;
          ctx.shadowColor = '#38bdf8';
          ctx.shadowBlur = 8;
        } else if (bubble.type === 'air') {
          ctx.fillStyle = `rgba(30, 24, 45, ${bubble.alpha * 0.9})`;
          ctx.shadowBlur = 0;
        } else {
          ctx.fillStyle = `rgba(10, 8, 16, ${bubble.alpha * 0.95})`;
          ctx.shadowBlur = 0;
        }
        ctx.fill();

        // White specular meniscus reflection
        ctx.beginPath();
        ctx.arc(bx - bubble.radius * 0.35, by - bubble.radius * 0.35, bubble.radius * 0.45, 0, Math.PI * 1.2);
        ctx.strokeStyle = `rgba(255, 255, 255, ${bubble.alpha * 0.75})`;
        ctx.lineWidth = 1;
        ctx.stroke();

        // Thin outer refractive rim
        ctx.beginPath();
        ctx.arc(bx, by, bubble.radius, 0, Math.PI * 2);
        ctx.strokeStyle =
          bubble.type === 'luminous'
            ? 'rgba(186, 230, 253, 0.6)'
            : 'rgba(140, 160, 220, 0.25)';
        ctx.lineWidth = 0.75;
        ctx.stroke();
      }
      ctx.restore();

      // 2. Render Viscous Liquid Filaments (Organic Bridges across the screen)
      ctx.save();
      for (let i = 0; i < filaments.length; i++) {
        const f = filaments[i];
        const n1 = nodes[f.fromNode];
        const n2 = nodes[f.toNode];
        if (!n1 || !n2) continue;

        const dx = n2.x - n1.x;
        const dy = n2.y - n1.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist > 340) continue; // Filament breaks if stretched too far

        const midX = (n1.x + n2.x) * 0.5;
        const midY = (n1.y + n2.y) * 0.5;

        // Curvature / sagging in zero-g magnetic field
        const wave = Math.sin(time * 1.5 + f.tension * 5) * 12;
        const perpX = -dy / dist;
        const perpY = dx / dist;
        const cpX = midX + perpX * wave;
        const cpY = midY + perpY * wave;

        const alpha = Math.max(0, 1 - dist / 340) * 0.85 * fluidIntensity;

        // Draw glossy outer liquid membrane
        ctx.strokeStyle = `rgba(18, 10, 32, ${alpha})`;
        ctx.lineWidth = f.width * (1 - dist / 380) * 2.2;
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(n1.x, n1.y);
        ctx.quadraticCurveTo(cpX, cpY, n2.x, n2.y);
        ctx.stroke();

        // Inner dark violet sheen
        ctx.strokeStyle = `rgba(45, 24, 68, ${alpha * 0.9})`;
        ctx.lineWidth = f.width * (1 - dist / 380) * 1.2;
        ctx.beginPath();
        ctx.moveTo(n1.x, n1.y);
        ctx.quadraticCurveTo(cpX, cpY, n2.x, n2.y);
        ctx.stroke();

        // Specular highlight filament ridge (metallic reflection)
        ctx.strokeStyle = `rgba(150, 140, 200, ${alpha * 0.35})`;
        ctx.lineWidth = Math.max(0.8, f.width * 0.25);
        ctx.beginPath();
        ctx.moveTo(n1.x + perpX * 1.5, n1.y + perpY * 1.5);
        ctx.quadraticCurveTo(cpX + perpX * 1.5, cpY + perpY * 1.5, n2.x + perpX * 1.5, n2.y + perpY * 1.5);
        ctx.stroke();
      }
      ctx.restore();

      // 3. Render Fluid Masses / Lobes with Realistic Rosensweig Magnetic Spikes & Metallic Obsidian
      for (let i = 0; i < nodes.length; i++) {
        const node = nodes[i];

        // Authentic Rosensweig magnetic spikes (sharp cones along magnetic flux vectors)
        const pointCount = node.spikeCount * 2;
        ctx.save();
        ctx.beginPath();

        for (let p = 0; p <= pointCount; p++) {
          const angle = (p / pointCount) * Math.PI * 2;
          const isTip = p % 2 === 1;

          // Rosensweig instability spike calculation
          const spikeFactor = isTip
            ? 0.28 + Math.sin(angle * 4 + time * 2.5 + node.phase) * 0.08
            : -0.05;
          const ripple = Math.sin(angle * 3 - time * 1.8) * (node.radius * 0.04);
          const r = node.radius * (1 + spikeFactor) + ripple;

          const px = node.x + Math.cos(angle) * r;
          const py = node.y + Math.sin(angle) * r;

          if (p === 0) {
            ctx.moveTo(px, py);
          } else {
            ctx.lineTo(px, py);
          }
        }
        ctx.closePath();

        // Fluid mass gradient
        let grad: CanvasGradient;
        if (node.colorType === 'core') {
          grad = ctx.createRadialGradient(node.x, node.y, 2, node.x, node.y, node.radius * 1.35);
          grad.addColorStop(0, 'rgba(235, 248, 255, 0.98)');
          grad.addColorStop(0.2, 'rgba(56, 189, 248, 0.75)');
          grad.addColorStop(0.5, 'rgba(30, 15, 55, 0.85)');
          grad.addColorStop(1, 'rgba(4, 2, 8, 0)');
        } else if (node.colorType === 'violet') {
          grad = ctx.createRadialGradient(
            node.x - node.radius * 0.25,
            node.y - node.radius * 0.25,
            3,
            node.x,
            node.y,
            node.radius * 1.2
          );
          grad.addColorStop(0, 'rgba(64, 38, 92, 0.9)');
          grad.addColorStop(0.45, 'rgba(20, 12, 34, 0.96)');
          grad.addColorStop(0.85, 'rgba(8, 5, 14, 0.98)');
          grad.addColorStop(1, 'rgba(2, 1, 5, 0.92)');
        } else {
          grad = ctx.createRadialGradient(
            node.x - node.radius * 0.25,
            node.y - node.radius * 0.25,
            2,
            node.x,
            node.y,
            node.radius * 1.2
          );
          grad.addColorStop(0, 'rgba(48, 44, 58, 0.9)');
          grad.addColorStop(0.5, 'rgba(14, 12, 18, 0.98)');
          grad.addColorStop(1, 'rgba(2, 2, 4, 0.95)');
        }

        ctx.fillStyle = grad;
        ctx.shadowColor = node.colorType === 'core' ? '#38bdf8' : 'rgba(20, 10, 40, 0.6)';
        ctx.shadowBlur = node.colorType === 'core' ? 32 : 16;
        ctx.fill();

        // Metallic chrome highlight rim
        ctx.shadowBlur = 0;
        ctx.strokeStyle =
          node.colorType === 'core'
            ? 'rgba(186, 230, 253, 0.7)'
            : 'rgba(180, 170, 220, 0.28)';
        ctx.lineWidth = 1.2;
        ctx.stroke();

        // Chrome specular glint spots on spike tips
        for (let p = 1; p <= pointCount; p += 2) {
          const angle = (p / pointCount) * Math.PI * 2;
          const r = node.radius * 1.25;
          const tipX = node.x + Math.cos(angle) * r;
          const tipY = node.y + Math.sin(angle) * r;

          ctx.beginPath();
          ctx.arc(tipX, tipY, 1.2, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(255, 255, 255, 0.75)';
          ctx.fill();
        }

        // Curved specular liquid meniscus reflection
        ctx.beginPath();
        ctx.arc(
          node.x - node.radius * 0.22,
          node.y - node.radius * 0.25,
          node.radius * 0.45,
          0.1,
          Math.PI * 0.85
        );
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.35)';
        ctx.lineWidth = 1.4;
        ctx.stroke();

        ctx.restore();
      }

      // 5. Interactive Cursor Ferrofluid Disturbance (pulls magnetic tendrils directly to the mouse)
      if (isInteractive) {
        ctx.save();
        const cursorGrad = ctx.createRadialGradient(mx, my, 0, mx, my, 80);
        cursorGrad.addColorStop(0, 'rgba(180, 220, 255, 0.12)');
        cursorGrad.addColorStop(0.5, 'rgba(65, 35, 110, 0.08)');
        cursorGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = cursorGrad;
        ctx.beginPath();
        ctx.arc(mx, my, 80, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }

      animId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mousedown', handleMouseDown);
      window.removeEventListener('mouseup', handleMouseUp);
      cancelAnimationFrame(animId);
    };
  }, [fluidIntensity, isInteractive]);

  return (
    <canvas
      id="fullscreen-ferrofluid-canvas"
      ref={canvasRef}
      style={{
        opacity: isVisible ? 1 : 0,
        transition: 'opacity 1.8s cubic-bezier(0.16, 1, 0.3, 1)',
      }}
      className="fixed inset-0 w-full h-full pointer-events-none z-[2]"
    />
  );
};
