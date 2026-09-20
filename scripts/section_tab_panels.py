def get_tab_panels():
    return """
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
                        <div style="font-size: 1.4rem; font-weight: 900; color: var(--amber); font-family: 'JetBrains Mono'; margin-top: 2px;">8 / 10 Engins</div>
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
                    <span class="card-title">📅 Planning d'Exécution, Gantt & Agenda par Équipes</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Progression journalière et affectation méthodique des équipes</div>
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
                </div>
            </div>

            <!-- CONTAINER FOR AGENDA & GANTT -->
            <div id="planning-agenda-view"></div>
            <div id="planning-gantt-view" style="display: none;"></div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 5: WATCH TOWER 3D & 2D RADAR           -->
    <!-- ========================================== -->
    <div id="tab-simulator" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap: wrap; gap: 0.75rem;">
                <div>
                    <span class="card-title">🛰️ Watch Tower 3D & Simulateur de Scénarios Méthodes</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Télémétrie d'engins, radar de zone et analyse de phasage CSPS</div>
                </div>

                <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
                    <select id="sim-scenario-select" class="input-field" style="width: auto;" onchange="loadScenario(this.value)">
                        <option value="scen_tranchee_vrd">1. Tranchée Assainissement & Blindage Profond (3.20m)</option>
                        <option value="scen_enrobes_chaud">2. Mise en Œuvre Enrobés Chauds BBSG 0/10</option>
                        <option value="scen_carrefour_giratoire">3. Carrefour Giratoire sous Circulation</option>
                    </select>

                    <div style="display: flex; background: #040711; padding: 2px; border-radius: 6px; border: 1px solid var(--border);">
                        <button class="btn-secondary sim-view-btn active" id="btn-sim-radar" onclick="setSimulatorViewMode('radar')">📡 Radar 2D</button>
                        <button class="btn-secondary sim-view-btn" id="btn-sim-3d" onclick="setSimulatorViewMode('3d')">📐 Scène 3D</button>
                    </div>

                    <button class="btn btn-secondary" id="btn-radar-toggle" onclick="toggleRadarLiveMode()">🟢 Signal Radar Direct</button>
                </div>
            </div>

            <div class="grid-split-40-60">
                <div>
                    <div id="scenario-info-card" style="margin-bottom: 1rem; background: rgba(15,23,42,0.6); padding: 1rem; border-radius: 8px; border: 1px solid rgba(51,65,85,0.6);"></div>
                    <div style="font-size: 0.8rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.5rem;">Étapes du Phasage Travaux</div>
                    <div id="scenario-steps-list"></div>
                    <div style="display: flex; gap: 0.5rem; margin-top: 0.75rem;">
                        <button class="btn btn-secondary" style="flex: 1;" onclick="prevScenarioStep()">◀ Étape Préc.</button>
                        <button class="btn btn-primary" style="flex: 1;" onclick="nextScenarioStep()">Étape Suiv. ▶</button>
                    </div>
                </div>

                <div>
                    <div id="radar-canvas-container" style="height: 380px; background: #090d16; border: 1px solid rgba(51,65,85,0.7); border-radius: 8px; overflow: hidden; position: relative;">
                        <canvas id="watchtower-radar-canvas" style="width: 100%; height: 100%;"></canvas>
                    </div>
                    <div id="view3d-canvas-container" style="height: 380px; background: #090d16; border: 1px solid rgba(51,65,85,0.7); border-radius: 8px; overflow: hidden; position: relative; display: none;">
                        <canvas id="watchtower-3d-canvas" style="width: 100%; height: 100%; cursor: grab;"></canvas>
                        <div style="position: absolute; bottom: 10px; right: 10px; display: flex; gap: 4px; z-index: 5;">
                            <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="set3DPreset('top')">Haut</button>
                            <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="set3DPreset('iso')">Iso</button>
                            <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="zoom3D(1.2)">🔍+</button>
                            <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="zoom3D(0.8)">🔍-</button>
                        </div>
                    </div>
                    <div id="step-details-box" style="margin-top: 1rem;"></div>
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
                    <div style="font-size: 0.8rem; color: #94a3b8;">Suivi des horamètres, contrôles VGP périodiques et CACES associés</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <button class="btn-secondary fleet-filter-btn active" onclick="filterFleet('all', this)">Tous</button>
                    <button class="btn-secondary fleet-filter-btn" onclick="filterFleet('pelle', this)">Pelles</button>
                    <button class="btn-secondary fleet-filter-btn" onclick="filterFleet('compacteur', this)">Compacteurs</button>
                    <button class="btn-secondary fleet-filter-btn" onclick="filterFleet('camion', this)">Camions</button>
                    <button class="btn btn-primary" onclick="openAddVehicleModal()">➕ Enregistrer un Engin</button>
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
                    <span class="card-title">🛒 Catalogue Fournitures, Petit Outillage & Stocks Dépôt</span>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Références normées, prix négociés et fiches techniques vectorielles</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <button class="btn-secondary catalog-filter-btn active" onclick="filterCatalog('all', this)">Tous</button>
                    <button class="btn-secondary catalog-filter-btn" onclick="filterCatalog('materials', this)">Matériaux & Bétons</button>
                    <button class="btn-secondary catalog-filter-btn" onclick="filterCatalog('tools', this)">Petit Outillage & Lasers</button>
                    <button class="btn-secondary catalog-filter-btn" onclick="filterCatalog('safety', this)">EPI & Signalétique</button>
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
            <div class="card-header">
                <span class="card-title">👷 Organigramme RH, Habilitations & Compagnons</span>
                <span class="badge badge-success">35 Salariés Actifs</span>
            </div>
            <div id="hr-tree-container" style="overflow-x: auto; padding: 1rem 0;"></div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 9: OPBTP SIGNAGE                       -->
    <!-- ========================================== -->
    <div id="tab-opbtp" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">🦺 Signalisation Temporaire & Balisage OPBTP</span>
                <span class="badge badge-warning">Sécurité Routière</span>
            </div>
            <div class="grid-split-40-60">
                <div>
                    <div class="input-group">
                        <label class="input-label">Type de Voie</label>
                        <select id="opbtp-road-type" class="input-field" onchange="calculateSignage()">
                            <option value="urbain">Agglomération / Rue Urbaine (50 km/h)</option>
                            <option value="bidirectionnel">Route Bidirectionnelle (80-90 km/h)</option>
                            <option value="autoroute">Voie Rapide / Autoroute (110-130 km/h)</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label class="input-label">Vitesse Approche Réglementaire</label>
                        <select id="opbtp-speed" class="input-field" onchange="calculateSignage()">
                            <option value="50">50 km/h</option>
                            <option value="80">80 km/h</option>
                            <option value="90">90 km/h</option>
                            <option value="110">110 km/h</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label class="input-label">Longueur de Chantier (ml)</label>
                        <input type="number" id="opbtp-length" class="input-field" value="120" min="20" max="5000" oninput="calculateSignage()">
                    </div>
                    <button class="btn btn-primary" style="width: 100%;" onclick="calculateSignage()">🔄 Recalculer la Signalétique</button>
                </div>
                <div id="opbtp-results"></div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 10: SAFETY & AIPR                      -->
    <!-- ========================================== -->
    <div id="tab-safety" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">🛡️ Sécurité de Chantier, DICT & AIPR</span>
                <span class="badge badge-success">0 Accident (Taux F = 0)</span>
            </div>
            <div class="grid-2">
                <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.6); padding: 1rem; border-radius: 8px;">
                    <h4 style="color: #38bdf8; font-size: 1rem; font-weight: 800; margin-bottom: 0.5rem;">🎨 Code Couleur Normalisé des Réseaux (AIPR)</h4>
                    <div style="display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.85rem;">
                        <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 14px; height: 14px; background: #ef4444; border-radius: 3px; display: inline-block;"></span> <strong>ROUGE :</strong> Électricité BT/HT & Éclairage Public</div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 14px; height: 14px; background: #eab308; border-radius: 3px; display: inline-block;"></span> <strong>JAUNE :</strong> Gaz combustible & Hydrocarbures</div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 14px; height: 14px; background: #3b82f6; border-radius: 3px; display: inline-block;"></span> <strong>BLEU :</strong> Eau Potable (AEP) & Incendie</div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 14px; height: 14px; background: #a855f7; border-radius: 3px; display: inline-block;"></span> <strong>VIOLET :</strong> Assainissement EU / EP</div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="width: 14px; height: 14px; background: #10b981; border-radius: 3px; display: inline-block;"></span> <strong>VERT :</strong> Télécommunications & Fibre Optique</div>
                    </div>
                </div>

                <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.6); padding: 1rem; border-radius: 8px;">
                    <h4 style="color: var(--emerald); font-size: 1rem; font-weight: 800; margin-bottom: 0.5rem;">📋 Règles d'Or Prévention Anti-Endommagement</h4>
                    <ul style="list-style: none; font-size: 0.85rem; color: #cbd5e1; line-height: 1.6;">
                        <li>✔️ DICT obligatoire au moins 9 jours avant l'engagement des fouilles.</li>
                        <li>✔️ Piquetage traçage obligatoire en présence du Chef de Chantier AIPR.</li>
                        <li>✔️ Terrassement doux (pelle à dents protégées ou aspiration) à moins de 0.50m des canalisations identifiées.</li>
                    </ul>
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
                    <button class="btn btn-secondary" onclick="triggerPhotoUpload()">📷 Joindre Photo Géotaggée</button>
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
    <!-- TAB 12: COMPAGNON MOBILE MODE              -->
    <!-- ========================================== -->
    <div id="tab-compagnon_mobile" class="tab-panel">
        <div class="card" style="max-width: 600px; margin: 0 auto;">
            <div class="card-header">
                <span class="card-title">📱 Mode Terrain Compagnon</span>
                <span class="badge badge-success">Connecté 4G</span>
            </div>
            <div style="display: flex; flex-direction: column; gap: 1rem;">
                <button class="btn btn-primary" style="padding: 1rem; font-size: 1rem;" onclick="triggerPhotoUpload()">
                    📷 Prendre Photo Chantier & Géolocaliser
                </button>
                <button class="btn btn-secondary" style="padding: 1rem; font-size: 1rem;" onclick="switchNav('opbtp')">
                    🦺 Guide de Balisage OPBTP Rapide
                </button>
                <button class="btn btn-secondary" style="padding: 1rem; font-size: 1rem;" onclick="switchNav('rdc')">
                    📋 Déclarer les Heures du Jour
                </button>
                <button class="btn btn-danger" style="padding: 1rem; font-size: 1rem;" onclick="triggerSimulatedCrisis()">
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
                    <div style="font-size: 0.8rem; color: #94a3b8;">Relations dynamiques stabilisées entre réglementations, fascicules CCTP et chantiers</div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
                    <button class="btn-secondary active" onclick="setObsidianHeuristic('all')">Tous les nœuds</button>
                    <button class="btn-secondary" onclick="setObsidianHeuristic('technique')">Technique VRD</button>
                    <button class="btn-secondary" onclick="setObsidianHeuristic('reglementaire')">Réglementaire</button>
                    <button class="btn-secondary" onclick="setObsidianHeuristic('financier')">Financier</button>
                    <button class="btn btn-secondary" onclick="exportObsidianVault()">📦 Exporter Vault</button>
                </div>
            </div>

            <div class="obsidian-layout">
                <div class="obsidian-graph-container">
                    <canvas id="obsidian-canvas" style="width: 100%; height: 100%;"></canvas>
                </div>
                <div class="obsidian-drawer">
                    <div style="font-size: 0.85rem; font-weight: 800; color: #38bdf8;">📌 Détails de la Fiche Active</div>
                    <div id="obsidian-node-info">
                        <div style="color: #64748b; font-size: 0.8rem;">Survolez ou cliquez sur un nœud pour inspecter ses liaisons et son contenu technique.</div>
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
                        <option value="all">Tous les chantiers</option>
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
                    <button class="btn btn-primary" onclick="openAddSupplierModal()">➕ Ajouter Fournisseur</button>
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
