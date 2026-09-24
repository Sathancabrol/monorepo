#!/usr/bin/env python3
"""
Patch v55: Add Devis Express VRD view to tab-sdp, update setSDPViewMode, and align all remaining DOM elements
"""

import re

# 1. Update scripts/section_tab_panels.py
with open("scripts/section_tab_panels.py", "r", encoding="utf-8") as f:
    panels = f.read()

# 1.1 Add express button to tab-sdp
old_sdp_buttons = """<button class="btn-secondary sdp-view-btn active" id="btn-sdp-dqe_tcd" onclick="setSDPViewMode('dqe_tcd')">📊 Tableau TCD Modifiable</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-cards" onclick="setSDPViewMode('cards')">🗂️ 28 Fiches SDP</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-comparator" onclick="setSDPViewMode('comparator')">⚖️ Comparateur Prix Concurrence</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-import" onclick="setSDPViewMode('import')">📂 Importer Excel / CSV</button>"""

new_sdp_buttons = """<button class="btn-secondary sdp-view-btn active" id="btn-sdp-dqe_tcd" onclick="setSDPViewMode('dqe_tcd')">📊 Tableau TCD Modifiable</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-cards" onclick="setSDPViewMode('cards')">🗂️ 28 Fiches SDP</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-comparator" onclick="setSDPViewMode('comparator')">⚖️ Comparateur Concurrence</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-express" onclick="setSDPViewMode('express')">⚡ Devis Express VRD</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-import" onclick="setSDPViewMode('import')">📂 Importer Excel / CSV</button>"""

panels = panels.replace(old_sdp_buttons, new_sdp_buttons)

# 1.2 Add sdp-express-view container
sdp_express_view_html = """
            <!-- 5. SDP EXPRESS ESTIMATOR VIEW -->
            <div id="sdp-express-view" style="display: none;">
                <div class="card" style="background: rgba(15,23,42,0.7); border: 1px solid rgba(56,189,248,0.3); margin-bottom: 1rem;">
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
            </div>
"""

# Insert before end of tab-sdp
pos_sdp_import = panels.find('id="sdp-import-view"')
if pos_sdp_import != -1:
    pos_end_import = panels.find('</div>', pos_sdp_import) + 6
    panels = panels[:pos_end_import] + sdp_express_view_html + panels[pos_end_import:]
    print("Injected sdp-express-view!")

# 1.3 Ensure Planning tab has project and team select filters
pos_plan = panels.find('id="tab-planning"')
if pos_plan != -1:
    pos_plan_header = panels.find('class="card-header"', pos_plan)
    if pos_plan_header != -1 and 'id="planning-project-select"' not in panels:
        plan_filters_html = """
            <!-- PLANNING FILTERS -->
            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.75rem; align-items: center; background: rgba(15,23,42,0.8); padding: 0.5rem 0.75rem; border-radius: 6px; border: 1px solid var(--border);">
                <span style="font-size: 0.8rem; font-weight: 700; color: #38bdf8;">🔍 Filtrer :</span>
                <select id="planning-project-select" class="select-field" style="width: auto; padding: 0.25rem 0.5rem; font-size: 0.75rem;" onchange="renderPlanningAgenda()">
                    <option value="all">Tous les Chantiers</option>
                    <option value="giratoire_barbazan">Giratoire Barbazan</option>
                    <option value="lotissement_aurouer">Lotissement Aurouer</option>
                    <option value="saint_nicolas_grave">Saint-Nicolas-de-la-Grave</option>
                </select>
                <select id="planning-team-select" class="select-field" style="width: auto; padding: 0.25rem 0.5rem; font-size: 0.75rem;" onchange="renderPlanningAgenda()">
                    <option value="all">Toutes les Équipes</option>
                    <option value="team_a">Équipe A - Terrassement</option>
                    <option value="team_b">Équipe B - Canalisations</option>
                    <option value="team_c">Équipe C - Enrobés</option>
                    <option value="team_d">Équipe D - Maçonnerie</option>
                </select>
            </div>
        """
        pos_after_header = panels.find('</div>', pos_plan_header) + 6
        panels = panels[:pos_after_header] + plan_filters_html + panels[pos_after_header:]
        print("Injected planning filters!")

