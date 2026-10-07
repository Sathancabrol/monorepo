#!/usr/bin/env python3
"""
Patch v68: 4X Hexagonal Territory Grid, Public Market Tender Explorer, Colas Sète Simulation, and Clean UI
"""

import re

# ==============================================================================
# 1. UPDATE scripts/section_head_and_styles.py (REMOVE .quick-hub-bar)
# ==============================================================================
with open("scripts/section_head_and_styles.py", "r", encoding="utf-8") as f:
    head_code = f.read()

# Remove quick-hub-bar HTML and CSS
head_code = re.sub(r'/\* =+ \*/\s*/\* 3\. QUICK-HUB DOCK.*?\*/[\s\S]*?/\* =+ \*/\s*/\* 4\. LEFT FLYOUT', '/* ========================================== */\n        /* 3. LEFT FLYOUT', head_code)
head_code = re.sub(r'<!-- =+ -->\s*<!-- 3\. QUICK-HUB DOCK.*?-->\s*<div class="quick-hub-bar"[\s\S]*?</div>', '', head_code)

with open("scripts/section_head_and_styles.py", "w", encoding="utf-8") as f:
    f.write(head_code)
print("Removed duplicate quick-hub-bar from section_head_and_styles.py!")

# ==============================================================================
# 2. UPDATE scripts/section_tab_panels.py (COCKPIT HEX GRID & PROJECTS HUB MARKET EXPLORER)
# ==============================================================================
with open("scripts/section_tab_panels.py", "r", encoding="utf-8") as f:
    tab_code = f.read()

# In tab-cockpit, add onboarding card + 4X Hex Grid toggle in SIG Map card
old_cockpit_map_header = """                    <div>
                        <span class="card-title">🗺️ Cartographie SIG des Chantiers & Flotte (Occitanie)</span>
                        <div style="font-size: 0.75rem; color: #94a3b8;">Déclic anti-collision radial, filtres d'affichage et géolocalisation live</div>
                    </div>
                    <div style="display: flex; gap: 0.3rem; align-items: center; flex-wrap: wrap;">"""

new_cockpit_map_header = """                    <div>
                        <span class="card-title" id="cockpit-map-title">🗺️ Cartographie SIG & Stratégie Territoriale (Sète / Bassin de Thau)</span>
                        <div style="font-size: 0.82rem; color: #cbd5e1;">Surveillance géospatiale, flux d'enrobés/GNT et contrôle territorial</div>
                    </div>
                    <div style="display: flex; gap: 0.4rem; align-items: center; flex-wrap: wrap;">
                        <button class="btn btn-secondary active" id="btn-map-satellite" onclick="window.toggleCockpitMapView('satellite')" style="font-size:0.8rem; padding:0.35rem 0.65rem;">🗺️ Satellite HD</button>
                        <button class="btn btn-secondary" id="btn-map-hex" onclick="window.toggleCockpitMapView('hexgrid')" style="font-size:0.8rem; padding:0.35rem 0.65rem; border-color:#f59e0b; color:#fbbf24;">⬡ Grille Hexagonale 4X</button>"""

if old_cockpit_map_header in tab_code:
    tab_code = tab_code.replace(old_cockpit_map_header, new_cockpit_map_header)

# Add hex container inside cockpit map card
old_map_div = '<div id="cockpit-osm-map" style="height: 380px; width: 100%; border-radius: 6px; border: 1px solid var(--border); position: relative; z-index: 1;"></div>'
new_map_div = """<div id="cockpit-osm-map" style="height: 420px; width: 100%; border-radius: 8px; border: 1px solid var(--border); position: relative; z-index: 1;"></div>
                <div id="cockpit-hex-container" style="display: none; height: 420px; width: 100%; border-radius: 8px; border: 1px solid #f59e0b; background: #020617; position: relative; overflow: hidden;">
                    <!-- SVG / Canvas Hexagonal Grid rendered dynamically -->
                    <div id="hex-grid-viewport" style="width:100%; height:100%;"></div>
                </div>
                <!-- TERRITORIAL SECTOR INTEL DRAWER (POPUP ON HEX CLICK) -->
                <div id="hex-sector-intel" style="display:none; margin-top:0.75rem; background:rgba(15,23,42,0.95); border:1px solid #38bdf8; border-radius:8px; padding:0.85rem;">
                    <!-- Injected dynamically -->
                </div>"""

if old_map_div in tab_code:
    tab_code = tab_code.replace(old_map_div, new_map_div)

