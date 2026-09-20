# -*- coding: utf-8 -*-

def get_js_part2():
    return r"""
    // ==========================================
    // 7. WATCH TOWER, 4D SIMULATION & GOD'S EYE
    // ==========================================
    const simulationScenarios = {
        'scen_tranchee_vrd': {
            id: 'scen_tranchee_vrd',
            title: '1. Tranchée Assainissement & Blindage Profond (3.20m)',
            desc: 'Pose de collecteur Béton Ø400 135A sous nappe phréatique avec rabattement et caisson de blindage acier.',
            steps: [
                { title: '1. Piquetage DICT 7 Couleurs & Traçage', details: 'Détection géoradar, marquage au sol de la conduite Gaz MPB PEHD 110 et câble HTA 20kV. Pose des panneaux AK5 et cônes K5a.', mach: 'Scie Diamant Stihl, Détecteur RD8100', progress: 100 },
                { title: '2. Découpe Enrobés & Terrassement Fouille', details: 'Sciage chaussée ép. 15cm. Terrassement en pleine masse à la pelle Liebherr 24t. Évacuation déblais par camion 8x4.', mach: 'Pelle 24t R924, Camion Scania 8x4', progress: 100 },
                { title: '3. Descente Caisson de Blindage Lourd R4534', details: 'Mise en fiche des caissons acier 3.50m x 2.40m au godet de terrassement. Vérification étaiement hydraulique et absence de personnel sous charge.', mach: 'Pelle R924, Caisson Krings 3.5m', progress: 85 },
                { title: '4. Réglage Lit de Pose Sable 4/10 au Laser', details: 'Mise en place de 15cm de sable concassé. Nivellement avec laser canalisateur Piper 200 à pente 1.45% avec mire réceptrice.', mach: 'Laser Canalisateur Leica Piper 200', progress: 60 },
                { title: '5. Descente & Emboîtement Tuyaux Béton Ø400', details: 'Élingage au crochet de sécurité, graissage des joints toriques élastomère et emboîtement au tire-fort hydraulique.', mach: 'Pelle R924, Élingues 2 brins CMU 3T', progress: 30 },
                { title: '6. Remblaiement Méthodique & Compactage Q4', details: 'Enrobage sable jusqu\'à 30cm au-dessus de la génératrice supérieure. Remblai GNT 0/31.5 par passes de 30cm au pilonneur.', mach: 'Pilonneuse Wacker BS60, Compacteur V3', progress: 0 }
            ]
        },
        'scen_enrobes_chaud': {
            id: 'scen_enrobes_chaud',
            title: '2. Mise en Œuvre Enrobés Chauds BBSG 0/10',
            desc: 'Application d\'une couche de roulement en BBSG 0/10 classe 3 à 160°C sur 1200 m² de chaussée urbaine.',
            steps: [
                { title: '1. Balayage Mécanique & Dépoussiérage', details: 'Aspiration et brossage haute pression sur la couche de base GB 0/14.', mach: 'Balayeuse Aspiratrice Ravo 540', progress: 100 },
                { title: '2. Répandage Émulsion d\'Accrochage C65B4', details: 'Dosage précis à 350 g/m² de bitume résiduel à la rampe automatique.', mach: 'Bouille à bitume hydrostatique', progress: 100 },
                { title: '3. Guidage Finisseur & Alimentation Camions', details: 'Alimentation continue de la trémie sans à-coups par rotation des camions bâchés.', mach: 'Finisseur Vögele Super 1800-3i', progress: 75 },
                { title: '4. Compactage Vibrant Tandem & Finition Gomme', details: '6 passes au rouleau tandem double bille vibrant suivies de 4 passes au compacteur à pneus.', mach: 'Compacteur Bomag BW 154, Pneu Hamm', progress: 40 },
                { title: '5. Sciage Joints de Raccordement & Mastic', details: 'Découpe franche des raccords transversaux et application de mastic bitumineux à chaud.', mach: 'Scie diamant, Chaudière à mastic', progress: 0 }
            ]
        },
        'scen_carrefour_giratoire': {
            id: 'scen_carrefour_giratoire',
            title: '3. Carrefour Giratoire Urbain sous Circulation',
            desc: 'Aménagement d\'un rond-point à 4 branches avec alternat temporaire et îlot central décoratif.',
            steps: [
                { title: '1. Phase 1 : Neutralisation Demi-Chaussée Ouest', details: 'Pose de séparateurs de voies K16 et feux tricolores d\'alternat KR11.', mach: 'Fourgon Balisage, Feux KR11 Sync', progress: 100 },
                { title: '2. Décaissement & Fondation GNT 0/31.5', details: 'Terrassement plateforme et réglage de 30cm de grave traitée au guidage 3D.', mach: 'Niveleuse Cat 140M GPS, Cylindre V5', progress: 90 },
                { title: '3. Pose Bordures T2 & Caniveaux CC1', details: 'Calage au béton dosé à 250 kg/m³ avec joints de dilatation tous les 10m.', mach: 'Pince à bordure ventouse, Bétonnière', progress: 65 },
                { title: '4. Coulage Anneau Pavé & Béton Désactivé', details: 'Coulage dalle béton C30/37 avec pulvérisation de désactivant et lavage HP.', mach: 'Camion malaxeur, Nettoyeur HP 200 bar', progress: 20 },
                { title: '5. Bascule Phase 2 & Couche BBSG Finale', details: 'Inversion de la circulation et tapis d\'enrobé continu sur l\'ensemble de l\'anneau.', mach: 'Finisseur Vögele, Compacteur Bomag', progress: 0 }
            ]
        }
    };

    function loadScenario(scenId) {
        currentScenarioId = scenId;
        activeScenarioStepIdx = 0;
        const scen = simulationScenarios[scenId] || simulationScenarios['scen_tranchee_vrd'];

        const card = document.getElementById('scenario-info-card');
        if (card) {
            card.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <span class="badge badge-info" style="font-size:0.7rem; font-family:'JetBrains Mono';">${scen.id}</span>
                        <h4 style="font-size:1.05rem; font-weight:800; color:#38bdf8; margin-top:3px;">${scen.title}</h4>
                        <p style="font-size:0.8rem; color:#cbd5e1; margin-top:4px; line-height:1.4;">${scen.desc}</p>
                    </div>
                </div>
            `;
        }

        renderScenarioStepsList();
        showStepDetails(0);
        drawStepVisual(0);
        logCockpit(`Scénario Watchtower chargé : ${scen.title}`, 'info');
    }

    function renderScenarioStepsList() {
        const scen = simulationScenarios[currentScenarioId] || simulationScenarios['scen_tranchee_vrd'];
        const list = document.getElementById('scenario-steps-list');
        if (!list) return;

        list.innerHTML = scen.steps.map((st, idx) => `
            <div onclick="selectScenarioStep(${idx})" style="background: ${idx === activeScenarioStepIdx ? 'rgba(56, 189, 248, 0.2)' : 'rgba(15, 23, 42, 0.7)'}; border: 1px solid ${idx === activeScenarioStepIdx ? '#38bdf8' : 'rgba(51, 65, 85, 0.6)'}; border-left: 4px solid ${idx === activeScenarioStepIdx ? '#38bdf8' : (st.progress === 100 ? '#10b981' : '#64748b')}; padding: 0.6rem; border-radius: 6px; margin-bottom: 0.4rem; cursor: pointer; transition: all 0.15s;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 0.8rem; font-weight: 800; color: ${idx === activeScenarioStepIdx ? '#38bdf8' : '#f8fafc'};">${st.title}</span>
                    <span class="badge ${st.progress === 100 ? 'badge-success' : (st.progress > 0 ? 'badge-info' : 'badge-warning')}" style="font-size: 0.65rem;">${st.progress}%</span>
                </div>
                <div style="font-size: 0.7rem; color: #94a3b8; margin-top: 2px;">🚜 ${st.mach}</div>
            </div>
        `).join('');
    }

    function selectScenarioStep(idx) {
        activeScenarioStepIdx = idx;
        renderScenarioStepsList();
        showStepDetails(idx);
        drawStepVisual(idx);

        const phaseLabel = document.getElementById('sim-4d-phase-label');
        if (phaseLabel) {
            const scen = simulationScenarios[currentScenarioId] || simulationScenarios['scen_tranchee_vrd'];
            phaseLabel.textContent = `ÉTAPE ${idx + 1}/${scen.steps.length} : ${(scen.steps[idx]?.title || '').toUpperCase()}`;
        }
    }

    function prevScenarioStep() {
        const scen = simulationScenarios[currentScenarioId] || simulationScenarios['scen_tranchee_vrd'];
        if (activeScenarioStepIdx > 0) selectScenarioStep(activeScenarioStepIdx - 1);
    }

    function nextScenarioStep() {
        const scen = simulationScenarios[currentScenarioId] || simulationScenarios['scen_tranchee_vrd'];
        if (activeScenarioStepIdx < scen.steps.length - 1) selectScenarioStep(activeScenarioStepIdx + 1);
        else selectScenarioStep(0);
    }

    function showStepDetails(idx) {
        const scen = simulationScenarios[currentScenarioId] || simulationScenarios['scen_tranchee_vrd'];
        const st = scen.steps[idx];
        const box = document.getElementById('step-details-box');
        if (!box || !st) return;

        box.innerHTML = `
            <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.7); border-radius: 8px; padding: 0.85rem;">
                <div style="font-size: 0.85rem; font-weight: 800; color: #38bdf8; margin-bottom: 4px;">🔍 Prescriptions Opérationnelles : ${st.title}</div>
                <div style="font-size: 0.8rem; color: #cbd5e1; line-height: 1.5; margin-bottom: 6px;">${st.details}</div>
                <div style="font-size: 0.75rem; color: var(--amber); font-weight: 700;">🚜 Matériel : ${st.mach}</div>
            </div>
        `;
    }

    function setSimulatorViewMode(mode) {
        simulatorViewMode = mode;
        document.querySelectorAll('.sim-view-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('btn-sim-' + mode)?.classList.add('active');

        const radarCont = document.getElementById('radar-canvas-container');
        const view3dCont = document.getElementById('view3d-canvas-container');
        const standardLayout = document.getElementById('sim-standard-layout');
        const globalLayout = document.getElementById('sim-global-layout');

        if (mode === 'global') {
            if (standardLayout) standardLayout.style.display = 'none';
            if (globalLayout) globalLayout.style.display = 'block';
            setTimeout(renderGodsEyeCanvas, 50);
        } else {
            if (standardLayout) standardLayout.style.display = 'grid';
            if (globalLayout) globalLayout.style.display = 'none';

            if (mode === 'radar') {
                if (radarCont) radarCont.style.display = 'block';
                if (view3dCont) view3dCont.style.display = 'none';
                setTimeout(initWatchtowerRadar, 50);
            } else {
                if (radarCont) radarCont.style.display = 'none';
                if (view3dCont) view3dCont.style.display = 'block';
                setTimeout(() => {
                    init3DCanvas();
                    drawStepVisual(activeScenarioStepIdx);
                }, 50);
            }
        }
    }

    function toggleRadarLiveMode() {
        isRadarLive = !isRadarLive;
        const btn = document.getElementById('btn-radar-toggle');
        if (btn) {
            btn.textContent = isRadarLive ? '🟢 Signal Direct' : '⏸️ Signal Figé';
            btn.className = isRadarLive ? 'btn btn-secondary' : 'btn btn-warning';
        }
    }

    function togglePlay4DSimulation() {
        is4DSimPlaying = !is4DSimPlaying;
        const btn = document.getElementById('btn-play-4d-sim');

        if (is4DSimPlaying) {
            if (btn) btn.innerHTML = '⏸️ Pause Simulation 4D';
            if (simulatorViewMode !== '3d') setSimulatorViewMode('3d');
            
            sim4DInterval = setInterval(() => {
                nextScenarioStep();
            }, 2500);
            logCockpit('Simulation 4D animée démarrée en continu.', 'ok');
        } else {
            if (btn) btn.innerHTML = '▶️ Lancer Simulation 4D';
            if (sim4DInterval) clearInterval(sim4DInterval);
            logCockpit('Simulation 4D mise en pause.', 'info');
        }
    }

    // 2D RADAR ANIMATION
    let radarAngle = 0;
    function initWatchtowerRadar() {
        radarCanvas = document.getElementById('watchtower-radar-canvas');
        if (!radarCanvas) return;
        radarCtx = radarCanvas.getContext('2d');
        const w = radarCanvas.parentElement.clientWidth || 500;
        const h = radarCanvas.parentElement.clientHeight || 400;
        radarCanvas.width = w;
        radarCanvas.height = h;

        if (radarAnimId) cancelAnimationFrame(radarAnimId);
        animateRadar();
    }

    function animateRadar() {
        if (!radarCanvas || !radarCtx) return;
        const w = radarCanvas.width;
        const h = radarCanvas.height;
        const cx = w / 2;
        const cy = h / 2;
        const maxR = Math.min(cx, cy) - 20;

        radarCtx.fillStyle = 'rgba(9, 13, 22, 0.2)';
        radarCtx.fillRect(0, 0, w, h);

        // Concentric Rings
        radarCtx.strokeStyle = 'rgba(56, 189, 248, 0.25)';
        radarCtx.lineWidth = 1;
        for (let r = maxR / 4; r <= maxR; r += maxR / 4) {
            radarCtx.beginPath();
            radarCtx.arc(cx, cy, r, 0, Math.PI * 2);
            radarCtx.stroke();
        }

        // Crosshairs
        radarCtx.beginPath();
        radarCtx.moveTo(cx, cy - maxR); radarCtx.lineTo(cx, cy + maxR);
        radarCtx.moveTo(cx - maxR, cy); radarCtx.lineTo(cx + maxR, cy);
        radarCtx.stroke();

        // Sweep Line
        if (isRadarLive) radarAngle += 0.03;
        radarCtx.strokeStyle = 'rgba(56, 189, 248, 0.8)';
        radarCtx.lineWidth = 2;
        radarCtx.beginPath();
        radarCtx.moveTo(cx, cy);
        radarCtx.lineTo(cx + Math.cos(radarAngle) * maxR, cy + Math.sin(radarAngle) * maxR);
        radarCtx.stroke();

        // Target Blips (Fleet Assets)
        const targets = [
            { label: 'PELLE-R924', dist: 0.45, ang: 1.2, color: '#f59e0b' },
            { label: 'CAMION-8X4', dist: 0.7, ang: 2.8, color: '#38bdf8' },
            { label: 'COMPACTEUR-V5', dist: 0.3, ang: 4.5, color: '#10b981' },
            { label: 'DRONE-LIDAR', dist: 0.85, ang: 5.6, color: '#c084fc' }
        ];

        targets.forEach(t => {
            const tx = cx + Math.cos(t.ang) * (maxR * t.dist);
            const ty = cy + Math.sin(t.ang) * (maxR * t.dist);

            radarCtx.fillStyle = t.color;
            radarCtx.beginPath();
            radarCtx.arc(tx, ty, 5, 0, Math.PI * 2);
            radarCtx.fill();

            radarCtx.font = 'bold 9px monospace';
            radarCtx.fillStyle = '#f8fafc';
            radarCtx.fillText(t.label, tx + 8, ty + 3);
        });

        // HUD Text
        radarCtx.font = 'bold 10px monospace';
        radarCtx.fillStyle = 'var(--emerald)';
        radarCtx.fillText(`TÉLÉMÉTRIE RTK : ACTIF (${targets.length} BALISES)`, 15, 20);
        radarCtx.fillText(`RAYON SURVEILLANCE : 250m`, 15, 35);

        if (simulatorViewMode === 'radar') {
            radarAnimId = requestAnimationFrame(animateRadar);
        }
    }

    // 3D / 4D SIMULATION ENGINE CANVAS
    let canvas3D, ctx3D;
    function init3DCanvas() {
        canvas3D = document.getElementById('watchtower-3d-canvas');
        if (!canvas3D) return;
        ctx3D = canvas3D.getContext('2d');
        const w = canvas3D.parentElement.clientWidth || 600;
        const h = canvas3D.parentElement.clientHeight || 400;
        canvas3D.width = w;
        canvas3D.height = h;

        canvas3D.onmousedown = (e) => {
            isDragging3D = true;
            lastMouseX = e.clientX;
            lastMouseY = e.clientY;
        };
        window.onmouseup = () => { isDragging3D = false; };
        window.onmousemove = (e) => {
            if (!isDragging3D) return;
            const dx = e.clientX - lastMouseX;
            const dy = e.clientY - lastMouseY;
            cameraRotY += dx * 0.5;
            cameraRotX += dy * 0.5;
            lastMouseX = e.clientX;
            lastMouseY = e.clientY;
            drawStepVisual(activeScenarioStepIdx);
        };
    }

    function set3DPreset(mode) {
        if (mode === 'top') { cameraRotX = 90; cameraRotY = 0; }
        if (mode === 'iso') { cameraRotX = 30; cameraRotY = -45; }
        drawStepVisual(activeScenarioStepIdx);
    }

    function zoom3D(factor) {
        cameraZoom *= factor;
        drawStepVisual(activeScenarioStepIdx);
    }

    function drawStepVisual(stepIdx) {
        if (!canvas3D || !ctx3D) {
            canvas3D = document.getElementById('watchtower-3d-canvas');
            if (canvas3D) ctx3D = canvas3D.getContext('2d');
            else return;
        }

        const w = canvas3D.width;
        const h = canvas3D.height;
        const cx = w / 2;
        const cy = h / 2 + 20;

        ctx3D.fillStyle = '#090d16';
        ctx3D.fillRect(0, 0, w, h);

        ctx3D.save();
        ctx3D.translate(cx, cy);
        ctx3D.scale(cameraZoom, cameraZoom);

        // Ground Plane Grid in Isometric View
        const radY = (cameraRotY * Math.PI) / 180;
        const radX = (cameraRotX * Math.PI) / 180;

        function project3D(x, y, z) {
            const cosY = Math.cos(radY), sinY = Math.sin(radY);
            const x1 = x * cosY - z * sinY;
            const z1 = x * sinY + z * cosY;

            const cosX = Math.cos(radX), sinX = Math.sin(radX);
            const y2 = y * cosX - z1 * sinX;
            const z2 = y * sinX + z1 * cosX;

            return { px: x1, py: y2, depth: z2 };
        }

        // Draw Ground Grid
        ctx3D.strokeStyle = 'rgba(51, 65, 85, 0.4)';
        ctx3D.lineWidth = 1;
        const gridSize = 180, gridStep = 30;

        for (let x = -gridSize; x <= gridSize; x += gridStep) {
            const p1 = project3D(x, 0, -gridSize);
            const p2 = project3D(x, 0, gridSize);
            ctx3D.beginPath(); ctx3D.moveTo(p1.px, p1.py); ctx3D.lineTo(p2.px, p2.py); ctx3D.stroke();
        }
        for (let z = -gridSize; z <= gridSize; z += gridStep) {
            const p1 = project3D(-gridSize, 0, z);
            const p2 = project3D(gridSize, 0, z);
            ctx3D.beginPath(); ctx3D.moveTo(p1.px, p1.py); ctx3D.lineTo(p2.px, p2.py); ctx3D.stroke();
        }

        // 1. Excavation Trench (Tranchée)
        const tLen = 140, tWidth = 35, tDepth = 45;
        const c1 = project3D(-tLen, 0, -tWidth);
        const c2 = project3D(tLen, 0, -tWidth);
        const c3 = project3D(tLen, 0, tWidth);
        const c4 = project3D(-tLen, 0, tWidth);

        const b1 = project3D(-tLen, tDepth, -tWidth);
        const b2 = project3D(tLen, tDepth, -tWidth);
        const b3 = project3D(tLen, tDepth, tWidth);
        const b4 = project3D(-tLen, tDepth, tWidth);

        // Trench Bottom
        ctx3D.fillStyle = '#1e1b18';
        ctx3D.beginPath();
        ctx3D.moveTo(b1.px, b1.py); ctx3D.lineTo(b2.px, b2.py); ctx3D.lineTo(b3.px, b3.py); ctx3D.lineTo(b4.px, b4.py);
        ctx3D.closePath(); ctx3D.fill();

        // Trench Walls
        ctx3D.fillStyle = '#292524';
        ctx3D.beginPath();
        ctx3D.moveTo(c1.px, c1.py); ctx3D.lineTo(c2.px, c2.py); ctx3D.lineTo(b2.px, b2.py); ctx3D.lineTo(b1.px, b1.py);
        ctx3D.closePath(); ctx3D.fill();

        // 2. Trench Shield (Caisson de Blindage) if step >= 2
        if (stepIdx >= 2) {
            ctx3D.fillStyle = 'rgba(234, 179, 8, 0.75)';
            ctx3D.strokeStyle = '#b45309';
            ctx3D.lineWidth = 2;
            const sh1 = project3D(-60, 5, -tWidth + 2);
            const sh2 = project3D(60, 5, -tWidth + 2);
            const sh3 = project3D(60, tDepth - 5, -tWidth + 2);
            const sh4 = project3D(-60, tDepth - 5, -tWidth + 2);
            ctx3D.beginPath(); ctx3D.moveTo(sh1.px, sh1.py); ctx3D.lineTo(sh2.px, sh2.py); ctx3D.lineTo(sh3.px, sh3.py); ctx3D.lineTo(sh4.px, sh4.py);
            ctx3D.closePath(); ctx3D.fill(); ctx3D.stroke();
        }

        // 3. Pipe (Tuyau Béton Ø400) if step >= 3
        if (stepIdx >= 3) {
            ctx3D.strokeStyle = '#38bdf8';
            ctx3D.lineWidth = 8;
            const pp1 = project3D(-120, tDepth - 10, 0);
            const pp2 = project3D(120, tDepth - 10, 0);
            ctx3D.beginPath(); ctx3D.moveTo(pp1.px, pp1.py); ctx3D.lineTo(pp2.px, pp2.py); ctx3D.stroke();

            // Laser Beam (Vert Fluo)
            ctx3D.strokeStyle = '#10b981';
            ctx3D.lineWidth = 2;
            ctx3D.setLineDash([4, 4]);
            const lz1 = project3D(-130, tDepth - 12, 0);
            const lz2 = project3D(130, tDepth - 12, 0);
            ctx3D.beginPath(); ctx3D.moveTo(lz1.px, lz1.py); ctx3D.lineTo(lz2.px, lz2.py); ctx3D.stroke();
            ctx3D.setLineDash([]);
        }

        // 4. Heavy Excavator Pelle Liebherr R924 Position
        const pellePos = project3D(90 + (stepIdx * 5), -20, 70);
        ctx3D.fillStyle = '#f59e0b';
        ctx3D.beginPath(); ctx3D.arc(pellePos.px, pellePos.py, 16, 0, Math.PI * 2); ctx3D.fill();
        ctx3D.strokeStyle = '#b45309'; ctx3D.lineWidth = 3; ctx3D.stroke();
        ctx3D.fillStyle = '#fff'; ctx3D.font = 'bold 9px monospace';
        ctx3D.fillText('🚜 R924', pellePos.px - 16, pellePos.py - 20);

        // 5. Hardhat Workers (Compagnons VRD)
        const worker1 = project3D(-20, tDepth - 15, 5);
        ctx3D.fillStyle = '#facc15';
        ctx3D.beginPath(); ctx3D.arc(worker1.px, worker1.py, 6, 0, Math.PI * 2); ctx3D.fill();
        ctx3D.fillStyle = '#fff'; ctx3D.font = 'bold 8px monospace';
        ctx3D.fillText('👷 M. Traoré', worker1.px - 20, worker1.py - 8);

        ctx3D.restore();

        // 2D Compass / HUD
        ctx3D.font = 'bold 11px JetBrains Mono';
        ctx3D.fillStyle = '#38bdf8';
        ctx3D.fillText(`PERSPECTIVE 3D : AZIMUT ${Math.round(cameraRotY)}° • ÉLÉVATION ${Math.round(cameraRotX)}°`, 12, h - 15);
    }

    // GOD'S EYE / REGIONAL OCCITANIE MAP CANVAS
    function renderGodsEyeCanvas() {
        const canvas = document.getElementById('godseye-map-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const w = canvas.parentElement.clientWidth || 700;
        const h = canvas.parentElement.clientHeight || 350;
        canvas.width = w;
        canvas.height = h;

        ctx.fillStyle = '#050811';
        ctx.fillRect(0, 0, w, h);

        // Occitanie Regional Coastline & Road Network Simulation
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.2)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(w * 0.1, h * 0.85);
        ctx.bezierCurveTo(w * 0.4, h * 0.8, w * 0.7, h * 0.75, w * 0.95, h * 0.6);
        ctx.stroke();

        // Sites Nodes
        const sites = [
            { name: "Alès (Giratoire RD906)", x: w * 0.45, y: h * 0.25, status: "Actif", alerts: 0 },
            { name: "Montpellier (Voie Verte)", x: w * 0.55, y: h * 0.45, status: "Actif", alerts: 0 },
            { name: "Pézenas (Centre Ancien)", x: w * 0.35, y: h * 0.55, status: "Actif", alerts: 0 },
            { name: "Sète (ZAC Littoral)", x: w * 0.45, y: h * 0.7, status: "Actif", alerts: 0 }
        ];

        // Connection Web
        ctx.strokeStyle = 'rgba(16, 185, 129, 0.3)';
        ctx.lineWidth = 1;
        ctx.setLineDash([3, 3]);
        for (let i = 0; i < sites.length; i++) {
            for (let j = i + 1; j < sites.length; j++) {
                ctx.beginPath();
                ctx.moveTo(sites[i].x, sites[i].y);
                ctx.lineTo(sites[j].x, sites[j].y);
                ctx.stroke();
            }
        }
        ctx.setLineDash([]);

        // Render Sites Markers
        sites.forEach(s => {
            ctx.fillStyle = 'rgba(16, 185, 129, 0.2)';
            ctx.beginPath(); ctx.arc(s.x, s.y, 16, 0, Math.PI * 2); ctx.fill();

            ctx.fillStyle = '#10b981';
            ctx.beginPath(); ctx.arc(s.x, s.y, 6, 0, Math.PI * 2); ctx.fill();

            ctx.font = 'bold 10px system-ui';
            ctx.fillStyle = '#f8fafc';
            ctx.fillText(s.name, s.x + 10, s.y + 4);
        });
    }

    // ==========================================
    // 8. FLEET MACHINERY & VISUAL SWITCHER
    // ==========================================
    const fleetAssetsState = {};

    function filterFleet(type, btn) {
        fleetFilter = type;
        document.querySelectorAll('.fleet-filter-btn').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
        renderFleetGrid();
    }

    function switchFleetCardView(vehId, viewMode) {
        fleetAssetsState[vehId] = viewMode;
        renderFleetGrid();
    }

    function renderFleetGrid() {
        const grid = document.getElementById('fleet-grid');
        if (!grid) return;

        const fleet = companyData.fleet || [];
        const filtered = fleet.filter(v => {
            if (fleetFilter === 'all') return true;
            return (v.type || '').toLowerCase().includes(fleetFilter);
        });

        grid.innerHTML = filtered.map(v => {
            const currentView = fleetAssetsState[v.id] || 'schema';
            let visualContent = '';

            if (currentView === 'photo') {
                visualContent = `<img src="${v.photo_url || 'https://images.unsplash.com/photo-1578632767115-351597cf2477?w=800'}" alt="${v.name}" style="width:100%; height:180px; object-fit:cover; border-radius:6px; border:1px solid rgba(51,65,85,0.7);">`;
            } else if (currentView === 'cam') {
                visualContent = `
                    <div style="background:#000; height:180px; border-radius:6px; border:1px solid var(--cyan); position:relative; overflow:hidden; display:flex; flex-direction:column; align-items:center; justify-content:center;">
                        <div style="font-size:2rem; margin-bottom:4px;">📹</div>
                        <div style="font-size:0.75rem; font-weight:800; color:#38bdf8; font-family:'JetBrains Mono';">CAMÉRA CABINE FLUX DIRECT</div>
                        <div style="font-size:0.65rem; color:#94a3b8; font-family:'JetBrains Mono';">Signal 5G • 1080p 30fps • 42ms</div>
                        <div style="position:absolute; top:6px; left:6px; background:rgba(15,23,42,0.8); padding:2px 6px; border-radius:3px; font-size:0.65rem; color:var(--emerald); font-family:'JetBrains Mono';">● LIVE</div>
                    </div>
                `;
            } else if (currentView === 'diag') {
                visualContent = `
                    <div style="background:rgba(15,23,42,0.9); height:180px; border-radius:6px; border:1px solid rgba(51,65,85,0.8); padding:0.75rem; font-size:0.75rem; display:flex; flex-direction:column; justify-content:space-between;">
                        <div style="font-weight:800; color:#38bdf8;">⚙️ Diagnostic Télémétrique CAN-bus</div>
                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:4px; font-size:0.7rem;">
                            <div>Niveau Carburant : <strong style="color:var(--emerald);">84%</strong></div>
                            <div>Pression Huile : <strong style="color:var(--emerald);">4.2 bar</strong></div>
                            <div>Température Moteur : <strong style="color:var(--amber);">88°C</strong></div>
                            <div>Heures Totales : <strong>${v.hours} h</strong></div>
                        </div>
                        <div style="font-size:0.65rem; color:#94a3b8;">GPS: ${v.geoloc ? v.geoloc.lat + '°N, ' + v.geoloc.lng + '°E' : 'Occitanie'}</div>
                    </div>
                `;
            } else {
                visualContent = `<div style="height:180px; border-radius:6px; overflow:hidden;">${getVehicleSVG(v.type, v.name)}</div>`;
            }

            return `
                <div class="card" style="border: 1px solid rgba(51,65,85,0.8); background: rgba(15,23,42,0.95); display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <!-- VIEW SWITCHER BUTTONS -->
                        <div style="display: flex; gap: 0.25rem; margin-bottom: 0.5rem; flex-wrap: wrap;">
                            <button class="btn-secondary ${currentView === 'schema' ? 'active' : ''}" style="padding: 0.2rem 0.4rem; font-size: 0.65rem;" onclick="switchFleetCardView('${v.id}', 'schema')">📐 Schéma</button>
                            <button class="btn-secondary ${currentView === 'photo' ? 'active' : ''}" style="padding: 0.2rem 0.4rem; font-size: 0.65rem;" onclick="switchFleetCardView('${v.id}', 'photo')">📸 Photo HD</button>
                            <button class="btn-secondary ${currentView === 'cam' ? 'active' : ''}" style="padding: 0.2rem 0.4rem; font-size: 0.65rem;" onclick="switchFleetCardView('${v.id}', 'cam')">📹 Caméra</button>
                            <button class="btn-secondary ${currentView === 'diag' ? 'active' : ''}" style="padding: 0.2rem 0.4rem; font-size: 0.65rem;" onclick="switchFleetCardView('${v.id}', 'diag')">⚙️ Diag</button>
                        </div>

                        <!-- VISUAL DISPLAY -->
                        <div style="margin-bottom: 0.75rem;">
                            ${visualContent}
                        </div>

                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                            <div>
                                <span class="badge badge-info" style="font-size: 0.65rem; font-family: 'JetBrains Mono';">${v.id}</span>
                                <h3 style="font-size: 1rem; font-weight: 800; color: #f8fafc; margin-top: 2px;">${v.name}</h3>
                                <div style="font-size: 0.75rem; color: #94a3b8;">${v.type} • Immat: <strong>${v.immat || 'TP-340-FR'}</strong></div>
                            </div>
                            <span class="badge badge-success">${v.status || 'Opérationnel'}</span>
                        </div>

                        <!-- SPECS SUMMARY -->
                        <div style="background: rgba(30,41,59,0.5); padding: 0.5rem; border-radius: 6px; font-size: 0.75rem; display: grid; grid-template-columns: 1fr 1fr; gap: 4px; margin-bottom: 0.75rem;">
                            <div>Heures: <strong>${v.hours} h</strong></div>
                            <div>Affectation: <strong>${v.project}</strong></div>
                            <div>VGP: <strong style="color: var(--emerald);">${v.vgp}</strong></div>
                            <div>Prix: <strong style="color: var(--amber);">${(v.price || 150000).toLocaleString('fr-FR')} €</strong></div>
                        </div>
                    </div>

                    <button class="btn btn-primary" style="width: 100%; font-size: 0.8rem;" onclick="openVehicleModal('${v.id}')">
                        🔍 Spécifications & Télémétrie Complète
                    </button>
                </div>
            `;
        }).join('');
    }

    function openVehicleModal(vehId) {
        const vehicle = (companyData.fleet || []).find(v => v.id === vehId) || (companyData.fleet || [])[0];
        if (!vehicle) return;

        const body = document.getElementById('vehicle-modal-body');
        if (!body) return;

        body.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; border-bottom: 1px solid rgba(51,65,85,0.7); padding-bottom: 0.75rem;">
                <div>
                    <span class="badge badge-info" style="font-size: 0.75rem; font-family: 'JetBrains Mono';">${vehicle.id}</span>
                    <h2 style="font-size: 1.3rem; font-weight: 900; color: #38bdf8; margin-top: 4px;">${vehicle.name}</h2>
                    <div style="font-size: 0.85rem; color: #94a3b8;">${vehicle.type} • Immatriculation : <strong>${vehicle.immat || 'TP-340-FR'}</strong> • Constructeur : <strong>${vehicle.brand || 'Liebherr'}</strong></div>
                </div>
                <span class="badge badge-success" style="font-size: 0.85rem;">${vehicle.status || 'Opérationnel'}</span>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.25rem;">
                <!-- PHOTO HD & SVG -->
                <div>
                    <div style="font-size: 0.75rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-bottom: 4px;">Photo Réelle HD :</div>
                    <img src="${vehicle.photo_url || 'https://images.unsplash.com/photo-1578632767115-351597cf2477?w=800'}" alt="${vehicle.name}" style="width: 100%; height: 190px; object-fit: cover; border-radius: 6px; border: 1px solid rgba(51,65,85,0.8); margin-bottom: 0.75rem;">
                    
                    <div style="font-size: 0.75rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-bottom: 4px;">Schéma Vectoriel Coté :</div>
                    <div style="height: 140px; border-radius: 6px; overflow: hidden; border: 1px solid rgba(51,65,85,0.8);">
                        ${getVehicleSVG(vehicle.type, vehicle.name)}
                    </div>
                </div>

                <!-- COMPREHENSIVE TECH SPECS TABLE -->
                <div>
                    <div style="font-size: 0.75rem; font-weight: 800; color: #38bdf8; text-transform: uppercase; margin-bottom: 6px;">📋 Fiche Technique & Paramètres VGP :</div>
                    <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.6); border-radius: 6px;">
                        <tbody>
                            <tr style="border-bottom: 1px solid rgba(51,65,85,0.4);"><td style="padding: 6px 10px; color: #94a3b8;">Prix d'Acquisition :</td><td style="padding: 6px 10px; font-weight: 800; color: var(--amber);">${(vehicle.price || 150000).toLocaleString('fr-FR')} € HT</td></tr>
                            <tr style="border-bottom: 1px solid rgba(51,65,85,0.4);"><td style="padding: 6px 10px; color: #94a3b8;">Poids Opérationnel (PTAC) :</td><td style="padding: 6px 10px; font-weight: 800;">${vehicle.weight || '24 500 kg'}</td></tr>
                            <tr style="border-bottom: 1px solid rgba(51,65,85,0.4);"><td style="padding: 6px 10px; color: #94a3b8;">Dimensions (L x l x h) :</td><td style="padding: 6px 10px; font-weight: 800;">${vehicle.dimensions || '9.80m x 2.98m x 3.15m'}</td></tr>
                            <tr style="border-bottom: 1px solid rgba(51,65,85,0.4);"><td style="padding: 6px 10px; color: #94a3b8;">Puissance Moteur :</td><td style="padding: 6px 10px; font-weight: 800; color: var(--emerald);">${vehicle.power || '129 kW (175 ch)'}</td></tr>
                            <tr style="border-bottom: 1px solid rgba(51,65,85,0.4);"><td style="padding: 6px 10px; color: #94a3b8;">Capacité Benne / Godet :</td><td style="padding: 6px 10px; font-weight: 800;">${vehicle.capacity || '1.25 m³'}</td></tr>
                            <tr style="border-bottom: 1px solid rgba(51,65,85,0.4);"><td style="padding: 6px 10px; color: #94a3b8;">Consommation Moyenne :</td><td style="padding: 6px 10px; font-weight: 800;">${vehicle.consumption || '16.5 L/h'} GNR</td></tr>
                            <tr style="border-bottom: 1px solid rgba(51,65,85,0.4);"><td style="padding: 6px 10px; color: #94a3b8;">Compteur Horaire :</td><td style="padding: 6px 10px; font-weight: 800;">${vehicle.hours} heures</td></tr>
                            <tr style="border-bottom: 1px solid rgba(51,65,85,0.4);"><td style="padding: 6px 10px; color: #94a3b8;">Chantier Actuel :</td><td style="padding: 6px 10px; font-weight: 800; color: #38bdf8;">${vehicle.project}</td></tr>
                            <tr><td style="padding: 6px 10px; color: #94a3b8;">Prochaine VGP :</td><td style="padding: 6px 10px; font-weight: 800; color: var(--emerald);">${vehicle.vgp} (Conforme)</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        `;

        openModal('vehicle-details-modal');
    }

    // ==========================================
    // 9. CATALOG & MATERIALS ENGINE
    // ==========================================
    function filterCatalog(category, btn) {
        catalogFilter = category;
        document.querySelectorAll('.catalog-filter-btn').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
        renderCatalogGrid();
    }

    function renderCatalogGrid() {
        const grid = document.getElementById('catalog-grid');
        if (!grid) return;

        const items = companyData.catalog || [];
        const filtered = items.filter(item => {
            if (catalogFilter === 'all') return true;
            if (catalogFilter === 'safety') return (item.category || '').toLowerCase().includes('sécurité') || (item.category || '').toLowerCase().includes('epi') || (item.category || '').toLowerCase().includes('signal');
            if (catalogFilter === 'tools') return (item.category || '').toLowerCase().includes('outillage') || (item.category || '').toLowerCase().includes('laser') || (item.category || '').toLowerCase().includes('topographie');
            if (catalogFilter === 'materials') return (item.category || '').toLowerCase().includes('béton') || (item.category || '').toLowerCase().includes('bordure') || (item.category || '').toLowerCase().includes('canalisation') || (item.category || '').toLowerCase().includes('voirie') || (item.category || '').toLowerCase().includes('fonte');
            return true;
        });

        grid.innerHTML = filtered.map(item => `
            <div class="card" style="border: 1px solid rgba(51,65,85,0.8); background: rgba(15,23,42,0.95); display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <!-- SVG TECHNICAL VECTOR -->
                    <div style="height: 120px; border-radius: 6px; overflow: hidden; margin-bottom: 0.75rem; border: 1px solid rgba(51,65,85,0.6);">
                        ${getToolMaterialSVG(item.id, item.name)}
                    </div>

                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.4rem;">
                        <div>
                            <span class="badge badge-info" style="font-size: 0.65rem; font-family: 'JetBrains Mono';">${item.id}</span>
                            <h3 style="font-size: 0.95rem; font-weight: 800; color: #f8fafc; margin-top: 2px;">${item.name}</h3>
                            <div style="font-size: 0.72rem; color: #94a3b8;">${item.category} • Norme: <strong>${item.norm || 'NF P98-305'}</strong></div>
                        </div>
                    </div>

                    <div style="background: rgba(30,41,59,0.5); padding: 0.5rem; border-radius: 6px; font-size: 0.75rem; display: grid; grid-template-columns: 1fr 1fr; gap: 4px; margin-bottom: 0.75rem;">
                        <div>Prix HT: <strong style="color: var(--amber);">${(item.price_ht || 0).toLocaleString('fr-FR')} € / ${item.unit || 'u'}</strong></div>
                        <div>Stock: <strong style="color: var(--emerald);">${item.stock || 50} ${item.unit || 'u'}</strong></div>
                        <div>Fournisseur: <strong>${item.supplier || 'Négoce Occitanie'}</strong></div>
                        <div>Dispo: <strong>24/48h</strong></div>
                    </div>
                </div>

                <button class="btn btn-secondary" style="width: 100%; font-size: 0.75rem;" onclick="openCatalogItemModal('${item.id}')">
                    📄 Fiche Technique & Commande
                </button>
            </div>
        `).join('');
    }

    function openCatalogItemModal(itemId) {
        const item = (companyData.catalog || []).find(i => i.id === itemId) || (companyData.catalog || [])[0];
        if (!item) return;

        const body = document.getElementById('catalog-item-modal-body');
        if (!body) return;

        body.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; border-bottom: 1px solid rgba(51,65,85,0.7); padding-bottom: 0.75rem;">
                <div>
                    <span class="badge badge-info" style="font-size: 0.75rem; font-family: 'JetBrains Mono';">${item.id}</span>
                    <h2 style="font-size: 1.25rem; font-weight: 900; color: #38bdf8; margin-top: 4px;">${item.name}</h2>
                    <div style="font-size: 0.85rem; color: #94a3b8;">Catégorie : <strong>${item.category}</strong> • Fournisseur : <strong>${item.supplier || 'Négoce Occitanie'}</strong></div>
                </div>
                <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem;" onclick="closeModal('catalog-item-modal')">✕</button>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.25rem;">
                <div style="height: 180px; border-radius: 6px; overflow: hidden; border: 1px solid rgba(51,65,85,0.8);">
                    ${getToolMaterialSVG(item.id, item.name)}
                </div>
                <div>
                    <div style="font-size: 0.8rem; font-weight: 800; color: #38bdf8; margin-bottom: 4px;">Spécifications Techniques :</div>
                    <p style="font-size: 0.8rem; color: #cbd5e1; line-height: 1.5; margin-bottom: 0.75rem;">${item.description || 'Fourniture certifiée conforme au fascicule 70 du CCTG et aux exigences de résistance mécanique NF.'}</p>
                    <div style="background: rgba(30,41,59,0.7); padding: 0.6rem; border-radius: 6px; font-size: 0.8rem;">
                        <div>Prix Unitaire HT : <strong style="color: var(--amber);">${(item.price_ht || 0).toLocaleString('fr-FR')} € / ${item.unit || 'u'}</strong></div>
                        <div>Stock Actuel : <strong style="color: var(--emerald);">${item.stock || 50} ${item.unit || 'u'}</strong></div>
                        <div>Norme de Conformité : <strong>${item.norm || 'NF P98-305'}</strong></div>
                    </div>
                </div>
            </div>

            <div style="display: flex; justify-content: flex-end; gap: 0.5rem;">
                <button class="btn btn-secondary" onclick="closeModal('catalog-item-modal')">Fermer</button>
                <button class="btn btn-primary" onclick="alert('Bon de commande généré pour ${item.name} !'); closeModal('catalog-item-modal');">🛒 Créer Demande d'Achat</button>
            </div>
        `;

        openModal('catalog-item-modal');
    }
"""
