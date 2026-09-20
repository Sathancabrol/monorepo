# -*- coding: utf-8 -*-

def get_tab_panels():
    return r"""
    <!-- ========================================== -->
    <!-- TAB 1: COCKPIT / DIRECTION OVERVIEW        -->
    <!-- ========================================== -->
    <div id="tab-cockpit" class="tab-panel active">
        <div class="grid-split-60-40" style="margin-bottom: 1rem;">
            <!-- KPIS SUMMARY -->
            <div class="card">
                <div class="card-header">
                    <span class="card-title">🎛️ Indicateurs Clés de Performance (KPIs Direction)</span>
                    <span class="badge badge-success">Temps Réel</span>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 0.75rem;">
                    <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.6); padding: 0.85rem; border-radius: 8px;">
                        <div style="font-size: 0.75rem; color: #64748b; font-weight: 700;">TRÉSORERIE CAISSE</div>
                        <div style="font-size: 1.4rem; font-weight: 900; color: var(--emerald); font-family: 'JetBrains Mono'; margin-top: 2px;" id="kpi-treasury-val">485 200 €</div>
                        <div style="font-size: 0.7rem; color: #10b981; margin-top: 2px;">+12.4% vs M-1</div>
                    </div>
                    <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.6); padding: 0.85rem; border-radius: 8px;">
                        <div style="font-size: 0.75rem; color: #64748b; font-weight: 700;">CHANTIERS ACTIFS</div>
                        <div style="font-size: 1.4rem; font-weight: 900; color: #38bdf8; font-family: 'JetBrains Mono'; margin-top: 2px;">4 En cours</div>
                        <div style="font-size: 0.7rem; color: #38bdf8; margin-top: 2px;">100% dans les délais</div>
                    </div>
                    <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.6); padding: 0.85rem; border-radius: 8px;">
                        <div style="font-size: 0.75rem; color: #64748b; font-weight: 700;">FLOTTE DÉPLOYÉE</div>
                        <div style="font-size: 1.4rem; font-weight: 900; color: var(--amber); font-family: 'JetBrains Mono'; margin-top: 2px;">6 / 6 Engins</div>
                        <div style="font-size: 0.7rem; color: #f59e0b; margin-top: 2px;">VGP 100% Valides</div>
                    </div>
                    <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.6); padding: 0.85rem; border-radius: 8px;">
                        <div style="font-size: 0.75rem; color: #64748b; font-weight: 700;">MARGE MOYENNE</div>
                        <div style="font-size: 1.4rem; font-weight: 900; color: #c084fc; font-family: 'JetBrains Mono'; margin-top: 2px;">14.2% HT</div>
                        <div style="font-size: 0.7rem; color: #c084fc; margin-top: 2px;">Objectif: >12%</div>
                    </div>
                </div>

                <div style="margin-top: 1.25rem;">
                    <div style="font-size: 0.8rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.5rem;">Navigation Rapide par Pôle</div>
                    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                        <button class="btn btn-secondary" onclick="switchNav('projects_hub')">📁 Chantiers en cours</button>
                        <button class="btn btn-secondary" onclick="switchNav('planning')">📅 Planning & Agenda</button>
                        <button class="btn btn-secondary" onclick="switchNav('simulator')">🛰️ Watch Tower 3D</button>
                        <button class="btn btn-secondary" onclick="switchNav('fleet')">🚜 Flotte & Engins</button>
                        <button class="btn btn-secondary" onclick="switchNav('catalog')">🛒 Catalogue & Stocks</button>
                        <button class="btn btn-secondary" onclick="switchNav('hr')">👷 Organigramme RH</button>
                        <button class="btn btn-secondary" onclick="switchNav('sdp')">💰 28 SDP & DQE TCD</button>
                        <button class="btn btn-secondary" onclick="switchNav('obsidian')">🕸️ Graphe Obsidian</button>
                    </div>
                </div>
            </div>

            <!-- TERMINAL LOGS -->
            <div class="card">
                <div class="card-header">
                    <span class="card-title">📡 Journal d'Événements Télémétriques</span>
                    <span class="badge badge-info">Agent IA Actif</span>
                </div>
                <div id="cockpit-terminal" style="background: #030712; border: 1px solid rgba(51,65,85,0.6); border-radius: 6px; padding: 0.75rem; height: 210px; overflow-y: auto; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; line-height: 1.6; color: #94a3b8;">
                    <div><span style="color:#64748b;">[08:00:00]</span> <span style="color:var(--emerald); font-weight:700;">●</span> Synchronisation base de données chantiers terminée.</div>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 2: COMPANY & TRESORERIE                -->
    <!-- ========================================== -->
    <div id="tab-company" class="tab-panel">
        <div class="card" style="margin-bottom: 1rem;">
            <div class="card-header">
                <span class="card-title">🏢 Entreprise & Trésorerie d'Exploitation</span>
                <button class="btn btn-primary" onclick="simulatePaymentSituation()">💶 Encaisser Situation (+125k€)</button>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem;">
                <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.6); padding: 1rem; border-radius: 8px;">
                    <div style="font-size: 0.75rem; color: #64748b;">SOLDE DISPONIBLE EN CAISSE</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: var(--emerald); font-family: 'JetBrains Mono'; margin-top: 4px;" id="company-caisse-val">485 200 €</div>
                    <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px;">Comptes CIC / Banque Populaire Occitanie</div>
                </div>
                <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.6); padding: 1rem; border-radius: 8px;">
                    <div style="font-size: 0.75rem; color: #64748b;">CARNET DE COMMANDES (12 MOIS)</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: #38bdf8; font-family: 'JetBrains Mono'; margin-top: 4px;">5 890 000 €</div>
                    <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px;">18 mois d'activité sécurisés</div>
                </div>
                <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.6); padding: 1rem; border-radius: 8px;">
                    <div style="font-size: 0.75rem; color: #64748b;">SITUATIONS CLIENTS EN ATTENTE</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: var(--amber); font-family: 'JetBrains Mono'; margin-top: 4px;">318 450 €</div>
                    <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px;">Chorus Pro / Dépôt Validé MOE</div>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 3: PROJECTS HUB & DOCS                 -->
    <!-- ========================================== -->
    <div id="tab-projects_hub" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">📁 Chantiers en Cours, Dossiers Techniques & Téléchargements CCTP</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Supervision des 4 opérations VRD avec accès direct aux pièces écrites</div>
                </div>
                <button class="btn btn-primary" onclick="alert('Module création de nouveau marché public ouvert.');">➕ Nouveau Chantier</button>
            </div>
            <div id="projects-grid" class="grid-2">
                <!-- Populated dynamically by renderProjectsHub() -->
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 4: PLANNING GANTT & AGENDA             -->
    <!-- ========================================== -->
    <div id="tab-planning" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.75rem;">
                <div>
                    <span class="card-title">📅 Planning d'Exécution, Gantt & Agenda Interactif par Équipes</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Cliquez sur n'importe quelle case de tâche pour ouvrir sa fiche détaillée d'affectation</div>
                </div>

                <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary planning-mode-btn active" id="btn-plan-agenda_week" onclick="setPlanningViewMode('agenda_week')">📆 Agenda Semaine</button>
                        <button class="btn-secondary planning-mode-btn" id="btn-plan-gantt" onclick="setPlanningViewMode('gantt')">📊 Gantt Multi-Chantiers</button>
                    </div>

                    <div style="display: flex; gap: 0.3rem;">
                        <button class="btn btn-secondary" onclick="changeAgendaWeek(-1)">◀ Semaine Préc.</button>
                        <button class="btn btn-secondary" onclick="resetAgendaWeek()">Aujourd'hui</button>
                        <button class="btn btn-secondary" onclick="changeAgendaWeek(1)">Semaine Suiv. ▶</button>
                    </div>

                    <select id="planning-project-select" class="input-field" style="width: auto; padding: 0.35rem 0.6rem;" onchange="renderPlanningAgenda()">
                        <option value="all">Tous les chantiers</option>
                        <option value="projet_ales">Giratoire RD906 Alès</option>
                        <option value="projet_sete">ZAC Littoral Sète</option>
                        <option value="projet_pezenas">Centre Ancien Pézenas</option>
                        <option value="projet_montpellier">Voie Verte Montpellier</option>
                    </select>

                    <select id="planning-team-select" class="input-field" style="width: auto; padding: 0.35rem 0.6rem;" onchange="renderPlanningAgenda()">
                        <option value="all">Toutes les équipes</option>
                        <option value="team_a">Équipe VRD A (M. Traoré)</option>
                        <option value="team_b">Équipe Réseaux Secs B (K. Benali)</option>
                        <option value="team_c">Équipe Enrobés C (P. Durand)</option>
                        <option value="team_topo">Cellule Topo (D. Lemoine)</option>
                    </select>
                </div>
            </div>

            <!-- CONTAINER FOR AGENDA & GANTT -->
            <div id="planning-agenda-view"></div>
            <div id="planning-gantt-view" style="display: none;"></div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 5: WATCH TOWER 3D, 4D & GOD'S EYE VIEW -->
    <!-- ========================================== -->
    <div id="tab-simulator" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.75rem;">
                <div>
                    <span class="card-title">🛰️ Watch Tower : Télémétrie, Simulation 4D & Vue Globale Osiris</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Supervision temps réel, radar de zone et synchronisation 4D des étapes de travaux</div>
                </div>

                <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
                    <select id="sim-scenario-select" class="input-field" style="width: auto;" onchange="loadScenario(this.value)">
                        <option value="scen_tranchee_vrd">1. Tranchée Assainissement & Blindage Profond (3.20m)</option>
                        <option value="scen_enrobes_chaud">2. Mise en Œuvre Enrobés Chauds BBSG 0/10</option>
                        <option value="scen_carrefour_giratoire">3. Carrefour Giratoire Urbain sous Circulation</option>
                    </select>

                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary sim-view-btn active" id="btn-sim-radar" onclick="setSimulatorViewMode('radar')">📡 Radar 2D</button>
                        <button class="btn-secondary sim-view-btn" id="btn-sim-3d" onclick="setSimulatorViewMode('3d')">📐 Scène 4D Animée</button>
                        <button class="btn-secondary sim-view-btn" id="btn-sim-global" onclick="setSimulatorViewMode('global')">🌍 Vue Globale Osiris</button>
                    </div>

                    <button class="btn btn-secondary" id="btn-radar-toggle" onclick="toggleRadarLiveMode()">🟢 Signal Direct</button>
                    <button class="btn btn-primary" id="btn-play-4d-sim" onclick="togglePlay4DSimulation()">▶️ Lancer Simulation 4D</button>
                </div>
            </div>

            <div class="grid-split-40-60" id="sim-standard-layout">
                <div>
                    <div id="scenario-info-card" style="margin-bottom: 1rem; background: rgba(15,23,42,0.6); padding: 1rem; border-radius: 8px; border: 1px solid rgba(51,65,85,0.6);"></div>
                    <div style="font-size: 0.8rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.5rem;">Étapes du Phasage Travaux (Cliquez pour Synchroniser la Scène 4D)</div>
                    <div id="scenario-steps-list"></div>
                    <div style="display: flex; gap: 0.5rem; margin-top: 0.75rem;">
                        <button class="btn btn-secondary" style="flex: 1;" onclick="prevScenarioStep()">◀ Étape Préc.</button>
                        <button class="btn btn-primary" style="flex: 1;" onclick="nextScenarioStep()">Étape Suiv. ▶</button>
                    </div>
                </div>

                <div>
                    <!-- 2D RADAR -->
                    <div id="radar-canvas-container" style="height: 400px; background: #090d16; border: 1px solid rgba(51,65,85,0.7); border-radius: 8px; overflow: hidden; position: relative;">
                        <canvas id="watchtower-radar-canvas" style="width: 100%; height: 100%;"></canvas>
                    </div>

                    <!-- 3D / 4D SIMULATION CANVAS -->
                    <div id="view3d-canvas-container" style="height: 400px; background: #090d16; border: 1px solid rgba(51,65,85,0.7); border-radius: 8px; overflow: hidden; position: relative; display: none;">
                        <canvas id="watchtower-3d-canvas" style="width: 100%; height: 100%; cursor: grab;"></canvas>
                        <div style="position: absolute; top: 12px; left: 12px; background: rgba(15,23,42,0.9); padding: 6px 12px; border-radius: 6px; border: 1px solid var(--cyan); font-size: 0.75rem; font-family: 'JetBrains Mono'; color: #38bdf8;">
                            🎬 SIMULATION 4D TEMPS RÉEL : <span id="sim-4d-phase-label" style="color:#fff; font-weight:700;">PHASE 1</span>
                        </div>
                        <div style="position: absolute; bottom: 12px; right: 12px; display: flex; gap: 4px; z-index: 5;">
                            <button class="btn btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.7rem;" onclick="set3DPreset('top')">Haut</button>
                            <button class="btn btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.7rem;" onclick="set3DPreset('iso')">Iso</button>
                            <button class="btn btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.7rem;" onclick="zoom3D(1.2)">🔍+</button>
                            <button class="btn btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.7rem;" onclick="zoom3D(0.8)">🔍-</button>
                        </div>
                    </div>

                    <div id="step-details-box" style="margin-top: 1rem;"></div>
                </div>
            </div>

            <!-- GLOBAL GOD'S EYE VIEW / OSIRIS LAYOUT -->
            <div id="sim-global-layout" style="display: none; margin-top: 1rem;">
                <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.7); border-radius: 8px; padding: 1.25rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; flex-wrap:wrap; gap:0.5rem;">
                        <div>
                            <h3 style="font-size:1.2rem; font-weight:800; color:#38bdf8;">🌍 Vue Globale Stratégique : Watchtower • Osiris • Monorepo BTP</h3>
                            <div style="font-size:0.8rem; color:#94a3b8;">Agrégation multi-satellitaire, flux télématiques et passerelles vers les outils du monorepo</div>
                        </div>
                        <div style="display:flex; gap:0.4rem;">
                            <button class="btn btn-secondary" onclick="alert('Module Watchtower Cesium 3D Globe activé !');">🌐 Watchtower Globe</button>
                            <button class="btn btn-secondary" onclick="alert('Connexion au flux Osiris Intelligence BTP active.');">👁️ Osiris BTP</button>
                            <button class="btn btn-secondary" onclick="alert('Passerelle Cognitorium active.');">🧠 Cognitorium</button>
                        </div>
                    </div>

                    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:1rem; margin-bottom:1.5rem;">
                        <div style="background:rgba(30,41,59,0.5); padding:1rem; border-radius:6px; border:1px solid rgba(51,65,85,0.5);">
                            <div style="font-size:0.75rem; color:#64748b;">RADAR RÉGIONAL OCCITANIE</div>
                            <div style="font-size:1.1rem; font-weight:800; color:var(--emerald); margin-top:2px;">4 Sites Connectés (5G)</div>
                            <div style="font-size:0.75rem; color:#94a3b8; margin-top:4px;">Alès, Sète, Pézenas, Montpellier</div>
                        </div>
                        <div style="background:rgba(30,41,59,0.5); padding:1rem; border-radius:6px; border:1px solid rgba(51,65,85,0.5);">
                            <div style="font-size:0.75rem; color:#64748b;">BALISES TÉLÉMÉTRIQUES ACTIVES</div>
                            <div style="font-size:1.1rem; font-weight:800; color:#38bdf8; margin-top:2px;">14 Balises GPS RTK</div>
                            <div style="font-size:0.75rem; color:#94a3b8; margin-top:4px;">Précision cinématique ±10mm</div>
                        </div>
                        <div style="background:rgba(30,41,59,0.5); padding:1rem; border-radius:6px; border:1px solid rgba(51,65,85,0.5);">
                            <div style="font-size:0.75rem; color:#64748b;">CAPTEURS SÉCURITÉ & DICT</div>
                            <div style="font-size:1.1rem; font-weight:800; color:var(--amber); margin-top:2px;">0 Alerte Majeure</div>
                            <div style="font-size:0.75rem; color:#94a3b8; margin-top:4px;">Surveillance géoradar active</div>
                        </div>
                    </div>

                    <div style="height:350px; background:#000; border:1px solid var(--border); border-radius:8px; position:relative; overflow:hidden; display:flex; align-items:center; justify-content:center;">
                        <canvas id="godseye-map-canvas" style="width:100%; height:100%;"></canvas>
                        <div style="position:absolute; top:12px; left:12px; background:rgba(15,23,42,0.9); padding:6px 12px; border-radius:6px; border:1px solid #38bdf8; font-size:0.75rem; font-family:'JetBrains Mono'; color:#38bdf8;">
                            🛰️ GOD'S EYE VIEW : COUVERTURE GLOBALE OCCITANIE BTP
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 6: FLEET MACHINERY                     -->
    <!-- ========================================== -->
    <div id="tab-fleet" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">🚜 Parc Matériel & Flotte d'Engins TP</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Photos réelles HD, schémas techniques, caméras embarquées, géolocalisation et spécifications VGP</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <button class="btn-secondary fleet-filter-btn active" onclick="filterFleet('all', this)">Tous</button>
                    <button class="btn-secondary fleet-filter-btn" onclick="filterFleet('pelle', this)">Pelles</button>
                    <button class="btn-secondary fleet-filter-btn" onclick="filterFleet('compacteur', this)">Compacteurs</button>
                    <button class="btn-secondary fleet-filter-btn" onclick="filterFleet('camion', this)">Camions</button>
                    <button class="btn btn-primary" onclick="alert('Module enregistrement nouvel engin ouvert.');">➕ Enregistrer un Engin</button>
                </div>
            </div>
            <div id="fleet-grid" class="grid-3">
                <!-- Populated dynamically by renderFleetGrid() -->
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 7: CATALOG & TOOLS                     -->
    <!-- ========================================== -->
    <div id="tab-catalog" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">🛒 Catalogue Fournitures, EPI, Petit Outillage & Bétons</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Fournitures normées, outillage de précision, tuyaux assainissement et bordures avec fiches techniques vectorielles</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <button class="btn-secondary catalog-filter-btn active" onclick="filterCatalog('all', this)">Tous les articles</button>
                    <button class="btn-secondary catalog-filter-btn" onclick="filterCatalog('safety', this)">🦺 EPI & Signalétique</button>
                    <button class="btn-secondary catalog-filter-btn" onclick="filterCatalog('tools', this)">⚙️ Petit Outillage & Lasers</button>
                    <button class="btn-secondary catalog-filter-btn" onclick="filterCatalog('materials', this)">🧱 Bétons, Bordures & Tuyaux</button>
                </div>
            </div>
            <div id="catalog-grid" class="grid-3">
                <!-- Populated dynamically by renderCatalogGrid() -->
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 8: HR ORGANIGRAM                       -->
    <!-- ========================================== -->
    <div id="tab-hr" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">👷 Organigramme RH, Habilitations & Agents IA Intégrés</span>
                    <div style="font-size:0.8rem; color:#94a3b8;">Cliquez sur n'importe quel collaborateur ou Agent IA pour ouvrir sa fiche détaillée</div>
                </div>
                <span class="badge badge-success">35 Salariés • 5 Agents IA Actifs</span>
            </div>
            <div id="hr-tree-container" style="overflow-x: auto; padding: 1rem 0;"></div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 9: OPBTP SIGNAGE                       -->
    <!-- ========================================== -->
    <div id="tab-opbtp" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">🦺 Signalisation Temporaire & Balisage Visuel OPBTP</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Simulation dynamique pour 6 configurations réglementaires de chantier</div>
                </div>
                <div style="display: flex; gap: 0.4rem;">
                    <button class="btn btn-secondary" id="btn-opbtp-sim-play" onclick="toggleOpbtpTrafficSimulation()">▶️ Lancer Simulation Trafic</button>
                    <button class="btn btn-primary" onclick="calculateSignage()">🔄 Recalculer Plan</button>
                </div>
            </div>

            <div class="grid-split-40-60">
                <div>
                    <div class="input-group">
                        <label class="input-label">Configuration du Chantier (6 Scénarios Réglementaires)</label>
                        <select id="opbtp-task-type" class="input-field" onchange="calculateSignage()">
                            <option value="tranchee_traversee">1. 🕳️ Tranchée en Traversée de Chaussée (Alternat KR11)</option>
                            <option value="rond_point">2. 🔄 Création Giratoire sous Circulation (Déviation K16)</option>
                            <option value="tranchee_trottoir">3. 🚶 Tranchée sous Trottoir (Passage Piétons Déporté)</option>
                            <option value="voie_etroite">4. 🏘️ Chantier en Impasse / Voie Étroite (Rue Barrée B44)</option>
                            <option value="retrecissement">5. 🛣️ Rétrécissement de Voie avec Priorité B15/C18</option>
                            <option value="nuit">6. 🌙 Intervention d'Urgence de Nuit (Balises K8 & Flashs)</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label class="input-label">Type de Voie & Vitesse de Référence</label>
                        <select id="opbtp-road-type" class="input-field" onchange="calculateSignage()">
                            <option value="urbain">Agglomération / Rue Urbaine (50 km/h)</option>
                            <option value="bidirectionnel">Route Bidirectionnelle Rase Campagne (80 km/h)</option>
                            <option value="autoroute">Voie Rapide / 2x2 Voies (110 km/h)</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label class="input-label">Longueur de Chantier (mètres linéaires)</label>
                        <input type="number" id="opbtp-length" class="input-field" value="120" min="20" max="5000" oninput="calculateSignage()">
                    </div>
                </div>
                <div id="opbtp-results"></div>
            </div>

            <!-- VISUAL ROAD SIGNAGE DIAGRAM -->
            <div style="margin-top: 1.5rem; background: #090d16; border: 1px solid rgba(51,65,85,0.7); border-radius: 8px; padding: 1rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem; flex-wrap:wrap; gap:0.5rem;">
                    <div>
                        <h4 style="font-size:1rem; font-weight:800; color:#38bdf8;" id="opbtp-diagram-title">📐 Schéma Visuel d'Implantation des Panneaux & Trafic</h4>
                        <div style="font-size:0.75rem; color:#94a3b8;" id="opbtp-diagram-subtitle">Instruction Interministérielle Livre I - 8e partie</div>
                    </div>
                    <div style="display:flex; gap:0.3rem;">
                        <button class="btn btn-secondary" style="padding:0.25rem 0.5rem; font-size:0.75rem;" onclick="switchTrafficLightState()">🚦 Inverser Feux KR11</button>
                    </div>
                </div>
                <div style="height: 240px; position:relative; overflow:hidden;" id="opbtp-canvas-wrapper">
                    <canvas id="opbtp-signage-canvas" style="width: 100%; height: 100%;"></canvas>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 10: SAFETY & AIPR                      -->
    <!-- ========================================== -->
    <div id="tab-safety" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">🛡️ Sécurité AIPR, DICT & Code Couleur des Réseaux</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Prévention des risques d'endommagement, blindage et consignes réglementaires</div>
                </div>
                <button class="btn btn-danger" onclick="openSafetyEmergencySimulator()">🚨 Lancer Simulateur de Crise & Heatmap</button>
            </div>

            <div class="grid-2" style="margin-bottom: 1.5rem;">
                <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.6); padding: 1rem; border-radius: 8px;">
                    <h4 style="color: #38bdf8; font-size: 1rem; font-weight: 800; margin-bottom: 0.5rem;">🎨 Code Couleur Normalisé des 7 Réseaux (AIPR)</h4>
                    <div style="display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.85rem;">
                        <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 14px; height: 14px; background: #ef4444; border-radius: 3px; display: inline-block;"></span> <strong>ROUGE :</strong> Électricité BT/HTA/HTB & Éclairage Public</div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 14px; height: 14px; background: #eab308; border-radius: 3px; display: inline-block;"></span> <strong>JAUNE :</strong> Gaz combustible (MPB/MPC) & Hydrocarbures</div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 14px; height: 14px; background: #3b82f6; border-radius: 3px; display: inline-block;"></span> <strong>BLEU :</strong> Eau Potable (AEP) & Défense Incendie</div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 14px; height: 14px; background: #a855f7; border-radius: 3px; display: inline-block;"></span> <strong>VIOLET :</strong> Assainissement Eaux Usées (EU) / Pluviales (EP)</div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 14px; height: 14px; background: #10b981; border-radius: 3px; display: inline-block;"></span> <strong>VERT :</strong> Télécommunications, Fibre Optique & Vidéoprotection</div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 14px; height: 14px; background: #f97316; border-radius: 3px; display: inline-block;"></span> <strong>ORANGE :</strong> Produits Chimiques & Matières Dangereuses</div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 14px; height: 14px; background: #ffffff; border-radius: 3px; display: inline-block;"></span> <strong>BLANC :</strong> Piquetage / Traçage Zone de Chantier</div>
                    </div>
                </div>

                <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.6); padding: 1rem; border-radius: 8px;">
                    <h4 style="color: var(--emerald); font-size: 1rem; font-weight: 800; margin-bottom: 0.5rem;">📋 Recommandations & Impératifs Chantier / Bureau</h4>
                    <ul style="list-style: none; font-size: 0.85rem; color: #cbd5e1; line-height: 1.6;">
                        <li>✔️ <strong>Bureau</strong> : Déclaration DICT dématérialisée obligatoire sous 9 jours minimum.</li>
                        <li>✔️ <strong>Chantier</strong> : Piquetage traçage obligatoire en présence de l'Encadrant AIPR certifié.</li>
                        <li>✔️ <strong>Fouilles</strong> : Blindage impératif dès 1.30m de profondeur selon R4534.</li>
                        <li>✔️ <strong>Approche</strong> : Terrassement doux / aspiration à moins de 0.50m des conduites sensibles.</li>
                        <li>✔️ <strong>Lignes HTA</strong> : Distance de sécurité minimale de 3m (<50kV) et 5m (>50kV).</li>
                    </ul>
                </div>
            </div>

            <!-- NEW PERMANENT VISUAL SIMULATION WINDOW (BOTTOM OF AIPR TAB) -->
            <div style="background: rgba(15,23,42,0.9); border: 2px solid var(--cyan); border-radius: 8px; padding: 1.25rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; flex-wrap:wrap; gap:0.5rem;">
                    <div>
                        <h3 style="font-size:1.15rem; font-weight:800; color:#38bdf8;">🔬 Simulateur Visuel de Situations Réelles de Chantier & Détection Réseaux</h3>
                        <div style="font-size:0.8rem; color:#94a3b8;">Visualisation en coupe de terrain des distances d'approche et des interactions engin / réseaux</div>
                    </div>
                    <div style="display:flex; gap:0.4rem; flex-wrap:wrap;">
                        <button class="btn-secondary aipr-sim-btn active" onclick="setAiprSituation('gaz')">1. Conduite Gaz PEHD</button>
                        <button class="btn-secondary aipr-sim-btn" onclick="setAiprSituation('hta')">2. Ligne Aérienne HTA 20kV</button>
                        <button class="btn-secondary aipr-sim-btn" onclick="setAiprSituation('fibre_aep')">3. Fibre + AEP Fonte</button>
                        <button class="btn-secondary aipr-sim-btn" onclick="setAiprSituation('blindage')">4. Blindage Profond 3.2m</button>
                    </div>
                </div>

                <div class="grid-split-60-40">
                    <div style="height: 320px; background: #000; border: 1px solid rgba(56,189,248,0.4); border-radius: 6px; position: relative; overflow: hidden;">
                        <canvas id="aipr-simulation-canvas" style="width: 100%; height: 100%; cursor: pointer;"></canvas>
                        <div id="aipr-sim-hud" style="position: absolute; bottom: 8px; left: 8px; background: rgba(15,23,42,0.9); padding: 4px 10px; border-radius: 4px; font-family: 'JetBrains Mono'; font-size: 0.75rem; color: #38bdf8; border: 1px solid rgba(56,189,248,0.3);">
                            SITUATION : FOUILLE À PROXIMITÉ CONDUITE GAZ PEHD 4 BAR
                        </div>
                    </div>
                    <div id="aipr-situation-action-box" style="background: rgba(30,41,59,0.5); border: 1px solid rgba(51,65,85,0.6); padding: 1rem; border-radius: 6px; display: flex; flex-direction: column; justify-content: space-between;">
                        <!-- Populated dynamically by setAiprSituation() -->
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 11: RDC DAILY LOGBOOK                  -->
    <!-- ========================================== -->
    <div id="tab-rdc" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">📋 Rapports Journaliers de Chantier (RDC) & Registre d'Heures</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Journal légal des opérations, intempéries, incidents et pointage MO/Engins</div>
                </div>
                <div style="display: flex; gap: 0.4rem;">
                    <button class="btn btn-secondary" onclick="openRdcCameraModal()">📷 Prendre Photo / Flux Direct</button>
                    <button class="btn btn-primary" onclick="exportRDC()">📥 Exporter Registre Complet (PDF)</button>
                </div>
            </div>

            <!-- RDC FORM -->
            <div style="background: rgba(15,23,42,0.7); border: 1px solid rgba(51,65,85,0.6); padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
                <h4 style="font-size: 0.95rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.75rem;">➕ Nouvelle Saisie RDC Journalière</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.75rem; margin-bottom: 0.75rem;">
                    <div>
                        <label class="input-label">Chantier</label>
                        <select id="rdc-proj-select" class="input-field">
                            <option value="Giratoire RD906 Alès">Giratoire RD906 Alès</option>
                            <option value="ZAC Littoral Sète">ZAC Littoral Sète</option>
                            <option value="Centre Ancien Pézenas">Centre Ancien Pézenas</option>
                            <option value="Voie Verte Montpellier">Voie Verte Montpellier</option>
                        </select>
                    </div>
                    <div>
                        <label class="input-label">Date</label>
                        <input type="date" id="rdc-date" class="input-field">
                    </div>
                    <div>
                        <label class="input-label">Chef de Chantier</label>
                        <input type="text" id="rdc-chief" class="input-field" value="A. Martin">
                    </div>
                    <div>
                        <label class="input-label">Météo / T°</label>
                        <input type="text" id="rdc-weather" class="input-field" value="Ensoleillé (23°C)">
                    </div>
                    <div>
                        <label class="input-label">Heures Main d'Œuvre</label>
                        <input type="number" id="rdc-heures-mo" class="input-field" value="35">
                    </div>
                    <div>
                        <label class="input-label">Heures Engins</label>
                        <input type="number" id="rdc-heures-engins" class="input-field" value="14">
                    </div>
                </div>
                <div class="input-group">
                    <label class="input-label">Travaux Réalisés & Observations</label>
                    <input type="text" id="rdc-desc" class="input-field" value="Pose de 90 ml de bordures T2 et coulage calage béton. Contrôle altimétrique conforme.">
                </div>
                <div style="display: flex; justify-content: flex-end; gap: 0.5rem;">
                    <button class="btn btn-secondary" onclick="openRdcCameraModal()">📷 Prendre Photo / Flux Direct</button>
                    <button class="btn btn-primary" onclick="saveRdcEntry()">💾 Enregistrer le Rapport</button>
                </div>
            </div>

            <!-- RDC TABLE -->
            <div style="background: rgba(15,23,42,0.6); border: 1px solid rgba(51,65,85,0.6); border-radius: 8px; overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem; min-width: 800px;">
                    <thead>
                        <tr style="background: rgba(30,41,59,0.9); color: #94a3b8; text-align: left;">
                            <th style="padding: 0.75rem;">N° RDC</th>
                            <th style="padding: 0.75rem;">Chantier</th>
                            <th style="padding: 0.75rem;">Date</th>
                            <th style="padding: 0.75rem;">Chef</th>
                            <th style="padding: 0.75rem;">Notes Travaux</th>
                            <th style="padding: 0.75rem;">Heures MO</th>
                            <th style="padding: 0.75rem;">Heures Engins</th>
                            <th style="padding: 0.75rem;">Export</th>
                        </tr>
                    </thead>
                    <tbody id="rdc-table-body">
                        <!-- Populated dynamically by renderRdcTable() -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 12: COMPAGNON MOBILE MODE (WITH DIRECT PLANNING) -->
    <!-- ========================================== -->
    <div id="tab-compagnon_mobile" class="tab-panel">
        <div class="card" style="max-width: 780px; margin: 0 auto;">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">📱 Mode Terrain Compagnon & Mon Planning</span>
                    <div style="font-size:0.8rem; color:#94a3b8;">Espace dédié aux ouvriers et chefs d'équipe sur chantier</div>
                </div>
                <span class="badge badge-success">Connecté 4G • GPS RTK Actif</span>
            </div>

            <!-- TEAM SELECTION FOR COMPAGNON -->
            <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(30,41,59,0.6); padding:0.75rem; border-radius:6px; margin-bottom:1rem; flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <div style="font-size:0.75rem; color:#94a3b8;">MON ÉQUIPE :</div>
                    <select id="compagnon-team-select" class="input-field" style="width:auto; padding:0.35rem 0.6rem; font-weight:800; color:#38bdf8;" onchange="renderCompagnonPlanning()">
                        <option value="team_a">Équipe VRD A (Mamadou Traoré)</option>
                        <option value="team_b">Équipe Réseaux Secs B (Karim Benali)</option>
                        <option value="team_c">Équipe Enrobés C (Patrick Durand)</option>
                        <option value="team_topo">Cellule Topo (David Lemoine)</option>
                    </select>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:0.75rem; color:#94a3b8;">CHANTIER :</div>
                    <div style="font-size:0.9rem; font-weight:800; color:var(--emerald);" id="compagnon-current-site">Giratoire RD906 Alès</div>
                </div>
            </div>

            <!-- COMPAGNON'S DIRECT PLANNING BOX -->
            <div id="compagnon-planning-container" style="margin-bottom:1.25rem;">
                <!-- Populated dynamically by renderCompagnonPlanning() -->
            </div>

            <!-- FIELD QUICK ACTION BUTTONS -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;">
                <button class="btn btn-primary" style="padding: 0.85rem; font-size: 0.9rem;" onclick="openRdcCameraModal()">
                    📷 Prendre Photo Chantier & Géoloc
                </button>
                <button class="btn btn-secondary" style="padding: 0.85rem; font-size: 0.9rem;" onclick="switchNav('opbtp')">
                    🦺 Guide de Balisage OPBTP
                </button>
                <button class="btn btn-secondary" style="padding: 0.85rem; font-size: 0.9rem;" onclick="switchNav('rdc')">
                    📋 Déclarer mes Heures du Jour
                </button>
                <button class="btn btn-danger" style="padding: 0.85rem; font-size: 0.9rem;" onclick="triggerSimulatedCrisis()">
                    ⚠️ Alerte Sécurité / Arrêt d'Urgence
                </button>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 13: OBSIDIAN GRAPH VIEW                -->
    <!-- ========================================== -->
    <div id="tab-obsidian" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">🕸️ Graphe de Connaissances Obsidian (Génie Civil & VRD)</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Relations dynamiques stabilisées : cliquez sur un nœud pour inspecter sa fiche Markdown</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <input type="text" id="obsidian-search-input" placeholder="🔍 Rechercher..." class="input-field" style="width: 140px; padding: 0.35rem 0.5rem;" oninput="searchObsidianNodes(this.value)">
                    <button class="btn-secondary active obs-cat-btn" onclick="setObsidianHeuristic('all', this)">Tous</button>
                    <button class="btn-secondary obs-cat-btn" onclick="setObsidianHeuristic('technique', this)">Technique</button>
                    <button class="btn-secondary obs-cat-btn" onclick="setObsidianHeuristic('reglementaire', this)">Réglementaire</button>
                    <button class="btn-secondary obs-cat-btn" onclick="setObsidianHeuristic('financier', this)">Financier</button>
                    <button class="btn-secondary obs-cat-btn" onclick="setObsidianHeuristic('management', this)">Sécurité/RH</button>
                    <button class="btn btn-secondary" onclick="resetObsidianCamera()">🎯 Recentrer</button>
                </div>
            </div>

            <div class="obsidian-layout">
                <div class="obsidian-graph-container" style="height: 550px; position: relative;">
                    <canvas id="obsidian-canvas" style="width: 100%; height: 100%; cursor: grab;"></canvas>
                    <div style="position: absolute; bottom: 12px; left: 12px; display: flex; gap: 4px; z-index: 5;">
                        <button class="btn btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="zoomObsidian(1.2)">🔍 +</button>
                        <button class="btn btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="zoomObsidian(0.8)">🔍 -</button>
                        <button class="btn btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="reorganizeObsidianNodes()">🔄 Réorganiser</button>
                    </div>
                </div>
                <div class="obsidian-drawer" style="height: 550px;">
                    <div style="font-size: 0.85rem; font-weight: 800; color: #38bdf8;">📌 Détails de la Fiche Technique Active</div>
                    <div id="obsidian-node-info">
                        <div style="color: #64748b; font-size: 0.8rem; line-height: 1.5;">Cliquez ou glissez un nœud sur le graphe pour afficher son contenu technique complet, ses règles associées et ses liaisons transversales.</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 14: SCHEMAS & FORMULAS                 -->
    <!-- ========================================== -->
    <div id="tab-schemas" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">📐 Formules Mathématiques & Calculs Réactifs TP</span>
                <span class="badge badge-info">Ingénierie VRD</span>
            </div>
            <div class="grid-split-40-60">
                <div>
                    <div class="input-group">
                        <label class="input-label">Sélectionnez la Formule de Génie Civil</label>
                        <select id="formula-type-select" class="input-field" onchange="updateFormulaCalculator()">
                            <option value="compactage">Ratio Compactage GTR Q/S & Débit horaire</option>
                            <option value="manning">Hydraulique : Débit Collecteur Manning-Strickler</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label class="input-label">Paramètre 1 (Épaisseur couche en m ou Diamètre DN en m)</label>
                        <input type="number" id="f-param-1" class="input-field" value="0.30" step="0.05" oninput="updateFormulaCalculator()">
                    </div>
                    <div class="input-group">
                        <label class="input-label">Paramètre 2 (Vitesse rouleau km/h ou Pente canalisation m/m)</label>
                        <input type="number" id="f-param-2" class="input-field" value="4.0" step="0.5" oninput="updateFormulaCalculator()">
                    </div>
                    <div class="input-group">
                        <label class="input-label">Paramètre 3 (Largeur bille en m)</label>
                        <input type="number" id="f-param-3" class="input-field" value="2.10" step="0.1" oninput="updateFormulaCalculator()">
                    </div>
                    <div class="input-group">
                        <label class="input-label">Paramètre 4 (Nombre de passes N)</label>
                        <input type="number" id="f-param-4" class="input-field" value="6" step="1" oninput="updateFormulaCalculator()">
                    </div>
                </div>
                <div id="formula-calculation-output">
                    <!-- Populated dynamically by updateFormulaCalculator() -->
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 15: SDP & DQE PIVOT TABLE              -->
    <!-- ========================================== -->
    <div id="tab-sdp" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.75rem;">
                <div>
                    <span class="card-title">💰 28 Sous-Détails de Prix (SDP) & Tableau Croisé Dynamique DQE</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Décomposition analytique du Déboursé Sec (D.S.) et application du coefficient K=1.35</div>
                </div>

                <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary sdp-view-btn active" id="btn-sdp-dqe_tcd" onclick="setSDPViewMode('dqe_tcd')">📊 Tableau Croisé DQE</button>
                        <button class="btn-secondary sdp-view-btn" id="btn-sdp-cards" onclick="setSDPViewMode('cards')">🗂️ 28 Fiches SDP</button>
                    </div>

                    <select id="dqe-project-select" class="input-field" style="width: auto; padding: 0.35rem 0.6rem;" onchange="renderDQEPivotTable()">
                        <option value="all">Tous les chantiers (28 prix)</option>
                        <option value="projet_ales">Giratoire RD906 Alès</option>
                        <option value="projet_sete">ZAC Littoral Sète</option>
                        <option value="projet_pezenas">Centre Ancien Pézenas</option>
                        <option value="projet_montpellier">Voie Verte Montpellier</option>
                    </select>

                    <select id="dqe-lot-select" class="input-field" style="width: auto; padding: 0.35rem 0.6rem;" onchange="renderDQEPivotTable()">
                        <option value="all">Tous les lots</option>
                        <option value="Terrassement">Lot 1 : Terrassement</option>
                        <option value="Assainissement">Lot 2 : Assainissement</option>
                        <option value="Voirie">Lot 3 : Voirie</option>
                        <option value="Réseaux Secs">Lot 4 : Réseaux Secs</option>
                    </select>

                    <button class="btn btn-primary" onclick="exportDQEtoCSV()">📥 Exporter CSV</button>
                    <button class="btn btn-secondary" onclick="printDQESummary()">🖨️ Imprimer</button>
                </div>
            </div>

            <!-- DQE & SDP CONTAINERS -->
            <div id="sdp-dqe-tcd-view"></div>
            <div id="sdp-cards-view" style="display: none;"></div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 16: PROCUREMENT & SUPPLIERS            -->
    <!-- ========================================== -->
    <div id="tab-procurement" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">🛒 Fournisseurs Partenaires & Négociations Tarifs</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Carrières, centrales à béton et négoces régionaux en Occitanie</div>
                </div>
                <div style="display: flex; gap: 0.4rem;">
                    <button class="btn-secondary" onclick="sortSuppliers('rating')">Trier par Note ⭐</button>
                    <button class="btn-secondary" onclick="sortSuppliers('distance')">Trier par Distance 📍</button>
                    <button class="btn btn-primary" onclick="alert('Module ajout partenaire ouvert.');">➕ Ajouter Fournisseur</button>
                </div>
            </div>
            <div id="suppliers-grid" class="grid-3">
                <!-- Populated dynamically by renderProcurement() -->
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 17: LEDGER SHA-256 AUDIT TRAIL         -->
    <!-- ========================================== -->
    <div id="tab-ledger" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.5rem;">
                <div>
                    <span class="card-title">⛓️ Registre Cryptographique & Piste d'Audit SHA-256</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Scellement immuable des réceptions, situations de travaux et contrôles</div>
                </div>
                <button class="btn btn-primary" onclick="verifyLedgerIntegrity()">🔒 Vérifier l'Intégrité de la Chaîne</button>
            </div>
            <div id="ledger-transactions-list">
                <!-- Populated dynamically by renderLedger() -->
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 18: REPORTS & DOCS CCTP                -->
    <!-- ========================================== -->
    <div id="tab-docs" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">📚 Dossiers Réglementaires & Rapports d'Expertise CCTP</span>
                <span class="badge badge-success">8 Rapports Exhaustifs</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem;">
                <div class="card" style="background: rgba(15,23,42,0.8);">
                    <h4 style="font-size: 1rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.5rem;">01. Analyse Marchés & DCE</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.75rem;">CCAG Travaux 2021, décomposition forfait/bordereau, révision de prix TP01/TP02.</p>
                    <button class="btn btn-secondary" style="width: 100%; font-size: 0.75rem;" onclick="downloadDoc('01_ANALYSE_MARCHES_DCE')">📄 Télécharger Rapport</button>
                </div>
                <div class="card" style="background: rgba(15,23,42,0.8);">
                    <h4 style="font-size: 1rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.5rem;">02. Étude de Prix & SDP</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.75rem;">Méthodologie des 28 déboursés secs, barème de vente et coefficient K=1.35.</p>
                    <button class="btn btn-secondary" style="width: 100%; font-size: 0.75rem;" onclick="downloadDoc('02_ETUDE_DE_PRIX_METHODES')">📄 Télécharger Rapport</button>
                </div>
                <div class="card" style="background: rgba(15,23,42,0.8);">
                    <h4 style="font-size: 1rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.5rem;">03. Technique Voirie & Réseaux</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.75rem;">Fascicules 70-1, 71, CCTG, pose de canalisations fonte/PVC et enrobés BBSG.</p>
                    <button class="btn btn-secondary" style="width: 100%; font-size: 0.75rem;" onclick="downloadDoc('03_TECHNIQUE_VOIRIE_RESEAUX')">📄 Télécharger Rapport</button>
                </div>
                <div class="card" style="background: rgba(15,23,42,0.8);">
                    <h4 style="font-size: 1rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.5rem;">04. DICT, AIPR & Sécurité</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.75rem;">Réglementation anti-endommagement, guichet unique et signalétique OPBTP.</p>
                    <button class="btn btn-secondary" style="width: 100%; font-size: 0.75rem;" onclick="downloadDoc('04_REGLEMENTATION_AIPR_DICT')">📄 Télécharger Rapport</button>
                </div>
            </div>
        </div>
    </div>
"""
