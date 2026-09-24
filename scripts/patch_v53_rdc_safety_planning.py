#!/usr/bin/env python3
"""
Patch v53: Add RDC Deliveries view, Safety 1/4h Briefing view, and Planning Intempéries view
"""

import re

with open("scripts/section_tab_panels.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update RDC buttons in tab-rdc
old_rdc_buttons = """<button class="btn-secondary rdc-view-btn active" id="btn-rdc-rapport" onclick="setRdcViewMode('rapport')">📝 Rapport Quotidien</button>
                        <button class="btn-secondary rdc-view-btn" id="btn-rdc-pointage" onclick="setRdcViewMode('pointage')">👷 Pointage des Équipes</button>
                        <button class="btn-secondary rdc-view-btn" id="btn-rdc-rentabilite" onclick="setRdcViewMode('rentabilite')">📊 Rentabilité Heures DQE</button>"""

new_rdc_buttons = """<button class="btn-secondary rdc-view-btn active" id="btn-rdc-rapport" onclick="setRdcViewMode('rapport')">📝 Rapport Quotidien</button>
                        <button class="btn-secondary rdc-view-btn" id="btn-rdc-pointage" onclick="setRdcViewMode('pointage')">👷 Pointage des Équipes</button>
                        <button class="btn-secondary rdc-view-btn" id="btn-rdc-rentabilite" onclick="setRdcViewMode('rentabilite')">📊 Rentabilité Heures DQE</button>
                        <button class="btn-secondary rdc-view-btn" id="btn-rdc-livraisons" onclick="setRdcViewMode('livraisons')">🚛 Bons de Livraison & Pesée</button>"""

text = text.replace(old_rdc_buttons, new_rdc_buttons)

# 2. Add RDC livraisons view
rdc_livraisons_html = """
            <!-- 4. RDC LIVRAISONS & BONS DE PESEE VIEW -->
            <div id="rdc-livraisons-view" style="display: none;">
                <div class="card" style="background: rgba(15,23,42,0.6); border: 1px solid var(--border); margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.75rem;">
                        <div>
                            <h4 style="color: #38bdf8; margin: 0; display: flex; align-items: center; gap: 0.5rem;">
                                <span>🚛</span> Registre des Bons de Livraison Fournisseurs & Pesées Centrales
                            </h4>
                            <div style="font-size: 0.8rem; color: #94a3b8;">Suivi des tonnages enrobés, GNT, sables, bétons BPE et contrôle du rendement surface ($m^2/tonne$)</div>
                        </div>
                        <div style="display: flex; gap: 0.4rem;">
                            <button class="btn btn-secondary" onclick="exportLivraisonsCSV()">📥 Exporter Registre CSV</button>
                            <button class="btn btn-primary" onclick="openAddLivraisonModal()">➕ Saisir Bon de Pesée</button>
                        </div>
                    </div>

                    <!-- Summary KPIs -->
                    <div class="grid-4-col" style="gap: 0.5rem; margin-bottom: 1rem;">
                        <div style="background: #0b1120; border: 1px solid var(--border); border-radius: 6px; padding: 0.6rem; text-align: center;">
                            <div style="font-size: 0.75rem; color: #94a3b8;">Enrobés Bitumineux Livrés</div>
                            <div id="kpi-livraison-enrobes" style="font-size: 1.2rem; font-weight: 800; color: #f59e0b;">428.50 t</div>
                        </div>
                        <div style="background: #0b1120; border: 1px solid var(--border); border-radius: 6px; padding: 0.6rem; text-align: center;">
                            <div style="font-size: 0.75rem; color: #94a3b8;">Graves GNT 0/31.5 & 0/20</div>
                            <div id="kpi-livraison-gnt" style="font-size: 1.2rem; font-weight: 800; color: #38bdf8;">1 240.00 t</div>
                        </div>
                        <div style="background: #0b1120; border: 1px solid var(--border); border-radius: 6px; padding: 0.6rem; text-align: center;">
                            <div style="font-size: 0.75rem; color: #94a3b8;">Bétons Prêts à l'Emploi (BPE)</div>
                            <div id="kpi-livraison-beton" style="font-size: 1.2rem; font-weight: 800; color: #22c55e;">84.50 m³</div>
                        </div>
                        <div style="background: #0b1120; border: 1px solid var(--border); border-radius: 6px; padding: 0.6rem; text-align: center;">
                            <div style="font-size: 0.75rem; color: #94a3b8;">Rendement Moyen Enrobés</div>
                            <div id="kpi-livraison-rendement" style="font-size: 1.2rem; font-weight: 800; color: #a855f7;">132 kg/m² (e = 5.5 cm)</div>
                        </div>
                    </div>

                    <!-- Deliveries Table -->
                    <div style="overflow-x: auto; max-height: 350px; border: 1px solid var(--border); border-radius: 6px;">
                        <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; text-align: left;">
                            <thead style="background: #020617; position: sticky; top: 0; z-index: 10;">
                                <tr style="border-bottom: 2px solid var(--border);">
                                    <th style="padding: 6px 10px; color: #94a3b8;">N° BL</th>
                                    <th style="padding: 6px 10px; color: #94a3b8;">Date / Heure</th>
                                    <th style="padding: 6px 10px; color: #94a3b8;">Fournisseur / Centrale</th>
                                    <th style="padding: 6px 10px; color: #38bdf8;">Matériau / Formule</th>
                                    <th style="padding: 6px 10px; color: #f59e0b;">Immat. / Transporteur</th>
                                    <th style="padding: 6px 10px; color: #22c55e;">Quantité Pesée</th>
                                    <th style="padding: 6px 10px; color: #ef4444;">Température T°C</th>
                                    <th style="padding: 6px 10px; color: #a855f7;">Localisation Chantier</th>
                                    <th style="padding: 6px 10px; color: #94a3b8;">Statut</th>
                                </tr>
                            </thead>
                            <tbody id="rdc-livraisons-table-body">
                                <!-- Populated dynamically by renderRdcLivraisonsTable() -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
"""

# Insert rdc_livraisons_html before end of tab-rdc
pos_rdc_end = text.find('id="tab-compagnon_mobile"')
if pos_rdc_end != -1:
    pos_tab_rdc_div = text.rfind('</div>\n        </div>\n    </div>', 0, pos_rdc_end)
    if pos_tab_rdc_div != -1:
        text = text[:pos_tab_rdc_div] + rdc_livraisons_html + text[pos_tab_rdc_div:]
        print("Injected rdc_livraisons_html into tab-rdc!")

# 3. Update Planning Tab to include Weather Delay Tracker & Critical Path
old_planning_header = """<button class="btn-secondary plan-view-btn" id="btn-plan-taches" onclick="setPlanningViewMode('taches')">📑 Suivi des Tâches & Retards</button>
                    </div>"""

new_planning_header = """<button class="btn-secondary plan-view-btn" id="btn-plan-taches" onclick="setPlanningViewMode('taches')">📑 Suivi des Tâches & Retards</button>
                        <button class="btn-secondary plan-view-btn" id="btn-plan-intemperies" onclick="setPlanningViewMode('intemperies')">🌧️ Décompte Intempéries CCAG</button>
                    </div>"""

text = text.replace(old_planning_header, new_planning_header)

planning_intemperies_html = """
            <!-- 4. PLANNING INTEMPERIES & PROLONGATION CCAG VIEW -->
            <div id="planning-intemperies-view" style="display: none;">
                <div class="card" style="background: rgba(15,23,42,0.6); border: 1px solid var(--border); margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.75rem;">
                        <div>
                            <h4 style="color: #38bdf8; margin: 0; display: flex; align-items: center; gap: 0.5rem;">
                                <span>🌧️</span> Registre des Arrêts pour Intempéries & Prolongation Contractuelle (CCAG Art. 18.2.3)
                            </h4>
                            <div style="font-size: 0.8rem; color: #94a3b8;">Décompte légal des journées d'intempéries indemnisables (Pluie > 10 mm, Vent violent, Gel) et calcul du report de la date limite de réception</div>
                        </div>
                        <div style="display: flex; gap: 0.4rem;">
                            <button class="btn btn-secondary" onclick="exportIntemperiesCSV()">📥 Exporter Registre CSV</button>
                            <button class="btn btn-primary" onclick="openAddIntemperieModal()">➕ Déclarer Journée d'Intempérie</button>
                        </div>
                    </div>

                    <div class="grid-4-col" style="gap: 0.5rem; margin-bottom: 1rem;">
                        <div style="background: #0b1120; border: 1px solid var(--border); border-radius: 6px; padding: 0.6rem; text-align: center;">
                            <div style="font-size: 0.75rem; color: #94a3b8;">Jours d'Intempéries Constatés</div>
                            <div id="kpi-intemperies-jours" style="font-size: 1.2rem; font-weight: 800; color: #38bdf8;">6 Jours Ouvrés</div>
                        </div>
                        <div style="background: #0b1120; border: 1px solid var(--border); border-radius: 6px; padding: 0.6rem; text-align: center;">
                            <div style="font-size: 0.75rem; color: #94a3b8;">Jours Prévisibles Marché</div>
                            <div style="font-size: 1.2rem; font-weight: 800; color: #94a3b8;">3 Jours (CCAP)</div>
                        </div>
                        <div style="background: #0b1120; border: 1px solid var(--border); border-radius: 6px; padding: 0.6rem; text-align: center;">
                            <div style="font-size: 0.75rem; color: #94a3b8;">Dépassement Justifié</div>
                            <div id="kpi-intemperies-depassement" style="font-size: 1.2rem; font-weight: 800; color: #22c55e;">+3 Jours de Droit</div>
                        </div>
                        <div style="background: #0b1120; border: 1px solid var(--border); border-radius: 6px; padding: 0.6rem; text-align: center;">
                            <div style="font-size: 0.75rem; color: #94a3b8;">Nouvelle Date Réception Contractuelle</div>
                            <div id="kpi-intemperies-nouvelle-date" style="font-size: 1.2rem; font-weight: 800; color: #f59e0b;">28 Octobre 2026</div>
                        </div>
                    </div>

                    <div style="overflow-x: auto; max-height: 280px; border: 1px solid var(--border); border-radius: 6px;">
                        <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; text-align: left;">
                            <thead style="background: #020617; position: sticky; top: 0; z-index: 10;">
                                <tr style="border-bottom: 2px solid var(--border);">
                                    <th style="padding: 6px 10px; color: #94a3b8;">Date Constat</th>
                                    <th style="padding: 6px 10px; color: #38bdf8;">Phénomène Météo</th>
                                    <th style="padding: 6px 10px; color: #94a3b8;">Valeur Mesurée</th>
                                    <th style="padding: 6px 10px; color: #ef4444;">Tâches Directement Bloquées</th>
                                    <th style="padding: 6px 10px; color: #f59e0b;">Chômage Intempéries CNETP</th>
                                    <th style="padding: 6px 10px; color: #22c55e;">Validation Maître d'Œuvre</th>
                                </tr>
                            </thead>
                            <tbody id="planning-intemperies-table-body">
                                <!-- Populated dynamically by renderPlanningIntemperiesTable() -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
"""

# Insert planning_intemperies_html into tab-planning
pos_plan_end = text.find('id="tab-simulator"')
if pos_plan_end != -1:
    pos_tab_plan_div = text.rfind('</div>\n        </div>\n    </div>', 0, pos_plan_end)
    if pos_tab_plan_div != -1:
        text = text[:pos_tab_plan_div] + planning_intemperies_html + text[pos_tab_plan_div:]
        print("Injected planning_intemperies_html into tab-planning!")

# 4. Update tab-safety to include 1/4h Security Briefings
old_safety_header = """<button class="btn btn-secondary" id="btn-aipr-blindage-toggle" onclick="toggleAiprBlindage()">🛡️ Blindage R4534 : ACTIF</button>
                    <button class="btn btn-primary" onclick="openSafetyVisionAuditorModal()">📸 Audit Vision IA Sécurité (EPI / Fouilles)</button>
                    <button class="btn btn-danger" onclick="openSafetyEmergencySimulator()">🚨 Simuler Rupture & Urgence</button>"""

new_safety_header = """<button class="btn btn-secondary" id="btn-aipr-blindage-toggle" onclick="toggleAiprBlindage()">🛡️ Blindage R4534 : ACTIF</button>
                    <button class="btn btn-secondary" onclick="openSafetyQuarterHourModal()">📋 Fiches 1/4h Sécurité OPPBTP</button>
                    <button class="btn btn-primary" onclick="openSafetyVisionAuditorModal()">📸 Audit Vision IA Sécurité (EPI / Fouilles)</button>
                    <button class="btn btn-danger" onclick="openSafetyEmergencySimulator()">🚨 Simuler Rupture & Urgence</button>"""

text = text.replace(old_safety_header, new_safety_header)

with open("scripts/section_tab_panels.py", "w", encoding="utf-8") as f:
    f.write(text)

print("scripts/section_tab_panels.py successfully updated with v53 views!")
