import re
from pathlib import Path

TARGET = Path("/home/user/monorepo/projects/btp-conduite-travaux/template.html")

with open(TARGET, "r", encoding="utf-8") as f:
    text = f.read()

# Replace Tool Catalog + Order Modal + Item Details Modal
idx_cat_start = text.find("// TAB 7: TOOLS & MATERIALS CATALOG")
idx_hr_start = text.find("// TAB 8: HR & VEHICLE ORGANIGRAMME")

if idx_cat_start == -1 or idx_hr_start == -1:
    print("Error locating catalog/hr markers in template.html")
    exit(1)

new_catalog_js = """// TAB 7: TOOLS & MATERIALS CATALOG (WITH STOCK STATUS BADGES & 3D DETAIL SHEETS)
    function renderToolCatalog() {
        const grid = document.getElementById('catalog-items-grid');
        if (!grid) return;

        let items = [];
        if (catalogFilter === 'materials') {
            items = (companyData.materials_catalog || []).map(m => ({
                ...m,
                is_material: true,
                description: `Fournisseur : ${m.fournisseur} | Norme : ${m.norme} | Stock : ${m.stock}`,
                prix_achat_neuf: `${m.prix_unitaire.toFixed(2)} € / ${m.unit}`,
                tarif_location_jour: 'Livraison sur chantier',
                conso_moyenne: m.conditionnement,
                rendement: 'Conforme CCTP',
                stock_status: m.id === 'mat_07' ? 'out_of_stock' : (m.id === 'mat_10' ? 'in_transit' : 'in_stock'),
                stock_qty: m.stock || 'En stock',
                weight: m.conditionnement || 'Palette 900kg'
            }));
        } else {
            const allTools = companyData.tool_catalog || [];
            items = allTools.filter(t => {
                if (catalogFilter === 'all') return true;
                if (catalogFilter === 'outillage_main') return t.task === 'outillage_main' || t.task === 'securite_epi';
                return t.task === catalogFilter;
            });
        }

        grid.innerHTML = items.map(item => {
            let stockBadge = '';
            if (item.stock_status === 'out_of_stock') {
                stockBadge = '<span class="stock-badge-out"><span class="stock-dot-red"></span> En Rupture (Réappro 3j)</span>';
            } else if (item.stock_status === 'in_transit') {
                stockBadge = '<span class="stock-badge-transit">🚚 Livraison en cours</span>';
            } else {
                stockBadge = '<span class="stock-badge-in">📦 En Stock</span>';
            }

            return `
                <div class="catalog-card">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div style="display:flex; align-items:center; gap:0.5rem;">
                            <span style="font-size:1.6rem;">${item.icon || '🔧'}</span>
                            <div>
                                <div style="font-weight:700; font-size:0.88rem; color:var(--text-main);">${item.name}</div>
                                <div style="font-size:0.7rem; color:var(--cyan);">${item.category}</div>
                            </div>
                        </div>
                        ${stockBadge}
                    </div>
                    <p style="font-size:0.75rem; color:var(--text-muted); line-height:1.5; margin:0.4rem 0;">${item.description}</p>
                    <div style="background:var(--bg); padding:0.6rem; border-radius:7px; font-size:0.72rem; display:grid; grid-template-columns:1fr 1fr; gap:0.35rem; margin-bottom:0.4rem;">
                        <div>Prix / Unité : <b style="color:var(--text-main);">${item.prix_achat_neuf}</b></div>
                        <div>Dispo / Loc : <b style="color:var(--emerald);">${item.tarif_location_jour}</b></div>
                        <div>Conditionnement : <b>${item.conso_moyenne}</b></div>
                        <div>Rendement : <b style="color:var(--cyan);">${item.rendement}</b></div>
                    </div>
                    <div style="display:flex; gap:0.4rem; margin-top:0.3rem;">
                        <button class="btn-primary" style="flex:1; justify-content:center; font-size:0.72rem; padding:0.4rem;" onclick="openOrderModal('${item.id}', '${item.name.replace(/'/g, "\\\\'")}', '${item.prix_achat_neuf}')">
                            🛒 Commander
                        </button>
                        <button class="btn-secondary" style="font-size:0.72rem; padding:0.4rem;" onclick="openItemDetailSheet('${item.id}')">
                            🔍 Fiche Détails
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }

    function filterCatalog(taskKey, btn) {
        catalogFilter = taskKey;
        document.querySelectorAll('#catalog-filter-bar button').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
        renderToolCatalog();
    }

    function openItemDetailSheet(itemId) {
        let item = (companyData.tool_catalog || []).find(t => t.id === itemId);
        if (!item) {
            const mat = (companyData.materials_catalog || []).find(m => m.id === itemId);
            if (mat) {
                item = {
                    ...mat,
                    is_material: true,
                    prix_achat_neuf: `${mat.prix_unitaire.toFixed(2)} € / ${mat.unit}`,
                    tarif_location_jour: 'Livraison sur chantier',
                    conso_moyenne: mat.conditionnement,
                    rendement: 'Conforme CCTP',
                    stock_qty: mat.stock || 'Sur stock régional',
                    weight: mat.conditionnement || 'Palette standard',
                    supplier: mat.fournisseur,
                    impact_qualite: 'Certification NF EN'
                };
            }
        }
        if (!item) return;

        const content = document.getElementById('item-details-content');
        content.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1rem; border-bottom:1px solid var(--border); padding-bottom:0.6rem;">
                <div style="display:flex; align-items:center; gap:0.6rem;">
                    <span style="font-size:2.2rem;">${item.icon || '🔧'}</span>
                    <div>
                        <h3 style="font-size:1.15rem; font-weight:800; color:var(--cyan);">${item.name}</h3>
                        <div style="font-size:0.75rem; color:var(--text-muted);">${item.category} — ${item.task_label || 'Matériau VRD'}</div>
                    </div>
                </div>
                <button class="btn-secondary" style="padding:0.2rem 0.5rem;" onclick="closeModal('modal-item-details')">✕</button>
            </div>

            <!-- Wireframe / Visual simulation card -->
            <div style="background:#020617; border:1px solid var(--border); border-radius:8px; padding:0.8rem; margin-bottom:1rem; text-align:center;">
                <div style="font-size:0.72rem; color:var(--cyan); font-family:var(--font-mono); margin-bottom:0.4rem;">📐 MODÉLISATION 3D & COTES NORMALISÉES</div>
                <div style="font-size:1.8rem; margin:0.5rem 0;">${item.icon || '📦'} ──────── 📐 ──────── 🛡️</div>
                <div style="font-size:0.72rem; color:var(--text-muted);">Poids / Masse : <b>${item.weight || 'Standard'}</b> | Conditionnement : <b>${item.conso_moyenne || 'Unité'}</b></div>
            </div>

            <div class="grid-2" style="margin-bottom:1rem;">
                <div style="background:var(--bg); padding:0.8rem; border-radius:8px; font-size:0.75rem; line-height:1.8;">
                    <div style="font-weight:700; color:var(--cyan); margin-bottom:0.2rem;">📊 Caractéristiques Commerciales :</div>
                    <div>Prix Unitaire Achat : <b style="color:var(--text-main);">${item.prix_achat_neuf}</b></div>
                    <div>Tarif Location / Mise à Dispo : <b style="color:var(--emerald);">${item.tarif_location_jour}</b></div>
                    <div>Fournisseur Référencé : <b>${item.supplier || 'Centrale Partenaire'}</b></div>
                    <div>État du Stock : <b style="color:var(--emerald);">${item.stock_qty || 'Disponible'}</b></div>
                </div>
                <div style="background:var(--bg); padding:0.8rem; border-radius:8px; font-size:0.75rem; line-height:1.8;">
                    <div style="font-weight:700; color:var(--emerald); margin-bottom:0.2rem;">🛡️ Conformité & Sécurité :</div>
                    <div>Habilitation / CACES : <b>${item.caces || 'Notice constructeur & EPI'}</b></div>
                    <div>Rendement Théorique : <b>${item.rendement || 'Conforme CCTP'}</b></div>
                    <div>Impact Qualité : <b style="color:var(--cyan);">${item.impact_qualite || 'Zéro non-conformité'}</b></div>
                </div>
            </div>

            <div style="display:flex; justify-content:space-between; gap:0.5rem;">
                <button class="btn-secondary" style="font-size:0.75rem;" onclick="closeModal('modal-item-details')">Fermer</button>
                <button class="btn-primary" style="font-size:0.75rem;" onclick="closeModal('modal-item-details'); openOrderModal('${item.id}', '${item.name.replace(/'/g, "\\\\'")}', '${item.prix_achat_neuf}')">
                    🛒 Commander cet Article
                </button>
            </div>
        `;

        openModal('modal-item-details');
    }

    function openOrderModal(itemId, itemName, itemPrice) {
        document.getElementById('order-modal-title').innerText = `🛒 Commande : ${itemName}`;
        const body = document.getElementById('order-modal-body');
        body.innerHTML = `
            <div class="input-group">
                <label class="input-label">Article / Matériau :</label>
                <input type="text" class="input-field" value="${itemName} (${itemPrice})" readonly>
            </div>
            <div class="grid-2">
                <div class="input-group">
                    <label class="input-label">Chantier de Destination :</label>
                    <select class="input-field" id="order-dest-project">
                        <option value="Giratoire RD906 Alès">Giratoire RD906 Alès</option>
                        <option value="ZAC Littoral Sète">ZAC Littoral Sète</option>
                        <option value="Centre Ancien Pézenas">Centre Ancien Pézenas</option>
                        <option value="Voie Verte Montpellier">Voie Verte Montpellier</option>
                    </select>
                </div>
                <div class="input-group">
                    <label class="input-label">Quantité à Commander :</label>
                    <input type="number" class="input-field" id="order-quantity" value="10">
                </div>
            </div>
            <div class="input-group">
                <label class="input-label">Date de Livraison Souhaitée :</label>
                <input type="date" class="input-field" id="order-delivery-date" value="2026-09-22">
            </div>
            <button class="btn-primary" style="justify-content:center; margin-top:0.5rem;" onclick="submitOrder('${itemName.replace(/'/g, "\\\\'")}')">
                💳 Valider Bon de Commande & Déduire de la Caisse
            </button>
        `;
        openModal('modal-order-item');
    }

    function submitOrder(itemName) {
        const qty = parseInt(document.getElementById('order-quantity').value || 10);
        const proj = document.getElementById('order-dest-project').value;
        const totalCost = qty * 45;

        caisseBalance -= totalCost;
        updateCaisseDisplay();
        closeModal('modal-order-item');
        logCockpit(`🛒 Bon de commande #${Math.floor(1000 + Math.random()*9000)} émis pour ${qty}x ${itemName} sur ${proj} (-${totalCost} €).`, 'ok');
        alert(`Bon de commande validé avec succès pour ${proj} ! Trésorerie actualisée (-${totalCost} €).`);
    }

"""

