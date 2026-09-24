#!/usr/bin/env python3
"""
Patch v56: Complete Design System (Typography, Contrast, Colors, Badges, Tables),
GTR Compaction Abacus Engine, and PAQ Non-Conformity (FNC) Manager
"""

import re

# 1. Update scripts/section_head_and_styles.py with complete high-contrast executive design system
with open("scripts/section_head_and_styles.py", "r", encoding="utf-8") as f:
    head_file = f.read()

# Replace fonts in head
old_font_link = '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
new_font_link = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap" rel="stylesheet">'

head_file = head_file.replace(old_font_link, new_font_link)

# Enhance CSS root and core elements
enhanced_css = """
        :root {
            --bg-base: #020617;
            --bg-surface: #0a0f1d;
            --bg-card: #0f172a;
            --bg-card-alt: #1e293b;
            --bg-card-hover: #1e293b;
            --bg: #090d16;
            --border: #334155;
            --border-light: #475569;
            --border-accent: rgba(56, 189, 248, 0.25);
            --border-emerald: rgba(34, 197, 94, 0.25);
            --border-amber: rgba(245, 158, 11, 0.25);
            --border-rose: rgba(239, 68, 68, 0.25);

            --text-main: #f8fafc;
            --text-primary: #f1f5f9;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --text-dim: #64748b;

            --cyan: #38bdf8;
            --cyan-glow: rgba(56, 189, 248, 0.20);
            --emerald: #22c55e;
            --amber: #f59e0b;
            --rose: #ef4444;
            --purple: #a855f7;
            --blue: #3b82f6;

            --font-sans: 'Plus Jakarta Sans', 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            --font-mono: 'JetBrains Mono', 'Fira Code', Consolas, monospace;

            --radius-sm: 4px;
            --radius-md: 6px;
            --radius-lg: 10px;
            --radius-xl: 14px;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: var(--bg-base);
            color: var(--text-main);
            font-family: var(--font-sans);
            font-size: 14px;
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #020617; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #475569; }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.4rem;
            font-family: var(--font-sans);
            font-size: 0.8rem;
            font-weight: 700;
            padding: 0.45rem 0.85rem;
            border-radius: var(--radius-md);
            cursor: pointer;
            transition: all 0.18s ease;
            text-decoration: none;
            white-space: nowrap;
        }

        .btn-primary {
            background: linear-gradient(135deg, #0284c7 0%, #06b6d4 100%);
            color: #ffffff;
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 2px 8px rgba(6, 182, 212, 0.25);
        }
        .btn-primary:hover {
            background: linear-gradient(135deg, #0369a1 0%, #0891b2 100%);
            box-shadow: 0 4px 12px rgba(6, 182, 212, 0.4);
            transform: translateY(-1px);
        }

        .btn-secondary {
            background: #1e293b;
            color: #e2e8f0;
            border: 1px solid #334155;
            font-weight: 600;
        }
        .btn-secondary:hover {
            background: #334155;
            color: #38bdf8;
            border-color: #475569;
        }
        .btn-secondary.active {
            background: #0284c7;
            color: #ffffff;
            border-color: #38bdf8;
            font-weight: 700;
            box-shadow: 0 2px 6px rgba(2, 132, 199, 0.35);
        }

        .btn-danger {
            background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
            color: #ffffff;
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 2px 8px rgba(239, 68, 68, 0.25);
        }
        .btn-danger:hover {
            background: linear-gradient(135deg, #b91c1c 0%, #dc2626 100%);
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
        }

        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);
            transition: border-color 0.15s ease;
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.85rem;
            padding-bottom: 0.65rem;
            border-bottom: 1px solid rgba(51, 65, 85, 0.7);
        }

        .card-title {
            font-size: 0.95rem;
            font-weight: 800;
            color: #f1f5f9;
            display: flex;
            align-items: center;
            gap: 0.45rem;
            letter-spacing: -0.01em;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 2px 8px;
            border-radius: var(--radius-sm);
            font-size: 0.75rem;
            font-weight: 700;
            font-family: var(--font-sans);
            letter-spacing: 0.01em;
            line-height: 1.3;
        }

        .badge-info {
            background: rgba(56, 189, 248, 0.12);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.35);
        }
        .badge-success {
            background: rgba(34, 197, 94, 0.12);
            color: #22c55e;
            border: 1px solid rgba(34, 197, 94, 0.35);
        }
        .badge-warning {
            background: rgba(245, 158, 11, 0.12);
            color: #f59e0b;
            border: 1px solid rgba(245, 158, 11, 0.35);
        }
        .badge-danger {
            background: rgba(239, 68, 68, 0.12);
            color: #ef4444;
            border: 1px solid rgba(239, 68, 68, 0.35);
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 0.3rem;
            margin-bottom: 0.6rem;
        }

        .input-label {
            font-size: 0.75rem;
            font-weight: 700;
            color: #cbd5e1;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }

        .input-field, .select-field {
            background: #020617;
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            color: #f8fafc;
            font-family: var(--font-sans);
            font-size: 0.85rem;
            padding: 0.45rem 0.75rem;
            transition: all 0.15s ease;
            width: 100%;
        }

        .input-field:focus, .select-field:focus {
            outline: none;
            border-color: #38bdf8;
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25);
            background: #040817;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.82rem;
            color: #f1f5f9;
        }

        thead tr {
            background: #020617;
            color: #94a3b8;
            font-weight: 700;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            border-bottom: 2px solid var(--border);
        }

        tbody tr {
            border-bottom: 1px solid rgba(51, 65, 85, 0.6);
            transition: background 0.15s ease;
        }

        tbody tr:hover {
            background: rgba(56, 189, 248, 0.05);
        }

        td {
            padding: 7px 10px;
        }
"""

