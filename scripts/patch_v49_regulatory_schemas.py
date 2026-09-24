# -*- coding: utf-8 -*-
"""
Update Section 21 in section_js_part3.py to implement interactive regulatory synthesis schemas
and window.onload calling initCockpitTicker.
"""

regulatory_schemas_logic = r'''
    function filterDocsView(cat, btn) {
        document.querySelectorAll('.doc-tab-filter').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');

        const docsGrid = document.getElementById('regulatory-docs-grid');
        const schemasView = document.getElementById('regulatory-schemas-view');

        if (cat === 'schemas_synthese') {
            if (docsGrid) docsGrid.style.display = 'none';
            if (schemasView) {
                schemasView.style.display = 'block';
                renderRegulatorySchemas();
            }
        } else {
            if (schemasView) schemasView.style.display = 'none';
            if (docsGrid) {
                docsGrid.style.display = 'grid';
                renderRegulatoryDocs(cat);
            }
        }
    }

    function renderRegulatorySchemas() {
        const cont = document.getElementById('regulatory-schemas-view');
        if (!cont) return;

        cont.innerHTML = `
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(480px, 1fr)); gap: 1rem;">
                
                <!-- SCHEMA 1: WORKFLOW DT / DICT & AIPR -->
                <div class="card" style="border: 2px solid #38bdf8; background: rgba(15,23,42,0.95);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
                        <h3 style="font-size:1.05rem; font-weight:800; color:#38bdf8; margin:0;">📜 1. Workflow Légal DT - DICT & AIPR (Décret 2012-140)</h3>
                        <span class="badge badge-info">Obligation Légale</span>
                    </div>
                    <div style="background: rgba(30,41,59,0.5); padding: 0.75rem; border-radius: 6px; margin-bottom: 0.75rem;">
                        <svg viewBox="0 0 500 130" style="width:100%; height:auto; display:block;">
                            <!-- Stage 1 -->
                            <rect x="5" y="15" width="100" height="90" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
                            <text x="55" y="38" fill="#38bdf8" font-size="11" font-weight="bold" text-anchor="middle">1. PROJET (MOA)</text>
                            <text x="55" y="58" fill="#cbd5e1" font-size="9" text-anchor="middle">Déclaration DT</text>
                            <text x="55" y="72" fill="#94a3b8" font-size="8" text-anchor="middle">Guichet Unique</text>
                            <text x="55" y="88" fill="#e2e8f0" font-size="8" font-weight="bold" text-anchor="middle">Délai : 9 jours</text>

                            <!-- Arrow 1 -->
                            <path d="M 110 60 L 130 60" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow)"/>

                            <!-- Stage 2 -->
                            <rect x="135" y="15" width="105" height="90" rx="6" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
                            <text x="187" y="38" fill="#f59e0b" font-size="11" font-weight="bold" text-anchor="middle">2. ENTREPRISE</text>
                            <text x="187" y="58" fill="#cbd5e1" font-size="9" text-anchor="middle">Déclaration DICT</text>
                            <text x="187" y="72" fill="#94a3b8" font-size="8" text-anchor="middle">9 j ouvrés avant TX</text>
                            <text x="187" y="88" fill="#e2e8f0" font-size="8" font-weight="bold" text-anchor="middle">Récépissé Exploitant</text>

                            <!-- Arrow 2 -->
                            <path d="M 245 60 L 265 60" stroke="#f59e0b" stroke-width="2"/>

                            <!-- Stage 3 -->
                            <rect x="270" y="15" width="105" height="90" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
                            <text x="322" y="38" fill="#10b981" font-size="11" font-weight="bold" text-anchor="middle">3. TERRAIN</text>
                            <text x="322" y="58" fill="#cbd5e1" font-size="9" text-anchor="middle">Piquetage & Traçage</text>
                            <text x="322" y="72" fill="#94a3b8" font-size="8" text-anchor="middle">Marquage 7 couleurs</text>
                            <text x="322" y="88" fill="#e2e8f0" font-size="8" font-weight="bold" text-anchor="middle">Classe A / B / C</text>

                            <!-- Arrow 3 -->
                            <path d="M 380 60 L 400 60" stroke="#10b981" stroke-width="2"/>

                            <!-- Stage 4 -->
                            <rect x="405" y="15" width="90" height="90" rx="6" fill="#1e293b" stroke="#ec4899" stroke-width="2"/>
                            <text x="450" y="38" fill="#ec4899" font-size="11" font-weight="bold" text-anchor="middle">4. EXÉCUTION</text>
                            <text x="450" y="58" fill="#cbd5e1" font-size="9" text-anchor="middle">AIPR Obligatoire</text>
                            <text x="450" y="72" fill="#94a3b8" font-size="8" text-anchor="middle">Fouille douce <1m</text>
                            <text x="450" y="88" fill="#e2e8f0" font-size="8" font-weight="bold" text-anchor="middle">Vigie & Détecteur</text>
                        </svg>
                    </div>
                    <div style="font-size:0.8rem; color:#cbd5e1; line-height:1.5;">
                        <strong>Devoirs Entreprise :</strong> 100% des conducteurs et chefs d'équipe doivent détenir l'AIPR Encadrant/Opérateur en cours de validité (5 ans). Tout réseau sensible (Gaz, HTB, HTA) impose un arrêt immédiat en cas de divergence de classe C (> 1.50m) et l'émission d'un constat d'arrêt contradictoire.
                    </div>
                </div>

                <!-- SCHEMA 2: CYCLE DE VALIDATION MENSUEL CCAG TRAVAUX 2021 -->
                <div class="card" style="border: 2px solid #10b981; background: rgba(15,23,42,0.95);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
                        <h3 style="font-size:1.05rem; font-weight:800; color:#10b981; margin:0;">💶 2. Cycle Facturation & Acomptes (CCAG Travaux 2021 Art. 11)</h3>
                        <span class="badge badge-success">Délai Global 30 Jours</span>
                    </div>
                    <div style="background: rgba(30,41,59,0.5); padding: 0.75rem; border-radius: 6px; margin-bottom: 0.75rem;">
                        <svg viewBox="0 0 500 130" style="width:100%; height:auto; display:block;">
                            <!-- Step 1 -->
                            <rect x="5" y="15" width="110" height="90" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
                            <text x="60" y="38" fill="#10b981" font-size="11" font-weight="bold" text-anchor="middle">J-0 (Fin de Mois)</text>
                            <text x="60" y="58" fill="#cbd5e1" font-size="9" text-anchor="middle">Projet de Décompte</text>
                            <text x="60" y="72" fill="#94a3b8" font-size="8" text-anchor="middle">Métrés contradictoires</text>
                            <text x="60" y="88" fill="#e2e8f0" font-size="8" font-weight="bold" text-anchor="middle">Envoi MOE / Chorus Pro</text>

                            <!-- Arrow 1 -->
                            <path d="M 120 60 L 138 60" stroke="#10b981" stroke-width="2"/>

                            <!-- Step 2 -->
                            <rect x="142" y="15" width="105" height="90" rx="6" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
                            <text x="194" y="38" fill="#f59e0b" font-size="11" font-weight="bold" text-anchor="middle">Délai MOE (7j)</text>
                            <text x="194" y="58" fill="#cbd5e1" font-size="9" text-anchor="middle">État d'Acompte</text>
                            <text x="194" y="72" fill="#94a3b8" font-size="8" text-anchor="middle">Vérification prix/avancement</text>
                            <text x="194" y="88" fill="#e2e8f0" font-size="8" font-weight="bold" text-anchor="middle">Transmission MOA</text>

                            <!-- Arrow 2 -->
                            <path d="M 252 60 L 270 60" stroke="#f59e0b" stroke-width="2"/>

                            <!-- Step 3 -->
                            <rect x="274" y="15" width="105" height="90" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
                            <text x="326" y="38" fill="#38bdf8" font-size="11" font-weight="bold" text-anchor="middle">Délai MOA (15j)</text>
                            <text x="326" y="58" fill="#cbd5e1" font-size="9" text-anchor="middle">Mandatement</text>
                            <text x="326" y="72" fill="#94a3b8" font-size="8" text-anchor="middle">Ordre de paiement</text>
                            <text x="326" y="88" fill="#e2e8f0" font-size="8" font-weight="bold" text-anchor="middle">Comptable Public</text>

                            <!-- Arrow 3 -->
                            <path d="M 384 60 L 402 60" stroke="#38bdf8" stroke-width="2"/>

                            <!-- Step 4 -->
                            <rect x="406" y="15" width="88" height="90" rx="6" fill="#1e293b" stroke="#a855f7" stroke-width="2"/>
                            <text x="450" y="38" fill="#a855f7" font-size="11" font-weight="bold" text-anchor="middle">Max 30 Jours</text>
                            <text x="450" y="58" fill="#cbd5e1" font-size="9" text-anchor="middle">Virement Bancaire</text>
                            <text x="450" y="72" fill="#94a3b8" font-size="8" text-anchor="middle">Intérêts moratoires</text>
                            <text x="450" y="88" fill="#e2e8f0" font-size="8" font-weight="bold" text-anchor="middle">si dépassement</text>
                        </svg>
                    </div>
                    <div style="font-size:0.8rem; color:#cbd5e1; line-height:1.5;">
                        <strong>Règle CCAG 2021 :</strong> Le silence du maître d'œuvre au-delà de 7 jours vaut acceptation tacite du décompte mensuel soumis par le titulaire. En cas de retard de règlement au-delà de 30 jours, des intérêts moratoires + forfait 40€ sont dus de plein droit.
                    </div>
                </div>

                <!-- SCHEMA 3: ARBITRAGE DU COMPACTAGE GTR / SETRA -->
                <div class="card" style="border: 2px solid #f59e0b; background: rgba(15,23,42,0.95);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
                        <h3 style="font-size:1.05rem; font-weight:800; color:#f59e0b; margin:0;">🔨 3. Arbre de Décision Compactage GTR / NF P 98-331</h3>
                        <span class="badge badge-warning">Objectifs q1 à q4</span>
                    </div>
                    <div style="background: rgba(30,41,59,0.5); padding: 0.75rem; border-radius: 6px; margin-bottom: 0.75rem;">
                        <svg viewBox="0 0 500 130" style="width:100%; height:auto; display:block;">
                            <!-- Zone 1 -->
                            <rect x="5" y="15" width="115" height="90" rx="6" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
                            <text x="62" y="38" fill="#f59e0b" font-size="10" font-weight="bold" text-anchor="middle">FOND DE FOUILLE</text>
                            <text x="62" y="58" fill="#cbd5e1" font-size="9" text-anchor="middle">Lit de Pose (10cm)</text>
                            <text x="62" y="72" fill="#94a3b8" font-size="8" text-anchor="middle">Sable 0/4 ou Gravillon</text>
                            <text x="62" y="88" fill="#10b981" font-size="8" font-weight="bold" text-anchor="middle">Compactage manuel doux</text>

                            <!-- Arrow 1 -->
                            <path d="M 125 60 L 143 60" stroke="#f59e0b" stroke-width="2"/>

                            <!-- Zone 2 -->
                            <rect x="147" y="15" width="115" height="90" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
                            <text x="204" y="38" fill="#38bdf8" font-size="10" font-weight="bold" text-anchor="middle">ZONE D'ENROBAGE</text>
                            <text x="204" y="58" fill="#cbd5e1" font-size="9" text-anchor="middle">Flancs & +20cm tuyau</text>
                            <text x="204" y="72" fill="#94a3b8" font-size="8" text-anchor="middle">Objectif q4 (90% OPN)</text>
                            <text x="204" y="88" fill="#e2e8f0" font-size="8" font-weight="bold" text-anchor="middle">Pilonneuse légère</text>

                            <!-- Arrow 2 -->
                            <path d="M 267 60 L 285 60" stroke="#38bdf8" stroke-width="2"/>

                            <!-- Zone 3 -->
                            <rect x="289" y="15" width="105" height="90" rx="6" fill="#1e293b" stroke="#ec4899" stroke-width="2"/>
                            <text x="341" y="38" fill="#ec4899" font-size="10" font-weight="bold" text-anchor="middle">REMBLAI PRINCIPAL</text>
                            <text x="341" y="58" fill="#cbd5e1" font-size="9" text-anchor="middle">Couches de 30cm</text>
                            <text x="341" y="72" fill="#94a3b8" font-size="8" text-anchor="middle">Objectif q3 (95% OPN)</text>
                            <text x="341" y="88" fill="#e2e8f0" font-size="8" font-weight="bold" text-anchor="middle">Rouleau vibrant V2-V3</text>

                            <!-- Arrow 3 -->
                            <path d="M 399 60 L 417 60" stroke="#ec4899" stroke-width="2"/>

                            <!-- Zone 4 -->
                            <rect x="421" y="15" width="75" height="90" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
                            <text x="458" y="38" fill="#10b981" font-size="10" font-weight="bold" text-anchor="middle">CHAUSSÉE</text>
                            <text x="458" y="58" fill="#cbd5e1" font-size="9" text-anchor="middle">Objectif q2</text>
                            <text x="458" y="72" fill="#94a3b8" font-size="8" text-anchor="middle">EV2 >= 80 MPa</text>
                            <text x="458" y="88" fill="#10b981" font-size="8" font-weight="bold" text-anchor="middle">Contrôle pénétro</text>
                        </svg>
                    </div>
                    <div style="font-size:0.8rem; color:#cbd5e1; line-height:1.5;">
                        <strong>Contrôle Obligatoire :</strong> Réalisation de sondages au pénétromètre dynamique léger (PANDA) sur chaque tranchée remblayée avant réouverture à la circulation publique avec PV contradictoire transmis au gestionnaire de voirie.
                    </div>
                </div>

                <!-- SCHEMA 4: SIGNALISATION TEMPORAIRE & BALISAGE DE CHANTIER -->
                <div class="card" style="border: 2px solid #ef4444; background: rgba(15,23,42,0.95);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
                        <h3 style="font-size:1.05rem; font-weight:800; color:#ef4444; margin:0;">🚧 4. Balisage de Chantier Urbain (IISR 8ème Partie)</h3>
                        <span class="badge badge-danger">Sécurité & Arrêté de Voirie</span>
                    </div>
                    <div style="background: rgba(30,41,59,0.5); padding: 0.75rem; border-radius: 6px; margin-bottom: 0.75rem;">
                        <svg viewBox="0 0 500 130" style="width:100%; height:auto; display:block;">
                            <!-- Panneau 1 -->
                            <rect x="5" y="15" width="110" height="90" rx="6" fill="#1e293b" stroke="#ef4444" stroke-width="2"/>
                            <text x="60" y="38" fill="#ef4444" font-size="10" font-weight="bold" text-anchor="middle">1. APPROCHE (AK5)</text>
                            <text x="60" y="58" fill="#cbd5e1" font-size="9" text-anchor="middle">Panneau Travaux AK5</text>
                            <text x="60" y="72" fill="#94a3b8" font-size="8" text-anchor="middle">À 100m en amont</text>
                            <text x="60" y="88" fill="#e2e8f0" font-size="8" font-weight="bold" text-anchor="middle">Tri-flash LED K2</text>

                            <!-- Arrow 1 -->
                            <path d="M 120 60 L 138 60" stroke="#ef4444" stroke-width="2"/>

                            <!-- Panneau 2 -->
                            <rect x="142" y="15" width="110" height="90" rx="6" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
                            <text x="197" y="38" fill="#f59e0b" font-size="10" font-weight="bold" text-anchor="middle">2. VITESSE (B14)</text>
                            <text x="197" y="58" fill="#cbd5e1" font-size="9" text-anchor="middle">Limitation à 30 km/h</text>
                            <text x="197" y="72" fill="#94a3b8" font-size="8" text-anchor="middle">Interdiction dépasser B3</text>
                            <text x="197" y="88" fill="#e2e8f0" font-size="8" font-weight="bold" text-anchor="middle">À 50m du chantier</text>

                            <!-- Arrow 2 -->
                            <path d="M 257 60 L 275 60" stroke="#f59e0b" stroke-width="2"/>

                            <!-- Panneau 3 -->
                            <rect x="279" y="15" width="105" height="90" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
                            <text x="331" y="38" fill="#38bdf8" font-size="10" font-weight="bold" text-anchor="middle">3. BIAIS (K8 / K5a)</text>
                            <text x="331" y="58" fill="#cbd5e1" font-size="9" text-anchor="middle">Biseau de cônes K5a</text>
                            <text x="331" y="72" fill="#94a3b8" font-size="8" text-anchor="middle">Espacement max 3m</text>
                            <text x="331" y="88" fill="#e2e8f0" font-size="8" font-weight="bold" text-anchor="middle">Balises d'alignement</text>

                            <!-- Arrow 3 -->
                            <path d="M 389 60 L 407 60" stroke="#38bdf8" stroke-width="2"/>

                            <!-- Panneau 4 -->
                            <rect x="411" y="15" width="84" height="90" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
                            <text x="453" y="38" fill="#10b981" font-size="10" font-weight="bold" text-anchor="middle">4. FIN (B31)</text>
                            <text x="453" y="58" fill="#cbd5e1" font-size="9" text-anchor="middle">Fin de prescriptions</text>
                            <text x="453" y="72" fill="#94a3b8" font-size="8" text-anchor="middle">Rétablissement</text>
                            <text x="453" y="88" fill="#10b981" font-size="8" font-weight="bold" text-anchor="middle">À 20m aval</text>
                        </svg>
                    </div>
                    <div style="font-size:0.8rem; color:#cbd5e1; line-height:1.5;">
                        <strong>Arrêté Municipal :</strong> Tout empiètement sur la chaussée publique ou le trottoir sans affichage préalable de l'Arrêté de Police de Circulation expose l'entreprise à une interruption de chantier immédiate et des poursuites de voirie.
                    </div>
                </div>

            </div>
        `;
    }
'''

with open('scripts/section_js_part3.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace filterDocsView
fd_start = text.find('function filterDocsView(cat, btn) {')
fd_end = text.find('function renderRegulatoryDocs(filterCat = \'all\') {')
if fd_start != -1 and fd_end != -1:
    text = text[:fd_start] + regulatory_schemas_logic.strip() + "\n\n    " + text[fd_end:]
    print("Regulatory schemas view and filterDocsView updated successfully!")
else:
    print("Error locating filterDocsView in section_js_part3.py")

# Also ensure window.addEventListener('DOMContentLoaded') calls initCockpitTicker()
init_ticker_call = "if (typeof initCockpitTicker === 'function') initCockpitTicker();"
if 'initCockpitTicker()' not in text:
    target_pos = text.find("window.addEventListener('DOMContentLoaded'")
    if target_pos != -1:
        # find where updateCockpitStats or initSigMap is called
        sig_call = text.find("initSigMap();", target_pos)
        if sig_call != -1:
            text = text[:sig_call] + "initCockpitTicker();\n        " + text[sig_call:]
            print("initCockpitTicker added to DOMContentLoaded!")

with open('scripts/section_js_part3.py', 'w', encoding='utf-8') as f:
    f.write(text)
