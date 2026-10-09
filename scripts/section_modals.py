# -*- coding: utf-8 -*-

def get_modals():
    return r"""
    <!-- ========================================== -->
    <!-- MODAL 1: DETAIL CHANTIER                   -->
    <!-- ========================================== -->
    <div class="modal-backdrop" id="project-details-modal">
        <div class="modal-box">
            <div class="card-header">
                <div class="card-title" id="project-modal-title">Fiche Chantier</div>
                <button class="btn btn-secondary" onclick="closeModal('project-details-modal')">✕</button>
            </div>
            <div id="project-modal-body"></div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL 2: DETAIL TACHE PLANNING             -->
    <!-- ========================================== -->
    <div class="modal-backdrop" id="task-details-modal">
        <div class="modal-box">
            <div class="card-header">
                <div class="card-title" id="task-modal-title">Détail de la Tâche</div>
                <button class="btn btn-secondary" onclick="closeModal('task-details-modal')">✕</button>
            </div>
            <div id="task-modal-body"></div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL 3: DETAIL ENGIN FLOTTE               -->
    <!-- ========================================== -->
    <div class="modal-backdrop" id="vehicle-details-modal">
        <div class="modal-box">
            <div class="card-header">
                <div class="card-title" id="vehicle-modal-title">Fiche Technique Matériel</div>
                <button class="btn btn-secondary" onclick="closeModal('vehicle-details-modal')">✕</button>
            </div>
            <div id="vehicle-modal-body"></div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL 4: DETAIL ARTICLE CATALOGUE          -->
    <!-- ========================================== -->
    <div class="modal-backdrop" id="catalog-item-modal">
        <div class="modal-box">
            <div class="card-header">
                <div class="card-title" id="catalog-item-modal-title">Fiche Fourniture / BPU</div>
                <button class="btn btn-secondary" onclick="closeModal('catalog-item-modal')">✕</button>
            </div>
            <div id="catalog-item-modal-body"></div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL 5: DETAIL ZONE DEPOT                 -->
    <!-- ========================================== -->
    <div class="modal-backdrop" id="depot-zone-modal">
        <div class="modal-box">
            <div class="card-header">
                <div class="card-title" id="depot-zone-modal-title">Inventaire Zone Dépôt</div>
                <button class="btn btn-secondary" onclick="closeModal('depot-zone-modal')">✕</button>
            </div>
            <div id="depot-zone-modal-body"></div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL 6: DETAIL SDP DQE                    -->
    <!-- ========================================== -->
    <div class="modal-backdrop" id="sdp-detail-modal">
        <div class="modal-box" style="max-width:900px;">
            <div class="card-header">
                <div class="card-title" id="sdp-detail-modal-title">Sous-Détail de Prix (SDP)</div>
                <button class="btn btn-secondary" onclick="closeModal('sdp-detail-modal')">✕</button>
            </div>
            <div id="sdp-detail-modal-body"></div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL 7: DETAIL SALARIE / RH               -->
    <!-- ========================================== -->
    <div class="modal-backdrop" id="employee-detail-modal">
        <div class="modal-box">
            <div class="card-header">
                <div class="card-title" id="employee-detail-modal-title">Fiche Salarié & Habilitations</div>
                <button class="btn btn-secondary" onclick="closeModal('employee-detail-modal')">✕</button>
            </div>
            <div id="employee-modal-body"></div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL 8: CAMERA & PHOTO RDC TERRAIN        -->
    <!-- ========================================== -->
    <div class="modal-backdrop" id="rdc-camera-modal">
        <div class="modal-box" style="max-width:650px;">
            <div class="card-header">
                <div class="card-title">📸 Prise de Vue Chantier In Situ</div>
                <button class="btn btn-secondary" onclick="closeModal('rdc-camera-modal')">✕</button>
            </div>
            <div style="background:#020617; border:2px dashed var(--border); border-radius:8px; height:260px; display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:1rem; position:relative; overflow:hidden;">
                <div id="simulated-camera-feed" style="width:100%; height:100%; display:flex; flex-direction:column; align-items:center; justify-content:center; background:linear-gradient(180deg, #0b1329, #020617);">
                    <div style="font-size:3rem; margin-bottom:0.5rem;" id="cam-feed-icon">🚜</div>
                    <div style="font-weight:800; font-size:1.1rem; color:#f8fafc;" id="cam-feed-title">Vue Chantier Port de Sète - Quai Richelieu (Drague Hydromer)</div>
                    <div style="font-size:0.8rem; color:#38bdf8;" id="cam-feed-sub">Axe Giratoire • Pose Bordures T2 & Compactage GNT</div>
                </div>
            </div>
            <div style="display:flex; justify-content:space-between; gap:0.5rem;">
                <button class="btn btn-secondary" onclick="window.updateCameraFeedView()">🔄 Changer Angle Caméra</button>
                <button class="btn btn-primary" onclick="window.capturePhotoForRDC()">📸 Capturer & Joindre au RDC</button>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL 9: GESTIONNAIRE DE CRISE SECURITE    -->
    <!-- ========================================== -->
    <div class="modal-backdrop" id="safety-crisis-modal">
        <div class="modal-box" style="border-color:#ef4444; max-width:750px;">
            <div class="card-header" style="border-bottom-color:rgba(239,68,68,0.4);">
                <div class="card-title" style="color:#ef4444;">🚨 Protocole d'Urgence & Sécurité Chantier</div>
                <button class="btn btn-secondary" onclick="closeModal('safety-crisis-modal')">✕</button>
            </div>
            <div id="safety-crisis-modal-body"></div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL 10: VISIONNEUSE DE DOCUMENT VAULT    -->
    <!-- ========================================== -->
    <div class="modal-backdrop" id="doc-reader-modal">
        <div class="modal-box" style="max-width:900px; max-height:85vh; display:flex; flex-direction:column;">
            <div class="card-header">
                <div class="card-title" id="doc-reader-title">Document</div>
                <button class="btn btn-secondary" onclick="closeModal('doc-reader-modal')">✕</button>
            </div>
            <div id="doc-reader-body" style="background:rgba(15,23,42,0.8); border:1px solid var(--border); border-radius:8px; padding:1.25rem; overflow-y:auto; flex:1; font-family:var(--font-mono); font-size:0.85rem; line-height:1.6; white-space:pre-wrap; color:#e2e8f0;"></div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL 11: UNIFIED ACCOUNT & IDENTITY MODAL -->
    <!-- ========================================== -->
    <div class="modal-backdrop" id="account-modal">
        <div class="modal-box" style="max-width:940px; max-height:90vh; display:flex; flex-direction:column;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; border-bottom:1px solid rgba(56,189,248,0.3); padding-bottom:0.75rem;">
                <div>
                    <h3 style="color:#38bdf8; font-size:1.3rem; font-weight:900; margin:0;" id="account-modal-title">🏢 Gestion du Compte, Entreprise & Rôle Utilisateur</h3>
                    <div style="font-size:0.85rem; color:#cbd5e1;">Connexion, création d'entreprise TP, identification hiérarchique et suppression</div>
                </div>
                <button class="btn btn-secondary" style="padding:0.3rem 0.65rem; font-size:1rem;" onclick="window.closeAccountModal()">✕</button>
            </div>

            <!-- TABS SELECTOR INSIDE MODAL -->
            <div style="display:flex; gap:0.5rem; background:#020617; padding:5px; border-radius:8px; border:1px solid var(--border); margin-bottom:1rem; flex-wrap:wrap;">
                <button class="btn-secondary account-tab-btn active" id="btn-acc-login" onclick="window.setAccountTab('login')">🔑 1. Connexion / Profils</button>
                <button class="btn-secondary account-tab-btn" id="btn-acc-create" onclick="window.setAccountTab('create')">➕ 2. Créer une Entreprise</button>
                <button class="btn-secondary account-tab-btn" id="btn-acc-identity" onclick="window.setAccountTab('identity')">👤 3. Mon Identité & Rôle</button>
                <button class="btn-secondary account-tab-btn" id="btn-acc-delete" onclick="window.setAccountTab('delete')">🗑️ 4. Suppression / Reset</button>
            </div>

            <!-- TAB 1: CONNEXION / PROFILS PRÉCONFIGURÉS -->
            <div class="acc-tab-content" id="acc-tab-login" style="display:block;">
                <div style="font-size:0.88rem; color:#cbd5e1; margin-bottom:0.75rem;">Sélectionnez une entreprise ou un profil de travail actif :</div>
                <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:0.85rem;" id="account-company-presets-grid">
                    <div class="catalog-card" style="cursor:pointer; border:2px solid #f59e0b; background:linear-gradient(135deg, rgba(15,23,42,0.98) 0%, rgba(217,119,6,0.15) 100%); padding:1.1rem;" onclick="window.loginCompanyProfile('colas_sete')">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong style="color:#fef08a; font-size:1.05rem;">🏢 Colas Agence de Sète & Bassin de Thau</strong>
                            <span class="badge-warning" style="padding:3px 8px; border-radius:4px; font-size:0.75rem; font-weight:900;">SIMULATION RÉEL / RÉTRO-INGÉNIERIE</span>
                        </div>
                        <div style="font-size:0.85rem; color:#f1f5f9; margin:0.45rem 0;">Major TP • CA annuel 18.5 M€ • Caisse active 1 450 000 € • Centrale d'enrobage Frontignan</div>
                        <div style="font-size:0.8rem; color:#cbd5e1;">68 Salariés • 14 Engins lourds • 3 Marchés publics majeurs • Rétro-ingénierie des flux inertes</div>
                        <button class="btn btn-primary" style="margin-top:0.65rem; width:100%; background:linear-gradient(135deg, #d97706, #b45309);">⚡ Activer la Simulation Colas Sète</button>
                    </div>

                    <div class="catalog-card" style="cursor:pointer; border:1px solid var(--border); background:rgba(15,23,42,0.95); padding:1rem;" onclick="window.loginCompanyProfile('artisan_2k')">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong style="color:#ffffff; font-size:1rem;">🚜 Artisan Solo Sud VRD</strong>
                            <span class="badge-warning" style="padding:2px 6px; border-radius:4px; font-size:0.75rem; font-weight:800;">MICRO-TP</span>
                        </div>
                        <div style="font-size:0.82rem; color:#cbd5e1; margin:0.4rem 0;">Artisan indépendant / Micro-entreprise • Trésorerie 2 400 €</div>
                        <div style="font-size:0.78rem; color:#94a3b8;">1 Chantier actif • 1 Salarié • 1 Minipelle + Camionette</div>
                        <button class="btn btn-secondary" style="margin-top:0.6rem; width:100%;">Activer le Profil Artisan</button>
                    </div>

                    <div class="catalog-card" style="cursor:pointer; border:1px solid var(--border); background:rgba(15,23,42,0.95); padding:1rem;" onclick="window.loginCompanyProfile('stagiaire_tp')">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong style="color:#ffffff; font-size:1rem;">🎓 Formation Conduite Travaux</strong>
                            <span class="badge-info" style="padding:2px 6px; border-radius:4px; font-size:0.75rem; font-weight:800;">ÉCOLE</span>
                        </div>
                        <div style="font-size:0.82rem; color:#cbd5e1; margin:0.4rem 0;">Centre de formation TP / Étude de cas • Trésorerie fictive 150k€</div>
                        <div style="font-size:0.78rem; color:#94a3b8;">Cas d'école complets Barbazan & Aurouer guidés</div>
                        <button class="btn btn-secondary" style="margin-top:0.6rem; width:100%;">Charger la Session Formation</button>
                    </div>

                    <div class="catalog-card" style="cursor:pointer; border:1px solid var(--border); background:rgba(15,23,42,0.95); padding:1rem;" onclick="window.loginCompanyProfile('compte_neuf')">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong style="color:#ffffff; font-size:1rem;">✨ Compte Neutre Vierge</strong>
                            <span style="color:#94a3b8; font-size:0.75rem; font-weight:800;">0 DONNÉE</span>
                        </div>
                        <div style="font-size:0.82rem; color:#cbd5e1; margin:0.4rem 0;">Environnement vierge pour démarrage complet personnalisé</div>
                        <div style="font-size:0.78rem; color:#94a3b8;">0 Chantier • 0 Salarié • Trésorerie de base 50 000 €</div>
                        <button class="btn btn-secondary" style="margin-top:0.6rem; width:100%;">Ouvrir Compte Vierge</button>
                    </div>
                </div>
            </div>

            <!-- TAB 2: CRÉATION D'ENTREPRISE -->
            <div class="acc-tab-content" id="acc-tab-create" style="display:none;">
                <form id="create-company-form" onsubmit="window.handleCreateCompany(event)">
                    <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:1rem;">
                        <div class="input-group">
                            <label class="input-label">Raison Sociale / Nom d'Entreprise *</label>
                            <input type="text" class="input-field" id="new-comp-name" placeholder="Ex: Méditerranée Travaux Publics" required>
                        </div>
                        <div class="input-group">
                            <label class="input-label">Forme Juridique *</label>
                            <select class="input-field" id="new-comp-legal">
                                <option value="SAS">SAS - Société par Actions Simplifiée</option>
                                <option value="SARL">SARL - Société à Responsabilité Limitée</option>
                                <option value="EURL">EURL - Entreprise Unipersonnelle</option>
                                <option value="SA">SA - Société Anonyme</option>
                                <option value="ARTISAN">Artisan / Micro-Entreprise TP</option>
                            </select>
                        </div>
                        <div class="input-group">
                            <label class="input-label">Capital Social Initial (€)</label>
                            <input type="number" class="input-field" id="new-comp-capital" value="50000" min="1000">
                        </div>
                        <div class="input-group">
                            <label class="input-label">Trésorerie de Départ (€)</label>
                            <input type="number" class="input-field" id="new-comp-treasury" value="120000" min="0">
                        </div>
                        <div class="input-group">
                            <label class="input-label">Ville du Siège Social / Région</label>
                            <input type="text" class="input-field" id="new-comp-city" value="Sète (Hérault 34)">
                        </div>
                        <div class="input-group">
                            <label class="input-label">Spécialité Principale</label>
                            <select class="input-field" id="new-comp-spec">
                                <option value="vrd">Terrassement, VRD & Voirie</option>
                                <option value="assainissement">Canalisations, Assainissement & AEP</option>
                                <option value="enrobes">Application d'Enrobés & Chaussées</option>
                                <option value="genie_civil">Génie Civil & Ouvrages d'Art</option>
                            </select>
                        </div>
                    </div>

                    <div class="input-group" style="margin-top:0.5rem; background:rgba(2,6,23,0.7); padding:0.85rem; border-radius:8px; border:1px solid var(--border);">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                            <label class="input-label" style="margin:0;">Taille de l'équipe initiale (Effectif Salariés) :</label>
                            <span style="font-weight:900; color:#38bdf8; font-size:1.1rem; font-family:var(--font-mono);" id="new-comp-headcount-disp">12 Salariés</span>
                        </div>
                        <input type="range" style="width:100%; accent-color:#38bdf8;" min="1" max="150" value="12" id="new-comp-headcount-slider" oninput="document.getElementById('new-comp-headcount-disp').textContent = this.value + ' Salariés'">
                    </div>

                    <div style="display:flex; justify-content:flex-end; gap:0.75rem; margin-top:1rem;">
                        <button type="button" class="btn btn-secondary" onclick="window.setAccountTab('login')">Annuler</button>
                        <button type="submit" class="btn btn-primary">🚀 Créer et Activer l'Entreprise</button>
                    </div>
                </form>
            </div>

            <!-- TAB 3: IDENTITÉ & RÔLE -->
            <div class="acc-tab-content" id="acc-tab-identity" style="display:none;">
                <form id="save-identity-form" onsubmit="window.handleSaveUserIdentity(event)">
                    <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:1rem;">
                        <div class="input-group">
                            <label class="input-label">Nom & Prénom de l'utilisateur *</label>
                            <input type="text" class="input-field" id="user-fullname" value="Jean DUPONT" required>
                        </div>
                        <div class="input-group">
                            <label class="input-label">Rôle & Perspective Opérationnelle *</label>
                            <select class="input-field" id="user-role-select" onchange="window.updateRolePreview(this.value)">
                                <option value="direction">👑 Direction & Gérant Entreprise</option>
                                <option value="conduite">👷 Conducteur de Travaux Principal</option>
                                <option value="chef_chantier">🦺 Chef de Chantier / Responsable Terrain</option>
                                <option value="compagnon">🛠️ Compagnon / Poseur / Chef d'équipe</option>
                            </select>
                        </div>
                    </div>

                    <div class="input-group" style="background:rgba(2,6,23,0.7); padding:0.85rem; border-radius:8px; border:1px solid var(--border); margin-top:0.5rem;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                            <label class="input-label" style="margin:0;">Ajustement de l'effectif total sous votre direction :</label>
                            <span style="font-weight:900; color:#4ade80; font-size:1.1rem; font-family:var(--font-mono);" id="user-headcount-display">24 Salariés</span>
                        </div>
                        <input type="range" style="width:100%; accent-color:#22c55e;" min="0" max="150" value="24" id="user-headcount-slider" oninput="window.updateHeadcountSlider(this.value)">
                        <div style="font-size:0.75rem; color:#94a3b8; margin-top:0.35rem;">Masse salariale estimée : <strong id="user-payroll-est" style="color:#ffffff;">84 000 € / mois</strong> (charges incluses)</div>
                    </div>

                    <div style="display:flex; justify-content:flex-end; gap:0.75rem; margin-top:1rem;">
                        <button type="submit" class="btn btn-primary">💾 Sauvegarder mon Profil & Identité</button>
                    </div>
                </form>
            </div>

            <!-- TAB 4: SUPPRESSION / RESET -->
            <div class="acc-tab-content" id="acc-tab-delete" style="display:none;">
                <div style="background:rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.4); padding:1rem; border-radius:8px; margin-bottom:1rem;">
                    <h4 style="color:#f87171; font-weight:800; margin-bottom:0.4rem;">⚠️ Zone Sensible & Réinitialisation</h4>
                    <p style="font-size:0.85rem; color:#fecaca;">Vous pouvez supprimer l'entreprise active ou réinitialiser complètement l'application aux paramètres d'usine.</p>
                </div>
                <div style="display:flex; flex-direction:column; gap:0.75rem;">
                    <button class="btn btn-danger" onclick="window.deleteActiveCompany()">🗑️ Supprimer l'Entreprise Active</button>
                    <button class="btn btn-secondary" style="border-color:#ef4444; color:#f87171;" onclick="window.resetAllDataFactory()">🔄 Réinitialiser Données Usine (Factory Reset)</button>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL 12: AJOUTER LIVRAISON & PESEE        -->
    <!-- ========================================== -->
    <div id="modal-add-livraison" class="modal-backdrop">
        <div class="modal-box" style="max-width: 650px;">
            <div class="card-header">
                <div class="card-title">📝 Nouveau Bon de Pesée / Livraison Chantier</div>
                <button class="btn btn-secondary" onclick="closeModal('modal-add-livraison')">✕</button>
            </div>
            <div>
                <form id="form-add-livraison" onsubmit="window.saveNewLivraison(event)">
                    <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:0.6rem; margin-bottom:0.5rem;">
                        <div class="input-group">
                            <label class="input-label">N° Bon de Pesée</label>
                            <input type="text" class="input-field" id="new-bl-num" required placeholder="Ex: BL-2026-0894">
                        </div>
                        <div class="input-group">
                            <label class="input-label">Date & Heure de Pesée</label>
                            <input type="datetime-local" class="input-field" id="new-bl-date" required>
                        </div>
                    </div>
                    <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:0.6rem; margin-bottom:0.5rem;">
                        <div class="input-group">
                            <label class="input-label">Centrale d'Enrobage / Carrière</label>
                            <select class="input-field" id="new-bl-fournisseur">
                                <option value="Colas Midi-Méditerranée Béziers">Colas Midi-Méditerranée Béziers</option>
                                <option value="Eurovia Enrobés Montpellier Ouest">Eurovia Enrobés Montpellier Ouest</option>
                                <option value="Carrières GSM Bassin de Thau">Carrières GSM Bassin de Thau</option>
                                <option value="Lafarge Holcim Bétons Sète">Lafarge Holcim Bétons Sète</option>
                            </select>
                        </div>
                        <div class="input-group">
                            <label class="input-label">Matériau / Formule</label>
                            <select class="input-field" id="new-bl-materiau">
                                <option value="BBSG 0/10 Classique (Enrobé)">BBSG 0/10 Classique (Enrobé)</option>
                                <option value="BBME 0/10 Module Élevé">BBME 0/10 Module Élevé</option>
                                <option value="GNT 0/31.5 Non Traitée">GNT 0/31.5 Non Traitée</option>
                                <option value="GNT 0/20 Réglage Fin">GNT 0/20 Réglage Fin</option>
                            </select>
                        </div>
                    </div>
                    <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:0.6rem; margin-bottom:0.5rem;">
                        <div class="input-group">
                            <label class="input-label">Immat. Camion</label>
                            <input type="text" class="input-field" id="new-bl-camion" placeholder="Ex: GA-420-TX">
                        </div>
                        <div class="input-group">
                            <label class="input-label">Quantité Pesée (t)</label>
                            <input type="number" step="0.01" class="input-field" id="new-bl-qte" required placeholder="Ex: 28.40">
                        </div>
                        <div class="input-group">
                            <label class="input-label">Température (°C)</label>
                            <input type="number" class="input-field" id="new-bl-temp" value="165">
                        </div>
                    </div>
                    <div style="display:flex; justify-content:flex-end; gap:0.5rem; margin-top:1rem;">
                        <button type="button" class="btn btn-secondary" onclick="closeModal('modal-add-livraison')">Annuler</button>
                        <button type="submit" class="btn btn-primary">💾 Enregistrer Bon de Pesée</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL 13: AJOUTER JOURNEE D'INTEMPERIE     -->
    <!-- ========================================== -->
    <div id="modal-add-intemperie" class="modal-backdrop">
        <div class="modal-box" style="max-width: 600px;">
            <div class="card-header">
                <div class="card-title">🌧️ Déclaration d'Arrêt pour Intempérie (CCAG Art. 18.2.3)</div>
                <button class="btn btn-secondary" onclick="closeModal('modal-add-intemperie')">✕</button>
            </div>
            <div>
                <form id="form-add-intemperie" onsubmit="window.saveNewIntemperie(event)">
                    <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:0.6rem; margin-bottom:0.5rem;">
                        <div class="input-group">
                            <label class="input-label">Date du Constat</label>
                            <input type="date" class="input-field" id="new-intemp-date" required>
                        </div>
                        <div class="input-group">
                            <label class="input-label">Phénomène Météorologique</label>
                            <select class="input-field" id="new-intemp-type">
                                <option value="Pluie Diluvienne (> 10 mm/j)">Pluie Diluvienne (> 10 mm/j)</option>
                                <option value="Vent Violent / Rafales (> 60 km/h)">Vent Violent / Rafales (> 60 km/h)</option>
                                <option value="Gel Sévère (< -2°C)">Gel Sévère (< -2°C)</option>
                                <option value="Canicule Alerte Orange/Rouge">Canicule Alerte Orange/Rouge</option>
                            </select>
                        </div>
                    </div>
                    <div style="display:flex; justify-content:flex-end; gap:0.5rem; margin-top:1rem;">
                        <button type="button" class="btn btn-secondary" onclick="closeModal('modal-add-intemperie')">Annuler</button>
                        <button type="submit" class="btn btn-primary">💾 Valider et Enregistrer</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL 14: FICHES 1/4H SECURITE OPPBTP      -->
    <!-- ========================================== -->
    <div id="modal-safety-quarter-hour" class="modal-backdrop">
        <div class="modal-box" style="max-width: 850px; max-height: 90vh; display: flex; flex-direction: column;">
            <div class="card-header">
                <div class="card-title">🦺 Module Fiches 1/4 d'Heure Sécurité OPPBTP & Accueil Sécurité</div>
                <button class="btn btn-secondary" onclick="closeModal('modal-safety-quarter-hour')">✕</button>
            </div>
            <div style="overflow-y: auto; flex: 1;">
                <div style="display: flex; gap: 0.5rem; margin-bottom: 1rem; align-items: center; flex-wrap: wrap;">
                    <span style="font-weight: 700; color: #38bdf8; font-size: 0.85rem;">Thématique 1/4h Sécurité :</span>
                    <select class="input-field" id="safety-theme-select" style="flex: 1; min-width: 280px;" onchange="window.loadSafetyBriefingContent()">
                        <option value="aipr_gaz_elec">1. Travaux à proximité des réseaux enterrés (AIPR / Gaz / HTA)</option>
                        <option value="blindage_tranchee">2. Risque d'éboulement & Blindage des tranchées (R.4534)</option>
                        <option value="engins_pietons">3. Coactivité et heurts Engins / Piétons sur chantier</option>
                        <option value="elinguage_levage">4. Élingage, Manutention et Levage de blindages/tuyaux</option>
                        <option value="enrobes_brulures">5. Risques chimiques & Brûlures lors de la pose d'enrobés à chaud</option>
                    </select>
                    <button class="btn btn-primary" onclick="window.printSafetyBriefing()">🖨️ Imprimer Fiche</button>
                </div>

                <div id="safety-briefing-content" style="background: rgba(15,23,42,0.8); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                    <!-- Injected dynamically -->
                </div>
            </div>
        </div>
    </div>

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