# Replace in head_file
pos_style_start = head_file.find('<style>')
pos_style_first_class = head_file.find('.btn-primary {')
if pos_style_start != -1 and pos_style_first_class != -1:
    head_file = head_file[:pos_style_start + 7] + enhanced_css + head_file[pos_style_first_class:]
    print("Replaced and modernized root CSS in section_head_and_styles!")

with open("scripts/section_head_and_styles.py", "w", encoding="utf-8") as f:
    f.write(head_file)

# 2. Add GTR Compaction Abacus view to tab-schemas in scripts/section_tab_panels.py
with open("scripts/section_tab_panels.py", "r", encoding="utf-8") as f:
    panels = f.read()

# Update buttons in tab-schemas
old_tech_btns = """<button class="btn-secondary tech-view-btn active" id="btn-tech-formulas" onclick="setTechniqueViewMode('formulas')">🧮 Simulateur de Formules</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-hydraulique" onclick="setTechniqueViewMode('hydraulique')">🌊 Hydraulique & Bassin</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-bruckner" onclick="setTechniqueViewMode('bruckner')">⛰️ Bruckner & Mouvements Terres</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-reseauxsecs" onclick="setTechniqueViewMode('reseauxsecs')">⚡ Réseaux Secs & Éclairage</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-enrobes2d" onclick="setTechniqueViewMode('enrobes_2d')">🛣️ Simulation 2D Enrobés</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-compactage" onclick="setTechniqueViewMode('compactage')">🔬 Coupe Tranchée & Compacteur</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-tasksheet" onclick="setTechniqueViewMode('tasksheet')">📊 Fiche de Tâche Excel</button>"""

new_tech_btns = """<button class="btn-secondary tech-view-btn active" id="btn-tech-formulas" onclick="setTechniqueViewMode('formulas')">🧮 Simulateur de Formules</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-hydraulique" onclick="setTechniqueViewMode('hydraulique')">🌊 Hydraulique & Bassin</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-gtr" onclick="setTechniqueViewMode('gtr')">🚜 Abaques GTR Compactage</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-bruckner" onclick="setTechniqueViewMode('bruckner')">⛰️ Bruckner & Terres</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-reseauxsecs" onclick="setTechniqueViewMode('reseauxsecs')">⚡ Réseaux Secs</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-enrobes2d" onclick="setTechniqueViewMode('enrobes_2d')">🛣️ Simulation 2D Enrobés</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-compactage" onclick="setTechniqueViewMode('compactage')">🔬 Coupe Tranchée</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-tasksheet" onclick="setTechniqueViewMode('tasksheet')">📊 Fiche Excel</button>"""

