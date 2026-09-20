import re
import json
from pathlib import Path

TARGET_TEMPLATE = Path("/home/user/monorepo/projects/btp-conduite-travaux/template.html")

with open(TARGET_TEMPLATE, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add CSS for stock status pulsing badges and project detail modals
css_injection = """
/* STOCK STATUS PULSING BADGES */
@keyframes pulseRed {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
    70% { transform: scale(1.1); box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}
.stock-badge-out {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(239, 68, 68, 0.15);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.4);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.68rem;
    font-weight: 700;
}
.stock-dot-red {
    width: 7px;
    height: 7px;
    background: #ef4444;
    border-radius: 50%;
    animation: pulseRed 1.5s infinite;
}
.stock-badge-in {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(16, 185, 129, 0.15);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.4);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.68rem;
    font-weight: 700;
}
.stock-badge-transit {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(245, 158, 11, 0.15);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.4);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.68rem;
    font-weight: 700;
}
.project-card-clickable {
    cursor: pointer;
    transition: all 0.2s ease;
}
.project-card-clickable:hover {
    transform: translateY(-2px);
    border-color: var(--cyan) !important;
    box-shadow: 0 4px 15px rgba(6, 182, 212, 0.15);
}
"""

if "/* STOCK STATUS PULSING BADGES */" not in text:
    text = text.replace("</style>", css_injection + "\n</style>")
    print("Injected stock badge CSS!")

# 2. Update navigation tab labels: rename safety tab
text = text.replace("{ id: 'aipr_safety', label: '⚡ Sécurité Gaz/Élec' }", "{ id: 'safety', label: '🛡️ Sécurité & Prévention' }")
text = text.replace("id=\"tab-aipr_safety\"", "id=\"tab-safety\"")

# 3. Add Project Details Modal HTML into modal section
project_modal_html = """
<!-- MODAL PROJECT DETAILS POPUP -->
<div class="modal-backdrop" id="modal-project-details">
    <div class="modal-box" style="max-width:850px; max-height:90vh; overflow-y:auto;" id="project-details-content">
        <!-- Populated by JS -->
    </div>
</div>

<!-- MODAL ITEM DETAIL SHEET POPUP -->
<div class="modal-backdrop" id="modal-item-details">
    <div class="modal-box" style="max-width:650px;" id="item-details-content">
        <!-- Populated by JS -->
    </div>
</div>

<!-- MODAL ADD/EDIT SUPPLIER -->
<div class="modal-backdrop" id="modal-supplier-edit">
    <div class="modal-box" style="max-width:550px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; border-bottom:1px solid var(--border); padding-bottom:0.5rem;">
            <h3 style="font-size:1.1rem; font-weight:800; color:var(--cyan);" id="supplier-modal-title">➕ Ajouter / Modifier un Fournisseur</h3>
            <button class="btn-secondary" style="padding:0.2rem 0.5rem;" onclick="closeModal('modal-supplier-edit')">✕</button>
        </div>
        <input type="hidden" id="sup-edit-id">
        <div class="input-group">
            <label class="input-label">Nom du Fournisseur / Centrale :</label>
            <input type="text" class="input-field" id="sup-edit-name" placeholder="ex: Carrières du Littoral">
        </div>
        <div class="input-group">
            <label class="input-label">Spécialité & Matériaux :</label>
            <input type="text" class="input-field" id="sup-edit-spec" placeholder="ex: GNT 0/31.5, Béton C25/30, Bordures">
        </div>
        <div class="grid-2">
            <div class="input-group">
                <label class="input-label">Distance Moyenne Chantier (km) :</label>
                <input type="number" class="input-field" id="sup-edit-dist" value="12">
            </div>
            <div class="input-group">
                <label class="input-label">Indice de Prix :</label>
                <select class="input-field" id="sup-edit-price">
                    <option value="€ (Très Économique)">€ (Très Économique)</option>
                    <option value="€€ (Compétitif Standard)" selected>€€ (Compétitif Standard)</option>
                    <option value="€€€ (Haut de Gamme / Spécifique)">€€€ (Haut de Gamme / Spécifique)</option>
                </select>
            </div>
        </div>
        <div class="grid-2">
            <div class="input-group">
                <label class="input-label">Téléphone / Contact Direct :</label>
                <input type="text" class="input-field" id="sup-edit-phone" placeholder="04 67 00 00 00">
            </div>
            <div class="input-group">
                <label class="input-label">Note Qualité & Ponctualité (sur 5) :</label>
                <input type="number" step="0.1" class="input-field" id="sup-edit-rating" value="4.8">
            </div>
        </div>
        <div class="input-group">
            <label class="input-label">Délai Moyen de Livraison :</label>
            <input type="text" class="input-field" id="sup-edit-delay" placeholder="ex: Livraison 24h ou navette matin">
        </div>
        <button class="btn-primary" style="width:100%; justify-content:center; margin-top:0.5rem;" onclick="saveSupplier()">
            💾 Enregistrer dans le Répertoire Fournisseurs
        </button>
    </div>
</div>
"""

if "<!-- MODAL PROJECT DETAILS POPUP -->" not in text:
    text = text.replace('<div class="modal-backdrop" id="modal-add-vehicle">', project_modal_html + '\n<div class="modal-backdrop" id="modal-add-vehicle">')
    print("Injected modals HTML!")

with open(TARGET_TEMPLATE, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated template.html base structure!")
