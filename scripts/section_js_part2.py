def get_js_part2():
    return """
    // ==========================================
    // 7. WATCH TOWER 3D & 2D RADAR SIMULATOR
    // ==========================================
    const simulationScenarios = {
        'scen_tranchee_vrd': {
            title: "Tranchée Assainissement & Blindage Profond (3.20m)",
            desc: "Pose collecteur fonte DN400 sous nappe phréatique avec blindage caisson double glissière et rabattement de nappe.",
            steps: [
                { id: 'st1', phase: "Phase 1 : Détection & Piquetage Réseaux", risks: "Endommagement réseaux gaz/élec existants", action: "Réalisation DICT + Détection géo-radar + Piquetage 7 couleurs AIPR.", machinery: "Camion Atelier + Détecteur RD8100", safety: "Port EPI obligatoire + Marquage peinture normée" },
                { id: 'st2', phase: "Phase 2 : Démolition & Terrassement Supérieur", risks: "Éboulement de berge + Projection cailloux", action: "Sciage enrobé au disque diamanté, décapage 0.80m à la pelle 24T avec godet sans dents.", machinery: "Pelle 24T Liebherr + Scie Stihl TS800", safety: "Zone d'exclusion 10m autour de la tourelle" },
                { id: 'st3', phase: "Phase 3 : Fonçage des Caissons de Blindage", risks: "Ensevelissement du personnel en fouille", action: "Pose caissons Krings 3.50m x 2.40m, fonçage progressif par poussée vérin godet.", machinery: "Pelle 24T + Élingues 4 brins contrôlées", safety: "Interdiction formelle de descendre hors blindage" },
                { id: 'st4', phase: "Phase 4 : Pose Tuyaux Fonte DN400 & Calage", risks: "Écrasement membre lors du levage tuyaux", action: "Manutention au palonnier, guidage au cordage, emboîtement au tire-fort hydraulique.", machinery: "Pelle 15T sur pneus + Laser Piper 200", safety: "Contrôle atmosphère H2S/CO en fond de fouille" },
                { id: 'st5', phase: "Phase 5 : Remblaiement & Compactage Méthodique", risks: "Tassement ultérieur de chaussée", action: "Remblai GNT 0/31.5 par couches de 30cm, compactage au pilonneur vibrant + contrôle q4 au pénétromètre.", machinery: "Compacteur Tandem Bomag + Pénétromètre PANDA", safety: "Protection auditive contre bruit pilonneuse" }
            ]
        },
        'scen_enrobes_chaud': {
            title: "Mise en Œuvre Enrobés Chauds (BBSG 0/10)",
            desc: "Application d'une couche de roulement 6cm sur 4500m² avec finisseur guidé laser et compactage lourd.",
            steps: [
                { id: 'e1', phase: "Phase 1 : Balayage & Émulsion d'Accrochage", risks: "Brûlures thermiques émulsion chaude + Glissance", action: "Balayeuse aspiratrice haute pression + Répandeuse émulsion cationique à 65°C (350g/m²).", machinery: "Balayeuse Ravo + Répandeuse Émulsion", safety: "Balisage d'approche AK5 + B14 (30 km/h)" },
                { id: 'e2', phase: "Phase 2 : Approvisionnement par Semi 38t", risks: "Écrasement piétons lors des manœuvres en marche arrière", action: "Guidage systématique des camions par homme de trafic qualifié avec gilet HV classe 3.", machinery: "Semi-remorques calorifugées 38t", safety: "Bipeur de recul + Caméra 360° en service" },
                { id: 'e3', phase: "Phase 3 : Réglage au Finisseur Haute Densité", risks: "Brûlures contact table chauffante + Inhalation fumées", action: "Alimentation continue, réglage épaisseur automatique par palpeurs à ultrasons, T° > 140°C.", machinery: "Finisseur Vögele Super 1800-3i", safety: "Aspiration des fumées de bitume active" },
                { id: 'e4', phase: "Phase 4 : Compactage & Finition des Joints", risks: "Fissuration thermique ou surcompactage", action: "Train de compactage : 4 passes tandem vibrant lourd + 2 passes rouleau à pneus lisse.", machinery: "Bomag BW 174 AP + Rouleau Pneus Hamm", safety: "Arrosage permanent des billes sans excès" }
            ]
        },
        'scen_carrefour_giratoire': {
            title: "Création Carrefour Giratoire Urbain sous Circulation",
            desc: "Aménagement complet d'un rond-point 4 branches avec gestion des flux résiduels et déviations de nuit.",
            steps: [
                { id: 'g1', phase: "Phase 1 : Dévoiement Provisoire de Circulation", risks: "Collision véhicules tiers avec la zone chantier", action: "Pose séparateurs modulaires de voies (SMV béton K16), signalisation temporaire de nuit.", machinery: "Camion Grue Palfinger + Fourgon Signalisation", safety: "Garde-corps et balises K5c rétroréfléchissantes" },
                { id: 'g2', phase: "Phase 2 : Démolition & Terrassement de l'Îlot Central", risks: "Sectionnement réseaux non répertoriés", action: "Décapage terre végétale, fouilles en pleine masse avec contrôle continu détecteur réseau.", machinery: "Pelle 15T + Camion 8x4 Scania", safety: "Sondages préliminaires manuels obligatoires" },
                { id: 'g3', phase: "Phase 3 : Pose des Bordures T2 / I2 & Franchissable", risks: "Troubles musculo-squelettiques (TMS) manutention lourde", action: "Pose bordures granit et béton au pince-bordure hydraulique sur lit de béton C25/30.", machinery: "Pince hydraulique sur mini-pelle + Bétonnière", safety: "Port gants anti-coupure et chaussures de sécurité S3" },
                { id: 'g4', phase: "Phase 4 : Éclairage Public & Massifs Candelabres", risks: "Risque électrique lors du raccordement armoire", action: "Coulage massifs béton 1m³, passage gaines TPC rouge 90mm, raccordement hors tension vérifié.", machinery: "Tarière hydraulique + Camion Nacelle 18m", safety: "Habilitation électrique B2V / H0V requise" }
            ]
        }
    };

    function loadScenario(scenKey) {
        currentScenarioId = scenKey;
        activeScenarioStepIdx = 0;
        const scen = simulationScenarios[scenKey];
        if (!scen) return;

        const infoCard = document.getElementById('scenario-info-card');
        if (infoCard) {
            infoCard.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.75rem;">
                    <div>
                        <span class="badge badge-info">Scénario Interactif</span>
                        <h3 style="font-size:1.15rem; font-weight:800; color:#f8fafc; margin-top:0.25rem;">${scen.title}</h3>
                    </div>
                    <span style="font-family:'JetBrains Mono'; font-size:0.8rem; color:#38bdf8; background:rgba(2,132,199,0.2); padding:0.2rem 0.5rem; border-radius:4px;">${scen.steps.length} Étapes</span>
                </div>
                <p style="font-size:0.85rem; color:#94a3b8; line-height:1.4;">${scen.desc}</p>
            `;
        }

        renderScenarioStepList();
        drawStepVisual(activeScenarioStepIdx);
        logCockpit(`Scénario chargé : ${scen.title}`, 'info');
    }

    function renderScenarioStepList() {
        const list = document.getElementById('scenario-steps-list');
        const scen = simulationScenarios[currentScenarioId];
        if (!list || !scen) return;

        list.innerHTML = scen.steps.map((st, idx) => `
            <div onclick="selectScenarioStep(${idx})" style="padding:0.75rem; border-radius:6px; cursor:pointer; margin-bottom:0.5rem; border:1px solid ${idx === activeScenarioStepIdx ? 'var(--cyan)' : 'rgba(51,65,85,0.4)'}; background:${idx === activeScenarioStepIdx ? 'rgba(6,182,212,0.15)' : 'rgba(15,23,42,0.5)'}; transition:all 0.2s;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="font-size:0.85rem; color:${idx === activeScenarioStepIdx ? '#38bdf8' : '#f8fafc'};">${st.phase}</strong>
                    <span style="font-size:0.7rem; font-family:'JetBrains Mono'; color:#64748b;">Étape ${idx + 1}/${scen.steps.length}</span>
                </div>
                <div style="font-size:0.75rem; color:#94a3b8; margin-top:0.2rem;">⚠️ Risque : <span style="color:#fca5a5;">${st.risks}</span></div>
            </div>
        `).join('');
    }

    function selectScenarioStep(idx) {
        activeScenarioStepIdx = idx;
        renderScenarioStepList();
        drawStepVisual(idx);
    }

    function nextScenarioStep() {
        const scen = simulationScenarios[currentScenarioId];
        if (scen && activeScenarioStepIdx < scen.steps.length - 1) {
            selectScenarioStep(activeScenarioStepIdx + 1);
        }
    }

    function prevScenarioStep() {
        if (activeScenarioStepIdx > 0) {
            selectScenarioStep(activeScenarioStepIdx - 1);
        }
    }

    function drawStepVisual(stepIdx) {
        const scen = simulationScenarios[currentScenarioId];
        if (!scen) return;
        const st = scen.steps[stepIdx];
        if (!st) return;

        const detailsBox = document.getElementById('step-details-box');
        if (detailsBox) {
            detailsBox.innerHTML = `
                <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(51,65,85,0.7); border-radius:8px; padding:1rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
                        <h4 style="font-size:1rem; font-weight:800; color:#38bdf8;">📌 ${st.phase}</h4>
                        <span class="badge badge-success">Conforme CSPS / SPS</span>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem; font-size:0.85rem; margin-bottom:0.75rem;">
                        <div>
                            <span style="color:#64748b; font-size:0.75rem;">ENGINS & OUTILLAGE MOBILISÉS :</span>
                            <div style="color:#f8fafc; font-weight:700;">🚜 ${st.machinery}</div>
                        </div>
                        <div>
                            <span style="color:#64748b; font-size:0.75rem;">PRESCRIPTION SÉCURITÉ OPBTP :</span>
                            <div style="color:var(--amber); font-weight:700;">🦺 ${st.safety}</div>
                        </div>
                    </div>
                    <div style="background:rgba(2,132,199,0.1); border-left:3px solid #0284c7; padding:0.6rem; border-radius:4px; font-size:0.85rem; color:#cbd5e1;">
                        <strong>Action Méthode :</strong> ${st.action}
                    </div>
                </div>
            `;
        }
    }

    function setSimulatorView(mode) {
        simulatorViewMode = mode;
        document.querySelectorAll('.sim-view-btn').forEach(b => b.classList.remove('active'));
        document.getElementById(`btn-sim-${mode}`)?.classList.add('active');

        const radarEl = document.getElementById('radar-canvas-container');
        const view3dEl = document.getElementById('view3d-canvas-container');

        if (mode === 'radar') {
            if (radarEl) radarEl.style.display = 'block';
            if (view3dEl) view3dEl.style.display = 'none';
        } else {
            if (radarEl) radarEl.style.display = 'none';
            if (view3dEl) view3dEl.style.display = 'block';
            init3DCanvas();
        }
    }

    function toggleRadarStream() {
        isRadarLive = !isRadarLive;
        const btn = document.getElementById('btn-radar-toggle');
        if (btn) btn.textContent = isRadarLive ? '🟢 Signal Radar En Direct' : '🔴 Radar En Pause';
        logCockpit(`Radar télémétrique : ${isRadarLive ? 'Actif' : 'En Pause'}`, isRadarLive ? 'ok' : 'warn');
    }

    function initWatchtowerRadar() {
        radarCanvas = document.getElementById('watchtower-radar-canvas');
        if (!radarCanvas) return;
        radarCtx = radarCanvas.getContext('2d');

        // Resize canvas to parent
        radarCanvas.width = radarCanvas.offsetWidth || 600;
        radarCanvas.height = radarCanvas.offsetHeight || 400;

        let angle = 0;
        const radarTargets = [
            { x: 0.35, y: 0.4, label: 'Pelle CAT 320 (ZAC Pins)', color: '#10b981', code: 'ENG-01' },
            { x: 0.65, y: 0.3, label: 'Porteur 8x4 Scania (Bd Haussmann)', color: '#38bdf8', code: 'ENG-03' },
            { x: 0.5, y: 0.7, label: 'Compacteur Bomag (ZI Nord)', color: '#f59e0b', code: 'ENG-02' },
            { x: 0.8, y: 0.75, label: 'Équipe A (Tranchée Ouverte)', color: '#ec4899', code: 'EQ-A' },
            { x: 0.2, y: 0.8, label: 'Drone LiDAR DJI Matrice', color: '#06b6d4', code: 'DRN-01' }
        ];

        function renderRadarFrame() {
            if (!radarCtx || radarCanvas.style.display === 'none') {
                radarAnimId = requestAnimationFrame(renderRadarFrame);
                return;
            }

            const w = radarCanvas.width;
            const h = radarCanvas.height;
            const cx = w / 2;
            const cy = h / 2;
            const maxR = Math.min(cx, cy) - 20;

            radarCtx.fillStyle = '#090d16';
            radarCtx.fillRect(0, 0, w, h);

            // Draw concentric range circles
            radarCtx.strokeStyle = 'rgba(6, 182, 212, 0.25)';
            radarCtx.lineWidth = 1;
            for (let r = maxR / 4; r <= maxR; r += maxR / 4) {
                radarCtx.beginPath();
                radarCtx.arc(cx, cy, r, 0, Math.PI * 2);
                radarCtx.stroke();
            }

            // Draw crosshairs
            radarCtx.beginPath();
            radarCtx.moveTo(cx - maxR, cy);
            radarCtx.lineTo(cx + maxR, cy);
            radarCtx.moveTo(cx, cy - maxR);
            radarCtx.lineTo(cx, cy + maxR);
            radarCtx.stroke();

            // Draw sweeping line
            if (isRadarLive) angle += 0.03;
            const sweepX = cx + Math.cos(angle) * maxR;
            const sweepY = cy + Math.sin(angle) * maxR;

            const grad = radarCtx.createRadialGradient(cx, cy, 0, cx, cy, maxR);
            grad.addColorStop(0, 'rgba(6, 182, 212, 0.4)');
            grad.addColorStop(1, 'rgba(6, 182, 212, 0)');

            radarCtx.beginPath();
            radarCtx.moveTo(cx, cy);
            radarCtx.arc(cx, cy, maxR, angle - 0.35, angle);
            radarCtx.closePath();
            radarCtx.fillStyle = 'rgba(6, 182, 212, 0.15)';
            radarCtx.fill();

            radarCtx.beginPath();
            radarCtx.moveTo(cx, cy);
            radarCtx.lineTo(sweepX, sweepY);
            radarCtx.strokeStyle = '#38bdf8';
            radarCtx.lineWidth = 2;
            radarCtx.stroke();

            // Draw targets
            radarTargets.forEach(t => {
                const tx = t.x * w;
                const ty = t.y * h;

                radarCtx.fillStyle = t.color;
                radarCtx.beginPath();
                radarCtx.arc(tx, ty, 5, 0, Math.PI * 2);
                radarCtx.fill();

                radarCtx.strokeStyle = t.color;
                radarCtx.beginPath();
                radarCtx.arc(tx, ty, 9, 0, Math.PI * 2);
                radarCtx.stroke();

                radarCtx.fillStyle = '#f8fafc';
                radarCtx.font = '10px "JetBrains Mono"';
                radarCtx.fillText(`[${t.code}] ${t.label}`, tx + 12, ty + 4);
            });

            radarAnimId = requestAnimationFrame(renderRadarFrame);
        }

        cancelAnimationFrame(radarAnimId);
        renderRadarFrame();
    }

    function init3DCanvas() {
        const c = document.getElementById('watchtower-3d-canvas');
        if (!c) return;
        const ctx = c.getContext('2d');
        c.width = c.offsetWidth || 600;
        c.height = c.offsetHeight || 400;

        // Mouse drag event listeners for camera
        c.onmousedown = (e) => {
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
            cameraRotX = Math.max(10, Math.min(80, cameraRotX + dy * 0.5));
            lastMouseX = e.clientX;
            lastMouseY = e.clientY;
            render3DScene(ctx, c.width, c.height);
        };

        render3DScene(ctx, c.width, c.height);
    }

    function render3DScene(ctx, w, h) {
        if (!ctx) return;
        ctx.fillStyle = '#090d16';
        ctx.fillRect(0, 0, w, h);

        const cx = w / 2;
        const cy = h / 2 + 30;

        // Draw isometric terrain grid
        ctx.strokeStyle = 'rgba(51, 65, 85, 0.4)';
        ctx.lineWidth = 1;

        const gridSize = 14;
        const spacing = 22 * cameraZoom;
        const radY = (cameraRotY * Math.PI) / 180;
        const radX = (cameraRotX * Math.PI) / 180;

        for (let i = -gridSize; i <= gridSize; i++) {
            ctx.beginPath();
            for (let j = -gridSize; j <= gridSize; j++) {
                const x0 = i * spacing;
                const z0 = j * spacing;
                const rx = x0 * Math.cos(radY) - z0 * Math.sin(radY);
                const rz = x0 * Math.sin(radY) + z0 * Math.cos(radY);
                const sy = -rz * Math.sin(radX);
                const sx = rx;
                if (j === -gridSize) ctx.moveTo(cx + sx, cy + sy);
                else ctx.lineTo(cx + sx, cy + sy);
            }
            ctx.stroke();
        }

        // Draw 3D Trench Object in center
        ctx.fillStyle = '#0284c7';
        ctx.font = 'bold 12px "JetBrains Mono"';
        ctx.fillText(`📐 Vue Isométrique 3D Chantier (Rot: ${Math.round(cameraRotY)}°, Incl: ${Math.round(cameraRotX)}°)`, 20, 30);
        ctx.fillStyle = '#94a3b8';
        ctx.font = '10px system-ui';
        ctx.fillText('Maintenez le clic gauche et glissez pour faire pivoter la caméra en orbite 3D', 20, 50);

        // Draw excavation trench box
        ctx.fillStyle = 'rgba(239, 68, 68, 0.3)';
        ctx.strokeStyle = '#ef4444';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.rect(cx - 80, cy - 30, 160, 60);
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = '#ffffff';
        ctx.fillText('ZONE DE FOUILLE BLINDÉE', cx - 70, cy + 5);
    }

    // ==========================================
    // 8. FLEET & MACHINERY ENGINE
    // ==========================================
    function filterFleet(type, btn) {
        fleetFilter = type;
        document.querySelectorAll('.fleet-filter-btn').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
        renderFleetGrid();
    }

    function renderFleetGrid() {
        const grid = document.getElementById('fleet-grid');
        if (!grid || !companyData.fleet) return;

        const filtered = companyData.fleet.filter(f => fleetFilter === 'all' || f.type.toLowerCase().includes(fleetFilter));

        grid.innerHTML = filtered.map(f => `
            <div class="card" style="display:flex; flex-direction:column; justify-content:space-between;">
                <div>
                    <div style="height:140px; margin-bottom:1rem; border-radius:6px; overflow:hidden; border:1px solid rgba(51,65,85,0.6);">
                        ${getVehicleSVG(f.type, f.name)}
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
                        <span class="badge ${f.status === 'Sur chantier' ? 'badge-success' : 'badge-warning'}">${f.status}</span>
                        <span style="font-family:'JetBrains Mono'; font-size:0.8rem; color:#94a3b8;">${f.id}</span>
                    </div>
                    <h3 style="font-size:1.1rem; font-weight:800; color:#f8fafc; margin-bottom:0.25rem;">${f.name}</h3>
                    <div style="font-size:0.8rem; color:#38bdf8; font-weight:700; margin-bottom:0.75rem;">${f.type}</div>

                    <div style="font-size:0.8rem; background:rgba(15,23,42,0.6); padding:0.6rem; border-radius:6px; border:1px solid rgba(51,65,85,0.4); margin-bottom:0.75rem;">
                        <div><span style="color:#64748b;">Affectation :</span> <strong style="color:#f1f5f9;">${f.assigned}</strong></div>
                        <div><span style="color:#64748b;">Opérateur :</span> <strong style="color:#f1f5f9;">${f.operator}</strong></div>
                        <div><span style="color:#64748b;">Heures compteur :</span> <strong style="font-family:'JetBrains Mono'; color:var(--emerald);">${f.hours} h</strong></div>
                        <div><span style="color:#64748b;">Prochaine VGP :</span> <strong style="font-family:'JetBrains Mono'; color:#f59e0b;">${f.vgp}</strong></div>
                    </div>
                </div>

                <div style="display:flex; gap:0.5rem; margin-top:0.5rem;">
                    <button class="btn btn-primary" style="flex:1; font-size:0.8rem;" onclick="openVehicleModal('${f.id}')">
                        📋 Fiche Technique VGP
                    </button>
                </div>
            </div>
        `).join('');
    }

    function openVehicleModal(vehicleId) {
        const v = (companyData.fleet || []).find(x => x.id === vehicleId);
        if (!v) return;

        const body = document.getElementById('vehicle-modal-body');
        if (!body) return;

        body.innerHTML = `
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1.5rem; margin-bottom:1.5rem;">
                <div style="height:220px; border-radius:8px; overflow:hidden; border:1px solid rgba(51,65,85,0.8);">
                    ${getVehicleSVG(v.type, v.name)}
                </div>
                <div>
                    <span class="badge ${v.status === 'Sur chantier' ? 'badge-success' : 'badge-warning'}">${v.status}</span>
                    <h2 style="font-size:1.5rem; font-weight:900; color:#f8fafc; margin-top:0.35rem;">${v.name}</h2>
                    <div style="color:#38bdf8; font-weight:700; margin-bottom:1rem;">${v.type} • Matr. ${v.id}</div>

                    <div style="background:rgba(15,23,42,0.8); padding:0.85rem; border-radius:6px; border:1px solid rgba(51,65,85,0.6); font-size:0.85rem;">
                        <div style="margin-bottom:0.4rem;"><span style="color:#64748b;">Chantier en cours :</span> <strong style="color:#f8fafc;">${v.assigned}</strong></div>
                        <div style="margin-bottom:0.4rem;"><span style="color:#64748b;">Chauffeur / Machiniste :</span> <strong style="color:#f8fafc;">${v.operator}</strong></div>
                        <div style="margin-bottom:0.4rem;"><span style="color:#64748b;">Heures moteur cumulées :</span> <strong style="font-family:'JetBrains Mono'; color:var(--emerald);">${v.hours} h</strong></div>
                        <div><span style="color:#64748b;">Validité Contrôle VGP :</span> <strong style="font-family:'JetBrains Mono'; color:#f59e0b;">${v.vgp} (Conforme APAVE)</strong></div>
                    </div>
                </div>
            </div>

            <h3 style="font-size:1.1rem; font-weight:800; color:#38bdf8; margin-bottom:0.75rem;">⚙️ Spécifications & Carnet d'Entretien</h3>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:0.75rem; font-size:0.85rem;">
                <div style="background:rgba(30,41,59,0.5); padding:0.75rem; border-radius:6px; border:1px solid rgba(51,65,85,0.5);">
                    <div style="color:#64748b; font-size:0.75rem;">CONSOMMATION MOYENNE</div>
                    <div style="font-weight:700; color:#f8fafc; margin-top:2px;">18.5 L/heure (GNR B100)</div>
                </div>
                <div style="background:rgba(30,41,59,0.5); padding:0.75rem; border-radius:6px; border:1px solid rgba(51,65,85,0.5);">
                    <div style="color:#64748b; font-size:0.75rem;">CACES EXIGÉ</div>
                    <div style="font-weight:700; color:var(--emerald); margin-top:2px;">R482 Catégorie B1 / C1</div>
                </div>
                <div style="background:rgba(30,41,59,0.5); padding:0.75rem; border-radius:6px; border:1px solid rgba(51,65,85,0.5);">
                    <div style="color:#64748b; font-size:0.75rem;">CLASSE ÉMISSION</div>
                    <div style="font-weight:700; color:#38bdf8; margin-top:2px;">Stage V / Filtre à Particules</div>
                </div>
                <div style="background:rgba(30,41,59,0.5); padding:0.75rem; border-radius:6px; border:1px solid rgba(51,65,85,0.5);">
                    <div style="color:#64748b; font-size:0.75rem;">GÉOLOCALISATION GPS</div>
                    <div style="font-weight:700; color:var(--emerald); margin-top:2px;">🟢 Balise Active (Télématique 4G)</div>
                </div>
            </div>
        `;
        openModal('vehicle-details-modal');
    }
"""

