import json
from pathlib import Path

TARGET = Path("/home/user/monorepo/projects/btp-conduite-travaux/template.html")

with open(TARGET, "r", encoding="utf-8") as f:
    text = f.read()

# Replace renderToolCatalog and add openItemDetailSheet and drawItem3DPreview
old_catalog_js = """function renderToolCatalog() {
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
                rendement: 'Conforme CCTP'
            }));
        } else {
            const allTools = companyData.tool_catalog || [];
            items = allTools.filter(t => catalogFilter === 'all' || t.task === catalogFilter);
        }

        grid.innerHTML = items.map(item => `
            <div class="catalog-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div style="display:flex; align-items:center; gap:0.5rem;">
                        <span style="font-size:1.5rem;">${item.icon || '🔧'}</span>
                        <div>
                            <div style="font-weight:800; font-size:0.88rem; color:var(--text-main);">${item.name}</div>
                            <span class="card-badge" style="color:var(--cyan);">${item.category}</span>
                        </div>
                    </div>
                </div>
                <p style="font-size:0.75rem; color:var(--text-muted); line-height:1.5;">${item.description}</p>
                <div style="background:var(--bg); padding:0.6rem; border-radius:7px; font-size:0.72rem; display:grid; grid-template-columns:1fr 1fr; gap:0.35rem;">
                    <div>Prix / Unité : <b style="color:var(--text-main);">${item.prix_achat_neuf}</b></div>
                    <div>Location / Dispo : <b style="color:var(--emerald);">${item.tarif_location_jour}</b></div>
                    <div>Conditionnement : <b>${item.conso_moyenne}</b></div>
                    <div>Rendement : <b style="color:var(--cyan);">${item.rendement}</b></div>
                </div>
                <div style="display:flex; gap:0.4rem; margin-top:0.3rem;">
                    <button class="btn-primary" style="flex:1; justify-content:center; font-size:0.72rem; padding:0.4rem;" onclick="openOrderModal('${item.id}', '${item.name}', '${item.prix_achat_neuf}')">
                        🛒 Commander / Réserver
                    </button>
                    ${!item.is_material ? `<button class="btn-secondary" style="font-size:0.72rem; padding:0.4rem;" onclick="addCatalogItemToFleet('${item.id}')">➕ Ajouter Flotte</button>` : ''}
                </div>
            </div>
        `).join('');
    }"""