# Add pedagogical onboarding card right under cockpit start
onboarding_markup = """    <div id="tab-cockpit" class="tab-panel active">
        <!-- PEDAGOGICAL ONBOARDING CARD FOR COMPTE NEUF -->
        <div id="cockpit-onboarding-card" class="card" style="display:none; background:linear-gradient(135deg, rgba(2,132,199,0.25) 0%, rgba(15,23,42,0.98) 100%); border:2px solid #38bdf8; margin-bottom:1rem; padding:1.25rem; box-shadow:0 0 25px rgba(56,189,248,0.25);">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem;">
                <div style="flex:1;">
                    <div style="font-size:1.2rem; font-weight:900; color:#38bdf8; display:flex; align-items:center; gap:0.5rem;">
                        🎯 MISSION D'INITIATION TP : Créez ou Remportez votre Premier Chantier
                    </div>
                    <div style="font-size:0.9rem; color:#e2e8f0; margin:0.4rem 0 0.85rem 0;">
                        Bienvenue dans votre système de conduite de travaux ! Explorez les marchés publics territoriaux, réalisez les sous-détails de prix et planifiez vos premières rotations :
                    </div>
                    <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:0.75rem;">
                        <div style="background:rgba(2,6,23,0.85); border:1px solid rgba(56,189,248,0.3); border-radius:8px; padding:0.75rem;">
                            <strong style="color:#38bdf8; font-size:0.85rem;">1. MARCHÉS PUBLICS</strong>
                            <p style="font-size:0.78rem; color:#cbd5e1; margin-top:0.25rem;">Consultez les 4 appels d'offres ouverts à Sète & Thau.</p>
                            <button class="btn btn-primary" style="font-size:0.78rem; padding:0.35rem 0.6rem; width:100%; margin-top:0.5rem;" onclick="window.switchNav('projects_hub')">🔍 Voir Marchés</button>
                        </div>
                        <div style="background:rgba(2,6,23,0.85); border:1px solid rgba(56,189,248,0.3); border-radius:8px; padding:0.75rem;">
                            <strong style="color:#4ade80; font-size:0.85rem;">2. ÉTUDE DE PRIX (SDP)</strong>
                            <p style="font-size:0.78rem; color:#cbd5e1; margin-top:0.25rem;">Calculez déboursés secs, main-d'œuvre et matériaux.</p>
                            <button class="btn btn-secondary" style="font-size:0.78rem; padding:0.35rem 0.6rem; width:100%; margin-top:0.5rem;" onclick="window.switchNav('devis_express')">📐 Devis Express</button>
                        </div>
                        <div style="background:rgba(2,6,23,0.85); border:1px solid rgba(56,189,248,0.3); border-radius:8px; padding:0.75rem;">
                            <strong style="color:#fbbf24; font-size:0.85rem;">3. LOGISTIQUE & FLOTTE</strong>
                            <p style="font-size:0.78rem; color:#cbd5e1; margin-top:0.25rem;">Allouez engins, rotations 8x4 et centrales d'enrobage.</p>
                            <button class="btn btn-secondary" style="font-size:0.78rem; padding:0.35rem 0.6rem; width:100%; margin-top:0.5rem;" onclick="window.switchNav('materiel_depot')">🚜 Matériel & Stock</button>
                        </div>
                        <div style="background:rgba(2,6,23,0.85); border:1px solid rgba(56,189,248,0.3); border-radius:8px; padding:0.75rem;">
                            <strong style="color:#a855f7; font-size:0.85rem;">4. SÉCURITÉ & AIPR</strong>
                            <p style="font-size:0.78rem; color:#cbd5e1; margin-top:0.25rem;">Validez DICT, blindage tranchées et 1/4h sécurité.</p>
                            <button class="btn btn-secondary" style="font-size:0.78rem; padding:0.35rem 0.6rem; width:100%; margin-top:0.5rem;" onclick="window.switchNav('safety_qse')">🦺 Sécurité QSE</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>"""

if '<div id="tab-cockpit" class="tab-panel active">' in tab_code:
    tab_code = tab_code.replace('<div id="tab-cockpit" class="tab-panel active">', onboarding_markup)

# In tab-projects_hub, add Public Market Tender Explorer banner and action buttons
old_hub_header = """        <div class="card" style="margin-bottom: 1rem;">
            <div class="card-header">
                <div>
                    <span class="card-title">🏗️ Hub Central des 4 Chantiers Référents (DCE & Plans Intégrés)</span>
                    <div style="font-size: 0.75rem; color: #94a3b8;">Supervision contractuelle, technique, financière et planning global</div>
                </div>
                <div style="display: flex; gap: 0.4rem;">
                    <button class="btn btn-primary" onclick="window.exportProjectsSummaryPDF()">📄 Synthèse PDF Globale</button>
                </div>
            </div>"""

