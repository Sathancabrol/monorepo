import re
from pathlib import Path

TARGET = Path("/home/user/monorepo/projects/btp-conduite-travaux/template.html")

with open(TARGET, "r", encoding="utf-8") as f:
    text = f.read()

# ==========================================
# 1. TAB PROJECTS HUB HTML
# ==========================================
old_hub = """    <!-- 3. TAB HUB CHANTIERS & ARCHIVES (ONGOING & HISTORY) -->
    <div id="tab-projects_hub" class="tab-panel">
        <div class="card" style="margin-bottom:1.2rem;">
            <div class="card-header">
                <span class="card-title">📁 Portfolio des Chantiers & Archives Dossiers</span>
                <div style="display:flex; gap:0.4rem;">
                    <button class="btn-secondary active" id="btn-hub-active" style="font-size:0.75rem;" onclick="renderProjectsHub('active')">⚡ Chantiers en cours (4)</button>
                    <button class="btn-secondary" id="btn-hub-archived" style="font-size:0.75rem;" onclick="renderProjectsHub('archived')">📦 Chantiers Clôturés & Archives (2)</button>
                </div>
            </div>
            <div id="projects-hub-content" class="catalog-grid">
                <!-- Rendered by JS -->
            </div>
        </div>
    </div>"""

new_hub = """    <!-- 3. TAB HUB CHANTIERS & ARCHIVES (ONGOING & HISTORY) -->
    <div id="tab-projects_hub" class="tab-panel">
        <div class="card" style="margin-bottom:1.2rem;">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">📁 Portfolio des Chantiers & Archives Dossiers</span>
                    <span class="card-badge" style="color:var(--cyan); margin-left:0.5rem;">Dossiers DCE & DOE Accessibles</span>
                </div>
                <div style="display:flex; gap:0.4rem;">
                    <button class="btn-secondary active" id="btn-hub-active" style="font-size:0.75rem;" onclick="renderProjectsHub('active')">⚡ Chantiers en cours (4)</button>
                    <button class="btn-secondary" id="btn-hub-archived" style="font-size:0.75rem;" onclick="renderProjectsHub('archived')">📦 Chantiers Clôturés & Archives (2)</button>
                </div>
            </div>
            <div style="margin-bottom:0.8rem; font-size:0.75rem; color:var(--text-muted);">
                💡 <b>Astuce :</b> Cliquez sur n'importe quelle carte de chantier (ex: <i>Rénov réseau de Pézenas</i>, <i>Giratoire Alès</i>) pour ouvrir sa <b>fiche complète en popup</b> avec tous les détails financiers, techniques, humains et téléchargements contractuels.
            </div>
            <div id="projects-hub-content" class="catalog-grid">
                <!-- Rendered by JS -->
            </div>
        </div>
    </div>"""

text = text.replace(old_hub, new_hub)

# ==========================================
# 2. TAB PLANNING GANTT HTML
# ==========================================
old_plan = """    <!-- 4. TAB PLANNING GANTT MULTI-PROJETS -->
    <div id="tab-planning" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">📅 Planning Directeur Multi-Chantiers (Gantt VRD)</span>
                <span class="card-badge" style="color:var(--emerald);">10 Tâches Clés Suivies</span>
            </div>
            <div style="overflow-x:auto;">
                <table style="width:100%; border-collapse:collapse; font-size:0.75rem;" id="planning-gantt-table">
                    <!-- Rendered by JS -->
                </table>
            </div>
        </div>
    </div>"""

new_plan = """    <!-- 4. TAB PLANNING GANTT MULTI-PROJETS -->
    <div id="tab-planning" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">📅 Planning Directeur Multi-Chantiers (Gantt VRD)</span>
                    <span class="card-badge" id="planning-view-badge" style="color:var(--emerald); margin-left:0.5rem;">Vue par Tâche</span>
                </div>
                <div style="display:flex; gap:0.35rem; flex-wrap:wrap;" id="planning-view-bar">
                    <button class="btn-secondary active" id="btn-plan-task" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setPlanningViewMode('task', this)">📊 Par Tâche (Gantt)</button>
                    <button class="btn-secondary" id="btn-plan-time" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setPlanningViewMode('time', this)">⏳ Par Période (Mois/Année)</button>
                    <button class="btn-secondary" id="btn-plan-team" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setPlanningViewMode('team', this)">👥 Par Équipe / Conducteur</button>
                    <button class="btn-secondary" id="btn-plan-machine" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="setPlanningViewMode('machine', this)">🚜 Par Engin Affecté</button>
                </div>
            </div>
            <div style="overflow-x:auto; margin-top:0.5rem;">
                <table style="width:100%; border-collapse:collapse; font-size:0.75rem;" id="planning-gantt-table">
                    <!-- Rendered by JS -->
                </table>
            </div>
        </div>
    </div>"""

