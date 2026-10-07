# -*- coding: utf-8 -*-
"""
Master Patch to implement:
- Module 1: Real Document Download Engine (PDF, HTML printable, Excel CSV, DC4, DGD, Memoire Technique, Factur-X)
- Module 2: Daily Crew Timesheets & DQE Real-time Profitability (Pointage RH & Écarts)
- Module 3: Dynamic Excel/CSV Import for BPU/DQE
- Module 4: Heavy Vehicle Routing & Trackdéchets BSDD Logistics (Bassin de Thau)
- Module 5: PWA Offline & Backup/Restore Engine (.btp-backup)
- Module 6: AI DCE Ingestion & Clause Extractor
- Module 7: Computer Vision Safety Auditor (PPE & Trench Shoring Inspection)
"""

# 1. Update section_tab_panels.py
with open('scripts/section_tab_panels.py', 'r', encoding='utf-8') as f:
    tab_panels_text = f.read()

# Let's add sub-navigation and panels in tab-rdc
old_rdc_header = r'''                    <span class="card-title">📋 Journal Quotidien de Chantier (RDC) & Prises de Vue Multi-Sources</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Pointage des équipes, heures engins, métrés exécutés, météo et photos de suivi</div>
                </div>
                <div style="display: flex; gap: 0.4rem;">
                    <button class="btn btn-primary" onclick="openRdcCameraModal()">📸 Capturer Photo Chantier (Webcam / Drone)</button>
                    <button class="btn btn-secondary" onclick="exportRdcPDF()">📥 Exporter RDC en PDF</button>
                </div>'''

new_rdc_header = r'''                    <span class="card-title">📋 Journal Quotidien de Chantier (RDC) & Pointage RH des Équipes</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Pointage nominatif des ouvriers, heures engins, métrés exécutés et rentabilité DQE en direct</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary rdc-view-btn active" id="btn-rdc-rapport" onclick="setRdcViewMode('rapport')">📝 Rapport Quotidien</button>
                        <button class="btn-secondary rdc-view-btn" id="btn-rdc-pointage" onclick="setRdcViewMode('pointage')">👷 Pointage des Équipes</button>
                        <button class="btn-secondary rdc-view-btn" id="btn-rdc-rentabilite" onclick="setRdcViewMode('rentabilite')">📊 Rentabilité Heures DQE</button>
                    </div>
                    <button class="btn btn-secondary" onclick="openRdcCameraModal()">📸 Photo Chantier</button>
                    <button class="btn btn-primary" onclick="downloadProfessionalDoc('rdc_pdf')">📥 Exporter RDC PDF</button>
                </div>'''

if old_rdc_header in tab_panels_text:
    tab_panels_text = tab_panels_text.replace(old_rdc_header, new_rdc_header)
    print("tab-rdc header updated with pointage & rentabilité navigation!")

# Let's add the pointage and rentabilité views inside tab-rdc
old_rdc_content = r'''            <!-- RDC FORM & ENTRIES GRID -->
            <div class="grid-split-40-60">'''

new_rdc_content = r'''            <!-- 1. RDC RAPPORT VIEW -->
            <div id="rdc-rapport-view">
            <div class="grid-split-40-60">'''

if old_rdc_content in tab_panels_text:
    tab_panels_text = tab_panels_text.replace(old_rdc_content, new_rdc_content)

old_rdc_end = r'''                <div id="rdc-entries-list">
                    <!-- Populated dynamically -->
                </div>
            </div>
        </div>
    </div>'''

