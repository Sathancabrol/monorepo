from pathlib import Path

TARGET = Path("/home/user/monorepo/projects/btp-conduite-travaux/template.html")

with open(TARGET, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update tab-planning HTML
old_plan_block = """<div id="tab-planning" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">📅 Planning Directeur Multi-Chantiers (Gantt & Jalons)</span>
                <span class="card-badge" style="color:var(--cyan);">Mise à Jour Hebdomadaire</span>
            </div>
            <div style="overflow-x:auto;">
                <table class="cctp-table" id="planning-table">
                    <thead>
                        <tr>
                            <th>Chantier</th>
                            <th>Tâche Opérationnelle</th>
                            <th>Début</th>
                            <th>Fin Prévue</th>
                            <th>Responsable</th>
                            <th>Avancement</th>
                            <th>Statut</th>
                        </tr>
                    </thead>
                    <tbody id="planning-tbody">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>"""

new_plan_block = """<div id="tab-planning" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">📅 Planning Directeur Multi-Chantiers (Gantt VRD)</span>
                    <span class="card-badge" id="planning-view-badge" style="color:var(--emerald); margin-left:0.5rem;">Vue par Tâche</span>
                </div>
                <!-- Planning View Switcher Buttons -->
                <div style="display:flex; gap:0.35rem; flex-wrap:wrap;" id="planning-view-bar">
                    <button class="btn-secondary active" id="btn-plan-task" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setPlanningViewMode('task', this)">📊 Par Tâche (Gantt)</button>
                    <button class="btn-secondary" id="btn-plan-time" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setPlanningViewMode('time', this)">⏳ Par Période (Mois/Année)</button>
                    <button class="btn-secondary" id="btn-plan-team" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setPlanningViewMode('team', this)">👥 Par Équipe / Conducteur</button>
                    <button class="btn-secondary" id="btn-plan-machine" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setPlanningViewMode('machine', this)">🚜 Par Engin Affecté</button>
                </div>
            </div>
            <div style="overflow-x:auto; margin-top:0.5rem;">
                <table style="width:100%; border-collapse:collapse; font-size:0.75rem;" id="planning-gantt-table">
                    <!-- Rendered dynamically by JS -->
                </table>
            </div>
        </div>
    </div>"""

if old_plan_block in text:
    text = text.replace(old_plan_block, new_plan_block)
    print("Replaced tab-planning HTML!")

# 2. Update tab-sdp HTML
old_sdp_block = """<div id="tab-sdp" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">💰 Calculateur & Simulateur de Devis 28 SDP (Déboursés Secs)</span>
                <div style="display:flex; gap:0.5rem;">
                    <button class="btn-primary" style="font-size:0.75rem;" onclick="exportSDPDevis()">📄 Exporter BPU / Devis</button>
                </div>
            </div>
            <div style="overflow-x:auto;">
                <table class="cctp-table" id="sdp-table">
                    <thead>
                        <tr>
                            <th>Code SDP</th>
                            <th>Désignation de l'Ouvrage</th>
                            <th>Unité</th>
                            <th>MO (€)</th>
                            <th>Matériel (€)</th>
                            <th>Matériaux (€)</th>
                            <th>Déboursé Sec Total (€)</th>
                        </tr>
                    </thead>
                    <tbody id="sdp-tbody"></tbody>
                </table>
            </div>
        </div>
    </div>"""

new_sdp_block = """<div id="tab-sdp" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">💰 Base des 28 Sous-Détails de Prix (SDP) — Guide & Calculateur de Prix de Vente</span>
                    <span class="card-badge" style="color:var(--emerald); margin-left:0.5rem;">BPU & DQE Dynamiques</span>
                </div>
                <button class="btn-primary" style="font-size:0.75rem;" onclick="exportSDPDevis()">📄 Exporter BPU / Devis DQE</button>
            </div>

            <!-- Pedagogical Explanation Guide for SDP -->
            <div style="background:rgba(6,182,212,0.08); border:1px solid rgba(6,182,212,0.3); border-radius:8px; padding:1rem; margin-bottom:1.2rem; font-size:0.78rem; line-height:1.7;">
                <div style="font-weight:800; font-size:0.9rem; color:var(--cyan); margin-bottom:0.4rem;">
                    📚 Comprendre le Sous-Détail de Prix (SDP) en Travaux Publics :
                </div>
                <p style="color:var(--text-main); margin-bottom:0.6rem;">
                    Un <b>Sous-Détail de Prix (SDP)</b> est la décomposition analytique exacte de ce que coûte la réalisation d'une unité d'ouvrage (ex: <i>1 mètre linéaire de tranchée</i>, <i>1 tonne d'enrobé</i>, <i>1 m² de bordure</i>). Il se calcule en 4 étapes fondamentales :
                </p>
                <div class="grid-4" style="gap:0.6rem; margin-top:0.6rem;">
                    <div style="background:var(--bg); padding:0.6rem; border-radius:6px; border:1px solid var(--border);">
                        <b style="color:var(--amber);">1. Déboursé Sec (DS)</b><br>
                        Coût direct = Matériaux (MAT) + Main d'œuvre (MO) + Matériel & Engins (EQ).
                    </div>
                    <div style="background:var(--bg); padding:0.6rem; border-radius:6px; border:1px solid var(--border);">
                        <b style="color:var(--cyan);">2. Frais de Chantier (FC)</b><br>
                        Installation de chantier, géomètre, balisage, laboratoire (6% à 10% du DS).
                    </div>
                    <div style="background:var(--bg); padding:0.6rem; border-radius:6px; border:1px solid var(--border);">
                        <b style="color:var(--purple);">3. Frais Généraux (FG)</b><br>
                        Coût du siège social, direction, assurances, comptabilité (12% à 16% du DS).
                    </div>
                    <div style="background:var(--bg); padding:0.6rem; border-radius:6px; border:1px solid var(--border);">
                        <b style="color:var(--emerald);">4. Coefficient K & Prix de Vente</b><br>
                        <b>PV HT = DS × K</b>. K intègre les FG, FC, aléas et la marge nette bénéficiaire.
                    </div>
                </div>
            </div>

            <!-- Interactive Parameters Bar -->
            <div style="margin-bottom:1rem; display:flex; gap:1.2rem; align-items:center; flex-wrap:wrap; font-size:0.75rem; background:var(--bg); padding:0.8rem; border-radius:6px; border:1px solid var(--border);">
                <span><b>Taux Horaire Moyen MO :</b> <input type="number" id="sdp-tx-mo" value="38.5" style="width:65px; padding:3px; border-radius:4px; border:1px solid var(--border); background:var(--card-bg); color:var(--text-main);" onchange="renderSDPTable()"> €/h</span>
                <span><b>Carburant GNR :</b> <input type="number" id="sdp-tx-gnr" value="1.45" step="0.05" style="width:65px; padding:3px; border-radius:4px; border:1px solid var(--border); background:var(--card-bg); color:var(--text-main);" onchange="renderSDPTable()"> €/L</span>
                <span><b>Frais Généraux (FG) :</b> <input type="number" id="sdp-tx-fg" value="14" style="width:55px; padding:3px; border-radius:4px; border:1px solid var(--border); background:var(--card-bg); color:var(--text-main);" onchange="renderSDPTable()"> %</span>
                <span><b>Coefficient de Marge Nette :</b> <input type="number" id="sdp-tx-marge" value="12" style="width:55px; padding:3px; border-radius:4px; border:1px solid var(--border); background:var(--card-bg); color:var(--text-main);" onchange="renderSDPTable()"> %</span>
                <button class="btn-primary" style="margin-left:auto; font-size:0.72rem;" onclick="renderSDPTable()">🔄 Recalculer les 28 Prix Unitaires</button>
            </div>

            <div style="overflow-x:auto;">
                <table style="width:100%; border-collapse:collapse; font-size:0.75rem;" id="sdp-table-content">
                    <!-- Rendered by JS -->
                </table>
            </div>
        </div>
    </div>"""

if old_sdp_block in text:
    text = text.replace(old_sdp_block, new_sdp_block)
    print("Replaced tab-sdp HTML!")

# 3. Update tab-ledger HTML
old_ledger_block = """<div id="tab-ledger" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">⛓️ Cryptographic Audit Ledger SHA-256</span>
                <span class="card-badge" style="color:var(--purple);">Traçabilité Inaltérable</span>
            </div>
            <div id="ledger-entries-container" style="display:flex; flex-direction:column; gap:0.75rem;"></div>
        </div>
    </div>"""

new_ledger_block = """<div id="tab-ledger" class="tab-panel">
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

            <!-- Pedagogical Explanation of Ledger in Public Works -->
            <div style="background:rgba(6,182,212,0.08); border:1px solid rgba(6,182,212,0.3); border-radius:8px; padding:1rem; margin-bottom:1.2rem; font-size:0.78rem; line-height:1.7;">
                <div style="font-weight:800; font-size:0.9rem; color:var(--cyan); margin-bottom:0.4rem;">
                    🔐 Pourquoi un Registre Immuable (Ledger) sur vos Chantiers ?
                </div>
                <p style="color:var(--text-main); margin-bottom:0.5rem;">
                    Sur un chantier de Travaux Publics, les litiges financiers et contractuels (pénalités de retard, aléas géotechniques, modifications d'Ordres de Service, réceptions de DICT) coûtent en moyenne <b>12% de la marge nette</b>.
                </p>
                <div class="grid-3" style="gap:0.6rem; margin-top:0.6rem;">
                    <div style="background:var(--bg); padding:0.6rem; border-radius:6px; border:1px solid var(--border);">
                        <b style="color:var(--cyan);">1. Horodatage Infalsifiable</b><br>
                        Chaque événement (RDC, DICT validée, situation mensuelle) est scellé par une empreinte <b>SHA-256</b> unique.
                    </div>
                    <div style="background:var(--bg); padding:0.6rem; border-radius:6px; border:1px solid var(--border);">
                        <b style="color:var(--purple);">2. Chaînage Cryptographique</b><br>
                        Chaque bloc contient le hash du bloc précédent ($Hash_{n-1}$). Modifier un événement passé brise mathématiquement toute la chaîne.
                    </div>
                    <div style="background:var(--bg); padding:0.6rem; border-radius:6px; border:1px solid var(--border);">
                        <b style="color:var(--emerald);">3. Force Probante Juridique</b><br>
                        Garantit à la maîtrise d'ouvrage et aux experts judiciaires l'antériorité et la conformité absolue des décisions prises.
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
    </div>"""

if old_ledger_block in text:
    text = text.replace(old_ledger_block, new_ledger_block)
    print("Replaced tab-ledger HTML!")

# 4. Update tab-obsidian HTML with Multi-Heuristics HUD
old_obs_block = """<div id="tab-obsidian" class="tab-panel">
        <div class="obsidian-layout">
            <div class="obsidian-graph-container" id="obsidian-graph-viewport">
                <div class="obsidian-hud">
                    <div style="display:flex; align-items:center; gap:0.5rem; background:rgba(15,23,42,0.9); padding:0.4rem 0.8rem; border-radius:8px; border:1px solid var(--border);">
                        <span style="font-size:0.85rem;">🕸️</span>
                        <input type="text" id="obsidian-search" placeholder="Rechercher note, tag..." oninput="onObsidianSearch(this.value)" style="background:transparent; border:none; color:#fff; font-size:0.8rem; outline:none; width:180px;">
                    </div>
                    <div style="display:flex; align-items:center; gap:0.4rem;" id="obsidian-tag-filters">
                        <button class="obsidian-chip active" onclick="filterObsidianGroup('ALL', this)" style="background:var(--bg-card); border:1px solid var(--border); color:#fff; padding:0.3rem 0.6rem; border-radius:6px; font-size:0.7rem; cursor:pointer;">Tous</button>
                        <button class="obsidian-chip" onclick="filterObsidianGroup('00-08 Rapports Maîtres', this)" style="background:var(--bg-card); border:1px solid var(--border); color:#38bdf8; padding:0.3rem 0.6rem; border-radius:6px; font-size:0.7rem; cursor:pointer;">Rapports</button>
                        <button class="obsidian-chip" onclick="filterObsidianGroup('Cycle de Vie A-Z', this)" style="background:var(--bg-card); border:1px solid var(--border); color:#34d399; padding:0.3rem 0.6rem; border-radius:6px; font-size:0.7rem; cursor:pointer;">Phases A-Z</button>
                    </div>
                    <div style="display:flex; align-items:center; gap:0.4rem;">
                        <button class="btn-secondary" style="font-size:0.72rem; padding:0.35rem 0.65rem;" onclick="resetObsidianView()">🔄 Recentrer</button>
                        <button class="btn-primary" style="font-size:0.72rem; padding:0.35rem 0.65rem;" onclick="exportObsidianVault()">📥 Exporter Vault</button>
                    </div>
                </div>
                <canvas id="obsidian-canvas" style="width:100%; height:100%; display:block;"></canvas>
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
    </div>"""

new_obs_block = """<div id="tab-obsidian" class="tab-panel">
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
    </div>"""

if old_obs_block in text:
    text = text.replace(old_obs_block, new_obs_block)
    print("Replaced tab-obsidian HTML!")

with open(TARGET, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved patch_template_final.py successfully!")