text = text.replace(old_plan, new_plan)

# ==========================================
# 3. TAB CATALOG HTML
# ==========================================
old_cat = """    <!-- 7. TAB CATALOGUE D'OUTILS & MATÉRIAUX PAR TÂCHE CHANTIER -->
    <div id="tab-catalog" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">🛒 Catalogue d'Outils, Matériels & Matériaux VRD</span>
                <div style="display:flex; gap:0.4rem; flex-wrap:wrap;" id="catalog-filter-bar">
                    <button class="btn-secondary active" style="font-size:0.7rem;" onclick="filterCatalog('all', this)">Tous</button>
                    <button class="btn-secondary" style="font-size:0.7rem;" onclick="filterCatalog('tranchee', this)">🕳️ Creuser Tranchée</button>
                    <button class="btn-secondary" style="font-size:0.7rem;" onclick="filterCatalog('terrassement', this)">🏔️ Terrassement</button>
                    <button class="btn-secondary" style="font-size:0.7rem;" onclick="filterCatalog('compactage', this)">🔨 Compactage</button>
                    <button class="btn-secondary" style="font-size:0.7rem;" onclick="filterCatalog('enrobes', this)">🛣️ Enrobés</button>
                    <button class="btn-secondary" style="font-size:0.7rem;" onclick="filterCatalog('materials', this)">🧱 Matériaux & Fournitures</button>
                </div>
            </div>
            <div class="catalog-grid" id="catalog-items-grid">
                <!-- Rendered by JS -->
            </div>
        </div>
    </div>"""

new_cat = """    <!-- 7. TAB CATALOGUE D'OUTILS, MATÉRIELS & MATÉRIAUX PAR TÂCHE CHANTIER -->
    <div id="tab-catalog" class="tab-panel">
        <div class="card">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">🛒 Catalogue d'Outils, Matériels, EPI & Matériaux VRD</span>
                    <span class="card-badge" style="color:var(--cyan); margin-left:0.5rem;">Stocks en Temps Réel</span>
                </div>
                <div style="display:flex; gap:0.35rem; flex-wrap:wrap;" id="catalog-filter-bar">
                    <button class="btn-secondary active" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="filterCatalog('all', this)">Tous</button>
                    <button class="btn-secondary" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="filterCatalog('outillage_main', this)">🔨 Outillage Standard & EPI</button>
                    <button class="btn-secondary" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="filterCatalog('tranchee', this)">🕳️ Tranchée & Canalisations</button>
                    <button class="btn-secondary" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="filterCatalog('terrassement', this)">🏔️ Terrassement</button>
                    <button class="btn-secondary" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="filterCatalog('compactage', this)">🔨 Compactage</button>
                    <button class="btn-secondary" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="filterCatalog('enrobes', this)">🛣️ Enrobés</button>
                    <button class="btn-secondary" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="filterCatalog('bordures', this)">📐 Bordures & Trottoirs</button>
                    <button class="btn-secondary" style="font-size:0.7rem; padding:0.25rem 0.55rem;" onclick="filterCatalog('materials', this)">🧱 Matériaux & Fournitures</button>
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:1rem; margin-bottom:0.8rem; font-size:0.72rem; background:var(--bg); padding:0.4rem 0.8rem; border-radius:6px; flex-wrap:wrap;">
                <span style="font-weight:700; color:var(--text-main);">Légende des Stocks :</span>
                <span class="stock-badge-in">📦 En Stock (Disponible)</span>
                <span class="stock-badge-transit">🚚 Livraison en cours (24h)</span>
                <span class="stock-badge-out"><span class="stock-dot-red"></span> 🔴 En Rupture (Réappro 3j)</span>
                <span style="color:var(--text-muted); margin-left:auto;">💡 Cliquez sur <b>🔍 Fiche Détails</b> pour voir la fiche technique 3D complète.</span>
            </div>
            <div class="catalog-grid" id="catalog-items-grid">
                <!-- Rendered by JS -->
            </div>
        </div>
    </div>"""

text = text.replace(old_cat, new_cat)