new_catalog_js = """function getStockBadge(item) {
        if (item.stock_status === 'out_of_stock' || (item.stock && (item.stock.startsWith('0') || item.stock.includes('Rupture')))) {
            return `<span class="stock-badge-out"><span class="stock-dot-red"></span> Rupture de Stock</span>`;
        } else if (item.stock_status === 'in_transit' || (item.stock && item.stock.includes('transit'))) {
            return `<span class="stock-badge-transit">🚚 En cours d'acheminement</span>`;
        } else {
            return `<span class="stock-badge-in">📦 En Stock (${item.stock || item.stock_qty || 'Dispo'})</span>`;
        }
    }

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
                rendement: 'Conforme CCTP'
            }));
        } else {
            const allTools = companyData.tool_catalog || [];
            items = allTools.filter(t => catalogFilter === 'all' || t.task === catalogFilter);
        }

        grid.innerHTML = items.map(item => `
            <div class="catalog-card" style="cursor:pointer;" onclick="openItemDetailSheet('${item.id}')">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.4rem;">
                    <div style="display:flex; align-items:center; gap:0.5rem;">
                        <span style="font-size:1.6rem;">${item.icon || '🔧'}</span>
                        <div>
                            <div style="font-weight:800; font-size:0.88rem; color:var(--text-main);">${item.name}</div>
                            <span class="card-badge" style="color:var(--cyan);">${item.category}</span>
                        </div>
                    </div>
                    <div>
                        ${getStockBadge(item)}
                    </div>
                </div>
                <p style="font-size:0.75rem; color:var(--text-muted); line-height:1.5;">${item.description}</p>
                <div style="background:var(--bg); padding:0.6rem; border-radius:7px; font-size:0.72rem; display:grid; grid-template-columns:1fr 1fr; gap:0.35rem; margin-top:0.4rem;">
                    <div>Prix / Unité : <b style="color:var(--text-main);">${item.prix_achat_neuf}</b></div>
                    <div>Location / Dispo : <b style="color:var(--emerald);">${item.tarif_location_jour}</b></div>
                    <div>Conditionnement : <b>${item.conso_moyenne}</b></div>
                    <div>Rendement : <b style="color:var(--cyan);">${item.rendement}</b></div>
                </div>
                <div style="display:flex; gap:0.4rem; margin-top:0.5rem;" onclick="event.stopPropagation();">
                    <button class="btn-secondary" style="font-size:0.72rem; padding:0.35rem 0.6rem;" onclick="openItemDetailSheet('${item.id}')">
                        🔍 Fiche & 3D
                    </button>
                    <button class="btn-primary" style="flex:1; justify-content:center; font-size:0.72rem; padding:0.35rem 0.6rem;" onclick="openOrderModal('${item.id}', '${item.name.replace(/'/g, "\\'")}', '${item.prix_achat_neuf}')">
                        🛒 Commander / Réserver
                    </button>
                    ${!item.is_material ? `<button class="btn-secondary" style="font-size:0.72rem; padding:0.35rem 0.5rem;" onclick="addCatalogItemToFleet('${item.id}')">➕ Flotte</button>` : ''}
                </div>
            </div>
        `).join('');
    }

    function openItemDetailSheet(itemId) {
        let item = (companyData.materials_catalog || []).find(m => m.id === itemId);
        let isMat = true;
        if (!item) {
            item = (companyData.tool_catalog || []).find(t => t.id === itemId);
            isMat = false;
        }
        if (!item) return;

        const content = document.getElementById('item-details-content');
        if (!content) return;

        const badgeHtml = getStockBadge(item);

        content.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1rem; border-bottom:1px solid var(--border); padding-bottom:0.75rem;">
                <div style="display:flex; align-items:center; gap:0.8rem;">
                    <div style="font-size:2.5rem; background:var(--bg); padding:0.4rem 0.8rem; border-radius:10px; border:1px solid var(--border);">${item.icon || '📦'}</div>
                    <div>
                        <h3 style="font-size:1.15rem; font-weight:800; color:var(--text-main); margin-bottom:0.2rem;">${item.name}</h3>
                        <div style="display:flex; gap:0.4rem; align-items:center;">
                            <span class="card-badge" style="color:var(--cyan);">${item.category}</span>
                            ${badgeHtml}
                        </div>
                    </div>
                </div>
                <button class="btn-secondary" style="padding:0.25rem 0.6rem;" onclick="closeModal('modal-item-details')">✕</button>
            </div>

            <div class="grid-2" style="gap:1rem; margin-bottom:1rem;">
                <!-- 3D Isometric Preview Canvas -->
                <div style="background:#030712; border:1px solid var(--border); border-radius:8px; padding:0.5rem; text-align:center;">
                    <div style="font-size:0.7rem; color:var(--cyan); font-weight:700; margin-bottom:0.3rem;">📐 Modèle Géométrique 3D / Vue Technique</div>
                    <canvas id="item-3d-canvas" width="260" height="180" style="display:block; margin:0 auto; background:#040711; border-radius:6px;"></canvas>
                    <div style="font-size:0.65rem; color:var(--text-muted); margin-top:0.3rem;">Rendu vectoriel isométrique temps réel</div>
                </div>

                <!-- Technical Specifications -->
                <div style="display:flex; flex-direction:column; gap:0.5rem; font-size:0.76rem;">
                    <div style="background:var(--bg); padding:0.6rem; border-radius:6px; border:1px solid var(--border);">
                        <b>🏷️ Référence :</b> <span style="font-family:var(--font-mono); color:var(--purple);">${item.id}</span><br>
                        <b>🏢 Fournisseur Homologué :</b> <span style="color:var(--cyan);">${item.fournisseur || 'Distributeur TP Occitanie'}</span><br>
                        <b>📜 Norme de Conformité :</b> <span style="color:var(--emerald);">${item.norme || 'CE / NF EN 1340'}</span>
                    </div>
                    <div style="background:var(--bg); padding:0.6rem; border-radius:6px; border:1px solid var(--border);">
                        <b>⚖️ Poids / Masse :</b> ${item.poids || 'Variable selon calibre'}<br>
                        <b>📏 Dimensions & Gabarit :</b> ${item.dimensions || item.conditionnement || 'Standard BTP'}<br>
                        <b>💶 Prix Unitaire HT :</b> <b style="color:var(--emerald);">${item.prix_unitaire ? item.prix_unitaire + ' € / ' + item.unit : (item.prix_achat_neuf || '185.00 €')}</b>
                    </div>
                </div>
            </div>

            <div style="background:var(--bg); padding:0.75rem; border-radius:6px; border:1px solid var(--border); margin-bottom:1rem; font-size:0.75rem; line-height:1.6;">
                <b style="color:var(--amber);">📋 Descriptif & Prescriptions CCTP :</b><br>
                ${item.description || 'Matériel professionnel certifié conforme aux exigences des chantiers de voirie et réseaux divers. Résistant aux conditions climatiques sévères et contraintes mécaniques extrêmes.'}
                <div style="margin-top:0.4rem; color:var(--text-muted);">
                    <b>Consommation / Rendement :</b> ${item.rendement || '100%'} | <b>Conditionnement :</b> ${item.conditionnement || item.conso_moyenne || 'Standard palette'}
                </div>
            </div>

            <div style="display:flex; justify-content:flex-end; gap:0.5rem;">
                <button class="btn-secondary" style="font-size:0.75rem;" onclick="closeModal('modal-item-details')">Fermer</button>
                <button class="btn-primary" style="font-size:0.75rem;" onclick="closeModal('modal-item-details'); openOrderModal('${item.id}', '${item.name.replace(/'/g, "\\'")}', '${item.prix_unitaire ? item.prix_unitaire + ' €' : item.prix_achat_neuf}')">
                    🛒 Passer Commande Fournisseur
                </button>
            </div>
        `;

        openModal('modal-item-details');

        // Draw 3D wireframe render on item-3d-canvas
        setTimeout(() => {
            const canvas = document.getElementById('item-3d-canvas');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            const w = canvas.width;
            const h = canvas.height;
            ctx.clearRect(0, 0, w, h);

            // Draw isometric grid
            ctx.strokeStyle = '#1e293b';
            ctx.lineWidth = 1;
            for(let x = 0; x < w; x += 20) {
                ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
            }
            for(let y = 0; y < h; y += 20) {
                ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
            }

            // Draw isometric 3D object representation
            const cx = w / 2;
            const cy = h / 2 + 10;
            const size = 50;

            // Draw top face
            ctx.fillStyle = 'rgba(6,182,212,0.35)';
            ctx.strokeStyle = '#06b6d4';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(cx, cy - size);
            ctx.lineTo(cx + size * 1.3, cy - size / 2);
            ctx.lineTo(cx, cy);
            ctx.lineTo(cx - size * 1.3, cy - size / 2);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();

            // Draw left face
            ctx.fillStyle = 'rgba(14,165,233,0.2)';
            ctx.strokeStyle = '#0ea5e9';
            ctx.beginPath();
            ctx.moveTo(cx - size * 1.3, cy - size / 2);
            ctx.lineTo(cx, cy);
            ctx.lineTo(cx, cy + size);
            ctx.lineTo(cx - size * 1.3, cy + size / 2);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();

            // Draw right face
            ctx.fillStyle = 'rgba(168,85,247,0.25)';
            ctx.strokeStyle = '#a855f7';
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.lineTo(cx + size * 1.3, cy - size / 2);
            ctx.lineTo(cx + size * 1.3, cy + size / 2);
            ctx.lineTo(cx, cy + size);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();

            // Label
            ctx.fillStyle = '#f8fafc';
            ctx.font = 'bold 11px system-ui';
            ctx.textAlign = 'center';
            ctx.fillText(item.name.substring(0, 24), cx, h - 12);
        }, 50);
    }"""

if old_catalog_js in text:
    text = text.replace(old_catalog_js, new_catalog_js)
    print("Replaced renderToolCatalog and added openItemDetailSheet!")
else:
    print("old_catalog_js not found exactly! Using function search...")
    idx1 = text.find("function renderToolCatalog")
    idx2 = text.find("function filterCatalog", idx1)
    if idx1 != -1 and idx2 != -1:
        text = text[:idx1] + new_catalog_js + "\n\n    " + text[idx2:]
        print("Replaced by range successfully!")

with open(TARGET, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved update_catalog_details.py successfully!")
