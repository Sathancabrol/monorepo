import re
from pathlib import Path

TARGET = Path("/home/user/monorepo/scripts/build_html_dashboard.py")

with open(TARGET, "r", encoding="utf-8") as f:
    code = f.read()

# Replace the radar and 3D simulation JavaScript logic
idx_radar = code.find("// RADAR / 3D CUBE VISUALIZER")
idx_catalog = code.find("// TAB 7: TOOLS & MATERIALS CATALOG")

if idx_radar == -1 or idx_catalog == -1:
    print("Error locating radar or catalog markers in build_html_dashboard.py")
    exit(1)

new_radar_js = """    // ==========================================
    // WATCH TOWER : 2D VUE SATELLITE & 3D GRILLE XYZ
    // ==========================================
    let radarCanvas, radarCtx, radarAnimId;
    let simulatorViewMode = 'radar'; // 'radar' (2D Vue Satellite) or '3dcube' (3D Grille XYZ)
    let isRadarLive = true;
    let fleetFilter = 'all';

    // 3D Camera & Projection State
    let camYaw = 40;       // Yaw angle in degrees (0-360)
    let camPitch = 25;     // Pitch angle in degrees (-20 to +85)
    let camZoom = 1.0;     // Zoom factor
    let camPanX = 0;
    let camPanY = 0;
    let isDragging3D = false;
    let lastMouseX = 0;
    let lastMouseY = 0;

    function rotate3D(dYaw, dPitch) {
        camYaw = (camYaw + dYaw + 360) % 360;
        camPitch = Math.max(-20, Math.min(85, camPitch + dPitch));
    }

    function zoom3D(factor) {
        camZoom = Math.max(0.4, Math.min(2.8, camZoom * factor));
    }

    function set3DPreset(preset) {
        if (preset === 'iso') {
            camYaw = 40; camPitch = 25; camZoom = 1.0; camPanX = 0; camPanY = 0;
        } else if (preset === 'top') {
            camYaw = 0; camPitch = 85; camZoom = 1.05; camPanX = 0; camPanY = 0;
        } else if (preset === 'section') {
            camYaw = 90; camPitch = 5; camZoom = 1.25; camPanX = 0; camPanY = 0;
        } else if (preset === 'reset') {
            camYaw = 40; camPitch = 25; camZoom = 1.0; camPanX = 0; camPanY = 0;
        }
    }

    function project3D(x, y, z, cx, cy) {
        // Metric coordinates: x (Longitudinal 0..50m), y (Transversal -10..+10m), z (Altimetry -3..+15m)
        const scale = 8.2 * camZoom;
        const radYaw = (camYaw * Math.PI) / 180;
        const radPitch = (camPitch * Math.PI) / 180;

        // Origin at x=25, y=0, z=0
        const ox = x - 25;
        const oy = y;
        const oz = z;

        // Rotate around Z (Yaw)
        const x1 = ox * Math.cos(radYaw) - oy * Math.sin(radYaw);
        const y1 = ox * Math.sin(radYaw) + oy * Math.cos(radYaw);
        const z1 = oz;

        // Rotate around X (Pitch)
        const x2 = x1;
        const y2 = y1 * Math.cos(radPitch) - z1 * Math.sin(radPitch);
        const z2 = y1 * Math.sin(radPitch) + z1 * Math.cos(radPitch);

        const sx = cx + camPanX + x2 * scale;
        const sy = cy + camPanY - z2 * scale - y2 * (scale * 0.45);

        return { sx, sy, depth: y2 };
    }

    function initWatchtowerRadar() {
        radarCanvas = document.getElementById('watchtower-radar-canvas');
        if (!radarCanvas) return;
        const rect = radarCanvas.getBoundingClientRect();
        radarCanvas.width = rect.width * window.devicePixelRatio;
        radarCanvas.height = rect.height * window.devicePixelRatio;
        radarCtx = radarCanvas.getContext('2d');
        radarCtx.scale(window.devicePixelRatio, window.devicePixelRatio);

        // Interactive mouse drag to orbit in 3D
        radarCanvas.onmousedown = (e) => {
            if (simulatorViewMode === '3dcube') {
                isDragging3D = true;
                lastMouseX = e.clientX;
                lastMouseY = e.clientY;
                radarCanvas.style.cursor = 'grabbing';
            }
        };
        window.addEventListener('mousemove', (e) => {
            if (isDragging3D && simulatorViewMode === '3dcube') {
                const dx = e.clientX - lastMouseX;
                const dy = e.clientY - lastMouseY;
                lastMouseX = e.clientX;
                lastMouseY = e.clientY;
                rotate3D(dx * 0.6, -dy * 0.6);
            }
        });
        window.addEventListener('mouseup', () => {
            if (isDragging3D) {
                isDragging3D = false;
                if (radarCanvas) radarCanvas.style.cursor = 'grab';
            }
        });

        if (!radarAnimId) animateSimulatorRadar();
        update3DCoordsTable(currentScenarioId || 'scen_tranchee_vrd');
    }

    function setSimulatorViewMode(mode) {
        simulatorViewMode = mode;
        const btnRadar = document.getElementById('btn-view-radar');
        const btn3D = document.getElementById('btn-view-3dcube');
        const toolbar = document.getElementById('sim-3d-toolbar');
        const badge = document.getElementById('sim-canvas-overlay-badge');

        if (btnRadar) btnRadar.classList.toggle('active', mode === 'radar');
        if (btn3D) btn3D.classList.toggle('active', mode === '3dcube');
        if (toolbar) toolbar.style.display = (mode === '3dcube' ? 'flex' : 'none');
        if (badge) {
            badge.innerText = (mode === 'radar' 
                ? '🛰️ Vue Satellite Haute Résolution | RGF93 CC43' 
                : '🧊 3D : Grille XYZ & Emplacements Théoriques');
        }
    }

    function toggleRadarLiveMode() {
        isRadarLive = !isRadarLive;
        const btn = document.getElementById('btn-radar-mode-toggle');
        if (btn) btn.innerText = isRadarLive ? '🟢 Mode Live Actif' : '⏸️ Mode Statique OPBTP';
        logCockpit(`Watch Tower : Bascule vers le mode ${isRadarLive ? 'Live Animé' : 'Statique Réglementaire'}.`, 'info');
    }

    function animateSimulatorRadar() {
        if (!radarCtx || !radarCanvas) return;
        const w = radarCanvas.width / window.devicePixelRatio;
        const h = radarCanvas.height / window.devicePixelRatio;
        radarCtx.clearRect(0, 0, w, h);

        if (simulatorViewMode === 'radar') {
            renderSatelliteView2D(radarCtx, w, h);
        } else {
            renderTheoretical3DGrid(radarCtx, w, h);
        }

        radarAnimId = requestAnimationFrame(animateSimulatorRadar);
    }

    // ----------------------------------------------------
    // 1. 2D SATELLITE VIEW (HIGH-DEFINITION ORTHOPHOTO MAP)
    // ----------------------------------------------------
    function renderSatelliteView2D(ctx, w, h) {
        const t = isRadarLive ? Date.now() * 0.0015 : 0;

        // Ground / Orthophoto Terrain Background
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, w, h);

        // Terrain texture & vegetation
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(0, 0, w, 90);
        ctx.fillStyle = '#0f291e'; // Green verge
        ctx.fillRect(0, 90, w, 35);
        ctx.fillRect(0, h - 100, w, 100);

        // Water Canal / Littoral edge for Sète
        ctx.fillStyle = '#083344';
        ctx.fillRect(0, h - 50, w, 50);
        ctx.fillStyle = '#06b6d4';
        ctx.font = '9px JetBrains Mono';
        ctx.fillText('🌊 CANAL / PLAN D\\'EAU (LITTORAL SÈTE)', 20, h - 20);

        // Main Road Asphalt Strip
        ctx.fillStyle = '#1e2029';
        ctx.fillRect(0, 125, w, 190);

        // Road markings & dashes
        ctx.strokeStyle = '#f8fafc';
        ctx.lineWidth = 2;
        ctx.setLineDash([12, 10]);
        ctx.beginPath(); ctx.moveTo(0, 220); ctx.lineTo(w, 220); ctx.stroke();
        ctx.setLineDash([]);

        // RGF93 CC43 Grid Lines
        ctx.strokeStyle = 'rgba(51, 65, 85, 0.4)';
        ctx.lineWidth = 1;
        for (let x = 0; x < w; x += 60) {
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
        }
        for (let y = 0; y < h; y += 60) {
            ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
        }

        // Compass Rose (North Arrow)
        ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
        ctx.strokeStyle = 'var(--border)';
        ctx.lineWidth = 1;
        ctx.beginPath(); ctx.arc(w - 40, 45, 20, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
        ctx.fillStyle = '#ef4444';
        ctx.beginPath(); ctx.moveTo(w - 40, 30); ctx.lineTo(w - 45, 45); ctx.lineTo(w - 40, 42); ctx.fill();
        ctx.fillStyle = '#e2e8f0';
        ctx.beginPath(); ctx.moveTo(w - 40, 30); ctx.lineTo(w - 35, 45); ctx.lineTo(w - 40, 42); ctx.fill();
        ctx.font = 'bold 9px JetBrains Mono'; ctx.textAlign = 'center'; ctx.fillText('N', w - 40, 25);

        // NETWORKS (AIPR OVERLAY)
        // 1. Gas MPB 4 bar
        ctx.fillStyle = 'rgba(239, 68, 68, 0.15)';
        ctx.fillRect(40, 100, w - 80, 25);
        ctx.strokeStyle = '#eab308';
        ctx.lineWidth = 3;
        ctx.beginPath(); ctx.moveTo(40, 112); ctx.lineTo(w - 40, 112); ctx.stroke();
        ctx.fillStyle = '#eab308'; ctx.font = '9px JetBrains Mono'; ctx.textAlign = 'left';
        ctx.fillText('⚡ GAZ MPB 4 BARS PEHD 100 (DLA 3m)', 50, 108);

        // 2. Aerial Electric Line 20kV
        ctx.strokeStyle = '#f97316';
        ctx.setLineDash([4, 4]);
        ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(20, 40); ctx.lineTo(w - 20, 40); ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#f97316'; ctx.fillText('⚠️ LIGNE AÉRIENNE HTA 20 kV (DLA 3m/5m)', 30, 35);

        // 3. Assainissement EP/EU Trench
        ctx.fillStyle = 'rgba(6, 182, 212, 0.2)';
        ctx.fillRect(80, 170, w - 160, 40);
        ctx.strokeStyle = '#06b6d4';
        ctx.lineWidth = 2;
        ctx.strokeRect(80, 170, w - 160, 40);
        ctx.fillStyle = '#38bdf8';
        ctx.fillText('💧 TRANCHÉE ASSAINISSEMENT FONTE DN400 (-1.80m)', 90, 195);

        // OPBTP SIGNAGE POSTS
        const signs = [
            { x: 30, y: 140, label: 'AK5 Travaux' },
            { x: 70, y: 140, label: 'B14 50km/h' },
            { x: 120, y: 140, label: 'KR11J Feux' }
        ];
        signs.forEach(s => {
            ctx.fillStyle = '#f59e0b';
            ctx.beginPath(); ctx.arc(s.x, s.y, 6, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#0f172a'; ctx.font = 'bold 7px JetBrains Mono'; ctx.textAlign = 'center';
            ctx.fillText('⚠️', s.x, s.y + 2.5);
            ctx.fillStyle = '#cbd5e1'; ctx.font = '8px Plus Jakarta Sans'; ctx.fillText(s.label, s.x, s.y + 14);
        });

        // MACHINES & VECTORS
        const jX1 = isRadarLive ? Math.sin(t * 1.5) * 4 : 0;
        const jY1 = isRadarLive ? Math.cos(t * 1.5) * 2 : 0;

        // 1. Excavator Liebherr 24t
        ctx.fillStyle = '#f59e0b';
        ctx.fillRect(160 + jX1 - 14, 180 + jY1 - 10, 28, 20);
        ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.strokeRect(160 + jX1 - 14, 180 + jY1 - 10, 28, 20);
        ctx.fillStyle = '#fff'; ctx.font = 'bold 9px Plus Jakarta Sans'; ctx.textAlign = 'left';
        ctx.fillText('🚜 Pelle Liebherr 24t', 160 + jX1 + 18, 186 + jY1);

        // Excavator swing radius (AIPR safety circle)
        ctx.strokeStyle = 'rgba(245, 158, 11, 0.4)';
        ctx.setLineDash([3, 3]);
        ctx.beginPath(); ctx.arc(160 + jX1, 180 + jY1, 35, 0, Math.PI * 2); ctx.stroke();
        ctx.setLineDash([]);

        // 2. Scania 8x4 Truck
        ctx.fillStyle = '#3b82f6';
        ctx.fillRect(280 - 18, 150 - 9, 36, 18);
        ctx.strokeStyle = '#fff'; ctx.strokeRect(280 - 18, 150 - 9, 36, 18);
        ctx.fillStyle = '#e2e8f0'; ctx.fillText('🚛 Scania 8x4 Bi-Benne', 280 + 22, 155);

        // 3. Compacteur Bomag
        ctx.fillStyle = '#10b981';
        ctx.fillRect(390 - 12, 240 - 10, 24, 20);
        ctx.fillStyle = '#e2e8f0'; ctx.fillText('🔨 Bomag BW213', 390 + 16, 246);

        // 4. Robot Husqvarna DXR 300
        ctx.fillStyle = '#a855f7';
        ctx.fillRect(120 - 8, 230 - 8, 16, 16);
        ctx.fillStyle = '#e2e8f0'; ctx.fillText('🤖 Robot DXR 300', 120 + 12, 236);

        // 5. Exoskeleton & Workers
        const workers = [
            { x: 210, y: 195, label: 'K. Benali (AIPR / Canalisateur)', exo: false },
            { x: 235, y: 185, label: 'F. Roche (🦾 Exosquelette HAPO)', exo: true }
        ];
        workers.forEach(wkr => {
            ctx.beginPath(); ctx.arc(wkr.x, wkr.y, 6, 0, Math.PI * 2);
            ctx.fillStyle = wkr.exo ? '#38bdf8' : '#10b981'; ctx.fill();
            ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke();
            ctx.fillStyle = '#cbd5e1'; ctx.font = '8px Plus Jakarta Sans';
            ctx.fillText(wkr.label, wkr.x + 9, wkr.y + 3);
        });

        // 6. Drone DJI Matrice 350 RTK (Aerial survey)
        const droneX = 330 + (isRadarLive ? Math.cos(t * 2) * 20 : 0);
        const droneY = 80 + (isRadarLive ? Math.sin(t * 2) * 12 : 0);

        // Drone LiDAR Cone
        ctx.fillStyle = 'rgba(16, 185, 129, 0.12)';
        ctx.beginPath();
        ctx.moveTo(droneX, droneY);
        ctx.lineTo(droneX - 45, droneY + 85);
        ctx.lineTo(droneX + 45, droneY + 85);
        ctx.closePath(); ctx.fill();
        ctx.strokeStyle = 'rgba(16, 185, 129, 0.4)'; ctx.stroke();

        // Drone Body
        ctx.fillStyle = '#06b6d4';
        ctx.beginPath(); ctx.arc(droneX, droneY, 7, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke();
        ctx.fillStyle = '#06b6d4'; ctx.font = 'bold 8px Plus Jakarta Sans';
        ctx.fillText('🛸 Drone DJI M350 LiDAR (Z=+10m)', droneX + 11, droneY + 3);
    }

    // ----------------------------------------------------
    // 2. 3D THEORETICAL XYZ GRID & PLACEMENT ENVIRONMENT
    // ----------------------------------------------------
    function renderTheoretical3DGrid(ctx, w, h) {
        const cx = w / 2;
        const cy = h / 2 + 30;

        // Dark Blueprint / 3D Spatial Canvas Background
        ctx.fillStyle = '#060d1a';
        ctx.fillRect(0, 0, w, h);

        // 3D Metric Grid on Ground (Z = 0.00m)
        ctx.strokeStyle = 'rgba(30, 58, 95, 0.6)';
        ctx.lineWidth = 1;
        for (let x = 0; x <= 50; x += 5) {
            const p1 = project3D(x, -10, 0, cx, cy);
            const p2 = project3D(x, 10, 0, cx, cy);
            ctx.beginPath(); ctx.moveTo(p1.sx, p1.sy); ctx.lineTo(p2.sx, p2.sy); ctx.stroke();
        }
        for (let y = -10; y <= 10; y += 2.5) {
            const p1 = project3D(0, y, 0, cx, cy);
            const p2 = project3D(50, y, 0, cx, cy);
            ctx.beginPath(); ctx.moveTo(p1.sx, p1.sy); ctx.lineTo(p2.sx, p2.sy); ctx.stroke();
        }

        // 3D COORDINATE AXES (X Rouge, Y Vert, Z Bleu)
        const o = project3D(0, 0, 0, cx, cy);
        const axX = project3D(52, 0, 0, cx, cy);
        const axY = project3D(0, 12, 0, cx, cy);
        const axZ = project3D(0, 0, 14, cx, cy);
        const axZneg = project3D(0, 0, -3.5, cx, cy);

        // X Axis (Longitudinal)
        ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 2.5;
        ctx.beginPath(); ctx.moveTo(o.sx, o.sy); ctx.lineTo(axX.sx, axX.sy); ctx.stroke();
        ctx.fillStyle = '#ef4444'; ctx.font = 'bold 10px JetBrains Mono'; ctx.fillText('AXE X (+50m Alignement)', axX.sx + 4, axX.sy);

        // Y Axis (Transversal)
        ctx.strokeStyle = '#10b981'; ctx.lineWidth = 2.5;
        ctx.beginPath(); ctx.moveTo(o.sx, o.sy); ctx.lineTo(axY.sx, axY.sy); ctx.stroke();
        ctx.fillStyle = '#10b981'; ctx.fillText('AXE Y (±10m Transversal)', axY.sx + 4, axY.sy);

        // Z Axis (Altimetry NGF)
        ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2.5;
        ctx.beginPath(); ctx.moveTo(o.sx, o.sy); ctx.lineTo(axZ.sx, axZ.sy); ctx.stroke();
        ctx.fillStyle = '#38bdf8'; ctx.fillText('AXE Z (+15m Altimétrie / Aérien)', axZ.sx + 4, axZ.sy - 4);

        // Negative Z (Underground fouille)
        ctx.strokeStyle = '#94a3b8'; ctx.setLineDash([4, 4]); ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.moveTo(o.sx, o.sy); ctx.lineTo(axZneg.sx, axZneg.sy); ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#94a3b8'; ctx.fillText('Z < 0 (Fond de Fouille -3.00m)', axZneg.sx + 4, axZneg.sy + 10);

        // THEORETICAL 3D OBJECTS ACCORDING TO ACTIVE SCENARIO
        const scenId = currentScenarioId || 'scen_tranchee_vrd';

        if (scenId === 'scen_tranchee_vrd') {
            // 1. Excavation Trench 3D Box (X: 10..38m, Y: -1.0..+1.0m, Z: 0..-2.60m)
            const corners = [
                project3D(10, -1.0, 0, cx, cy), project3D(38, -1.0, 0, cx, cy),
                project3D(38, 1.0, 0, cx, cy), project3D(10, 1.0, 0, cx, cy),
                project3D(10, -1.0, -2.6, cx, cy), project3D(38, -1.0, -2.6, cx, cy),
                project3D(38, 1.0, -2.6, cx, cy), project3D(10, 1.0, -2.6, cx, cy)
            ];

            // Trench Volume
            ctx.fillStyle = 'rgba(180, 83, 9, 0.18)';
            ctx.beginPath();
            ctx.moveTo(corners[4].sx, corners[4].sy);
            ctx.lineTo(corners[5].sx, corners[5].sy);
            ctx.lineTo(corners[6].sx, corners[6].sy);
            ctx.lineTo(corners[7].sx, corners[7].sy);
            ctx.closePath(); ctx.fill();

            // Trench edges
            ctx.strokeStyle = '#d97706'; ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(corners[0].sx, corners[0].sy); ctx.lineTo(corners[1].sx, corners[1].sy);
            ctx.lineTo(corners[2].sx, corners[2].sy); ctx.lineTo(corners[3].sx, corners[3].sy);
            ctx.closePath();
            ctx.moveTo(corners[0].sx, corners[0].sy); ctx.lineTo(corners[4].sx, corners[4].sy);
            ctx.moveTo(corners[1].sx, corners[1].sy); ctx.lineTo(corners[5].sx, corners[5].sy);
            ctx.moveTo(corners[2].sx, corners[2].sy); ctx.lineTo(corners[6].sx, corners[6].sy);
            ctx.moveTo(corners[3].sx, corners[3].sy); ctx.lineTo(corners[7].sx, corners[7].sy);
            ctx.stroke();

            // 2. Steel Shoring Box SBH (X: 14..32m, Z: 0..-2.6m)
            const sh1 = project3D(14, -0.9, 0, cx, cy);
            const sh2 = project3D(32, -0.9, 0, cx, cy);
            const sh3 = project3D(32, -0.9, -2.4, cx, cy);
            const sh4 = project3D(14, -0.9, -2.4, cx, cy);
            ctx.fillStyle = 'rgba(59, 130, 246, 0.35)';
            ctx.beginPath(); ctx.moveTo(sh1.sx, sh1.sy); ctx.lineTo(sh2.sx, sh2.sy); ctx.lineTo(sh3.sx, sh3.sy); ctx.lineTo(sh4.sx, sh4.sy); ctx.closePath(); ctx.fill();
            ctx.strokeStyle = '#3b82f6'; ctx.stroke();

            // 3. Pipe Fonte DN400 at Z = -1.80m with theoretical -1.5% slope
            const pStart = project3D(10, 0, -1.80, cx, cy);
            const pEnd = project3D(38, 0, -2.22, cx, cy); // 28m * -1.5% = -0.42m
            ctx.strokeStyle = '#06b6d4'; ctx.lineWidth = 6;
            ctx.beginPath(); ctx.moveTo(pStart.sx, pStart.sy); ctx.lineTo(pEnd.sx, pEnd.sy); ctx.stroke();
            ctx.fillStyle = '#06b6d4'; ctx.font = 'bold 9px JetBrains Mono';
            ctx.fillText('💧 Collecteur Fonte DN400 (Pente -1.5%, Z=-1.80m)', pStart.sx + 6, pStart.sy);

            // 4. Gaz MPB 4 bar at Y=+2.5m, Z=-1.0m
            const g1 = project3D(0, 2.5, -1.0, cx, cy);
            const g2 = project3D(50, 2.5, -1.0, cx, cy);
            ctx.strokeStyle = '#eab308'; ctx.lineWidth = 4;
            ctx.beginPath(); ctx.moveTo(g1.sx, g1.sy); ctx.lineTo(g2.sx, g2.sy); ctx.stroke();
            ctx.fillStyle = '#eab308'; ctx.font = '9px JetBrains Mono';
            ctx.fillText('⚡ Conduite Gaz MPB 4b (Z=-1.00m, DLA 3m)', g1.sx + 10, g1.sy);

            // 5. Aerial Power Line at Z=+7.5m, Y=-6.0m
            const e1 = project3D(0, -6.0, 7.5, cx, cy);
            const e2 = project3D(50, -6.0, 7.5, cx, cy);
            ctx.strokeStyle = '#f97316'; ctx.setLineDash([6, 4]); ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(e1.sx, e1.sy); ctx.lineTo(e2.sx, e2.sy); ctx.stroke();
            ctx.setLineDash([]);
            ctx.fillStyle = '#f97316'; ctx.fillText('⚡ Ligne HTA 20kV (Z=+7.50m)', e1.sx, e1.sy - 4);

            // 6. Machines in 3D: Pelle Liebherr 24t at (7, 0, 0)
            const pelle = project3D(7, 0, 0, cx, cy);
            ctx.fillStyle = '#f59e0b';
            ctx.beginPath(); ctx.arc(pelle.sx, pelle.sy, 10, 0, Math.PI * 2); ctx.fill();
            ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke();
            ctx.fillStyle = '#fff'; ctx.font = 'bold 9px Plus Jakarta Sans';
            ctx.fillText('🚜 Pelle Liebherr 24t (X=7.0m, Y=0.0m, Z=0.0m)', pelle.sx + 12, pelle.sy + 3);

            // 7. Scania 8x4 at (0, 4.5, 0)
            const scania = project3D(2, 4.5, 0, cx, cy);
            ctx.fillStyle = '#3b82f6';
            ctx.beginPath(); ctx.arc(scania.sx, scania.sy, 8, 0, Math.PI * 2); ctx.fill();
            ctx.strokeStyle = '#fff'; ctx.stroke();
            ctx.fillStyle = '#93c5fd'; ctx.fillText('🚛 Scania 8x4 (X=2.0m, Y=4.5m, Z=0.0m)', scania.sx + 10, scania.sy + 3);

            // 8. Drone DJI Matrice 350 RTK hovering at (24, 5.0, +10.0m)
            const drone = project3D(24, 5.0, 10.0, cx, cy);
            const groundProj = project3D(24, 5.0, 0, cx, cy);

            // LiDAR 3D Cone
            ctx.fillStyle = 'rgba(16, 185, 129, 0.15)';
            ctx.beginPath();
            ctx.moveTo(drone.sx, drone.sy);
            const cL1 = project3D(18, 0, 0, cx, cy);
            const cL2 = project3D(30, 10, 0, cx, cy);
            ctx.lineTo(cL1.sx, cL1.sy);
            ctx.lineTo(cL2.sx, cL2.sy);
            ctx.closePath(); ctx.fill();

            // Drone Symbol
            ctx.fillStyle = '#06b6d4';
            ctx.beginPath(); ctx.arc(drone.sx, drone.sy, 7, 0, Math.PI * 2); ctx.fill();
            ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke();
            ctx.fillStyle = '#38bdf8'; ctx.font = 'bold 9px Plus Jakarta Sans';
            ctx.fillText('🛸 Drone DJI M350 LiDAR (X=24m, Y=5m, Z=+10.0m)', drone.sx + 10, drone.sy - 3);

            // 9. Exoskeleton Worker HAPO BTP at (15, -1.8, 0)
            const exoW = project3D(15, -1.8, 0, cx, cy);
            ctx.fillStyle = '#10b981';
            ctx.beginPath(); ctx.arc(exoW.sx, exoW.sy, 6, 0, Math.PI * 2); ctx.fill();
            ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke();
            ctx.fillStyle = '#a7f3d0'; ctx.font = '8px Plus Jakarta Sans';
            ctx.fillText('🦾 F. Roche (Exosquelette HAPO X=15m, Y=-1.8m, Z=0.0m)', exoW.sx + 8, exoW.sy + 3);

            // 10. OPBTP Signs at X = -15m, X = -5m, X = 0m
            const sAK5 = project3D(0, -4.0, 0, cx, cy);
            ctx.fillStyle = '#f59e0b';
            ctx.beginPath(); ctx.arc(sAK5.sx, sAK5.sy, 5, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#fde68a'; ctx.font = '8px Plus Jakarta Sans';
            ctx.fillText('🦺 Balisage OPBTP AK5/KR11J (X=0.0m)', sAK5.sx + 8, sAK5.sy + 3);

        } else if (scenId === 'scen_giratoire_enrobes') {
            // Giratoire Layers in 3D:
            // 1. Layer PST Chaux (Z: -0.40 to -0.20m)
            const l1_a = project3D(0, -5, -0.20, cx, cy);
            const l1_b = project3D(50, -5, -0.20, cx, cy);
            const l1_c = project3D(50, 5, -0.20, cx, cy);
            const l1_d = project3D(0, 5, -0.20, cx, cy);
            ctx.fillStyle = 'rgba(217, 119, 6, 0.25)';
            ctx.beginPath(); ctx.moveTo(l1_a.sx, l1_a.sy); ctx.lineTo(l1_b.sx, l1_b.sy); ctx.lineTo(l1_c.sx, l1_c.sy); ctx.lineTo(l1_d.sx, l1_d.sy); ctx.closePath(); ctx.fill();

            // 2. Layer GNT 0/31.5 (25cm, Z: -0.20 to 0.00m)
            const l2_a = project3D(0, -4, 0, cx, cy);
            const l2_b = project3D(50, -4, 0, cx, cy);
            const l2_c = project3D(50, 4, 0, cx, cy);
            const l2_d = project3D(0, 4, 0, cx, cy);
            ctx.fillStyle = 'rgba(100, 116, 139, 0.35)';
            ctx.beginPath(); ctx.moveTo(l2_a.sx, l2_a.sy); ctx.lineTo(l2_b.sx, l2_b.sy); ctx.lineTo(l2_c.sx, l2_c.sy); ctx.lineTo(l2_d.sx, l2_d.sy); ctx.closePath(); ctx.fill();
            ctx.strokeStyle = '#94a3b8'; ctx.stroke();

            // 3. Layer BBSG 0/10 (6cm, Z: 0.00 to +0.06m)
            const l3_a = project3D(20, -3.5, 0.06, cx, cy);
            const l3_b = project3D(50, -3.5, 0.06, cx, cy);
            const l3_c = project3D(50, 3.5, 0.06, cx, cy);
            const l3_d = project3D(20, 3.5, 0.06, cx, cy);
            ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
            ctx.beginPath(); ctx.moveTo(l3_a.sx, l3_a.sy); ctx.lineTo(l3_b.sx, l3_b.sy); ctx.lineTo(l3_c.sx, l3_c.sy); ctx.lineTo(l3_d.sx, l3_d.sy); ctx.closePath(); ctx.fill();
            ctx.strokeStyle = '#38bdf8'; ctx.stroke();

            // Machines: Compacteur Bomag at (25, 0, 0)
            const bomag = project3D(25, 0, 0, cx, cy);
            ctx.fillStyle = '#10b981'; ctx.beginPath(); ctx.arc(bomag.sx, bomag.sy, 8, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#a7f3d0'; ctx.font = 'bold 9px Plus Jakarta Sans';
            ctx.fillText('🔨 Compacteur Bomag BW213 (X=25m, Y=0m, Z=0.0m)', bomag.sx + 10, bomag.sy + 3);

            // Finisseur Dynapac at (42, 0, +0.06m)
            const fin = project3D(42, 0, 0.06, cx, cy);
            ctx.fillStyle = '#f59e0b'; ctx.beginPath(); ctx.arc(fin.sx, fin.sy, 9, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#fde68a'; ctx.fillText('🛣️ Finisseur Dynapac SD2500 (X=42m, Y=0m, Z=+0.06m)', fin.sx + 11, fin.sy + 3);

            // Station Totale Leica iCON 70 at (5, -7, 0) with red laser beam
            const topo = project3D(5, -7, 0, cx, cy);
            ctx.fillStyle = '#a855f7'; ctx.beginPath(); ctx.arc(topo.sx, topo.sy, 6, 0, Math.PI * 2); ctx.fill();
            ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 1; ctx.setLineDash([2, 2]);
            ctx.beginPath(); ctx.moveTo(topo.sx, topo.sy); ctx.lineTo(fin.sx, fin.sy); ctx.stroke();
            ctx.setLineDash([]);
            ctx.fillStyle = '#c084fc'; ctx.fillText('📐 Guidage Topo 3D Leica iCON 70 (X=5m, Y=-7m, Z=0.0m)', topo.sx + 8, topo.sy + 3);

        } else if (scenId === 'scen_bordures_trottoir') {
            // Bordures T2 Alignment along Y = -3.5m (X: 5..45m, Z: 0..+0.28m)
            const bStart = project3D(5, -3.5, 0.14, cx, cy);
            const bEnd = project3D(45, -3.5, 0.14, cx, cy);
            ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 5;
            ctx.beginPath(); ctx.moveTo(bStart.sx, bStart.sy); ctx.lineTo(bEnd.sx, bEnd.sy); ctx.stroke();
            ctx.fillStyle = '#38bdf8'; ctx.font = 'bold 9px JetBrains Mono';
            ctx.fillText('📐 Alignement Bordures T2 (Y=-3.5m, Z=+0.14m)', bStart.sx + 6, bStart.sy);

            // Minipelle Kubota KX057 at (12, -1.5, 0)
            const mini = project3D(12, -1.5, 0, cx, cy);
            ctx.fillStyle = '#f59e0b'; ctx.beginPath(); ctx.arc(mini.sx, mini.sy, 7, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#fde68a'; ctx.font = '9px Plus Jakarta Sans';
            ctx.fillText('🚜 Minipelle Kubota KX057 (X=12m, Y=-1.5m, Z=0.0m)', mini.sx + 9, mini.sy + 3);

            // Worker equipped with Exoskeleton HAPO BTP at (18, -3.5, 0)
            const poseur = project3D(18, -3.5, 0, cx, cy);
            ctx.fillStyle = '#10b981'; ctx.beginPath(); ctx.arc(poseur.sx, poseur.sy, 6, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#a7f3d0';
            ctx.fillText('🦾 F. Roche (Exosquelette Lombaire HAPO Pose Bordure)', poseur.sx + 8, poseur.sy + 3);
        }

        // Header Label Overlay
        ctx.fillStyle = '#38bdf8';
        ctx.font = 'bold 11px JetBrains Mono';
        ctx.textAlign = 'center';
        ctx.fillText('🧊 ENVIRONNEMENT 3D THÉORIQUE & GRILLE XYZ MÉTRIQUE', cx, 25);
    }

    // ----------------------------------------------------
    // 3. UPDATE THEORETICAL XYZ COORDINATES TABLE
    // ----------------------------------------------------
    function update3DCoordsTable(scenId) {
        const table = document.getElementById('sim-3d-coords-table');
        if (!table) return;

        let rows = [];
        if (scenId === 'scen_tranchee_vrd') {
            rows = [
                { name: 'Pelle Chenilles Liebherr 24t', cat: 'Engin', x: '7.00 m', y: '0.00 m', z: '0.00 m', role: 'Terrassement fouille & blindage', alert: '🟢 Sécurité OK' },
                { name: 'Collecteur Fonte DN400', cat: 'Réseau', x: '10.00 → 38.00 m', y: '0.00 m', z: '-1.80 m', role: 'Pente théorique -1.50%', alert: '💧 Laser Piper actif' },
                { name: 'Blindage Caisson SBH', cat: 'Sécurité', x: '14.00 → 32.00 m', y: '±0.90 m', z: '0.00 → -2.40 m', role: 'Protection éboulement tranchée', alert: '🛡️ Conforme CCTP' },
                { name: 'Conduite Gaz MPB 4 bars', cat: 'Réseau DICT', x: '0.00 → 50.00 m', y: '+2.50 m', z: '-1.00 m', role: 'Zone sensible AIPR Classe A', alert: '⚠️ DLA 3.00m obligatoire' },
                { name: 'Ligne Aérienne 20 kV HTA', cat: 'Réseau Élec', x: '0.00 → 50.00 m', y: '-6.00 m', z: '+7.50 m', role: 'Surveillance gabarit flèche', alert: '🔴 DLA 3.00m respectée' },
                { name: 'Drone DJI Matrice 350 RTK', cat: 'Vecteur Topo', x: '24.00 m', y: '+5.00 m', z: '+10.00 m', role: 'Cartographie LiDAR & MNT 3D', alert: '🛸 Télépilote DGAC actif' },
                { name: 'Compagnon Exosquelette HAPO', cat: 'Humain / EPI', x: '15.00 m', y: '-1.80 m', z: '0.00 m', role: 'Manutention tuyaux & calage', alert: '🦾 Assistance -14kg' }
            ];
        } else if (scenId === 'scen_giratoire_enrobes') {
            rows = [
                { name: 'Finisseur Enrobé Dynapac', cat: 'Engin', x: '42.00 m', y: '0.00 m', z: '+0.06 m', role: 'Application BBSG 0/10 160°C', alert: '🛣️ Température validée' },
                { name: 'Compacteur Bomag BW213', cat: 'Engin', x: '25.00 m', y: '0.00 m', z: '0.00 m', role: 'Compactage GNT 0/31.5 (EV2>80)', alert: '🔨 Dynaplaque 110 MPa' },
                { name: 'Station Totale Leica iCON 70', cat: 'Topo 3D', x: '5.00 m', y: '-7.00 m', z: '0.00 m', role: 'Guidage laser centimétrique', alert: '📐 RGF93 CC43 OK' },
                { name: 'Drone DJI Matrice 350 RTK', cat: 'Vecteur Topo', x: '30.00 m', y: '0.00 m', z: '+12.00 m', role: 'Orthophoto d\\'avancement', alert: '🛸 Survol autorisé' }
            ];
        } else {
            rows = [
                { name: 'Alignement Bordures T2', cat: 'Ouvrage', x: '5.00 → 45.00 m', y: '-3.50 m', z: '+0.14 m', role: 'Pose sur semelle C25/30', alert: '📐 Pente 2.0% OK' },
                { name: 'Minipelle Kubota KX057', cat: 'Engin', x: '12.00 m', y: '-1.50 m', z: '0.00 m', role: 'Approvisionnement béton', alert: '🚜 CACES A validé' },
                { name: 'Poseur Exosquelette HAPO', cat: 'Compagnon', x: '18.00 m', y: '-3.50 m', z: '0.00 m', role: 'Pose manuelle avec pince', alert: '🦾 Décharge vertébrale' }
            ];
        }

        table.innerHTML = `
            <thead>
                <tr style="color:var(--cyan); border-bottom:1px solid var(--border); text-align:left;">
                    <th style="padding:4px 6px;">Élément / Matériel</th>
                    <th style="padding:4px 6px;">Catégorie</th>
                    <th style="padding:4px 6px;">X (Longitudinal)</th>
                    <th style="padding:4px 6px;">Y (Transversal)</th>
                    <th style="padding:4px 6px;">Z (Altimétrie)</th>
                    <th style="padding:4px 6px;">Rôle Théorique</th>
                    <th style="padding:4px 6px;">Statut</th>
                </tr>
            </thead>
            <tbody>
                ${rows.map(r => `
                    <tr style="border-bottom:1px solid rgba(51,65,85,0.3); color:var(--text-main);">
                        <td style="padding:4px 6px; font-weight:700;">${r.name}</td>
                        <td style="padding:4px 6px; color:var(--cyan);">${r.cat}</td>
                        <td style="padding:4px 6px; color:#ef4444;">${r.x}</td>
                        <td style="padding:4px 6px; color:#10b981;">${r.y}</td>
                        <td style="padding:4px 6px; color:#38bdf8;">${r.z}</td>
                        <td style="padding:4px 6px; color:var(--text-muted);">${r.role}</td>
                        <td style="padding:4px 6px;">${r.alert}</td>
                    </tr>
                `).join('')}
            </tbody>
        `;
    }

"""

code = code[:idx_radar] + new_radar_js + code[idx_catalog:]

with open(TARGET, "w", encoding="utf-8") as f:
    f.write(code)

print("Applied 2D Satellite & 3D Theoretical Grid logic to build_html_dashboard.py successfully!")
