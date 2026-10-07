import re
import json
from pathlib import Path

SOURCE = Path("/home/user/monorepo/scripts/build_html_dashboard.py")

with open(SOURCE, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update tab-simulator HTML
old_sim_snippet = """            <!-- Right: Radar & 3D Cube Visualizer -->
            <div class="card">
                <div class="card-header">
                    <span class="card-title">🗺️ Visualisation Chantier In-Situ</span>
                    <div style="display:flex; gap:0.35rem;">
                        <button class="btn-secondary" id="btn-view-radar" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setSimulatorViewMode('radar')">🛰️ Radar 2D</button>
                        <button class="btn-secondary" id="btn-view-3dcube" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setSimulatorViewMode('3dcube')">🧊 Cube 3D Grille</button>
                    </div>
                </div>
                <div class="step-canvas-wrap" style="height:440px;">
                    <canvas id="watchtower-radar-canvas" style="width:100%; height:100%;"></canvas>
                </div>
                <div style="display:flex; align-items:center; justify-content:space-between; margin-top:0.75rem; font-size:0.72rem; color:var(--text-muted); flex-wrap:wrap; gap:0.5rem;">
                    <span>🟢 Compagnons GPS (Sécurité active)</span>
                    <span>🚜 Pelle Liebherr 24t</span>
                    <span>🚛 Scania 8x4</span>
                    <span>🔴 Zone Danger Gaz MPB 4 bars</span>
                    <button class="btn-secondary" style="font-size:0.7rem; padding:0.3rem 0.6rem;" onclick="toggleRadarLiveMode()">🔄 Mode Statique / Live</button>
                </div>
            </div>"""

new_sim_snippet = """            <!-- Right: 2D Vue Satellite & 3D Environnement Théorique Grille XYZ -->
            <div class="card">
                <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                    <span class="card-title">🗺️ Visualisation Chantier In-Situ</span>
                    <div style="display:flex; gap:0.35rem; align-items:center; flex-wrap:wrap;">
                        <button class="btn-secondary active" id="btn-view-radar" style="font-size:0.7rem; padding:0.25rem 0.6rem;" onclick="setSimulatorViewMode('radar')">🛰️ 2D : Vue Satellite</button>
                        <button class="btn-secondary" id="btn-view-3dcube" style="font-size:0.7rem; padding:0.25rem 0.6rem;" onclick="setSimulatorViewMode('3dcube')">🧊 3D</button>
                        <button class="btn-secondary" id="btn-radar-mode-toggle" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="toggleRadarLiveMode()">🔄 Mode Statique / Live</button>
                    </div>
                </div>

                <!-- 3D Camera Controls & Presets (Displayed in 3D Mode) -->
                <div id="sim-3d-toolbar" style="display:none; background:var(--bg); border:1px solid var(--border); border-radius:6px; padding:0.4rem 0.6rem; margin-bottom:0.6rem; font-size:0.72rem; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.4rem;">
                    <div style="display:flex; align-items:center; gap:0.3rem; flex-wrap:wrap;">
                        <span style="font-weight:700; color:var(--cyan);">Caméra 3D :</span>
                        <button class="btn-secondary" style="padding:0.15rem 0.4rem; font-size:0.68rem;" onclick="rotate3D(-15, 0)">⟲ Gauche</button>
                        <button class="btn-secondary" style="padding:0.15rem 0.4rem; font-size:0.68rem;" onclick="rotate3D(15, 0)">⟳ Droite</button>
                        <button class="btn-secondary" style="padding:0.15rem 0.4rem; font-size:0.68rem;" onclick="rotate3D(0, 10)">🔼 Haut</button>
                        <button class="btn-secondary" style="padding:0.15rem 0.4rem; font-size:0.68rem;" onclick="rotate3D(0, -10)">🔽 Bas</button>
                        <button class="btn-secondary" style="padding:0.15rem 0.4rem; font-size:0.68rem;" onclick="zoom3D(1.15)">🔍 +</button>
                        <button class="btn-secondary" style="padding:0.15rem 0.4rem; font-size:0.68rem;" onclick="zoom3D(0.85)">🔍 -</button>
                    </div>
                    <div style="display:flex; align-items:center; gap:0.3rem; flex-wrap:wrap;">
                        <span style="font-weight:700; color:var(--text-muted);">Vues :</span>
                        <button class="btn-secondary" style="padding:0.15rem 0.45rem; font-size:0.68rem;" onclick="set3DPreset('iso')">📐 Isométrique 3D</button>
                        <button class="btn-secondary" style="padding:0.15rem 0.45rem; font-size:0.68rem;" onclick="set3DPreset('top')">🗺️ Dessus (Plan)</button>
                        <button class="btn-secondary" style="padding:0.15rem 0.45rem; font-size:0.68rem;" onclick="set3DPreset('section')">📏 Coupe Profil Z</button>
                        <button class="btn-secondary" style="padding:0.15rem 0.45rem; font-size:0.68rem;" onclick="set3DPreset('reset')">🎯 Reset</button>
                    </div>
                </div>

                <div class="step-canvas-wrap" style="height:440px; position:relative;">
                    <canvas id="watchtower-radar-canvas" style="width:100%; height:100%; cursor:grab;"></canvas>
                    <div id="sim-canvas-overlay-badge" style="position:absolute; top:8px; left:8px; background:rgba(15,23,42,0.85); border:1px solid var(--border); padding:0.25rem 0.5rem; border-radius:4px; font-size:0.68rem; font-family:var(--font-mono); color:var(--cyan);">
                        🛰️ Vue Satellite & Télémétrie RGF93 CC43
                    </div>
                </div>

                <div style="display:flex; align-items:center; justify-content:space-between; margin-top:0.75rem; font-size:0.72rem; color:var(--text-muted); flex-wrap:wrap; gap:0.4rem;">
                    <span>🟢 Compagnons & Exosquelettes GPS</span>
                    <span>🚜 Pelles & Engins Lourds</span>
                    <span>🛸 Drone LiDAR Survol Z=+10m</span>
                    <span>🔴 Danger Gaz MPB & Élec 20kV</span>
                </div>

                <!-- Dynamic Theoretical XYZ Placement Table for Selected Task -->
                <div style="margin-top:0.8rem; background:var(--bg); border:1px solid var(--border); border-radius:8px; padding:0.6rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                        <span style="font-size:0.75rem; font-weight:700; color:var(--cyan);">📊 Emplacements Théoriques selon Planning & Tâche (Grille XYZ) :</span>
                        <span class="card-badge" id="sim-3d-task-badge" style="color:var(--emerald);">Tâche Synchronisée</span>
                    </div>
                    <div style="overflow-x:auto;">
                        <table style="width:100%; border-collapse:collapse; font-size:0.7rem; font-family:var(--font-mono);" id="sim-3d-coords-table">
                            <!-- Populated dynamically by JS -->
                        </table>
                    </div>
                </div>
            </div>"""

if old_sim_snippet in content:
    content = content.replace(old_sim_snippet, new_sim_snippet)
    print("Replaced tab-simulator snippet successfully!")
else:
    print("Warning: old_sim_snippet not found by exact match, checking normalized...")

# 2. Update tab-fleet HTML
old_fleet_snippet = """    <!-- 6. TAB FLOTTE DE VÉHICULES & MATÉRIEL -->
    <div id="tab-fleet" class="tab-panel">
        <div class="card" style="margin-bottom:1.2rem;">
            <div class="card-header">
                <span class="card-title">🚜 Flotte d'Engins & Matériel Lourd</span>
                <div style="display:flex; gap:0.5rem;">
                    <button class="btn-primary" style="font-size:0.75rem; padding:0.35rem 0.75rem;" onclick="openAddVehicleModal()">
                        ➕ Ajouter un Engin
                    </button>
                </div>
            </div>
            <div class="grid-split-30-70">
                <div style="background:var(--bg); padding:1rem; border-radius:8px; border:1px solid var(--border);">
                    <div style="font-size:0.85rem; font-weight:700; color:var(--text-main); margin-bottom:0.75rem;">🔄 Réaffectation Rapide d'Engin</div>
                    <div class="input-group">
                        <label class="input-label">Sélectionner l'Engin :</label>
                        <select class="input-field" id="dispatch-fleet-select">
                            <!-- Populated by JS -->
                        </select>
                    </div>
                    <div class="input-group">
                        <label class="input-label">Chantier de Destination :</label>
                        <select class="input-field" id="dispatch-dest-select">
                            <option value="projet_ales">Giratoire RD906 Alès</option>
                            <option value="projet_sete">ZAC Littoral Sète</option>
                            <option value="projet_pezenas">Centre Ancien Pézenas</option>
                            <option value="projet_montpellier">Voie Verte Montpellier</option>
                        </select>
                    </div>
                    <button class="btn-primary" style="width:100%; justify-content:center;" onclick="executeDispatch()">
                        🚚 Transférer Engin & Mettre à Jour Parc
                    </button>
                </div>

                <div class="fleet-grid" id="fleet-cards-grid">
                    <!-- Rendered by JS -->
                </div>
            </div>
        </div>
    </div>"""

new_fleet_snippet = """    <!-- 6. TAB FLOTTE DE VÉHICULES, DRONES, EXOSQUELETTES & MATÉRIEL -->
    <div id="tab-fleet" class="tab-panel">
        <div class="card" style="margin-bottom:1.2rem;">
            <div class="card-header">
                <div>
                    <span class="card-title">🚜 Flotte d'Engins, Drones, Exosquelettes & Matériels VRD</span>
                    <span class="card-badge" id="hud-fleet-count" style="color:var(--cyan); margin-left:0.5rem;">14 Unités</span>
                </div>
                <div style="display:flex; gap:0.5rem;">
                    <button class="btn-primary" style="font-size:0.75rem; padding:0.35rem 0.75rem;" onclick="openAddVehicleModal()">
                        ➕ Ajouter un Équipement
                    </button>
                </div>
            </div>

            <!-- Fleet Filter Bar -->
            <div style="display:flex; gap:0.35rem; flex-wrap:wrap; margin-bottom:1rem;" id="fleet-filter-bar">
                <button class="btn-secondary active" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="filterFleet('all', this)">Tous (14)</button>
                <button class="btn-secondary" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="filterFleet('excavator', this)">🚜 Pelles Hydrauliques</button>
                <button class="btn-secondary" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="filterFleet('drone', this)">🛸 Drones & Télédétection Topo</button>
                <button class="btn-secondary" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="filterFleet('exosquelette', this)">🦾 Exosquelettes & Ergonomie</button>
                <button class="btn-secondary" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="filterFleet('robotique', this)">🤖 Robotique & Téléopération</button>
                <button class="btn-secondary" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="filterFleet('truck', this)">🚛 Camions & Transport</button>
                <button class="btn-secondary" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="filterFleet('compactor', this)">🔨 Compacteurs & Enrobés</button>
            </div>

            <div class="grid-split-30-70">
                <div style="background:var(--bg); padding:1rem; border-radius:8px; border:1px solid var(--border);">
                    <div style="font-size:0.85rem; font-weight:700; color:var(--text-main); margin-bottom:0.75rem;">🔄 Réaffectation Rapide d'Engin</div>
                    <div class="input-group">
                        <label class="input-label">Sélectionner l'Équipement :</label>
                        <select class="input-field" id="dispatch-fleet-select">
                            <!-- Populated by JS -->
                        </select>
                    </div>
                    <div class="input-group">
                        <label class="input-label">Chantier de Destination :</label>
                        <select class="input-field" id="dispatch-dest-select">
                            <option value="projet_ales">Giratoire RD906 Alès</option>
                            <option value="projet_sete">ZAC Littoral Sète</option>
                            <option value="projet_pezenas">Centre Ancien Pézenas</option>
                            <option value="projet_montpellier">Voie Verte Montpellier</option>
                        </select>
                    </div>
                    <button class="btn-primary" style="width:100%; justify-content:center;" onclick="executeDispatch()">
                        🚚 Transférer Équipement & Mettre à Jour Parc
                    </button>
                </div>

                <div class="fleet-grid" id="fleet-cards-grid">
                    <!-- Rendered by JS -->
                </div>
            </div>
        </div>
    </div>"""

if old_fleet_snippet in content:
    content = content.replace(old_fleet_snippet, new_fleet_snippet)
    print("Replaced tab-fleet snippet successfully!")
else:
    print("Warning: old_fleet_snippet not found by exact match!")

with open(SOURCE, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated HTML structure in build_html_dashboard.py")