new_hub_header = """        <!-- TENDER & PUBLIC MARKET OPPORTUNITIES EXPLORER -->
        <div class="card" style="margin-bottom: 1rem; border:2px solid #38bdf8; background:linear-gradient(135deg, rgba(15,23,42,0.95) 0%, rgba(2,132,199,0.15) 100%);">
            <div class="card-header">
                <div>
                    <span class="card-title" style="color:#38bdf8; font-size:1.15rem;">🏛️ Place des Marchés Publics & Appels d'Offres Ouverts (Sète / Hérault)</span>
                    <div style="font-size: 0.85rem; color: #cbd5e1;">Explorez les marchés territoriaux disponibles, téléchargez les DCE simulés et générez vos offres</div>
                </div>
                <div style="display: flex; gap: 0.5rem;">
                    <button class="btn btn-primary" onclick="window.openMarketExplorerModal()">🔍 Explorer les Marchés Disponibles (4)</button>
                    <button class="btn btn-secondary" onclick="window.openCreateProjectModal()" style="border-color:#4ade80; color:#4ade80;">➕ Nouveau Chantier Manuel</button>
                </div>
            </div>
        </div>

        <div class="card" style="margin-bottom: 1rem;">
            <div class="card-header">
                <div>
                    <span class="card-title">🏗️ Hub Central des Chantiers en Exécution & Supervision</span>
                    <div style="font-size: 0.85rem; color: #94a3b8;">Supervision contractuelle, technique, financière et planning global</div>
                </div>
                <div style="display: flex; gap: 0.4rem;">
                    <button class="btn btn-primary" onclick="window.exportProjectsSummaryPDF()">📄 Synthèse PDF Globale</button>
                </div>
            </div>"""

if old_hub_header in tab_code:
    tab_code = tab_code.replace(old_hub_header, new_hub_header)

with open("scripts/section_tab_panels.py", "w", encoding="utf-8") as f:
    f.write(tab_code)
print("Updated section_tab_panels.py with Cockpit 4X Hex Grid and Projects Hub Market Explorer!")

# ==============================================================================
# 3. UPDATE scripts/section_modals.py (COLAS SETE SIMULATION + MARKET EXPLORER MODALS)
# ==============================================================================
with open("scripts/section_modals.py", "r", encoding="utf-8") as f:
    modals_code = f.read()

# Replace Occitanie TP card with Colas Sète in account-modal
old_occitanie_card = """                    <div class="catalog-card" style="cursor:pointer; border:1px solid #38bdf8; background:rgba(15,23,42,0.95); padding:1rem;" onclick="window.loginCompanyProfile('occitanie_tp')">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong style="color:#ffffff; font-size:1rem;">🏢 Occitanie TP & VRD (SAS)</strong>
                            <span class="badge-success" style="padding:2px 6px; border-radius:4px; font-size:0.75rem; font-weight:800;">RECOMMANDÉ</span>
                        </div>
                        <div style="font-size:0.82rem; color:#cbd5e1; margin:0.4rem 0;">PME Régionale Occitanie • Capital 250k€ • Trésorerie 485 200 €</div>
                        <div style="font-size:0.78rem; color:#94a3b8;">4 Chantiers actifs • 24 Salariés • Flotte 6 engins lourds</div>
                        <button class="btn btn-primary" style="margin-top:0.6rem; width:100%;">Se Connecter à cette Entreprise</button>
                    </div>"""

new_colas_card = """                    <div class="catalog-card" style="cursor:pointer; border:2px solid #f59e0b; background:linear-gradient(135deg, rgba(15,23,42,0.98) 0%, rgba(217,119,6,0.15) 100%); padding:1.1rem;" onclick="window.loginCompanyProfile('colas_sete')">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong style="color:#fef08a; font-size:1.05rem;">🏢 Colas Agence de Sète & Bassin de Thau</strong>
                            <span class="badge-warning" style="padding:3px 8px; border-radius:4px; font-size:0.75rem; font-weight:900;">SIMULATION RÉEL / RÉTRO-INGÉNIERIE</span>
                        </div>
                        <div style="font-size:0.85rem; color:#f1f5f9; margin:0.45rem 0;">Major TP • CA annuel 18.5 M€ • Caisse active 1 450 000 € • Centrale d'enrobage Frontignan</div>
                        <div style="font-size:0.8rem; color:#cbd5e1;">68 Salariés • 14 Engins lourds • 3 Marchés publics majeurs • Rétro-ingénierie des flux inertes</div>
                        <button class="btn btn-primary" style="margin-top:0.65rem; width:100%; background:linear-gradient(135deg, #d97706, #b45309);">⚡ Activer la Simulation Colas Sète</button>
                    </div>"""

