#!/usr/bin/env python3
"""
Patch v53: Advanced BTP Engineering Calculators & Field Operations Suite
- Hydraulics & Retention Basin Sizing (Manning-Strickler, Rainfall Method, Orifice outflow)
- Mass Haul Optimization & Bruckner Cumulative Earthwork Curve (Épures de Lalanne)
- Dry Utilities & Public Lighting Electrical Sizing (NF C 15-100 / C 17-200 / NF P 98-332)
- Concrete/Asphalt Delivery Tickets & Asphalt Density/Spreading Tracker
- 1/4h Security Briefings & Onboarding Register with Digital Signatures
"""

import re
import os

print("Starting Patch v53 implementation...")

# 1. Update scripts/section_tab_panels.py
with open("scripts/section_tab_panels.py", "r", encoding="utf-8") as f:
    tab_panels = f.read()

# Let's inspect buttons in tab-schemas
old_tech_buttons = """<button class="btn-secondary tech-view-btn active" id="btn-tech-formulas" onclick="setTechniqueViewMode('formulas')">🧮 Simulateur de Formules</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-enrobes2d" onclick="setTechniqueViewMode('enrobes_2d')">🛣️ Simulation 2D Passes d'Enrobés</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-compactage" onclick="setTechniqueViewMode('compactage')">🔬 Coupe Tranchée & Compacteur</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-tasksheet" onclick="setTechniqueViewMode('tasksheet')">📊 Fiche de Tâche Type Excel</button>"""

new_tech_buttons = """<button class="btn-secondary tech-view-btn active" id="btn-tech-formulas" onclick="setTechniqueViewMode('formulas')">🧮 Simulateur de Formules</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-hydraulique" onclick="setTechniqueViewMode('hydraulique')">🌊 Hydraulique & Bassin</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-bruckner" onclick="setTechniqueViewMode('bruckner')">⛰️ Bruckner & Mouvements Terres</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-reseauxsecs" onclick="setTechniqueViewMode('reseauxsecs')">⚡ Réseaux Secs & Éclairage</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-enrobes2d" onclick="setTechniqueViewMode('enrobes_2d')">🛣️ Simulation 2D Enrobés</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-compactage" onclick="setTechniqueViewMode('compactage')">🔬 Coupe Tranchée & Compacteur</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-tasksheet" onclick="setTechniqueViewMode('tasksheet')">📊 Fiche de Tâche Excel</button>"""

if old_tech_buttons in tab_panels:
    tab_panels = tab_panels.replace(old_tech_buttons, new_tech_buttons)
    print("Updated tech buttons successfully!")
else:
    print("Warning: old_tech_buttons not matched directly, checking regex replacement")
    tab_panels = re.sub(
        r'<button class="btn-secondary tech-view-btn active" id="btn-tech-formulas"[\s\S]*?<button class="btn-secondary tech-view-btn" id="btn-tech-tasksheet" onclick="setTechniqueViewMode\(\'tasksheet\'\)">📊 Fiche de Tâche Type Excel</button>',
        new_tech_buttons,
        tab_panels
    )