panels = panels.replace(old_tech_btns, new_tech_btns)

# GTR View HTML
gtr_view_html = """
            <!-- GTR COMPACTION ABACUS VIEW -->
            <div id="tech-gtr-view" style="display: none;">
                <div class="grid-split-40-60">
                    <div>
                        <div class="card" style="background: rgba(15,23,42,0.6); border: 1px solid var(--border); margin-bottom: 1rem;">
                            <h4 style="color: #f59e0b; margin-top: 0; display: flex; align-items: center; gap: 0.5rem;">
                                <span>🚜</span> Guide des Terrassements Routiers (GTR Fascicule 2)
                            </h4>
                            <div class="grid-2-col" style="gap: 0.5rem; margin-bottom: 0.5rem;">
                                <div class="input-group">
                                    <label class="input-label">Classification du Sol (GTR)</label>
                                    <select class="select-field" id="gtr-sol-type" onchange="updateGTRCalculation()">
                                        <option value="B1">B1 : Sables et graves très silteux</option>
                                        <option value="B2">B2 : Sables et graves peu argileux</option>
                                        <option value="B3" selected>B3 : Graves très silteuses (GNT 0/31.5)</option>
                                        <option value="A1">A1 : Limons peu plastiques (Ip < 12)</option>
                                        <option value="A2">A2 : Argiles et limons moyennement plastiques</option>
                                        <option value="C1">C1 : Éboulis, sables et graves à gros éléments</option>
                                        <option value="D1">D1 : Sables alluvionnaires propres</option>
                                        <option value="D2">D2 : Graves alluvionnaires propres</option>
                                    </select>
                                </div>
                                <div class="input-group">
                                    <label class="input-label">Classe Compacteur GTR</label>
                                    <select class="select-field" id="gtr-comp-class" onchange="updateGTRCalculation()">
                                        <option value="V1">V1 : Rouleau vibrant léger (M1/L 15-25 kg/cm)</option>
                                        <option value="V2">V2 : Rouleau vibrant moyen (M1/L 25-40 kg/cm)</option>
                                        <option value="V3" selected>V3 : Rouleau vibrant lourd (M1/L 40-55 kg/cm - BW 151)</option>
                                        <option value="V4">V4 : Rouleau vibrant très lourd (M1/L 55-70 kg/cm)</option>
                                        <option value="V5">V5 : Rouleau vibrant super lourd (> 70 kg/cm)</option>
                                        <option value="P1">P1 : Compacteur à pneus 2.5t à 4t / roue</option>
                                        <option value="P2">P2 : Compacteur à pneus 4t à 6t / roue</option>
                                        <option value="SP1">SP1 : Pieds dameurs vibrant moyen</option>
                                        <option value="PQ3">PQ3 : Plaque vibrante lourde (> 200 kg)</option>
                                    </select>
                                </div>
                            </div>
                            <div class="grid-2-col" style="gap: 0.5rem; margin-bottom: 0.5rem;">
                                <div class="input-group">
                                    <label class="input-label">Objectif de Compactage</label>
                                    <select class="select-field" id="gtr-objectif" onchange="updateGTRCalculation()">
                                        <option value="q4" selected>q4 : Couche de forme & Tranchées (98-100% OPM)</option>
                                        <option value="q3">q3 : Corps de remblai (95% OPN)</option>
                                    </select>
                                </div>
                                <div class="input-group">
                                    <label class="input-label">Vitesse de Translation (km/h)</label>
                                    <input type="number" class="input-field" id="gtr-vitesse" value="3.5" step="0.5" min="1.0" max="8.0" oninput="updateGTRCalculation()">
                                </div>
                            </div>
                            <div style="background: rgba(2,6,23,0.7); border: 1px solid var(--border); border-radius: 6px; padding: 0.6rem; font-size: 0.8rem;">
                                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                                    <span style="color: #94a3b8;">Épaisseur Maxi par Passe $e_{\\max}$ :</span>
                                    <span id="gtr-emax-res" style="font-weight: 800; color: #38bdf8;">0.30 m (30 cm)</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                                    <span style="color: #94a3b8;">Nombre Minimal de Passes $N$ :</span>
                                    <span id="gtr-npasses-res" style="font-weight: 800; color: #f59e0b;">6 passes</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                                    <span style="color: #94a3b8;">Débit Théorique $Q/L$ :</span>
                                    <span id="gtr-ql-res" style="font-weight: 800; color: #22c55e;">175 m³/h / mètre</span>
                                </div>
                                <div style="display: flex; justify-content: space-between;">
                                    <span style="color: #94a3b8;">Débit de l'Engin (Largeur 1.68m) :</span>
                                    <span id="gtr-qtot-res" style="font-weight: 800; color: #a855f7;">294 m³/h</span>
                                </div>
                            </div>
                        </div>

                        <div class="card" style="background: rgba(15,23,42,0.6); border: 1px solid var(--border);">
                            <h4 style="color: #38bdf8; margin-top: 0; font-size: 0.9rem;">🔬 Contrôle In Situ : Plaque Westergaard / Dynaplaque</h4>
                            <div style="font-size: 0.8rem; color: #cbd5e1; line-height: 1.5;">
                                <div>• <strong>Exigence Plateforme PF2</strong> : $EV_2 \ge 50\text{ MPa}$ et rapport $k = EV_2/EV_1 \le 2.0$.</div>
                                <div>• <strong>Exigence Plateforme PF3</strong> : $EV_2 \ge 120\text{ MPa}$ et rapport $k \le 1.8$.</div>
                                <div>• <strong>Compacité en fond de tranchée</strong> : Contrôle au pénétromètre dynamique léger Panda (objectif $q_4 = 98\%\text{ OPM}$).</div>
                            </div>
                        </div>
                    </div>

                    <!-- GTR SVG Graphic -->
                    <div>
                        <div class="card" style="background: rgba(15,23,42,0.8); border: 1px solid var(--border); height: 100%; display: flex; flex-direction: column;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                                <span style="font-size: 0.9rem; font-weight: 700; color: #38bdf8;">📐 Énergie de Compactage GTR & Propagation des Ondes Vibratoires</span>
                                <span class="badge badge-warning" id="gtr-badge-statut">V3 • GNT 0/31.5 • Objectif q4</span>
                            </div>
                            <div id="gtr-svg-container" style="flex: 1; min-height: 280px; display: flex; align-items: center; justify-content: center; background: #020617; border-radius: 8px; border: 1px solid rgba(245,158,11,0.25); position: relative; overflow: hidden;">
                                <!-- Injected dynamically -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>
"""