text = text[:idx_cat_start] + new_catalog_js + text[idx_hr_start:]

# Replace OPBTP Calculator and Canvas
idx_opbtp_start = text.find("// TAB 9: OPBTP SIGNAGE CALCULATOR")
idx_fleet_start = text.find("// TAB 6: FLEET CRUD & FILTERING")

if idx_opbtp_start == -1 or idx_fleet_start == -1:
    print("Error locating opbtp markers in template.html")
    exit(1)

new_opbtp_js = """// TAB 9: OPBTP SIGNAGE CALCULATOR & DYNAMIC ILLUSTRATED CANVAS
    function calculateSignage() {
        const jType = document.getElementById('opbtp-job-type')?.value || 'voirie';
        const wType = document.getElementById('opbtp-work-type')?.value || 'alternat_feux';
        const rType = document.getElementById('opbtp-road-type')?.value || 'bidirectionnelle';
        const period = document.getElementById('opbtp-period')?.value || 'jour';
        const box = document.getElementById('opbtp-results-box');

        let signs = [];
        let distances = "150 m / 100 m / 50 m";
        let conesSpacing = "5 mètres";

        if (rType === 'urbain' || rType === 'rue_etroite') {
            distances = "50 m / 30 m / 10 m";
            conesSpacing = "2 mètres";
        }

        if (wType === 'alternat_feux') {
            signs = [
                "⚠️ <b>Panneau AK5 (Travaux) :</b> Implanté à 150m (Campagne) ou 50m (Urbain)",
                "🚦 <b>Panneau AK17 (Feux Temporaires) :</b> Implanté à 100m (Campagne) ou 30m (Urbain)",
                "⛔ <b>Panneau B14 (Limitation 50 km/h puis 30 km/h) :</b> Implanté à 50m",
                "🚦 <b>Feux Tricolores Synchronisés KR11J :</b> Avec détection radar de file d\\'attente",
                `🔶 <b>Cônes de Balisage K5a (Classe 2) :</b> Espacement tous les ${conesSpacing}`,
                "🛑 <b>Panneau B21 (Contournement obligatoire) :</b> En tête de biseau de rabattement"
            ];
        } else if (wType === 'route_barree') {
            signs = [
                "⛔ <b>Panneau KC1 & B1 (Route Barrée à 200m / Sens Interdit) :</b> Au carrefour amont",
                "↩️ <b>Panneaux KD22 (Itinéraire de Déviation VL / PL) :</b> Jalonnement continu",
                "🚧 <b>Barrages K2 :</b> Équipés de feux flashs synchronisés la nuit"
            ];
        } else if (wType === 'trottoir_pieton') {
            signs = [
                "🚶 <b>Panneau AK30 (Passage Piétons Déplacé) :</b> Implanté en amont",
                "🛡️ <b>Clôtures Opaque Heras & Lisses Rigides K2 :</b> Interdiction d\\'accès fouille",
                "♿ <b>Passerelle de Franchissement PMR :</b> Largeur 1.40m avec rampes $<5\%$"
            ];
        } else {
            signs = [
                "⚠️ <b>Panneau AK5 & AK4 (Travaux sur Accotement) :</b> Sans rétrécissement voie",
                "🔶 <b>Cônes K5a alignés :</b> Délimitation stricte de la zone d\\'évolution des engins"
            ];
        }

        if (box) {
            box.innerHTML = `
                <div style="font-weight:800; color:var(--amber); margin-bottom:0.4rem;">DISPOSITIF DE SIGNALISATION RECOMMANDÉ (OPBTP / SETRA) :</div>
                <div style="margin-bottom:0.5rem; font-size:0.78rem;"><b>Distances d'approche réglementaires :</b> <span style="color:var(--cyan);">${distances}</span></div>
                <ul style="list-style:inside; line-height:1.7; font-size:0.75rem; color:var(--text-main);">
                    ${signs.map(s => `<li>${s}</li>`).join('')}
                </ul>
            `;
        }

        renderOPBTPSignageCanvas(jType, wType, rType, period);
    }

    function renderOPBTPSignageCanvas(jType, wType, rType, period) {
        const canvas = document.getElementById('opbtp-signage-canvas');
        if (!canvas) return;
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * window.devicePixelRatio;
        canvas.height = rect.height * window.devicePixelRatio;
        const ctx = canvas.getContext('2d');
        ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
        const w = rect.width;
        const h = rect.height;

        // Background
        ctx.fillStyle = period === 'nuit' ? '#090d16' : '#1e293b';
        ctx.fillRect(0, 0, w, h);

        // Road surface
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 30, w, h - 60);

        // Road centerline markings
        ctx.strokeStyle = '#f8fafc';
        ctx.lineWidth = 1.5;
        ctx.setLineDash([8, 8]);
        ctx.beginPath(); ctx.moveTo(0, h/2); ctx.lineTo(w, h/2); ctx.stroke();
        ctx.setLineDash([]);

        // Work zone box
        const wzX = w * 0.45;
        const wzW = w * 0.35;
        ctx.fillStyle = 'rgba(239, 68, 68, 0.25)';
        ctx.fillRect(wzX, h/2, wzW, (h/2) - 30);
        ctx.strokeStyle = '#ef4444';
        ctx.strokeRect(wzX, h/2, wzW, (h/2) - 30);

        ctx.fillStyle = '#f87171';
        ctx.font = 'bold 8px Plus Jakarta Sans';
        ctx.fillText('🚧 ZONE CHANTIER', wzX + 10, h/2 + 20);

        // Cones Taper
        for (let i = 0; i < 6; i++) {
            const cX = wzX - (i * 12);
            const cY = (h/2) + (i * 4);
            ctx.fillStyle = '#f97316';
            ctx.beginPath(); ctx.arc(cX, cY, 3.5, 0, Math.PI * 2); ctx.fill();
        }

        // Signs placed along the approach
        const signs = [
            { x: 30, y: h - 20, label: 'AK5 150m' },
            { x: 80, y: h - 20, label: 'AK17 100m' },
            { x: 130, y: h - 20, label: 'B14 50km' },
            { x: 180, y: h - 20, label: '🚦 KR11J' }
        ];

        signs.forEach(s => {
            ctx.fillStyle = '#f59e0b';
            ctx.beginPath(); ctx.arc(s.x, s.y - 15, 6, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#0f172a'; ctx.font = 'bold 7px JetBrains Mono'; ctx.textAlign = 'center';
            ctx.fillText('⚠️', s.x, s.y - 12);
            ctx.fillStyle = '#cbd5e1'; ctx.font = '7px Plus Jakarta Sans';
            ctx.fillText(s.label, s.x, s.y);
        });
    }

"""

text = text[:idx_opbtp_start] + new_opbtp_js + text[idx_fleet_start:]

with open(TARGET, "w", encoding="utf-8") as f:
    f.write(text)

print("Applied Catalog and OPBTP Canvas JS successfully!")