# ==========================================
# 4. TAB OPBTP SIGNAGE CALCULATOR HTML
# ==========================================
old_opbtp = """    <!-- 9. TAB GUIDE SIGNALÉTIQUE DE CHANTIER OPBTP -->
    <div id="tab-opbtp" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">🦺 Recommandations & Signalisation Temporaire de Chantier (OPBTP / SETRA)</span>
            </div>
            <div class="grid-split-40-60">
                <div style="background:var(--bg); padding:1rem; border-radius:8px; border:1px solid var(--border);">
                    <div style="font-size:0.85rem; font-weight:700; color:var(--text-main); margin-bottom:0.8rem;">📐 Paramètres du Chantier Routier :</div>
                    <div class="input-group">
                        <label class="input-label">Type de Voie :</label>
                        <select class="input-field" id="opbtp-road-type" onchange="calculateSignage()">
                            <option value="bidirectionnelle">Route Bidirectionnelle (80/90 km/h)</option>
                            <option value="urbain">Voie Urbaine (50 km/h)</option>
                            <option value="giratoire">Giratoire / Carrefour Complexe</option>
                            <option value="mobile">Chantier Mobile Progressif</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label class="input-label">Type d'Emprise / Situation :</label>
                        <select class="input-field" id="opbtp-work-type" onchange="calculateSignage()">
                            <option value="alternat_feux">Alternat par Feux Tricolores (KR11J)</option>
                            <option value="route_barree">Route Totalement Barrée & Déviation</option>
                            <option value="trottoir_pieton">Empiétement Trottoir / Déviation Piétons</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label class="input-label">Période d'Intervention :</label>
                        <select class="input-field" id="opbtp-period">
                            <option value="jour">Chantier Fixe de Jour</option>
                            <option value="nuit">Chantier de Nuit (Balises Lumineuses K5a)</option>
                            <option value="urgent">Intervention Urgente & Courte Durée</option>
                        </select>
                    </div>
                    <button class="btn-primary" style="width:100%; justify-content:center;" onclick="calculateSignage()">
                        🔄 Calculer l'Implantation Réglementaire
                    </button>
                </div>

                <div style="background:var(--bg); padding:1rem; border-radius:8px; border:1px solid var(--border);" id="opbtp-results-box">
                    <!-- Populated by JS -->
                </div>
            </div>
        </div>
    </div>"""

new_opbtp = """    <!-- 9. TAB GUIDE SIGNALÉTIQUE DE CHANTIER OPBTP -->
    <div id="tab-opbtp" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <div>
                    <span class="card-title">🦺 Configurateur de Signalisation Temporaire (OPBTP / SETRA)</span>
                    <span class="card-badge" style="color:var(--amber); margin-left:0.5rem;">Assistant Visuel Simple en 3 Étapes</span>
                </div>
            </div>
            <div class="grid-split-40-60">
                <div style="background:var(--bg); padding:1rem; border-radius:8px; border:1px solid var(--border);">
                    <div style="font-size:0.85rem; font-weight:800; color:var(--cyan); margin-bottom:0.8rem;">⚙️ Définissez votre situation de travail :</div>
                    
                    <div class="input-group">
                        <label class="input-label">1. Type de Chantier :</label>
                        <select class="input-field" id="opbtp-job-type" onchange="calculateSignage()">
                            <option value="terrassement">🚜 Terrassement & Fouille Tranchée</option>
                            <option value="voirie" selected>🛣️ Voirie, Rabotage & Enrobés</option>
                            <option value="cana">💧 Pose de Canalisations / Assainissement</option>
                            <option value="elec_gaz">⚡ Réseaux Électriques & Gaz (AIPR)</option>
                            <option value="trottoirs">📐 Trottoirs, Bordures & Aménagements Urbains</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label class="input-label">2. Étape & Situation sur la Voie :</label>
                        <select class="input-field" id="opbtp-work-type" onchange="calculateSignage()">
                            <option value="alternat_feux" selected>🚦 Tranchée / Travaux empiétant sur 1 voie (Alternat Feux KR11J)</option>
                            <option value="route_barree">⛔ Route totalement barrée (Déviation délestage KD22)</option>
                            <option value="trottoir_pieton">🚶 Travaux sur trottoir / Couloir piétons protégé PMR</option>
                            <option value="accotement">🌾 Travaux sur accotement sans empiétement chaussée</option>
                            <option value="chantier_mobile">🚚 Chantier mobile d'application d'enrobés (Biseau K5a)</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label class="input-label">3. Configuration de la Voie :</label>
                        <select class="input-field" id="opbtp-road-type" onchange="calculateSignage()">
                            <option value="bidirectionnelle" selected>Route Bidirectionnelle Rase Campagne (80/90 km/h)</option>
                            <option value="urbain">Voie Urbaine Standard (50 km/h avec trottoir)</option>
                            <option value="giratoire">Giratoire / Carrefour Complexe</option>
                            <option value="rue_etroite">Rue Étroite Centre Ancien (Zone 30 / 20 km/h)</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label class="input-label">Conditions de Visibilité :</label>
                        <select class="input-field" id="opbtp-period" onchange="calculateSignage()">
                            <option value="jour">☀️ Chantier Fixe de Jour</option>
                            <option value="nuit">🌙 Chantier de Nuit (Balises Flash & Cônes Rétro Cl2)</option>
                            <option value="pluie">🌧️ Conditions Dégradées / Brouillard</option>
                        </select>
                    </div>

                    <button class="btn-primary" style="width:100%; justify-content:center; margin-top:0.4rem;" onclick="calculateSignage()">
                        🔄 Mettre à Jour le Schéma & les Panneaux
                    </button>
                </div>

                <div>
                    <!-- Interactive Visual Preview Canvas of the Signage Layout -->
                    <div style="background:var(--bg); padding:0.8rem; border-radius:8px; border:1px solid var(--border); margin-bottom:0.8rem;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                            <span style="font-size:0.75rem; font-weight:700; color:var(--cyan);">🖼️ Schéma Visuel de l'Implantation Réglementaire :</span>
                            <span class="card-badge" style="color:var(--emerald);">Schéma Dynamique</span>
                        </div>
                        <div style="height:200px; background:#0f172a; border-radius:6px; overflow:hidden;">
                            <canvas id="opbtp-signage-canvas" style="width:100%; height:100%;"></canvas>
                        </div>
                    </div>

                    <!-- Detailed Signage Prescriptions Box -->
                    <div style="background:var(--bg); padding:1rem; border-radius:8px; border:1px solid var(--border);" id="opbtp-results-box">
                        <!-- Populated dynamically by JS -->
                    </div>
                </div>
            </div>
        </div>
    </div>"""