new_rdc_end = r'''                <div id="rdc-entries-list">
                    <!-- Populated dynamically -->
                </div>
            </div>
            </div>

            <!-- 2. POINTAGE DES ÉQUIPES VIEW -->
            <div id="rdc-pointage-view" style="display: none; margin-top: 1rem;">
                <div style="background: rgba(15,23,42,0.95); border: 1px solid var(--border); border-radius: 8px; padding: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
                        <div>
                            <h4 style="font-size: 1rem; font-weight: 800; color: #38bdf8;">👷 Grille de Pointage Nominatif Journalier des Salariés (Semaine en Cours)</h4>
                            <div style="font-size: 0.75rem; color: #94a3b8;">Heures Normales (HN), Heures Sup (+25%/+50%), Paniers repas, Zones de déplacement et Intempéries</div>
                        </div>
                        <div style="display: flex; gap: 0.4rem;">
                            <button class="btn btn-secondary" onclick="saveCrewPointage()">💾 Enregistrer Pointage</button>
                            <button class="btn btn-primary" onclick="exportPointageCSV()">📥 Exporter Pointage CSV</button>
                        </div>
                    </div>
                    <div style="overflow-x: auto;">
                        <table style="width: 100%; border-collapse: collapse; font-size: 0.78rem; min-width: 950px;">
                            <thead>
                                <tr style="background: rgba(30,41,59,0.9); color: #94a3b8; text-align: left;">
                                    <th style="padding: 0.5rem;">SALARIÉ / QUALIFICATION</th>
                                    <th style="padding: 0.5rem;">ÉQUIPE</th>
                                    <th style="padding: 0.5rem; text-align: right;">THMO (€/h)</th>
                                    <th style="padding: 0.5rem; text-align: center;">LUN</th>
                                    <th style="padding: 0.5rem; text-align: center;">MAR</th>
                                    <th style="padding: 0.5rem; text-align: center;">MER</th>
                                    <th style="padding: 0.5rem; text-align: center;">JEU</th>
                                    <th style="padding: 0.5rem; text-align: center;">VEN</th>
                                    <th style="padding: 0.5rem; text-align: center; color: var(--emerald); font-weight: 800;">TOTAL (h)</th>
                                    <th style="padding: 0.5rem; text-align: center;">PANIERS</th>
                                    <th style="padding: 0.5rem; text-align: center;">TRAJET</th>
                                    <th style="padding: 0.5rem; text-align: right; color: #38bdf8;">COÛT RÉEL (€)</th>
                                </tr>
                            </thead>
                            <tbody id="rdc-pointage-tbody">
                                <!-- Populated dynamically by renderCrewPointageTable() -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- 3. RENTABILITÉ HEURES DQE VIEW -->
            <div id="rdc-rentabilite-view" style="display: none; margin-top: 1rem;">
                <div style="background: rgba(15,23,42,0.95); border: 1px solid var(--border); border-radius: 8px; padding: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
                        <div>
                            <h4 style="font-size: 1rem; font-weight: 800; color: #38bdf8;">📊 Suivi de Rentabilité Main d'Œuvre : Heures Prévues (DQE) vs Heures Réelles</h4>
                            <div style="font-size: 0.75rem; color: #94a3b8;">Détection en direct des dérives de productivité, écarts financiers (€) et avancement physique des ouvrages</div>
                        </div>
                        <button class="btn btn-primary" onclick="downloadProfessionalDoc('variance_dqe_pdf')">📥 Rapport d'Écarts PDF</button>
                    </div>
                    <div style="overflow-x: auto;">
                        <table style="width: 100%; border-collapse: collapse; font-size: 0.78rem; min-width: 900px;">
                            <thead>
                                <tr style="background: rgba(30,41,59,0.9); color: #94a3b8; text-align: left;">
                                    <th style="padding: 0.5rem;">CODE DQE</th>
                                    <th style="padding: 0.5rem;">DÉSIGNATION DE L'OUVRAGE</th>
                                    <th style="padding: 0.5rem; text-align: center;">QTÉ RÉALISÉE</th>
                                    <th style="padding: 0.5rem; text-align: right;">TU ÉTUDE (h/u)</th>
                                    <th style="padding: 0.5rem; text-align: right;">HEURES PRÉVUES</th>
                                    <th style="padding: 0.5rem; text-align: right; color: var(--amber);">HEURES PASSÉES</th>
                                    <th style="padding: 0.5rem; text-align: center;">PRODUCTIVITÉ</th>
                                    <th style="padding: 0.5rem; text-align: right; color: var(--emerald);">ÉCART FINANCIER (€)</th>
                                </tr>
                            </thead>
                            <tbody id="rdc-rentabilite-tbody">
                                <!-- Populated dynamically by renderRdcRentabiliteTable() -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>'''

