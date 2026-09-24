#!/usr/bin/env python3
"""
Patch v53: Inject Advanced Calculators & Enterprise Handlers into scripts/section_js_part3.py
"""

with open("scripts/section_js_part3.py", "r", encoding="utf-8") as f:
    js_text = f.read()

# Update setTechniqueViewMode
old_set_tech_view = """function setTechniqueViewMode(mode) {
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

        if (mode === 'tasksheet') renderTaskSheet();
        if (mode === 'enrobes_2d') renderAsphalt2DSimulation();
    }"""

new_set_tech_view = """function setTechniqueViewMode(mode) {
        techniqueViewMode = mode;
        document.querySelectorAll('.tech-view-btn').forEach(b => b.classList.remove('active'));
        const btnId = 'btn-tech-' + mode.replace('_', '');
        const btn = document.getElementById(btnId);
        if (btn) btn.classList.add('active');

        const fView = document.getElementById('tech-formulas-view');
        const hView = document.getElementById('tech-hydraulique-view');
        const bView = document.getElementById('tech-bruckner-view');
        const rView = document.getElementById('tech-reseauxsecs-view');
        const eView = document.getElementById('tech-enrobes-2d-view');
        const cView = document.getElementById('tech-compactage-cut-view');
        const tView = document.getElementById('tech-tasksheet-view');

        if (fView) fView.style.display = mode === 'formulas' ? 'block' : 'none';
        if (hView) hView.style.display = mode === 'hydraulique' ? 'block' : 'none';
        if (bView) bView.style.display = mode === 'bruckner' ? 'block' : 'none';
        if (rView) rView.style.display = mode === 'reseauxsecs' ? 'block' : 'none';
        if (eView) eView.style.display = mode === 'enrobes_2d' ? 'block' : 'none';
        if (cView) cView.style.display = mode === 'compactage' ? 'block' : 'none';
        if (tView) tView.style.display = mode === 'tasksheet' ? 'block' : 'none';

        if (mode === 'hydraulique') { updateHydrauliqueCalculation(); updateBassinCalculation(); }
        if (mode === 'bruckner') { renderBrucknerEngine(); }
        if (mode === 'reseauxsecs') { updateElectriqueCalculation(); updateEPCalculation(); }
        if (mode === 'tasksheet') renderTaskSheet();
        if (mode === 'enrobes_2d') renderAsphalt2DSimulation();
    }"""

js_text = js_text.replace(old_set_tech_view, new_set_tech_view)

# Update setRdcViewMode to handle livraisons
old_set_rdc_view = """function setRdcViewMode(mode) {
        rdcViewMode = mode;
        document.querySelectorAll('.rdc-view-btn').forEach(b => b.classList.remove('active'));
        const btn = document.getElementById('btn-rdc-' + mode);
        if (btn) btn.classList.add('active');

        const rapView = document.getElementById('rdc-rapport-view');
        const ptgView = document.getElementById('rdc-pointage-view');
        const renView = document.getElementById('rdc-rentabilite-view');

        if (rapView) rapView.style.display = mode === 'rapport' ? 'block' : 'none';
        if (ptgView) ptgView.style.display = mode === 'pointage' ? 'block' : 'none';
        if (renView) renView.style.display = mode === 'rentabilite' ? 'block' : 'none';

        if (mode === 'pointage') renderCrewPointageTable();
        if (mode === 'rentabilite') renderRdcRentabiliteTable();
    }"""

new_set_rdc_view = """function setRdcViewMode(mode) {
        rdcViewMode = mode;
        document.querySelectorAll('.rdc-view-btn').forEach(b => b.classList.remove('active'));
        const btn = document.getElementById('btn-rdc-' + mode);
        if (btn) btn.classList.add('active');

        const rapView = document.getElementById('rdc-rapport-view');
        const ptgView = document.getElementById('rdc-pointage-view');
        const renView = document.getElementById('rdc-rentabilite-view');
        const livView = document.getElementById('rdc-livraisons-view');

        if (rapView) rapView.style.display = mode === 'rapport' ? 'block' : 'none';
        if (ptgView) ptgView.style.display = mode === 'pointage' ? 'block' : 'none';
        if (renView) renView.style.display = mode === 'rentabilite' ? 'block' : 'none';
        if (livView) livView.style.display = mode === 'livraisons' ? 'block' : 'none';

        if (mode === 'pointage') renderCrewPointageTable();
        if (mode === 'rentabilite') renderRdcRentabiliteTable();
        if (mode === 'livraisons') renderRdcLivraisonsTable();
    }"""

js_text = js_text.replace(old_set_rdc_view, new_set_rdc_view)

# Update setPlanningViewMode to handle intemperies
old_set_plan_view = """function setPlanningViewMode(mode) {
        planningViewMode = mode;
        document.querySelectorAll('.plan-view-btn').forEach(b => b.classList.remove('active'));
        const btn = document.getElementById('btn-plan-' + mode);
        if (btn) btn.classList.add('active');

        const gView = document.getElementById('planning-gantt-view');
        const aView = document.getElementById('planning-agenda-view');
        const tView = document.getElementById('planning-taches-view');

        if (gView) gView.style.display = mode === 'gantt' ? 'block' : 'none';
        if (aView) aView.style.display = mode === 'agenda' ? 'block' : 'none';
        if (tView) tView.style.display = mode === 'taches' ? 'block' : 'none';
    }"""

new_set_plan_view = """function setPlanningViewMode(mode) {
        planningViewMode = mode;
        document.querySelectorAll('.plan-view-btn').forEach(b => b.classList.remove('active'));
        const btn = document.getElementById('btn-plan-' + mode);
        if (btn) btn.classList.add('active');

        const gView = document.getElementById('planning-gantt-view');
        const aView = document.getElementById('planning-agenda-view');
        const tView = document.getElementById('planning-taches-view');
        const iView = document.getElementById('planning-intemperies-view');

        if (gView) gView.style.display = mode === 'gantt' ? 'block' : 'none';
        if (aView) aView.style.display = mode === 'agenda' ? 'block' : 'none';
        if (tView) tView.style.display = mode === 'taches' ? 'block' : 'none';
        if (iView) iView.style.display = mode === 'intemperies' ? 'block' : 'none';

        if (mode === 'intemperies') renderPlanningIntemperiesTable();
    }"""

js_text = js_text.replace(old_set_plan_view, new_set_plan_view)

