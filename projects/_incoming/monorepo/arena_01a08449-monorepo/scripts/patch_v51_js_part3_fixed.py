# -*- coding: utf-8 -*-
"""
Patch section_tab_panels.py and section_js_part3.py for 2D enrobes simulation and setTechniqueViewMode
"""

with open('scripts/section_tab_panels.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Update the buttons in section_tab_panels.py
old_btns = r'''                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary tech-view-btn active" id="btn-tech-formulas" onclick="setTechniqueViewMode('formulas')">🧮 Simulateur de Formules</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-compactage" onclick="setTechniqueViewMode('compactage')">🔬 Coupe Tranchée & Compacteur</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-tasksheet" onclick="setTechniqueViewMode('tasksheet')">📊 Fiche de Tâche Type Excel</button>
                    </div>'''

new_btns = r'''                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border); flex-wrap: wrap; gap: 2px;">
                        <button class="btn-secondary tech-view-btn active" id="btn-tech-formulas" onclick="setTechniqueViewMode('formulas')">🧮 Simulateur de Formules</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-enrobes2d" onclick="setTechniqueViewMode('enrobes_2d')">🛣️ Simulation 2D Passes d'Enrobés</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-compactage" onclick="setTechniqueViewMode('compactage')">🔬 Coupe Tranchée & Compacteur</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-tasksheet" onclick="setTechniqueViewMode('tasksheet')">📊 Fiche de Tâche Type Excel</button>
                    </div>'''

if old_btns in text:
    text = text.replace(old_btns, new_btns)
    print("Buttons updated in section_tab_panels.py")
else:
    print("Warning: old_btns exact match not found, searching...")

with open('scripts/section_tab_panels.py', 'w', encoding='utf-8') as f:
    f.write(text)

# Now update section_js_part3.py
with open('scripts/section_js_part3.py', 'r', encoding='utf-8') as f:
    js_text = f.read()

enrobes_2d_code = r'''
    // ==========================================
    // 18.0 SIMULATION 2D : CALCUL DES PASSES D'ENROBÉS & FINISSEUR
    // ==========================================
    let isEnrobes2DSimRunning = false;
    let enrobes2DSimAnimId = null;
    let enrobes2DSimSpeed = 1; // 1, 2, 4
    
    // Simulation state
    let e2dFinisseurX = 40; // current linear position in px
    let e2dRollerX = 40;
    let e2dRollerDir = 1; // 1 = forward, -1 = reverse
    let e2dRollerStripIdx = 0; // 0, 1, 2...
    let e2dPassGrid = []; // 2D array of pass counts
    let e2dGridWidth = 180;
    let e2dGridHeight = 35;
    let e2dTotalTonnage = 0;
    let e2dCurrentTemp = 160.0;

    // Configurable parameters
    let e2dWidth = 3.50; // m
    let e2dFinSpeed = 3.5; // m/min
    let e2dCompSpeed = 4.5; // km/h
    let e2dTargetPasses = 6;
    let e2dThick = 5.0; // cm

    function setTechniqueViewMode(mode) {
        techniqueViewMode = mode;
        document.querySelectorAll('.tech-view-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('btn-tech-' + mode.replace('_', ''))?.classList.add('active');

        const fView = document.getElementById('tech-formulas-view');
        const cView = document.getElementById('tech-compactage-cut-view');
        const eView = document.getElementById('tech-enrobes-2d-view');
        const tView = document.getElementById('tech-tasksheet-view');

        if (fView) fView.style.display = mode === 'formulas' ? 'block' : 'none';
        if (cView) cView.style.display = mode === 'compactage' ? 'block' : 'none';
        if (eView) eView.style.display = mode === 'enrobes_2d' ? 'block' : 'none';
        if (tView) tView.style.display = mode === 'tasksheet' ? 'block' : 'none';

        if (mode === 'formulas') updateFormulaCalculator();
        else if (mode === 'compactage') setTimeout(initCompactageCutCanvas, 50);
        else if (mode === 'enrobes_2d') setTimeout(initEnrobes2DSimulation, 50);
        else renderTaskSheet();
    }

    const setSchemaViewMode = setTechniqueViewMode;

    function initEnrobes2DSimulation() {
        const canvas = document.getElementById('enrobes-2d-canvas');
        if (!canvas) return;
        const w = canvas.parentElement.clientWidth || 600;
        const h = canvas.parentElement.clientHeight || 380;
        canvas.width = w;
        canvas.height = h;

        // Init pass matrix
        e2dGridWidth = Math.floor((w - 100) / 3);
        e2dGridHeight = Math.floor(140 / 4);
        e2dPassGrid = Array.from({ length: e2dGridWidth }, () => Array(e2dGridHeight).fill(0));

        updateEnrobes2DParams();
        renderEnrobes2DSimulation();
    }

    function toggleEnrobes2DSim() {
        isEnrobes2DSimRunning = !isEnrobes2DSimRunning;
        const btn = document.getElementById('btn-enrobes2d-play');
        if (btn) btn.textContent = isEnrobes2DSimRunning ? '⏸️ Pause Simulation' : '▶️ Lancer Simulation 2D';

        if (isEnrobes2DSimRunning) {
            runEnrobes2DLoop();
            logCockpit("Simulation 2D passes d'enrobés et finisseur en cours d'exécution.", 'ok');
        } else {
            if (enrobes2DSimAnimId) cancelAnimationFrame(enrobes2DSimAnimId);
            logCockpit("Simulation 2D passes d'enrobés mise en pause.", 'info');
        }
    }

    function toggleEnrobes2DSpeed() {
        if (enrobes2DSimSpeed === 1) enrobes2DSimSpeed = 2;
        else if (enrobes2DSimSpeed === 2) enrobes2DSimSpeed = 4;
        else enrobes2DSimSpeed = 1;

        const btn = document.getElementById('btn-enrobes2d-speed');
        if (btn) btn.textContent = `⚡ Vitesse x${enrobes2DSimSpeed}`;
    }

    function stepEnrobes2DSim() {
        advanceEnrobes2DSim(1.5);
        renderEnrobes2DSimulation();
    }

    function resetEnrobes2DSim() {
        isEnrobes2DSimRunning = false;
        if (enrobes2DSimAnimId) cancelAnimationFrame(enrobes2DSimAnimId);
        const btn = document.getElementById('btn-enrobes2d-play');
        if (btn) btn.textContent = '▶️ Lancer Simulation 2D';

        e2dFinisseurX = 40;
        e2dRollerX = 40;
        e2dRollerDir = 1;
        e2dRollerStripIdx = 0;
        e2dTotalTonnage = 0;
        e2dCurrentTemp = 160.0;

        initEnrobes2DSimulation();
        logCockpit("Simulation 2D passes d'enrobés réinitialisée.", 'info');
    }

    function updateEnrobes2DParams() {
        e2dWidth = Number(document.getElementById('e2d-width-range')?.value || 3.50);
        e2dFinSpeed = Number(document.getElementById('e2d-fin-spd-range')?.value || 3.5);
        e2dCompSpeed = Number(document.getElementById('e2d-comp-spd-range')?.value || 4.5);
        e2dTargetPasses = Number(document.getElementById('e2d-passes-range')?.value || 6);
        e2dThick = Number(document.getElementById('e2d-thick-range')?.value || 5.0);

        const wEl = document.getElementById('e2d-width-val');
        const finSpdEl = document.getElementById('e2d-fin-spd-val');
        const compSpdEl = document.getElementById('e2d-comp-spd-val');
        const pasEl = document.getElementById('e2d-passes-val');
        const thkEl = document.getElementById('e2d-thick-val');

        if (wEl) wEl.textContent = `${e2dWidth.toFixed(2)} m`;
        if (finSpdEl) finSpdEl.textContent = `${e2dFinSpeed.toFixed(1)} m/min`;
        if (compSpdEl) compSpdEl.textContent = `${e2dCompSpeed.toFixed(1)} km/h`;
        if (pasEl) pasEl.textContent = `${e2dTargetPasses} passes`;
        if (thkEl) thkEl.textContent = `${e2dThick.toFixed(1)} cm`;

        // Adequacy check
        const qFinTonneH = e2dWidth * (e2dFinSpeed * 60) * (e2dThick / 100) * 2.45;
        const qCompTonneH = (1.70 * (e2dCompSpeed * 1000) * (e2dThick / 100) * 2.45) / e2dTargetPasses;
        const adeqEl = document.getElementById('e2d-stat-adeq');
        if (adeqEl) {
            if (qCompTonneH >= qFinTonneH) {
                adeqEl.textContent = "✅ 1 Tandem Suffisant";
                adeqEl.style.color = "var(--emerald)";
            } else {
                adeqEl.textContent = "⚠️ 2 Tandems Requis";
                adeqEl.style.color = "var(--amber)";
            }
        }
    }

    function runEnrobes2DLoop() {
        if (!isEnrobes2DSimRunning) return;
        advanceEnrobes2DSim(0.6 * enrobes2DSimSpeed);
        renderEnrobes2DSimulation();
        enrobes2DSimAnimId = requestAnimationFrame(runEnrobes2DLoop);
    }

    function advanceEnrobes2DSim(delta) {
        const canvas = document.getElementById('enrobes-2d-canvas');
        if (!canvas) return;
        const maxTrackWidth = canvas.width - 120;

        // 1. Advance Finisher
        if (e2dFinisseurX < maxTrackWidth) {
            e2dFinisseurX += (e2dFinSpeed / 60) * delta * 8;
        }

        // 2. Roller movement & passes
        const rollerMaxX = Math.min(e2dFinisseurX - 30, maxTrackWidth);
        const rollerMinX = 40;

        if (rollerMaxX > rollerMinX + 40) {
            e2dRollerX += e2dRollerDir * ((e2dCompSpeed * 1000 / 3600) * delta * 4);

            if (e2dRollerX >= rollerMaxX) {
                e2dRollerX = rollerMaxX;
                e2dRollerDir = -1;
                e2dRollerStripIdx = (e2dRollerStripIdx + 1) % 3; // switch rolling lane
            } else if (e2dRollerX <= rollerMinX) {
                e2dRollerX = rollerMinX;
                e2dRollerDir = 1;
                e2dRollerStripIdx = (e2dRollerStripIdx + 1) % 3;
            }

            // Increment passes on pass grid under roller
            const gridX = Math.floor((e2dRollerX - 40) / 3);
            const rollerStripY = Math.floor(e2dRollerStripIdx * (e2dGridHeight / 3));

            if (gridX >= 0 && gridX < e2dGridWidth) {
                for (let y = rollerStripY; y < Math.min(e2dGridHeight, rollerStripY + Math.floor(e2dGridHeight / 2.5)); y++) {
                    e2dPassGrid[gridX][y] = Math.min(12, e2dPassGrid[gridX][y] + 0.15 * delta);
                }
            }
        }

        // Update telemetry
        const linearMeters = ((e2dFinisseurX - 40) / (maxTrackWidth - 40)) * 120; // 120m section
        const surfaceM2 = linearMeters * e2dWidth;
        e2dTotalTonnage = surfaceM2 * (e2dThick / 100) * 2.45;

        // Temperature cooldown curve (160°C down to 110°C over distance)
        e2dCurrentTemp = Math.max(85.0, 160.0 - (linearMeters * 0.35));

        // Update DOM readouts
        const linEl = document.getElementById('e2d-stat-lin');
        const tonEl = document.getElementById('e2d-stat-ton');
        const compacEl = document.getElementById('e2d-stat-compac');
        const tempEl = document.getElementById('enrobes2d-temp-val');

        if (linEl) linEl.textContent = `${linearMeters.toFixed(1)} ml (${surfaceM2.toFixed(0)} m²)`;
        if (tonEl) tonEl.textContent = `${e2dTotalTonnage.toFixed(1)} t`;
        if (tempEl) {
            tempEl.textContent = `${e2dCurrentTemp.toFixed(1)} °C`;
            tempEl.style.color = e2dCurrentTemp > 125 ? '#10b981' : e2dCurrentTemp > 105 ? '#f59e0b' : '#f43f5e';
        }

        if (compacEl) {
            let totalPasses = 0, count = 0;
            for (let x = 0; x < Math.min(e2dGridWidth, Math.floor((e2dFinisseurX - 40) / 3)); x++) {
                for (let y = 0; y < e2dGridHeight; y++) {
                    totalPasses += e2dPassGrid[x][y];
                    count++;
                }
            }
            const avgPasses = count > 0 ? (totalPasses / count) : 0;
            const compacity = Math.min(99.5, 92.0 + (avgPasses / e2dTargetPasses) * 6.5);
            compacEl.textContent = `${compacity.toFixed(1)} % OPN (${avgPasses.toFixed(1)} passes)`;
            compacEl.style.color = compacity >= 98.0 ? 'var(--emerald)' : 'var(--amber)';
        }
    }

    function renderEnrobes2DSimulation() {
        const canvas = document.getElementById('enrobes-2d-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const w = canvas.width;
        const h = canvas.height;

        ctx.fillStyle = '#060a14';
        ctx.fillRect(0, 0, w, h);

        const roadY = h * 0.28;
        const roadH = 150;
        const roadStartX = 40;
        const roadEndX = w - 40;

        // 1. ROAD FOUNDATION / SUPPORT (GNT 0/31.5)
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(roadStartX, roadY, roadEndX - roadStartX, roadH);
        ctx.strokeStyle = '#475569';
        ctx.lineWidth = 2;
        ctx.strokeRect(roadStartX, roadY, roadEndX - roadStartX, roadH);

        // Curbs (Bordures T2 aux deux extrémités)
        ctx.fillStyle = '#64748b';
        ctx.fillRect(roadStartX, roadY - 8, roadEndX - roadStartX, 8);
        ctx.fillRect(roadStartX, roadY + roadH, roadEndX - roadStartX, 8);

        // 2. PASS HEATMAP RENDERING
        const cellW = 3;
        const cellH = roadH / e2dGridHeight;

        for (let x = 0; x < e2dGridWidth; x++) {
            const pxX = roadStartX + x * cellW;
            if (pxX > e2dFinisseurX) break; // Not paved yet

            for (let y = 0; y < e2dGridHeight; y++) {
                const pxY = roadY + y * cellH;
                const passes = e2dPassGrid[x] ? e2dPassGrid[x][y] : 0;

                if (passes <= 0.2) {
                    // Hot fresh asphalt (0 passes, 160°C)
                    ctx.fillStyle = '#0f172a';
                } else if (passes < 2.5) {
                    ctx.fillStyle = '#0284c7'; // 1-2 passes
                } else if (passes < 4.5) {
                    ctx.fillStyle = '#f59e0b'; // 3-4 passes
                } else if (passes <= 7.5) {
                    ctx.fillStyle = '#10b981'; // 5-6 passes (target)
                } else {
                    ctx.fillStyle = '#ec4899'; // Over-compacted
                }
                ctx.fillRect(pxX, pxY, cellW + 0.5, cellH + 0.5);
            }
        }

        // 3. FINISHER MACHINE (Vögele Super 1800)
        const finX = Math.min(e2dFinisseurX, roadEndX - 40);
        // Screed / Table de pose
        ctx.fillStyle = '#f59e0b';
        ctx.fillRect(finX - 12, roadY - 5, 14, roadH + 10);
        ctx.strokeStyle = '#f8fafc';
        ctx.lineWidth = 2;
        ctx.strokeRect(finX - 12, roadY - 5, 14, roadH + 10);

        // Finisher Tractor Body
        ctx.fillStyle = '#d97706';
        ctx.fillRect(finX, roadY + roadH * 0.2, 50, roadH * 0.6);
        // Hopper / Trémie à l'avant
        ctx.fillStyle = '#78350f';
        ctx.fillRect(finX + 35, roadY + roadH * 0.25, 25, roadH * 0.5);
        // Operator Station
        ctx.fillStyle = '#38bdf8';
        ctx.fillRect(finX + 12, roadY + roadH * 0.35, 18, roadH * 0.3);

        ctx.font = 'bold 10px monospace';
        ctx.fillStyle = '#f8fafc';
        ctx.fillText("FINISSEUR VÖGELE", finX + 2, roadY + roadH * 0.15);

        // Steam vapor effect behind screed
        if (isEnrobes2DSimRunning) {
            ctx.fillStyle = 'rgba(248, 250, 252, 0.25)';
            ctx.beginPath();
            ctx.arc(finX - 18, roadY + roadH * 0.3, 12, 0, Math.PI * 2);
            ctx.arc(finX - 25, roadY + roadH * 0.7, 15, 0, Math.PI * 2);
            ctx.fill();
        }

        // 4. TANDEM ROLLER COMPACTOR (Bomag BW 151)
        if (e2dRollerX > roadStartX + 10) {
            const rollX = e2dRollerX;
            const stripOffset = (e2dRollerStripIdx * (roadH / 3)) + (roadH / 6);
            const rollY = roadY + stripOffset - 22;

            // Chassis
            ctx.fillStyle = '#eab308';
            ctx.fillRect(rollX - 18, rollY + 6, 36, 32);
            // Front Drum (Cylindre avant vibrant)
            ctx.fillStyle = '#94a3b8';
            ctx.fillRect(rollX - 26, rollY, 8, 44);
            // Rear Drum (Cylindre arrière)
            ctx.fillStyle = '#94a3b8';
            ctx.fillRect(rollX + 18, rollY, 8, 44);

            // Cabin & Beacon
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(rollX - 8, rollY + 12, 16, 20);
            ctx.fillStyle = '#f59e0b';
            ctx.beginPath(); ctx.arc(rollX, rollY + 22, 3, 0, Math.PI * 2); ctx.fill();

            // Direction Arrow
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(rollX, rollY - 6);
            ctx.lineTo(rollX + e2dRollerDir * 14, rollY - 6);
            ctx.lineTo(rollX + e2dRollerDir * 8, rollY - 10);
            ctx.stroke();

            ctx.font = 'bold 9px monospace';
            ctx.fillStyle = '#ffffff';
            ctx.fillText("ROULEAU TANDEM", rollX - 24, rollY - 12);
        }

        // 5. THERMAL GRADIENT HUD BAR AT TOP
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(roadStartX, 15, roadEndX - roadStartX, 16);
        ctx.strokeStyle = 'rgba(56,189,248,0.3)';
        ctx.strokeRect(roadStartX, 15, roadEndX - roadStartX, 16);

        const grad = ctx.createLinearGradient(roadStartX, 0, roadEndX, 0);
        grad.addColorStop(0, '#f43f5e'); // 160°C
        grad.addColorStop(0.5, '#f59e0b'); // 130°C
        grad.addColorStop(1, '#0284c7'); // 90°C
        ctx.fillStyle = grad;
        ctx.fillRect(roadStartX + 2, 17, Math.max(10, e2dFinisseurX - roadStartX), 12);

        ctx.font = 'bold 9px monospace';
        ctx.fillStyle = '#f8fafc';
        ctx.fillText("TEMPÉRATURE DE L'ENROBÉ : 160°C (POSE) ➔ 130°C (COMPACTAGE OPTIMAL) ➔ 110°C (LIMITE VIBRATIONS)", roadStartX + 10, 26);
    }
'''

pos_tech = js_text.find('function setTechniqueViewMode(mode) {')
pos_comp_toggle = js_text.find('function toggleCompactageAnimation() {')

if pos_tech != -1 and pos_comp_toggle != -1:
    js_text = js_text[:pos_tech] + enrobes_2d_code.strip() + "\n\n    " + js_text[pos_comp_toggle:]
    print("setTechniqueViewMode & Enrobes 2D JS injected successfully!")
else:
    print("Error finding setTechniqueViewMode in section_js_part3.py")

with open('scripts/section_js_part3.py', 'w', encoding='utf-8') as f:
    f.write(js_text)
