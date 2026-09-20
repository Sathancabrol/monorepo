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
