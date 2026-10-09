# -*- coding: utf-8 -*-
"""
Patch section_tab_panels.py for:
1. Simulation 2D des passes d'enrobes in tab-schemas
2. Real Leaflet Map container in tab-simulator (Watchtower)
"""

with open('scripts/section_tab_panels.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. In tab-schemas, update the navigation header buttons
old_schemas_nav = r'''                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary schema-view-btn active" id="btn-schema-tasksheet" onclick="setSchemaViewMode('tasksheet')">📐 Fiches de Tâches VRD & Analyse</button>
                        <button class="btn-secondary schema-view-btn" id="btn-schema-compactage" onclick="setSchemaViewMode('compactage')">🔬 Coupe Géotechnique & Compactage</button>
                        <button class="btn-secondary schema-view-btn" id="btn-schema-formulas" onclick="setSchemaViewMode('formulas')">🚜 Formules & Calculateur Technique</button>
                    </div>'''

new_schemas_nav = r'''                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border); flex-wrap: wrap; gap: 2px;">
                        <button class="btn-secondary schema-view-btn active" id="btn-schema-tasksheet" onclick="setSchemaViewMode('tasksheet')">📐 Fiches de Tâches VRD & Analyse</button>
                        <button class="btn-secondary schema-view-btn" id="btn-schema-enrobes2d" onclick="setSchemaViewMode('enrobes_2d')">🛣️ Simulation 2D Passes d'Enrobés</button>
                        <button class="btn-secondary schema-view-btn" id="btn-schema-compactage" onclick="setSchemaViewMode('compactage')">🔬 Coupe Géotechnique & Compactage</button>
                        <button class="btn-secondary schema-view-btn" id="btn-schema-formulas" onclick="setSchemaViewMode('formulas')">🚜 Formules & Calculateur Technique</button>
                    </div>'''

if old_schemas_nav in text:
    text = text.replace(old_schemas_nav, new_schemas_nav)
    print("Schema view mode nav updated with enrobes_2d!")

# 2. Add #tech-enrobes-2d-view container right before #tech-compactage-cut-view
enrobes_2d_html = r'''
            <!-- 2. SIMULATION 2D : CALCUL DES PASSES DE COMPACTAGE D'ENROBÉ & FINISSEUR -->
            <div id="tech-enrobes-2d-view" style="display: none;">
                <div style="background: rgba(15,23,42,0.95); border: 2px solid var(--cyan); border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
                        <div>
                            <h4 style="font-size: 1.05rem; font-weight: 800; color: #38bdf8;">🛣️ Simulation 2D des Passes de Compactage d'Enrobés & Finisseur</h4>
                            <div style="font-size: 0.78rem; color: #94a3b8;">Plan 2D vue de dessus, trajectoire du rouleau tandem, heatmap de recouvrement des passes et courbe thermique (Norme NF EN 13108-1 / Guide Cerema)</div>
                        </div>
                        <div style="display: flex; gap: 0.3rem; flex-wrap: wrap;">
                            <button class="btn btn-primary" id="btn-enrobes2d-play" onclick="toggleEnrobes2DSim()">▶️ Lancer Simulation 2D</button>
                            <button class="btn btn-secondary" onclick="resetEnrobes2DSim()">↺ Réinitialiser</button>
                            <button class="btn btn-secondary" onclick="stepEnrobes2DSim()">⏭️ Pas +1</button>
                            <button class="btn btn-secondary" id="btn-enrobes2d-speed" onclick="toggleEnrobes2DSpeed()">⚡ Vitesse x1</button>
                        </div>
                    </div>

                    <!-- 2D SIMULATION CANVAS & REAL-TIME CONTROLS SPLIT -->
                    <div class="grid-split-60-40">
                        <div style="height: 380px; background: #070a14; border: 1px solid rgba(56,189,248,0.4); border-radius: 6px; position: relative; overflow: hidden;">
                            <canvas id="enrobes-2d-canvas" style="width: 100%; height: 100%; display: block;"></canvas>
                            
                            <!-- Heatmap Legend Overlay -->
                            <div style="position: absolute; bottom: 8px; left: 8px; background: rgba(15,23,42,0.9); padding: 4px 8px; border-radius: 4px; border: 1px solid rgba(56,189,248,0.3); display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
                                <span style="font-size: 0.68rem; font-weight: 800; color: #38bdf8;">HEATMAP PASSES :</span>
                                <div class="enrobes-pass-legend-item"><div class="enrobes-pass-color-box" style="background:#1e293b;"></div> 0p (160°C)</div>
                                <div class="enrobes-pass-legend-item"><div class="enrobes-pass-color-box" style="background:#0284c7;"></div> 1-2p</div>
                                <div class="enrobes-pass-legend-item"><div class="enrobes-pass-color-box" style="background:#f59e0b;"></div> 3-4p</div>
                                <div class="enrobes-pass-legend-item"><div class="enrobes-pass-color-box" style="background:#10b981;"></div> 5-6p (Validé)</div>
                                <div class="enrobes-pass-legend-item"><div class="enrobes-pass-color-box" style="background:#ec4899;"></div> >8p (Surcompactage)</div>
                            </div>

                            <!-- Temperature readout -->
                            <div style="position: absolute; top: 8px; right: 8px; background: rgba(15,23,42,0.9); padding: 4px 10px; border-radius: 4px; border: 1px solid rgba(244,63,94,0.4); font-size: 0.75rem; font-family: monospace;">
                                <span style="color:#f43f5e;">🌡️ T° Enrobé :</span> <strong id="enrobes2d-temp-val" style="color:#facc15;">148.5 °C</strong>
                            </div>
                        </div>

                        <!-- PARAMETERS & TELEMETRY PANEL -->
                        <div style="display: flex; flex-direction: column; justify-content: space-between; gap: 0.5rem;">
                            <div style="background: rgba(30,41,59,0.5); padding: 0.75rem; border-radius: 6px; border: 1px solid rgba(51,65,85,0.6);">
                                <div style="font-size: 0.8rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.4rem;">🎛️ Paramètres Atelier Finisseur & Compacteur</div>
                                <div style="font-size: 0.72rem; color: #cbd5e1; display: grid; gap: 0.4rem;">
                                    <div>
                                        <div style="display:flex; justify-content:space-between;"><span>Largeur Table Finisseur (L) :</span> <strong id="e2d-width-val" style="color:var(--emerald);">3.50 m</strong></div>
                                        <input type="range" id="e2d-width-range" min="2.50" max="7.00" step="0.25" value="3.50" class="input-field" oninput="updateEnrobes2DParams()">
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between;"><span>Vitesse Finisseur (m/min) :</span> <strong id="e2d-fin-spd-val" style="color:#38bdf8;">3.5 m/min</strong></div>
                                        <input type="range" id="e2d-fin-spd-range" min="1.5" max="6.0" step="0.5" value="3.5" class="input-field" oninput="updateEnrobes2DParams()">
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between;"><span>Vitesse Rouleau Tandem (km/h) :</span> <strong id="e2d-comp-spd-val" style="color:var(--amber);">4.5 km/h</strong></div>
                                        <input type="range" id="e2d-comp-spd-range" min="2.5" max="7.0" step="0.5" value="4.5" class="input-field" oninput="updateEnrobes2DParams()">
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between;"><span>Passes Recommandées Cibles (N) :</span> <strong id="e2d-passes-val" style="color:var(--emerald);">6 passes</strong></div>
                                        <input type="range" id="e2d-passes-range" min="4" max="10" step="1" value="6" class="input-field" oninput="updateEnrobes2DParams()">
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between;"><span>Épaisseur Couche BBSG (cm) :</span> <strong id="e2d-thick-val" style="color:#f8fafc;">5.0 cm</strong></div>
                                        <input type="range" id="e2d-thick-range" min="3.0" max="8.0" step="0.5" value="5.0" class="input-field" oninput="updateEnrobes2DParams()">
                                    </div>
                                </div>
                            </div>

                            <!-- REALTIME TELEMETRY GRID -->
                            <div class="grid-2" style="gap: 0.4rem;">
                                <div class="enrobes-stat-card">
                                    <span class="enrobes-stat-title">Avancement Linéaire</span>
                                    <span class="enrobes-stat-val text-cyan" id="e2d-stat-lin">0.0 ml</span>
                                </div>
                                <div class="enrobes-stat-card">
                                    <span class="enrobes-stat-title">Tonnage Enrobé Appliqué</span>
                                    <span class="enrobes-stat-val text-emerald" id="e2d-stat-ton">0.0 t</span>
                                </div>
                                <div class="enrobes-stat-card">
                                    <span class="enrobes-stat-title">Compacité Moyenne</span>
                                    <span class="enrobes-stat-val text-amber" id="e2d-stat-compac">94.2 % OPN</span>
                                </div>
                                <div class="enrobes-stat-card">
                                    <span class="enrobes-stat-title">Adéquation Atelier</span>
                                    <span class="enrobes-stat-val" style="color:#a855f7;" id="e2d-stat-adeq">1 Tandem Suffisant</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- METHODOLOGICAL COMPACTION PLAN GUIDE -->
                    <div style="margin-top: 1rem; background: rgba(30,41,59,0.5); padding: 0.75rem; border-radius: 6px; border: 1px solid rgba(51,65,85,0.6); font-size: 0.75rem; color: #cbd5e1; line-height: 1.5;">
                        <strong style="color: #38bdf8;">📋 Plan de Compactage Méthodique des Enrobés (Guide Cerema / SETRA) :</strong>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 0.6rem; margin-top: 0.4rem;">
                            <div><strong>1. Passe d'Attaque :</strong> Démarrage sur le bord libre bas de la bande pour caler la matière sans déformation latérale.</div>
                            <div><strong>2. Passes Courantes :</strong> Va-et-vient avec chevauchement de 15 à 20cm entre traces. Décalage des points d'inversion en biseau (éviter les ornières).</div>
                            <div><strong>3. Passe de Fermeture :</strong> Finition sur le joint longitudinal à chaud pour garantir l'étanchéité et l'uni de surface.</div>
                            <div><strong>4. Plage Thermique :</strong> Compactage impératif entre 160°C et 110°C. Arrêt des vibrations sous 90°C pour éviter la fracturation des granulats.</div>
                        </div>
                    </div>
                </div>
            </div>
'''

pos_compactage_view = text.find('<div id="tech-compactage-cut-view"')
if pos_compactage_view != -1:
    text = text[:pos_compactage_view] + enrobes_2d_html.strip() + "\n\n            " + text[pos_compactage_view:]
    print("tech-enrobes-2d-view added to section_tab_panels.py!")
else:
    print("Error: tech-compactage-cut-view not found")

# 3. In tab-simulator, replace the viewport with Leaflet real map container
old_viewport_container = r'''            <!-- MAIN WATCHTOWER VIEWPORTS -->
            <div id="watchtower-main-viewport-container" style="position: relative; width: 100%; height: 500px; background: #070a14; border: 1px solid rgba(56,189,248,0.4); border-radius: 8px; overflow: hidden;">
                
                <!-- 1. FULLSCREEN SATELLITE & MAPS CANVAS -->
                <canvas id="watchtower-maps-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; cursor: grab; display: block;"></canvas>

                <!-- 2. SPLIT / 3D CANVAS -->
                <canvas id="watchtower-3d-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; cursor: grab; display: none;"></canvas>

                <!-- 3. RADAR CANVAS -->
                <canvas id="watchtower-radar-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: none;"></canvas>'''

new_viewport_container = r'''            <!-- MAIN WATCHTOWER VIEWPORTS -->
            <div id="watchtower-main-viewport-container" style="position: relative; width: 100%; height: 520px; background: #070a14; border: 1px solid rgba(56,189,248,0.4); border-radius: 8px; overflow: hidden;">
                
                <!-- 1. REAL INTERACTIVE LEAFLET / OSM / SATELLITE MAP CONTAINER -->
                <div id="watchtower-real-map-div" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 10; display: block;"></div>

                <!-- 2. FULLSCREEN FALLBACK / CANVAS LAYER -->
                <canvas id="watchtower-maps-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; cursor: grab; display: none; z-index: 5;"></canvas>

                <!-- 3. SPLIT / 3D CANVAS -->
                <canvas id="watchtower-3d-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; cursor: grab; display: none; z-index: 12;"></canvas>

                <!-- 4. RADAR CANVAS -->
                <canvas id="watchtower-radar-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: none; z-index: 12;"></canvas>'''

if old_viewport_container in text:
    text = text.replace(old_viewport_container, new_viewport_container)
    print("watchtower-main-viewport-container updated with real Leaflet map div!")

with open('scripts/section_tab_panels.py', 'w', encoding='utf-8') as f:
    f.write(text)
