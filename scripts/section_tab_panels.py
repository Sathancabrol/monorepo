# -*- coding: utf-8 -*-

def get_tab_panels():
    return r"""
    <!-- ========================================== -->
    <!-- TAB 1: COCKPIT / DIRECTION OVERVIEW        -->
    <!-- ========================================== -->
    <div id="tab-cockpit" class="tab-panel active">
        <!-- LIVE TICKER ALERT -->
        <div class="hud-ticker">
            <span class="hud-ticker-label">URGENCES CHANTIER</span>
            <div class="hud-ticker-text">
                🚨 Chantier Alès : Visite d'inspection CSPS prévue à 14h30 • DICT ENEDIS validée sur Sète (PK 0+240) • Alerte météo : Rafales Tramontane 65 km/h prévues demain • Livraison 18t BBSG 0/10 confirmée 08h00.
            </div>
        </div>

        <!-- 4 KPI HERO CARDS -->
        <div class="grid-4">
            <div class="card kpi-card">
                <div class="kpi-label">Trésorerie & Caisse Active</div>
                <div class="kpi-val text-cyan" id="kpi-treasury-val">485 200 €</div>
                <div class="kpi-sub" id="kpi-treasury-sub">BFR Couvert : 42 jours d'exploitation</div>
            </div>
            <div class="card kpi-card">
                <div class="kpi-label">Chantiers en Cours</div>
                <div class="kpi-val text-emerald" id="kpi-active-projects-val">4 Actifs</div>
                <div class="kpi-sub" id="kpi-active-projects-sub">Alès, Sète, Pézenas, Montpellier</div>
            </div>
            <div class="card kpi-card">
                <div class="kpi-label">Effectif VRD Engagé</div>
                <div class="kpi-val" style="color:var(--amber);" id="kpi-effectif-val">24 Salariés</div>
                <div class="kpi-sub" id="kpi-effectif-sub">100% CACES & AIPR à jour</div>
            </div>
            <div class="card kpi-card">
                <div class="kpi-label">Conformité Sécurité / DICT</div>
                <div class="kpi-val" style="color:#a855f7;" id="kpi-safety-val">100% Validé</div>
                <div class="kpi-sub" id="kpi-safety-sub">0 Incident • Audit SHA-256 Actif</div>
            </div>
        </div>

        <!-- GIS INTERACTIVE MAP & AUTOPILOT -->
        <div class="grid-split-60-40" style="margin-top: 1rem;">
            <div class="card">
                <div class="card-header" style="flex-wrap: wrap; gap: 0.4rem;">
                    <div>
                        <span class="card-title">🗺️ Cartographie SIG des Chantiers & Flotte (Occitanie)</span>
                        <div style="font-size: 0.75rem; color: #94a3b8;">Déclic anti-collision radial, filtres d'affichage et géolocalisation live</div>
                    </div>
                    <div style="display: flex; gap: 0.3rem; align-items: center; flex-wrap: wrap;">
                        <button class="btn-secondary map-filter-btn active" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="filterCockpitMap('all', this)">Tous</button>
                        <button class="btn-secondary map-filter-btn" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="filterCockpitMap('chantier', this)">Chantiers</button>
                        <button class="btn-secondary map-filter-btn" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="filterCockpitMap('engin', this)">Engins</button>
                        <button class="btn-secondary map-filter-btn" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="filterCockpitMap('depot', this)">Dépôt</button>
                        <button class="btn-secondary map-filter-btn" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="filterCockpitMap('fournisseur', this)">Fournisseurs</button>
                        <button class="btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="resetCockpitMapZoom()">🔍 Reset</button>
                    </div>
                </div>
                <div class="map-container" style="height: 380px; position: relative; overflow: hidden;" id="cockpit-map-container">
                    <canvas id="cockpit-osm-map-canvas" style="width: 100%; height: 100%; cursor: grab;"></canvas>
                </div>

                <!-- SELECTED PIN DETAIL CARD -->
                <div id="cockpit-selected-pin-card" style="margin-top: 0.5rem; background: rgba(15,23,42,0.95); border: 1px solid var(--cyan); border-radius: 6px; padding: 0.6rem 0.8rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                    <div style="display: flex; align-items: center; gap: 0.6rem;">
                        <span id="pin-badge-cat" class="badge badge-info">POINT SIG</span>
                        <div>
                            <strong id="pin-name-val" style="color: #f8fafc; font-size: 0.85rem;">Sélectionnez un point sur la carte SIG</strong>
                            <div id="pin-desc-val" style="font-size: 0.72rem; color: #94a3b8;">Cliquez sur un marqueur pour inspecter ses données en direct</div>
                        </div>
                    </div>
                    <div id="pin-metrics-box" style="display: flex; gap: 0.75rem; font-size: 0.72rem; color: #cbd5e1;"></div>
                    <div>
                        <button class="btn btn-primary" id="btn-pin-open-details" style="font-size: 0.75rem; padding: 0.3rem 0.6rem;" onclick="openSelectedCockpitMapPointModal()">🔍 Inspecter Fiche Complète</button>
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <span class="card-title">⚡ Autopilot & Accès Rapides</span>
                    <button class="btn btn-primary" onclick="runAutopilot()">⚡ Audit IA Global</button>
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                    <div style="font-size: 0.8rem; color: #94a3b8;">Accédez directement aux modules majeurs de pilotage :</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.4rem;">
                        <button class="btn btn-secondary" onclick="switchNav('projects_hub')">📁 Chantiers en cours</button>
                        <button class="btn btn-secondary" onclick="switchNav('depot')">🏭 Dépôt & Entrepôt</button>
                        <button class="btn btn-secondary" onclick="switchNav('planning')">📅 Planning & Agenda</button>
                        <button class="btn btn-secondary" onclick="switchNav('simulator')">🛰️ Watch Tower 3D</button>
                        <button class="btn btn-secondary" onclick="switchNav('fleet')">🚜 Flotte & Engins</button>
                        <button class="btn btn-secondary" onclick="switchNav('catalog')">🛒 Stocks Matériaux</button>
                        <button class="btn btn-secondary" onclick="switchNav('hr')">👷 Organigramme RH</button>
                        <button class="btn btn-secondary" onclick="switchNav('sdp')">💰 28 SDP & DQE TCD</button>
                        <button class="btn btn-secondary" onclick="switchNav('schemas')">📐 Technique & Analyse</button>
                        <button class="btn btn-secondary" onclick="switchNav('procurement')">🛒 Fournisseurs</button>
                        <button class="btn btn-secondary" onclick="switchNav('archives')">🗄️ Archives & GED</button>
                        <button class="btn btn-secondary" onclick="switchNav('docs')">⚖️ Réglementation & Normes</button>
                    </div>

                    <div style="margin-top: 0.5rem; background: rgba(30,41,59,0.5); padding: 0.75rem; border-radius: 6px; border: 1px solid var(--border);">
                        <div style="font-size: 0.75rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.3rem;">📜 Dernier Journal d'Activité Cockpit :</div>
                        <div id="cockpit-activity-log" style="font-family: 'JetBrains Mono'; font-size: 0.72rem; color: #cbd5e1; max-height: 100px; overflow-y: auto;">
                            <!-- Activity lines populated dynamically -->
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- WEATHER & INTEMPÉRIES BANNER CCAG TRAVAUX -->
        <div style="margin-top: 1rem; background: rgba(15,23,42,0.85); border: 1px solid rgba(56,189,248,0.3); border-radius: 8px; padding: 0.75rem 1rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
                <span style="font-size: 1.5rem;">☀️</span>
                <div>
                    <div style="font-size: 0.82rem; font-weight: 800; color: #f8fafc;">Station Météo Chantiers Occitanie (Sète / Alès / Montpellier) : <strong>22°C • Vent Tramontane 25 km/h</strong></div>
                    <div style="font-size: 0.72rem; color: #94a3b8;">Conditions optimales de coulage béton C25/30 et pose d'enrobés BBSG (> 5°C) • Seuil arrêt intempéries CCAG : Non atteint</div>
                </div>
            </div>
            <div style="display: flex; gap: 0.4rem;">
                <span class="badge badge-success">✅ Conditions Chantier : Favorables</span>
                <button class="btn-secondary" style="font-size: 0.72rem; padding: 0.2rem 0.5rem;" onclick="alert('Registre intempéries officiel CCAG Travaux 2021 à jour : 0 jour d\'arrêt intempérie ce mois-ci.');">📋 Registre Intempéries</button>
            </div>
        </div>

        <!-- 4 COMPANY PROFILES DIRECT SWITCHER -->
        <div style="margin-top: 1rem; background: rgba(15,23,42,0.9); border: 1px solid var(--border); border-radius: 8px; padding: 0.75rem 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 0.4rem;">
                <div style="font-size: 0.82rem; font-weight: 800; color: var(--cyan);">🏢 Bascule Instantanée d'Entreprise & États Financiers :</div>
                <span style="font-size: 0.72rem; color: #94a3b8;">Synchronisation temps réel : Caisse, Chantiers, Flotte, Inventaire Dépôt & RH</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.5rem;">
                <button class="btn btn-secondary company-quick-btn active" id="btn-quick-occitanie_tp" onclick="switchCompanyProfile('occitanie_tp')">
                    🏢 <strong>Occitanie TP</strong><br><span style="font-size:0.68rem; color:var(--emerald);">PME 450k€ • 4 Chantiers</span>
                </button>
                <button class="btn btn-secondary company-quick-btn" id="btn-quick-compte_neuf" onclick="switchCompanyProfile('compte_neuf')">
                    ✨ <strong>Compte Vierge</strong><br><span style="font-size:0.68rem; color:#94a3b8;">0€ • Démarrage création</span>
                </button>
                <button class="btn btn-secondary company-quick-btn" id="btn-quick-stagiaire_tp" onclick="switchCompanyProfile('stagiaire_tp')">
                    🎓 <strong>Stagiaire TP</strong><br><span style="font-size:0.68rem; color:#38bdf8;">Cours & DCE Réel Barbazan</span>
                </button>
                <button class="btn btn-secondary company-quick-btn" id="btn-quick-artisan_2k" onclick="switchCompanyProfile('artisan_2k')">
                    🔨 <strong>Artisan BTP</strong><br><span style="font-size:0.68rem; color:var(--amber);">2 000€ • Bureau + EPI</span>
                </button>
            </div>
        </div>

        <!-- MULTI-AGENT AI FEEDS & REAL-TIME CHANTIER ALERTS -->
        <div class="grid-2" style="margin-top: 1rem;">
            <div class="card">
                <div class="card-header">
                    <span class="card-title">🤖 Agents IA Spécialisés & Analyses Métier</span>
                    <button class="btn btn-secondary" style="font-size:0.7rem; padding:0.2rem 0.5rem;" onclick="runAutopilot()">🔄 Relancer Audit</button>
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.76rem;" id="cockpit-ai-agents-list">
                    <!-- Populated dynamically -->
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <span class="card-title">📊 Synthèse Avancement Chantiers & Consommation Budgets</span>
                    <button class="btn btn-secondary" style="font-size:0.7rem; padding:0.2rem 0.5rem;" onclick="switchNav('projects_hub')">Voir Tous</button>
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.5rem;" id="cockpit-projects-summary-list">
                    <!-- Populated dynamically -->
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 2: COMPANY TREASURY & CAISSE           -->
    <!-- ========================================== -->
    <div id="tab-company" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">🏢 Trésorerie, Caisse & Santé Financière de l'Entreprise</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Suivi en temps réel des encaissements, situations de travaux, charges et prévisionnel de trésorerie</div>
                </div>
                <div style="display: flex; gap: 0.4rem;">
                    <button class="btn btn-secondary" onclick="openCompanySwitchModal()">🔄 Changer de Profil Société</button>
                    <button class="btn btn-primary" onclick="simulatePaymentSituation()">💰 Encaisser Situation n°3 (+125k€)</button>
                </div>
            </div>

            <!-- COMPANY PROFILE SUMMARY -->
            <div style="background: rgba(15,23,42,0.9); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <span class="badge badge-info" id="company-profile-badge">PME Établie TP</span>
                    <h2 style="font-size: 1.3rem; font-weight: 900; color: #f8fafc; margin-top: 4px;" id="company-profile-title">Occitanie TP & VRD SAS</h2>
                    <div style="font-size: 0.8rem; color: #94a3b8;" id="company-profile-sub">SIRET : 849 321 654 00018 • Capital : 500 000 € • Siège : Sète / Montpellier (34)</div>
                </div>
                <div style="display: flex; gap: 1.5rem;">
                    <div>
                        <div style="font-size: 0.75rem; color: #94a3b8;">SOLDE CAISSE DISPONIBLE</div>
                        <div style="font-size: 1.6rem; font-weight: 900; color: var(--emerald);" id="company-caisse-val">485 200 €</div>
                    </div>
                    <div>
                        <div style="font-size: 0.75rem; color: #94a3b8;">CHIFFRE D'AFFAIRES 2026</div>
                        <div style="font-size: 1.6rem; font-weight: 900; color: #38bdf8;" id="company-ca-val">1 850 000 €</div>
                    </div>
                </div>
            </div>

            <!-- TRANSACTIONS & CASHFLOW TABLE -->
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; font-size: 0.82rem;">
                    <thead>
                        <tr style="background: rgba(30,41,59,0.8); color: #94a3b8; text-align: left;">
                            <th onclick="sortCashflowTable('date')" style="padding: 0.6rem; cursor: pointer;">DATE ⬍</th>
                            <th onclick="sortCashflowTable('type')" style="padding: 0.6rem; cursor: pointer;">TYPE ⬍</th>
                            <th onclick="sortCashflowTable('label')" style="padding: 0.6rem; cursor: pointer;">LIBELLÉ / CHANTIER ⬍</th>
                            <th onclick="sortCashflowTable('amount')" style="padding: 0.6rem; text-align: right; cursor: pointer;">MONTANT HT ⬍</th>
                            <th onclick="sortCashflowTable('status')" style="padding: 0.6rem; text-align: center; cursor: pointer;">STATUT ⬍</th>
                        </tr>
                    </thead>
                    <tbody id="company-cashflow-tbody">
                        <!-- Populated dynamically -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 3: DEPOT & ENTREPOT (2D/3D & INVENTORY)-->
    <!-- ========================================== -->
    <div id="tab-depot" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">🏭 Dépôt Central & Entrepôt Travaux Publics (Parc, Bureaux 120m², Atelier & Casiers)</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Visualisation spatiale 2D/3D du site (Terrain 1200m², Bâtiment 120m², Atelier, Casiers GNT/Sable, Racks, Aire de lavage et localisation précise des actifs)</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary depot-view-btn active" id="btn-depot-2d" onclick="setDepotViewMode('2d')">📐 Plan 2D Masse</button>
                        <button class="btn-secondary depot-view-btn" id="btn-depot-3d" onclick="setDepotViewMode('3d')">🛰️ Perspective 3D</button>
                        <button class="btn-secondary depot-view-btn" id="btn-depot-list" onclick="setDepotViewMode('list')">📋 Inventaire Complet</button>
                    </div>
                    <button class="btn btn-primary" onclick="alert('Ajout d\'un nouvel équipement ou stock au dépôt.')">➕ Enregistrer Entrée Matériel</button>
                </div>
            </div>

            <!-- DEPOT STATS BANNER -->
            <div class="grid-4" style="margin-bottom: 1rem;">
                <div class="card kpi-card" style="padding: 0.75rem;">
                    <div class="kpi-label">Superficie Terrain</div>
                    <div class="kpi-val text-cyan">1 200 m²</div>
                    <div class="kpi-sub">Voirie lourde & giration PL</div>
                </div>
                <div class="card kpi-card" style="padding: 0.75rem;">
                    <div class="kpi-label">Bâtiments & Bureaux</div>
                    <div class="kpi-val text-emerald">120 m²</div>
                    <div class="kpi-sub">Accueil, Bureau CT, Vestiaires</div>
                </div>
                <div class="card kpi-card" style="padding: 0.75rem;">
                    <div class="kpi-label">Atelier & Garage Outillage</div>
                    <div class="kpi-val" style="color: var(--amber);">80 m²</div>
                    <div class="kpi-sub">Fosse vidange & Armoire sécurisée</div>
                </div>
                <div class="card kpi-card" style="padding: 0.75rem;">
                    <div class="kpi-label">Matériaux en Stock</div>
                    <div class="kpi-val" style="color: #c084fc;">140 Tonnes</div>
                    <div class="kpi-sub">GNT, Sables, Bétons, Enrobé froid</div>
                </div>
            </div>

            <!-- 2D / 3D INTERACTIVE VIEWPORT -->
            <div id="depot-viewport-container" style="background: #070a14; border: 1px solid rgba(56,189,248,0.4); border-radius: 8px; padding: 0.75rem; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 0.4rem;">
                    <div style="display: flex; gap: 0.3rem; align-items: center; flex-wrap: wrap;">
                        <span style="font-size: 0.75rem; font-weight: 800; color: #38bdf8;">Zone active :</span>
                        <button class="btn-secondary depot-zone-filter active" onclick="selectDepotZone('all', this)">Toutes les Zones</button>
                        <button class="btn-secondary depot-zone-filter" onclick="selectDepotZone('bureaux', this)">🏢 Bureaux (120m²)</button>
                        <button class="btn-secondary depot-zone-filter" onclick="selectDepotZone('atelier', this)">🔧 Atelier & Garage</button>
                        <button class="btn-secondary depot-zone-filter" onclick="selectDepotZone('casiers', this)">🧱 Casiers Matériaux</button>
                        <button class="btn-secondary depot-zone-filter" onclick="selectDepotZone('racks', this)">🪵 Racks Tuyaux</button>
                        <button class="btn-secondary depot-zone-filter" onclick="selectDepotZone('lavage', this)">🚿 Aire Lavage / Décanteur</button>
                        <button class="btn-secondary depot-zone-filter" onclick="selectDepotZone('parking', this)">🚜 Parc Engins</button>
                    </div>
                    <span id="depot-view-hud" style="font-family: 'JetBrains Mono'; font-size: 0.75rem; color: var(--emerald);">VUE PLAN 2D ACTIVE</span>
                </div>

                <div style="height: 340px; position: relative; overflow: hidden; border-radius: 6px; border: 1px solid rgba(51,65,85,0.7);">
                    <canvas id="depot-viewport-canvas" style="width: 100%; height: 100%; cursor: crosshair;"></canvas>
                </div>
            </div>

            <!-- SPATIALIZED INVENTORY LIST TABLE -->
            <div style="background: rgba(15,23,42,0.85); border: 1px solid var(--border); border-radius: 8px; padding: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
                    <h4 style="font-size: 1rem; font-weight: 800; color: #38bdf8;">📋 Inventaire Complet Spatialisé des Actifs du Dépôt</h4>
                    <input type="text" id="depot-inventory-search" placeholder="🔍 Filtrer l'inventaire..." class="input-field" style="width: 220px; font-size: 0.75rem;" oninput="filterDepotInventory(this.value)">
                </div>

                <div style="overflow-x: auto;">
                    <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; min-width: 850px;">
                        <thead>
                            <tr style="background: rgba(30,41,59,0.8); color: #94a3b8; text-align: left;">
                                <th onclick="sortDepotInventory('id')" style="padding: 0.55rem; cursor: pointer;">CODE ⬍</th>
                                <th onclick="sortDepotInventory('name')" style="padding: 0.55rem; cursor: pointer;">DÉSIGNATION ÉQUIPEMENT / MATÉRIAU ⬍</th>
                                <th onclick="sortDepotInventory('cat')" style="padding: 0.55rem; cursor: pointer;">CATÉGORIE ⬍</th>
                                <th onclick="sortDepotInventory('loc')" style="padding: 0.55rem; cursor: pointer;">LOCALISATION PRÉCISE AU DÉPÔT ⬍</th>
                                <th onclick="sortDepotInventory('status')" style="padding: 0.55rem; text-align: center; cursor: pointer;">DISPONIBILITÉ / STATUT ⬍</th>
                                <th onclick="sortDepotInventory('val')" style="padding: 0.55rem; text-align: right; cursor: pointer;">VALEUR (€) ⬍</th>
                                <th onclick="sortDepotInventory('vgp')" style="padding: 0.55rem; text-align: center; cursor: pointer;">CONTRÔLE VGP ⬍</th>
                                <th style="padding: 0.55rem; text-align: center;">ACTION</th>
                            </tr>
                        </thead>
                        <tbody id="depot-inventory-tbody">
                            <!-- Populated dynamically by renderDepotInventory() -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 4: PROJECTS HUB & CHANTIERS            -->
    <!-- ========================================== -->
    <div id="tab-projects_hub" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">📁 Hub des Chantiers & Marchés Publics en Cours (Occitanie)</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">4 chantiers opérationnels en cours (Alès, Sète, Pézenas, Montpellier) + 2 DCE d'apprentissage (Barbazan, Aurouer)</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <button class="btn-secondary project-filter-btn active" onclick="filterProjectsHub('all', this)">Tous les Chantiers (6)</button>
                    <button class="btn-secondary project-filter-btn" onclick="filterProjectsHub('internal', this)">🏢 Nos Chantiers Entreprise</button>
                    <button class="btn-secondary project-filter-btn" onclick="filterProjectsHub('dce_ref', this)">📚 Chantiers DCE Référence</button>
                    <button class="btn btn-primary" onclick="alert('Formulaire de création de nouveau marché public ouvert.');">➕ Nouveau Chantier</button>
                </div>
            </div>

            <div id="projects-grid" class="grid-2">
                <!-- Populated dynamically by renderProjectsHub() -->
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 5: PLANNING & GANTT / AGENDA           -->
    <!-- ========================================== -->
    <div id="tab-planning" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">📅 Planning Directeur, Gantt 4D & Agenda Hebdomadaire</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Planification des équipes, phasage des travaux par lot et jalons de réception</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <button class="btn-secondary planning-mode-btn active" id="btn-plan-agenda_week" onclick="setPlanningViewMode('agenda_week')">📅 Vue Hebdomadaire</button>
                    <button class="btn-secondary planning-mode-btn" id="btn-plan-agenda_month" onclick="setPlanningViewMode('agenda_month')">🗓️ Vue Mensuelle</button>
                    <button class="btn-secondary planning-mode-btn" id="btn-plan-gantt" onclick="setPlanningViewMode('gantt')">📊 Chronogramme Gantt</button>
                </div>
            </div>

            <!-- AGENDA VIEW CONTAINER -->
            <div id="planning-agenda-view">
                <!-- Populated dynamically by renderPlanningAgenda() -->
            </div>

            <!-- GANTT VIEW CONTAINER -->
            <div id="planning-gantt-view" style="display: none;">
                <!-- Populated dynamically by renderPlanningGantt() -->
            </div>
        </div>
    </div>

    <!-- ========================================== -->
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
            <div id="watchtower-main-viewport-container" style="position: relative; width: 100%; height: 520px; background: #070a14; border: 1px solid rgba(56,189,248,0.4); border-radius: 8px; overflow: hidden;">
                
                <!-- 1. REAL INTERACTIVE LEAFLET / OSM / SATELLITE MAP CONTAINER -->
                <div id="watchtower-real-map-div" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 10; display: block;"></div>

                <!-- 2. FULLSCREEN FALLBACK / CANVAS LAYER -->
                <canvas id="watchtower-maps-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; cursor: grab; display: none; z-index: 5;"></canvas>

                <!-- 3. SPLIT / 3D CANVAS -->
                <canvas id="watchtower-3d-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; cursor: grab; display: none; z-index: 12;"></canvas>

                <!-- 4. RADAR CANVAS -->
                <canvas id="watchtower-radar-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: none; z-index: 12;"></canvas>

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
    </div>

    <!-- ========================================== -->
    <!-- TAB 7: FLEET & HEAVY MACHINERY             -->
    <!-- ========================================== -->
    <div id="tab-fleet" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
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
            </div>

            <div id="fleet-grid" class="grid-3">
                <!-- Populated dynamically by renderFleetGrid() -->
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 8: CATALOG & MATERIAL STOCKS           -->
    <!-- ========================================== -->
    <div id="tab-catalog" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">🛒 Catalogue VRD, Stocks Matériaux & Outillage (Triable & Filtrable)</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Tuyaux fonte, bordures T2, enrobés, lasers de guidage et suivi des niveaux de stocks au dépôt</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary catalog-view-btn active" id="btn-cat-grid" onclick="setCatalogPresentationMode('grid')">🎛️ Cartes Grille</button>
                        <button class="btn-secondary catalog-view-btn" id="btn-cat-table" onclick="setCatalogPresentationMode('table')">📋 Tableau Triable</button>
                    </div>

                    <select id="catalog-sort-select" class="input-field" style="width: auto; padding: 0.3rem 0.6rem; font-size: 0.75rem;" onchange="sortCatalog(this.value)">
                        <option value="name_asc">Nom (A ➔ Z)</option>
                        <option value="name_desc">Nom (Z ➔ A)</option>
                        <option value="price_asc">Prix HT : Moins cher ➔ Plus cher</option>
                        <option value="price_desc">Prix HT : Plus cher ➔ Moins cher</option>
                        <option value="stock_desc">Stock : Plus grand ➔ Plus petit</option>
                        <option value="stock_asc">Stock : Plus petit ➔ Plus grand</option>
                        <option value="category">Catégorie / Famille</option>
                        <option value="supplier">Fournisseur</option>
                    </select>
                </div>
            </div>

            <!-- FILTER BUTTONS -->
            <div style="display: flex; gap: 0.4rem; margin-bottom: 1rem; flex-wrap: wrap;">
                <button class="btn-secondary active catalog-filter" onclick="filterCatalog('all', this)">Tous les Articles (20)</button>
                <button class="btn-secondary catalog-filter" onclick="filterCatalog('canalisation', this)">💧 Tuyaux & Canalisations</button>
                <button class="btn-secondary catalog-filter" onclick="filterCatalog('voirie', this)">🛣️ Bordures & Voirie</button>
                <button class="btn-secondary catalog-filter" onclick="filterCatalog('granulat', this)">🧱 Granulats & Sables</button>
                <button class="btn-secondary catalog-filter" onclick="filterCatalog('tools', this)">🛠️ Outillage & Lasers</button>
                <button class="btn-secondary catalog-filter" onclick="filterCatalog('safety', this)">🦺 Sécurité & EPI</button>
            </div>

            <!-- 1. GRID VIEW -->
            <div id="catalog-grid" class="grid-3">
                <!-- Populated dynamically by renderCatalogGrid() -->
            </div>

            <!-- 2. TABLE VIEW WITH SORTABLE COLUMN HEADERS -->
            <div id="catalog-table-view" style="display: none; overflow-x: auto; background: rgba(15,23,42,0.85); border: 1px solid var(--border); border-radius: 8px; padding: 0.5rem;">
                <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; min-width: 850px;">
                    <thead>
                        <tr style="background: rgba(30,41,59,0.8); color: #94a3b8; text-align: left;">
                            <th onclick="sortCatalog('name')" style="padding: 0.6rem; cursor: pointer;">DÉSIGNATION MATÉRIAU / OUTIL ⬍</th>
                            <th onclick="sortCatalog('category')" style="padding: 0.6rem; cursor: pointer;">CATÉGORIE ⬍</th>
                            <th onclick="sortCatalog('supplier')" style="padding: 0.6rem; cursor: pointer;">FOURNISSEUR ⬍</th>
                            <th onclick="sortCatalog('norm')" style="padding: 0.6rem; cursor: pointer;">NORME NF ⬍</th>
                            <th onclick="sortCatalog('price_ht')" style="padding: 0.6rem; text-align: right; cursor: pointer;">PRIX UNITAIRE HT ⬍</th>
                            <th onclick="sortCatalog('stock')" style="padding: 0.6rem; text-align: right; cursor: pointer;">STOCK DISPO ⬍</th>
                            <th style="padding: 0.6rem; text-align: center;">ACTION</th>
                        </tr>
                    </thead>
                    <tbody id="catalog-table-body">
                        <!-- Populated dynamically by renderCatalogTable() -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 9: HR ORGANIGRAM & TEAMS               -->
    <!-- ========================================== -->
    <div id="tab-hr" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">👷 Organigramme RH, Équipes de Chantier & Habilitations AIPR/CACES</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Hiérarchie Direction, Conducteurs de Travaux, Chefs d'Équipe et Compagnons qualifiés</div>
                </div>
                <button class="btn btn-secondary" onclick="toggleHrPartnersView()">🏛️ Partenaires MOA/MOE/CSPS</button>
            </div>

            <div id="hr-partners-container" style="background: rgba(15,23,42,0.9); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                <h4 style="font-size: 0.95rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.5rem;">🏛️ Intervenants Majeurs du Marché (MOA / MOE / CSPS / Contrôle)</h4>
                <div id="hr-partners-grid" class="grid-4"></div>
            </div>

            <div id="hr-tree-container" style="overflow-x: auto; padding: 1rem 0;">
                <!-- Populated dynamically by initHrTree() -->
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 10: OPBTP REALISTIC SIGNAGE SIMULATOR  -->
    <!-- ========================================== -->
    <div id="tab-opbtp" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">🦺 Signalisation Temporaire & Balisage Visuel OPBTP (Simulateur Réaliste IISR)</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Giratoire, Entrée de route, Croisement, Intra-urbain PMR, Petit pont, Implantation poteau électrique — Vitesse réglable et détection d'obstacles</div>
                </div>
                <div style="display: flex; gap: 0.4rem; align-items: center; flex-wrap: wrap;">
                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary opbtp-speed-btn" id="btn-spd-025" onclick="setOpbtpSpeedFactor(0.25)">x0.25 Ralenti</button>
                        <button class="btn-secondary opbtp-speed-btn active" id="btn-spd-05" onclick="setOpbtpSpeedFactor(0.5)">x0.5 Réel</button>
                        <button class="btn-secondary opbtp-speed-btn" id="btn-spd-10" onclick="setOpbtpSpeedFactor(1.0)">x1.0 Normal</button>
                    </div>

                    <button class="btn btn-secondary" id="btn-opbtp-sim-play" onclick="toggleOpbtpTrafficSimulation()">⏸️ Pause Trafic</button>
                    <button class="btn btn-secondary" onclick="stepOpbtpTrafficSimulation()">⏭️ Pas à Pas</button>
                    <button class="btn btn-primary" onclick="calculateSignage()">🔄 Recalculer Plan</button>
                </div>
            </div>

            <div class="grid-split-40-60">
                <!-- PARAMETERS & SELECTORS -->
                <div>
                    <div class="input-group">
                        <label class="input-label">1. Catégorie Majeure de Chantier & Géométrie</label>
                        <select id="opbtp-cat-select" class="input-field" onchange="updateOpbtpSubdomainOptions()">
                            <option value="urbain">1. 🏙️ Voirie Urbaine & Agglomération (6 cas)</option>
                            <option value="interurbain">2. 🛣️ Route Interurbaine Bidirectionnelle RD/RN (4 cas)</option>
                            <option value="ouvrages_speciaux">3. 🌉 Giratoires, Ponts & Carrefours Spécifiques (6 cas)</option>
                            <option value="voie_rapide">4. 🏎️ Voie Rapide & Autoroute 2x2 Voies (3 cas)</option>
                            <option value="urgence_nuit">5. 🌙 Travaux Mobiles & Urgence Nocturne (2 cas)</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label class="input-label">2. Configuration Précise du Chantier (Sous-Domaine IISR)</label>
                        <select id="opbtp-task-type" class="input-field" onchange="calculateSignage()">
                            <!-- Populated dynamically by updateOpbtpSubdomainOptions() -->
                        </select>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                        <div class="input-group">
                            <label class="input-label">Vitesse Réglementaire (km/h)</label>
                            <input type="range" id="opbtp-speed-range" min="30" max="110" step="10" value="50" class="input-field" oninput="document.getElementById('opbtp-speed-val').textContent = this.value + ' km/h'; calculateSignage();">
                            <span id="opbtp-speed-val" style="font-size: 0.75rem; color: #38bdf8; font-weight: 700;">50 km/h</span>
                        </div>

                        <div class="input-group">
                            <label class="input-label">Longueur Chantier (m)</label>
                            <input type="range" id="opbtp-length-range" min="20" max="500" step="10" value="120" class="input-field" oninput="document.getElementById('opbtp-len-val').textContent = this.value + ' m'; calculateSignage();">
                            <span id="opbtp-len-val" style="font-size: 0.75rem; color: var(--emerald); font-weight: 700;">120 m</span>
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                        <div class="input-group">
                            <label class="input-label">Densité du Trafic</label>
                            <select id="opbtp-density-select" class="input-field" onchange="setOpbtpTrafficDensity(this.value)">
                                <option value="2">Faible (2 Véhicules fluides)</option>
                                <option value="4" selected>Moyenne (4 Véhicules alternés)</option>
                                <option value="7">Dense (7 Véhicules avec file d'attente)</option>
                            </select>
                        </div>

                        <div class="input-group">
                            <label class="input-label">Cycle Feux KR11 (s)</label>
                            <input type="range" id="opbtp-cycle-range" min="15" max="60" step="5" value="30" class="input-field" oninput="document.getElementById('opbtp-cycle-val').textContent = this.value + ' s'; calculateSignage();">
                            <span id="opbtp-cycle-val" style="font-size: 0.75rem; color: #c084fc; font-weight: 700;">30 s</span>
                        </div>
                    </div>

                    <!-- INJECT VEHICLE BUTTONS -->
                    <div style="margin-top: 0.5rem; background: rgba(30,41,59,0.5); padding: 0.5rem; border-radius: 6px;">
                        <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 700; margin-bottom: 0.3rem;">🚗 Injection Manuelle de Véhicules :</div>
                        <div style="display: flex; gap: 0.3rem; flex-wrap: wrap;">
                            <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="injectOpbtpVehicle('VL')">+ 🚗 Citadine</button>
                            <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="injectOpbtpVehicle('PL')">+ 🚛 Camion 8x4</button>
                            <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="injectOpbtpVehicle('BUS')">+ 🚌 Bus</button>
                            <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="injectOpbtpVehicle('MOTO')">+ 🏍️ Moto</button>
                        </div>
                    </div>
                </div>

                <!-- JUSTIFICATIONS & RESULTS -->
                <div id="opbtp-results"></div>
            </div>

            <!-- VISUAL ROAD SIGNAGE DIAGRAM -->
            <div style="margin-top: 1.5rem; background: #090d16; border: 1px solid rgba(51,65,85,0.7); border-radius: 8px; padding: 1rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem; flex-wrap:wrap; gap:0.5rem;">
                    <div>
                        <h4 style="font-size:1rem; font-weight:800; color:#38bdf8;" id="opbtp-diagram-title">📐 Schéma Visuel d'Implantation des Panneaux & Simulation Trafic Réaliste</h4>
                        <div style="font-size:0.75rem; color:#94a3b8;" id="opbtp-diagram-subtitle">Échelle 1px = 0.5m • Vitesses réelles cinématiques • Véhicules avec distances de freinage sécurisées</div>
                    </div>
                    <div style="display:flex; gap:0.3rem;">
                        <button class="btn btn-secondary" style="padding:0.25rem 0.5rem; font-size:0.75rem;" onclick="switchTrafficLightState()">🚦 Inverser Feux KR11</button>
                    </div>
                </div>
                <div style="height: 280px; position:relative; overflow:hidden;" id="opbtp-canvas-wrapper">
                    <canvas id="opbtp-signage-canvas" style="width: 100%; height: 100%;"></canvas>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 11: SAFETY AIPR & MANIPULABLE EXCAVATOR-->
    <!-- ========================================== -->
    <div id="tab-safety" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">🛡️ Sécurité AIPR, DICT & Simulateur Manipulable avec Éléments Extérieurs</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Recommandations + matériels par étape, contrôle de l'engin, 7 réseaux normalisés et ajout/déplacement de passants, grilles K2 et vigies</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <button class="btn btn-secondary" id="btn-aipr-blindage-toggle" onclick="toggleAiprBlindage()">🛡️ Blindage R4534 : ACTIF</button>
                    <button class="btn btn-danger" onclick="openSafetyEmergencySimulator()">🚨 Simuler Rupture & Urgence</button>
                </div>
            </div>

            <!-- TASK / CONSTRUCTION STAGE SELECTOR -->
            <div style="background: rgba(15,23,42,0.9); border: 1px solid var(--cyan); border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 1rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 1.1rem;">🏗️</span>
                    <strong style="font-size: 0.82rem; color: #38bdf8;">Étape / Tâche du Chantier :</strong>
                </div>
                <select id="aipr-task-phase-select" class="input-field" style="max-width: 480px; font-weight: 700; color: #f8fafc;" onchange="setAiprTaskPhase(this.value)">
                    <option value="phase_1_terrassement">1. 🚜 Décapage terre végétale & Piquetage DICT Classe A</option>
                    <option value="phase_2_fouille_blindage">2. 🕳️ Ouverture tranchée profonde & Pose caissons blindage R4534</option>
                    <option value="phase_3_pose_canalisations" selected>3. 💧 Lit de pose sable & Pose canalisation Fonte DN400 / BA Ø400</option>
                    <option value="phase_4_reseaux_secs">4. ⚡ Pose fourreaux réseaux secs (Élec HTA, Fibre, Gaz) & Grillages</option>
                    <option value="phase_5_remblai_compactage">5. 🧱 Remblaiement méthodique par couches compactées (GTR 0/31.5)</option>
                    <option value="phase_6_voirie_enrobes">6. 🛣️ Pose bordures T2 & Couche d'enrobés BBSG 0/10</option>
                    <option value="phase_7_sondage_aspiration">7. 🔍 Sondage doux par aspiration / Piquetage DICT Classe A</option>
                </select>
                <div style="display: flex; gap: 0.3rem;">
                    <button class="btn-secondary aipr-sim-btn active" onclick="setAiprSituation('gaz')">⚡ Gaz MPB</button>
                    <button class="btn-secondary aipr-sim-btn" onclick="setAiprSituation('hta')">🔴 HTA 20kV</button>
                    <button class="btn-secondary aipr-sim-btn" onclick="setAiprSituation('fibre_aep')">💧 Eau/Fibre</button>
                    <button class="btn-secondary aipr-sim-btn" onclick="setAiprSituation('blindage')">🧱 Blindage 3.2m</button>
                    <button class="btn-secondary aipr-sim-btn" onclick="setAiprSituation('all_networks')">🌈 7 Réseaux</button>
                </div>
            </div>

            <!-- DYNAMIC RECOMMANDATIONS & MATÉRIELS CARD (ACCORDING TO STAGE) -->
            <div id="aipr-phase-recommendations-box" style="background: rgba(15,23,42,0.85); border: 1.5px solid #38bdf8; border-radius: 8px; padding: 0.85rem; margin-bottom: 1rem;">
                <!-- Populated dynamically by updateAiprPhaseDetails() -->
            </div>

            <!-- MANIPULABLE EXCAVATOR SIMULATION WINDOW -->
            <div style="background: rgba(15,23,42,0.95); border: 2px solid var(--cyan); border-radius: 8px; padding: 1rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem; flex-wrap:wrap; gap:0.5rem;">
                    <div>
                        <h3 style="font-size:1.1rem; font-weight:800; color:#38bdf8;">🔬 Simulateur 2D/3D Interactif : Déplacez l'Engin, Outils & Éléments Extérieurs</h3>
                        <div style="font-size:0.75rem; color:#94a3b8;">Glissez ou ajoutez des passants, barrières K2, vigies et observez les distances de sécurité aux réseaux</div>
                    </div>
                    <div style="display: flex; gap: 0.4rem; align-items: center; flex-wrap: wrap;">
                        <span style="font-size: 0.75rem; color: #94a3b8;">Machine :</span>
                        <select id="aipr-machine-type" class="input-field" style="width: auto; padding: 0.25rem 0.5rem; font-size: 0.75rem;" onchange="updateAiprExcavatorControls()">
                            <option value="liebherr_24t">🚜 Pelle Chenilles 24t (Liebherr R924)</option>
                            <option value="mecalac_12t">🚜 Pelleteuse Urbaine 12t (Mecalac 12MTX)</option>
                            <option value="kubota_5t">🚜 Mini-pelle 5.5t (Kubota KX057)</option>
                            <option value="aspiratrice_tp">🌪️ Aspiratrice-Excavatrice TP (Doux)</option>
                        </select>
                        <span style="font-size: 0.75rem; color: #94a3b8;">Outil :</span>
                        <select id="aipr-tool-type" class="input-field" style="width: auto; padding: 0.25rem 0.5rem; font-size: 0.75rem;" onchange="updateAiprExcavatorControls()">
                            <option value="godet_dents">⛏️ Godet Rétro à Dents</option>
                            <option value="godet_curage">🧹 Godet Curage Orientable</option>
                            <option value="brh">🔨 Brise-Roche Hydraulique (BRH)</option>
                            <option value="aspiration">🌪️ Buse Aspiration Souple</option>
                        </select>
                    </div>
                </div>

                <div class="grid-split-60-40">
                    <div style="height: 360px; background: #000; border: 1px solid rgba(56,189,248,0.4); border-radius: 6px; position: relative; overflow: hidden;">
                        <canvas id="aipr-simulation-canvas" style="width: 100%; height: 100%; cursor: crosshair;"></canvas>
                        <div id="aipr-sim-hud" style="position: absolute; bottom: 8px; left: 8px; background: rgba(15,23,42,0.9); padding: 4px 10px; border-radius: 4px; font-family: 'JetBrains Mono'; font-size: 0.72rem; color: #38bdf8; border: 1px solid rgba(56,189,248,0.3);">
                            SITUATION : FOUILLE À PROXIMITÉ CONDUITE GAZ PEHD 4 BAR
                        </div>
                    </div>

                    <div style="display: flex; flex-direction: column; justify-content: space-between; gap: 0.5rem;">
                        <!-- EXCAVATOR SLIDERS CONTROLS -->
                        <div style="background: rgba(30,41,59,0.5); padding: 0.75rem; border-radius: 6px; border: 1px solid rgba(51,65,85,0.6);">
                            <div style="font-size: 0.78rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.4rem;">🚜 Commandes Complètes de l'Engin & Cinématique</div>
                            
                            <div style="margin-bottom: 0.4rem;">
                                <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #94a3b8;">
                                    <span>Déplacement Horizontal Châssis (X)</span>
                                    <span id="aipr-pos-x-label" style="color:#38bdf8; font-weight:700;">PK 0+240 (x=60px)</span>
                                </div>
                                <input type="range" id="aipr-track-x-range" min="10" max="360" value="60" class="input-field" oninput="updateAiprExcavatorControls()">
                            </div>

                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.4rem; font-size: 0.75rem;">
                                <div>
                                    <label class="input-label">Angle Flèche (Boom)</label>
                                    <input type="range" id="aipr-boom-range" min="10" max="80" value="45" class="input-field" oninput="updateAiprExcavatorControls()">
                                </div>
                                <div>
                                    <label class="input-label">Angle Balancier (Stick)</label>
                                    <input type="range" id="aipr-stick-range" min="20" max="110" value="65" class="input-field" oninput="updateAiprExcavatorControls()">
                                </div>
                            </div>
                        </div>

                        <!-- EXTERIOR ELEMENTS MANAGEMENT (ADD/REMOVE/MOVE) -->
                        <div style="background: rgba(30,41,59,0.5); padding: 0.75rem; border-radius: 6px; border: 1px solid rgba(51,65,85,0.6);">
                            <div style="font-size: 0.78rem; font-weight: 800; color: var(--emerald); margin-bottom: 0.4rem;">🚶‍♂️ Éléments Extérieurs (Passants, Barrières, Vigie)</div>
                            <div style="display: flex; gap: 0.3rem; flex-wrap: wrap;">
                                <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="addAiprExteriorElement('pieton')">🚶‍♂️ + Passant</button>
                                <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="addAiprExteriorElement('barriere')">🚧 + Barrière K2</button>
                                <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="addAiprExteriorElement('vigie')">🦺 + Vigie</button>
                                <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="addAiprExteriorElement('piquet')">🚩 + Piquet Réseau</button>
                                <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.7rem; color: #ef4444;" onclick="removeLastAiprExteriorElement()">🗑️ Retirer</button>
                                <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="resetAiprExteriorElements()">🔄 Réinitialiser</button>
                            </div>
                        </div>

                        <!-- LIVE TELEMETRY -->
                        <div style="background: rgba(15,23,42,0.9); padding: 0.75rem; border-radius: 6px; border: 1px solid var(--border); font-size: 0.75rem;">
                            <div style="display:flex; justify-content:space-between; margin-bottom:2px;">
                                <span style="color:#94a3b8;">Profondeur Outil :</span>
                                <strong id="aipr-depth-val" style="color:#38bdf8;">-1.45 m</strong>
                            </div>
                            <div style="display:flex; justify-content:space-between; margin-bottom:2px;">
                                <span style="color:#94a3b8;">Distance Réseau Gaz :</span>
                                <strong id="aipr-dist-val" style="color:var(--emerald);">0.85 m (Conforme)</strong>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 12: DAILY SITE REPORT (RDC)            -->
    <!-- ========================================== -->
    <div id="tab-rdc" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">📋 Journal Quotidien de Chantier (RDC) & Prises de Vue Multi-Sources</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Pointage des équipes, heures engins, métrés exécutés, météo et photos de suivi</div>
                </div>
                <div style="display: flex; gap: 0.4rem;">
                    <button class="btn btn-primary" onclick="openRdcCameraModal()">📸 Capturer Photo Chantier (Webcam / Drone)</button>
                    <button class="btn btn-secondary" onclick="exportRdcPDF()">📥 Exporter RDC en PDF</button>
                </div>
            </div>

            <!-- RDC FORM & ENTRIES GRID -->
            <div class="grid-split-40-60">
                <div style="background: rgba(15,23,42,0.85); border: 1px solid var(--border); border-radius: 8px; padding: 1rem;">
                    <h4 style="font-size: 0.95rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.75rem;">✍️ Saisie du Rapport du Jour</h4>
                    
                    <div class="input-group">
                        <label class="input-label">Chantier Concerné</label>
                        <select id="rdc-proj-select" class="input-field">
                            <option value="Giratoire RD906 Alès">Giratoire RD906 Alès</option>
                            <option value="ZAC Littoral Sète">ZAC Littoral Sète</option>
                            <option value="Centre Ancien Pézenas">Centre Ancien Pézenas</option>
                            <option value="Voie Verte Montpellier">Voie Verte Montpellier</option>
                        </select>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                        <div class="input-group">
                            <label class="input-label">Date</label>
                            <input type="date" id="rdc-date" class="input-field" value="2026-09-21">
                        </div>
                        <div class="input-group">
                            <label class="input-label">Chef de Chantier</label>
                            <input type="text" id="rdc-chief" class="input-field" value="A. Martin">
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                        <div class="input-group">
                            <label class="input-label">Heures Main d'Œuvre</label>
                            <input type="number" id="rdc-heures-mo" class="input-field" value="35">
                        </div>
                        <div class="input-group">
                            <label class="input-label">Heures Engins (Pelle/Camion)</label>
                            <input type="number" id="rdc-heures-engins" class="input-field" value="14">
                        </div>
                    </div>

                    <div class="input-group">
                        <label class="input-label">Description des Travaux Exécutés</label>
                        <textarea id="rdc-desc" class="input-field" rows="3" placeholder="Terrassement tranchée PK 0+240, pose 28ml tuyaux Fonte DN400, remblaiement GNT...">Terrassement tranchée PK 0+240, pose 28ml tuyaux Fonte DN400, remblaiement GNT...</textarea>
                    </div>

                    <button class="btn btn-primary" style="width: 100%; margin-top: 0.5rem;" onclick="saveRdcEntry()">💾 Enregistrer Rapport RDC</button>
                </div>

                <div id="rdc-entries-list">
                    <!-- Populated dynamically -->
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 13: COMPAGNON MOBILE & FIELD VIEW      -->
    <!-- ========================================== -->
    <div id="tab-compagnon_mobile" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">📱 Mode Terrain Compagnon : Mon Planning & Mes Consignes VRD</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Interface simplifiée pour smartphone/tablette de chantier, pointage et consignes de sécurité</div>
                </div>
            </div>

            <div id="compagnon-mobile-content">
                <!-- Populated dynamically by renderCompagnonPlanning() -->
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 14: OBSIDIAN GRAPH & FOLDER EXPLORER   -->
    <!-- ========================================== -->
    <div id="tab-obsidian" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">📚 Base de Connaissances Obsidian (Génie Civil, VRD & Réglementation)</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Double affichage : Explorateur de Dossiers structuré & Graphe interactif de relations transversales</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary obs-view-btn active" id="btn-obs-folder" onclick="setObsidianViewMode('folder')">📂 Vue Dossiers (Treeview)</button>
                        <button class="btn-secondary obs-view-btn" id="btn-obs-graph" onclick="setObsidianViewMode('graph')">🕸️ Vue Graphe Réseau</button>
                    </div>
                    <input type="text" id="obsidian-search-input" placeholder="🔍 Rechercher..." class="input-field" style="width: 150px; padding: 0.35rem 0.5rem;" oninput="searchObsidianNodes(this.value)">
                    <button class="btn-secondary" onclick="resetObsidianCamera()">🎯 Recentrer Graphe</button>
                </div>
            </div>

            <!-- 1. FOLDER TREEVIEW EXPLORER VIEW -->
            <div id="obsidian-folder-view-container" style="display: grid; grid-template-columns: 320px 1fr; gap: 1rem;">
                <div class="folder-tree-container" id="obsidian-folder-tree-view">
                    <!-- Populated dynamically by renderObsidianFolderTree() -->
                </div>

                <div style="background: rgba(15,23,42,0.9); border: 1px solid var(--border); border-radius: 8px; padding: 1.25rem; max-height: 520px; overflow-y: auto;" id="obsidian-folder-doc-viewer">
                    <!-- Populated dynamically when clicking a file -->
                </div>
            </div>

            <!-- 2. NETWORK GRAPH VIEW -->
            <div id="obsidian-graph-view-container" style="display: none;">
                <div class="obsidian-layout">
                    <div class="obsidian-graph-container" style="height: 520px; position: relative;">
                        <canvas id="obsidian-canvas" style="width: 100%; height: 100%; cursor: grab;"></canvas>
                        <div style="position: absolute; bottom: 12px; left: 12px; display: flex; gap: 4px; z-index: 5;">
                            <button class="btn btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="zoomObsidian(1.2)">🔍 +</button>
                            <button class="btn btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="zoomObsidian(0.8)">🔍 -</button>
                            <button class="btn btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="reorganizeObsidianNodes()">🔄 Réorganiser</button>
                        </div>
                    </div>
                    <div class="obsidian-drawer" style="height: 520px;">
                        <div style="font-size: 0.85rem; font-weight: 800; color: #38bdf8;">📌 Détails de la Fiche Active</div>
                        <div id="obsidian-node-info">
                            <div style="color: #64748b; font-size: 0.8rem; line-height: 1.5;">Cliquez sur un nœud pour afficher son contenu technique complet.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 15: TECHNIQUE & ANALYSE (SIMULATEUR, COUPE COMPACTAGE & EXCEL) -->
    <!-- ========================================== -->
    <div id="tab-schemas" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">📐 Technique & Analyse : Formules, Coupe Technique Remblais & Fiches Excel</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Simulateur de calculs (Cubatures, Enrobés, Manning-Strickler), Visualisation dynamique Coupe de Tranchée/Compactage et Fiches de Tâches Excel</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border); flex-wrap: wrap; gap: 2px;">
                        <button class="btn-secondary tech-view-btn active" id="btn-tech-formulas" onclick="setTechniqueViewMode('formulas')">🧮 Simulateur de Formules</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-enrobes2d" onclick="setTechniqueViewMode('enrobes_2d')">🛣️ Simulation 2D Passes d'Enrobés</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-compactage" onclick="setTechniqueViewMode('compactage')">🔬 Coupe Tranchée & Compacteur</button>
                        <button class="btn-secondary tech-view-btn" id="btn-tech-tasksheet" onclick="setTechniqueViewMode('tasksheet')">📊 Fiche de Tâche Type Excel</button>
                    </div>
                    <button class="btn btn-primary" onclick="exportTechniqueReport()">📥 Exporter Note de Calcul</button>
                </div>
            </div>

            <!-- 1. FORMULAS CALCULATOR VIEW -->
            <div id="tech-formulas-view">
                <div class="grid-split-40-60">
                    <div>
                        <div class="input-group">
                            <label class="input-label">1. Sélectionnez la Famille de Calcul & Formule TP</label>
                            <select id="formula-type-select" class="input-field" style="font-weight:700; color:#38bdf8;" onchange="updateFormulaCalculator()">
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
                            </select>
                        </div>

                        <!-- DYNAMIC PARAMETER INPUTS -->
                        <div id="formula-inputs-container">
                            <!-- Populated dynamically by updateFormulaCalculator() -->
                        </div>
                    </div>

                    <!-- CALCULATION RESULTS & STEP BY STEP WORKED FORMULAS -->
                    <div id="formula-calculation-output">
                        <!-- Populated dynamically by updateFormulaCalculator() -->
                    </div>
                </div>
            </div>

            <!-- 2. CONCRETE CASE : COUPE TECHNIQUE DES COUCHES & COMPACTEUR VIBRANT -->
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

            <div id="tech-compactage-cut-view" style="display: none;">
                <div style="background: rgba(15,23,42,0.9); border: 2px solid var(--cyan); border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
                        <div>
                            <h4 style="font-size: 1.05rem; font-weight: 800; color: #38bdf8;">🔬 Vue en Coupe Technique des Couches de Remblai & Simulation Compacteur Vibrant</h4>
                            <div style="font-size: 0.78rem; color: #94a3b8;">Animation du rouleau compacteur en action, strates GTR (BBSG, GB3, GNT 0/31.5, Lit de pose) et télémétrie de portance EV2</div>
                        </div>
                        <div style="display: flex; gap: 0.3rem;">
                            <button class="btn btn-secondary" id="btn-compactage-anim" onclick="toggleCompactageAnimation()">⏸️ Pause Rouleau</button>
                            <button class="btn btn-primary" onclick="triggerPlaqueTest()">⚡ Essai à la Plaque EV2</button>
                        </div>
                    </div>

                    <div class="grid-split-60-40">
                        <div style="height: 360px; background: #070a14; border: 1px solid rgba(56,189,248,0.4); border-radius: 6px; position: relative; overflow: hidden;">
                            <canvas id="compactage-cut-canvas" style="width: 100%; height: 100%;"></canvas>
                        </div>

                        <div style="display: flex; flex-direction: column; justify-content: space-between; gap: 0.5rem;">
                            <div style="background: rgba(30,41,59,0.5); padding: 0.75rem; border-radius: 6px; border: 1px solid rgba(51,65,85,0.6);">
                                <div style="font-size: 0.8rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.4rem;">🎛️ Paramètres de Réglage Compactage GTR</div>
                                <div style="font-size: 0.72rem; color: #cbd5e1; display: grid; gap: 0.4rem;">
                                    <div>
                                        <div style="display:flex; justify-content:space-between;"><span>Vitesse du Rouleau (km/h) :</span> <strong id="cmp-spd-val" style="color:var(--emerald);">4.0 km/h</strong></div>
                                        <input type="range" id="cmp-spd-range" min="1.5" max="8.0" step="0.5" value="4.0" class="input-field" oninput="updateCompactageParams()">
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between;"><span>Nombre de Passes Recommandées (N) :</span> <strong id="cmp-passes-val" style="color:var(--amber);">6 passes</strong></div>
                                        <input type="range" id="cmp-passes-range" min="2" max="12" step="1" value="6" class="input-field" oninput="updateCompactageParams()">
                                    </div>
                                    <div>
                                        <div style="display:flex; justify-content:space-between;"><span>Épaisseur Couche GNT (cm) :</span> <strong id="cmp-thick-val" style="color:#38bdf8;">20 cm</strong></div>
                                        <input type="range" id="cmp-thick-range" min="10" max="45" step="5" value="20" class="input-field" oninput="updateCompactageParams()">
                                    </div>
                                </div>
                            </div>

                            <div style="background: rgba(15,23,42,0.9); padding: 0.75rem; border-radius: 6px; border: 1px solid var(--border); font-size: 0.75rem;">
                                <div style="font-weight: 800; color: #38bdf8; margin-bottom: 4px;">📊 Télémétrie & Conformité In-Situ :</div>
                                <div style="display: flex; justify-content: space-between; margin-bottom: 2px;">
                                    <span style="color: #94a3b8;">Module de Portance Plaque (EV2) :</span>
                                    <strong id="cmp-ev2-val" style="color: var(--emerald);">95.4 MPa (Norme ≥ 80 MPa)</strong>
                                </div>
                                <div style="display: flex; justify-content: space-between; margin-bottom: 2px;">
                                    <span style="color: #94a3b8;">Rapport de Compactage EV2/EV1 :</span>
                                    <strong id="cmp-k-val" style="color: var(--emerald);">1.68 (Norme ≤ 2.0)</strong>
                                </div>
                                <div style="display: flex; justify-content: space-between;">
                                    <span style="color: #94a3b8;">Cadence d'alimentation requise :</span>
                                    <strong id="cmp-debit-val" style="color: #f8fafc;">185 t/h</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 3. EXCEL-LIKE TASK SHEET VIEW -->
            <div id="tech-tasksheet-view" style="display: none;">
                <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(51,65,85,0.7); border-radius: 8px; padding: 1.25rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.5rem;">
                        <div>
                            <h4 style="font-size: 1.05rem; font-weight: 800; color: var(--emerald);">📊 Fiche de Tâche & Étude de Prix Décomposée (Format Tableur BTP In-Situ)</h4>
                            <div style="font-size: 0.78rem; color: #94a3b8;">Modifiez les rendements, effectifs et consommations pour recalculer en temps réel le déboursé sec unitaire</div>
                        </div>
                        <div style="display: flex; gap: 0.4rem;">
                            <select id="tasksheet-preset-select" class="input-field" style="width: auto; font-size: 0.8rem;" onchange="loadTaskSheetPreset(this.value)">
                                <option value="bordure_t2">Fiche 01 : Pose Bordure T2 avec Semelle Béton (ml)</option>
                                <option value="tranchee_ba400">Fiche 02 : Pose Tuyau Béton Armé Ø400 en Tranchée (ml)</option>
                                <option value="enrobe_bbsg">Fiche 03 : Mise en Œuvre Enrobés Chauds BBSG 0/10 (t)</option>
                                <option value="terrassement_gnt">Fiche 04 : Réglage Couche de Fondation GNT 0/31.5 (m³)</option>
                            </select>
                        </div>
                    </div>

                    <div id="tasksheet-table-container" style="overflow-x: auto;">
                        <!-- Populated dynamically by renderTaskSheet() -->
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 16: SDP & DQE INTERACTIVE TCD TABLE    -->
    <!-- ========================================== -->
    <div id="tab-sdp" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.75rem;">
                <div>
                    <span class="card-title">💰 28 Sous-Détails de Prix (SDP), DQE & Comparateur Multi-Entreprises</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Modifiez les déboursés secs, coefficients K et comparez nos prix à Colas, Eurovia, Eiffage et à la moyenne régionale FNTP</div>
                </div>

                <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary sdp-view-btn active" id="btn-sdp-dqe_tcd" onclick="setSDPViewMode('dqe_tcd')">📊 Tableau TCD Modifiable</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-cards" onclick="setSDPViewMode('cards')">🗂️ 28 Fiches SDP</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-comparator" onclick="setSDPViewMode('comparator')">⚖️ Comparateur Prix Concurrence</button>
                    </div>

                    <button class="btn btn-secondary" onclick="toggleSdpFormulas()">📐 Afficher Formules</button>

                    <select id="dqe-project-select" class="input-field" style="width: auto; padding: 0.35rem 0.6rem;" onchange="renderDQEPivotTable()">
                        <option value="all">Tous les chantiers (28 prix)</option>
                        <option value="projet_ales">Giratoire RD906 Alès</option>
                        <option value="projet_sete">ZAC Littoral Sète</option>
                        <option value="projet_pezenas">Centre Ancien Pézenas</option>
                        <option value="projet_montpellier">Voie Verte Montpellier</option>
                    </select>

                    <button class="btn btn-primary" onclick="exportDQEtoCSV()">📥 Exporter CSV</button>
                    <button class="btn btn-secondary" onclick="printDQESummary()">🖨️ Imprimer</button>
                </div>
            </div>

            <!-- FORMULAS EXPLANATION BOX (TOGGLEABLE) -->
            <div id="sdp-formulas-box" style="background: rgba(15,23,42,0.85); border: 1px solid var(--cyan); border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                <h4 style="font-size: 0.95rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.5rem;">📐 Formules Analytiques du Déboursé Sec (D.S.) & Prix de Vente HT (P.V.)</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 0.75rem; font-size: 0.78rem;">
                    <div style="background: rgba(30,41,59,0.5); padding: 0.6rem; border-radius: 6px;">
                        <strong style="color: var(--emerald);">1. Déboursé Sec Unitaire (D.S.) :</strong>
                        <div style="font-family: 'JetBrains Mono'; color: #f8fafc; margin: 3px 0;">DS = MO + Fournitures + Matériel / Engins</div>
                        <div style="color: #94a3b8;">Coût direct strict hors frais de structure et bénéfice.</div>
                    </div>
                    <div style="background: rgba(30,41,59,0.5); padding: 0.6rem; border-radius: 6px;">
                        <strong style="color: #38bdf8;">2. Prix de Vente Unitaire Hors Taxes (P.V.) :</strong>
                        <div style="font-family: 'JetBrains Mono'; color: #f8fafc; margin: 3px 0;">PV = DS × K (avec K = 1.350 standard)</div>
                        <div style="color: #94a3b8;">Coefficient K = 1 / [1 - (FG + FS + Aléas + Bénéfice Net)].</div>
                    </div>
                    <div style="background: rgba(30,41,59,0.5); padding: 0.6rem; border-radius: 6px;">
                        <strong style="color: var(--amber);">3. Montant Total du Prix :</strong>
                        <div style="font-family: 'JetBrains Mono'; color: #f8fafc; margin: 3px 0;">Total HT = Quantité × PV Unitaire HT</div>
                        <div style="color: #94a3b8;">Somme des prix = Montant global et forfaitaire du marché.</div>
                    </div>
                </div>
            </div>

            <!-- DQE & SDP CONTAINERS -->
            <div id="sdp-dqe-tcd-view"></div>
            <div id="sdp-cards-view" style="display: none;" class="grid-3"></div>

            <!-- MULTI-ENTERPRISE PRICE COMPARATOR VIEW -->
            <div id="sdp-comparator-view" style="display: none;">
                <div style="background: rgba(15,23,42,0.9); border: 1px solid var(--border); border-radius: 8px; padding: 1.25rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.5rem;">
                        <div>
                            <h4 style="font-size: 1.05rem; font-weight: 800; color: #38bdf8;">⚖️ Comparateur de Prix BTP Multi-Entreprises (Pour la même tâche)</h4>
                            <div style="font-size: 0.78rem; color: #94a3b8;">Analyse comparative de notre offre face à Colas, Eurovia, Eiffage et à la moyenne régionale FNTP</div>
                        </div>
                        <select id="sdp-compare-item-select" class="input-field" style="width: auto; font-size: 0.8rem;" onchange="renderEnterprisePriceComparison(this.value)">
                            <option value="DQE_004">Pose Bordures T2 (ml)</option>
                            <option value="DQE_002">Tranchée Blindée > 1.30m (m³)</option>
                            <option value="DQE_003">Pose Tuyau Béton Armé Ø400 (ml)</option>
                            <option value="DQE_005">Enrobés Chauds BBSG 0/10 (t)</option>
                            <option value="DQE_001">Décapage Terre Végétale 30cm (m²)</option>
                        </select>
                    </div>

                    <div id="sdp-comparison-results-container">
                        <!-- Populated dynamically by renderEnterprisePriceComparison() -->
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 17: BENCHMARK & INVENTAIRE             -->
    <!-- ========================================== -->
    <div id="tab-benchmark" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">📊 Benchmark des Prix Régionaux & Rendements d'Équipes TP</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Comparaison des sous-détails avec les DCE réels (Barbazan, Aurouer) et moyennes FNTP Occitanie</div>
                </div>
            </div>

            <!-- BENCHMARK TABLE -->
            <div style="overflow-x: auto; margin-bottom: 1.5rem;">
                <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; min-width: 900px;">
                    <thead>
                        <tr style="background: rgba(30,41,59,0.8); color: #94a3b8; text-align: left;">
                            <th onclick="sortBenchmarkTable('code')" style="padding: 0.6rem; cursor: pointer;">CODE ⬍</th>
                            <th onclick="sortBenchmarkTable('designation')" style="padding: 0.6rem; cursor: pointer;">DÉSIGNATION DES TRAVAUX ⬍</th>
                            <th onclick="sortBenchmarkTable('unit')" style="padding: 0.6rem; text-align: center; cursor: pointer;">UNITÉ ⬍</th>
                            <th onclick="sortBenchmarkTable('cost_internal')" style="padding: 0.6rem; text-align: right; cursor: pointer;">D.S. INTERNE ⬍</th>
                            <th onclick="sortBenchmarkTable('pv_internal')" style="padding: 0.6rem; text-align: right; cursor: pointer;">P.V. INTERNE ⬍</th>
                            <th onclick="sortBenchmarkTable('ref_dce_barbazan')" style="padding: 0.6rem; text-align: right; cursor: pointer;">RÉF DCE BARBAZAN ⬍</th>
                            <th onclick="sortBenchmarkTable('ref_dce_aurouer')" style="padding: 0.6rem; text-align: right; cursor: pointer;">RÉF DCE AUROUER ⬍</th>
                            <th onclick="sortBenchmarkTable('fntp_regional_avg')" style="padding: 0.6rem; text-align: right; cursor: pointer;">MOY. FNTP OCCITANIE ⬍</th>
                            <th onclick="sortBenchmarkTable('variance_pct')" style="padding: 0.6rem; text-align: center; cursor: pointer;">VARIANCE / STATUT ⬍</th>
                        </tr>
                    </thead>
                    <tbody id="benchmark-table-body">
                        <!-- Populated dynamically -->
                    </tbody>
                </table>
            </div>

            <!-- TEAMS BENCHMARK -->
            <h4 style="font-size: 0.95rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.5rem;">👷 Rendements Journaliers des Équipes VRD vs Référentiel FNTP</h4>
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; min-width: 900px;">
                    <thead>
                        <tr style="background: rgba(30,41,59,0.8); color: #94a3b8; text-align: left;">
                            <th onclick="sortTeamsBenchmarkTable('team_name')" style="padding: 0.6rem; cursor: pointer;">ÉQUIPE ⬍</th>
                            <th style="padding: 0.6rem;">COMPOSITION</th>
                            <th onclick="sortTeamsBenchmarkTable('hourly_cost_team')" style="padding: 0.6rem; text-align: right; cursor: pointer;">THMO ÉQUIPE ⬍</th>
                            <th onclick="sortTeamsBenchmarkTable('daily_yield_our')" style="padding: 0.6rem; text-align: right; cursor: pointer;">NOTRE RENDEMENT ⬍</th>
                            <th onclick="sortTeamsBenchmarkTable('fntp_ref_yield')" style="padding: 0.6rem; text-align: right; cursor: pointer;">REF FNTP ⬍</th>
                            <th onclick="sortTeamsBenchmarkTable('diff_yield')" style="padding: 0.6rem; text-align: center; cursor: pointer;">ÉCART % ⬍</th>
                            <th style="padding: 0.6rem;">ENGINS PRINCIPAUX</th>
                        </tr>
                    </thead>
                    <tbody id="teams-benchmark-table-body">
                        <!-- Populated dynamically -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 18: FOURNISSEURS & CARTE LOGISTIQUE    -->
    <!-- ========================================== -->
    <div id="tab-procurement" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">🛒 Fournisseurs Partenaires, Carrières & Carte Logistique</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Localisation des carrières, centrales à béton et négoces avec distances réelles, remises négociées et vue cartographique</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary map-layer-btn active" id="btn-layer-osm" onclick="setSuppliersMapLayer('osm')">🗺️ Plan OpenStreetMap</button>
                        <button class="btn-secondary map-layer-btn" id="btn-layer-sat" onclick="setSuppliersMapLayer('sat')">🛰️ Vue Satellite HD</button>
                    </div>
                    <button class="btn-secondary" onclick="sortSuppliers('rating')">Trier par Note ⭐</button>
                    <button class="btn-secondary" onclick="sortSuppliers('distance')">Trier par Distance 📍</button>
                    <button class="btn btn-primary" onclick="alert('Module ajout partenaire ouvert.');">➕ Ajouter Fournisseur</button>
                </div>
            </div>

            <!-- CARTE LOGISTIQUE OCCITANIE (PLAN OSM & VUE SATELLITE) -->
            <div style="background: #090d16; border: 1px solid rgba(51,65,85,0.7); border-radius: 8px; padding: 1rem; margin-bottom: 1.25rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem; flex-wrap:wrap; gap:0.4rem;">
                    <div>
                        <h4 style="font-size:0.95rem; font-weight:800; color:#38bdf8;">🗺️ Carte Logistique Réseau Occitanie</h4>
                        <div style="font-size:0.75rem; color:#94a3b8;">Rayons d'acheminement (15km, 30km, 50km) depuis le dépôt et itinéraires camions vers les chantiers</div>
                    </div>
                    <span class="badge badge-info" id="suppliers-map-badge" style="font-size:0.7rem;">OpenStreetMap Standard</span>
                </div>
                <div style="height: 300px; position:relative; overflow:hidden; border-radius:6px; border:1px solid rgba(56,189,248,0.3);">
                    <canvas id="suppliers-map-canvas" style="width:100%; height:100%; cursor:crosshair;"></canvas>
                </div>
            </div>

            <!-- SUPPLIERS GRID -->
            <div id="suppliers-grid" class="grid-3">
                <!-- Populated dynamically by renderProcurement() -->
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 19: LEDGER SHA-256 (GRAND LIVRE D'AUDIT) -->
    <!-- ========================================== -->
    <div id="tab-ledger" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">⛓️ Grand Livre d'Audit Immuable & Traçabilité Cryptographique SHA-256</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Scellement infalsifiable des ordres de service, situations de travaux, bons Trackdéchets et DGD</div>
                </div>
                <div style="display:flex; gap:0.4rem;">
                    <button class="btn btn-secondary" onclick="simulateTampering()">⚠️ Simuler Altération / Falsification</button>
                    <button class="btn btn-primary" onclick="verifyLedgerIntegrity()">🔒 Vérifier l'Intégrité de la Chaîne</button>
                </div>
            </div>

            <!-- EXPLANATION BANNER -->
            <div style="background: rgba(15,23,42,0.9); border: 2px solid var(--cyan); border-radius: 8px; padding: 1rem; margin-bottom: 1.25rem;">
                <div style="display:flex; align-items:flex-start; gap:0.75rem;">
                    <div style="font-size:2rem;">⛓️</div>
                    <div>
                        <h4 style="font-size:1.05rem; font-weight:900; color:#38bdf8; margin-bottom:0.3rem;">Qu'est-ce que le Ledger BTP & Pourquoi est-il indispensable ?</h4>
                        <div style="font-size:0.8rem; color:#cbd5e1; line-height:1.5;">
                            Dans les travaux publics et marchés publics (<strong>CCAG Travaux 2021</strong>), chaque acte contractuel (Ordre de Service, Bon de Livraison Béton/GNT, Bordereau Trackdéchets, Arrêt Intempéries, Décompte Général DGD) doit être <strong>juridiquement incontestable</strong>.
                            Le Ledger enregistre chaque événement dans une chaîne de blocs interne sécurisée par <strong>empreinte cryptographique SHA-256</strong> : si un document est modifié (même d'un centime ou d'une virgule), le sceau se brise instantanément et déclenche une alerte de non-conformité.
                        </div>
                    </div>
                </div>
            </div>

            <div id="ledger-transactions-list">
                <!-- Populated dynamically by renderLedger() -->
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 20: REGULATORY, NORMS & NATIONAL TOOLS -->
    <!-- ========================================== -->
    <div id="tab-docs" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">⚖️ Réglementation, Normes & Outils Nationaux TP & VRD</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Référentiel officiel national des textes légaux obligatoires, normes AFNOR/NF, CCTG Fascicules et guides méthodologiques CEREMA/OPPBTP/INRS</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <button class="btn-secondary active doc-tab-filter" onclick="filterDocsView('all', this)">Tous les Textes & Normes (12)</button>
                    <button class="btn-secondary doc-tab-filter" onclick="filterDocsView('loi_decret', this)">🏛️ Lois, Décrets & CCAG</button>
                    <button class="btn-secondary doc-tab-filter" onclick="filterDocsView('normes_nf', this)">📐 Normes NF & AFNOR</button>
                    <button class="btn-secondary doc-tab-filter" onclick="filterDocsView('cctg_fascicules', this)">📜 CCTG & Fascicules</button>
                    <button class="btn-secondary doc-tab-filter" onclick="filterDocsView('guides_outils', this)">🧰 Guides & Outils Méthodologie</button>
                </div>
            </div>

            <!-- REGULATORY & NORMS GRID -->
            <div id="regulatory-docs-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1rem; margin-top: 0.5rem;">
                <!-- Populated dynamically by renderRegulatoryDocs() -->
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 21: ARCHIVES (DOSSIERS FINIS & GED)    -->
    <!-- ========================================== -->
    <div id="tab-archives" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">🗄️ Archives Numériques & GED Sécurisée (Dossiers Finis, BdC, Paie, Cartes Pro)</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Conservation légale 10 ans : Marchés clos, DGD soldés, Bons de commande, Bulletins de paie RH, Cartes BTP & Habilitations AIPR</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <button class="btn-secondary active archive-cat-filter" onclick="filterArchives('all', this)">Tous les Documents (24)</button>
                    <button class="btn-secondary archive-cat-filter" onclick="filterArchives('marches_clos', this)">📁 Marchés Clos & DGD</button>
                    <button class="btn-secondary archive-cat-filter" onclick="filterArchives('bdc_factures', this)">💳 Bons de Commande & Factures</button>
                    <button class="btn-secondary archive-cat-filter" onclick="filterArchives('rh_paie', this)">👥 RH & Bulletins de Paie</button>
                    <button class="btn-secondary archive-cat-filter" onclick="filterArchives('cartes_pro', this)">🪪 Cartes BTP & CACES</button>
                    <button class="btn-secondary archive-cat-filter" onclick="filterArchives('trackdechets', this)">🚚 Fiches Trackdéchets</button>
                </div>
            </div>

            <!-- ARCHIVE SEARCH BAR -->
            <div style="background: rgba(15,23,42,0.85); border: 1px solid var(--border); border-radius: 8px; padding: 0.75rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem; flex: 1; min-width: 280px;">
                    <span style="font-size: 1.1rem;">🔍</span>
                    <input type="text" id="archives-search-input" placeholder="Rechercher par numéro de marché, nom de salarié, fournisseur ou certificat SHA-256..." class="input-field" style="width: 100%;" oninput="searchArchives(this.value)">
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <select id="archives-sort-select" class="input-field" style="width: auto; font-size: 0.75rem;" onchange="sortArchives(this.value)">
                        <option value="year_desc">Année (Récent ➔ Ancien)</option>
                        <option value="year_asc">Année (Ancien ➔ Récent)</option>
                        <option value="title_asc">Titre (A ➔ Z)</option>
                        <option value="partner">Tiers / Signataire</option>
                    </select>
                    <select id="archives-year-select" class="input-field" style="width: auto; font-size: 0.75rem;" onchange="filterArchivesByYear(this.value)">
                        <option value="all">Toutes les années</option>
                        <option value="2026">Exercice 2026</option>
                        <option value="2025">Exercice 2025</option>
                        <option value="2024">Exercice 2024</option>
                    </select>
                    <button class="btn btn-primary" onclick="alert('Module de téléversement et scellement d\'une nouvelle pièce d\'archive ouvert.');">📤 Archiver une Pièce</button>
                </div>
            </div>

            <!-- ARCHIVED DOCUMENTS GRID -->
            <div id="archives-grid" class="grid-3">
                <!-- Populated dynamically by renderArchives() -->
            </div>
        </div>
    </div>
"""
