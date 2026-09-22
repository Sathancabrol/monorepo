def get_modals():
    return """
    <!-- ========================================== -->
    <!-- MODALS & OVERLAYS                          -->
    <!-- ========================================== -->

    <!-- 1. PROJECT DETAILS MODAL (TIMELINE + GIS LAYERS + LOT BREAKDOWN) -->
    <div class="modal-backdrop" id="project-details-modal">
        <div class="modal-box" style="max-width:960px;">
            <div id="project-modal-body"></div>
            <div style="margin-top:1.5rem; text-align:right; border-top:1px solid rgba(51,65,85,0.5); padding-top:1rem;">
                <button class="btn btn-secondary" onclick="closeModal('project-details-modal')">Fermer la fiche chantier</button>
            </div>
        </div>
    </div>

    <!-- 2. PLANNING AGENDA TASK INSPECTION MODAL -->
    <div class="modal-backdrop" id="task-details-modal">
        <div class="modal-box" style="max-width:720px;">
            <div id="task-modal-body"></div>
            <div style="margin-top:1.5rem; display:flex; justify-content:space-between; align-items:center; border-top:1px solid rgba(51,65,85,0.5); padding-top:1rem;">
                <span class="badge badge-success" id="task-modal-badge">Tâche Planifiée</span>
                <button class="btn btn-secondary" onclick="closeModal('task-details-modal')">Fermer</button>
            </div>
        </div>
    </div>

    <!-- 3. VEHICLE ULTRA-DETAILED MODAL (PHOTOS + SVG + ONBOARD CAM + SPECS) -->
    <div class="modal-backdrop" id="vehicle-details-modal">
        <div class="modal-box" style="max-width:880px;">
            <div id="vehicle-modal-body"></div>
            <div style="margin-top:1.5rem; text-align:right; border-top:1px solid rgba(51,65,85,0.5); padding-top:1rem;">
                <button class="btn btn-secondary" onclick="closeModal('vehicle-details-modal')">Fermer la fiche engin</button>
            </div>
        </div>
    </div>

    <!-- 4. CATALOG ITEM MODAL -->
    <div class="modal-backdrop" id="catalog-item-modal">
        <div class="modal-box" style="max-width:720px;">
            <div id="catalog-item-modal-body"></div>
        </div>
    </div>

    <!-- 4b. DEPOT ACTIVE ZONE COMPLETE SHEET MODAL -->
    <div class="modal-backdrop" id="depot-zone-modal">
        <div class="modal-box" style="max-width:850px;">
            <div id="depot-zone-modal-body"></div>
            <div style="margin-top:1.5rem; display:flex; justify-content:space-between; align-items:center; border-top:1px solid rgba(51,65,85,0.5); padding-top:1rem;">
                <button class="btn btn-primary" onclick="alert('Bon de sortie / inventaire de zone exporté en PDF.');">📄 Exporter Fiche Inventaire</button>
                <button class="btn btn-secondary" onclick="closeModal('depot-zone-modal')">Fermer la fiche zone</button>
            </div>
        </div>
    </div>

    <!-- 5. SDP DETAIL MODAL -->
    <div class="modal-backdrop" id="sdp-detail-modal">
        <div class="modal-box" style="max-width:720px;">
            <div id="sdp-detail-modal-body"></div>
        </div>
    </div>

    <!-- 6. HR & AI AGENT DETAIL MODAL -->
    <div class="modal-backdrop" id="employee-detail-modal">
        <div class="modal-box" style="max-width:650px;">
            <div id="employee-modal-body"></div>
            <div style="margin-top:1.25rem; text-align:right; border-top:1px solid rgba(51,65,85,0.5); padding-top:0.75rem;">
                <button class="btn btn-secondary" onclick="closeModal('employee-detail-modal')">Fermer</button>
            </div>
        </div>
    </div>

    <!-- 7. RDC MULTI-CAMERA & LIVE CAPTURE MODAL -->
    <div class="modal-backdrop" id="rdc-camera-modal">
        <div class="modal-box" style="max-width:800px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; border-bottom:1px solid rgba(51,65,85,0.5); padding-bottom:0.5rem;">
                <h3 style="font-size:1.2rem; font-weight:800; color:#38bdf8;">📷 Module Caméra Terrain & Prise de Vue Télémétrique</h3>
                <button class="btn btn-secondary" style="padding:0.2rem 0.5rem;" onclick="closeModal('rdc-camera-modal')">✕</button>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem; margin-bottom:1rem;">
                <div>
                    <label class="input-label">Source Vidéo / Capteur</label>
                    <select id="camera-source-select" class="input-field" onchange="updateCameraFeedView()">
                        <option value="webcam">🎥 Webcam Locale (Direct)</option>
                        <option value="pelle">🚜 Caméra Tourelle Pelle 24t</option>
                        <option value="drone">🛰️ Drone Aérien LiDAR RTK</option>
                        <option value="phone">📱 Téléphone Compagnon (Visio)</option>
                        <option value="fixe">📹 Caméra Chantier Entrée Est</option>
                    </select>
                </div>
                <div>
                    <label class="input-label">Affecter au Chantier</label>
                    <select id="camera-project-select" class="input-field">
                        <option value="Giratoire RD906 Alès">Giratoire RD906 Alès</option>
                        <option value="ZAC Littoral Sète">ZAC Littoral Sète</option>
                        <option value="Centre Ancien Pézenas">Centre Ancien Pézenas</option>
                        <option value="Voie Verte Montpellier">Voie Verte Montpellier</option>
                    </select>
                </div>
            </div>

            <div style="background:#000; border:2px solid var(--cyan); border-radius:8px; height:320px; position:relative; overflow:hidden; display:flex; align-items:center; justify-content:center;">
                <video id="live-webcam-element" autoplay playsinline muted style="width:100%; height:100%; object-fit:cover; display:none;"></video>
                <div id="simulated-camera-feed" style="width:100%; height:100%; background:radial-gradient(circle at center, #1e293b 0%, #090d16 100%); display:flex; flex-direction:column; align-items:center; justify-content:center; color:#38bdf8;">
                    <div style="font-size:3rem; margin-bottom:0.5rem;" id="cam-feed-icon">🚜</div>
                    <div style="font-weight:800; font-size:1.1rem; color:#f8fafc;" id="cam-feed-title">FLUX TOURELLE PELLE 24T LIEBHERR</div>
                    <div style="font-size:0.8rem; font-family:'JetBrains Mono'; color:#94a3b8; margin-top:4px;">1080p 60fps • Latence 42ms • Signal 5G 98%</div>
                </div>

                <!-- HUD TELEMETRY OVERLAY -->
                <div style="position:absolute; top:12px; left:12px; background:rgba(15,23,42,0.85); padding:4px 8px; border-radius:4px; font-family:'JetBrains Mono'; font-size:0.75rem; color:var(--emerald); border:1px solid rgba(16,185,129,0.4);">
                    REC ● <span id="cam-live-time">00:00:00</span>
                </div>
                <div style="position:absolute; top:12px; right:12px; background:rgba(15,23,42,0.85); padding:4px 8px; border-radius:4px; font-family:'JetBrains Mono'; font-size:0.75rem; color:#38bdf8; border:1px solid rgba(56,189,248,0.4);">
                    GPS: 44.1284° N, 4.0833° E • Alt: 142m
                </div>
                <div style="position:absolute; bottom:12px; left:12px; background:rgba(15,23,42,0.85); padding:4px 8px; border-radius:4px; font-family:'JetBrains Mono'; font-size:0.75rem; color:#facc15;">
                    AIPR: Piquetage Conforme Gaz MPB
                </div>
            </div>

            <div style="margin-top:1rem; display:flex; justify-content:space-between; align-items:center;">
                <button class="btn btn-secondary" onclick="startWebcamCapture()">🔌 Activer Ma Webcam</button>
                <div style="display:flex; gap:0.5rem;">
                    <button class="btn btn-secondary" onclick="closeModal('rdc-camera-modal')">Annuler</button>
                    <button class="btn btn-primary" onclick="capturePhotoForRDC()">💾 Capturer & Intégrer au Journal RDC</button>
                </div>
            </div>
        </div>
    </div>

    <!-- 8. SAFETY CRISIS & HEATMAP SIMULATOR MODAL -->
    <div class="modal-backdrop" id="safety-crisis-modal">
        <div class="modal-box" style="max-width:850px;">
            <div id="safety-crisis-modal-body"></div>
            <div style="margin-top:1.5rem; text-align:right; border-top:1px solid rgba(51,65,85,0.5); padding-top:1rem;">
                <button class="btn btn-secondary" onclick="closeModal('safety-crisis-modal')">Fermer la simulation d'urgence</button>
            </div>
        </div>
    </div>

    <!-- 9. DOCUMENT VIEWER MODAL -->
    <div class="modal-backdrop" id="doc-reader-modal">
        <div class="modal-box" style="max-width:800px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; border-bottom:1px solid rgba(51,65,85,0.5); padding-bottom:0.75rem;">
                <h3 style="font-size:1.2rem; font-weight:800; color:#38bdf8;" id="doc-reader-title">📄 Visualiseur de Document CCTP</h3>
                <button class="btn btn-secondary" style="padding:0.25rem 0.5rem;" onclick="closeModal('doc-reader-modal')">✕</button>
            </div>
            <div id="doc-reader-body" style="background:rgba(15,23,42,0.8); border:1px solid rgba(51,65,85,0.6); padding:1rem; border-radius:6px; max-height:450px; overflow-y:auto; font-family:'JetBrains Mono', monospace; font-size:0.85rem; line-height:1.5; color:#cbd5e1; white-space:pre-wrap;"></div>
            <div style="margin-top:1rem; display:flex; justify-content:space-between; align-items:center;">
                <span class="badge badge-success">Document Conforme CCAG / CCTP</span>
                <button class="btn btn-primary" onclick="alert('Export PDF lancé...'); closeModal('doc-reader-modal');">📥 Télécharger</button>
            </div>
        </div>
    </div>

    <!-- 8. COMPANY SWITCHER MODAL (MULTI-PROFILES) -->
    <div class="modal-backdrop" id="company-switch-modal">
        <div class="modal-box" style="max-width:900px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; border-bottom:1px solid rgba(51,65,85,0.7); padding-bottom:0.75rem;">
                <div>
                    <h3 style="color:#38bdf8; font-size:1.3rem; font-weight:900;">🏢 Sélecteur d'Entreprise TP & Profils d'Exploitation</h3>
                    <div style="font-size:0.8rem; color:#94a3b8;">Basculez instantanément l'environnement, la trésorerie, la flotte, les équipes et les chantiers</div>
                </div>
                <button class="btn btn-secondary" style="padding:0.2rem 0.5rem;" onclick="closeModal('company-switch-modal')">✕</button>
            </div>

            <div class="grid-2" style="gap:1rem;">
                <!-- 1. OCCITANIE TP (ESTABLISHED) -->
                <div class="card company-profile-card active" id="prof-card-occitanie_tp" style="border:2px solid var(--cyan); background:rgba(15,23,42,0.95); cursor:pointer; padding:1.1rem; border-radius:8px;" onclick="switchCompanyProfile('occitanie_tp')">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
                        <span class="badge badge-info">PME Établie Régionale</span>
                        <span class="badge badge-success" id="prof-active-badge-occitanie_tp">Active</span>
                    </div>
                    <h4 style="font-size:1.05rem; font-weight:900; color:#f8fafc; margin-bottom:0.3rem;">🏢 1. Occitanie Travaux Publics & VRD SAS</h4>
                    <p style="font-size:0.78rem; color:#cbd5e1; line-height:1.4; margin-bottom:0.75rem;">Entreprise générale de VRD et terrassement en Occitanie. Flotte complète 6 engins, marchés publics Alès, Sète, Pézenas, Montpellier.</p>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:0.75rem; background:rgba(30,41,59,0.5); padding:0.6rem; border-radius:6px;">
                        <div>Trésorerie Caisse : <strong style="color:var(--emerald);">485 200 €</strong></div>
                        <div>Chantiers Actifs : <strong style="color:#38bdf8;">4 Chantiers (3.4 M€)</strong></div>
                        <div>Flotte Engins : <strong style="color:var(--amber);">6 Engins lourds</strong></div>
                        <div>Effectif : <strong>24 Collaborateurs</strong></div>
                    </div>
                </div>

                <!-- 2. VIERGE / COMPTE NEUF -->
                <div class="card company-profile-card" id="prof-card-compte_neuf" style="border:1px solid rgba(51,65,85,0.8); background:rgba(15,23,42,0.95); cursor:pointer; padding:1.1rem; border-radius:8px;" onclick="switchCompanyProfile('compte_neuf')">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
                        <span class="badge badge-warning">Compte Vierge / Typique</span>
                        <span class="badge" id="prof-active-badge-compte_neuf" style="display:none; background:var(--emerald);">Active</span>
                    </div>
                    <h4 style="font-size:1.05rem; font-weight:900; color:#f8fafc; margin-bottom:0.3rem;">📄 2. Nouvelle Entreprise TP (Démarrage Zéro)</h4>
                    <p style="font-size:0.78rem; color:#cbd5e1; line-height:1.4; margin-bottom:0.75rem;">Profil vierge sans fond ni chantier engagé. Idéal pour configurer et chiffrer une nouvelle entreprise TP à partir d'une page blanche.</p>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:0.75rem; background:rgba(30,41,59,0.5); padding:0.6rem; border-radius:6px;">
                        <div>Trésorerie Caisse : <strong style="color:#94a3b8;">0 €</strong></div>
                        <div>Chantiers Actifs : <strong style="color:#94a3b8;">0 Chantier</strong></div>
                        <div>Flotte Engins : <strong style="color:#94a3b8;">0 (Location)</strong></div>
                        <div>Effectif : <strong>1 Dirigeant</strong></div>
                    </div>
                </div>

                <!-- 3. STAGIAIRE TP / COURS CONDUITE TRAVAUX -->
                <div class="card company-profile-card" id="prof-card-stagiaire_tp" style="border:1px solid rgba(51,65,85,0.8); background:rgba(15,23,42,0.95); cursor:pointer; padding:1.1rem; border-radius:8px;" onclick="switchCompanyProfile('stagiaire_tp')">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
                        <span class="badge" style="background:rgba(168,85,247,0.2); color:#c084fc;">Dossiers de Cours & Formation</span>
                        <span class="badge" id="prof-active-badge-stagiaire_tp" style="display:none; background:var(--emerald);">Active</span>
                    </div>
                    <h4 style="font-size:1.05rem; font-weight:900; color:#f8fafc; margin-bottom:0.3rem;">🎓 3. Stagiaire TP & Conduite de Travaux (Études M4-L)</h4>
                    <p style="font-size:0.78rem; color:#cbd5e1; line-height:1.4; margin-bottom:0.75rem;">Simulation basée sur les dossiers réels du repo : DCE Giratoire Barbazan M4-L, Lotissement Aurouer 2021, Déviation Noé, fiches de tâches et ratios FNTP.</p>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:0.75rem; background:rgba(30,41,59,0.5); padding:0.6rem; border-radius:6px;">
                        <div>Trésorerie Caisse : <strong style="color:var(--emerald);">150 000 €</strong></div>
                        <div>Chantiers Référence : <strong style="color:#c084fc;">3 Dossiers Réels</strong></div>
                        <div>Flotte Engins : <strong style="color:var(--amber);">3 Engins École</strong></div>
                        <div>Effectif : <strong>1 Stagiaire + 8 Comp.</strong></div>
                    </div>
                </div>

                <!-- 4. ARTISAN PERSO (2k€ + BUREAU + EPI) -->
                <div class="card company-profile-card" id="prof-card-artisan_2k" style="border:1px solid rgba(51,65,85,0.8); background:rgba(15,23,42,0.95); cursor:pointer; padding:1.1rem; border-radius:8px;" onclick="switchCompanyProfile('artisan_2k')">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
                        <span class="badge badge-warning">Amorçage Artisanal 2 000 €</span>
                        <span class="badge" id="prof-active-badge-artisan_2k" style="display:none; background:var(--emerald);">Active</span>
                    </div>
                    <h4 style="font-size:1.05rem; font-weight:900; color:#f8fafc; margin-bottom:0.3rem;">🦺 4. Artisan TP Sud VRD (Perso 2k€ + Bureau + EPI)</h4>
                    <p style="font-size:0.78rem; color:#cbd5e1; line-height:1.4; margin-bottom:0.75rem;">Démarrage avec 2 000 € de capital, bureau loué en pépinière, lot complet d'EPI certifiés (Casques, gilets Cl.2, chaussures S3), outillage laser et réfection tranchée.</p>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:0.75rem; background:rgba(30,41,59,0.5); padding:0.6rem; border-radius:6px;">
                        <div>Fonds de Départ : <strong style="color:var(--emerald);">2 000 €</strong></div>
                        <div>Actifs : <strong style="color:#38bdf8;">Bureau + Lot EPI + Laser</strong></div>
                        <div>Chantier Actuel : <strong style="color:var(--amber);">1 Tranchée Pézenas (6.5k€)</strong></div>
                        <div>Effectif : <strong>1 Artisan AIPR + 1 Aide</strong></div>
                    </div>
                </div>
            </div>

            <div style="margin-top:1.25rem; display:flex; justify-content:space-between; align-items:center; border-top:1px solid rgba(51,65,85,0.5); padding-top:0.75rem;">
                <span style="font-size:0.78rem; color:#94a3b8;">Cliquez sur une entreprise pour charger immédiatement son écosystème complet.</span>
                <button class="btn btn-secondary" onclick="closeModal('company-switch-modal')">Fermer</button>
            </div>
        </div>
    </div>

    <!-- TACTICAL WHEEL POPUP -->
    <div id="tactical-wheel-menu" style="display:none; position:fixed; bottom:90px; right:25px; z-index:9999; background:rgba(15,23,42,0.95); backdrop-filter:blur(16px); border:1px solid var(--border); border-radius:12px; padding:1rem; box-shadow:0 10px 30px rgba(0,0,0,0.6); min-width:220px;">
        <div style="font-size:0.8rem; font-weight:800; color:#94a3b8; text-transform:uppercase; margin-bottom:0.75rem; border-bottom:1px solid rgba(51,65,85,0.5); padding-bottom:0.4rem;">
            ⚡ Actions Rapides
        </div>
        <div style="display:flex; flex-direction:column; gap:0.5rem;">
            <button class="btn btn-secondary" style="text-align:left; font-size:0.85rem;" onclick="quickAction('planning')">📅 Ouvrir Planning</button>
            <button class="btn btn-secondary" style="text-align:left; font-size:0.85rem;" onclick="quickAction('simulator')">🛰️ Watch Tower 3D</button>
            <button class="btn btn-secondary" style="text-align:left; font-size:0.85rem;" onclick="quickAction('rdc')">📋 Saisir Rapport RDC</button>
            <button class="btn btn-secondary" style="text-align:left; font-size:0.85rem;" onclick="quickAction('opbtp')">🦺 Calculer Signalisation</button>
            <button class="btn btn-secondary" style="text-align:left; font-size:0.85rem;" onclick="quickAction('sdp')">💰 Tableau Croisé DQE</button>
        </div>
    </div>
"""