# Now append all new engine logic
v53_js_engine = """

    /* ========================================================================== */
    /* V53: ADVANCED HYDRAULICS & BASSIN SIZING ENGINE                           */
    /* ========================================================================== */
    function updateHydrauliqueCalculation() {
        const matK = parseFloat(document.getElementById('hydrau-materiau')?.value || 100);
        const dnMm = parseFloat(document.getElementById('hydrau-dn')?.value || 300);
        const pentePct = parseFloat(document.getElementById('hydrau-pente')?.value || 1.5);
        const fillPct = parseFloat(document.getElementById('hydrau-fill')?.value || 50);

        const D = dnMm / 1000;
        const I = Math.max(0.0001, pentePct / 100);
        const hOverD = Math.max(0.01, Math.min(1.0, fillPct / 100));

        // Full Section
        const S_ps = (Math.PI * Math.pow(D, 2)) / 4;
        const Rh_ps = D / 4;
        const V_ps = matK * Math.pow(Rh_ps, 2/3) * Math.sqrt(I);
        const Q_ps = S_ps * V_ps * 1000; // L/s

        // Partial Section
        const h = hOverD * D;
        const theta = 2 * Math.acos(Math.max(-1, Math.min(1, 1 - 2 * hOverD))); // rad
        const S = (Math.pow(D, 2) / 8) * (theta - Math.sin(theta));
        const Pm = (D * theta) / 2;
        const Rh = Pm > 0 ? S / Pm : 0;
        const L_miroir = D * Math.sin(theta / 2);
        const V = matK * Math.pow(Rh, 2/3) * Math.sqrt(I);
        const Q = S * V * 1000; // L/s

        // Update DOM
        const qpsEl = document.getElementById('hydrau-qps-res');
        const qEl = document.getElementById('hydrau-q-res');
        const vEl = document.getElementById('hydrau-v-res');
        const autoEl = document.getElementById('hydrau-autocurage-res');
        const badgeEl = document.getElementById('hydrau-schema-badge');
        const sDet = document.getElementById('hydrau-s-detail');
        const rhDet = document.getElementById('hydrau-rh-detail');
        const lDet = document.getElementById('hydrau-l-detail');

        if (qpsEl) qpsEl.textContent = Q_ps.toFixed(1) + ' L/s (' + (Q_ps * 3.6).toFixed(1) + ' m³/h)';
        if (qEl) qEl.textContent = Q.toFixed(1) + ' L/s (' + (Q * 3.6).toFixed(1) + ' m³/h)';
        if (vEl) vEl.textContent = V.toFixed(2) + ' m/s';
        if (sDet) sDet.textContent = (S * 10000).toFixed(1) + ' cm² (' + S.toFixed(4) + ' m²)';
        if (rhDet) rhDet.textContent = (Rh * 100).toFixed(1) + ' cm';
        if (lDet) lDet.textContent = (L_miroir * 100).toFixed(1) + ' cm';
        if (badgeEl) badgeEl.textContent = 'DN ' + dnMm + ' mm | Pente ' + pentePct.toFixed(2) + '% | Remplissage ' + fillPct + '%';

        if (autoEl) {
            if (V >= 0.70 && V <= 3.0) {
                autoEl.className = 'badge badge-success';
                autoEl.textContent = '✅ Conforme Fascicule 70 (0.7 à 3.0 m/s)';
            } else if (V < 0.70) {
                autoEl.className = 'badge badge-warning';
                autoEl.textContent = '⚠️ Risque d\'ensablement (V < 0.70 m/s)';
            } else {
                autoEl.className = 'badge badge-danger';
                autoEl.textContent = '🚨 Risque d\'érosion (V > 3.0 m/s)';
            }
        }

        renderHydrauliqueSVG(dnMm, fillPct, V, Q);
    }

    function renderHydrauliqueSVG(dnMm, fillPct, V, Q) {
        const container = document.getElementById('hydrau-svg-container');
        if (!container) return;

        const R = 90;
        const cx = 160;
        const cy = 135;
        const fillFrac = fillPct / 100;
        const waterHeight = 2 * R * fillFrac;
        const waterY = cy + R - waterHeight;

        // Angle for arc
        const hOverD = fillFrac;
        const theta = 2 * Math.acos(Math.max(-1, Math.min(1, 1 - 2 * hOverD)));
        const halfAngle = theta / 2;
        const x1 = cx - R * Math.sin(halfAngle);
        const y1 = cy + R * Math.cos(halfAngle);
        const x2 = cx + R * Math.sin(halfAngle);
        const y2 = cy + R * Math.cos(halfAngle);
        const largeArc = theta > Math.PI ? 1 : 0;

        let waterPath = '';
        if (fillPct >= 99) {
            waterPath = `<circle cx="${cx}" cy="${cy}" r="${R}" fill="rgba(56,189,248,0.45)"/>`;
        } else if (fillPct <= 1) {
            waterPath = '';
        } else {
            waterPath = `<path d="M ${x1} ${y1} A ${R} ${R} 0 ${largeArc} 0 ${x2} ${y2} Z" fill="rgba(56,189,248,0.5)" stroke="#38bdf8" stroke-width="2"/>`;
        }

        const svg = `
            <svg viewBox="0 0 320 270" width="100%" height="260" style="max-height: 260px;">
                <defs>
                    <linearGradient id="pipeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#334155"/>
                        <stop offset="100%" stop-color="#0f172a"/>
                    </linearGradient>
                    <linearGradient id="waterFlow" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#0284c7"/>
                        <stop offset="100%" stop-color="#38bdf8"/>
                    </linearGradient>
                </defs>
                <!-- Trench Background -->
                <rect x="20" y="20" width="280" height="230" rx="6" fill="#090d16" stroke="#1e293b"/>
                
                <!-- Pipe Outer & Inner Wall -->
                <circle cx="${cx}" cy="${cy}" r="${R + 12}" fill="url(#pipeGrad)" stroke="#475569" stroke-width="3"/>
                <circle cx="${cx}" cy="${cy}" r="${R}" fill="#020617" stroke="#64748b" stroke-width="2"/>
                
                <!-- Water Area -->
                ${waterPath}
                
                <!-- Water Surface Line -->
                ${fillPct > 1 && fillPct < 99 ? `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#7dd3fc" stroke-width="2" stroke-dasharray="4,2"/>` : ''}
                
                <!-- Dimension Markers -->
                <line x1="${cx - R}" y1="${cy + R + 18}" x2="${cx + R}" y2="${cy + R + 18}" stroke="#94a3b8" stroke-width="1.5"/>
                <circle cx="${cx - R}" cy="${cy + R + 18}" r="2" fill="#94a3b8"/>
                <circle cx="${cx + R}" cy="${cy + R + 18}" r="2" fill="#94a3b8"/>
                <text x="${cx}" y="${cy + R + 32}" fill="#94a3b8" font-size="11" text-anchor="middle" font-weight="700">DN ${dnMm} mm</text>
                
                <!-- Water Depth Indicator -->
                <line x1="45" y1="${cy + R}" x2="45" y2="${cy + R - waterHeight}" stroke="#38bdf8" stroke-width="1.5"/>
                <line x1="40" y1="${cy + R}" x2="50" y2="${cy + R}" stroke="#38bdf8" stroke-width="1.5"/>
                <line x1="40" y1="${cy + R - waterHeight}" x2="50" y2="${cy + R - waterHeight}" stroke="#38bdf8" stroke-width="1.5"/>
                <text x="55" y="${cy + R - waterHeight / 2 + 4}" fill="#38bdf8" font-size="10" font-weight="700">h = ${(dnMm * fillFrac).toFixed(0)} mm</text>

                <!-- Flow velocity arrow -->
                <g transform="translate(${cx - 30}, ${cy - 10})">
                    <rect x="0" y="0" width="60" height="22" rx="4" fill="rgba(15,23,42,0.85)" stroke="#38bdf8"/>
                    <text x="30" y="15" fill="#38bdf8" font-size="11" font-weight="800" text-anchor="middle">➔ ${V.toFixed(2)} m/s</text>
                </g>
            </svg>
        `;
        container.innerHTML = svg;
    }

    function updateBassinCalculation() {
        const A_ha = parseFloat(document.getElementById('bassin-surface')?.value || 2.5);
        const C = parseFloat(document.getElementById('bassin-coef-c')?.value || 0.5);
        const H_pluie = parseFloat(document.getElementById('bassin-pluie')?.value || 45.0);
        const q_fuite_spec = parseFloat(document.getElementById('bassin-qfuite-spec')?.value || 2.0);

        const Q_fuite_total = q_fuite_spec * A_ha; // L/s
        const V_brut = 10 * H_pluie * A_ha * C; // m3
        const V_utile = V_brut * 0.88; // m3 factoring discharge during storm
        
        // Orifice sizing for ajutage under 1.50m water head: Q = mu * S * sqrt(2*g*H)
        const H_eau = 1.50; // m
        const mu = 0.62;
        const S_ajutage = (Q_fuite_total / 1000) / (mu * Math.sqrt(2 * 9.81 * H_eau)); // m2
        const D_ajutage_mm = Math.sqrt((4 * S_ajutage) / Math.PI) * 1000;

        const vRes = document.getElementById('bassin-volume-res');
        const qfRes = document.getElementById('bassin-qfuite-total-res');
        const ajRes = document.getElementById('bassin-ajutage-res');

        if (vRes) vRes.textContent = Math.round(V_utile) + ' m³ (' + (V_utile * 1.15).toFixed(0) + ' m³ avec risberme)';
        if (qfRes) qfRes.textContent = Q_fuite_total.toFixed(2) + ' L/s (' + (Q_fuite_total * 3.6).toFixed(1) + ' m³/h)';
        if (ajRes) ajRes.textContent = 'Ø ' + Math.round(D_ajutage_mm) + ' mm (Ajutage calibré sous 1.50 m)';
    }

    /* ========================================================================== */
    /* V53: BRUCKNER EARTHWORK & MASS HAUL CURVE ENGINE (LALANNE)                */
    /* ========================================================================== */
    const brucknerProfiles = [
        { pk: 'PK 0+000', dist: 0, sDeb: 18.5, sRem: 0.0, desc: 'Tête amont giratoire' },
        { pk: 'PK 0+100', dist: 100, sDeb: 24.0, sRem: 2.1, desc: 'Déblai rocheux meuble' },
        { pk: 'PK 0+200', dist: 100, sDeb: 32.5, sRem: 0.0, desc: 'Tranchée axe principal' },
        { pk: 'PK 0+300', dist: 100, sDeb: 21.0, sRem: 4.5, desc: 'Zone de transition' },
        { pk: 'PK 0+400', dist: 100, sDeb: 12.0, sRem: 15.0, desc: 'Point de passage Déblai/Remblai' },
        { pk: 'PK 0+500', dist: 100, sDeb: 2.5, sRem: 28.0, desc: 'Remblai accès échangeur' },
        { pk: 'PK 0+600', dist: 100, sDeb: 0.0, sRem: 35.0, desc: 'Grand remblai ouvrage' },
        { pk: 'PK 0+700', dist: 100, sDeb: 0.0, sRem: 22.0, desc: 'Remblai sur sol compressible' },
        { pk: 'PK 0+800', dist: 100, sDeb: 8.5, sRem: 12.0, desc: 'Transition vers raccordement' },
        { pk: 'PK 0+900', dist: 100, sDeb: 19.0, sRem: 4.0, desc: 'Déblai talutage 3H/2V' },
        { pk: 'PK 1+000', dist: 100, sDeb: 26.5, sRem: 0.0, desc: 'Déblai arase terrassement' },
        { pk: 'PK 1+100', dist: 100, sDeb: 15.0, sRem: 6.0, desc: 'Pente longitudinale 2%' },
        { pk: 'PK 1+200', dist: 100, sDeb: 0.0, sRem: 18.0, desc: 'Raccordement voirie existante' }
    ];

    function renderBrucknerEngine() {
        const tbody = document.getElementById('bruckner-table-body');
        if (!tbody) return;

        let cumVol = 0;
        let totalDeb = 0;
        let totalRem = 0;
        const calculatedProfiles = [];

        tbody.innerHTML = '';
        for (let i = 0; i < brucknerProfiles.length; i++) {
            const p = brucknerProfiles[i];
            let vDeb = 0;
            let vRem = 0;

            if (i > 0) {
                const prev = brucknerProfiles[i - 1];
                const dL = p.dist;
                vDeb = ((prev.sDeb + p.sDeb) / 2) * dL;
                vRem = ((prev.sRem + p.sRem) / 2) * dL;
            }

            // Factoring bulking 1.20 and compaction 0.90
            const vDebComp = vDeb * 1.20 * 0.85; // compactable
            const vRemComp = vRem * 0.90;
            const deltaV = vDebComp - vRemComp;
            cumVol += deltaV;
            totalDeb += vDeb * 1.20;
            totalRem += vRem * 0.90;

            let reco = '';
            if (cumVol > 2000) reco = '🚚 Réutilisation interne ➔ Tombereau 6x6';
            else if (cumVol < -1000) reco = '🚛 Emprunt extérieur GNT nécessaire';
            else reco = '⚖️ Équilibre local ➔ Bull / Pelle';

            calculatedProfiles.push({ ...p, vDeb, vRem, cumVol, reco });

            const tr = document.createElement('tr');
            tr.style.borderBottom = '1px solid var(--border)';
            tr.innerHTML = `
                <td style="padding: 6px 10px; font-weight: 700; color: #e2e8f0;">${p.pk}</td>
                <td style="padding: 6px 10px; color: #94a3b8;">${p.dist} m</td>
                <td style="padding: 6px 10px; color: #38bdf8; font-weight: 600;">${p.sDeb.toFixed(1)} m²</td>
                <td style="padding: 6px 10px; color: #ef4444; font-weight: 600;">${p.sRem.toFixed(1)} m²</td>
                <td style="padding: 6px 10px; color: #38bdf8;">${vDeb > 0 ? Math.round(vDeb) + ' m³' : '-'}</td>
                <td style="padding: 6px 10px; color: #ef4444;">${vRem > 0 ? Math.round(vRem) + ' m³' : '-'}</td>
                <td style="padding: 6px 10px; color: ${cumVol >= 0 ? '#22c55e' : '#ef4444'}; font-weight: 800;">${cumVol > 0 ? '+' : ''}${Math.round(cumVol)} m³</td>
                <td style="padding: 6px 10px; color: #a855f7; font-size: 0.75rem;">${reco}</td>
            `;
            tbody.appendChild(tr);
        }

        // Update KPIs
        const totDebEl = document.getElementById('bruckner-total-deb');
        const totRemEl = document.getElementById('bruckner-total-rem');
        const soldeEl = document.getElementById('bruckner-solde');
        const dmtEl = document.getElementById('bruckner-dmt');

        if (totDebEl) totDebEl.textContent = Math.round(totalDeb).toLocaleString() + ' m³';
        if (totRemEl) totRemEl.textContent = Math.round(totalRem).toLocaleString() + ' m³';
        if (soldeEl) {
            const solde = totalDeb - totalRem;
            soldeEl.textContent = (solde >= 0 ? '+' : '') + Math.round(solde).toLocaleString() + ' m³ (' + (solde >= 0 ? 'Excédent' : 'Déficit') + ')';
            soldeEl.style.color = solde >= 0 ? '#22c55e' : '#ef4444';
        }
        if (dmtEl) dmtEl.textContent = '285 m (Tombereau Articulé 25t)';

        drawBrucknerCanvas(calculatedProfiles);
    }

    function drawBrucknerCanvas(profiles) {
        const canvas = document.getElementById('bruckner-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const W = canvas.width;
        const H = canvas.height;

        ctx.clearRect(0, 0, W, H);

        const padLeft = 70;
        const padRight = 30;
        const padTop = 30;
        const padBottom = 35;
        const plotW = W - padLeft - padRight;
        const plotH = H - padTop - padBottom;

        // Find min and max cumVol
        let minVol = 0;
        let maxVol = 0;
        profiles.forEach(p => {
            if (p.cumVol < minVol) minVol = p.cumVol;
            if (p.cumVol > maxVol) maxVol = p.cumVol;
        });
        const range = Math.max(1000, maxVol - minVol);
        const zeroY = padTop + plotH * (maxVol / range);

        // Draw Grid
        ctx.strokeStyle = '#1e293b';
        ctx.lineWidth = 1;
        for (let g = 0; g <= 4; g++) {
            const gy = padTop + (plotH / 4) * g;
            ctx.beginPath();
            ctx.moveTo(padLeft, gy);
            ctx.lineTo(W - padRight, gy);
            ctx.stroke();

            const val = maxVol - (range / 4) * g;
            ctx.fillStyle = '#64748b';
            ctx.font = '10px Inter, sans-serif';
            ctx.textAlign = 'right';
            ctx.fillText(Math.round(val) + ' m³', padLeft - 8, gy + 3);
        }

        // Draw Zero Line (Ligne de terre)
        ctx.strokeStyle = '#22c55e';
        ctx.lineWidth = 1.5;
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.moveTo(padLeft, zeroY);
        ctx.lineTo(W - padRight, zeroY);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#22c55e';
        ctx.textAlign = 'left';
        ctx.fillText('Ligne d\'équilibre (0 m³)', W - padRight - 120, zeroY - 6);

        // Plot Curve
        ctx.beginPath();
        const pts = [];
        for (let i = 0; i < profiles.length; i++) {
            const x = padLeft + (plotW / (profiles.length - 1)) * i;
            const y = padTop + plotH * ((maxVol - profiles[i].cumVol) / range);
            pts.push({ x, y, p: profiles[i] });
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }

        ctx.strokeStyle = '#f59e0b';
        ctx.lineWidth = 3;
        ctx.stroke();

        // Fill area under curve
        ctx.lineTo(pts[pts.length - 1].x, zeroY);
        ctx.lineTo(pts[0].x, zeroY);
        ctx.closePath();
        ctx.fillStyle = 'rgba(245, 158, 11, 0.12)';
        ctx.fill();

        // Draw profile points and labels
        pts.forEach((pt, idx) => {
            ctx.fillStyle = pt.p.cumVol >= 0 ? '#38bdf8' : '#ef4444';
            ctx.beginPath();
            ctx.arc(pt.x, pt.y, 4, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = '#020617';
            ctx.lineWidth = 1.5;
            ctx.stroke();

            // X-axis label
            if (idx % 2 === 0 || idx === pts.length - 1) {
                ctx.fillStyle = '#94a3b8';
                ctx.font = '9px Inter, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(pt.p.pk, pt.x, H - 12);
            }
        });
    }

    function resetBrucknerData() {
        renderBrucknerEngine();
        showNotification('Données de terrassement Bruckner réinitialisées !', 'info');
    }

    function exportBrucknerCSV() {
        let csv = 'Profil_PK;Distance_m;Section_Deblai_m2;Section_Remblai_m2;Volume_Deblai_m3;Volume_Remblai_m3;Ordonnee_Bruckner_m3;Recommandation\\n';
        brucknerProfiles.forEach(p => {
            csv += `${p.pk};${p.dist};${p.sDeb};${p.sRem};${p.sDeb * 100};${p.sRem * 100};${p.cumVol || 0};${p.desc}\\n`;
        });
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'Bruckner_Cubatures_Terrassement.csv';
        link.click();
        showNotification('Fichier Bruckner CSV exporté avec succès !', 'success');
    }

    /* ========================================================================== */
    /* V53: DRY UTILITIES & ELECTRICAL SIZING (NF C 15-100 / C 17-200)           */
    /* ========================================================================== */
    function updateElectriqueCalculation() {
        const typeAlim = document.getElementById('elec-type-alim')?.value || 'mono';
        const metal = document.getElementById('elec-metal')?.value || 'cuivre';
        const P_watt = parseFloat(document.getElementById('elec-puissance')?.value || 1800);
        const L_m = parseFloat(document.getElementById('elec-longueur')?.value || 250);
        const S_mm2 = parseFloat(document.getElementById('elec-section')?.value || 6.0);

        const rho = metal === 'cuivre' ? 0.0225 : 0.036;
        const cosPhi = 0.90;
        const U_nom = typeAlim === 'mono' ? 230 : 400;

        let Ib = 0;
        let deltaU = 0;

        if (typeAlim === 'mono') {
            Ib = P_watt / (U_nom * cosPhi);
            deltaU = (2 * rho * L_m * Ib * cosPhi) / S_mm2;
        } else {
            Ib = P_watt / (Math.sqrt(3) * U_nom * cosPhi);
            deltaU = (Math.sqrt(3) * rho * L_m * Ib * cosPhi) / S_mm2;
        }

        const deltaUPct = (deltaU / U_nom) * 100;

        const ibEl = document.getElementById('elec-ib-res');
        const duEl = document.getElementById('elec-deltau-res');
        const confEl = document.getElementById('elec-conformite-res');

        if (ibEl) ibEl.textContent = Ib.toFixed(2) + ' A';
        if (duEl) duEl.textContent = deltaU.toFixed(2) + ' V (' + deltaUPct.toFixed(2) + ' %)';

        if (confEl) {
            if (deltaUPct <= 3.0) {
                confEl.className = 'badge badge-success';
                confEl.textContent = '✅ Conforme NF C 17-200 (< 3% éclairage)';
            } else if (deltaUPct <= 5.0) {
                confEl.className = 'badge badge-warning';
                confEl.textContent = '⚠️ Acceptable Tolérance (< 5% max)';
            } else {
                confEl.className = 'badge badge-danger';
                confEl.textContent = '🚨 Non Conforme (> 5% : augmenter section)';
            }
        }

        renderReseauxSecsSVG();
    }

    function updateEPCalculation() {
        const H_m = parseFloat(document.getElementById('ep-hauteur')?.value || 6.0);
        const D_m = parseFloat(document.getElementById('ep-interdist')?.value || 25.0);

        // Standard 55W LED luminaire output ~7500 lm
        const lux = (7500 * 0.72) / (D_m * 7.0) * Math.pow(6.0 / H_m, 1.8);
        const u0 = Math.min(0.65, Math.max(0.30, 0.45 * (24.0 / D_m)));

        const luxEl = document.getElementById('ep-lux-res');
        const u0El = document.getElementById('ep-u0-res');

        if (luxEl) luxEl.textContent = lux.toFixed(1) + ' Lux (Classe M4 Voirie)';
        if (u0El) {
            u0El.textContent = u0.toFixed(2) + (u0 >= 0.40 ? ' (Conforme > 0.40)' : ' (Faible < 0.40)');
            u0El.style.color = u0 >= 0.40 ? '#22c55e' : '#f59e0b';
        }
    }

    function renderReseauxSecsSVG() {
        const container = document.getElementById('reseauxsecs-svg-container');
        if (!container) return;

        const svg = `
            <svg viewBox="0 0 340 270" width="100%" height="260" style="max-height: 260px;">
                <defs>
                    <pattern id="sandPat" width="6" height="6" patternUnits="userSpaceOnUse">
                        <circle cx="2" cy="2" r="1" fill="#78350f" opacity="0.4"/>
                    </pattern>
                </defs>
                <!-- Ground Surface -->
                <rect x="0" y="20" width="340" height="250" fill="#090d16"/>
                <line x1="10" y1="35" x2="330" y2="35" stroke="#94a3b8" stroke-width="2"/>
                <text x="20" y="30" fill="#94a3b8" font-size="10" font-weight="700">NIVEAU DU TROTTOIR / CHAUSSÉE (TN)</text>

                <!-- Trench Wall -->
                <polygon points="40,35 60,240 280,240 300,35" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>

                <!-- Sand Bedding -->
                <polygon points="56,150 60,240 280,240 284,150" fill="url(#sandPat)" stroke="#92400e" stroke-width="1" opacity="0.7"/>

                <!-- Warning Mesh (Grillages Avertisseurs 20cm above) -->
                <!-- Electric Red Mesh -->
                <line x1="80" y1="120" x2="140" y2="120" stroke="#ef4444" stroke-width="3" stroke-dasharray="4,2"/>
                <text x="110" y="115" fill="#ef4444" font-size="8" text-anchor="middle" font-weight="700">GRILLAGE ROUGE (ELEC)</text>

                <!-- Telecom Green Mesh -->
                <line x1="160" y1="130" x2="210" y2="130" stroke="#22c55e" stroke-width="3" stroke-dasharray="4,2"/>
                <text x="185" y="125" fill="#22c55e" font-size="8" text-anchor="middle" font-weight="700">VERT (FIBRE)</text>

                <!-- Conduits in Sand Bedding -->
                <!-- Enedis BT Cable (Red Ø90) -->
                <circle cx="95" cy="180" r="16" fill="#7f1d1d" stroke="#ef4444" stroke-width="2"/>
                <circle cx="95" cy="180" r="12" fill="#020617"/>
                <text x="95" y="183" fill="#ef4444" font-size="8" font-weight="800" text-anchor="middle">BT Ø90</text>

                <!-- EP Cable (Red Ø63) -->
                <circle cx="135" cy="185" r="12" fill="#7f1d1d" stroke="#f87171" stroke-width="2"/>
                <circle cx="135" cy="185" r="9" fill="#020617"/>
                <text x="135" y="188" fill="#f87171" font-size="7" font-weight="800" text-anchor="middle">EP Ø63</text>

                <!-- Telecom Conduit (Green Ø45) -->
                <circle cx="180" cy="190" r="11" fill="#14532d" stroke="#22c55e" stroke-width="2"/>
                <circle cx="180" cy="190" r="8" fill="#020617"/>
                <text x="180" y="193" fill="#22c55e" font-size="7" font-weight="800" text-anchor="middle">FO Ø45</text>

                <!-- Gaz Yellow Pipe (Yellow Ø40) -->
                <circle cx="230" cy="185" r="13" fill="#713f12" stroke="#eab308" stroke-width="2"/>
                <circle cx="230" cy="185" r="10" fill="#020617"/>
                <text x="230" y="188" fill="#eab308" font-size="7" font-weight="800" text-anchor="middle">GAZ Ø40</text>

                <!-- Depth Marker -->
                <line x1="315" y1="35" x2="315" y2="240" stroke="#38bdf8" stroke-width="1.5"/>
                <line x1="310" y1="35" x2="320" y2="35" stroke="#38bdf8" stroke-width="1.5"/>
                <line x1="310" y1="240" x2="320" y2="240" stroke="#38bdf8" stroke-width="1.5"/>
                <text x="310" y="140" fill="#38bdf8" font-size="10" font-weight="700" text-anchor="end">P = 0.80 m</text>
            </svg>
        `;
        container.innerHTML = svg;
    }

    /* ========================================================================== */
    /* V53: MATERIAL DELIVERIES & WEIGH TICKETS TRACKER                          */
    /* ========================================================================== */
    const rdcLivraisonsData = [
        { id: 'BL-8841', date: '2026-09-24 07:45', supplier: 'Colas Centrale Saint-Thibéry', material: 'BBSG 0/10 Classique', truck: 'GA-420-TX (38t)', qty: 29.40, unit: 't', temp: 168, loc: 'Axe 1 - PK 0+000 à 0+120', status: 'Conforme' },
        { id: 'BL-8842', date: '2026-09-24 08:30', supplier: 'Colas Centrale Saint-Thibéry', material: 'BBSG 0/10 Classique', truck: 'EM-912-BB (38t)', qty: 31.10, unit: 't', temp: 165, loc: 'Axe 1 - PK 0+120 à 0+240', status: 'Conforme' },
        { id: 'BL-8843', date: '2026-09-24 09:15', supplier: 'Colas Centrale Saint-Thibéry', material: 'BBSG 0/10 Classique', truck: 'CV-104-LK (8x4)', qty: 18.20, unit: 't', temp: 162, loc: 'Anneau Giratoire', status: 'Conforme' },
        { id: 'BL-8844', date: '2026-09-24 10:00', supplier: 'Carrières GSM Bassin de Thau', material: 'GNT 0/31.5 Non Traitée', truck: 'FG-882-MM (38t)', qty: 32.50, unit: 't', temp: 22, loc: 'Accotement Nord PK 0+400', status: 'Conforme' },
        { id: 'BL-8845', date: '2026-09-24 10:45', supplier: 'Lafarge Holcim Bétons Sète', material: 'Béton C25/30 XF1 Bordures', truck: 'Toupie T-14 (8x4)', qty: 7.50, unit: 'm³', temp: 20, loc: 'Ilot Séparateur Sud', status: 'Conforme' },
        { id: 'BL-8846', date: '2026-09-24 11:30', supplier: 'Carrières GSM Bassin de Thau', material: 'Sable 0/4 Sablon Tranchée', truck: 'BK-552-ZX (8x4)', qty: 16.80, unit: 't', temp: 21, loc: 'Tranchée EP / Telecom', status: 'Conforme' }
    ];

    function renderRdcLivraisonsTable() {
        const tbody = document.getElementById('rdc-livraisons-table-body');
        if (!tbody) return;

        let totEnrobes = 0;
        let totGnt = 0;
        let totBeton = 0;

        tbody.innerHTML = '';
        rdcLivraisonsData.forEach(item => {
            if (item.material.includes('BBSG') || item.material.includes('BBME')) totEnrobes += item.qty;
            if (item.material.includes('GNT')) totGnt += item.qty;
            if (item.material.includes('Béton')) totBeton += item.qty;

            const tr = document.createElement('tr');
            tr.style.borderBottom = '1px solid var(--border)';
            tr.innerHTML = `
                <td style="padding: 6px 10px; font-weight: 700; color: #38bdf8;">${item.id}</td>
                <td style="padding: 6px 10px; color: #94a3b8;">${item.date}</td>
                <td style="padding: 6px 10px; color: #e2e8f0;">${item.supplier}</td>
                <td style="padding: 6px 10px; color: #f59e0b; font-weight: 600;">${item.material}</td>
                <td style="padding: 6px 10px; color: #94a3b8;">${item.truck}</td>
                <td style="padding: 6px 10px; color: #22c55e; font-weight: 800;">${item.qty.toFixed(2)} ${item.unit}</td>
                <td style="padding: 6px 10px; color: ${item.temp >= 150 ? '#ef4444' : '#38bdf8'}; font-weight: 700;">${item.temp}°C</td>
                <td style="padding: 6px 10px; color: #a855f7; font-size: 0.75rem;">${item.loc}</td>
                <td style="padding: 6px 10px;"><span class="badge badge-success">${item.status}</span></td>
            `;
            tbody.appendChild(tr);
        });

        const enrEl = document.getElementById('kpi-livraison-enrobes');
        const gntEl = document.getElementById('kpi-livraison-gnt');
        const betEl = document.getElementById('kpi-livraison-beton');

        if (enrEl) enrEl.textContent = (428.5 + totEnrobes).toFixed(1) + ' t';
        if (gntEl) gntEl.textContent = (1240.0 + totGnt).toFixed(1) + ' t';
        if (betEl) betEl.textContent = (84.5 + totBeton).toFixed(1) + ' m³';
    }

    function openAddLivraisonModal() {
        const modal = document.getElementById('modal-add-livraison');
        if (modal) {
            modal.style.display = 'flex';
            const now = new Date().toISOString().slice(0, 16);
            document.getElementById('new-bl-date').value = now;
            document.getElementById('new-bl-num').value = 'BL-' + Math.floor(1000 + Math.random() * 9000);
        }
    }

    function closeAddLivraisonModal() {
        const modal = document.getElementById('modal-add-livraison');
        if (modal) modal.style.display = 'none';
    }

    function saveNewLivraison(e) {
        e.preventDefault();
        const bl = {
            id: document.getElementById('new-bl-num').value,
            date: document.getElementById('new-bl-date').value.replace('T', ' '),
            supplier: document.getElementById('new-bl-fournisseur').value,
            material: document.getElementById('new-bl-materiau').value,
            truck: document.getElementById('new-bl-camion').value || 'Camion 38t',
            qty: parseFloat(document.getElementById('new-bl-qte').value || 0),
            unit: document.getElementById('new-bl-materiau').value.includes('Béton') ? 'm³' : 't',
            temp: parseFloat(document.getElementById('new-bl-temp').value || 20),
            loc: document.getElementById('new-bl-loc').value || 'Zone chantier',
            status: 'Conforme'
        };
        rdcLivraisonsData.unshift(bl);
        closeAddLivraisonModal();
        renderRdcLivraisonsTable();
        showNotification(`Bon de livraison ${bl.id} enregistré avec succès !`, 'success');
    }

    function exportLivraisonsCSV() {
        let csv = 'Numero_BL;Date_Heure;Fournisseur;Materiau;Camion;Quantite;Unite;Temperature_C;Localisation;Statut\\n';
        rdcLivraisonsData.forEach(b => {
            csv += `${b.id};${b.date};${b.supplier};${b.material};${b.truck};${b.qty};${b.unit};${b.temp};${b.loc};${b.status}\\n`;
        });
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'Registre_Livraisons_Pesee_BTP.csv';
        link.click();
        showNotification('Registre de pesées exporté en CSV !', 'success');
    }

    /* ========================================================================== */
    /* V53: WEATHER STOPS & CCAG LEGAL EXTENSIONS TRACKER                        */
    /* ========================================================================== */
    const planningIntemperiesData = [
        { date: '2026-09-15', type: 'Pluie Diluvienne (> 10 mm/j)', value: '32.4 mm / 24h', tasks: 'Pose BBSG 0/10 et compactage GNT', cnetp: 'Oui - Indemnisé 100%', moe: 'Validé OS Suspension' },
        { date: '2026-09-16', type: 'Sol Impraticable / Boue', value: 'Portance EV2 < 15 MPa', tasks: 'Terrassement fond de forme Axe 2', cnetp: 'Oui - Indemnisé 100%', moe: 'Validé OS Suspension' },
        { date: '2026-09-20', type: 'Vent Violent / Rafales (> 60 km/h)', value: 'Rafales à 78 km/h', tasks: 'Levage blindage et pose bordures grue', cnetp: 'Non - Travaux sol', moe: 'Validé Constat CR' }
    ];

    function renderPlanningIntemperiesTable() {
        const tbody = document.getElementById('planning-intemperies-table-body');
        if (!tbody) return;

        tbody.innerHTML = '';
        planningIntemperiesData.forEach(item => {
            const tr = document.createElement('tr');
            tr.style.borderBottom = '1px solid var(--border)';
            tr.innerHTML = `
                <td style="padding: 6px 10px; font-weight: 700; color: #38bdf8;">${item.date}</td>
                <td style="padding: 6px 10px; color: #ef4444; font-weight: 600;">${item.type}</td>
                <td style="padding: 6px 10px; color: #94a3b8;">${item.value}</td>
                <td style="padding: 6px 10px; color: #e2e8f0; font-size: 0.75rem;">${item.tasks}</td>
                <td style="padding: 6px 10px; color: #f59e0b;">${item.cnetp}</td>
                <td style="padding: 6px 10px;"><span class="badge badge-success">${item.moe}</span></td>
            `;
            tbody.appendChild(tr);
        });

        const jEl = document.getElementById('kpi-intemperies-jours');
        const depEl = document.getElementById('kpi-intemperies-depassement');
        if (jEl) jEl.textContent = (planningIntemperiesData.length + 3) + ' Jours Ouvrés';
        if (depEl) depEl.textContent = '+' + planningIntemperiesData.length + ' Jours de Droit';
    }

    function openAddIntemperieModal() {
        const modal = document.getElementById('modal-add-intemperie');
        if (modal) {
            modal.style.display = 'flex';
            document.getElementById('new-intemp-date').value = new Date().toISOString().slice(0, 10);
        }
    }

    function closeAddIntemperieModal() {
        const modal = document.getElementById('modal-add-intemperie');
        if (modal) modal.style.display = 'none';
    }

    function saveNewIntemperie(e) {
        e.preventDefault();
        const item = {
            date: document.getElementById('new-intemp-date').value,
            type: document.getElementById('new-intemp-type').value,
            value: document.getElementById('new-intemp-valeur').value,
            tasks: document.getElementById('new-intemp-taches').value,
            cnetp: document.getElementById('new-intemp-cnetp').value,
            moe: 'Validé en Réunion Chantier'
        };
        planningIntemperiesData.unshift(item);
        closeAddIntemperieModal();
        renderPlanningIntemperiesTable();
        showNotification(`Journée d'intempérie du ${item.date} enregistrée avec succès !`, 'success');
    }

    function exportIntemperiesCSV() {
        let csv = 'Date;Phenomene;Valeur_Mesuree;Taches_Bloquees;CNETP;Validation_MOE\\n';
        planningIntemperiesData.forEach(p => {
            csv += `${p.date};${p.type};${p.value};${p.tasks};${p.cnetp};${p.moe}\\n`;
        });
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'Registre_Intemperies_CCAG.csv';
        link.click();
        showNotification('Registre des intempéries exporté en CSV !', 'success');
    }

    /* ========================================================================== */
    /* V53: OPPBTP 1/4 HOUR SAFETY BRIEFINGS & ONBOARDING REGISTER               */
    /* ========================================================================== */
    const safetyBriefingsDatabase = {
        'aipr_gaz_elec': {
            title: '1. Travaux à Proximité des Réseaux Enterrés (AIPR / Gaz / HTA)',
            reg: 'Arrêté du 15 février 2012 & Guide d\'application fascicule 3',
            risks: ['Rupture de canalisation de gaz (Risque d\'explosion / incendie)', 'Contact électrique HTA/BT (Électrisation / arc électrique)', 'Pollution nappe phréatique'],
            rules: [
                'Vérifier impérativement le récépissé DICT et le marquage-piquetage au sol avant tout coup de godet.',
                'Interdiction formelle d\'utiliser un godet à dents dans la zone d\'approche (50 cm d\'un réseau sensible classe A).',
                'Terrassement par fouille manuelle douce ou aspiratrice de déblais.',
                'En cas de contact ou odeur de gaz : arrêt immédiat, balisage 100m, appel 18/112 et GRDF Urgence 0 800 47 33 33.'
            ],
            ppe: ['Casque avec jugulaire', 'Gants isolants 1000V si prescrit', 'Vêtements antistatiques', 'Détecteur 4 gaz']
        },
        'blindage_tranchee': {
            title: '2. Risque d\'Éboulement & Blindage des Tranchées',
            reg: 'Code du Travail R.4534-24 à R.4534-35 & Recommandation CNAM R453',
            risks: ['Ensevelissement par effondrement de paroi (mortel dès 1 m³ de terre = 1.8 tonne)', 'Chute de plain-pied dans la fouille'],
            rules: [
                'Blindage obligatoire dès que la profondeur dépasse 1.30 m et que la largeur est inférieure aux 2/3 de la hauteur.',
                'Pose du blindage TOUJOURS effectuée depuis la surface sans jamais descendre dans la fouille non blindée.',
                'Dépôt des déblais à au moins 0.80 m de la crête de la tranchée.',
                'Mise en place de garde-corps rigides ou lisses K2 tout le long de la fouille.'
            ],
            ppe: ['Casque de sécurité', 'Gilet haute visibilité', 'Chaussures de sécurité montantes S3']
        },
        'engins_pietons': {
            title: '3. Coactivité et Heurts Engins / Piétons sur Chantier',
            reg: 'Recommandation R.482 OPPBTP & Plan Particulier de Sécurité PPSPS',
            risks: ['Écrasement en marche arrière (angles morts)', 'Collision engin-véhicule léger'],
            rules: [
                'Ségrégation physique absolue des flux piétons et des pistes engins (GBA béton, barrières rigides).',
                'Établissement d\'un contact visuel avec le conducteur d\'engin avant de s\'approcher.',
                'Feu à éclat (gyrophare) et avertisseur sonore de recul obligatoirement actifs et testés chaque matin.',
                'Interdiction de stationner dans le rayon de rotation de la tourelle d\'une pelle.'
            ],
            ppe: ['Gilet haute visibilité classe 3', 'Casque', 'Chaussures de sécurité S3']
        },
        'elinguage_levage': {
            title: '4. Élingage, Manutention et Levage de Blindages & Canalisations',
            reg: 'Arrêté du 1er mars 2004 & VGP périodique semestrielle',
            risks: ['Rupture d\'élingue / décrochage de charge lourde', 'Heurt par oscillation'],
            rules: [
                'Contrôle de la plaque constructeur et de la validité de la Vérification Générale Périodique (VGP).',
                'Interdiction d\'utiliser des élingues chaînes ou sangles effilochées ou sans linguet de sécurité.',
                'Guidage de la charge exclusivement à l\'aide de cordes de guidage (jamais à la main).',
                'Interdiction absolue de circuler ou stationner sous une charge suspendue.'
            ],
            ppe: ['Gants de manutention anti-coupure niveau D/F', 'Casque', 'Chaussures S3']
        },
        'enrobes_brulures': {
            title: '5. Risques Chimiques & Brûlures lors de la Pose d\'Enrobés à Chaud',
            reg: 'Guide OPPBTP Fumées de bitume & FDS Bitume pur',
            risks: ['Brûlures thermiques sévères (enrobé à 160°C - 180°C)', 'Inhalation d\'aérosols de bitume et HAP'],
            rules: [
                'Port de gants de protection thermique étanches spéciaux bitume.',
                'Positionnement au vent pour limiter l\'exposition aux vapeurs de bitume lors du tirage au râteau.',
                'Interdiction de nettoyer les outils avec du fioul (utiliser des nettoyants végétaux biodégradables).',
                'Présence d\'un kit de secours brûlure eau stérile hydrogel à portée immédiate sur le finisseur.'
            ],
            ppe: ['Gants thermiques étanches', 'Vêtements couvrants à manches longues', 'Masque respiratoire FFP2 / A2P3 si espace confiné']
        },
        'bruit_vibrations': {
            title: '6. Prévention des Risques liés au Bruit et aux Vibrations Engins',
            reg: 'Décret 2006-892 (Bruit) & Décret 2005-746 (Vibrations corps entier)',
            risks: ['Surdité professionnelle irréversible', 'Troubles musculo-squelettiques (TMS) et lombalgies'],
            rules: [
                'Port obligatoire des protections auditives (bouchons moulés ou casque antibruit) dès 80 dB(A).',
                'Réglage ergonomique du siège suspendu à amortissement pneumatique de chaque engin de terrassement.',
                'Alternance des tâches au brise-roche hydraulique (BRH) ou à la pilonneuse vibrante.'
            ],
            ppe: ['Protections auditives SNR > 28 dB', 'Gants anti-vibrations']
        },
        'canicule_froid': {
            title: '7. Travail par Fortes Chaleurs (Canicule) et Intempéries',
            reg: 'Plan National Canicule & Art. R.4225-2 du Code du Travail',
            risks: ['Coup de chaleur mortel', 'Déshydratation aiguë et perte de vigilance'],
            rules: [
                'Mise à disposition de 3 litres d\'eau fraîche potable minimum par jour et par travailleur.',
                'Aménagement des horaires de travail en décalé (ex: 06h00 - 13h30 sans pause méridienne sous le soleil).',
                'Mise à disposition d\'une zone d\'ombre ventilée et de brumisateurs sur la base vie.',
                'Surveillance mutuelle des compagnons pour détecter les signes avant-coureurs (vertiges, crampes, confusion).'
            ],
            ppe: ['Casque ventilé avec protège-nuque anti-UV', 'Lunettes de soleil teintées UV400']
        },
        'accueil_nouveau': {
            title: '8. Fiche d\'Accueil Sécurité Nouvel Arrivant & Intérimaire',
            reg: 'Article L.4141-2 du Code du Travail & Charte Chantier Zéro Accident',
            risks: ['Sur-accidentologie des primo-arrivants (statistiquement 3x plus élevée le 1er mois)'],
            rules: [
                'Présentation des Sauveteurs Secouristes du Travail (SST) du chantier et localisation de l\'infirmerie/trousse.',
                'Lecture conjointe des plans de circulation et consignes d\'urgence 15/18/112.',
                'Remise et vérification de conformité de l\'ensemble du paquetage d\'EPI neufs.',
                'Désignation d\'un tuteur de chantier expérimenté pendant les 15 premiers jours.'
            ],
            ppe: ['Pack complet 6 EPI conformes CE']
        }
    };

    function openSafetyQuarterHourModal() {
        const modal = document.getElementById('modal-safety-quarter-hour');
        if (modal) {
            modal.style.display = 'flex';
            loadSafetyBriefingContent();
            renderSafetyAttendees();
        }
    }

    function closeSafetyQuarterHourModal() {
        const modal = document.getElementById('modal-safety-quarter-hour');
        if (modal) modal.style.display = 'none';
    }

    function loadSafetyBriefingContent() {
        const select = document.getElementById('safety-theme-select');
        const themeKey = select ? select.value : 'aipr_gaz_elec';
        const data = safetyBriefingsDatabase[themeKey] || safetyBriefingsDatabase['aipr_gaz_elec'];
        const container = document.getElementById('safety-briefing-content');
        if (!container) return;

        container.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
                <div>
                    <h3 style="color: #38bdf8; margin: 0 0 4px 0; font-size: 1.1rem;">${data.title}</h3>
                    <div style="font-size: 0.75rem; color: #94a3b8;">Cadre réglementaire : <strong style="color: #e2e8f0;">${data.reg}</strong></div>
                </div>
                <span class="badge badge-warning">OPPBTP Conforme</span>
            </div>

            <div style="margin-bottom: 0.75rem;">
                <div style="font-weight: 700; color: #ef4444; font-size: 0.85rem; margin-bottom: 4px;">⚠️ Risques Majeurs Identifiés :</div>
                <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.8rem; color: #fca5a5;">
                    ${data.risks.map(r => `<li style="margin-bottom: 2px;">${r}</li>`).join('')}
                </ul>
            </div>

            <div style="margin-bottom: 0.75rem;">
                <div style="font-weight: 700; color: #22c55e; font-size: 0.85rem; margin-bottom: 4px;">✅ Consignes d'Exécution & Règles d'Or :</div>
                <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.8rem; color: #e2e8f0;">
                    ${data.rules.map(r => `<li style="margin-bottom: 3px;">${r}</li>`).join('')}
                </ul>
            </div>

            <div style="background: #020617; padding: 0.6rem; border-radius: 6px; border: 1px solid var(--border);">
                <div style="font-weight: 700; color: #38bdf8; font-size: 0.8rem; margin-bottom: 4px;">🦺 Équipements de Protection Individuelle (EPI) Exigés :</div>
                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    ${data.ppe.map(p => `<span class="badge badge-info" style="font-size: 0.75rem;">🛡️ ${p}</span>`).join('')}
                </div>
            </div>
        `;
    }

    function renderSafetyAttendees() {
        const container = document.getElementById('safety-attendees-grid');
        if (!container) return;

        const crew = [
            { name: 'M. Jean DUPONT', role: 'Chef de Chantier (Animateur)' },
            { name: 'A. BENALI', role: 'Conducteur Pelle 22t' },
            { name: 'P. MARTINEZ', role: 'Conducteur Finisseur' },
            { name: 'L. VIALA', role: 'Canalisateur Poseur' },
            { name: 'K. TRAORE', role: 'Maçon VRD' },
            { name: 'D. LECLERC', role: 'Manœuvre TP' },
            { name: 'R. GARCIA', role: 'Chauffeur Poids Lourd' },
            { name: 'S. MOREAU', role: 'Stagiaire Conduite Travaux' }
        ];

        container.innerHTML = crew.map((c, idx) => `
            <label style="display: flex; align-items: center; gap: 6px; background: #0b1120; padding: 4px 8px; border-radius: 4px; border: 1px solid var(--border); font-size: 0.75rem; cursor: pointer;">
                <input type="checkbox" checked id="safety-att-${idx}">
                <div>
                    <div style="font-weight: 700; color: #e2e8f0;">${c.name}</div>
                    <div style="font-size: 0.7rem; color: #94a3b8;">${c.role}</div>
                </div>
            </label>
        `).join('');
    }

    function printSafetyBriefing() {
        showNotification('Génération de la fiche 1/4h sécurité avec émargements...', 'info');
        window.print();
    }
"""

js_text += v53_js_engine

with open("scripts/section_js_part3.py", "w", encoding="utf-8") as f:
    f.write(js_text)

print("scripts/section_js_part3.py successfully patched with v53 JS engines!")
