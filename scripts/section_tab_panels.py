def get_tab_panels():
    return """
    <!-- 1. TAB COCKPIT -->
    <div id="tab-cockpit" class="tab-panel active">
        <!-- TOP 4 KPI CARDS -->
        <div class="grid-4" style="margin-bottom:1rem;">
            <div class="card" style="border-left:4px solid var(--emerald);">
                <div style="font-size:0.7rem; color:var(--text-muted); font-weight:700;">TRÉSORERIE DISPONIBLE</div>
                <div style="font-size:1.4rem; font-weight:900; color:#fff; margin:0.2rem 0;" id="kpi-treasury-val">485 200 €</div>
                <div style="font-size:0.7rem; color:var(--emerald);">● Caisse saine (+32.4k€ ce mois)</div>
            </div>
            <div class="card" style="border-left:4px solid var(--cyan);">
                <div style="font-size:0.7rem; color:var(--text-muted); font-weight:700;">MARGE GLOBALE PORTFOLIO</div>
                <div style="font-size:1.4rem; font-weight:900; color:var(--cyan); margin:0.2rem 0;">+14.8 %</div>
                <div style="font-size:0.7rem; color:var(--cyan);">● Objectif budget > 12.0% atteint</div>
            </div>
            <div class="card" style="border-left:4px solid var(--amber);">
                <div style="font-size:0.7rem; color:var(--text-muted); font-weight:700;">EFFECTIF ACTIF & ENGINS</div>
                <div style="font-size:1.4rem; font-weight:900; color:var(--amber); margin:0.2rem 0;">12 Salariés | 14 Engins</div>
                <div style="font-size:0.7rem; color:var(--amber);">● 4 chantiers opérationnels</div>
            </div>
            <div class="card" style="border-left:4px solid var(--purple);">
                <div style="font-size:0.7rem; color:var(--text-muted); font-weight:700;">CONFORMITÉ SÉCURITÉ & AIPR</div>
                <div style="font-size:1.4rem; font-weight:900; color:var(--purple); margin:0.2rem 0;">100 % Conforme</div>
                <div style="font-size:0.7rem; color:var(--purple);">● 0 accident | DICT scellées</div>
            </div>
        </div>

        <!-- AGENTS SWARM HUD -->
        <div class="card" style="margin-bottom:1rem; background:linear-gradient(135deg, rgba(15,23,42,0.9), rgba(4,7,17,0.9)); border:1px solid rgba(6,182,212,0.3);">
            <div class="card-header">
                <span class="card-title">🤖 Essaim d'Agents IA Autonomes BTP (Active Swarm)</span>
                <span class="card-badge" style="color:var(--emerald);">8 AGENTS CONNECTÉS</span>
            </div>
            <div id="swarm-chips-container" style="display:flex; flex-wrap:wrap; gap:0.5rem;">
                <!-- Populated by JS -->
            </div>
        </div>

        <div class="grid-split-60-40">
            <!-- COCKPIT TERMINAL & ALERTS -->
            <div class="card">
                <div class="card-header">
                    <span class="card-title">📡 Flux Télémétrique & Journal des Événements</span>
                    <button class="btn-secondary" style="font-size:0.7rem; padding:0.2rem 0.5rem;" onclick="document.getElementById('cockpit-terminal').innerHTML=''">Effacer</button>
                </div>
                <div id="cockpit-terminal" style="background:#040711; border:1px solid var(--border); border-radius:6px; padding:0.8rem; font-family:var(--font-mono); font-size:0.72rem; height:240px; overflow-y:auto; display:flex; flex-direction:column; gap:0.35rem;">
                    <!-- Real-time logs -->
                </div>
            </div>

            <!-- QUICK ACTIONS & SITE SHORTCUTS -->
            <div class="card">
                <div class="card-header">
                    <span class="card-title">⚡ Actions Directes de Commandement</span>
                    <span class="card-badge" style="color:var(--cyan);">Raccourcis</span>
                </div>
                <div style="display:flex; flex-direction:column; gap:0.5rem;">
                    <button class="btn-secondary" style="justify-content:flex-start; padding:0.6rem;" onclick="switchNav('projects_hub')">
                        📁 <b>Chantiers & Documents :</b> Inspecter les 4 chantiers et télécharger les DCE
                    </button>
                    <button class="btn-secondary" style="justify-content:flex-start; padding:0.6rem;" onclick="switchNav('planning')">
                        📅 <b>Planning Gantt & Agenda :</b> Consulter le planning hebdomadaire
                    </button>
                    <button class="btn-secondary" style="justify-content:flex-start; padding:0.6rem;" onclick="switchNav('simulator')">
                        🛰️ <b>Watch Tower :</b> Lancer le simulateur 2D/3D et radar de chantier
                    </button>
                    <button class="btn-secondary" style="justify-content:flex-start; padding:0.6rem;" onclick="switchNav('sdp')">
                        💰 <b>Tableau Croisé Dynamique DQE :</b> Analyser les coûts et marges
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- 2. TAB COMPANY & CAISSE -->
    <div id="tab-company" class="tab-panel">
        <div class="card" style="margin-bottom:1rem;">
            <div class="card-header">
                <span class="card-title">🏢 Entreprise BTP — Trésorerie, Caisse & Santé Financière</span>
                <button class="btn-primary" onclick="simulatePaymentSituation()">💶 Simuler Paiement Situation (+65 000 €)</button>
            </div>
            <div class="grid-3" style="gap:1rem; margin-bottom:1rem;">
                <div style="background:var(--bg); padding:0.8rem; border-radius:8px; border:1px solid var(--border);">
                    <div style="font-size:0.72rem; color:var(--text-muted);">Solde Compte Courant :</div>
                    <div style="font-size:1.3rem; font-weight:900; color:var(--emerald);" id="company-treasury-big">485 200 €</div>
                    <div style="font-size:0.7rem; color:var(--text-muted); margin-top:0.2rem;">Ligne de crédit autorisée : 150 000 €</div>
                </div>
                <div style="background:var(--bg); padding:0.8rem; border-radius:8px; border:1px solid var(--border);">
                    <div style="font-size:0.72rem; color:var(--text-muted);">Encours Facturation Clients :</div>
                    <div style="font-size:1.3rem; font-weight:900; color:var(--cyan);">245 800 €</div>
                    <div style="font-size:0.7rem; color:var(--text-muted); margin-top:0.2rem;">Délai moyen de paiement : 38 jours</div>
                </div>
                <div style="background:var(--bg); padding:0.8rem; border-radius:8px; border:1px solid var(--border);">
                    <div style="font-size:0.72rem; color:var(--text-muted);">Dépenses Mensuelles Fixes :</div>
                    <div style="font-size:1.3rem; font-weight:900; color:var(--rose);">82 400 € / mois</div>
                    <div style="font-size:0.7rem; color:var(--text-muted); margin-top:0.2rem;">Masse salariale + Loyers + Crédits-baux</div>
                </div>
            </div>
            <div id="company-invoices-table"></div>
        </div>
    </div>

    <!-- 3. TAB PROJECTS HUB (CHANTIERS & DOCS) -->
    <div id="tab-projects_hub" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">📁 Chantiers, Dossiers Contractuels & Téléchargements CCTP/DICT</span>
                    <span class="card-badge" style="color:var(--cyan); margin-left:0.5rem;">4 Actifs | 2 Archivés</span>
                </div>
                <div style="display:flex; gap:0.4rem;">
                    <button class="btn-secondary active" id="btn-hub-active" style="font-size:0.75rem;" onclick="renderProjectsHub('active')">🟢 Chantiers en Cours (4)</button>
                    <button class="btn-secondary" id="btn-hub-archived" style="font-size:0.75rem;" onclick="renderProjectsHub('archived')">📦 Archivés & DOE (2)</button>
                </div>
            </div>
            <p style="font-size:0.76rem; color:var(--text-muted); margin-bottom:1rem;">
                💡 <b>Astuce :</b> Cliquez sur n'importe quel chantier pour ouvrir sa <b>fiche complète</b> avec décomposition financière détaillée, indicateurs de performance CPI/SPI, effectifs, engins affectés et <b>téléchargement direct des dossiers contractuels</b> (CCTP, BPU, Plans DWG, DICT, OS, DOE).
            </p>
            <div id="projects-hub-content" class="grid-2">
                <!-- Rendered by JS -->
            </div>
        </div>
    </div>

    <!-- 4. TAB PLANNING GANTT & AGENDA HEBDO/JOURNALIER -->
    <div id="tab-planning" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">📅 Planning Directeur Multi-Chantiers & Agenda Opérationnel</span>
                    <span class="card-badge" id="planning-view-badge" style="color:var(--emerald); margin-left:0.5rem;">Agenda Hebdomadaire S38</span>
                </div>
                <!-- Planning View Switcher Buttons -->
                <div style="display:flex; gap:0.35rem; flex-wrap:wrap;" id="planning-view-bar">
                    <button class="btn-secondary" id="btn-plan-gantt" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setPlanningViewMode('gantt', this)">📊 1. Gantt Multi-Chantiers</button>
                    <button class="btn-secondary active" id="btn-plan-agenda-week" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setPlanningViewMode('agenda_week', this)">📅 2. Agenda Hebdomadaire (S38)</button>
                    <button class="btn-secondary" id="btn-plan-agenda-day" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setPlanningViewMode('agenda_day', this)">📆 3. Agenda Journalier (Heure par Heure)</button>
                    <button class="btn-secondary" id="btn-plan-time" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setPlanningViewMode('time', this)">⏳ 4. Par Période (Mois / Trimestre)</button>
                    <button class="btn-secondary" id="btn-plan-team" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setPlanningViewMode('team', this)">👥 5. Par Équipe / Conducteur</button>
                    <button class="btn-secondary" id="btn-plan-machine" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setPlanningViewMode('machine', this)">🚜 6. Par Engin Affecté</button>
                </div>
            </div>

            <!-- Agenda Week Navigation Bar -->
            <div id="agenda-nav-header" style="display:flex; justify-content:space-between; align-items:center; background:var(--bg); border:1px solid var(--border); border-radius:6px; padding:0.5rem 0.8rem; margin-bottom:0.8rem;">
                <div style="display:flex; align-items:center; gap:0.5rem;">
                    <button class="btn-secondary" style="padding:0.2rem 0.5rem; font-size:0.72rem;" onclick="changeAgendaWeek(-1)">◀ Semaine Précédente</button>
                    <span style="font-weight:800; color:var(--cyan); font-size:0.85rem;" id="agenda-week-label">Semaine S38 : 15 - 21 Septembre 2026</span>
                    <button class="btn-secondary" style="padding:0.2rem 0.5rem; font-size:0.72rem;" onclick="changeAgendaWeek(1)">Semaine Suivante ▶</button>
                </div>
                <div style="display:flex; align-items:center; gap:0.4rem;">
                    <span class="card-badge" style="color:var(--emerald);">Aujourd'hui : Dimanche 20 Sept 2026</span>
                    <button class="btn-primary" style="font-size:0.7rem; padding:0.25rem 0.5rem;" onclick="alert('Ajout d’une nouvelle tâche dans l’agenda')">➕ Planifier Tâche / Équipe</button>
                </div>
            </div>

            <div style="overflow-x:auto;" id="planning-content-container">
                <!-- Rendered dynamically by JS -->
            </div>
        </div>
    </div>

    <!-- 5. TAB WATCH TOWER SIMULATEUR VRD 2D / 3D -->
    <div id="tab-simulator" class="tab-panel">
        <div class="grid-split-40-60">
            <!-- Left: Step-by-Step Decision Engine & Step Visual Window -->
            <div class="card">
                <div class="card-header">
                    <span class="card-title">🛰️ Watch Tower — Guide Pas-à-Pas</span>
                    <span class="card-badge" id="sim-scenario-badge" style="color:var(--cyan);">Scénario 1</span>
                </div>
                <div style="margin-bottom:0.8rem;">
                    <label class="input-label">Choisir le Scénario Classique VRD :</label>
                    <select class="input-field" style="width:100%;" id="sim-scenario-select" onchange="loadScenario(this.value)">
                        <option value="scen_tranchee_vrd">1. Tranchée Réseau Assainissement sous Nappe & Gaz (ZAC Sète)</option>
                        <option value="scen_giratoire_enrobes">2. Terrassement, Plateforme GNT & Enrobés Giratoire (RD906 Alès)</option>
                        <option value="scen_bordures_trottoir">3. Pose de Bordures T2 & Béton Désactivé (Pézenas / MTP)</option>
                    </select>
                </div>

                <div class="step-window-card" style="background:#040711; border:1px solid var(--border); border-radius:8px; padding:0.6rem; margin-bottom:0.8rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                        <span style="font-size:0.75rem; font-weight:700; color:var(--cyan);" id="step-window-title">Fenêtre Visuelle Étape</span>
                        <span class="card-badge" id="step-window-badge" style="color:var(--emerald);">Simulation Active</span>
                    </div>
                    <div style="height:140px; width:100%; position:relative;">
                        <canvas id="step-visual-canvas" width="400" height="140" style="width:100%; height:100%; display:block; border-radius:4px;"></canvas>
                    </div>
                </div>

                <div id="sim-mission-box" style="display:flex; flex-direction:column; gap:0.75rem;">
                    <!-- Rendered by JS -->
                </div>
            </div>

            <!-- Right: 2D Vue Satellite & 3D Environnement Théorique Grille XYZ -->
            <div class="card">
                <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                    <span class="card-title">🗺️ Visualisation Chantier In-Situ</span>
                    <div style="display:flex; gap:0.35rem; align-items:center; flex-wrap:wrap;">
                        <button class="btn-secondary active" id="btn-view-radar" style="font-size:0.7rem; padding:0.25rem 0.6rem;" onclick="setSimulatorViewMode('radar')">🛰️ 2D : Vue Satellite</button>
                        <button class="btn-secondary" id="btn-view-3dcube" style="font-size:0.7rem; padding:0.25rem 0.6rem;" onclick="setSimulatorViewMode('3dcube')">🧊 3D : Cube Géotechnique</button>
                        <button class="btn-secondary" id="btn-radar-mode-toggle" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="toggleRadarLiveMode()">🔄 Mode Statique / Live</button>
                    </div>
                </div>

                <!-- 3D Camera Controls & Presets (Displayed in 3D Mode) -->
                <div id="sim-3d-toolbar" style="display:none; background:var(--bg); border:1px solid var(--border); border-radius:6px; padding:0.4rem 0.6rem; margin-bottom:0.6rem; font-size:0.72rem; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.4rem;">
                    <div style="display:flex; align-items:center; gap:0.3rem; flex-wrap:wrap;">
                        <span style="font-weight:700; color:var(--cyan);">Caméra 3D :</span>
                        <button class="btn-secondary" style="padding:0.15rem 0.4rem; font-size:0.68rem;" onclick="rotate3D(-15, 0)">⟲ Gauche</button>
                        <button class="btn-secondary" style="padding:0.15rem 0.4rem; font-size:0.68rem;" onclick="rotate3D(15, 0)">⟳ Droite</button>
                        <button class="btn-secondary" style="padding:0.15rem 0.4rem; font-size:0.68rem;" onclick="rotate3D(0, 10)">🔼 Haut</button>
                        <button class="btn-secondary" style="padding:0.15rem 0.4rem; font-size:0.68rem;" onclick="rotate3D(0, -10)">🔽 Bas</button>
                        <button class="btn-secondary" style="padding:0.15rem 0.4rem; font-size:0.68rem;" onclick="zoom3D(1.15)">🔍 +</button>
                        <button class="btn-secondary" style="padding:0.15rem 0.4rem; font-size:0.68rem;" onclick="zoom3D(0.85)">🔍 -</button>
                    </div>
                    <div style="display:flex; align-items:center; gap:0.3rem; flex-wrap:wrap;">
                        <span style="font-weight:700; color:var(--text-muted);">Vues :</span>
                        <button class="btn-secondary" style="padding:0.15rem 0.45rem; font-size:0.68rem;" onclick="set3DPreset('iso')">📐 Isométrique 3D</button>
                        <button class="btn-secondary" style="padding:0.15rem 0.45rem; font-size:0.68rem;" onclick="set3DPreset('top')">🗺️ Dessus (Plan)</button>
                        <button class="btn-secondary" style="padding:0.15rem 0.45rem; font-size:0.68rem;" onclick="set3DPreset('section')">📏 Coupe Profil Z</button>
                        <button class="btn-secondary" style="padding:0.15rem 0.45rem; font-size:0.68rem;" onclick="set3DPreset('reset')">🎯 Reset</button>
                    </div>
                </div>

                <div class="step-canvas-wrap" style="height:440px; position:relative; background:#040711; border:1px solid var(--border); border-radius:8px; overflow:hidden;">
                    <canvas id="watchtower-radar-canvas" style="width:100%; height:100%; cursor:grab;"></canvas>
                    <div id="sim-canvas-overlay-badge" style="position:absolute; top:8px; left:8px; background:rgba(15,23,42,0.85); border:1px solid var(--border); padding:0.25rem 0.5rem; border-radius:4px; font-size:0.68rem; font-family:var(--font-mono); color:var(--cyan);">
                        🛰️ Vue Satellite & Télémétrie RGF93 CC43
                    </div>
                </div>

                <div style="display:flex; align-items:center; justify-content:space-between; margin-top:0.75rem; font-size:0.72rem; color:var(--text-muted); flex-wrap:wrap; gap:0.4rem;">
                    <span>🟢 Compagnons & Exosquelettes GPS</span>
                    <span>🚜 Pelles & Engins Lourds</span>
                    <span>🛸 Drone LiDAR Survol Z=+10m</span>
                    <span>🔴 Danger Gaz MPB & Élec 20kV</span>
                </div>

                <!-- Dynamic Theoretical XYZ Placement Table for Selected Task -->
                <div style="margin-top:0.8rem; background:var(--bg); border:1px solid var(--border); border-radius:8px; padding:0.6rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                        <span style="font-size:0.75rem; font-weight:700; color:var(--cyan);">📊 Emplacements Théoriques selon Planning & Tâche (Grille XYZ) :</span>
                        <span class="card-badge" id="sim-3d-task-badge" style="color:var(--emerald);">Tâche Synchronisée</span>
                    </div>
                    <div style="overflow-x:auto;">
                        <table style="width:100%; border-collapse:collapse; font-size:0.7rem; font-family:var(--font-mono);" id="sim-3d-coords-table">
                            <!-- Populated dynamically by JS -->
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 6. TAB FLOTTE ENGINS & PARC MATÉRIEL -->
    <div id="tab-fleet" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">🚜 Flotte d'Engins, Véhicules, Drones & Outillage Lourd</span>
                    <span class="card-badge" style="color:var(--amber); margin-left:0.5rem;">14 Machines Répertoriées</span>
                </div>
                <div style="display:flex; gap:0.4rem; flex-wrap:wrap;">
                    <button class="btn-secondary active" onclick="filterFleet('all', this)" style="font-size:0.72rem;">Tous (14)</button>
                    <button class="btn-secondary" onclick="filterFleet('heavy', this)" style="font-size:0.72rem;">🚜 Pelles & Lourds</button>
                    <button class="btn-secondary" onclick="filterFleet('compact', this)" style="font-size:0.72rem;">🔨 Compactage & Enrobés</button>
                    <button class="btn-secondary" onclick="filterFleet('truck', this)" style="font-size:0.72rem;">🚛 Camions 8x4</button>
                    <button class="btn-secondary" onclick="filterFleet('drone', this)" style="font-size:0.72rem;">🛸 Drones & High-Tech</button>
                    <button class="btn-primary" style="font-size:0.72rem;" onclick="openAddVehicleModal()">➕ Ajouter un Engin</button>
                </div>
            </div>
            <p style="font-size:0.76rem; color:var(--text-muted); margin-bottom:1rem;">
                💡 Cliquez sur n'importe quel engin pour afficher sa <b>fiche technique détaillée avec illustration technique haute précision</b>, contrôles VGP, niveau de carburant, heures moteur et options de ravitaillement.
            </p>
            <div id="fleet-items-grid" class="grid-3" style="gap:1rem;">
                <!-- Populated by JS -->
            </div>
        </div>
    </div>

    <!-- 7. TAB CATALOGUE OUTILS & MATÉRIAUX -->
    <div id="tab-catalog" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">🛒 Matériaux de Chantier & Outillage Standard BTP</span>
                    <span class="card-badge" style="color:var(--emerald); margin-left:0.5rem;">VRD & Travaux Publics</span>
                </div>
                <div style="display:flex; gap:0.35rem; flex-wrap:wrap;" id="catalog-filter-bar">
                    <button class="btn-secondary active" onclick="filterCatalog('materials', this)" style="font-size:0.72rem;">🧱 Matériaux & Fournitures VRD</button>
                    <button class="btn-secondary" onclick="filterCatalog('all', this)" style="font-size:0.72rem;">🔧 Tous les Outils Standards</button>
                    <button class="btn-secondary" onclick="filterCatalog('terrassement', this)" style="font-size:0.72rem;">🚜 Terrassement</button>
                    <button class="btn-secondary" onclick="filterCatalog('compactage', this)" style="font-size:0.72rem;">🔨 Compactage</button>
                    <button class="btn-secondary" onclick="filterCatalog('sciage', this)" style="font-size:0.72rem;">⚙️ Sciage & Découpe</button>
                    <button class="btn-secondary" onclick="filterCatalog('pose_bordures', this)" style="font-size:0.72rem;">📐 Pose de Bordures</button>
                    <button class="btn-secondary" onclick="filterCatalog('topographie', this)" style="font-size:0.72rem;">🎯 Topo & Lasers</button>
                    <button class="btn-secondary" onclick="filterCatalog('securite', this)" style="font-size:0.72rem;">🦺 Sécurité & EPI</button>
                </div>
            </div>
            <p style="font-size:0.76rem; color:var(--text-muted); margin-bottom:1rem;">
                📦 <b>Indicateurs de Stock Visuels :</b> <span class="stock-badge-in">📦 En Stock</span> | <span class="stock-badge-transit">🚚 En cours d'acheminement</span> | <span class="stock-badge-out"><span class="stock-dot-red"></span> Rupture de Stock</span>. Cliquez sur un article pour voir son <b>illustration technique et modèle 3D vectoriel</b>.
            </p>
            <div id="catalog-items-grid" class="grid-3" style="gap:1rem;">
                <!-- Populated by JS -->
            </div>
        </div>
    </div>

    <!-- 8. TAB ORGANIGRAMME RH -->
    <div id="tab-hr" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">👷 Organigramme RH, Compétences & Habilitations AIPR</span>
                <span class="card-badge" style="color:var(--cyan);">12 Collaborateurs</span>
            </div>
            <div id="hr-tree-container" style="display:flex; flex-direction:column; gap:1.2rem;">
                <!-- Populated by JS -->
            </div>
        </div>
    </div>

    <!-- 9. TAB SIGNALÉTIQUE OPBTP -->
    <div id="tab-opbtp" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">🦺 Sélecteur Visuel & Recommandations de Signalisation Temporaire (OPBTP / SETRA)</span>
                <span class="card-badge" style="color:var(--amber);">Conforme Manuel des Panneaux</span>
            </div>
            <div class="grid-split-40-60">
                <!-- 3-Step Simple Selector Form -->
                <div style="background:var(--bg); padding:1rem; border-radius:8px; border:1px solid var(--border);">
                    <div style="font-weight:800; color:var(--cyan); font-size:0.85rem; margin-bottom:0.8rem;">
                        📋 Configuration du Chantier en 3 Étapes Simples :
                    </div>

                    <div class="input-group">
                        <label class="input-label">1. Type de Voie & Vitesse :</label>
                        <select class="input-field" id="opbtp-road-type" onchange="calculateSignage()">
                            <option value="bidir_hors_agglo_80">Route bidirectionnelle rase campagne (80 km/h)</option>
                            <option value="urbain_50">Voie urbaine standard (50 km/h)</option>
                            <option value="centre_ville_30">Zone 30 / Centre ancien étroit (30 km/h)</option>
                            <option value="2x2_110">Route à chaussées séparées 2x2 voies (110 km/h)</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label class="input-label">2. Nature des Travaux :</label>
                        <select class="input-field" id="opbtp-work-type" onchange="calculateSignage()">
                            <option value="tranchee_long">Tranchée longitudinale VRD sous chaussée</option>
                            <option value="giratoire">Création / Réfection de giratoire</option>
                            <option value="trottoir_bordure">Travaux de trottoir / bordures hors voie circulée</option>
                            <option value="enrobe_rabotage">Rabotage & Application d'enrobés pleines voies</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label class="input-label">3. Mode de Gestion du Trafic :</label>
                        <select class="input-field" id="opbtp-traffic-mode" onchange="calculateSignage()">
                            <option value="alternat_feux">Alternat par feux tricolores temporaires (KR11j)</option>
                            <option value="alternat_piquets">Alternat manuel par piquets K10</option>
                            <option value="deviation">Déviation totale avec arrêté municipal</option>
                            <option value="empietement">Empiètement léger avec maintien des 2 sens</option>
                        </select>
                    </div>

                    <div id="opbtp-calc-results" style="background:var(--bg-card); padding:0.8rem; border-radius:6px; border:1px solid var(--border); font-size:0.75rem; margin-top:0.8rem; line-height:1.6;">
                        <!-- Calculated automatically -->
                    </div>
                </div>

                <!-- Dynamic Visual 2D Road Canvas Preview -->
                <div style="background:#040711; border:1px solid var(--border); border-radius:8px; padding:0.8rem; display:flex; flex-direction:column; gap:0.5rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:0.8rem; font-weight:800; color:var(--cyan);">📐 Plan de Phasage & Schéma d'Implantation Réglementaire</span>
                        <span class="card-badge" style="color:var(--emerald);">SETRA / OPBTP</span>
                    </div>
                    <div style="height:340px; width:100%; position:relative;">
                        <canvas id="opbtp-signage-canvas" width="600" height="340" style="width:100%; height:100%; display:block; background:#090d16; border-radius:6px;"></canvas>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:0.7rem; color:var(--text-muted);">
                        <span>AK5 &rarr; B14 &rarr; KR11j &rarr; K5a/K8</span>
                        <span>Distance calculée automatique selon V85</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 10. TAB SÉCURITÉ & PRÉVENTION AIPR -->
    <div id="tab-safety" class="tab-panel">
        <div class="card" style="margin-bottom:1rem; border-left:4px solid var(--rose);">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">🦺 Guide Opérationnel de Sécurité & Prévention BTP (AIPR & Normes OPBTP)</span>
                    <span class="card-badge" style="color:var(--rose); margin-left:0.5rem;">Zéro Accident Mortel</span>
                </div>
                <div style="display:flex; gap:0.4rem;">
                    <button class="btn-primary" style="font-size:0.72rem; padding:0.35rem 0.65rem; background:#dc2626; border-color:#ef4444;" onclick="alert('🚨 PROTOCOLE URGENCE CHANTIER DÉCLENCHÉ :\\n1. Stopper tous les engins immédiatement\\n2. Périmètre de sécurité 100m\\n3. Appel SAMU (15) ou Pompiers (18)\\n4. Informer le Conducteur de Travaux et CSPS.')">
                        🚨 Déclencher Procédure d'Urgence
                    </button>
                </div>
            </div>
            <p style="font-size:0.78rem; color:var(--text-muted); line-height:1.6; margin-top:0.3rem;">
                Ce guide rassemble l'ensemble des règles obligatoires et des recommandations OPPBTP / INRS applicables sur tous nos chantiers de Voirie, Réseaux Divers et Terrassement.
            </p>
        </div>

        <div class="grid-3" style="gap:1rem; margin-bottom:1rem;">
            <!-- 1. Distances DLA -->
            <div class="card" style="border-top:3px solid var(--amber);">
                <div style="font-weight:800; font-size:0.88rem; color:var(--amber); margin-bottom:0.6rem;">⚡ 1. Distances de Sécurité DLA & AIPR</div>
                <ul style="font-size:0.75rem; color:var(--text-muted); line-height:1.7; list-style:inside;">
                    <li><b>Lignes Aériennes &lt; 50 kV (HTA/BT) :</b> Distance Limite d'Approche (DLA) = <b>3,00 mètres</b>.</li>
                    <li><b>Lignes Aériennes &ge; 50 kV (HTB) :</b> DLA = <b>5,00 mètres</b> infranchissable.</li>
                    <li><b>Fuseaux d'Incertitude Cartographique :</b>
                        <br>&bull; <i>Classe A :</i> &plusmn; 40 cm (rigide &plusmn; 10 cm).
                        <br>&bull; <i>Classe B :</i> &plusmn; 1,50 m (investigations requises).
                        <br>&bull; <i>Classe C :</i> &gt; 1,50 m (tranchées de reconnaissance obligatoires).
                    </li>
                    <li><b>Approche &lt; 50 cm Réseau Gaz :</b> Terrassement mécanique à godet denté strictement interdit &rarr; Terrassement manuel ou aspiratrice.</li>
                </ul>
            </div>

            <!-- 2. Blindage -->
            <div class="card" style="border-top:3px solid var(--cyan);">
                <div style="font-weight:800; font-size:0.88rem; color:var(--cyan); margin-bottom:0.6rem;">🛡️ 2. Blindage Obligatoire des Fouilles</div>
                <ul style="font-size:0.75rem; color:var(--text-muted); line-height:1.7; list-style:inside;">
                    <li><b>Règle R.4534-24 :</b> Blindage obligatoire pour toute tranchée de <b>profondeur &gt; 1,30 m</b> et de largeur &le; aux 2/3 de la profondeur.</li>
                    <li><b>Types de Blindage Homologués :</b>
                        <br>&bull; <i>Caissons coulissants acier :</i> prof. jusqu'à 4,50 m.
                        <br>&bull; <i>Blindage léger alu (Titan) :</i> réseaux urbains &lt; 2,50 m.
                        <br>&bull; <i>Talutage naturel :</i> pente &le; 1/1 (45°) si emprise suffisante.
                    </li>
                    <li><b>Interdiction d'Accès :</b> Ne jamais descendre au fond d'une fouille non blindée.</li>
                </ul>
            </div>

            <!-- 3. Pack EPI -->
            <div class="card" style="border-top:3px solid var(--emerald);">
                <div style="font-weight:800; font-size:0.88rem; color:var(--emerald); margin-bottom:0.6rem;">🦺 3. Pack EPI & Protections Individuelles</div>
                <ul style="font-size:0.75rem; color:var(--text-muted); line-height:1.7; list-style:inside;">
                    <li><b>Casque de Chantier (NF EN 397) :</b> Port de la jugulaire obligatoire en bordure de tranchée et sous la flèche d'engin.</li>
                    <li><b>Haute Visibilité (EN ISO 20471) :</b> Gilet ou parka Classe 2 minimum, Classe 3 de nuit.</li>
                    <li><b>Chaussures de Sécurité (S3 SRC) :</b> Semelle anti-perforation acier/composite et embout 200 Joules.</li>
                    <li><b>Gants de Manutention (EN 388) :</b> Résistance à la coupure niveau D ou F pour pose de bordures et tuyaux.</li>
                    <li><b>Protections Auditives :</b> Bouchons SNR 28dB lors du découpage de chaussée.</li>
                </ul>
            </div>

            <!-- 4. Angles Morts -->
            <div class="card" style="border-top:3px solid var(--rose);">
                <div style="font-weight:800; font-size:0.88rem; color:var(--rose); margin-bottom:0.6rem;">🚜 4. Angles Morts & Trafic Engins</div>
                <ul style="font-size:0.75rem; color:var(--text-muted); line-height:1.7; list-style:inside;">
                    <li><b>Rayon de Rotation Pelle :</b> Périmètre d'exclusion de <b>10 mètres</b> autour de la tourelle des pelles &ge; 14T.</li>
                    <li><b>Zone de Recul Camions 8x4 :</b> Ne jamais stationner à l'arrière d'un camion benne en manœuvre.</li>
                    <li><b>Contact Visuel Pilote :</b> Si vous ne voyez pas les yeux du conducteur dans son rétroviseur, il ne vous voit pas !</li>
                    <li><b>Bips de Recul & Caméras 360° :</b> Vérification quotidienne du bon fonctionnement.</li>
                </ul>
            </div>

            <!-- 5. Enrobés Chauds -->
            <div class="card" style="border-top:3px solid var(--purple);">
                <div style="font-weight:800; font-size:0.88rem; color:var(--purple); margin-bottom:0.6rem;">🧪 5. Enrobés Chauds & Risques Chimiques</div>
                <ul style="font-size:0.75rem; color:var(--text-muted); line-height:1.7; list-style:inside;">
                    <li><b>Température d'Application (150°C - 170°C) :</b> Risque majeur de brûlures thermiques au 3e degré. Gants cuir manchettes longues obligatoires.</li>
                    <li><b>Émanations d'HAP & Bitume :</b> Se placer systématiquement au vent du finisseur. Masque A2P3 en espace confiné.</li>
                    <li><b>Produits de Collage & Émulsion :</b> Port de lunettes étanches lors du répandage à la lance. Rince-œil portatif disponible dans le camion atelier.</li>
                </ul>
            </div>

            <!-- 6. Contacts Urgence -->
            <div class="card" style="border-top:3px solid #dc2626;">
                <div style="font-weight:800; font-size:0.88rem; color:#ef4444; margin-bottom:0.6rem;">📞 6. Procédures d'Urgence & Contacts Vitaux</div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; font-size:0.75rem;">
                    <div style="background:var(--bg); padding:0.5rem; border-radius:6px; border:1px solid var(--border);">
                        <b>🚑 SAMU :</b> <span style="color:#ef4444; font-weight:800;">15</span><br>
                        <b>🚒 Pompiers :</b> <span style="color:#ef4444; font-weight:800;">18</span><br>
                        <b>📱 Urgence UE :</b> <span style="color:#ef4444; font-weight:800;">112</span>
                    </div>
                    <div style="background:var(--bg); padding:0.5rem; border-radius:6px; border:1px solid var(--border);">
                        <b>🔥 Urgence Gaz :</b> <span style="color:var(--amber); font-weight:800;">0 800 47 33 33</span><br>
                        <b>⚡ Enedis Dépannage :</b> <span style="color:var(--cyan); font-weight:800;">09 72 67 50 34</span><br>
                        <b>💧 Urgence Eau :</b> <span style="color:var(--purple); font-weight:800;">04 67 12 34 56</span>
                    </div>
                </div>
                <p style="font-size:0.7rem; color:var(--text-muted); margin-top:0.4rem;">
                    <b>Protocole PAS :</b> Protéger (couper contact, baliser) &rarr; Alerter (préciser PK / adresse exacte) &rarr; Secourir (SST uniquement).
                </p>
            </div>
        </div>
    </div>

    <!-- 11. TAB RAPPORT JOURNALIER (RDC) -->
    <div id="tab-rdc" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">📋 Rapport Quotidien de Chantier (RDC Automatique)</span>
                <button class="btn-primary" onclick="exportRDC()">📄 Exporter PDF Signé</button>
            </div>
            <div id="rdc-preview-container" style="background:var(--bg); border:1px solid var(--border); border-radius:8px; padding:1.2rem; font-family:var(--font-mono); font-size:0.75rem; line-height:1.7;">
                <!-- Rendered by JS -->
            </div>
        </div>
    </div>

    <!-- 12. TAB COMPAGNON MOBILE -->
    <div id="tab-compagnon_mobile" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">📱 Assistant Terrain Compagnon BTP</span>
                <span class="card-badge" style="color:var(--emerald);">Mode Chantier Actif</span>
            </div>
            <div class="grid-3" style="gap:1rem;">
                <div class="project-card" style="cursor:pointer;" onclick="alert('Quart d’heure sécurité validé pour aujourd’hui (EPI vérifiés). Pointage 8h00 enregistré.')">
                    <div style="font-size:2rem; margin-bottom:0.5rem;">🦺</div>
                    <div style="font-weight:800; font-size:0.9rem;">Quart d'Heure Sécurité</div>
                    <p style="font-size:0.72rem; color:var(--text-muted); margin-top:0.3rem;">Valider le pointage EPI et les consignes du jour.</p>
                </div>
                <div class="project-card" style="cursor:pointer;" onclick="triggerPhotoUpload()">
                    <div style="font-size:2rem; margin-bottom:0.5rem;">📸</div>
                    <div style="font-weight:800; font-size:0.9rem;">Photo Témoin & Aléa</div>
                    <p style="font-size:0.72rem; color:var(--text-muted); margin-top:0.3rem;">Prendre une photo géoréférencée pour le RDC.</p>
                </div>
                <div class="project-card" style="cursor:pointer;" onclick="switchNav('opbtp')">
                    <div style="font-size:2rem; margin-bottom:0.5rem;">📐</div>
                    <div style="font-weight:800; font-size:0.9rem;">Balisage de Voie</div>
                    <p style="font-size:0.72rem; color:var(--text-muted); margin-top:0.3rem;">Consulter le schéma d'implantation de panneaux.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- 13. TAB GRAPHE OBSIDIAN -->
    <div id="tab-obsidian" class="tab-panel">
        <div class="card" style="margin-bottom:0.8rem;">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">🕸️ Graphe de Connaissances BTP — Multi-Heuristiques & Arborescences</span>
                    <span class="card-badge" id="obsidian-heuristic-badge" style="color:var(--cyan); margin-left:0.5rem;">Heuristique 1 : Thématique</span>
                </div>
                <!-- Multiple Heuristics Switcher -->
                <div style="display:flex; gap:0.35rem; flex-wrap:wrap;">
                    <button class="btn-secondary active" id="btn-heur-domains" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setObsidianHeuristic('domains', this)">🏷️ Heuristique 1 : Thématique / Domaines</button>
                    <button class="btn-secondary" id="btn-heur-chrono" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setObsidianHeuristic('chrono', this)">⏳ Heuristique 2 : Cycle de Vie Chantier</button>
                    <button class="btn-secondary" id="btn-heur-tree" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setObsidianHeuristic('tree', this)">🌳 Heuristique 3 : Arbre Décisionnel</button>
                    <button class="btn-secondary" id="btn-heur-risk" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setObsidianHeuristic('risk', this)">⚠️ Heuristique 4 : Matrice des Risques</button>
                </div>
            </div>
        </div>

        <div class="obsidian-layout">
            <div class="obsidian-graph-container" id="obsidian-graph-viewport">
                <div class="obsidian-hud">
                    <div style="display:flex; align-items:center; gap:0.5rem; background:rgba(15,23,42,0.9); padding:0.4rem 0.8rem; border-radius:8px; border:1px solid var(--border);">
                        <span style="font-size:0.85rem;">🕸️</span>
                        <input type="text" id="obsidian-search" placeholder="Rechercher note, tag..." oninput="onObsidianSearch(this.value)" style="background:transparent; border:none; color:#fff; font-size:0.8rem; outline:none; width:160px;">
                    </div>
                    <div style="display:flex; align-items:center; gap:0.4rem;">
                        <button class="btn-secondary" style="font-size:0.72rem; padding:0.35rem 0.65rem;" onclick="resetObsidianView()">🔄 Recentrer</button>
                        <button class="btn-primary" style="font-size:0.72rem; padding:0.35rem 0.65rem;" onclick="exportObsidianVault()">📥 Exporter Vault</button>
                    </div>
                </div>
                <canvas id="obsidian-canvas" style="width:100%; height:100%; display:block; cursor:grab;"></canvas>
            </div>

            <div class="obsidian-drawer">
                <div>
                    <span class="card-badge" id="obsidian-note-group-badge" style="margin-bottom:0.4rem; display:inline-block;">Rapport Maître</span>
                    <h2 id="obsidian-note-title" style="font-size:1.15rem; font-weight:800; color:var(--text-main);">Note Obsidian</h2>
                </div>
                <div id="obsidian-frontmatter-view" style="background:#040711; padding:0.6rem; border-radius:6px; border:1px solid var(--border); font-family:var(--font-mono); font-size:0.68rem; color:#94a3b8; line-height:1.5;"></div>
                <div id="obsidian-note-body" style="font-size:0.8rem; color:#cbd5e1; line-height:1.6; border-top:1px solid var(--border); padding-top:0.8rem;"></div>
                <div style="border-top:1px solid var(--border); padding-top:0.6rem; font-size:0.75rem;">
                    <div style="font-weight:700; color:var(--text-main); margin-bottom:0.3rem;">🔗 Rétro-liens (Backlinks) : <span id="obsidian-backlinks-count" style="color:var(--purple);">0</span></div>
                    <div id="obsidian-backlinks-list" style="display:flex; flex-wrap:wrap; gap:0.3rem;"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- 14. TAB SCHÉMAS & FORMULES INTERACTIVES -->
    <div id="tab-schemas" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">📐 Formules Fondamentales & Schémas Techniques A &agrave; Z</span>
                <span class="card-badge" style="color:var(--emerald);">Calculateurs Pédagogiques Actifs</span>
            </div>
            
            <div class="grid-4" style="gap:0.6rem; margin-bottom:1rem;" id="formula-selector-bar">
                <button class="btn-secondary active" onclick="updateFormulaCalculator('dynaplaque', this)">🪨 1. Dynaplaque (EV2/EV1)</button>
                <button class="btn-secondary" onclick="updateFormulaCalculator('pente', this)">📐 2. Pente & Nivellement</button>
                <button class="btn-secondary" onclick="updateFormulaCalculator('caquot', this)">💧 3. Débit Caquot Pluvial</button>
                <button class="btn-secondary" onclick="updateFormulaCalculator('foisonnement', this)">🚛 4. Foisonnement Camions</button>
            </div>

            <div class="grid-split-60-40">
                <!-- Interactive Calculator Box -->
                <div id="formula-calc-panel" style="background:var(--bg); padding:1rem; border-radius:8px; border:1px solid var(--border);">
                    <!-- Rendered by JS -->
                </div>

                <!-- Pedagogical Schematics & Rules Explanation -->
                <div id="formula-guide-panel" style="background:var(--bg); padding:1rem; border-radius:8px; border:1px solid var(--border); font-size:0.76rem; line-height:1.7;">
                    <!-- Rendered by JS -->
                </div>
            </div>
        </div>
    </div>

    <!-- 15. TAB 28 SDP DEVIS & TABLEAU CROISÉ DYNAMIQUE DQE -->
    <div id="tab-sdp" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">💰 Base des 28 Sous-Détails de Prix (SDP) & Tableau Croisé Dynamique DQE Entreprise TP</span>
                    <span class="card-badge" id="sdp-mode-badge" style="color:var(--emerald); margin-left:0.5rem;">TCD DQE Multi-Lots</span>
                </div>
                <div style="display:flex; gap:0.4rem; flex-wrap:wrap;">
                    <button class="btn-secondary" id="btn-sdp-mode-base" style="font-size:0.75rem;" onclick="setSDPViewMode('base', this)">📋 1. Base 28 SDP & Paramètres K</button>
                    <button class="btn-secondary active" id="btn-sdp-mode-dqe" style="font-size:0.75rem;" onclick="setSDPViewMode('dqe_tcd', this)">📊 2. Tableau Croisé Dynamique DQE</button>
                    <button class="btn-primary" style="font-size:0.75rem;" onclick="exportDQEtoCSV()">📥 Exporter TCD (CSV / Excel)</button>
                    <button class="btn-secondary" style="font-size:0.75rem;" onclick="printDQESummary()">🖨️ Imprimer DQE</button>
                </div>
            </div>

            <!-- View 1: 28 SDP Base Panel -->
            <div id="sdp-base-view-container" style="display:none;">
                <div style="background:rgba(6,182,212,0.08); border:1px solid rgba(6,182,212,0.3); border-radius:8px; padding:1rem; margin-bottom:1rem; font-size:0.78rem; line-height:1.7;">
                    <div style="font-weight:800; font-size:0.9rem; color:var(--cyan); margin-bottom:0.4rem;">
                        📚 Comprendre le Sous-Détail de Prix (SDP) en Travaux Publics :
                    </div>
                    <p style="color:var(--text-main); margin-bottom:0.6rem;">
                        Un <b>Sous-Détail de Prix (SDP)</b> est la décomposition analytique exacte du coût d'une unité d'ouvrage. Formule fondamentale : <b>PV HT = DS × K</b>.
                    </p>
                    <div class="grid-4" style="gap:0.6rem; margin-top:0.6rem;">
                        <div style="background:var(--bg); padding:0.6rem; border-radius:6px; border:1px solid var(--border);">
                            <b style="color:var(--amber);">1. Déboursé Sec (DS)</b><br>
                            MAT + MO + Engins + Sous-traitance.
                        </div>
                        <div style="background:var(--bg); padding:0.6rem; border-radius:6px; border:1px solid var(--border);">
                            <b style="color:var(--cyan);">2. Frais de Chantier (FC)</b><br>
                            Installation, géomètre, balisage (6% à 10%).
                        </div>
                        <div style="background:var(--bg); padding:0.6rem; border-radius:6px; border:1px solid var(--border);">
                            <b style="color:var(--purple);">3. Frais Généraux (FG)</b><br>
                            Siège, direction, assurances (12% à 16%).
                        </div>
                        <div style="background:var(--bg); padding:0.6rem; border-radius:6px; border:1px solid var(--border);">
                            <b style="color:var(--emerald);">4. Coefficient K</b><br>
                            Intègre FC, FG, aléas et marge nette.
                        </div>
                    </div>
                </div>

                <!-- Parameters Bar -->
                <div style="margin-bottom:1rem; display:flex; gap:1.2rem; align-items:center; flex-wrap:wrap; font-size:0.75rem; background:var(--bg); padding:0.8rem; border-radius:6px; border:1px solid var(--border);">
                    <span><b>Taux MO :</b> <input type="number" id="sdp-tx-mo" value="38.5" style="width:60px; padding:3px; border-radius:4px; border:1px solid var(--border); background:var(--bg-card); color:var(--text-main);" onchange="renderSDPTable()"> €/h</span>
                    <span><b>GNR :</b> <input type="number" id="sdp-tx-gnr" value="1.45" step="0.05" style="width:60px; padding:3px; border-radius:4px; border:1px solid var(--border); background:var(--bg-card); color:var(--text-main);" onchange="renderSDPTable()"> €/L</span>
                    <span><b>FG :</b> <input type="number" id="sdp-tx-fg" value="14" style="width:50px; padding:3px; border-radius:4px; border:1px solid var(--border); background:var(--bg-card); color:var(--text-main);" onchange="renderSDPTable()"> %</span>
                    <span><b>Marge Nette :</b> <input type="number" id="sdp-tx-marge" value="12" style="width:50px; padding:3px; border-radius:4px; border:1px solid var(--border); background:var(--bg-card); color:var(--text-main);" onchange="renderSDPTable()"> %</span>
                    <button class="btn-primary" style="margin-left:auto; font-size:0.72rem;" onclick="renderSDPTable()">🔄 Recalculer les 28 Prix</button>
                </div>

                <div style="overflow-x:auto;">
                    <table style="width:100%; border-collapse:collapse; font-size:0.75rem;" id="sdp-table-content"></table>
                </div>
            </div>

            <!-- View 2: Tableau Croisé Dynamique DQE Multi-Lots -->
            <div id="sdp-dqe-view-container">
                <!-- TCD Filter & Dimensions Controls Bar -->
                <div style="background:var(--bg); border:1px solid var(--border); border-radius:8px; padding:0.8rem; margin-bottom:1rem; display:flex; flex-wrap:wrap; gap:1rem; align-items:center; font-size:0.75rem;">
                    <div>
                        <label class="input-label" style="display:inline-block; margin-right:0.3rem;">Chantier :</label>
                        <select class="input-field" id="tcd-filter-project" style="width:200px; display:inline-block;" onchange="renderDQEPivotTable()">
                            <option value="ALL">Tous les Chantiers (Portfolio Global)</option>
                            <option value="projet_ales">Giratoire RD906 Alès</option>
                            <option value="projet_sete">ZAC Littoral Sète</option>
                            <option value="projet_pezenas">Centre Ancien Pézenas</option>
                            <option value="projet_montpellier">Voie Verte Montpellier</option>
                        </select>
                    </div>

                    <div>
                        <label class="input-label" style="display:inline-block; margin-right:0.3rem;">Regroupement Principal (Lignes) :</label>
                        <select class="input-field" id="tcd-grouping-dim" style="width:180px; display:inline-block;" onchange="renderDQEPivotTable()">
                            <option value="lot">Par Lot Technique (Terrass., Assain., Voirie...)</option>
                            <option value="project">Par Chantier / Projet</option>
                            <option value="statut">Par Statut d'Exécution</option>
                        </select>
                    </div>

                    <div>
                        <label class="input-label" style="display:inline-block; margin-right:0.3rem;">Recherche Ouvrage :</label>
                        <input type="text" id="tcd-search-kw" placeholder="Filtrer bordure, tuyau, enrobé..." class="input-field" style="width:180px; display:inline-block;" oninput="renderDQEPivotTable()">
                    </div>

                    <div style="margin-left:auto; display:flex; gap:0.5rem; align-items:center;">
                        <span class="card-badge" id="tcd-stats-badge" style="color:var(--emerald);">25 Ouvrages DQE</span>
                    </div>
                </div>

                <!-- TCD Summary KPI Cards -->
                <div class="grid-4" style="gap:0.8rem; margin-bottom:1rem;" id="tcd-kpi-summary-cards">
                    <!-- Populated dynamically -->
                </div>

                <!-- Interactive Pivot Table Container -->
                <div style="overflow-x:auto; border:1px solid var(--border); border-radius:8px; background:var(--bg-card);">
                    <table style="width:100%; border-collapse:collapse; font-size:0.75rem;" id="tcd-dqe-table">
                        <!-- Populated by JS -->
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- 16. TAB FOURNISSEURS & COMMANDES INTERACTIVES -->
    <div id="tab-procurement" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">🛒 Marketplace des Fournisseurs & Centrales BTP (Occitanie)</span>
                    <span class="card-badge" style="color:var(--cyan); margin-left:0.5rem;">5 Partenaires Homologués</span>
                </div>
                <div style="display:flex; gap:0.4rem; flex-wrap:wrap;">
                    <button class="btn-secondary active" onclick="sortSuppliers('dist', this)" style="font-size:0.72rem;">📍 Plus Proche du Chantier</button>
                    <button class="btn-secondary" onclick="sortSuppliers('rating', this)" style="font-size:0.72rem;">★ Meilleure Qualité</button>
                    <button class="btn-secondary" onclick="sortSuppliers('price', this)" style="font-size:0.72rem;">💶 Tarif Économique</button>
                    <button class="btn-primary" style="font-size:0.72rem;" onclick="openAddSupplierModal()">➕ Nouveau Fournisseur</button>
                </div>
            </div>
            <div id="suppliers-list" style="display:flex; flex-direction:column; gap:0.75rem; margin-top:0.5rem;">
                <!-- Populated by JS -->
            </div>
        </div>
    </div>

    <!-- 17. TAB LEDGER & REGISTRE CRYPTOGRAPHIQUE SHA-256 -->
    <div id="tab-ledger" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">⛓️ Registre Cryptographique Immuable (Ledger SHA-256) — Guide & Validateur</span>
                    <span class="card-badge" style="color:var(--cyan); margin-left:0.5rem;">Chaîne Inviolable Certifiée</span>
                </div>
                <button class="btn-primary" style="font-size:0.75rem; padding:0.35rem 0.75rem;" onclick="verifyLedgerIntegrity()">
                    🔍 Vérifier l'Intégrité de la Chaîne
                </button>
            </div>

            <div style="background:rgba(6,182,212,0.08); border:1px solid rgba(6,182,212,0.3); border-radius:8px; padding:1rem; margin-bottom:1.2rem; font-size:0.78rem; line-height:1.7;">
                <div style="font-weight:800; font-size:0.9rem; color:var(--cyan); margin-bottom:0.4rem;">
                    🔐 Pourquoi un Registre Immuable (Ledger) sur vos Chantiers ?
                </div>
                <p style="color:var(--text-main); margin-bottom:0.5rem;">
                    Sur un chantier de Travaux Publics, les litiges financiers et contractuels coûtent en moyenne <b>12% de la marge nette</b>. Le registre cryptographique apporte une preuve formelle irréfutable.
                </p>
                <div class="grid-3" style="gap:0.6rem; margin-top:0.6rem;">
                    <div style="background:var(--bg); padding:0.6rem; border-radius:6px; border:1px solid var(--border);">
                        <b style="color:var(--cyan);">1. Horodatage Infalsifiable</b><br>
                        Chaque événement (RDC, DICT validée, situation mensuelle) est scellé par une empreinte <b>SHA-256</b> unique.
                    </div>
                    <div style="background:var(--bg); padding:0.6rem; border-radius:6px; border:1px solid var(--border);">
                        <b style="color:var(--purple);">2. Chaînage Cryptographique</b><br>
                        Chaque bloc contient le hash du bloc précédent (Hash_n-1). Modifier un événement passé brise mathématiquement toute la chaîne.
                    </div>
                    <div style="background:var(--bg); padding:0.6rem; border-radius:6px; border:1px solid var(--border);">
                        <b style="color:var(--emerald);">3. Force Probante Juridique</b><br>
                        Garantit à la maîtrise d'ouvrage et aux experts judiciaires la conformité absolue des décisions prises.
                    </div>
                </div>
            </div>

            <div id="ledger-verification-banner" style="display:none; background:rgba(16,185,129,0.15); border:1px solid var(--emerald); padding:0.6rem 1rem; border-radius:6px; margin-bottom:1rem; color:var(--emerald); font-weight:700; font-size:0.8rem;">
                ✅ INTÉGRITÉ CRYPTOGRAPHIQUE VALIDÉE : 100% des blocs SHA-256 sont consécutifs et inviolés. Zéro altération détectée.
            </div>

            <div style="overflow-x:auto;">
                <table style="width:100%; border-collapse:collapse; font-size:0.75rem; font-family:var(--font-mono);" id="ledger-table-content">
                    <!-- Rendered by JS -->
                </table>
            </div>
        </div>
    </div>

    <!-- 18. TAB DOCUMENTATION CCTP & 9 RAPPORTS -->
    <div id="tab-docs" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">📚 Documentation Technique CCTP & 9 Rapports d'Ingénierie</span>
                <span class="card-badge" style="color:var(--cyan);">Corpus Complet</span>
            </div>
            <div class="grid-split-40-60">
                <div id="docs-list-container" style="display:flex; flex-direction:column; gap:0.4rem;"></div>
                <div id="doc-viewer-container" style="background:var(--bg); border:1px solid var(--border); border-radius:8px; padding:1.2rem; font-size:0.8rem; line-height:1.7; max-height:600px; overflow-y:auto;">
                    <div style="color:var(--text-muted);">Sélectionnez un rapport à gauche pour afficher son contenu intégral.</div>
                </div>
            </div>
        </div>
    </div>
    """
