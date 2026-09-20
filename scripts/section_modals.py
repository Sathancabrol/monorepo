def get_modals():
    return """
    <!-- ========================================== -->
    <!-- MODALS & OVERLAYS                          -->
    <!-- ========================================== -->

    <!-- PROJECT DETAILS MODAL -->
    <div class="modal-backdrop" id="project-details-modal">
        <div class="modal-box" style="max-width:850px;">
            <div id="project-modal-body"></div>
            <div style="margin-top:1.5rem; text-align:right; border-top:1px solid rgba(51,65,85,0.5); padding-top:1rem;">
                <button class="btn btn-secondary" onclick="closeModal('project-details-modal')">Fermer la fiche</button>
            </div>
        </div>
    </div>

    <!-- VEHICLE DETAILS MODAL -->
    <div class="modal-backdrop" id="vehicle-details-modal">
        <div class="modal-box" style="max-width:750px;">
            <div id="vehicle-modal-body"></div>
            <div style="margin-top:1.5rem; text-align:right; border-top:1px solid rgba(51,65,85,0.5); padding-top:1rem;">
                <button class="btn btn-secondary" onclick="closeModal('vehicle-details-modal')">Fermer la fiche</button>
            </div>
        </div>
    </div>

    <!-- CATALOG ITEM MODAL -->
    <div class="modal-backdrop" id="catalog-item-modal">
        <div class="modal-box" style="max-width:700px;">
            <div id="catalog-item-modal-body"></div>
        </div>
    </div>

    <!-- SDP DETAIL MODAL -->
    <div class="modal-backdrop" id="sdp-detail-modal">
        <div class="modal-box" style="max-width:700px;">
            <div id="sdp-detail-modal-body"></div>
        </div>
    </div>

    <!-- DOCUMENT VIEWER MODAL -->
    <div class="modal-backdrop" id="doc-reader-modal">
        <div class="modal-box" style="max-width:800px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; border-bottom:1px solid rgba(51,65,85,0.5); padding-bottom:0.75rem;">
                <h3 style="font-size:1.2rem; font-weight:800; color:#38bdf8;" id="doc-reader-title">📄 Visualiseur de Document</h3>
                <button class="btn btn-secondary" style="padding:0.25rem 0.5rem;" onclick="closeModal('doc-reader-modal')">✕</button>
            </div>
            <div id="doc-reader-body" style="background:rgba(15,23,42,0.8); border:1px solid rgba(51,65,85,0.6); padding:1rem; border-radius:6px; max-height:450px; overflow-y:auto; font-family:'JetBrains Mono', monospace; font-size:0.85rem; line-height:1.5; color:#cbd5e1; white-space:pre-wrap;"></div>
            <div style="margin-top:1rem; display:flex; justify-content:space-between; align-items:center;">
                <span class="badge badge-success">Document Certifié Conforme CCTP</span>
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