# 1.4 In Company Cashflow tab, ensure cashflow-formulas-box and company-cashflow-table-body exist
if 'id="cashflow-formulas-box"' not in panels:
    pos_comp_card = panels.find('id="tab-company"')
    if pos_comp_card != -1:
        cashflow_box_html = """
            <div id="cashflow-formulas-box" style="display: none; background: #020617; border: 1px solid var(--border); border-radius: 6px; padding: 0.75rem; margin-bottom: 1rem; font-size: 0.8rem;">
                <div style="font-weight: 700; color: #38bdf8; margin-bottom: 4px;">📐 Formules Financières CCAG Travaux :</div>
                <div>• <strong>Besoin en Fonds de Roulement (BFR)</strong> : $BFR = \\text{Stocks} + \\text{Créances Clients (Situations émises)} - \\text{Dettes Fournisseurs/Sous-traitants}$.</div>
                <div>• <strong>Retenue de Garantie</strong> : $5\\% \\text{ HT}$ prélevée sur chaque acompte mensuel (Chorus Pro), libérée à la réception sans réserve (DGD).</div>
                <div>• <strong>Avance Forfaitaire</strong> : $10\\%$ du montant du marché HT si délai > 2 mois, remboursée par précompte sur acomptes dès $65\\%$ d'avancement.</div>
            </div>
        """
        pos_comp_insert = panels.find('class="grid-4"', pos_comp_card)
        if pos_comp_insert != -1:
            panels = panels[:pos_comp_insert] + cashflow_box_html + panels[pos_comp_insert:]
            print("Injected cashflow-formulas-box!")

with open("scripts/section_tab_panels.py", "w", encoding="utf-8") as f:
    f.write(panels)

# 2. Update scripts/section_js_part3.py for setSDPViewMode
with open("scripts/section_js_part3.py", "r", encoding="utf-8") as f:
    js_text = f.read()

old_sdp_view_func = """function setSDPViewMode(mode) {
        sdpViewMode = mode;
        document.querySelectorAll('.sdp-view-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('btn-sdp-' + mode)?.classList.add('active');

        const dqeView = document.getElementById('sdp-dqe-tcd-view');
        const cardsView = document.getElementById('sdp-cards-view');
        const compView = document.getElementById('sdp-comparator-view');

        if (dqeView) dqeView.style.display = mode === 'dqe_tcd' ? 'block' : 'none';
        if (cardsView) cardsView.style.display = mode === 'cards' ? 'grid' : 'none';
        if (compView) compView.style.display = mode === 'comparator' ? 'block' : 'none';

        if (mode === 'comparator') renderConcurrenceTable();
    }"""

new_sdp_view_func = """function setSDPViewMode(mode) {
        sdpViewMode = mode;
        document.querySelectorAll('.sdp-view-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('btn-sdp-' + mode)?.classList.add('active');

        const dqeView = document.getElementById('sdp-dqe-tcd-view');
        const cardsView = document.getElementById('sdp-cards-view');
        const compView = document.getElementById('sdp-comparator-view');
        const impView = document.getElementById('sdp-import-view');
        const expView = document.getElementById('sdp-express-view');

        if (dqeView) dqeView.style.display = mode === 'dqe_tcd' ? 'block' : 'none';
        if (cardsView) cardsView.style.display = mode === 'cards' ? 'grid' : 'none';
        if (compView) compView.style.display = mode === 'comparator' ? 'block' : 'none';
        if (impView) impView.style.display = mode === 'import' ? 'block' : 'none';
        if (expView) expView.style.display = mode === 'express' ? 'block' : 'none';

        if (mode === 'comparator') renderConcurrenceTable();
        if (mode === 'express') calculateDevisExpress();
    }"""

if old_sdp_view_func in js_text:
    js_text = js_text.replace(old_sdp_view_func, new_sdp_view_func)
    print("Updated setSDPViewMode function in js_part3!")

with open("scripts/section_js_part3.py", "w", encoding="utf-8") as f:
    f.write(js_text)

print("Patch v55 executed successfully!")