text = text.replace(old_opbtp, new_opbtp)

# ==========================================
# 5. TAB SAFETY (EX-AIPR_SAFETY) HTML
# ==========================================
old_safety = """    <!-- 10. TAB SÉCURITÉ GAZ & ÉLECTRICITÉ (AIPR) -->
    <div id="tab-safety" class="tab-panel">
        <div class="card" style="margin-bottom:1.2rem;">
            <div class="card-header">
                <span class="card-title">⚡ Guide de Sécurité Réseaux Gaz & Électricité (AIPR & DICT)</span>
                <button class="btn-danger" style="font-size:0.75rem;" onclick="triggerSimulatedCrisis()">🚨 Déclencher Arrêt d'Urgence AIPR</button>
            </div>
            <div class="grid-2">
                <div style="background:var(--bg); padding:1rem; border-radius:8px; border:1px solid var(--border); font-size:0.8rem; line-height:1.7;">
                    <div style="font-weight:800; color:#eab308; margin-bottom:0.4rem;">🟡 Conduites de Gaz (Réseaux MPB 4 bars) :</div>
                    <div><b>1. Sondages préalables :</b> Sondages manuels doux obligatoires (pelle ronde ou aspiratrice-excavatrice) à moins de 40 cm du tracé théorique de la DICT.</div>
                    <div><b>2. Engins mécaniques :</b> Interdiction formelle du brise-roche (BRH) et du godet denté à moins de 50 cm d'une canalisation gaz en charge.</div>
                    <div><b>3. Procédure d'urgence Gaz :</b> En cas d'odeur de gaz ou d'arrachement, évacuation immédiate dans un rayon de 100m, interdiction de fumer ou d'actionner des moteurs, appel immédiat au numéro vert <b>0 800 47 33 33 (GRDF)</b>.</div>
                </div>

                <div style="background:var(--bg); padding:1rem; border-radius:8px; border:1px solid var(--border); font-size:0.8rem; line-height:1.7;">
                    <div style="font-weight:800; color:#f97316; margin-bottom:0.4rem;">⚡ Réseaux Électriques Aériens & Souterrains :</div>
                    <div><b>1. Distances Limites d'Approche (DLA) :</b>
                        <ul style="margin-left:1.2rem;">
                            <li>Lignes aériennes < 50 kV (HTA) : <b>3.00 mètres minimum</b>.</li>
                            <li>Lignes aériennes > 50 kV (HTB) : <b>5.00 mètres minimum</b>.</li>
                        </ul>
                    </div>
                    <div><b>2. Câbles souterrains BT/HTA :</b> Dégagement manuel après repérage au détecteur électromagnétique. Tout câble sous tension doit être considéré comme dangereux.</div>
                    <div><b>3. Habilitations requises :</b> Titulaire AIPR Encadrant ou Opérateur sur le chantier + Habilitation électrique H0B0 pour tout compagnon intervenant dans l'environnement électrique.</div>
                </div>
            </div>
        </div>
    </div>"""