if old_rdc_end in tab_panels_text:
    tab_panels_text = tab_panels_text.replace(old_rdc_end, new_rdc_end)
    print("tab-rdc views added successfully!")

# Let's add the Excel Import Zone in tab-sdp
old_sdp_header = r'''                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary sdp-view-btn active" id="btn-sdp-tcd" onclick="setSdpPresentationMode('dqe_tcd')">📊 TCD & Tableau DQE</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-cards" onclick="setSdpPresentationMode('cards')">📐 28 Cartes SDP</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-ratios" onclick="setSdpPresentationMode('ratios')">⚖️ Ratios & Rendements</button>
                    </div>
                    <button class="btn btn-secondary" onclick="exportDqeCSV()">📥 Exporter DQE CSV</button>
                </div>'''

new_sdp_header = r'''                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap; align-items: center;">
                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary sdp-view-btn active" id="btn-sdp-tcd" onclick="setSdpPresentationMode('dqe_tcd')">📊 TCD & Tableau DQE</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-cards" onclick="setSdpPresentationMode('cards')">📐 28 Cartes SDP</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-ratios" onclick="setSdpPresentationMode('ratios')">⚖️ Ratios & Rendements</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-import" onclick="setSdpPresentationMode('import')">📂 Importer Excel / CSV</button>
                    </div>
                    <button class="btn btn-secondary" onclick="downloadProfessionalDoc('dqe_excel_csv')">📥 Exporter DQE Excel</button>
                    <button class="btn btn-primary" onclick="downloadProfessionalDoc('memoire_technique')">📑 Générer Mémoire Technique</button>
                </div>'''

if old_sdp_header in tab_panels_text:
    tab_panels_text = tab_panels_text.replace(old_sdp_header, new_sdp_header)
    print("tab-sdp header updated with Excel import & Mémoire technique!")

# Add sdp-import-view container right before closing of tab-sdp
sdp_import_html = r'''
            <!-- 4. EXCEL / CSV IMPORT DROPZONE VIEW -->
            <div id="sdp-import-view" style="display: none; margin-top: 1rem;">
                <div style="background: rgba(15,23,42,0.95); border: 2px dashed rgba(56,189,248,0.5); border-radius: 8px; padding: 2rem; text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📂</div>
                    <h3 style="font-size: 1.1rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.4rem;">Glissez-déposez votre Bordereau Excel / CSV de Marché Public (BPU / DQE)</h3>
                    <p style="font-size: 0.8rem; color: #cbd5e1; max-width: 600px; margin: 0 auto 1.25rem auto;">
                        Le parseur intelligent extrait automatiquement les colonnes (Code article, Désignation, Unité, Quantité, Prix Unitaire), calcule le déboursé sec total, génère le TCD et applique votre coefficient de marge K.
                    </p>
                    <div style="display: flex; justify-content: center; gap: 0.6rem; flex-wrap: wrap;">
                        <input type="file" id="dqe-file-input" accept=".csv, .xlsx, .xls, .txt" style="display: none;" onchange="handleDQEFileUpload(this)">
                        <button class="btn btn-primary" onclick="document.getElementById('dqe-file-input').click()">📄 Parcourir les Fichiers (.xlsx / .csv)</button>
                        <button class="btn btn-secondary" onclick="loadSampleDQEFile()">⚡ Charger Fichier Exemple Marché Barbazan</button>
                    </div>
                    <div id="dqe-import-status" style="margin-top: 1rem; font-size: 0.8rem; font-weight: 700; color: var(--emerald);"></div>
                </div>
            </div>
'''

pos_sdp_ratios = tab_panels_text.find('id="sdp-ratios-view"')
if pos_sdp_ratios != -1:
    pos_sdp_close = tab_panels_text.find('</div>\n    </div>', pos_sdp_ratios)
    if pos_sdp_close != -1:
        tab_panels_text = tab_panels_text[:pos_sdp_close] + sdp_import_html.strip() + "\n        " + tab_panels_text[pos_sdp_close:]
        print("sdp-import-view added to section_tab_panels.py!")

with open('scripts/section_tab_panels.py', 'w', encoding='utf-8') as f:
    f.write(tab_panels_text)