if old_occitanie_card in modals_code:
    modals_code = modals_code.replace(old_occitanie_card, new_colas_card)

# Append Market Explorer Modal and Create Project Modal before final closure
new_extra_modals = r"""
    <!-- ========================================== -->
    <!-- MODAL 15: EXPLORATEUR DE MARCHÉS PUBLICS   -->
    <!-- ========================================== -->
    <div class="modal-backdrop" id="modal-market-explorer">
        <div class="modal-box" style="max-width:980px; max-height:90vh; display:flex; flex-direction:column;">
            <div class="card-header">
                <div>
                    <div class="card-title" style="color:#38bdf8;">🏛️ Place de Marché des Appels d'Offres Publics Ouverts (Sète & Thau)</div>
                    <div style="font-size:0.82rem; color:#cbd5e1;">DCE, CCTP, BPU et simulation directe de soumission pour attribution</div>
                </div>
                <button class="btn btn-secondary" onclick="window.closeModal('modal-market-explorer')">✕</button>
            </div>
            <div style="overflow-y:auto; flex:1; padding-right:0.5rem;" id="market-tenders-list">
                <!-- Injected dynamically via renderMarketTendersList() -->
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL 16: CRÉATION DE CHANTIER MANUEL      -->
    <!-- ========================================== -->
    <div class="modal-backdrop" id="modal-create-project">
        <div class="modal-box" style="max-width:750px;">
            <div class="card-header">
                <div class="card-title" style="color:#4ade80;">➕ Créer un Nouveau Chantier / Affaire</div>
                <button class="btn btn-secondary" onclick="window.closeModal('modal-create-project')">✕</button>
            </div>
            <form id="create-project-form" onsubmit="window.handleCreateProject(event)">
                <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:0.85rem;">
                    <div class="input-group">
                        <label class="input-label">Nom du Chantier *</label>
                        <input type="text" class="input-field" id="new-proj-name" placeholder="Ex: Réaménagement Quai d'Orient" required>
                    </div>
                    <div class="input-group">
                        <label class="input-label">Maître d'Ouvrage (Client) *</label>
                        <input type="text" class="input-field" id="new-proj-client" placeholder="Ex: Ville de Sète" required>
                    </div>
                    <div class="input-group">
                        <label class="input-label">Montant du Marché (€ HT)</label>
                        <input type="number" class="input-field" id="new-proj-budget" value="350000" min="10000">
                    </div>
                    <div class="input-group">
                        <label class="input-label">Commune / Localisation</label>
                        <input type="text" class="input-field" id="new-proj-city" value="Sète (Hérault 34)">
                    </div>
                    <div class="input-group">
                        <label class="input-label">Date de Démarrage</label>
                        <input type="date" class="input-field" id="new-proj-date">
                    </div>
                    <div class="input-group">
                        <label class="input-label">Délai d'Exécution (Mois)</label>
                        <input type="number" class="input-field" id="new-proj-duration" value="3" min="1">
                    </div>
                </div>
                <div class="input-group" style="margin-top:0.5rem;">
                    <label class="input-label">Description & Lots Techniques</label>
                    <textarea class="input-field" id="new-proj-desc" style="height:70px;" placeholder="Terrassement, pose bordures T2, enrobés BBSG 0/10, assainissement EP Ø300..."></textarea>
                </div>
                <div style="display:flex; justify-content:flex-end; gap:0.75rem; margin-top:1rem;">
                    <button type="button" class="btn btn-secondary" onclick="window.closeModal('modal-create-project')">Annuler</button>
                    <button type="submit" class="btn btn-primary">🚀 Créer et Intégrer au Hub</button>
                </div>
            </form>
        </div>
    </div>
"""

pos_end_modals = modals_code.rfind('"""')
if pos_end_modals != -1:
    modals_code = modals_code[:pos_end_modals] + new_extra_modals + modals_code[pos_end_modals:]

with open("scripts/section_modals.py", "w", encoding="utf-8") as f:
    f.write(modals_code)
print("Updated section_modals.py with Colas Sète and Market Explorer modals!")

# ==============================================================================
# 4. UPDATE scripts/section_js_part1.py (4X HEX GRID, COLAS LOGIC & TENDERS)
# ==============================================================================
with open("scripts/section_js_part1.py", "r", encoding="utf-8") as f:
    js1_code = f.read()