new_safety = """    <!-- 10. TAB SÉCURITÉ & PRÉVENTION DU CHANTIER -->
    <div id="tab-safety" class="tab-panel">
        <div class="card" style="margin-bottom:1.2rem;">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">🛡️ Sécurité & Prévention Générale du Chantier (AIPR, EPI, Tranchées, Angles Morts)</span>
                    <span class="card-badge" style="color:var(--emerald); margin-left:0.5rem;">Zéro Accident Corporel</span>
                </div>
                <button class="btn-danger" style="font-size:0.75rem;" onclick="triggerSimulatedCrisis()">🚨 Déclencher Arrêt d'Urgence AIPR / Chantier</button>
            </div>

            <div class="grid-3" style="margin-top:0.5rem;">
                <!-- 1. Distances de Sécurité & AIPR -->
                <div style="background:var(--bg); padding:1rem; border-radius:8px; border:1px solid var(--border); font-size:0.78rem; line-height:1.6;">
                    <div style="display:flex; align-items:center; gap:0.4rem; font-weight:800; color:#eab308; margin-bottom:0.5rem; font-size:0.85rem;">
                        <span>⚡</span> 1. Distances Limites & AIPR
                    </div>
                    <div><b>Lignes Aériennes HTA (<50kV) :</b> <span style="color:#ef4444; font-weight:700;">3,00 m minimum</span> de la flèche de pelle.</div>
                    <div><b>Lignes Aériennes HTB (>50kV) :</b> <span style="color:#ef4444; font-weight:700;">5,00 m minimum</span>.</div>
                    <div><b>Gaz MPB 4 bars :</b> Sondage manuel doux ou aspiratrice obligatoire à $<40\text{ cm}$.</div>
                    <div><b>Recul d'Engin :</b> Périmètre d'exclusion de <span style="color:var(--cyan); font-weight:700;">5,00 m</span> derrière tout engin en manoeuvre.</div>
                    <div style="margin-top:0.4rem; font-size:0.72rem; color:var(--text-muted);">📞 Urgence Gaz : <b>0 800 47 33 33</b> | Élec : <b>09 72 67 50 34</b></div>
                </div>

                <!-- 2. Blindage des Tranchées -->
                <div style="background:var(--bg); padding:1rem; border-radius:8px; border:1px solid var(--border); font-size:0.78rem; line-height:1.6;">
                    <div style="display:flex; align-items:center; gap:0.4rem; font-weight:800; color:#38bdf8; margin-bottom:0.5rem; font-size:0.85rem;">
                        <span>🛡️</span> 2. Blindage Obligatoire (R.4534-24)
                    </div>
                    <div><b>Seuil Réglementaire :</b> Blindage obligatoire dès <span style="color:#ef4444; font-weight:700;">1,30 m de profondeur</span> ou en terrain meuble.</div>
                    <div><b>Systèmes Autorisés :</b> Caissons acier double guidage SBH ou palplanches vérinées.</div>
                    <div><b>Interdiction Stricte :</b> Zéro opérateur en fouille avant la pose complète des étrésillons.</div>
                    <div><b>Tête de Talus :</b> Garde-corps rigide et butée de sécurité pour les engins à $>1\text{ m}$.</div>
                </div>

                <!-- 3. Équipements de Protection Individuelle (EPI) -->
                <div style="background:var(--bg); padding:1rem; border-radius:8px; border:1px solid var(--border); font-size:0.78rem; line-height:1.6;">
                    <div style="display:flex; align-items:center; gap:0.4rem; font-weight:800; color:#10b981; margin-bottom:0.5rem; font-size:0.85rem;">
                        <span>🦺</span> 3. Port Obligatoire des EPI
                    </div>
                    <div><b>Casque NF EN 397 :</b> Avec jugulaire attachée en permanence.</div>
                    <div><b>Gilet Haute Visibilité :</b> Classe 3 pour travaux sous circulation.</div>
                    <div><b>Chaussures S3 :</b> Coquille 200J et semelle anti-perforation acier.</div>
                    <div><b>Gants NF EN 388 :</b> Niveau D/F pour découpe et pose bordures.</div>
                    <div><b>Protections Auditives :</b> Bouchons/Casques à $>80\text{ dB(A)}$.</div>
                </div>
            </div>

            <div class="grid-3" style="margin-top:1rem;">
                <!-- 4. Angles Morts & Pelles 360 -->
                <div style="background:var(--bg); padding:1rem; border-radius:8px; border:1px solid var(--border); font-size:0.78rem; line-height:1.6;">
                    <div style="display:flex; align-items:center; gap:0.4rem; font-weight:800; color:#f59e0b; margin-bottom:0.5rem; font-size:0.85rem;">
                        <span>🚜</span> 4. Angles Morts & Rayon de Giratoire
                    </div>
                    <div><b>Rayon de Giration 360° :</b> Balisage de la zone arrière du contrepoids de pelle (zone interdite piéton).</div>
                    <div><b>Contact Visuel :</b> Tout piéton doit croiser le regard du chauffeur avant d'approcher l'engin.</div>
                    <div><b>Marche Arrière PL :</b> Signaleur obligatoire en gilet fluo muni d'un sifflet.</div>
                </div>

                <!-- 5. Risques Chimiques & Enrobés Chauds -->
                <div style="background:var(--bg); padding:1rem; border-radius:8px; border:1px solid var(--border); font-size:0.78rem; line-height:1.6;">
                    <div style="display:flex; align-items:center; gap:0.4rem; font-weight:800; color:#a855f7; margin-bottom:0.5rem; font-size:0.85rem;">
                        <span>🔥</span> 5. Enrobés Chauds (>160°C) & Bitume
                    </div>
                    <div><b>Brûlures Thermiques :</b> Gants cuir épais à manchettes et vêtements couvrants 100% coton.</div>
                    <div><b>Fumées de Bitume :</b> Travail sous le vent, privilégier les enrobés tièdes basse émission.</div>
                    <div><b>Canicule & Hydratation :</b> 3 litres d'eau fraîche par jour/compagnon et abris ombragés.</div>
                </div>

                <!-- 6. Procédure d'Urgence & Crise -->
                <div style="background:var(--bg); padding:1rem; border-radius:8px; border:1px solid var(--border); font-size:0.78rem; line-height:1.6;">
                    <div style="display:flex; align-items:center; gap:0.4rem; font-weight:800; color:#ef4444; margin-bottom:0.5rem; font-size:0.85rem;">
                        <span>🚨</span> 6. Procédure d'Urgence (P.A.S)
                    </div>
                    <div><b>1. PROTÉGER :</b> Couper les moteurs, baliser à 100m, interdire flammes/étincelles.</div>
                    <div><b>2. ALERTER :</b> Pompiers (18/112), SAMU (15), Concessionnaires Gaz/Élec.</div>
                    <div><b>3. SECOURIR :</b> Sauveteur Secouriste du Travail (SST) prodigue les premiers gestes.</div>
                </div>
            </div>
        </div>
    </div>"""

