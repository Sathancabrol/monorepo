# -*- coding: utf-8 -*-
"""
Script to update section_tab_panels.py with:
1. Options 9 and 10 in formula-type-select (Pentes talus remblais/déblais, Dévers enrobés).
2. Advanced Maps & Satellite controls in tab-simulator (Watchtower).
"""

with open('scripts/section_tab_panels.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add options 9 and 10 to formula-type-select
old_formula_select = r'''                            <select id="formula-type-select" class="input-field" style="font-weight:700; color:#38bdf8;" onchange="updateFormulaCalculator()">
                                <option value="cubature_terrassement">1. 🚜 Cubature Terrassement : Déblai, Foisonnement, Remblai & Rotations Camions</option>
                                <option value="tonnage_enrobes">2. 🛣️ Tonnage & Enrobés : Chaussée BBSG, Émulsion C65B4 & Fini m²</option>
                                <option value="perimetre_bordures">3. 📏 Linéaires & Périmètres : Bordures T2/P1, Caniveaux CC1 & Semelle Béton</option>
                                <option value="manning_hydraulique">4. 💧 Hydraulique : Débit Collecteur Manning-Strickler & Auto-curage</option>
                                <option value="pente_canalisateur">5. 📐 Pente & Altimétrie : Calcul de Fil d'Eau Laser & ΔH</option>
                                <option value="compactage_gtr">6. 🔨 Compactage GTR : Débit Q/S, Nombre de Passes N & Vitesse</option>
                                <option value="revision_tp08">7. 📈 Révision de Prix : Formule Paramétrique Marchés Publics TP08</option>
                                <option value="debourse_sec_k">8. 💰 Déboursé Sec (DS) & Prix de Vente HT avec Coefficient K</option>
                            </select>'''

new_formula_select = r'''                            <select id="formula-type-select" class="input-field" style="font-weight:700; color:#38bdf8;" onchange="updateFormulaCalculator()">
                                <option value="cubature_terrassement">1. 🚜 Cubature Terrassement : Déblai, Foisonnement, Remblai & Rotations Camions</option>
                                <option value="pente_talus_terrassement">2. 📐 Pentes de Talus & Emprises : Déblais / Remblais (TN, Roches, Argiles, GNT, Risbermes & Stabilité)</option>
                                <option value="devers_chaussee_enrobes">3. 🛣️ Dévers & Pente Transversale : Chaussée, Enrobés BBSG/GB3 & Raccordement Fil d'Eau</option>
                                <option value="tonnage_enrobes">4. 🛣️ Tonnage & Enrobés : Chaussée BBSG, Émulsion C65B4 & Fini m²</option>
                                <option value="perimetre_bordures">5. 📏 Linéaires & Périmètres : Bordures T2/P1, Caniveaux CC1 & Semelle Béton</option>
                                <option value="manning_hydraulique">6. 💧 Hydraulique : Débit Collecteur Manning-Strickler & Auto-curage</option>
                                <option value="pente_canalisateur">7. 📐 Pente & Altimétrie : Calcul de Fil d'Eau Laser & ΔH</option>
                                <option value="compactage_gtr">8. 🔨 Compactage GTR : Débit Q/S, Nombre de Passes N & Vitesse</option>
                                <option value="revision_tp08">9. 📈 Révision de Prix : Formule Paramétrique Marchés Publics TP08</option>
                                <option value="debourse_sec_k">10. 💰 Déboursé Sec (DS) & Prix de Vente HT avec Coefficient K</option>
                            </select>'''

if old_formula_select in text:
    text = text.replace(old_formula_select, new_formula_select)
    print("Formula select updated successfully!")
else:
    print("Warning: old_formula_select exact match not found, searching with regex")
    import re
    text = re.sub(r'<select id="formula-type-select"[\s\S]*?<\/select>', new_formula_select, text, count=1)
    print("Formula select replaced via regex!")

# 2. Update tab-simulator in section_tab_panels.py
new_tab_simulator = r'''    <!-- ========================================== -->
    <!-- TAB 6: WATCH TOWER 3D / SATELLITE & MAPS   -->
    <!-- ========================================== -->
    <div id="tab-simulator" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">🛰️ Watch Tower : Jumeau Numérique 3D & Cartographie Satellite / OSM / Maps HD</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Imagerie Satellite HD, Cadastre IGN, Réseaux DICT (Gaz/Elec/Eau/Telecom), Mesures Terrain, Street View 360° et Radar RTK</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap; align-items: center;">
                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary sim-view-btn active" id="btn-sim-maps" onclick="setSimulatorViewMode('maps')">🛰️ Vue Satellite & Maps HD</button>
                        <button class="btn-secondary sim-view-btn" id="btn-sim-3d" onclick="setSimulatorViewMode('3d')">🏗️ Jumeau 3D Chantier</button>
                        <button class="btn-secondary sim-view-btn" id="btn-sim-radar" onclick="setSimulatorViewMode('radar')">📡 Radar Télémétrie</button>
                        <button class="btn-secondary sim-view-btn" id="btn-sim-standard" onclick="setSimulatorViewMode('standard')">📐 Split 3D / Maps</button>
                    </div>
                    <button class="btn btn-secondary" onclick="exportWatchtowerMapPNG()">📸 Capture Plan PNG</button>
                    <button class="btn btn-primary" id="btn-play-4d-sim" onclick="togglePlay4DSimulation()">▶️ Simulation 4D</button>
                </div>
            </div>

            <!-- MAPS & GIS INTERACTIVE TOOLBAR (ACTIVE IN MAPS / SATELLITE MODE) -->
            <div id="watchtower-maps-toolbar" style="background: rgba(15,23,42,0.95); border: 1px solid var(--border); border-radius: 8px; padding: 0.6rem 0.8rem; margin-bottom: 0.75rem; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 0.5rem;">
                <!-- Layer selector -->
                <div style="display: flex; align-items: center; gap: 0.4rem; flex-wrap: wrap;">
                    <span style="font-size: 0.75rem; font-weight: 800; color: #38bdf8;">🗺️ COUCHE :</span>
                    <div style="display: flex; background: #0b1120; border-radius: 6px; border: 1px solid rgba(56,189,248,0.3); overflow: hidden;">
                        <button class="btn-secondary map-layer-btn active" id="btn-layer-satellite" style="padding: 4px 8px; font-size: 0.72rem;" onclick="setWatchtowerMapLayer('satellite')">🛰️ Satellite HD</button>
                        <button class="btn-secondary map-layer-btn" id="btn-layer-osm" style="padding: 4px 8px; font-size: 0.72rem;" onclick="setWatchtowerMapLayer('osm')">🗺️ OpenStreetMap</button>
                        <button class="btn-secondary map-layer-btn" id="btn-layer-cadastre" style="padding: 4px 8px; font-size: 0.72rem;" onclick="setWatchtowerMapLayer('cadastre')">🏛️ Cadastre IGN</button>
                        <button class="btn-secondary map-layer-btn" id="btn-layer-hybride" style="padding: 4px 8px; font-size: 0.72rem;" onclick="setWatchtowerMapLayer('hybride')">🔀 Hybride Réseaux</button>
                        <button class="btn-secondary map-layer-btn" id="btn-layer-relief" style="padding: 4px 8px; font-size: 0.72rem;" onclick="setWatchtowerMapLayer('relief')">🏔️ Relief MNT</button>
                    </div>
                </div>

                <!-- POI Search & Quick-Fly -->
                <div style="display: flex; align-items: center; gap: 0.4rem; flex-wrap: wrap;">
                    <span style="font-size: 0.75rem; font-weight: 800; color: var(--emerald);">📍 LIEU / CHANTIER :</span>
                    <select id="watchtower-poi-select" class="input-field" style="width: auto; padding: 0.3rem 0.6rem; font-size: 0.75rem; font-weight: 700; color: #38bdf8;" onchange="flyToWatchtowerPOI(this.value)">
                        <option value="sete_quai">📍 Sète - Quai de la République (Assainissement Ø400)</option>
                        <option value="ales_giratoire">📍 Alès - Giratoire RD906 (Terrassement & Enrobés)</option>
                        <option value="beziers_zac">📍 Béziers - ZAC Ouest (Plateforme VRD)</option>
                        <option value="frontignan_rd612">📍 Frontignan - Piste RD612 (Bordures & Piste Cyclable)</option>
                        <option value="meze_port">📍 Mèze - Port des Nacres (Pluvial & Bordures)</option>
                        <option value="agde_rn112">📍 Agde - Entrée Ville RN112 (GB3 & BBSG)</option>
                        <option value="depot_sete">🏭 Dépôt & Base Logistique Sète (300m² Parc / 120m² Hangars)</option>
                        <option value="centrale_pinet">🏗️ Centrale Enrobés Eiffage/Colas Pinet</option>
                        <option value="carriere_loupian">⛏️ Carrière Calcaire de Loupian</option>
                        <option value="isdi_villeveyrac">♻️ Centre Recyclage ISDI Villeveyrac</option>
                    </select>
                </div>

                <!-- GIS Measurement & Interaction Tools -->
                <div style="display: flex; align-items: center; gap: 0.3rem; flex-wrap: wrap;">
                    <button class="btn btn-secondary map-tool-btn" id="btn-tool-pan" style="padding: 4px 8px; font-size: 0.72rem;" onclick="setWatchtowerTool('pan')">✋ Navigation</button>
                    <button class="btn btn-secondary map-tool-btn" id="btn-tool-measure-dist" style="padding: 4px 8px; font-size: 0.72rem;" onclick="setWatchtowerTool('measure_dist')">📏 Distance (ml)</button>
                    <button class="btn btn-secondary map-tool-btn" id="btn-tool-measure-area" style="padding: 4px 8px; font-size: 0.72rem;" onclick="setWatchtowerTool('measure_area')">📐 Surface (m²)</button>
                    <button class="btn btn-secondary map-tool-btn" id="btn-tool-profile" style="padding: 4px 8px; font-size: 0.72rem;" onclick="setWatchtowerTool('profile')">⛰️ Profil Pente</button>
                    <button class="btn btn-secondary map-tool-btn" id="btn-tool-streetview" style="padding: 4px 8px; font-size: 0.72rem;" onclick="setWatchtowerTool('streetview')">🧍 Street View 360°</button>
                    <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 0.72rem;" onclick="clearWatchtowerMeasurements()">🗑️ Effacer</button>
                </div>
            </div>

            <!-- DICT NETWORK OVERLAYS FILTER BAR -->
            <div id="watchtower-dict-bar" style="background: rgba(30,41,59,0.5); border: 1px solid rgba(51,65,85,0.6); border-radius: 6px; padding: 0.4rem 0.8rem; margin-bottom: 0.75rem; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 0.5rem; font-size: 0.72rem;">
                <div style="display: flex; align-items: center; gap: 0.4rem; flex-wrap: wrap;">
                    <strong style="color: #cbd5e1;">⚡ CALQUES RÉSEAUX DICT :</strong>
                    <label style="cursor: pointer; display: flex; align-items: center; gap: 3px; color: #facc15;"><input type="checkbox" id="dict-toggle-gaz" checked onchange="renderWatchtowerMaps()"> 🟡 Gaz GRDF (PEHD)</label>
                    <label style="cursor: pointer; display: flex; align-items: center; gap: 3px; color: #ef4444;"><input type="checkbox" id="dict-toggle-elec" checked onchange="renderWatchtowerMaps()"> 🔴 Élec Enedis (HTA/BT)</label>
                    <label style="cursor: pointer; display: flex; align-items: center; gap: 3px; color: #38bdf8;"><input type="checkbox" id="dict-toggle-aep" checked onchange="renderWatchtowerMaps()"> 🔵 Eau AEP (Fonte)</label>
                    <label style="cursor: pointer; display: flex; align-items: center; gap: 3px; color: #fb923c;"><input type="checkbox" id="dict-toggle-eu" checked onchange="renderWatchtowerMaps()"> 🟤 Assainissement (Ø400)</label>
                    <label style="cursor: pointer; display: flex; align-items: center; gap: 3px; color: #4ade80;"><input type="checkbox" id="dict-toggle-telecom" checked onchange="renderWatchtowerMaps()"> 🟢 Fibre/Télécom (L1T)</label>
                    <label style="cursor: pointer; display: flex; align-items: center; gap: 3px; color: #c084fc;"><input type="checkbox" id="dict-toggle-traffic" checked onchange="renderWatchtowerMaps()"> 🚦 Trafic Temps Réel</label>
                </div>
                <div id="watchtower-measurement-readout" style="font-weight: 800; color: #38bdf8;">
                    Mesure : Aucune sélection
                </div>
            </div>

            <!-- MAIN WATCHTOWER VIEWPORTS -->
            <div id="watchtower-main-viewport-container" style="position: relative; width: 100%; height: 500px; background: #070a14; border: 1px solid rgba(56,189,248,0.4); border-radius: 8px; overflow: hidden;">
                
                <!-- 1. FULLSCREEN SATELLITE & MAPS CANVAS -->
                <canvas id="watchtower-maps-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; cursor: grab; display: block;"></canvas>

                <!-- 2. SPLIT / 3D CANVAS -->
                <canvas id="watchtower-3d-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; cursor: grab; display: none;"></canvas>

                <!-- 3. RADAR CANVAS -->
                <canvas id="watchtower-radar-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: none;"></canvas>

                <!-- 4. STREET VIEW 360° IMMERSIVE VIEWPORT (OVERLAY) -->
                <div id="watchtower-streetview-modal-overlay" style="display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #050811; z-index: 50;">
                    <canvas id="watchtower-streetview-canvas" style="width: 100%; height: 100%; cursor: move;"></canvas>
                    <div style="position: absolute; top: 12px; left: 12px; background: rgba(15,23,42,0.9); padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; color: #38bdf8; border: 1px solid rgba(56,189,248,0.4); display: flex; align-items: center; gap: 0.5rem;">
                        <span>🚶‍♂️ <strong>VUE CAMÉRA CHANTIER 360° IMMERSIVE</strong> (Street View BTP)</span>
                        <span class="badge badge-success">Sol Terrain Réel</span>
                    </div>
                    <div style="position: absolute; top: 12px; right: 12px; display: flex; gap: 0.4rem;">
                        <button class="btn btn-secondary" style="font-size: 0.75rem;" onclick="rotateStreetView(-30)">↺ Tourner Gauche</button>
                        <button class="btn btn-secondary" style="font-size: 0.75rem;" onclick="rotateStreetView(30)">↻ Tourner Droite</button>
                        <button class="btn btn-danger" style="font-size: 0.75rem;" onclick="closeStreetViewMode()">✕ Quitter Street View</button>
                    </div>
                    <div style="position: absolute; bottom: 12px; left: 12px; right: 12px; background: rgba(15,23,42,0.85); padding: 6px 12px; border-radius: 6px; font-size: 0.75rem; color: #cbd5e1; display: flex; justify-content: space-between; align-items: center;">
                        <span>Glissez la souris pour pivoter à 360° • Ouvriers en poste, Pelle 24t en action, Tranchée blindée & Balisage urbain AK5</span>
                        <span style="font-weight: 800; color: var(--emerald);" id="streetview-hud-pos">PK 0+240 • Alt. 14.8m</span>
                    </div>
                </div>

                <!-- MAP CONTROLS OVERLAY (HUD) -->
                <div style="position: absolute; top: 10px; right: 10px; display: flex; flex-direction: column; gap: 6px; z-index: 20;">
                    <button class="btn btn-secondary" style="padding: 6px 10px; font-weight: 800; font-size: 0.9rem;" onclick="zoomWatchtowerMap(1.25)" title="Zoom avant">+</button>
                    <button class="btn btn-secondary" style="padding: 6px 10px; font-weight: 800; font-size: 0.9rem;" onclick="zoomWatchtowerMap(0.8)" title="Zoom arrière">-</button>
                    <button class="btn btn-secondary" style="padding: 6px 8px; font-size: 0.75rem;" onclick="resetWatchtowerNorth()" title="Réorienter vers le Nord">🧭 N</button>
                </div>

                <!-- GPS & TELEMETRY FOOTER BAR -->
                <div style="position: absolute; bottom: 0; left: 0; right: 0; background: rgba(15,23,42,0.92); border-top: 1px solid rgba(56,189,248,0.3); padding: 4px 12px; display: flex; justify-content: space-between; align-items: center; font-size: 0.72rem; color: #94a3b8; z-index: 20; font-family: 'JetBrains Mono', monospace;">
                    <div id="watchtower-coords-hud">
                        📍 WGS84: 43.4072° N, 3.6961° E • L93: X=772 450m, Y=6 268 920m • Alt: 14.8m NGF
                    </div>
                    <div style="display: flex; gap: 1rem; align-items: center;">
                        <span id="watchtower-scale-hud">Échelle : 1:500 (50m)</span>
                        <span class="badge badge-success" style="font-size: 0.65rem;">🟢 RTK FIX ±1cm</span>
                    </div>
                </div>
            </div>

            <!-- SCENARIO & PROGRESSION STRIP -->
            <div style="background: rgba(15,23,42,0.9); border: 1px solid var(--border); border-radius: 8px; padding: 0.75rem 1rem; margin-top: 1rem; margin-bottom: 1rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 1.1rem;">⏱️</span>
                    <strong style="font-size: 0.85rem; color: #38bdf8;" id="sim-4d-phase-label">PHASE 1 : TERRASSEMENT & PURGE</strong>
                    <span class="badge badge-info" id="scenario-active-step-badge">Étape 1/5</span>
                </div>
                <div style="display: flex; gap: 0.3rem; flex-wrap: wrap;">
                    <button class="btn-secondary" onclick="loadScenario('scen_tranchee_vrd')">Tranchée Assainissement</button>
                    <button class="btn-secondary" onclick="loadScenario('scen_giratoire_ales')">Giratoire Alès</button>
                    <button class="btn-secondary" onclick="prevScenarioStep()">⏮️ Étape Préc.</button>
                    <button class="btn-secondary" onclick="nextScenarioStep()">⏭️ Étape Suiv.</button>
                </div>
            </div>

            <div id="scenario-info-card" style="margin-bottom: 0.75rem;">
                <!-- Populated dynamically by loadScenario() -->
            </div>

            <!-- STEPS LIST & STEP DETAILS -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div>
                    <h5 style="font-size: 0.85rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.5rem;">📑 Chronologie des Étapes du Scénario</h5>
                    <div id="scenario-steps-list">
                        <!-- Populated dynamically -->
                    </div>
                </div>
                <div>
                    <h5 style="font-size: 0.85rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.5rem;">🔍 Prescriptions & Télémétrie</h5>
                    <div id="step-details-box">
                        <!-- Populated dynamically -->
                    </div>
                </div>
            </div>

            <!-- DIRECTORY OF ACTORS & LIVE TASKS -->
            <div style="margin-top: 1.5rem;">
                <h4 style="font-size: 1rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.75rem;">👥 Répertoire Détaillé des Acteurs du Chantier & Tâches en Direct</h4>
                <div id="watchtower-actors-grid" class="grid-3">
                    <!-- Populated dynamically by renderWatchtowerActors() -->
                </div>
            </div>
        </div>
    </div>'''

# Find tab-simulator block and replace it
pos_sim_start = text.find('<!-- ========================================== -->\n    <!-- TAB 6: WATCH TOWER 3D')
if pos_sim_start == -1:
    pos_sim_start = text.find('<div id="tab-simulator"')

pos_fleet_start = text.find('<!-- ========================================== -->\n    <!-- TAB 7: FLEET')
if pos_fleet_start == -1:
    pos_fleet_start = text.find('<div id="tab-fleet"')

if pos_sim_start != -1 and pos_fleet_start != -1:
    text = text[:pos_sim_start] + new_tab_simulator.strip() + "\n\n    " + text[pos_fleet_start:]
    print("tab-simulator in section_tab_panels.py updated successfully!")
else:
    print("Error locating tab-simulator in section_tab_panels.py")

with open('scripts/section_tab_panels.py', 'w', encoding='utf-8') as f:
    f.write(text)