# Enhance presets in loginCompanyProfile
old_presets_def = """        var presets = {
            'occitanie_tp': { name: 'Occitanie TP & VRD', treasury: 485200, headcount: 24, projects: 4, fleet: 6 },
            'artisan_2k': { name: 'Artisan Sud VRD', treasury: 2400, headcount: 1, projects: 1, fleet: 1 },
            'stagiaire_tp': { name: 'Formation Conduite Travaux', treasury: 150000, headcount: 8, projects: 2, fleet: 3 },
            'compte_neuf': { name: 'Nouvelle Entreprise TP', treasury: 50000, headcount: 2, projects: 0, fleet: 1 }
        };"""

new_presets_def = """        var presets = {
            'colas_sete': { name: 'Colas Agence Sète & Bassin de Thau', treasury: 1450000, headcount: 68, projects: 3, fleet: 14, role: 'direction', desc: 'Simulation Réelle Major TP / Rétro-Ingénierie Territoriale' },
            'occitanie_tp': { name: 'Colas Agence Sète & Bassin de Thau', treasury: 1450000, headcount: 68, projects: 3, fleet: 14, role: 'direction' },
            'artisan_2k': { name: 'Artisan Solo Sud VRD', treasury: 2400, headcount: 1, projects: 1, fleet: 1, role: 'compagnon', desc: 'Micro-entreprise TP' },
            'stagiaire_tp': { name: 'Formation Conduite Travaux', treasury: 150000, headcount: 8, projects: 2, fleet: 3, role: 'conduite', desc: "Cas d'école Barbazan & Aurouer" },
            'compte_neuf': { name: 'Compte Neuf (Mode Initiation Pédagogique)', treasury: 50000, headcount: 2, projects: 0, fleet: 1, role: 'direction', desc: 'Démarrage guidé pas-à-pas' }
        };"""

if old_presets_def in js1_code:
    js1_code = js1_code.replace(old_presets_def, new_presets_def)