def get_js_part2_continued():
    return """
    // ==========================================
    // 9. TOOLS & MATERIALS CATALOG ENGINE
    // ==========================================
    function filterCatalog(cat, btn) {
        catalogFilter = cat;
        document.querySelectorAll('.catalog-filter-btn').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
        renderCatalogGrid();
    }

    function renderCatalogGrid() {
        const grid = document.getElementById('catalog-grid');
        if (!grid || !companyData.catalog) return;

        const filtered = companyData.catalog.filter(c => catalogFilter === 'all' || c.category === catalogFilter);

        grid.innerHTML = filtered.map(item => `
            <div class="card" style="display:flex; flex-direction:column; justify-content:space-between;">
                <div>
                    <div style="height:120px; margin-bottom:0.75rem; border-radius:6px; overflow:hidden; border:1px solid rgba(51,65,85,0.5);">
                        ${getToolMaterialSVG(item.id, item.name)}
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.25rem;">
                        <span class="badge ${item.stock > 10 ? 'badge-success' : 'badge-warning'}">Stock: ${item.stock} ${item.unit}</span>
                        <span style="font-family:'JetBrains Mono'; font-size:0.75rem; color:#64748b;">${item.id}</span>
                    </div>
                    <h3 style="font-size:1rem; font-weight:800; color:#f8fafc; margin-bottom:0.25rem;">${item.name}</h3>
                    <div style="font-size:0.75rem; color:#94a3b8; margin-bottom:0.75rem;">Fournisseur : <strong style="color:#cbd5e1;">${item.supplier}</strong></div>

                    <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(15,23,42,0.6); padding:0.5rem 0.75rem; border-radius:6px; border:1px solid rgba(51,65,85,0.4); margin-bottom:0.75rem;">
                        <span style="font-size:0.75rem; color:#64748b;">Prix Unitaire HT</span>
                        <span style="font-family:'JetBrains Mono'; font-weight:800; font-size:1rem; color:var(--emerald);">${item.unit_price.toFixed(2)} € / ${item.unit}</span>
                    </div>
                </div>

                <button class="btn btn-primary" style="font-size:0.75rem; padding:0.4rem;" onclick="openCatalogItemModal('${item.id}')">
                    🔍 Fiche Technique Produit
                </button>
            </div>
        `).join('');
    }

    function openCatalogItemModal(itemId) {
        const item = (companyData.catalog || []).find(x => x.id === itemId);
        if (!item) return;

        const body = document.getElementById('catalog-item-modal-body');
        if (!body) return;

        body.innerHTML = `
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1.5rem; margin-bottom:1.5rem;">
                <div style="height:200px; border-radius:8px; overflow:hidden; border:1px solid rgba(51,65,85,0.8);">
                    ${getToolMaterialSVG(item.id, item.name)}
                </div>
                <div>
                    <span class="badge badge-info">${item.category.toUpperCase()}</span>
                    <h2 style="font-size:1.4rem; font-weight:900; color:#f8fafc; margin-top:0.35rem;">${item.name}</h2>
                    <div style="color:#94a3b8; font-size:0.85rem; margin-bottom:1rem;">Réf Fournisseur : <strong style="color:#38bdf8;">${item.supplier}</strong> (Réf: ${item.id})</div>

                    <div style="background:rgba(15,23,42,0.8); padding:0.85rem; border-radius:6px; border:1px solid rgba(51,65,85,0.6); font-size:0.85rem;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem;">
                            <span style="color:#64748b;">Prix Unitaire Achat HT :</span>
                            <strong style="font-family:'JetBrains Mono'; color:var(--emerald); font-size:1.1rem;">${item.unit_price.toFixed(2)} € / ${item.unit}</strong>
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem;">
                            <span style="color:#64748b;">Stock Actuel Dépôt :</span>
                            <strong style="font-family:'JetBrains Mono'; color:#38bdf8;">${item.stock} ${item.unit}</strong>
                        </div>
                        <div style="display:flex; justify-content:space-between;">
                            <span style="color:#64748b;">Norme de Conformité :</span>
                            <strong style="color:#f8fafc;">${item.norm || 'NF EN 1340 / CE'}</strong>
                        </div>
                    </div>
                </div>
            </div>

            <div style="background:rgba(2,132,199,0.1); border-left:3px solid #0284c7; padding:0.85rem; border-radius:6px; font-size:0.85rem; color:#cbd5e1; margin-bottom:1.25rem;">
                <strong>Consignes de Manutention & Pose :</strong> Manipuler obligatoirement avec pinces et élingues homologuées. Stockage sur sol stabilisé et calé. Port des gants et chaussures de sécurité obligatoire lors de la manipulation.
            </div>

            <div style="display:flex; justify-content:flex-end; gap:0.5rem;">
                <button class="btn btn-secondary" onclick="closeModal('catalog-item-modal')">Fermer</button>
                <button class="btn btn-primary" onclick="alert('Commande de réapprovisionnement transmise à l\'acheteur !'); closeModal('catalog-item-modal');">🛒 Créer Bon de Commande</button>
            </div>
        `;
        openModal('catalog-item-modal');
    }

    // ==========================================
    // 10. HR ORGANIGRAM TREE ENGINE
    // ==========================================
    function initHrTree() {
        const container = document.getElementById('hr-tree-container');
        if (!container || !companyData.hr_hierarchy) return;

        const h = companyData.hr_hierarchy;

        container.innerHTML = `
            <div style="display:flex; flex-direction:column; align-items:center; gap:1.5rem; min-width:800px; padding:1rem;">
                <!-- DIRECTION -->
                <div style="background:rgba(30,41,59,0.95); border:2px solid #06b6d4; border-radius:10px; padding:1rem 1.5rem; text-align:center; width:300px; box-shadow:0 4px 15px rgba(6,182,212,0.2);">
                    <div style="font-size:1.5rem; margin-bottom:0.25rem;">👑</div>
                    <div style="font-weight:900; font-size:1.1rem; color:#f8fafc;">${h.director.name}</div>
                    <div style="font-size:0.8rem; color:#38bdf8; font-weight:700;">${h.director.role}</div>
                    <div style="font-size:0.75rem; color:#94a3b8; margin-top:0.25rem;">Certifié : ${h.director.cert}</div>
                </div>

                <div style="width:2px; height:24px; background:#06b6d4;"></div>

                <!-- CONDUCTEURS -->
                <div style="display:flex; gap:2rem; justify-content:center; width:100%;">
                    ${h.conducteurs.map(cd => `
                        <div style="flex:1; max-width:380px; display:flex; flex-direction:column; align-items:center;">
                            <div style="background:rgba(30,41,59,0.9); border:1px solid #3b82f6; border-radius:8px; padding:1rem; text-align:center; width:100%; box-shadow:0 4px 10px rgba(0,0,0,0.3);">
                                <div style="font-size:1.3rem; margin-bottom:0.25rem;">👷‍♂️</div>
                                <div style="font-weight:800; font-size:1rem; color:#f8fafc;">${cd.name}</div>
                                <div style="font-size:0.8rem; color:#38bdf8; font-weight:700;">${cd.role}</div>
                                <div style="font-size:0.75rem; color:#cbd5e1; margin-top:0.25rem;">Chantiers : <strong>${cd.assigned.join(', ')}</strong></div>
                            </div>

                            <div style="width:2px; height:20px; background:#3b82f6;"></div>

                            <!-- CHEFS & ÉQUIPES -->
                            <div style="display:flex; flex-direction:column; gap:0.75rem; width:100%;">
                                ${cd.chefs.map(ch => `
                                    <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(51,65,85,0.7); border-radius:8px; padding:0.75rem; width:100%;">
                                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.35rem;">
                                            <strong style="color:#f8fafc; font-size:0.85rem;">🚜 ${ch.name}</strong>
                                            <span class="badge badge-success" style="font-size:0.65rem;">Chef de Chantier</span>
                                        </div>
                                        <div style="font-size:0.75rem; color:#94a3b8; margin-bottom:0.5rem;">Affecté à : <strong style="color:#38bdf8;">${ch.site}</strong></div>
                                        <div style="border-top:1px solid rgba(51,65,85,0.4); padding-top:0.35rem; font-size:0.75rem; color:#cbd5e1;">
                                            <span style="color:#64748b;">Équipe :</span> ${ch.workers.join(', ')}
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    // ==========================================
    // 11. OPBTP SIGNAGE CALCULATOR
    // ==========================================
    function calculateSignage() {
        const roadType = document.getElementById('opbtp-road-type')?.value || 'urbain';
        const speed = document.getElementById('opbtp-speed')?.value || '50';
        const length = parseFloat(document.getElementById('opbtp-length')?.value || 100);

        let dApproach = 50;
        let dInterPanneaux = 30;
        let taperRatio = 15;
        let conesCount = Math.max(10, Math.ceil(length / 5));

        if (roadType === 'bidirectionnel') {
            dApproach = (speed === '80' || speed === '90') ? 150 : 100;
            dInterPanneaux = 50;
            taperRatio = 25;
            conesCount = Math.max(20, Math.ceil(length / 3));
        } else if (roadType === 'autoroute') {
            dApproach = 500;
            dInterPanneaux = 100;
            taperRatio = 50;
            conesCount = Math.max(50, Math.ceil(length / 2));
        }

        const out = document.getElementById('opbtp-results');
        if (!out) return;

        out.innerHTML = `
            <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(51,65,85,0.7); border-radius:8px; padding:1.25rem;">
                <h4 style="font-size:1.1rem; font-weight:800; color:#38bdf8; margin-bottom:1rem;">📋 Résultats du Calcul Réglementaire OPBTP</h4>

                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:1rem; margin-bottom:1.25rem;">
                    <div style="background:rgba(30,41,59,0.5); padding:0.85rem; border-radius:6px; border:1px solid rgba(51,65,85,0.4);">
                        <div style="font-size:0.75rem; color:#64748b;">DISTANCE PRÉ-SIGNALISATION (AK5)</div>
                        <div style="font-size:1.3rem; font-weight:900; color:var(--emerald); font-family:'JetBrains Mono'; margin-top:2px;">${dApproach} m</div>
                    </div>
                    <div style="background:rgba(30,41,59,0.5); padding:0.85rem; border-radius:6px; border:1px solid rgba(51,65,85,0.4);">
                        <div style="font-size:0.75rem; color:#64748b;">ESPACEMENT ENTRE PANNEAUX</div>
                        <div style="font-size:1.3rem; font-weight:900; color:#38bdf8; font-family:'JetBrains Mono'; margin-top:2px;">${dInterPanneaux} m</div>
                    </div>
                    <div style="background:rgba(30,41,59,0.5); padding:0.85rem; border-radius:6px; border:1px solid rgba(51,65,85,0.4);">
                        <div style="font-size:0.75rem; color:#64748b;">LONGUEUR DU BIAIS (K5a)</div>
                        <div style="font-size:1.3rem; font-weight:900; color:var(--amber); font-family:'JetBrains Mono'; margin-top:2px;">${taperRatio} m</div>
                    </div>
                    <div style="background:rgba(30,41,59,0.5); padding:0.85rem; border-radius:6px; border:1px solid rgba(51,65,85,0.4);">
                        <div style="font-size:0.75rem; color:#64748b;">CÔNES K5a RECOMMANDÉS</div>
                        <div style="font-size:1.3rem; font-weight:900; color:#f8fafc; font-family:'JetBrains Mono'; margin-top:2px;">${conesCount} unités</div>
                    </div>
                </div>

                <div style="background:rgba(234,179,8,0.1); border-left:3px solid #eab308; padding:0.85rem; border-radius:6px; font-size:0.85rem; color:#fef08a;">
                    <strong>Séquence de Panneaux Réglementaire :</strong> AK5 (Travaux) ➜ B14 (Limitation Vitesse ${speed} km/h) ➜ BK15 (Interdiction de dépasser) ➜ AK3 (Rétrécissement) ➜ B21b (Obligation de contournement).
                </div>
            </div>
        `;
    }

    // ==========================================
    // 12. RDC DAILY LOGBOOK ENGINE
    // ==========================================
    function saveRdcEntry() {
        const proj = document.getElementById('rdc-proj-select')?.value;
        const date = document.getElementById('rdc-date')?.value || new Date().toISOString().split('T')[0];
        const chief = document.getElementById('rdc-chief')?.value || 'M. Traoré';
        const weather = document.getElementById('rdc-weather')?.value || 'Ensoleillé (22°C)';
        const desc = document.getElementById('rdc-desc')?.value || 'Pose de bordures et caniveaux sur section A.';
        const hMO = parseFloat(document.getElementById('rdc-heures-mo')?.value || 35);
        const hEng = parseFloat(document.getElementById('rdc-heures-engins')?.value || 14);

        if (!reportsData.rdc_entries) reportsData.rdc_entries = [];

        const newEntry = {
            id: `RDC-${Date.now().toString().slice(-4)}`,
            project: proj,
            date: date,
            chief: chief,
            weather: weather,
            notes: desc,
            hours_mo: hMO,
            hours_engins: hEng,
            incidents: 'Aucun'
        };

        reportsData.rdc_entries.unshift(newEntry);
        renderRdcTable();
        logCockpit(`Rapport journalier de chantier enregistré pour le projet ${proj}.`, 'ok');
        alert('Rapport RDC enregistré avec succès dans le registre chantiers !');
    }

    function renderRdcTable() {
        const tbody = document.getElementById('rdc-table-body');
        if (!tbody || !reportsData.rdc_entries) return;

        tbody.innerHTML = reportsData.rdc_entries.map(r => `
            <tr style="border-bottom:1px solid rgba(51,65,85,0.3);">
                <td style="padding:0.75rem; font-family:'JetBrains Mono'; font-weight:700; color:#38bdf8;">${r.id}</td>
                <td style="padding:0.75rem; font-weight:600; color:#f8fafc;">${r.project}</td>
                <td style="padding:0.75rem; font-family:'JetBrains Mono'; color:#94a3b8;">${r.date}</td>
                <td style="padding:0.75rem; color:#cbd5e1;">${r.chief}</td>
                <td style="padding:0.75rem; font-size:0.8rem; color:#94a3b8; max-width:260px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${r.notes}</td>
                <td style="padding:0.75rem; font-family:'JetBrains Mono'; color:var(--emerald); font-weight:700;">${r.hours_mo} h</td>
                <td style="padding:0.75rem; font-family:'JetBrains Mono'; color:#f59e0b; font-weight:700;">${r.hours_engins} h</td>
                <td style="padding:0.75rem;">
                    <button class="btn btn-secondary" style="padding:0.25rem 0.5rem; font-size:0.7rem;" onclick="downloadProjectDoc('${r.id}_RDC_${r.date}', '${r.project}', 'pdf')">
                        📄 PDF
                    </button>
                </td>
            </tr>
        `).join('');
    }
"""
