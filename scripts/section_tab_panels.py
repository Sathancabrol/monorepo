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
                <div class="kpi-val text-cyan" id="kpi-treasury-val">184 500 €</div>
                <div class="kpi-sub">BFR Couvert : 42 jours d'exploitation</div>
            </div>
            <div class="card kpi-card">
                <div class="kpi-label">Chantiers en Cours</div>
                <div class="kpi-val text-emerald">4 Actifs</div>
                <div class="kpi-sub">Alès, Sète, Pézenas, Montpellier</div>
            </div>
            <div class="card kpi-card">
                <div class="kpi-label">Effectif VRD Engagé</div>
                <div class="kpi-val" style="color:var(--amber);">18 Salariés</div>
                <div class="kpi-sub">100% CACES & AIPR à jour</div>
            </div>
            <div class="card kpi-card">
                <div class="kpi-label">Conformité Sécurité / DICT</div>
                <div class="kpi-val" style="color:#a855f7;">100% Validé</div>
                <div class="kpi-sub">0 Incident • Audit SHA-256 Actif</div>
            </div>
        </div>

        <!-- GIS INTERACTIVE MAP & AUTOPILOT -->
        <div class="grid-split-60-40" style="margin-top: 1rem;">
            <div class="card">
                <div class="card-header">
                    <span class="card-title">🗺️ Cartographie SIG des Chantiers & Flotte (Occitanie)</span>
                    <span class="badge badge-info">OpenStreetMap Live</span>
                </div>
                <div class="map-container" style="height: 380px;" id="cockpit-map-container">
                    <canvas id="cockpit-osm-canvas" style="width: 100%; height: 100%;"></canvas>
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
                        <button class="btn btn-secondary" onclick="switchNav('docs')">📚 Dossiers Réglementaires</button>
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
                    <h2 style="font-size: 1.3rem; font-weight: 900; color: #f8fafc; margin-top: 4px;" id="company-profile-title">Occitanie Travaux Publics SAS</h2>
                    <div style="font-size: 0.8rem; color: #94a3b8;">SIRET : 842 190 345 00021 • Capital : 150 000 € • Siège : Sète (34)</div>
                </div>
                <div style="display: flex; gap: 1.5rem;">
                    <div>
                        <div style="font-size: 0.75rem; color: #94a3b8;">SOLDE CAISSE DISPONIBLE</div>
                        <div style="font-size: 1.6rem; font-weight: 900; color: var(--emerald);" id="company-caisse-val">184 500 €</div>
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
                    <div style="font-size: 0.8rem; color: #94a3b8;">Planification des équipes, phasage des travaux et jalons de réception</div>
                </div>
                <div style="display: flex; gap: 0.4rem;">
                    <button class="btn-secondary planning-mode-btn active" onclick="setPlanningViewMode('agenda_week')">📅 Semaine</button>
                    <button class="btn-secondary planning-mode-btn" onclick="setPlanningViewMode('agenda_month')">🗓️ Mois</button>
                    <button class="btn-secondary planning-mode-btn" onclick="setPlanningViewMode('gantt')">📊 Diagramme Gantt</button>
                </div>
            </div>

            <div id="planning-content-view">
                <!-- Populated dynamically by renderPlanningAgenda() or renderPlanningGantt() -->
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 6: WATCH TOWER 3D / 4D SIMULATION      -->
    <!-- ========================================== -->
    <div id="tab-simulator" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">🛰️ Watch Tower 3D/4D : Jumeau Numérique Synchrone & Radar Chantier</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Pelle Liebherr 24t articulée, Benne 8x4, Blindage Krings, Laser Piper, Drone RTK et Répertoire des Acteurs</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <button class="btn btn-secondary" onclick="resetSimulatorView('iso')">📐 Vue Isométrique</button>
                    <button class="btn btn-secondary" onclick="resetSimulatorView('top')">🧭 Vue Dessus</button>
                    <button class="btn btn-secondary" onclick="zoomSimulator(1.2)">🔍 +</button>
                    <button class="btn btn-secondary" onclick="zoomSimulator(0.8)">🔍 -</button>
                    <button class="btn btn-primary" id="btn-toggle-4d-sim" onclick="toggle4DSimulation()">▶️ Lancer Simulation 4D</button>
                </div>
            </div>

            <!-- 4D PHASES PROGRESSION BAR -->
            <div style="background: rgba(15,23,42,0.9); border: 1px solid var(--border); border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 1rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 1.1rem;">⏱️</span>
                    <strong style="font-size: 0.85rem; color: #38bdf8;">Phasage 4D & Progression :</strong>
                </div>
                <div style="display: flex; gap: 0.3rem; flex-wrap: wrap;">
                    <button class="btn-secondary sim-phase-btn active" onclick="setSimPhase(1)">Phase 1 : Terrassement & Purge</button>
                    <button class="btn-secondary sim-phase-btn" onclick="setSimPhase(2)">Phase 2 : Canalisations Ø400</button>
                    <button class="btn-secondary sim-phase-btn" onclick="setSimPhase(3)">Phase 3 : Bordures & Trottoirs</button>
                    <button class="btn-secondary sim-phase-btn" onclick="setSimPhase(4)">Phase 4 : Enrobés BBSG</button>
                    <button class="btn-secondary sim-phase-btn" onclick="setSimPhase(5)">Phase 5 : Réception & OPR</button>
                </div>
            </div>

            <!-- 3D VIEWPORT & RADAR SPLIT -->
            <div class="grid-split-60-40">
                <div style="height: 420px; background: #070a14; border: 1px solid rgba(56,189,248,0.4); border-radius: 8px; position: relative; overflow: hidden;">
                    <canvas id="watchtower-3d-canvas" style="width: 100%; height: 100%; cursor: grab;"></canvas>
                    <div style="position: absolute; top: 10px; left: 10px; background: rgba(15,23,42,0.85); padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; color: #38bdf8; border: 1px solid rgba(56,189,248,0.3);">
                        CHANTIER : GIRATOIRE RD906 ALÈS • PK 0+240
                    </div>
                </div>

                <div style="height: 420px; background: #070a14; border: 1px solid rgba(56,189,248,0.4); border-radius: 8px; position: relative; overflow: hidden;">
                    <canvas id="watchtower-radar-canvas" style="width: 100%; height: 100%;"></canvas>
                    <div style="position: absolute; top: 10px; right: 10px; background: rgba(15,23,42,0.85); padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; color: var(--emerald); border: 1px solid rgba(16,185,129,0.3);">
                        RADAR TÉLÉMÉTRIE & PROXIMITÉ
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
                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary tech-view-btn active" id="btn-tech-formulas" onclick="setTechniqueViewMode('formulas')">🧮 Simulateur de Formules</button>
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
                                <option value="tonnage_enrobes">2. 🛣️ Tonnage & Enrobés : Chaussée BBSG, Émulsion C65B4 & Fini m²</option>
                                <option value="perimetre_bordures">3. 📏 Linéaires & Périmètres : Bordures T2/P1, Caniveaux CC1 & Semelle Béton</option>
                                <option value="manning_hydraulique">4. 💧 Hydraulique : Débit Collecteur Manning-Strickler & Auto-curage</option>
                                <option value="pente_canalisateur">5. 📐 Pente & Altimétrie : Calcul de Fil d'Eau Laser & ΔH</option>
                                <option value="compactage_gtr">6. 🔨 Compactage GTR : Débit Q/S, Nombre de Passes N & Vitesse</option>
                                <option value="revision_tp08">7. 📈 Révision de Prix : Formule Paramétrique Marchés Publics TP08</option>
                                <option value="debourse_sec_k">8. 💰 Déboursé Sec (DS) & Prix de Vente HT avec Coefficient K</option>
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
                                    <strong id="cmp-ev2-val" style="color: var(--emerald);">95.4 MPa (Norme $\ge 80$ MPa)</strong>
                                </div>
                                <div style="display: flex; justify-content: space-between; margin-bottom: 2px;">
                                    <span style="color: #94a3b8;">Rapport de Compactage EV2/EV1 :</span>
                                    <strong id="cmp-k-val" style="color: var(--emerald);">1.68 (Norme $\le 2.0$)</strong>
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