# Add hex grid and tender handlers to js1_code
extra_handlers = r"""
    // ==========================================
    // 4X HEXAGONAL TERRITORY GRID & MARKET EXPLORER
    // ==========================================
    window.toggleCockpitMapView = function(mode) {
        var osmMap = document.getElementById('cockpit-osm-map');
        var hexCont = document.getElementById('cockpit-hex-container');
        var btnSat = document.getElementById('btn-map-satellite');
        var btnHex = document.getElementById('btn-map-hex');
        var title = document.getElementById('cockpit-map-title');

        if (mode === 'hexgrid') {
            if (osmMap) osmMap.style.display = 'none';
            if (hexCont) hexCont.style.display = 'block';
            if (btnSat) btnSat.classList.remove('active');
            if (btnHex) btnHex.classList.add('active');
            if (title) title.innerHTML = '⬡ Vue Stratégique Hexagonale 4X — Contrôle Territoire Thau / Hérault';
            window.renderCockpitHexGrid();
        } else {
            if (osmMap) osmMap.style.display = 'block';
            if (hexCont) hexCont.style.display = 'none';
            if (btnSat) btnSat.classList.add('active');
            if (btnHex) btnHex.classList.remove('active');
            if (title) title.innerHTML = '🗺️ Cartographie SIG des Chantiers & Flotte (Occitanie)';
            if (window.initCockpitOsmMap) window.initCockpitOsmMap();
        }
    };

    window.territoryHexSectors = [
        { id: 'sete_port', name: 'Sète Ville & Port', x: 260, y: 180, control: 'Colas Sète (54%)', activeProjects: 2, dominantActor: 'Colas Agence Sète', infra: 'Dépôt Quai des Moulins • VRD Portuaire', potential: 'Marché Quai Victor Hugo (450k€)' },
        { id: 'frontignan_plant', name: 'Frontignan / La Peyrade', x: 380, y: 120, control: 'Colas Sète (72%)', activeProjects: 1, dominantActor: 'Centrale Enrobés Colas', infra: 'Poste d\'enrobage discontinu 180 t/h • Stock GNT', potential: 'Réseau AEP Plage (620k€)' },
        { id: 'balaruc_nord', name: 'Balaruc / Bassin Nord', x: 240, y: 80, control: 'Eurovia (40%) / Colas (35%)', activeProjects: 1, dominantActor: 'Coactivité Mixte', infra: 'Réseaux thermaux & Piste cyclable', potential: 'Voie Verte Balaruc (280k€)' },
        { id: 'meze_quarry', name: 'Mèze / Carrières GSM', x: 120, y: 140, control: 'Colas Sète (45%) / Eiffage (30%)', activeProjects: 1, dominantActor: 'Carrières GSM Thau', infra: 'Extraction calcaire 0/31.5 • Dépôt granulats', potential: 'Giratoire RD613 (510k€)' },
        { id: 'marseillan_lagune', name: 'Marseillan / Lagune', x: 100, y: 260, control: 'PME Locales (55%)', activeProjects: 0, dominantActor: 'Artisans du Bassin', infra: 'Zone lagunaire protégée • Stations relevage', potential: 'Aménagement Port Tabarka (190k€)' },
        { id: 'agde_littoral', name: 'Agde / Cap d\'Agde', x: 140, y: 360, control: 'Eurovia Méditerranée (50%)', activeProjects: 2, dominantActor: 'Eurovia Agde', infra: 'Centrale Béton CEMEX • Digues Maritimes', potential: 'Réfection Voirie Littorale (340k€)' },
        { id: 'montpellier_ouest', name: 'Montpellier Ouest / A9', x: 420, y: 40, control: 'Eiffage Route (48%)', activeProjects: 3, dominantActor: 'Eiffage Occitanie', infra: 'Échangeur A9/A750 • Carrière GSM Pignan', potential: 'Élargissement Giratoire RD613 (780k€)' }
    ];

    window.renderCockpitHexGrid = function() {
        var viewport = document.getElementById('hex-grid-viewport');
        if (!viewport) return;

        var sectors = window.territoryHexSectors;
        var svgHtml = '<svg viewBox="0 0 540 420" width="100%" height="100%" style="background:#020617;">' +
            '<defs>' +
            '<linearGradient id="hexGradColas" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#d97706" stop-opacity="0.6"/><stop offset="100%" stop-color="#b45309" stop-opacity="0.9"/></linearGradient>' +
            '<linearGradient id="hexGradEurovia" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0284c7" stop-opacity="0.6"/><stop offset="100%" stop-color="#0369a1" stop-opacity="0.9"/></linearGradient>' +
            '<linearGradient id="hexGradPME" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#10b981" stop-opacity="0.6"/><stop offset="100%" stop-color="#047857" stop-opacity="0.9"/></linearGradient>' +
            '<filter id="hexGlow"><feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#38bdf8" flood-opacity="0.5"/></filter>' +
            '</defs>' +
            '<!-- LOGISTIC FLOW LINES -->' +
            '<line x1="380" y1="120" x2="260" y2="180" stroke="#f59e0b" stroke-width="2.5" stroke-dasharray="4,4" opacity="0.8"/>' +
            '<line x1="120" y1="140" x2="260" y2="180" stroke="#10b981" stroke-width="2" stroke-dasharray="3,3" opacity="0.7"/>' +
            '<line x1="380" y1="120" x2="240" y2="80" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4,4" opacity="0.8"/>';

        function getHexPath(cx, cy, r) {
            var pts = [];
            for (var a = 0; a < 6; a++) {
                var rad = (Math.PI / 180) * (60 * a - 30);
                pts.push((cx + r * Math.cos(rad)).toFixed(1) + ',' + (cy + r * Math.sin(rad)).toFixed(1));
            }
            return 'M ' + pts.join(' L ') + ' Z';
        }

        sectors.forEach(function(s) {
            var fill = (s.control.includes('Colas')) ? 'url(#hexGradColas)' : (s.control.includes('Eurovia') ? 'url(#hexGradEurovia)' : 'url(#hexGradPME)');
            svgHtml += '<g style="cursor:pointer;" onclick="window.selectTerritorySector(\'' + s.id + '\')">' +
                '<path d="' + getHexPath(s.x, s.y, 48) + '" fill="' + fill + '" stroke="#38bdf8" stroke-width="1.5" filter="url(#hexGlow)"/>' +
                '<circle cx="' + s.x + '" cy="' + (s.y - 14) + '" r="10" fill="#020617" stroke="#38bdf8" stroke-width="1"/>' +
                '<text x="' + s.x + '" y="' + (s.y - 10) + '" text-anchor="middle" fill="#fef08a" font-size="10" font-weight="900">⬡</text>' +
                '<text x="' + s.x + '" y="' + (s.y + 4) + '" text-anchor="middle" fill="#ffffff" font-size="10" font-weight="800">' + s.name + '</text>' +
                '<text x="' + s.x + '" y="' + (s.y + 18) + '" text-anchor="middle" fill="#cbd5e1" font-size="8" font-weight="700">' + s.control.split(' ')[0] + ' ' + (s.control.split(' ')[1]||'') + '</text>' +
                '</g>';
        });

        svgHtml += '</svg>';
        viewport.innerHTML = svgHtml;
    };

    window.selectTerritorySector = function(sectorId) {
        var s = window.territoryHexSectors.find(function(x) { return x.id === sectorId; });
        if (!s) return;
        var intel = document.getElementById('hex-sector-intel');
        if (!intel) return;

        intel.style.display = 'block';
        intel.innerHTML = '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem; border-bottom:1px solid rgba(56,189,248,0.3); padding-bottom:0.4rem;">' +
            '<strong style="color:#38bdf8; font-size:1rem;">⬡ Intelligence Territoriale : ' + s.name + '</strong>' +
            '<span class="badge-warning" style="padding:2px 6px; border-radius:4px; font-size:0.75rem;">' + s.control + '</span>' +
            '</div>' +
            '<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:0.6rem; font-size:0.82rem; color:#f1f5f9;">' +
            '<div><strong>🏭 Infrastructures :</strong><div style="color:#cbd5e1;">' + s.infra + '</div></div>' +
            '<div><strong>🏗️ Chantiers en cours :</strong><div style="color:#4ade80;">' + s.activeProjects + ' Actifs (' + s.dominantActor + ')</div></div>' +
            '<div><strong>🎯 Opportunité Marché :</strong><div style="color:#fef08a;">' + s.potential + '</div></div>' +
            '</div>' +
            '<div style="margin-top:0.6rem; display:flex; justify-content:flex-end;">' +
            '<button class="btn btn-primary" style="font-size:0.78rem; padding:0.3rem 0.65rem;" onclick="window.openMarketExplorerModal()">🏛️ Explorer les Appels d\'Offres de ce Secteur</button>' +
            '</div>';
    };

    window.openMarketExplorerModal = function() {
        window.openModal('modal-market-explorer');
        window.renderMarketTendersList();
    };

    window.openCreateProjectModal = function() {
        window.openModal('modal-create-project');
    };

    window.publicTendersDataset = [
        {
            id: 'marche_victor_hugo',
            title: 'Réhabilitation Voirie & Eaux Pluviales Avenue Victor Hugo',
            client: 'Ville de Sète (Direction Voirie)',
            budget: 450000,
            duration: '4 Mois',
            location: 'Sète Centre (Quai / Avenue)',
            deadline: '18/11/2026',
            lots: 'Lot 1 : Démolition, Rabotage 5cm, Bordures T2 granit, Enrobé BBSG 0/10 (1 200 t), Canalisations EP Ø400 béton.',
            dce: 'DCE-SETE-VH-2026.pdf (CCTP, BPU, DQE estimatif 450k€)'
        },
        {
            id: 'marche_voie_verte',
            title: 'Création Voie Verte & Piste Cyclable Intercommunale',
            client: 'Sète Agglopôle Méditerranée',
            budget: 280000,
            duration: '2.5 Mois',
            location: 'Balaruc-les-Bains / Thau Nord',
            deadline: '24/11/2026',
            lots: 'Lot Unique : Terrassement meuble, GNT 0/20 compactée (1 800 m²), Enrobé clair drainant / sablé, Signalétique OPPBTP.',
            dce: 'DCE-AGGLO-BALARUC-2026.pdf (Plans profils types, CCTP)'
        },
        {
            id: 'marche_aep_plage',
            title: 'Renouvellement Réseau AEP & Assainissement EU',
            client: 'Ville de Frontignan',
            budget: 620000,
            duration: '5 Mois',
            location: 'Frontignan Plage',
            deadline: '02/12/2026',
            lots: 'Lot 1 : Tranchées sous blindage caisson (R.4534), Tuyaux Fonte Ø200, PVC Assainissement Ø300, Réfection chaussée GNT + BBSG.',
            dce: 'DCE-FRONTIGNAN-AEP-2026.pdf (DICT, Fiches réseaux secs/humides)'
        },
        {
            id: 'marche_giratoire_meze',
            title: 'Aménagement Giratoire d\'Entrée de Ville RD613',
            client: 'Conseil Départemental de l\'Hérault (CD34)',
            budget: 510000,
            duration: '3.5 Mois',
            location: 'Mèze (Carrefour RD613)',
            deadline: '10/12/2026',
            lots: 'Lot 1 : Terrassement déblais/remblais (3 500 m³), Îlot central galets maçonnés, Couche de base GB4 + Roulement BBME 0/10.',
            dce: 'DCE-CD34-MEZE-GIRATOIRE.pdf (Profils en long, étude GTR classe B4)'
        }
    ];

    window.renderMarketTendersList = function() {
        var list = document.getElementById('market-tenders-list');
        if (!list) return;

        var tenders = window.publicTendersDataset;
        var html = '';

        tenders.forEach(function(t) {
            html += '<div class="card" style="margin-bottom:0.85rem; border:1px solid rgba(56,189,248,0.3); background:rgba(15,23,42,0.95); padding:1rem;">' +
                '<div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.5rem;">' +
                '<div>' +
                '<span class="badge-info" style="font-size:0.75rem; padding:2px 6px; border-radius:4px; font-weight:800;">' + t.client + '</span>' +
                '<h4 style="color:#ffffff; font-size:1.05rem; font-weight:900; margin:0.3rem 0;">' + t.title + '</h4>' +
                '<div style="font-size:0.82rem; color:#cbd5e1;">📍 Localisation : ' + t.location + ' • Délai : ' + t.duration + ' • Date Limite Réponse : <strong style="color:#f87171;">' + t.deadline + '</strong></div>' +
                '</div>' +
                '<div style="text-align:right;">' +
                '<span style="font-size:1.15rem; font-weight:900; color:#4ade80; font-family:var(--font-mono);">' + new Intl.NumberFormat('fr-FR').format(t.budget) + ' € HT</span>' +
                '<div style="font-size:0.75rem; color:#94a3b8;">Estimation Maître d\'Ouvrage</div>' +
                '</div>' +
                '</div>' +
                '<div style="background:#020617; border:1px solid var(--border); border-radius:6px; padding:0.6rem; margin:0.6rem 0; font-size:0.82rem; color:#cbd5e1;">' +
                '<strong style="color:#38bdf8;">📋 Consistance des Travaux :</strong> ' + t.lots + '<br>' +
                '<span style="color:#94a3b8; font-size:0.78rem;">📁 Pièces DCE associées : ' + t.dce + '</span>' +
                '</div>' +
                '<div style="display:flex; justify-content:flex-end; gap:0.6rem;">' +
                '<button class="btn btn-secondary" style="font-size:0.8rem; padding:0.35rem 0.75rem;" onclick="window.downloadSimulatedDCE(\'' + t.id + '\')">📄 Télécharger DCE Complet</button>' +
                '<button class="btn btn-primary" style="font-size:0.8rem; padding:0.35rem 0.85rem;" onclick="window.simulateTenderProposal(\'' + t.id + '\')">🎯 Répondre & Générer Offre (Devis Express)</button>' +
                '</div>' +
                '</div>';
        });

        list.innerHTML = html;
    };

    window.downloadSimulatedDCE = function(id) {
        var t = window.publicTendersDataset.find(function(x) { return x.id === id; });
        if (window.showNotification) window.showNotification('Téléchargement du dossier de consultation : ' + (t ? t.title : id), 'info');
    };

    window.simulateTenderProposal = function(id) {
        var t = window.publicTendersDataset.find(function(x) { return x.id === id; });
        if (!t) return;

        window.closeModal('modal-market-explorer');
        window.switchNav('devis_express');
        if (window.showNotification) window.showNotification('DCE "' + t.title + '" importé dans le calculateur Devis Express !', 'success');
    };

    window.handleCreateProject = function(e) {
        if (e && e.preventDefault) e.preventDefault();
        var name = document.getElementById('new-proj-name')?.value || 'Nouveau Chantier';
        var client = document.getElementById('new-proj-client')?.value || 'Ville de Sète';
        var budget = parseFloat(document.getElementById('new-proj-budget')?.value || 350000);

        window.userAccountState.projectsCount = (window.userAccountState.projectsCount || 0) + 1;
        window.updateAllHudAndTickerMetrics();
        window.closeModal('modal-create-project');

        if (window.showNotification) window.showNotification('Chantier "' + name + '" (' + new Intl.NumberFormat('fr-FR').format(budget) + ' €) intégré au Hub avec succès !', 'success');
        window.switchNav('projects_hub');
    };
"""

pos_export_start = js1_code.find('window.switchNav = function')
if pos_export_start != -1:
    js1_code = js1_code[:pos_export_start] + extra_handlers + "\n" + js1_code[pos_export_start:]

with open("scripts/section_js_part1.py", "w", encoding="utf-8") as f:
    f.write(js1_code)
print("Updated section_js_part1.py with 4X Hex Grid and Market Explorer logic!")
