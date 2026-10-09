#!/usr/bin/env python3
"""
Patch v60: Update Account Modal with Login / Create / Delete / Role / Headcount
"""

with open("scripts/section_modals.py", "r", encoding="utf-8") as f:
    text = f.read()

new_account_modal_html = """    <!-- ========================================== -->
    <!-- ACCOUNT & COMPANY MANAGEMENT MODAL         -->
    <!-- ========================================== -->
    <div class="modal-backdrop" id="account-modal">
        <div class="modal-box" style="max-width:920px; max-height:90vh; display:flex; flex-direction:column;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem; border-bottom:1px solid rgba(51,65,85,0.7); padding-bottom:0.6rem;">
                <div>
                    <h3 style="color:#38bdf8; font-size:1.2rem; font-weight:900; margin:0;" id="account-modal-title">🏢 Gestion du Compte, Entreprise & Rôle Utilisateur</h3>
                    <div style="font-size:0.78rem; color:#94a3b8;">Connexion, création d'entité TP, suppression et identification hiérarchique</div>
                </div>
                <button class="btn btn-secondary" style="padding:0.2rem 0.5rem;" onclick="closeAccountModal()">✕</button>
            </div>

            <!-- TABS SELECTOR INSIDE MODAL -->
            <div style="display:flex; gap:0.4rem; background:#020617; padding:4px; border-radius:6px; border:1px solid var(--border); margin-bottom:0.85rem; flex-wrap:wrap;">
                <button class="btn-secondary account-tab-btn active" id="btn-acc-login" onclick="setAccountTab('login')">🔑 1. Connexion / Entreprises</button>
                <button class="btn-secondary account-tab-btn" id="btn-acc-create" onclick="setAccountTab('create')">➕ 2. Créer une Entreprise</button>
                <button class="btn-secondary account-tab-btn" id="btn-acc-identity" onclick="setAccountTab('identity')">👤 3. Mon Identité & Rôle</button>
                <button class="btn-secondary account-tab-btn" id="btn-acc-delete" onclick="setAccountTab('delete')">🗑️ 4. Supprimer / Réinitialiser</button>
            </div>

            <div style="overflow-y:auto; flex:1; padding-right:4px;">
                <!-- TAB 1: CONNEXION / CHOIX ENTREPRISE -->
                <div id="acc-tab-login" class="acc-tab-content">
                    <div class="grid-2" style="gap:0.75rem;">
                        <!-- 1. OCCITANIE TP (ESTABLISHED) -->
                        <div class="card company-profile-card active" id="prof-card-occitanie_tp" style="border:2px solid var(--cyan); background:rgba(15,23,42,0.95); cursor:pointer; padding:0.9rem; border-radius:8px;" onclick="loginCompanyProfile('occitanie_tp')">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.4rem;">
                                <span class="badge badge-info">PME Établie Régionale</span>
                                <span class="badge badge-success" id="prof-active-badge-occitanie_tp">Active</span>
                            </div>
                            <h4 style="font-size:0.95rem; font-weight:900; color:#f8fafc; margin-bottom:0.2rem;">🏢 1. Occitanie Travaux Publics & VRD SAS</h4>
                            <p style="font-size:0.75rem; color:#cbd5e1; line-height:1.3; margin-bottom:0.5rem;">Entreprise générale de VRD et terrassement. Flotte 6 engins, 4 chantiers actifs (3.4 M€), 24 salariés.</p>
                            <div style="display:grid; grid-template-columns:1fr 1fr; gap:4px; font-size:0.72rem; background:rgba(30,41,59,0.5); padding:0.5rem; border-radius:6px;">
                                <div>Trésorerie : <strong style="color:var(--emerald);">485 200 €</strong></div>
                                <div>Chantiers : <strong style="color:#38bdf8;">4 Actifs</strong></div>
                                <div>Flotte : <strong style="color:var(--amber);">6 Engins</strong></div>
                                <div>Effectif : <strong>24 Collaborateurs</strong></div>
                            </div>
                        </div>

                        <!-- 2. ARTISAN PERSO (2k€ + BUREAU + EPI) -->
                        <div class="card company-profile-card" id="prof-card-artisan_2k" style="border:1px solid rgba(51,65,85,0.8); background:rgba(15,23,42,0.95); cursor:pointer; padding:0.9rem; border-radius:8px;" onclick="loginCompanyProfile('artisan_2k')">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.4rem;">
                                <span class="badge badge-warning">Artisan Solo / 2 000 €</span>
                                <span class="badge" id="prof-active-badge-artisan_2k" style="display:none; background:var(--emerald);">Active</span>
                            </div>
                            <h4 style="font-size:0.95rem; font-weight:900; color:#f8fafc; margin-bottom:0.2rem;">🦺 2. Artisan Sud VRD (Amorçage 2k€)</h4>
                            <p style="font-size:0.75rem; color:#cbd5e1; line-height:1.3; margin-bottom:0.5rem;">Démarrage artisanal 2 000 €, outillage laser, paquetage EPI certifié, 1 tranchée en cours (6.5k€).</p>
                            <div style="display:grid; grid-template-columns:1fr 1fr; gap:4px; font-size:0.72rem; background:rgba(30,41,59,0.5); padding:0.5rem; border-radius:6px;">
                                <div>Fonds Départ : <strong style="color:var(--emerald);">2 000 €</strong></div>
                                <div>Actifs : <strong style="color:#38bdf8;">Bureau + EPI + Laser</strong></div>
                                <div>Chantier : <strong style="color:var(--amber);">1 Tranchée Pézenas</strong></div>
                                <div>Effectif : <strong>1 Artisan + 1 Aide</strong></div>
                            </div>
                        </div>

                        <!-- 3. STAGIAIRE TP / COURS CONDUITE TRAVAUX -->
                        <div class="card company-profile-card" id="prof-card-stagiaire_tp" style="border:1px solid rgba(51,65,85,0.8); background:rgba(15,23,42,0.95); cursor:pointer; padding:0.9rem; border-radius:8px;" onclick="loginCompanyProfile('stagiaire_tp')">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.4rem;">
                                <span class="badge" style="background:rgba(168,85,247,0.2); color:#c084fc;">Dossiers de Cours & Études</span>
                                <span class="badge" id="prof-active-badge-stagiaire_tp" style="display:none; background:var(--emerald);">Active</span>
                            </div>
                            <h4 style="font-size:0.95rem; font-weight:900; color:#f8fafc; margin-bottom:0.2rem;">🎓 3. Formation Conduite de Travaux (DCE M4-L)</h4>
                            <p style="font-size:0.75rem; color:#cbd5e1; line-height:1.3; margin-bottom:0.5rem;">Études basées sur Barbazan M4-L, Lotissement Aurouer et Déviation Noé avec fiches de tâches.</p>
                            <div style="display:grid; grid-template-columns:1fr 1fr; gap:4px; font-size:0.72rem; background:rgba(30,41,59,0.5); padding:0.5rem; border-radius:6px;">
                                <div>Trésorerie : <strong style="color:var(--emerald);">150 000 €</strong></div>
                                <div>Dossiers : <strong style="color:#c084fc;">3 DCE Réels</strong></div>
                                <div>Engins : <strong style="color:var(--amber);">3 Engins École</strong></div>
                                <div>Effectif : <strong>1 Stagiaire + 8 Comp.</strong></div>
                            </div>
                        </div>

                        <!-- 4. VIERGE / COMPTE NEUF -->
                        <div class="card company-profile-card" id="prof-card-compte_neuf" style="border:1px solid rgba(51,65,85,0.8); background:rgba(15,23,42,0.95); cursor:pointer; padding:0.9rem; border-radius:8px;" onclick="loginCompanyProfile('compte_neuf')">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.4rem;">
                                <span class="badge badge-warning">Page Blanche / Démarrage</span>
                                <span class="badge" id="prof-active-badge-compte_neuf" style="display:none; background:var(--emerald);">Active</span>
                            </div>
                            <h4 style="font-size:0.95rem; font-weight:900; color:#f8fafc; margin-bottom:0.2rem;">📄 4. Nouvelle Entreprise TP (Compte Neuf)</h4>
                            <p style="font-size:0.75rem; color:#cbd5e1; line-height:1.3; margin-bottom:0.5rem;">Environnement vierge pour configurer et tester une entreprise de A à Z sans données préalables.</p>
                            <div style="display:grid; grid-template-columns:1fr 1fr; gap:4px; font-size:0.72rem; background:rgba(30,41,59,0.5); padding:0.5rem; border-radius:6px;">
                                <div>Trésorerie : <strong style="color:#94a3b8;">0 €</strong></div>
                                <div>Chantiers : <strong style="color:#94a3b8;">0 Chantier</strong></div>
                                <div>Flotte : <strong style="color:#94a3b8;">0 (Location)</strong></div>
                                <div>Effectif : <strong>1 Dirigeant</strong></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- TAB 2: CRÉATION D'ENTREPRISE -->
                <div id="acc-tab-create" class="acc-tab-content" style="display:none;">
                    <form id="form-create-company" onsubmit="handleCreateCompany(event)" style="background:rgba(15,23,42,0.6); border:1px solid var(--border); border-radius:8px; padding:1rem;">
                        <div class="grid-2-col" style="gap:0.75rem; margin-bottom:0.6rem;">
                            <div class="input-group">
                                <label class="input-label">Raison Sociale / Nom de l'Entreprise</label>
                                <input type="text" class="input-field" id="new-comp-name" required placeholder="Ex: Méditerranée VRD & Canalisations SAS">
                            </div>
                            <div class="input-group">
                                <label class="input-label">Forme Juridique</label>
                                <select class="select-field" id="new-comp-forme">
                                    <option value="SAS" selected>SAS / SASU</option>
                                    <option value="SARL">SARL / EURL</option>
                                    <option value="Artisan">Artisan Individuel / EI</option>
                                    <option value="Micro">Micro-Entreprise BTP</option>
                                </select>
                            </div>
                        </div>

                        <div class="grid-3-col" style="gap:0.75rem; margin-bottom:0.6rem;">
                            <div class="input-group">
                                <label class="input-label">Capital de Départ (€)</label>
                                <input type="number" class="input-field" id="new-comp-capital" value="50000" step="5000">
                            </div>
                            <div class="input-group">
                                <label class="input-label">Trésorerie / Caisse Active (€)</label>
                                <input type="number" class="input-field" id="new-comp-treasury" value="120000" step="10000">
                            </div>
                            <div class="input-group">
                                <label class="input-label">Ville / Siège d'Exploitation</label>
                                <input type="text" class="input-field" id="new-comp-city" value="Sète (Bassin de Thau)">
                            </div>
                        </div>

                        <div class="grid-2-col" style="gap:0.75rem; margin-bottom:0.75rem;">
                            <div class="input-group">
                                <label class="input-label">Spécialité Principale</label>
                                <select class="select-field" id="new-comp-specialite">
                                    <option value="vrd_terrassement" selected>VRD, Voirie & Terrassement Général</option>
                                    <option value="enrobes_routes">Application d'Enrobés & Chaussées</option>
                                    <option value="assainissement_aep">Canalisations, Assainissement & AEP</option>
                                    <option value="maconnerie_bordures">Maçonnerie VRD & Aménagements Urbains</option>
                                </select>
                            </div>
                            <div class="input-group">
                                <label class="input-label">Effectif Initial : <span id="new-comp-headcount-badge" style="color:#38bdf8; font-weight:800;">12 Salariés</span></label>
                                <input type="range" min="1" max="100" value="12" class="input-field" id="new-comp-headcount-slider" oninput="document.getElementById('new-comp-headcount-badge').textContent = this.value + ' Salariés'">
                            </div>
                        </div>

                        <div style="display:flex; justify-content:flex-end; gap:0.5rem;">
                            <button type="submit" class="btn btn-primary">🚀 Créer et Activer l'Entreprise</button>
                        </div>
                    </form>
                </div>

                <!-- TAB 3: MON IDENTITÉ & RÔLE DANS L'ENTREPRISE -->
                <div id="acc-tab-identity" class="acc-tab-content" style="display:none;">
                    <form id="form-user-identity" onsubmit="handleSaveUserIdentity(event)" style="background:rgba(15,23,42,0.6); border:1px solid var(--border); border-radius:8px; padding:1rem;">
                        <div class="grid-2-col" style="gap:0.75rem; margin-bottom:0.75rem;">
                            <div class="input-group">
                                <label class="input-label">Votre Nom & Prénom</label>
                                <input type="text" class="input-field" id="user-fullname" value="Jean DUPONT" required>
                            </div>
                            <div class="input-group">
                                <label class="input-label">Votre Fonction / Rôle dans la Société</label>
                                <select class="select-field" id="user-role-select" onchange="updateRolePreview(this.value)">
                                    <option value="patron" selected>👑 Direction Générale / Gérant / Patron</option>
                                    <option value="conduite">👷 Conduite de Travaux / Ingénieur Travaux</option>
                                    <option value="chef">🦺 Chef de Chantier / Maîtrise</option>
                                    <option value="compagnon">🛠️ Compagnon Terrain / Ouvrier VRD</option>
                                </select>
                            </div>
                        </div>

                        <!-- HIERARCHY HEADCOUNT SLIDER -->
                        <div style="background:#020617; border:1px solid var(--border); border-radius:6px; padding:0.85rem; margin-bottom:1rem;">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                                <label class="input-label" style="margin:0;">👥 Nombre de Collaborateurs sous votre Responsabilité :</label>
                                <span id="user-headcount-display" style="font-size:1.1rem; font-weight:900; color:#38bdf8;">24 Salariés</span>
                            </div>
                            <input type="range" min="0" max="150" value="24" id="user-headcount-slider" style="width:100%; cursor:pointer;" oninput="updateHeadcountSlider(this.value)">
                            <div style="display:flex; justify-content:space-between; font-size:0.7rem; color:#64748b; margin-top:2px;">
                                <span>0 (Solo / Indépendant)</span>
                                <span>50 (PME Régionale)</span>
                                <span>150+ (Groupe TP)</span>
                            </div>
                        </div>

                        <div style="display:flex; justify-content:flex-end;">
                            <button type="submit" class="btn btn-primary">💾 Enregistrer Mon Profil & Rôle</button>
                        </div>
                    </form>
                </div>

                <!-- TAB 4: SUPPRESSION / RÉINITIALISATION -->
                <div id="acc-tab-delete" class="acc-tab-content" style="display:none;">
                    <div style="background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.35); border-radius:8px; padding:1rem; margin-bottom:1rem;">
                        <h4 style="color:#ef4444; margin:0 0 0.5rem 0; font-size:1rem; display:flex; align-items:center; gap:0.4rem;">
                            <span>⚠️</span> Zone de Danger : Suppression & Remise à Zéro
                        </h4>
                        <p style="font-size:0.8rem; color:#fca5a5; line-height:1.4; margin-bottom:0.75rem;">
                            La suppression d'un compte efface les journaux de chantier, pointages, livraisons et personnalisations associées à cette entreprise.
                        </p>
                        <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
                            <button class="btn btn-danger" onclick="deleteActiveCompany()">🗑️ Supprimer l'Entreprise Active</button>
                            <button class="btn btn-secondary" onclick="resetAllDataFactory()">🔄 Réinitialiser Données d'Usine</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
"""

# Replace in section_modals.py from company-switch-modal to modal-add-livraison
pos_comp_start = text.find('company-switch-modal')
if pos_comp_start != -1:
    pos_modal_box_start = text.rfind('<div class="modal-backdrop"', 0, pos_comp_start)
    if pos_modal_box_start == -1:
        pos_modal_box_start = text.rfind('<div id="company-switch-modal"', 0, pos_comp_start)
    
    pos_modal_livraison = text.find('<!-- MODAL: AJOUTER BON DE LIVRAISON', pos_comp_start)
    if pos_modal_livraison != -1:
        text = text[:pos_modal_box_start] + new_account_modal_html + '\n\n' + text[pos_modal_livraison:]
        print("Replaced company-switch-modal with new_account_modal_html!")

with open("scripts/section_modals.py", "w", encoding="utf-8") as f:
    f.write(text)

print("scripts/section_modals.py updated successfully!")