text = text.replace(old_safety, new_safety)

# ==========================================
# 6. TAB SDP EXPLANATION & CALCULATOR HTML
# ==========================================
old_sdp = """    <!-- 12. TAB SOUS-DÉTAILS DE PRIX (SDP) -->
    <div id="tab-sdp" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">💰 Base des 28 Sous-Détails de Prix (SDP) — Étude & Déboursé Sec</span>
                <span class="card-badge" style="color:var(--emerald);">BPU & DQE Dynamiques</span>
            </div>
            <div style="margin-bottom:1rem; display:flex; gap:0.8rem; align-items:center; flex-wrap:wrap; font-size:0.75rem; background:var(--bg); padding:0.6rem; border-radius:6px;">
                <span><b>Taux Horaire MO :</b> <input type="number" id="sdp-tx-mo" value="38.5" style="width:60px; padding:2px;" onchange="renderSDPTable()"> €/h</span>
                <span><b>GNR Carburant :</b> <input type="number" id="sdp-tx-gnr" value="1.45" style="width:60px; padding:2px;" onchange="renderSDPTable()"> €/L</span>
                <span><b>Frais Généraux :</b> <input type="number" id="sdp-tx-fg" value="14" style="width:50px; padding:2px;" onchange="renderSDPTable()"> %</span>
                <span><b>Marge Nette :</b> <input type="number" id="sdp-tx-marge" value="12" style="width:50px; padding:2px;" onchange="renderSDPTable()"> %</span>
            </div>
            <div style="overflow-x:auto;">
                <table style="width:100%; border-collapse:collapse; font-size:0.75rem;" id="sdp-table-content">
                    <!-- Rendered by JS -->
                </table>
            </div>
        </div>
    </div>"""

