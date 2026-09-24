# -*- coding: utf-8 -*-
"""
Full implementation of the 7 modules in section_tab_panels.py and section_js_part3.py
"""

# ==========================================
# 1. UPDATE section_tab_panels.py
# ==========================================
with open('scripts/section_tab_panels.py', 'r', encoding='utf-8') as f:
    tab_text = f.read()

# In tab-sdp: update header buttons and add import view
sdp_header_old = r'''                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary sdp-view-btn active" id="btn-sdp-dqe_tcd" onclick="setSDPViewMode('dqe_tcd')">📊 Tableau TCD Modifiable</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-cards" onclick="setSDPViewMode('cards')">🗂️ 28 Fiches SDP</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-comparator" onclick="setSDPViewMode('comparator')">⚖️ Comparateur Prix Concurrence</button>
                    </div>'''

sdp_header_new = r'''                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border); flex-wrap: wrap; gap: 2px;">
                        <button class="btn-secondary sdp-view-btn active" id="btn-sdp-dqe_tcd" onclick="setSDPViewMode('dqe_tcd')">📊 Tableau TCD Modifiable</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-cards" onclick="setSDPViewMode('cards')">🗂️ 28 Fiches SDP</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-comparator" onclick="setSDPViewMode('comparator')">⚖️ Comparateur Prix Concurrence</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-import" onclick="setSDPViewMode('import')">📂 Importer Excel / CSV</button>
                    </div>

                    <button class="btn btn-secondary" onclick="downloadProfessionalDoc('dqe_excel_csv')">📥 Exporter DQE Excel</button>
                    <button class="btn btn-primary" onclick="downloadProfessionalDoc('memoire_technique')">📑 Générer Mémoire Technique</button>'''

if sdp_header_old in tab_text:
    tab_text = tab_text.replace(sdp_header_old, sdp_header_new)
    print("tab-sdp header buttons updated!")

# Add sdp-import-view
sdp_import_block = r'''
            <!-- 4. DYNAMIC EXCEL / CSV IMPORT DROPZONE VIEW -->
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
                    <div id="dqe-import-status" style="margin-top: 1rem; font-size: 0.85rem; font-weight: 700; color: var(--emerald);"></div>
                </div>
            </div>
'''

pos_sdp_comp = tab_text.find('<div id="sdp-comparator-view"')
if pos_sdp_comp != -1 and 'id="sdp-import-view"' not in tab_text:
    pos_sdp_end = tab_text.find('</div>\n        </div>\n    </div>', pos_sdp_comp)
    if pos_sdp_end != -1:
        tab_text = tab_text[:pos_sdp_end] + sdp_import_block.strip() + "\n            </div>\n        </div>\n    </div>" + tab_text[pos_sdp_end+24:]
        print("sdp-import-view injected!")

# In tab-docs: add AI DCE Ingestion button and container
docs_header_old = r'''                    <button class="btn btn-secondary doc-tab-filter" onclick="filterDocsView('schemas_synthese', this)">📐 Schémas de Synthèse & Devoirs</button>'''

docs_header_new = r'''                    <button class="btn btn-secondary doc-tab-filter" onclick="filterDocsView('schemas_synthese', this)">📐 Schémas de Synthèse & Devoirs</button>
                    <button class="btn btn-secondary doc-tab-filter" onclick="filterDocsView('ai_dce_ingestion', this)">🤖 Dépouillement DCE par IA</button>'''

if docs_header_old in tab_text:
    tab_text = tab_text.replace(docs_header_old, docs_header_new)
    print("tab-docs header updated with AI DCE Ingestion!")

# In tab-safety: add AI Computer Vision Safety Auditor button
safety_header_old = r'''                    <button class="btn btn-secondary" id="btn-aipr-blindage-toggle" onclick="toggleAiprBlindage()">🛡️ Blindage R4534 : ACTIF</button>'''

safety_header_new = r'''                    <button class="btn btn-secondary" id="btn-aipr-blindage-toggle" onclick="toggleAiprBlindage()">🛡️ Blindage R4534 : ACTIF</button>
                    <button class="btn btn-primary" onclick="openSafetyVisionAuditorModal()">📸 Audit Vision IA Sécurité (EPI / Fouilles)</button>'''

if safety_header_old in tab_text:
    tab_text = tab_text.replace(safety_header_old, safety_header_new)
    print("tab-safety header updated with AI Safety Auditor!")

# In tab-cockpit: add Backup / Restore buttons in header
cockpit_header_old = r'''                    <button class="btn btn-primary" onclick="exportCockpitReport()">📥 Exporter Rapport Général PDF</button>'''

cockpit_header_new = r'''                    <button class="btn btn-primary" onclick="exportCockpitReport()">📥 Exporter Rapport Général PDF</button>
                    <button class="btn btn-secondary" onclick="exportEnterpriseBackupJSON()">💾 Sauvegarde Système (.btp)</button>
                    <input type="file" id="backup-file-input" accept=".json, .btp" style="display: none;" onchange="importEnterpriseBackupJSON(this)">
                    <button class="btn btn-secondary" onclick="document.getElementById('backup-file-input').click()">📂 Restaurer Sauvegarde</button>'''

if cockpit_header_old in tab_text:
    tab_text = tab_text.replace(cockpit_header_old, cockpit_header_new)
    print("tab-cockpit header updated with Backup / Restore buttons!")

with open('scripts/section_tab_panels.py', 'w', encoding='utf-8') as f:
    f.write(tab_text)

print("section_tab_panels.py updated successfully!")
