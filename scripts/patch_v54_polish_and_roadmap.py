#!/usr/bin/env python3
"""
Patch v54: Polish DOM IDs, Compagnon View, Fleet View, Cockpit Live Terminal, Emergency Modal, and Express VRD Cost Estimator
"""

import re

# 1. Update scripts/section_tab_panels.py
with open("scripts/section_tab_panels.py", "r", encoding="utf-8") as f:
    panels = f.read()

# 1.1 Cockpit Terminal
cockpit_terminal_html = """
        <!-- LIVE SYSTEM TERMINAL & AUTOPILOT LOG -->
        <div class="card" style="margin-top: 1rem; background: #020617; border: 1px solid rgba(56,189,248,0.25);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 0.85rem; font-weight: 800; color: #38bdf8;">🖥️ TERMINAL D'EXÉCUTION & TÉLÉMÉTRIE TEMPS RÉEL (AUTOPILOT IA)</span>
                    <span class="badge badge-success" style="font-size: 0.65rem;">SURVEILLANCE ACTIVE</span>
                </div>
                <button class="btn btn-secondary" style="font-size: 0.7rem; padding: 0.2rem 0.5rem;" onclick="runAutopilot()">▶️ Exécuter Cycle IA</button>
            </div>
            <div id="cockpit-terminal" style="font-family: 'JetBrains Mono', Consolas, monospace; font-size: 0.75rem; background: #040711; padding: 0.6rem 0.8rem; border-radius: 6px; border: 1px solid var(--border); color: #38bdf8; max-height: 120px; overflow-y: auto; line-height: 1.5;">
                <div style="color: #22c55e;">[10:54:10] Initialisation du noyau BTP Conduite Travaux v5.3 : 100% opérationnel</div>
                <div style="color: #94a3b8;">[10:54:12] Système SIG Watchtower synchronisé : 4 couches cartographiques HD actives</div>
                <div style="color: #eab308;">[10:54:15] Détection station météo Bassin de Thau : Vent 14 km/h NO, T°C 22°C (Conditions optimales pose BBSG)</div>
                <div style="color: #38bdf8;">[10:54:20] Registre des pesées centrale : 428.5t enrobés validées conformes</div>
            </div>
        </div>
"""

# Insert cockpit_terminal_html right before <!-- TAB 2: COMPANY TREASURY
pos_tab2 = panels.find('<!-- ========================================== -->\n    <!-- TAB 2: COMPANY')
if pos_tab2 != -1:
    pos_end_cockpit = panels.rfind('</div>\n    </div>', 0, pos_tab2)
    panels = panels[:pos_end_cockpit] + cockpit_terminal_html + panels[pos_end_cockpit:]
    print("Injected cockpit terminal!")

# 1.2 Compagnon Mobile Planning Container
compagnon_header = """<div id="compagnon-mobile-content">
                <!-- Populated dynamically by renderCompagnonPlanning() -->
            </div>"""

new_compagnon_content = """<div style="background: rgba(15,23,42,0.8); border: 1px solid var(--border); border-radius: 8px; padding: 0.75rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 0.85rem; font-weight: 700; color: #38bdf8;">👷 Sélection Équipe :</span>
                    <select id="compagnon-team-select" class="select-field" style="width: auto; padding: 0.3rem 0.6rem; font-size: 0.8rem;" onchange="renderCompagnonPlanning()">
                        <option value="team_a" selected>Équipe A - Terrassement & Plateforme (M. Dupont)</option>
                        <option value="team_b">Équipe B - Canalisations & Assainissement (A. Benali)</option>
                        <option value="team_c">Équipe C - Enrobés & Finisseur (P. Martinez)</option>
                        <option value="team_d">Équipe D - Bordures & Maçonnerie VRD (K. Traore)</option>
                    </select>
                </div>
                <div style="display: flex; align-items: center; gap: 0.4rem;">
                    <span style="font-size: 0.8rem; color: #94a3b8;">Chantier Assigné :</span>
                    <span id="compagnon-current-site" class="badge badge-info" style="font-size: 0.8rem; font-weight: 700;">Giratoire Barbazan</span>
                </div>
            </div>

            <div id="compagnon-planning-container">
                <!-- Populated dynamically by renderCompagnonPlanning() -->
            </div>"""

panels = panels.replace(compagnon_header, new_compagnon_content)