# Now let's inject the 3 new views into tab-schemas right after tech-tasksheet-view
new_tech_views = """
            <!-- 5. HYDRAULIQUE & BASSIN DE RETENTION VIEW -->
            <div id="tech-hydraulique-view" style="display: none;">
                <div class="grid-split-40-60">
                    <div>
                        <div class="card" style="background: rgba(15,23,42,0.6); border: 1px solid var(--border); margin-bottom: 1rem;">
                            <h4 style="color: #38bdf8; margin-top: 0; display: flex; align-items: center; gap: 0.5rem;">
                                <span>🌊</span> Dimensionnement Hydraulique (Manning-Strickler)
                            </h4>
                            <div class="grid-2-col" style="gap: 0.5rem; margin-bottom: 0.5rem;">
                                <div class="input-group">
                                    <label class="input-label">Matériau de Buse</label>
                                    <select class="select-field" id="hydrau-materiau" onchange="updateHydrauliqueCalculation()">
                                        <option value="100" selected>PVC / PEHD Lisse (K = 100)</option>
                                        <option value="85">Béton Armé 135A (K = 85)</option>
                                        <option value="80">Fonte Ductile (K = 80)</option>
                                        <option value="55">Maçonnerie / Pierres (K = 55)</option>
                                    </select>
                                </div>
                                <div class="input-group">
                                    <label class="input-label">Diamètre Nominal DN (mm)</label>
                                    <select class="select-field" id="hydrau-dn" onchange="updateHydrauliqueCalculation()">
                                        <option value="150">DN 150 mm</option>
                                        <option value="200">DN 200 mm</option>
                                        <option value="250">DN 250 mm</option>
                                        <option value="300" selected>DN 300 mm</option>
                                        <option value="400">DN 400 mm</option>
                                        <option value="500">DN 500 mm</option>
                                        <option value="600">DN 600 mm</option>
                                        <option value="800">DN 800 mm</option>
                                        <option value="1000">DN 1000 mm</option>
                                        <option value="1200">DN 1200 mm</option>
                                    </select>
                                </div>
                            </div>
                            <div class="grid-2-col" style="gap: 0.5rem; margin-bottom: 0.5rem;">
                                <div class="input-group">
                                    <label class="input-label">Pente du Réseau I (%)</label>
                                    <input type="number" class="input-field" id="hydrau-pente" value="1.50" step="0.1" min="0.1" max="15.0" oninput="updateHydrauliqueCalculation()">
                                </div>
                                <div class="input-group">
                                    <label class="input-label">Hauteur Remplissage h/D (%)</label>
                                    <input type="number" class="input-field" id="hydrau-fill" value="50" step="5" min="5" max="100" oninput="updateHydrauliqueCalculation()">
                                </div>
                            </div>
                            <div style="background: rgba(2,6,23,0.7); border: 1px solid var(--border); border-radius: 6px; padding: 0.6rem; font-size: 0.8rem;">
                                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                                    <span style="color: #94a3b8;">Débit à Pleine Section $Q_{ps}$ :</span>
                                    <span id="hydrau-qps-res" style="font-weight: 700; color: #38bdf8;">-- L/s</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                                    <span style="color: #94a3b8;">Débit Réel Écoulé $Q$ :</span>
                                    <span id="hydrau-q-res" style="font-weight: 800; color: #22c55e;">-- L/s</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                                    <span style="color: #94a3b8;">Vitesse Réelle $V$ :</span>
                                    <span id="hydrau-v-res" style="font-weight: 800; color: #f59e0b;">-- m/s</span>
                                </div>
                                <div style="display: flex; justify-content: space-between;">
                                    <span style="color: #94a3b8;">Diagnostic Autocurage :</span>
                                    <span id="hydrau-autocurage-res" class="badge badge-success">Conforme (0.7 à 3.0 m/s)</span>
                                </div>
                            </div>
                        </div>

                        <div class="card" style="background: rgba(15,23,42,0.6); border: 1px solid var(--border);">
                            <h4 style="color: #a855f7; margin-top: 0; display: flex; align-items: center; gap: 0.5rem;">
                                <span>🌧️</span> Dimensionnement Bassin Rétention & Ajutage
                            </h4>
                            <div class="grid-2-col" style="gap: 0.5rem; margin-bottom: 0.5rem;">
                                <div class="input-group">
                                    <label class="input-label">Surface Versante A (ha)</label>
                                    <input type="number" class="input-field" id="bassin-surface" value="2.50" step="0.1" min="0.1" oninput="updateBassinCalculation()">
                                </div>
                                <div class="input-group">
                                    <label class="input-label">Coef. Ruissellement C</label>
                                    <select class="select-field" id="bassin-coef-c" onchange="updateBassinCalculation()">
                                        <option value="0.20">Espaces Verts / Sable (C = 0.20)</option>
                                        <option value="0.50" selected>Lotissement Résidentiel (C = 0.50)</option>
                                        <option value="0.85">Voirie / Parking Étanche (C = 0.85)</option>
                                        <option value="0.95">Toitures / Béton (C = 0.95)</option>
                                    </select>
                                </div>
                            </div>
                            <div class="grid-2-col" style="gap: 0.5rem; margin-bottom: 0.5rem;">
                                <div class="input-group">
                                    <label class="input-label">Hauteur Pluie Décennale (mm)</label>
                                    <input type="number" class="input-field" id="bassin-pluie" value="45.0" step="1" oninput="updateBassinCalculation()">
                                </div>
                                <div class="input-group">
                                    <label class="input-label">Débit Fuite Autorisé (L/s/ha)</label>
                                    <input type="number" class="input-field" id="bassin-qfuite-spec" value="2.0" step="0.5" oninput="updateBassinCalculation()">
                                </div>
                            </div>
                            <div style="background: rgba(2,6,23,0.7); border: 1px solid var(--border); border-radius: 6px; padding: 0.6rem; font-size: 0.8rem;">
                                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                                    <span style="color: #94a3b8;">Volume Utile Requis $V_{\\text{utile}}$ :</span>
                                    <span id="bassin-volume-res" style="font-weight: 800; color: #a855f7;">-- m³</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                                    <span style="color: #94a3b8;">Débit de Fuite Total $Q_{\\text{fuite}}$ :</span>
                                    <span id="bassin-qfuite-total-res" style="font-weight: 700; color: #38bdf8;">-- L/s</span>
                                </div>
                                <div style="display: flex; justify-content: space-between;">
                                    <span style="color: #94a3b8;">Diamètre Ajutage Recommandé :</span>
                                    <span id="bassin-ajutage-res" style="font-weight: 700; color: #22c55e;">-- mm</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- SVG CROSS SECTION & GRAPHICS -->
                    <div>
                        <div class="card" style="background: rgba(15,23,42,0.8); border: 1px solid var(--border); height: 100%; display: flex; flex-direction: column;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                                <span style="font-size: 0.9rem; font-weight: 700; color: #38bdf8;">📐 Profil en Travers de la Buse & Niveau d'Écoulement Dynamique</span>
                                <span class="badge badge-info" id="hydrau-schema-badge">DN 300 mm | Remplissage 50%</span>
                            </div>
                            <div id="hydrau-svg-container" style="flex: 1; min-height: 280px; display: flex; align-items: center; justify-content: center; background: #020617; border-radius: 8px; border: 1px solid rgba(56,189,248,0.2); position: relative; overflow: hidden;">
                                <!-- SVG injected dynamically -->
                            </div>
                            <div style="margin-top: 0.75rem; display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; font-size: 0.75rem; text-align: center;">
                                <div style="background: #0b1120; padding: 0.4rem; border-radius: 6px; border: 1px solid var(--border);">
                                    <div style="color: #94a3b8;">Section Mouillée (S)</div>
                                    <div id="hydrau-s-detail" style="font-weight: 700; color: #38bdf8; font-size: 0.9rem;">-- m²</div>
                                </div>
                                <div style="background: #0b1120; padding: 0.4rem; border-radius: 6px; border: 1px solid var(--border);">
                                    <div style="color: #94a3b8;">Rayon Hydraulique (Rh)</div>
                                    <div id="hydrau-rh-detail" style="font-weight: 700; color: #f59e0b; font-size: 0.9rem;">-- m</div>
                                </div>
                                <div style="background: #0b1120; padding: 0.4rem; border-radius: 6px; border: 1px solid var(--border);">
                                    <div style="color: #94a3b8;">Largeur au Miroir (L)</div>
                                    <div id="hydrau-l-detail" style="font-weight: 700; color: #22c55e; font-size: 0.9rem;">-- m</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 6. OPTIMISATION MOUVEMENTS DE TERRES & COURBE DE BRUCKNER VIEW -->
            <div id="tech-bruckner-view" style="display: none;">
                <div class="card" style="background: rgba(15,23,42,0.6); border: 1px solid var(--border); margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.75rem;">
                        <div>
                            <h4 style="color: #f59e0b; margin: 0; display: flex; align-items: center; gap: 0.5rem;">
                                <span>⛰️</span> Épure de Lalanne & Courbe Cumulative des Terres (Bruckner)
                            </h4>
                            <div style="font-size: 0.8rem; color: #94a3b8;">Équilibrage Déblais / Remblais le long du tracé (PK 0+000 à PK 1+200), calcul de la distance moyenne de transport et optimisation des engins</div>
                        </div>
                        <div style="display: flex; gap: 0.4rem;">
                            <button class="btn btn-secondary" onclick="resetBrucknerData()">🔄 Réinitialiser Données</button>
                            <button class="btn btn-primary" onclick="exportBrucknerCSV()">📥 Exporter Cubatures CSV</button>
                        </div>
                    </div>

                    <!-- Canvas for Bruckner Curve -->
                    <div style="background: #020617; border-radius: 8px; border: 1px solid rgba(245,158,11,0.3); padding: 0.75rem; margin-bottom: 1rem; position: relative;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.4rem;">
                            <span style="font-weight: 700; color: #f59e0b;">📈 Graphique de Bruckner : Volumes Cumulés (m³) en fonction du Profil en Long (PK)</span>
                            <div style="display: flex; gap: 1rem;">
                                <span style="display: inline-flex; align-items: center; gap: 4px;"><span style="width: 10px; height: 10px; background: #38bdf8; border-radius: 2px;"></span> Déblai excédentaire (pente montante)</span>
                                <span style="display: inline-flex; align-items: center; gap: 4px;"><span style="width: 10px; height: 10px; background: #ef4444; border-radius: 2px;"></span> Remblai à combler (pente descendante)</span>
                                <span style="display: inline-flex; align-items: center; gap: 4px;"><span style="width: 10px; height: 10px; background: #22c55e; border-radius: 2px;"></span> Ligne de Répartition d'Équilibre</span>
                            </div>
                        </div>
                        <canvas id="bruckner-canvas" width="1000" height="240" style="width: 100%; height: 240px; border-radius: 4px;"></canvas>
                    </div>

                    <!-- Summary KPIs -->
                    <div class="grid-4-col" style="gap: 0.5rem; margin-bottom: 1rem;">
                        <div style="background: rgba(56,189,248,0.1); border: 1px solid rgba(56,189,248,0.3); border-radius: 6px; padding: 0.6rem; text-align: center;">
                            <div style="font-size: 0.75rem; color: #94a3b8;">Total Déblais Foisonnés ($C_f=1.20$)</div>
                            <div id="bruckner-total-deb" style="font-size: 1.2rem; font-weight: 800; color: #38bdf8;">14 850 m³</div>
                        </div>
                        <div style="background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3); border-radius: 6px; padding: 0.6rem; text-align: center;">
                            <div style="font-size: 0.75rem; color: #94a3b8;">Total Remblais Compactés ($C_c=0.90$)</div>
                            <div id="bruckner-total-rem" style="font-size: 1.2rem; font-weight: 800; color: #ef4444;">11 200 m³</div>
                        </div>
                        <div style="background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.3); border-radius: 6px; padding: 0.6rem; text-align: center;">
                            <div style="font-size: 0.75rem; color: #94a3b8;">Bilan Équilibre & Solde Décharge</div>
                            <div id="bruckner-solde" style="font-size: 1.2rem; font-weight: 800; color: #22c55e;">+3 650 m³ (Excédent)</div>
                        </div>
                        <div style="background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.3); border-radius: 6px; padding: 0.6rem; text-align: center;">
                            <div style="font-size: 0.75rem; color: #94a3b8;">Distance Moyenne de Transport</div>
                            <div id="bruckner-dmt" style="font-size: 1.2rem; font-weight: 800; color: #f59e0b;">285 m (Tombereau 6x6)</div>
                        </div>
                    </div>

                    <!-- Profile Cubature Table -->
                    <div style="overflow-x: auto; max-height: 280px; border: 1px solid var(--border); border-radius: 6px;">
                        <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; text-align: left;">
                            <thead style="background: #020617; position: sticky; top: 0; z-index: 10;">
                                <tr style="border-bottom: 2px solid var(--border);">
                                    <th style="padding: 6px 10px; color: #94a3b8;">Profil (PK)</th>
                                    <th style="padding: 6px 10px; color: #94a3b8;">Dist. Partielle (m)</th>
                                    <th style="padding: 6px 10px; color: #38bdf8;">Section Déblai (m²)</th>
                                    <th style="padding: 6px 10px; color: #ef4444;">Section Remblai (m²)</th>
                                    <th style="padding: 6px 10px; color: #38bdf8;">Vol. Déblai (m³)</th>
                                    <th style="padding: 6px 10px; color: #ef4444;">Vol. Remblai (m³)</th>
                                    <th style="padding: 6px 10px; color: #f59e0b;">Ordonnée Bruckner (m³)</th>
                                    <th style="padding: 6px 10px; color: #a855f7;">Recommandation Logistique</th>
                                </tr>
                            </thead>
                            <tbody id="bruckner-table-body">
                                <!-- Populated dynamically -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- 7. RESEAUX SECS & ECLAIRAGE PUBLIC VIEW -->
            <div id="tech-reseauxsecs-view" style="display: none;">
                <div class="grid-split-40-60">
                    <div>
                        <div class="card" style="background: rgba(15,23,42,0.6); border: 1px solid var(--border); margin-bottom: 1rem;">
                            <h4 style="color: #38bdf8; margin-top: 0; display: flex; align-items: center; gap: 0.5rem;">
                                <span>⚡</span> Calcul Chute de Tension (NF C 15-100 / C 17-200)
                            </h4>
                            <div class="grid-2-col" style="gap: 0.5rem; margin-bottom: 0.5rem;">
                                <div class="input-group">
                                    <label class="input-label">Type d'Alimentation</label>
                                    <select class="select-field" id="elec-type-alim" onchange="updateElectriqueCalculation()">
                                        <option value="mono" selected>Monophasé 230 V</option>
                                        <option value="tri">Triphasé 400 V</option>
                                    </select>
                                </div>
                                <div class="input-group">
                                    <label class="input-label">Nature du Conducteur</label>
                                    <select class="select-field" id="elec-metal" onchange="updateElectriqueCalculation()">
                                        <option value="cuivre" selected>Cuivre (ρ = 0.0225 Ω·mm²/m)</option>
                                        <option value="alu">Aluminium (ρ = 0.036 Ω·mm²/m)</option>
                                    </select>
                                </div>
                            </div>
                            <div class="grid-2-col" style="gap: 0.5rem; margin-bottom: 0.5rem;">
                                <div class="input-group">
                                    <label class="input-label">Puissance Totale (Watts)</label>
                                    <input type="number" class="input-field" id="elec-puissance" value="1800" step="100" min="50" oninput="updateElectriqueCalculation()">
                                </div>
                                <div class="input-group">
                                    <label class="input-label">Longueur de Ligne L (m)</label>
                                    <input type="number" class="input-field" id="elec-longueur" value="250" step="10" min="5" oninput="updateElectriqueCalculation()">
                                </div>
                            </div>
                            <div class="input-group" style="margin-bottom: 0.75rem;">
                                <label class="input-label">Section de Câble $S$ (mm²)</label>
                                <select class="select-field" id="elec-section" onchange="updateElectriqueCalculation()">
                                    <option value="2.5">2.5 mm²</option>
                                    <option value="4">4 mm²</option>
                                    <option value="6" selected>6 mm²</option>
                                    <option value="10">10 mm²</option>
                                    <option value="16">16 mm²</option>
                                    <option value="25">25 mm²</option>
                                    <option value="35">35 mm²</option>
                                    <option value="50">50 mm²</option>
                                </select>
                            </div>
                            <div style="background: rgba(2,6,23,0.7); border: 1px solid var(--border); border-radius: 6px; padding: 0.6rem; font-size: 0.8rem;">
                                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                                    <span style="color: #94a3b8;">Courant d'Emploi $I_b$ :</span>
                                    <span id="elec-ib-res" style="font-weight: 700; color: #38bdf8;">7.83 A</span>
                                </div>
                                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                                    <span style="color: #94a3b8;">Chute de Tension $\\Delta U$ :</span>
                                    <span id="elec-deltau-res" style="font-weight: 800; color: #22c55e;">4.12 V (1.79 %)</span>
                                </div>
                                <div style="display: flex; justify-content: space-between;">
                                    <span style="color: #94a3b8;">Conformité NF C 17-200 (max 5%) :</span>
                                    <span id="elec-conformite-res" class="badge badge-success">Conforme (< 3%)</span>
                                </div>
                            </div>
                        </div>

                        <div class="card" style="background: rgba(15,23,42,0.6); border: 1px solid var(--border);">
                            <h4 style="color: #eab308; margin-top: 0; display: flex; align-items: center; gap: 0.5rem;">
                                <span>💡</span> Candélabres & Éclairage Public VRD
                            </h4>
                            <div class="grid-2-col" style="gap: 0.5rem; margin-bottom: 0.5rem;">
                                <div class="input-group">
                                    <label class="input-label">Hauteur de Mât (m)</label>
                                    <input type="number" class="input-field" id="ep-hauteur" value="6.0" step="0.5" oninput="updateEPCalculation()">
                                </div>
                                <div class="input-group">
                                    <label class="input-label">Interdistance (m)</label>
                                    <input type="number" class="input-field" id="ep-interdist" value="25.0" step="1" oninput="updateEPCalculation()">
                                </div>
                            </div>
                            <div style="background: rgba(2,6,23,0.7); border: 1px solid var(--border); border-radius: 6px; padding: 0.6rem; font-size: 0.8rem;">
                                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                                    <span style="color: #94a3b8;">Éclairement Moyen Estimé :</span>
                                    <span id="ep-lux-res" style="font-weight: 800; color: #eab308;">18.5 Lux (Classe M4)</span>
                                </div>
                                <div style="display: flex; justify-content: space-between;">
                                    <span style="color: #94a3b8;">Uniformité Globale $U_0$ :</span>
                                    <span id="ep-u0-res" style="font-weight: 700; color: #22c55e;">0.42 (Conforme > 0.40)</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Trench Cross Section NF P 98-332 -->
                    <div>
                        <div class="card" style="background: rgba(15,23,42,0.8); border: 1px solid var(--border); height: 100%; display: flex; flex-direction: column;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                                <span style="font-size: 0.9rem; font-weight: 700; color: #38bdf8;">📐 Coupe Tranchée Commune Réseaux Secs (Norme NF P 98-332)</span>
                                <span class="badge badge-info">Distances de garde & Grillages avertisseurs</span>
                            </div>
                            <div id="reseauxsecs-svg-container" style="flex: 1; min-height: 280px; display: flex; align-items: center; justify-content: center; background: #020617; border-radius: 8px; border: 1px solid rgba(56,189,248,0.2); position: relative; overflow: hidden;">
                                <!-- SVG injected dynamically -->
                            </div>
                            <div style="margin-top: 0.75rem; background: #0b1120; padding: 0.6rem; border-radius: 6px; border: 1px solid var(--border); font-size: 0.75rem; color: #94a3b8;">
                                <div style="font-weight: 700; color: #e2e8f0; margin-bottom: 4px;">🔴 Règles de pose NF P 98-332 & Fascicule 70 :</div>
                                <div>• <strong>Enedis BT/HTA (Rouge)</strong> : Profondeur min. 0.80 m sous trottoir (1.00 m sous chaussée) avec grillage rouge 20 cm au-dessus.</div>
                                <div>• <strong>Télécom / Fibre Optique (Vert)</strong> : Profondeur min. 0.60 m avec gaine TPC verte Ø45 ou Ø60.</div>
                                <div>• <strong>Éclairage Public (Bleu/Rouge)</strong> : Profondeur min. 0.60 m avec câble U1000 R2V sous fourreau TPC rouge.</div>
                                <div>• <strong>Garde minimale entre réseaux</strong> : 20 cm de remblai meuble sablonneux sans cailloux tranchants.</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
"""