new_sdp = """    <!-- 12. TAB SOUS-DÉTAILS DE PRIX (SDP) -->
    <div id="tab-sdp" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <div>
                    <span class="card-title">💰 Base des 28 Sous-Détails de Prix (SDP) — Guide & Calculateur de Prix de Vente</span>
                    <span class="card-badge" style="color:var(--emerald); margin-left:0.5rem;">BPU & DQE Dynamiques</span>
                </div>
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

text = text.replace(old_sdp, new_sdp)

# ==========================================
# 7. TAB OBSIDIAN GRAPH HTML
# ==========================================
old_obsidian = """    <!-- 11. TAB OBSIDIAN KNOWLEDGE GRAPH -->
    <div id="tab-obsidian" class="tab-panel">
        <div class="grid-split-70-30">
            <div class="card">
                <div class="card-header">
                    <span class="card-title">🕸️ Graphe de Connaissances BTP (DCE, CCTP, Normes & Prix)</span>
                    <div style="display:flex; gap:0.35rem;">
                        <button class="btn-secondary active" id="filter-all-nodes" style="font-size:0.7rem;" onclick="filterObsidianNodes('all', this)">Tous (59)</button>
                        <button class="btn-secondary" style="font-size:0.7rem;" onclick="filterObsidianNodes('juridique', this)">Marchés</button>
                        <button class="btn-secondary" style="font-size:0.7rem;" onclick="filterObsidianNodes('technique', this)">Technique</button>
                        <button class="btn-secondary" style="font-size:0.7rem;" onclick="filterObsidianNodes('financier', this)">Finances</button>
                    </div>
                </div>
                <div class="obsidian-graph-canvas-wrap">
                    <canvas id="obsidian-canvas" style="width:100%; height:100%;"></canvas>
                </div>
            </div>

            <div class="card" id="obsidian-node-details">
                <div class="card-header">
                    <span class="card-title" id="obsidian-node-title">📄 Note Interactive</span>
                    <span class="card-badge" id="obsidian-node-badge" style="color:var(--cyan);">Sélectionnez un nœud</span>
                </div>
                <div id="obsidian-node-body" style="font-size:0.78rem; color:var(--text-muted); line-height:1.6; max-height:480px; overflow-y:auto;">
                    Cliquez sur un nœud dans le graphe interactif pour afficher sa fiche détaillée, ses métadonnées et ses liens transversaux.
                </div>
            </div>
        </div>
    </div>"""

new_obsidian = """    <!-- 11. TAB OBSIDIAN KNOWLEDGE GRAPH -->
    <div id="tab-obsidian" class="tab-panel">
        <div class="card" style="margin-bottom:1rem;">
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

        <div class="grid-split-70-30">
            <div class="card">
                <div class="obsidian-graph-canvas-wrap" style="height:520px;">
                    <canvas id="obsidian-canvas" style="width:100%; height:100%; cursor:grab;"></canvas>
                </div>
            </div>

            <div class="card" id="obsidian-node-details">
                <div class="card-header">
                    <span class="card-title" id="obsidian-node-title">📄 Note & Documentation</span>
                    <span class="card-badge" id="obsidian-node-badge" style="color:var(--cyan);">Sélectionnez un nœud</span>
                </div>
                <div id="obsidian-node-body" style="font-size:0.78rem; color:var(--text-muted); line-height:1.6; max-height:460px; overflow-y:auto;">
                    Cliquez sur un nœud dans le graphe interactif pour afficher sa fiche détaillée, ses métadonnées et ses liens transversaux.
                </div>
            </div>
        </div>
    </div>"""

text = text.replace(old_obsidian, new_obsidian)

# ==========================================
# 8. TAB SCHEMAS HTML
# ==========================================
old_schemas = """    <!-- 13. TAB SCHÉMAS A-Z & FORMULES -->
    <div id="tab-schemas" class="tab-panel">
        <div class="grid-split-40-60">
            <div class="card">
                <div class="card-header">
                    <span class="card-title">📐 Formules & Calculatrices In Situ</span>
                </div>
                <div class="input-group">
                    <label class="input-label">Choisir la Formule / Contrôle :</label>
                    <select class="input-field" id="formula-select" onchange="updateFormulaCalculator(this.value)">
                        <option value="dynaplaque">1. Dynaplaque & Portance (EV2 / EV1)</option>
                        <option value="pente">2. Pente & Fil d'Eau Assainissement (ΔH / L)</option>
                        <option value="compactage">3. Taux de Compactage & Énergie Proctor</option>
                        <option value="enrobes">4. Température & Refroidissement BBSG</option>
                    </select>
                </div>
                <div id="formula-inputs" style="margin-top:0.8rem;">
                    <!-- Populated by JS -->
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <span class="card-title">📊 Visualisation Graphique de la Formule</span>
                    <span class="card-badge" id="formula-status-badge" style="color:var(--emerald);">Conforme NF</span>
                </div>
                <div class="step-canvas-wrap" style="height:350px;">
                    <canvas id="schema-canvas" style="width:100%; height:100%;"></canvas>
                </div>
                <div id="formula-verdict" style="margin-top:0.8rem; font-size:0.78rem; color:var(--text-muted); line-height:1.6;">
                    <!-- Populated by JS -->
                </div>
            </div>
        </div>
    </div>"""

new_schemas = """    <!-- 13. TAB SCHÉMAS A-Z & FORMULES PÉDAGOGIQUES -->
    <div id="tab-schemas" class="tab-panel">
        <div class="card" style="margin-bottom:1rem;">
            <div class="card-header">
                <span class="card-title">📐 Formules Fondamentales & Calculatrices Graphiques Interactives A-Z</span>
                <span class="card-badge" style="color:var(--cyan);">Conforme Normes AFNOR / SETRA / Fascicules 70 & 71</span>
            </div>
            <p style="font-size:0.75rem; color:var(--text-muted); line-height:1.6;">
                Cette section interactive permet aux conducteurs de travaux et chefs de chantier de vérifier immédiatement la conformité des essais in-situ (portance, pentes, débits, foisonnement) avec feedback visuel en temps réel.
            </p>
        </div>

        <div class="grid-split-40-60">
            <div class="card">
                <div class="card-header">
                    <span class="card-title">⚙️ Paramètres de Calcul :</span>
                </div>
                <div class="input-group">
                    <label class="input-label">Sélectionner la Formule / Essai :</label>
                    <select class="input-field" id="formula-select" onchange="updateFormulaCalculator(this.value)">
                        <option value="dynaplaque">1. Essai de Portance à la Plaque (EV2, EV1, Ratio k ≤ 2.2)</option>
                        <option value="pente">2. Pente & Vitesse d'Auto-Curage Assainissement (ΔH / L)</option>
                        <option value="caquot">3. Débit de Pointe Eaux Pluviales (Formule de Caquot Q=C·I·A)</option>
                        <option value="foisonnement">4. Foisonnement des Terres & Rotations Camions 8x4</option>
                    </select>
                </div>
                <div id="formula-inputs" style="margin-top:0.8rem;">
                    <!-- Populated dynamically by JS -->
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <span class="card-title">📊 Rendu Graphique & Jauge de Conformité</span>
                    <span class="card-badge" id="formula-status-badge" style="color:var(--emerald);">Conforme NF</span>
                </div>
                <div class="step-canvas-wrap" style="height:350px;">
                    <canvas id="schema-canvas" style="width:100%; height:100%;"></canvas>
                </div>
                <div id="formula-verdict" style="margin-top:0.8rem; font-size:0.78rem; color:var(--text-muted); line-height:1.6;">
                    <!-- Populated by JS -->
                </div>
            </div>
        </div>
    </div>"""

text = text.replace(old_schemas, new_schemas)

# ==========================================
# 9. TAB PROCUREMENT (FOURNISSEURS) HTML
# ==========================================
old_proc = """    <!-- 14. TAB FOURNISSEURS & APPROVISIONNEMENTS -->
    <div id="tab-procurement" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">🛒 Répertoire Fournisseurs & Commandes Directes</span>
            </div>
            <div id="suppliers-list" style="display:flex; flex-direction:column; gap:0.6rem;">
                <!-- Rendered by JS -->
            </div>
        </div>
    </div>"""

new_proc = """    <!-- 14. TAB FOURNISSEURS & MARKETPLACE COMPARATIF -->
    <div id="tab-procurement" class="tab-panel">
        <div class="card" style="margin-bottom:1.2rem;">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">🛒 Répertoire & Marketplace Comparatif des Fournisseurs BTP</span>
                    <span class="card-badge" style="color:var(--emerald); margin-left:0.5rem;">5 Centrales & Fournisseurs Partenaires</span>
                </div>
                <button class="btn-primary" style="font-size:0.75rem; padding:0.35rem 0.75rem;" onclick="openAddSupplierModal()">
                    ➕ Ajouter un Fournisseur
                </button>
            </div>

            <!-- Sorting & Search Bar -->
            <div style="display:flex; gap:0.6rem; align-items:center; margin-bottom:1rem; flex-wrap:wrap; font-size:0.75rem; background:var(--bg); padding:0.6rem 0.8rem; border-radius:6px; border:1px solid var(--border);">
                <span><b>Trier la Marketplace par :</b></span>
                <button class="btn-secondary active" id="btn-sort-dist" style="font-size:0.7rem;" onclick="sortSuppliers('dist', this)">📍 Distance Chantier (Proximité)</button>
                <button class="btn-secondary" id="btn-sort-rating" style="font-size:0.7rem;" onclick="sortSuppliers('rating', this)">⭐ Note Qualité & Ponctualité</button>
                <button class="btn-secondary" id="btn-sort-price" style="font-size:0.7rem;" onclick="sortSuppliers('price', this)">💰 Indice de Prix</button>
            </div>

            <!-- Suppliers Comparative Table / Cards Grid -->
            <div id="suppliers-list" style="display:flex; flex-direction:column; gap:0.75rem;">
                <!-- Rendered dynamically by JS -->
            </div>
        </div>
    </div>"""

text = text.replace(old_proc, new_proc)

# ==========================================
# 10. TAB LEDGER HTML
# ==========================================
old_led = """    <!-- 15. TAB REGISTRE IMMUABLE (LEDGER SHA-256) -->
    <div id="tab-ledger" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">⛓️ Registre Cryptographique Immuable (Ledger SHA-256)</span>
                <span class="card-badge" style="color:var(--cyan);">Traçabilité Absolue</span>
            </div>
            <div style="overflow-x:auto;">
                <table style="width:100%; border-collapse:collapse; font-size:0.75rem; font-family:var(--font-mono);" id="ledger-table-content">
                    <!-- Rendered by JS -->
                </table>
            </div>
        </div>
    </div>"""

new_led = """    <!-- 15. TAB REGISTRE IMMUABLE (LEDGER SHA-256) -->
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

text = text.replace(old_led, new_led)

with open(TARGET, "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully updated all HTML tab templates in template.html!")