# 1.3 Fleet View Mode Switcher
old_fleet_header = """<div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">🚜 Flotte d'Engins TP, Dispatch & Entretien VGP</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Pelles chenilles, Mecalac, Bennes 8x4, Cylindres et suivi des visites générales périodiques</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <select id="fleet-sort-select" class="input-field" style="width: auto; padding: 0.3rem 0.6rem; font-size: 0.75rem;" onchange="sortFleet(this.value)">
                        <option value="name_asc">Trier : Nom (A ➔ Z)</option>
                        <option value="name_desc">Trier : Nom (Z ➔ A)</option>
                        <option value="val_desc">Trier : Valeur d'achat la plus haute</option>
                        <option value="val_asc">Trier : Valeur d'achat la plus basse</option>
                        <option value="cost_desc">Trier : Coût horaire le plus élevé</option>
                        <option value="category">Trier : Catégorie d'engin</option>
                    </select>
                    <button class="btn btn-primary" onclick="alert('Fiche engin TP ouverte.');">➕ Ajouter Engin</button>
                </div>
            </div>"""

new_fleet_header = """<div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">🚜 Flotte d'Engins TP, Dispatch & Entretien VGP</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Pelles chenilles, Mecalac, Bennes 8x4, Cylindres et suivi des visites générales périodiques</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap; align-items: center;">
                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary fleet-view-btn active" id="btn-fleet-grid" onclick="setFleetPresentationMode('grid')">🔲 Grille Cartes</button>
                        <button class="btn-secondary fleet-view-btn" id="btn-fleet-table" onclick="setFleetPresentationMode('table')">📑 Tableau Détaillé</button>
                        <button class="btn-secondary fleet-view-btn" id="btn-fleet-telemetry" onclick="setFleetPresentationMode('telemetry')">📡 Télémétrie GPS/CAN</button>
                    </div>
                    <select id="fleet-sort-select" class="input-field" style="width: auto; padding: 0.3rem 0.6rem; font-size: 0.75rem;" onchange="sortFleet(this.value)">
                        <option value="name_asc">Trier : Nom (A ➔ Z)</option>
                        <option value="name_desc">Trier : Nom (Z ➔ A)</option>
                        <option value="val_desc">Trier : Valeur d'achat la plus haute</option>
                        <option value="val_asc">Trier : Valeur d'achat la plus basse</option>
                        <option value="cost_desc">Trier : Coût horaire le plus élevé</option>
                        <option value="category">Trier : Catégorie d'engin</option>
                    </select>
                    <button class="btn btn-primary" onclick="alert('Fiche engin TP ouverte.');">➕ Ajouter Engin</button>
                </div>
            </div>"""

panels = panels.replace(old_fleet_header, new_fleet_header)

# In fleet tab, add fleet-table-view and fleet-telemetry-view right after fleet-grid
fleet_views_html = """
            <div id="fleet-table-view" style="display: none; overflow-x: auto; margin-top: 1rem;">
                <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; min-width: 900px;">
                    <thead>
                        <tr style="background: rgba(30,41,59,0.8); color: #94a3b8; text-align: left;">
                            <th style="padding: 0.6rem;">ENGIN</th>
                            <th style="padding: 0.6rem;">CATÉGORIE</th>
                            <th style="padding: 0.6rem;">IMMAT / PARC</th>
                            <th style="padding: 0.6rem;">STATUT</th>
                            <th style="padding: 0.6rem;">AFFECTATION CHANTIER</th>
                            <th style="padding: 0.6rem; text-align: right;">VALEUR ACHAT</th>
                            <th style="padding: 0.6rem; text-align: right;">COÛT HORAIRE</th>
                            <th style="padding: 0.6rem;">DERNIÈRE VGP</th>
                        </tr>
                    </thead>
                    <tbody id="fleet-table-body">
                        <!-- Populated dynamically -->
                    </tbody>
                </table>
            </div>

            <div id="fleet-telemetry-view" style="display: none; margin-top: 1rem;">
                <div class="grid-3" id="fleet-telemetry-grid">
                    <!-- Populated dynamically by renderFleetTelemetryView() -->
                </div>
            </div>
"""

pos_fleet_grid = panels.find('id="fleet-grid"')
if pos_fleet_grid != -1:
    pos_end_fleet_grid = panels.find('</div>', pos_fleet_grid) + 6
    panels = panels[:pos_end_fleet_grid] + fleet_views_html + panels[pos_end_fleet_grid:]
    print("Injected fleet table and telemetry views!")