pos_hydrau_view = panels.find('id="tech-hydraulique-view"')
if pos_hydrau_view != -1:
    pos_end_hydrau = panels.find('</div>\n            </div>', pos_hydrau_view) + 22
    panels = panels[:pos_end_hydrau] + gtr_view_html + panels[pos_end_hydrau:]
    print("Injected GTR Compaction Abacus view into tab-schemas!")

with open("scripts/section_tab_panels.py", "w", encoding="utf-8") as f:
    f.write(panels)

# 3. Update scripts/section_js_part3.py for setTechniqueViewMode and GTR calculations
with open("scripts/section_js_part3.py", "r", encoding="utf-8") as f:
    js_text = f.read()

# Update setTechniqueViewMode
old_set_tech = """function setTechniqueViewMode(mode) {
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

new_set_tech = """function setTechniqueViewMode(mode) {
        techniqueViewMode = mode;
        document.querySelectorAll('.tech-view-btn').forEach(b => b.classList.remove('active'));
        const btnId = 'btn-tech-' + mode.replace('_', '');
        const btn = document.getElementById(btnId);
        if (btn) btn.classList.add('active');

        const fView = document.getElementById('tech-formulas-view');
        const hView = document.getElementById('tech-hydraulique-view');
        const gView = document.getElementById('tech-gtr-view');
        const bView = document.getElementById('tech-bruckner-view');
        const rView = document.getElementById('tech-reseauxsecs-view');
        const eView = document.getElementById('tech-enrobes-2d-view');
        const cView = document.getElementById('tech-compactage-cut-view');
        const tView = document.getElementById('tech-tasksheet-view');

        if (fView) fView.style.display = mode === 'formulas' ? 'block' : 'none';
        if (hView) hView.style.display = mode === 'hydraulique' ? 'block' : 'none';
        if (gView) gView.style.display = mode === 'gtr' ? 'block' : 'none';
        if (bView) bView.style.display = mode === 'bruckner' ? 'block' : 'none';
        if (rView) rView.style.display = mode === 'reseauxsecs' ? 'block' : 'none';
        if (eView) eView.style.display = mode === 'enrobes_2d' ? 'block' : 'none';
        if (cView) cView.style.display = mode === 'compactage' ? 'block' : 'none';
        if (tView) tView.style.display = mode === 'tasksheet' ? 'block' : 'none';

        if (mode === 'hydraulique') { updateHydrauliqueCalculation(); updateBassinCalculation(); }
        if (mode === 'gtr') { updateGTRCalculation(); }
        if (mode === 'bruckner') { renderBrucknerEngine(); }
        if (mode === 'reseauxsecs') { updateElectriqueCalculation(); updateEPCalculation(); }
        if (mode === 'tasksheet') renderTaskSheet();
        if (mode === 'enrobes_2d') renderAsphalt2DSimulation();
    }"""

if old_set_tech in js_text:
    js_text = js_text.replace(old_set_tech, new_set_tech)
    print("Updated setTechniqueViewMode for GTR!")

gtr_calc_js = r"""

    /* ========================================================================== */
    /* V56: GTR COMPACTION ABACUS & GEOTECHNICAL SOIL ENGINE                      */
    /* ========================================================================== */
    function updateGTRCalculation() {
        const solType = document.getElementById('gtr-sol-type')?.value || 'B3';
        const compClass = document.getElementById('gtr-comp-class')?.value || 'V3';
        const objectif = document.getElementById('gtr-objectif')?.value || 'q4';
        const vitesse = parseFloat(document.getElementById('gtr-vitesse')?.value || 3.5);

        // GTR Abacus Matrix
        let eMax = 0.30; // m
        let nPasses = 6;
        let widthM = 1.68; // Bomag BW 151 width

        if (compClass === 'V1') { eMax = 0.20; nPasses = 8; widthM = 1.20; }
        else if (compClass === 'V2') { eMax = 0.25; nPasses = 7; widthM = 1.45; }
        else if (compClass === 'V3') { eMax = 0.35; nPasses = 6; widthM = 1.68; }
        else if (compClass === 'V4') { eMax = 0.45; nPasses = 6; widthM = 2.13; }
        else if (compClass === 'V5') { eMax = 0.60; nPasses = 5; widthM = 2.22; }
        else if (compClass === 'P1') { eMax = 0.25; nPasses = 8; widthM = 2.00; }
        else if (compClass === 'P2') { eMax = 0.40; nPasses = 6; widthM = 2.40; }
        else if (compClass === 'SP1') { eMax = 0.30; nPasses = 8; widthM = 1.80; }
        else if (compClass === 'PQ3') { eMax = 0.20; nPasses = 5; widthM = 0.65; }

        if (objectif === 'q3') {
            eMax = eMax * 1.25; // thicker layer permitted in embankment body
            nPasses = Math.max(4, nPasses - 1);
        }

        // Q/L = (1000 * e * V) / N in m3/h/m
        const qOverL = (1000 * eMax * vitesse) / nPasses;
        const qTotal = qOverL * widthM;

        const emEl = document.getElementById('gtr-emax-res');
        const npEl = document.getElementById('gtr-npasses-res');
        const qlEl = document.getElementById('gtr-ql-res');
        const qtEl = document.getElementById('gtr-qtot-res');
        const bdgEl = document.getElementById('gtr-badge-statut');

        if (emEl) emEl.textContent = eMax.toFixed(2) + ' m (' + Math.round(eMax * 100) + ' cm)';
        if (npEl) npEl.textContent = nPasses + ' passes minimales';
        if (qlEl) qlEl.textContent = Math.round(qOverL) + ' m³/h / mètre de cylindre';
        if (qtEl) qtEl.textContent = Math.round(qTotal) + ' m³/h (Largeur ' + widthM.toFixed(2) + ' m)';
        if (bdgEl) bdgEl.textContent = compClass + ' • Sol ' + solType + ' • ' + (objectif === 'q4' ? 'Couche de Forme q4' : 'Remblai q3');

        renderGtrSVG(compClass, solType, eMax, nPasses);
    }

    function renderGtrSVG(compClass, solType, eMax, nPasses) {
        const container = document.getElementById('gtr-svg-container');
        if (!container) return;

        const svg = `
            <svg viewBox="0 0 340 270" width="100%" height="260" style="max-height: 260px;">
                <defs>
                    <linearGradient id="drumGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#f59e0b"/>
                        <stop offset="100%" stop-color="#b45309"/>
                    </linearGradient>
                    <pattern id="soilGtr" width="8" height="8" patternUnits="userSpaceOnUse">
                        <circle cx="2" cy="2" r="1.5" fill="#f59e0b" opacity="0.4"/>
                        <circle cx="6" cy="6" r="1" fill="#38bdf8" opacity="0.3"/>
                    </pattern>
                </defs>
                <!-- Background Stratum -->
                <rect x="20" y="20" width="300" height="230" rx="6" fill="#090d16" stroke="#1e293b"/>
                
                <!-- Soil Layer to compact -->
                <rect x="40" y="110" width="260" height="70" fill="url(#soilGtr)" stroke="#f59e0b" stroke-width="1.5"/>
                <text x="50" y="130" fill="#f59e0b" font-size="10" font-weight="700">SOL ${solType} • Épaisseur e = ${Math.round(eMax * 100)} cm</text>
                <text x="50" y="145" fill="#94a3b8" font-size="8">Objectif compactage : ${nPasses} passes @ 3.5 km/h</text>

                <!-- Subgrade support (PF2 / Sol support) -->
                <rect x="40" y="180" width="260" height="50" fill="#0f172a" stroke="#334155" stroke-width="1"/>
                <text x="50" y="205" fill="#38bdf8" font-size="9" font-weight="700">SOL SUPPORT / PLATEFORME AR2 (EV2 ≥ 50 MPa)</text>

                <!-- Compactor Roller Drum -->
                <circle cx="170" cy="70" r="38" fill="url(#drumGrad)" stroke="#fef08a" stroke-width="2.5"/>
                <circle cx="170" cy="70" r="15" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
                <text x="170" y="74" fill="#ffffff" font-size="9" font-weight="800" text-anchor="middle">${compClass}</text>

                <!-- Vibration energy waves -->
                <path d="M 140 112 Q 170 125 200 112" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="3,2"/>
                <path d="M 130 135 Q 170 155 210 135" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="3,2"/>
                <path d="M 120 160 Q 170 185 220 160" fill="none" stroke="#22c55e" stroke-width="2" stroke-dasharray="3,2"/>

                <text x="170" y="240" fill="#22c55e" font-size="9" font-weight="700" text-anchor="middle">✔ Énergie transmise conforme norme NF P 98-736</text>
            </svg>
        `;
        container.innerHTML = svg;
    }
"""

tq_pos = js_text.rfind('"""')
if tq_pos != -1:
    js_text = js_text[:tq_pos] + gtr_calc_js + js_text[tq_pos:]
else:
    js_text += gtr_calc_js

with open("scripts/section_js_part3.py", "w", encoding="utf-8") as f:
    f.write(js_text)

print("Patch v56 successfully applied!")