# Let's insert new_tech_views before closing tag of tab-schemas
pos_tasksheet_view = tab_panels.find('id="tech-tasksheet-view"')
if pos_tasksheet_view != -1:
    pos_end_tab_schemas = tab_panels.find('</div>\n    </div>\n\n    <!-- ========================================== -->\n    <!-- TAB 16: SDP', pos_tasksheet_view)
    if pos_end_tab_schemas != -1:
        tab_panels = tab_panels[:pos_end_tab_schemas] + new_tech_views + tab_panels[pos_end_tab_schemas:]
        print("Injected new tech views into tab-schemas successfully!")
    else:
        print("Searching fallback closing tag for tab-schemas...")
        pos_tab16 = tab_panels.find('id="tab-sdp"')
        if pos_tab16 != -1:
            last_div = tab_panels.rfind('</div>', 0, pos_tab16)
            last_div = tab_panels.rfind('</div>', 0, last_div)
            tab_panels = tab_panels[:last_div] + new_tech_views + tab_panels[last_div:]
            print("Injected via fallback into tab-schemas!")

# Write updated scripts/section_tab_panels.py
with open("scripts/section_tab_panels.py", "w", encoding="utf-8") as f:
    f.write(tab_panels)

print("scripts/section_tab_panels.py updated successfully!")