# 1.4 Add Express VRD Estimator (Devis Express) in SDP Tab
sdp_express_html = """
            <!-- EXPRESS VRD ESTIMATOR SUBSECTION -->
            <div class="card" style="margin-top: 1.5rem; background: rgba(15,23,42,0.7); border: 1px solid rgba(56,189,248,0.3);">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.75rem;">
                    <div>
                        <h4 style="color: #38bdf8; margin: 0; display: flex; align-items: center; gap: 0.5rem;">
                            <span>⚡</span> Estimateur Express de Prix & Devis VRD / Terrassement
                        </h4>
                        <div style="font-size: 0.8rem; color: #94a3b8;">Chiffrage instantané selon ratios métriques (Linéaire voirie, couche de forme, assainissement, bordures)</div>
                    </div>
                    <button class="btn btn-primary" onclick="exportDevisExpressPDF()">📥 Exporter Devis Express PDF</button>
                </div>

                <div class="grid-4-col" style="gap: 0.5rem; margin-bottom: 0.75rem;">
                    <div class="input-group">
                        <label class="input-label">Linéaire de Voirie (m)</label>
                        <input type="number" class="input-field" id="exp-voirie-len" value="350" step="10" oninput="calculateDevisExpress()">
                    </div>
                    <div class="input-group">
                        <label class="input-label">Largeur Chaussée (m)</label>
                        <input type="number" class="input-field" id="exp-voirie-width" value="6.5" step="0.5" oninput="calculateDevisExpress()">
                    </div>
                    <div class="input-group">
                        <label class="input-label">Épaisseur GNT 0/31.5 (cm)</label>
                        <input type="number" class="input-field" id="exp-gnt-ep" value="25" step="5" oninput="calculateDevisExpress()">
                    </div>
                    <div class="input-group">
                        <label class="input-label">Épaisseur Enrobé BBSG (cm)</label>
                        <input type="number" class="input-field" id="exp-enr-ep" value="6" step="1" oninput="calculateDevisExpress()">
                    </div>
                </div>

                <div class="grid-4-col" style="gap: 0.5rem; margin-bottom: 1rem;">
                    <div class="input-group">
                        <label class="input-label">Linéaire Réseau EP DN300 (m)</label>
                        <input type="number" class="input-field" id="exp-ep-len" value="350" step="10" oninput="calculateDevisExpress()">
                    </div>
                    <div class="input-group">
                        <label class="input-label">Nombre de Regards Ø1000</label>
                        <input type="number" class="input-field" id="exp-regards-nb" value="9" step="1" oninput="calculateDevisExpress()">
                    </div>
                    <div class="input-group">
                        <label class="input-label">Linéaire Bordures T2 (m)</label>
                        <input type="number" class="input-field" id="exp-bordures-len" value="700" step="20" oninput="calculateDevisExpress()">
                    </div>
                    <div class="input-group">
                        <label class="input-label">Nombre Candélabres LED</label>
                        <input type="number" class="input-field" id="exp-cand-nb" value="14" step="1" oninput="calculateDevisExpress()">
                    </div>
                </div>

                <!-- Express Costing Breakdown -->
                <div class="grid-4-col" style="gap: 0.5rem;">
                    <div style="background: #020617; border: 1px solid var(--border); border-radius: 6px; padding: 0.6rem; text-align: center;">
                        <div style="font-size: 0.75rem; color: #94a3b8;">Déboursé Sec Total (DS)</div>
                        <div id="exp-res-ds" style="font-size: 1.2rem; font-weight: 800; color: #38bdf8;">142 650 € HT</div>
                    </div>
                    <div style="background: #020617; border: 1px solid var(--border); border-radius: 6px; padding: 0.6rem; text-align: center;">
                        <div style="font-size: 0.75rem; color: #94a3b8;">Frais Généraux (14%)</div>
                        <div id="exp-res-fg" style="font-size: 1.2rem; font-weight: 800; color: #f59e0b;">19 971 € HT</div>
                    </div>
                    <div style="background: #020617; border: 1px solid var(--border); border-radius: 6px; padding: 0.6rem; text-align: center;">
                        <div style="font-size: 0.75rem; color: #94a3b8;">Marge Nette & Bénéfice (9%)</div>
                        <div id="exp-res-marge" style="font-size: 1.2rem; font-weight: 800; color: #22c55e;">14 635 € HT</div>
                    </div>
                    <div style="background: #020617; border: 1px solid rgba(168,85,247,0.4); border-radius: 6px; padding: 0.6rem; text-align: center;">
                        <div style="font-size: 0.75rem; color: #a855f7;">Prix de Vente Total (PV HT)</div>
                        <div id="exp-res-pv" style="font-size: 1.3rem; font-weight: 900; color: #c084fc;">177 256 € HT</div>
                    </div>
                </div>
            </div>
"""

pos_sdp = panels.find('id="tab-sdp"')
if pos_sdp != -1:
    pos_end_sdp = panels.find('</div>\n    </div>\n\n    <!-- ========================================== -->\n    <!-- TAB 17: BENCHMARK', pos_sdp)
    if pos_end_sdp != -1:
        panels = panels[:pos_end_sdp] + sdp_express_html + panels[pos_end_sdp:]
        print("Injected express VRD estimator in tab-sdp!")

with open("scripts/section_tab_panels.py", "w", encoding="utf-8") as f:
    f.write(panels)

print("scripts/section_tab_panels.py successfully updated!")
