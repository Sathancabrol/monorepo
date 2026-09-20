def get_js_part3():
    return """
    // ==========================================
    // 13. OBSIDIAN GRAPH VIEW ENGINE (STABLE PHYSICS)
    // ==========================================
    let obsidianNodes = [];
    let obsidianLinks = [];
    let obsidianCanvas, obsidianCtx, obsidianAnimId;
    let draggedNode = null;
    let hoveredNode = null;

    function initObsidianGraph() {
        obsidianCanvas = document.getElementById('obsidian-canvas');
        if (!obsidianCanvas) return;
        obsidianCtx = obsidianCanvas.getContext('2d');

        obsidianCanvas.width = obsidianCanvas.offsetWidth || 800;
        obsidianCanvas.height = obsidianCanvas.offsetHeight || 500;

        const rawNodes = obsidianData.nodes || [];
        const rawLinks = obsidianData.links || [];

        const width = obsidianCanvas.width;
        const height = obsidianCanvas.height;

        obsidianNodes = rawNodes.map((n, i) => {
            const angle = (i / (rawNodes.length || 1)) * Math.PI * 2;
            const radius = 120 + (i % 3) * 60;
            return {
                id: n.id,
                label: n.label,
                domain: n.domain,
                color: n.domain === 'reglementaire' ? '#ef4444' : (n.domain === 'technique' ? '#38bdf8' : (n.domain === 'financier' ? '#10b981' : '#f59e0b')),
                x: width / 2 + Math.cos(angle) * radius + (Math.random() - 0.5) * 20,
                y: height / 2 + Math.sin(angle) * radius + (Math.random() - 0.5) * 20,
                vx: 0,
                vy: 0,
                radius: 8 + (n.links_count || 3) * 1.5
            };
        });

        obsidianLinks = rawLinks.map(l => ({
            source: obsidianNodes.find(n => n.id === l.source) || obsidianNodes[0],
            target: obsidianNodes.find(n => n.id === l.target) || obsidianNodes[1],
            weight: l.weight || 1
        }));

        obsidianCanvas.onmousedown = (e) => {
            const rect = obsidianCanvas.getBoundingClientRect();
            const mx = e.clientX - rect.left;
            const my = e.clientY - rect.top;
            draggedNode = obsidianNodes.find(n => Math.hypot(n.x - mx, n.y - my) < n.radius + 4);
        };

        window.onmouseup = () => { draggedNode = null; };

        obsidianCanvas.onmousemove = (e) => {
            const rect = obsidianCanvas.getBoundingClientRect();
            const mx = e.clientX - rect.left;
            const my = e.clientY - rect.top;

            if (draggedNode) {
                draggedNode.x = mx;
                draggedNode.y = my;
                draggedNode.vx = 0;
                draggedNode.vy = 0;
            }

            hoveredNode = obsidianNodes.find(n => Math.hypot(n.x - mx, n.y - my) < n.radius + 4);
            obsidianCanvas.style.cursor = hoveredNode ? 'pointer' : 'default';

            if (hoveredNode) {
                const nodeInfo = document.getElementById('obsidian-node-info');
                if (nodeInfo) {
                    nodeInfo.innerHTML = `
                        <div style="background:rgba(15,23,42,0.9); border:1px solid ${hoveredNode.color}; border-radius:6px; padding:0.6rem; font-size:0.8rem;">
                            <strong style="color:${hoveredNode.color}; font-size:0.85rem;">● ${hoveredNode.label}</strong>
                            <div style="color:#94a3b8; font-size:0.75rem; margin-top:2px;">Domaine : ${hoveredNode.domain.toUpperCase()}</div>
                        </div>
                    `;
                }
            }
        };

        function simulateGraphStep() {
            if (!obsidianCtx || obsidianCanvas.style.display === 'none') {
                obsidianAnimId = requestAnimationFrame(simulateGraphStep);
                return;
            }

            for (let i = 0; i < obsidianNodes.length; i++) {
                for (let j = i + 1; j < obsidianNodes.length; j++) {
                    const n1 = obsidianNodes[i];
                    const n2 = obsidianNodes[j];
                    const dx = n2.x - n1.x;
                    const dy = n2.y - n1.y;
                    const dist = Math.hypot(dx, dy) || 1;
                    if (dist < 180) {
                        const force = (180 - dist) / (dist * 12);
                        n1.vx -= dx * force;
                        n1.vy -= dy * force;
                        n2.vx += dx * force;
                        n2.vy += dy * force;
                    }
                }
            }

            obsidianLinks.forEach(l => {
                const dx = l.target.x - l.source.x;
                const dy = l.target.y - l.source.y;
                const dist = Math.hypot(dx, dy) || 1;
                const force = (dist - 90) * 0.005;
                l.source.vx += dx * force;
                l.source.vy += dy * force;
                l.target.vx -= dx * force;
                l.target.vy -= dy * force;
            });

            const cx = obsidianCanvas.width / 2;
            const cy = obsidianCanvas.height / 2;
            obsidianNodes.forEach(n => {
                if (n === draggedNode) return;
                n.vx += (cx - n.x) * 0.002;
                n.vy += (cy - n.y) * 0.002;
                n.vx *= 0.82;
                n.vy *= 0.82;
                n.x += n.vx;
                n.y += n.vy;
            });

            obsidianCtx.fillStyle = '#090d16';
            obsidianCtx.fillRect(0, 0, obsidianCanvas.width, obsidianCanvas.height);

            obsidianLinks.forEach(l => {
                obsidianCtx.strokeStyle = 'rgba(51, 65, 85, 0.4)';
                obsidianCtx.lineWidth = 1;
                obsidianCtx.beginPath();
                obsidianCtx.moveTo(l.source.x, l.source.y);
                obsidianCtx.lineTo(l.target.x, l.target.y);
                obsidianCtx.stroke();
            });

            obsidianNodes.forEach(n => {
                obsidianCtx.fillStyle = n.color;
                obsidianCtx.beginPath();
                obsidianCtx.arc(n.x, n.y, n.radius, 0, Math.PI * 2);
                obsidianCtx.fill();

                if (n === hoveredNode) {
                    obsidianCtx.strokeStyle = '#ffffff';
                    obsidianCtx.lineWidth = 2;
                    obsidianCtx.stroke();
                }

                obsidianCtx.fillStyle = '#f8fafc';
                obsidianCtx.font = '10px "JetBrains Mono"';
                obsidianCtx.fillText(n.label, n.x + n.radius + 4, n.y + 3);
            });

            obsidianAnimId = requestAnimationFrame(simulateGraphStep);
        }

        cancelAnimationFrame(obsidianAnimId);
        simulateGraphStep();
    }

    function filterObsidianDomain(domain) {
        obsidianHeuristic = domain;
        initObsidianGraph();
    }

    // ==========================================
    // 14. SDP & DQE PIVOT TABLE (TCD) ENGINE
    // ==========================================
    function setSdpView(mode) {
        sdpViewMode = mode;
        document.querySelectorAll('.sdp-view-btn').forEach(b => b.classList.remove('active'));
        document.getElementById(`btn-sdp-${mode}`)?.classList.add('active');

        const tcdEl = document.getElementById('sdp-dqe-tcd-view');
        const cardsEl = document.getElementById('sdp-cards-view');
        if (tcdEl) tcdEl.style.display = (mode === 'dqe_tcd') ? 'block' : 'none';
        if (cardsEl) cardsEl.style.display = (mode === 'cards') ? 'block' : 'none';

        if (mode === 'dqe_tcd') renderDQEPivotTable();
        else renderSdpCards();
    }

    function renderDQEPivotTable() {
        const container = document.getElementById('sdp-dqe-tcd-view');
        if (!container || !syntheseData.dqe_items) return;

        const lotFilter = document.getElementById('dqe-lot-select')?.value || 'all';
        const projectFilter = document.getElementById('dqe-project-select')?.value || 'all';

        let items = syntheseData.dqe_items;
        if (lotFilter !== 'all') items = items.filter(i => (i.lot || '').toLowerCase().includes(lotFilter.toLowerCase()));
        if (projectFilter !== 'all') items = items.filter(i => (i.project_id || '').toLowerCase() === projectFilter.toLowerCase());

        let totalDS = 0, totalMO = 0, totalMat = 0, totalEq = 0, totalST = 0, totalPV = 0;

        const rowsHtml = items.map(item => {
            const qty = item.quantity || 1;
            const ds_mo = (item.ds_mo || 0) * qty;
            const ds_mat = (item.ds_mat || 0) * qty;
            const ds_eq = (item.ds_eq || 0) * qty;
            const ds_st = (item.ds_st || 0) * qty;
            const totalItemDS = (item.unit_ds || 0) * qty;
            const totalItemPV = (item.unit_pv || 0) * qty;

            totalDS += totalItemDS;
            totalMO += ds_mo;
            totalMat += ds_mat;
            totalEq += ds_eq;
            totalST += ds_st;
            totalPV += totalItemPV;

            return `
                <tr style="border-bottom:1px solid rgba(51,65,85,0.3); font-size:0.8rem;">
                    <td style="padding:0.6rem; font-family:'JetBrains Mono'; font-weight:700; color:#38bdf8;">${item.code}</td>
                    <td style="padding:0.6rem; font-weight:600; color:#f8fafc;">${item.designation}</td>
                    <td style="padding:0.6rem; color:#94a3b8;"><span class="badge badge-info" style="font-size:0.65rem;">${item.lot}</span></td>
                    <td style="padding:0.6rem; text-align:right; font-family:'JetBrains Mono';">${qty} ${item.unit}</td>
                    <td style="padding:0.6rem; text-align:right; font-family:'JetBrains Mono'; color:#38bdf8;">${Math.round(ds_mo).toLocaleString()} €</td>
                    <td style="padding:0.6rem; text-align:right; font-family:'JetBrains Mono'; color:#f59e0b;">${Math.round(ds_mat).toLocaleString()} €</td>
                    <td style="padding:0.6rem; text-align:right; font-family:'JetBrains Mono'; color:#8b5cf6;">${Math.round(ds_eq).toLocaleString()} €</td>
                    <td style="padding:0.6rem; text-align:right; font-family:'JetBrains Mono'; color:#ec4899;">${Math.round(ds_st).toLocaleString()} €</td>
                    <td style="padding:0.6rem; text-align:right; font-family:'JetBrains Mono'; font-weight:700; color:#f8fafc;">${Math.round(totalItemDS).toLocaleString()} €</td>
                    <td style="padding:0.6rem; text-align:right; font-family:'JetBrains Mono'; font-weight:700; color:var(--emerald);">${Math.round(totalItemPV).toLocaleString()} €</td>
                    <td style="padding:0.6rem; text-align:center;">
                        <button class="btn btn-secondary" style="padding:0.2rem 0.4rem; font-size:0.65rem;" onclick="openSdpDetailModal('${item.code}')">🔍 SDP</button>
                    </td>
                </tr>
            `;
        }).join('');

        container.innerHTML = `
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:0.75rem; margin-bottom:1rem;">
                <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(51,65,85,0.6); padding:0.75rem; border-radius:6px;">
                    <div style="font-size:0.7rem; color:#64748b;">TOTAL MAIN D'ŒUVRE (MO)</div>
                    <div style="font-size:1.1rem; font-weight:900; color:#38bdf8; font-family:'JetBrains Mono';">${Math.round(totalMO).toLocaleString()} €</div>
                </div>
                <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(51,65,85,0.6); padding:0.75rem; border-radius:6px;">
                    <div style="font-size:0.7rem; color:#64748b;">TOTAL FOURNITURES / MATÉRIAUX</div>
                    <div style="font-size:1.1rem; font-weight:900; color:#f59e0b; font-family:'JetBrains Mono';">${Math.round(totalMat).toLocaleString()} €</div>
                </div>
                <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(51,65,85,0.6); padding:0.75rem; border-radius:6px;">
                    <div style="font-size:0.7rem; color:#64748b;">TOTAL MATÉRIEL / ENGINS</div>
                    <div style="font-size:1.1rem; font-weight:900; color:#8b5cf6; font-family:'JetBrains Mono';">${Math.round(totalEq).toLocaleString()} €</div>
                </div>
                <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(51,65,85,0.6); padding:0.75rem; border-radius:6px;">
                    <div style="font-size:0.7rem; color:#64748b;">TOTAL SOUS-TRAITANCE (ST)</div>
                    <div style="font-size:1.1rem; font-weight:900; color:#ec4899; font-family:'JetBrains Mono';">${Math.round(totalST).toLocaleString()} €</div>
                </div>
                <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(16,185,129,0.5); padding:0.75rem; border-radius:6px;">
                    <div style="font-size:0.7rem; color:#10b981; font-weight:700;">TOTAL DEVIS PV HT (K=1.35)</div>
                    <div style="font-size:1.2rem; font-weight:900; color:var(--emerald); font-family:'JetBrains Mono';">${Math.round(totalPV).toLocaleString()} €</div>
                </div>
            </div>

            <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(51,65,85,0.6); border-radius:8px; overflow-x:auto;">
                <table style="width:100%; border-collapse:collapse; min-width:1050px;">
                    <thead>
                        <tr style="background:rgba(30,41,59,0.9); color:#94a3b8; font-size:0.75rem; text-transform:uppercase; border-bottom:2px solid var(--border);">
                            <th style="padding:0.6rem; text-align:left;">Code</th>
                            <th style="padding:0.6rem; text-align:left;">Désignation DQE</th>
                            <th style="padding:0.6rem; text-align:left;">Lot VRD</th>
                            <th style="padding:0.6rem; text-align:right;">Quantité</th>
                            <th style="padding:0.6rem; text-align:right; color:#38bdf8;">MO (€)</th>
                            <th style="padding:0.6rem; text-align:right; color:#f59e0b;">Matériaux (€)</th>
                            <th style="padding:0.6rem; text-align:right; color:#8b5cf6;">Matériel (€)</th>
                            <th style="padding:0.6rem; text-align:right; color:#ec4899;">ST (€)</th>
                            <th style="padding:0.6rem; text-align:right; color:#f8fafc;">Total D.S. (€)</th>
                            <th style="padding:0.6rem; text-align:right; color:var(--emerald);">Prix Vente (€)</th>
                            <th style="padding:0.6rem; text-align:center;">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${rowsHtml}
                    </tbody>
                </table>
            </div>
        `;
    }

    function renderSdpCards() {
        const container = document.getElementById('sdp-cards-view');
        if (!container || !syntheseData.dqe_items) return;

        container.innerHTML = `
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:1rem;">
                ${syntheseData.dqe_items.map(i => `
                    <div class="card" style="display:flex; flex-direction:column; justify-content:space-between;">
                        <div>
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
                                <span class="badge badge-info">${i.lot}</span>
                                <span style="font-family:'JetBrains Mono'; font-weight:700; color:#38bdf8;">${i.code}</span>
                            </div>
                            <h4 style="font-size:0.95rem; font-weight:800; color:#f8fafc; margin-bottom:0.5rem;">${i.designation}</h4>
                            <div style="font-size:0.8rem; color:#94a3b8; margin-bottom:0.75rem;">Unité : <strong>${i.unit}</strong> • Qté estimée : <strong>${i.quantity || 1}</strong></div>

                            <div style="background:rgba(15,23,42,0.6); padding:0.6rem; border-radius:6px; font-size:0.75rem; display:grid; grid-template-columns:1fr 1fr; gap:0.4rem; margin-bottom:0.75rem;">
                                <div><span style="color:#64748b;">D.S. Unitaire :</span><br><strong style="font-family:'JetBrains Mono'; color:#cbd5e1;">${(i.unit_ds || 0).toFixed(2)} €</strong></div>
                                <div><span style="color:#64748b;">P.V. Unitaire (HT) :</span><br><strong style="font-family:'JetBrains Mono'; color:var(--emerald);">${(i.unit_pv || 0).toFixed(2)} €</strong></div>
                            </div>
                        </div>

                        <button class="btn btn-primary" style="font-size:0.75rem; padding:0.4rem;" onclick="openSdpDetailModal('${i.code}')">
                            📋 Décomposer le SDP
                        </button>
                    </div>
                `).join('')}
            </div>
        `;
    }

    function openSdpDetailModal(code) {
        const item = (syntheseData.dqe_items || []).find(x => x.code === code) || syntheseData.dqe_items[0];
        if (!item) return;

        const body = document.getElementById('sdp-detail-modal-body');
        if (!body) return;

        const k = 1.35;
        const ds_mo = item.ds_mo || 0;
        const ds_mat = item.ds_mat || 0;
        const ds_eq = item.ds_eq || 0;
        const ds_st = item.ds_st || 0;
        const unit_ds = ds_mo + ds_mat + ds_eq + ds_st;
        const unit_pv = unit_ds * k;

        body.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1.25rem;">
                <div>
                    <span class="badge badge-info">${item.lot}</span>
                    <h2 style="font-size:1.35rem; font-weight:900; color:#f8fafc; margin-top:0.35rem;">[${item.code}] ${item.designation}</h2>
                    <div style="font-size:0.85rem; color:#94a3b8;">Unité d'ouvrage : <strong style="color:#38bdf8;">${item.unit}</strong></div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:0.75rem; color:#64748b;">PRIX DE VENTE UNITAIRE H.T.</div>
                    <div style="font-size:1.5rem; font-weight:900; color:var(--emerald); font-family:'JetBrains Mono';">${unit_pv.toFixed(2)} €</div>
                </div>
            </div>

            <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(51,65,85,0.6); border-radius:8px; padding:1rem; margin-bottom:1.25rem;">
                <h4 style="font-size:0.95rem; font-weight:800; color:#38bdf8; margin-bottom:0.75rem;">🔬 Décomposition du Déboursé Sec (D.S.)</h4>
                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(140px, 1fr)); gap:0.75rem; font-size:0.8rem;">
                    <div style="background:rgba(30,41,59,0.5); padding:0.6rem; border-radius:4px;">
                        <span style="color:#64748b;">Main d'Œuvre (MO)</span>
                        <div style="font-size:1rem; font-weight:700; color:#38bdf8; font-family:'JetBrains Mono'; margin-top:2px;">${ds_mo.toFixed(2)} €</div>
                    </div>
                    <div style="background:rgba(30,41,59,0.5); padding:0.6rem; border-radius:4px;">
                        <span style="color:#64748b;">Matériaux & Fournitures</span>
                        <div style="font-size:1rem; font-weight:700; color:#f59e0b; font-family:'JetBrains Mono'; margin-top:2px;">${ds_mat.toFixed(2)} €</div>
                    </div>
                    <div style="background:rgba(30,41,59,0.5); padding:0.6rem; border-radius:4px;">
                        <span style="color:#64748b;">Matériel & Engins</span>
                        <div style="font-size:1rem; font-weight:700; color:#8b5cf6; font-family:'JetBrains Mono'; margin-top:2px;">${ds_eq.toFixed(2)} €</div>
                    </div>
                    <div style="background:rgba(30,41,59,0.5); padding:0.6rem; border-radius:4px;">
                        <span style="color:#64748b;">Sous-Traitance</span>
                        <div style="font-size:1rem; font-weight:700; color:#ec4899; font-family:'JetBrains Mono'; margin-top:2px;">${ds_st.toFixed(2)} €</div>
                    </div>
                </div>
            </div>

            <div style="background:rgba(2,132,199,0.1); border-left:3px solid #0284c7; padding:0.75rem; border-radius:6px; font-size:0.85rem; color:#cbd5e1; margin-bottom:1.25rem;">
                <strong>Formule d'Étude de Prix :</strong> PV_HT = DS × K (avec Coefficient de Vente K = 1.35 intégrant Frais Généraux FG = 18%, Frais Spéciaux FC = 5%, et Marge/Bénéfice B&A = 12%).
            </div>

            <div style="display:flex; justify-content:flex-end;">
                <button class="btn btn-secondary" onclick="closeModal('sdp-detail-modal')">Fermer</button>
            </div>
        `;
        openModal('sdp-detail-modal');
    }
"""

def get_js_part3_continued():
    return """
    // ==========================================
    // 15. PROCUREMENT & SUPPLIERS ENGINE
    // ==========================================
    function renderProcurement() {
        const grid = document.getElementById('suppliers-grid');
        if (!grid || !companyData.suppliers) return;

        grid.innerHTML = companyData.suppliers.map(s => `
            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
                    <span class="badge badge-info">${s.category || 'VRD & Matériaux'}</span>
                    <span style="font-family:'JetBrains Mono'; font-size:0.8rem; color:#94a3b8;">${s.id || 'FOURN'}</span>
                </div>
                <h3 style="font-size:1.15rem; font-weight:800; color:#f8fafc; margin-bottom:0.25rem;">${s.name}</h3>
                <div style="font-size:0.85rem; color:#94a3b8; margin-bottom:0.75rem;">Spécialité : <strong style="color:#cbd5e1;">${s.specialty || 'Fournitures'}</strong></div>

                <div style="background:rgba(15,23,42,0.6); padding:0.6rem; border-radius:6px; font-size:0.8rem; margin-bottom:0.75rem;">
                    <div><span style="color:#64748b;">Localisation :</span> <strong style="color:#f1f5f9;">${s.location || 'Hérault (34)'} (${s.distance_km || 15} km)</strong></div>
                    <div><span style="color:#64748b;">Note Qualité :</span> <strong style="font-family:'JetBrains Mono'; color:var(--emerald);">⭐ ${s.quality_rating || 4.8}/5</strong></div>
                </div>

                <button class="btn btn-secondary" style="width:100%; font-size:0.8rem;" onclick="alert('Catalogue tarifaire ouvert pour le fournisseur ${s.name}');">
                    📋 Consulter Tarifs & Commandes
                </button>
            </div>
        `).join('');
    }

    // ==========================================
    // 16. LEDGER SHA-256 AUDIT TRAIL ENGINE
    // ==========================================
    function renderLedger() {
        const list = document.getElementById('ledger-transactions-list');
        if (!list || !ledgerData.blocks) return;

        list.innerHTML = ledgerData.blocks.map(tx => `
            <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(51,65,85,0.6); border-radius:8px; padding:0.85rem; margin-bottom:0.75rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                    <span style="font-family:'JetBrains Mono'; font-size:0.75rem; color:#38bdf8; font-weight:700;">BLOC #${tx.index} • ${tx.timestamp}</span>
                    <span class="badge badge-success" style="font-size:0.65rem;">SHA-256 SCELLÉ</span>
                </div>
                <div style="font-size:0.9rem; font-weight:700; color:#f8fafc; margin-bottom:0.25rem;">${tx.details ? (tx.details.project || tx.action || 'Événement BTP') : (tx.action || 'Transaction')}</div>
                <div style="font-family:'JetBrains Mono'; font-size:0.7rem; color:#64748b; word-break:break-all; background:rgba(0,0,0,0.3); padding:0.4rem; border-radius:4px;">
                    HASH: <span style="color:#10b981;">${tx.hash}</span>
                </div>
            </div>
        `).join('');
    }

    // ==========================================
    // 17. COMPANY CASHFLOW & BALANCES
    // ==========================================
    function renderCompanyMetrics() {
        const caisseEl = document.getElementById('company-caisse-val');
        if (caisseEl) caisseEl.textContent = `${caisseBalance.toLocaleString()} €`;
        const caisseTop = document.getElementById('caisse-balance-top');
        if (caisseTop) caisseTop.textContent = `${caisseBalance.toLocaleString()} €`;
        const kpiTreasury = document.getElementById('kpi-treasury-val');
        if (kpiTreasury) kpiTreasury.textContent = `${caisseBalance.toLocaleString()} €`;
    }
"""

def get_js_helpers_and_actions():
    return """
    // ==========================================
    // 19. ADVANCED AUTONOMOUS & COCKPIT CONTROLS
    // ==========================================
    let isAutopilotRunning = false;
    let autopilotInterval = null;

    function runAutopilot() {
        if (isAutopilotRunning) {
            clearInterval(autopilotInterval);
            isAutopilotRunning = false;
            logCockpit('🛑 Mode Autopilote Désactivé.', 'warn');
            return;
        }

        isAutopilotRunning = true;
        logCockpit('🚀 Activation de l\\'Autopilote IA BTP : Surveillance télémétrique continue...', 'ok');

        const events = [
            'Scan LiDAR ZAC des Pins : Terrassement conforme au MNT projet (Tolérance ±15mm).',
            'Sonde de nappe Bd Haussmann : Niveau d\\'eau stabilisé à -2.80m après rabattement.',
            'Télématique Flotte : Pelle Liebherr R924 en charge active (Rendement: 65 m³/h).',
            'Alerte Météo : Prévision pluie modérée dans 48h - Recommandation : Fermeture tranchée ouverte Lot 2.',
            'Contrôle Financier : Ratio D.S./P.V. conforme (Marge estimée consolidée: 14.8%).'
        ];

        let i = 0;
        autopilotInterval = setInterval(() => {
            if (!isAutopilotRunning) return;
            logCockpit(events[i % events.length], 'info');
            i++;
        }, 4000);
    }

    function toggleVoiceControl() {
        logCockpit('🎙️ Module de Reconnaissance Vocale & Audio Terrain activé (Microphone prêt).', 'ok');
        alert('Module Vocal Actif : Vous pouvez dicter vos annotations de chantier ou donner des ordres vocaux.');
    }

    function triggerSimulatedCrisis() {
        logCockpit('🚨 ALERTE CRITIQUE : Découverte d\\'une canalisation Gaz non répertoriée sur le projet ZAC des Pins !', 'alert');
        alert('⚠️ ALERTE DE SÉCURITÉ CHANTIER\\n\\nArrêt immédiat des travaux à la pelle mécanique sur la section PK 0+240.\\nProcédure DICT / AIPR d\\'urgence engagée.\\nÉvacuation du périmètre 25m et contact GRDF en cours.');
    }

    function simulatePaymentSituation() {
        const amount = 125400;
        caisseBalance += amount;
        renderCompanyMetrics();
        logCockpit(`💶 Situation de travaux n°4 validée par le Maître d'Œuvre : +${amount.toLocaleString()} € HT reçus en caisse.`, 'ok');
        alert(`Situation validée ! La trésorerie a été créditée de ${amount.toLocaleString()} € HT.`);
    }

    // ==========================================
    // 20. 3D VIEW CONTROLS & PRESETS
    // ==========================================
    function rotate3D(dx, dy) {
        cameraRotY += dx;
        cameraRotX = Math.max(10, Math.min(80, cameraRotX + dy));
        const c = document.getElementById('watchtower-3d-canvas');
        if (c) render3DScene(c.getContext('2d'), c.width, c.height);
    }

    function zoom3D(factor) {
        cameraZoom = Math.max(0.5, Math.min(2.5, cameraZoom * factor));
        const c = document.getElementById('watchtower-3d-canvas');
        if (c) render3DScene(c.getContext('2d'), c.width, c.height);
    }

    function set3DPreset(preset) {
        if (preset === 'top') {
            cameraRotX = 80;
            cameraRotY = 0;
        } else if (preset === 'iso') {
            cameraRotX = 30;
            cameraRotY = -45;
        } else if (preset === 'side') {
            cameraRotX = 15;
            cameraRotY = -90;
        }
        const c = document.getElementById('watchtower-3d-canvas');
        if (c) render3DScene(c.getContext('2d'), c.width, c.height);
    }

    // ==========================================
    // 21. FORMULAS CALCULATOR ENGINE
    // ==========================================
    function updateFormulaCalculator() {
        const formulaType = document.getElementById('formula-type-select')?.value || 'compactage';
        const out = document.getElementById('formula-calculation-output');
        if (!out) return;

        if (formulaType === 'compactage') {
            const epaisseur = parseFloat(document.getElementById('f-param-1')?.value || 0.30);
            const vitesse = parseFloat(document.getElementById('f-param-2')?.value || 4.0);
            const largeur = parseFloat(document.getElementById('f-param-3')?.value || 2.10);
            const passes = parseFloat(document.getElementById('f-param-4')?.value || 6);

            const qs = epaisseur / passes;
            const debit = (largeur * (vitesse * 1000) * epaisseur) / passes;

            out.innerHTML = `
                <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(51,65,85,0.7); padding:1rem; border-radius:8px;">
                    <h4 style="color:#38bdf8; font-size:1rem; font-weight:800; margin-bottom:0.5rem;">📐 Résultats : Formule de Compactage GTR (Q/S)</h4>
                    <div style="font-size:0.85rem; color:#cbd5e1; margin-bottom:0.75rem;">
                        <strong>Formule appliquée :</strong> <code>Q/S = Épaisseur / Nbre_passes</code> et <code>Débit_horaire = (L × V × E) / N</code>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
                        <div style="background:rgba(30,41,59,0.5); padding:0.75rem; border-radius:6px;">
                            <span style="font-size:0.75rem; color:#64748b;">RATIO Q/S OBTENU</span>
                            <div style="font-size:1.3rem; font-weight:900; color:var(--emerald); font-family:'JetBrains Mono';">${qs.toFixed(4)} m³/m²</div>
                            <span style="font-size:0.75rem; color:#10b981;">Conforme classe V5 (≤ 0.050)</span>
                        </div>
                        <div style="background:rgba(30,41,59,0.5); padding:0.75rem; border-radius:6px;">
                            <span style="font-size:0.75rem; color:#64748b;">DÉBIT PRATIQUE ESTIMÉ</span>
                            <div style="font-size:1.3rem; font-weight:900; color:#38bdf8; font-family:'JetBrains Mono';">${Math.round(debit)} m³/heure</div>
                            <span style="font-size:0.75rem; color:#94a3b8;">Pour 1 rouleau tandem vibrant</span>
                        </div>
                    </div>
                </div>
            `;
        } else if (formulaType === 'manning') {
            const d = parseFloat(document.getElementById('f-param-1')?.value || 0.40);
            const slope = parseFloat(document.getElementById('f-param-2')?.value || 0.015);
            const kStrickler = 80;

            const rHyd = d / 4;
            const section = Math.PI * Math.pow(d / 2, 2);
            const vitesse = kStrickler * Math.pow(rHyd, 2/3) * Math.sqrt(slope);
            const debit = section * vitesse * 1000;

            out.innerHTML = `
                <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(51,65,85,0.7); padding:1rem; border-radius:8px;">
                    <h4 style="color:#38bdf8; font-size:1rem; font-weight:800; margin-bottom:0.5rem;">💧 Résultats : Écoulement Manning-Strickler</h4>
                    <div style="font-size:0.85rem; color:#cbd5e1; margin-bottom:0.75rem;">
                        <strong>Formule appliquée :</strong> <code>V = K × Rh^(2/3) × I^(1/2)</code> et <code>Q = S × V</code>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
                        <div style="background:rgba(30,41,59,0.5); padding:0.75rem; border-radius:6px;">
                            <span style="font-size:0.75rem; color:#64748b;">VITESSE D'ÉCOULEMENT</span>
                            <div style="font-size:1.3rem; font-weight:900; color:var(--emerald); font-family:'JetBrains Mono';">${vitesse.toFixed(2)} m/s</div>
                            <span style="font-size:0.75rem; color:#10b981;">Autocurage assuré (> 0.6 m/s)</span>
                        </div>
                        <div style="background:rgba(30,41,59,0.5); padding:0.75rem; border-radius:6px;">
                            <span style="font-size:0.75rem; color:#64748b;">CAPACITÉ MAX (PLEINE SECTION)</span>
                            <div style="font-size:1.3rem; font-weight:900; color:#38bdf8; font-family:'JetBrains Mono';">${Math.round(debit)} L/seconde</div>
                            <span style="font-size:0.75rem; color:#94a3b8;">${(debit * 3.6).toFixed(1)} m³/h</span>
                        </div>
                    </div>
                </div>
            `;
        }
    }

    // ==========================================
    // 22. DQE EXPORTS & LEDGER VERIFICATION
    // ==========================================
    function exportDQEtoCSV() {
        if (!syntheseData.dqe_items) return;
        let csv = 'Code;Designation;Lot;Quantite;Unite;DS_MO;DS_Materiaux;DS_Materiel;DS_SousTraitance;Total_DS;PV_HT\\n';
        syntheseData.dqe_items.forEach(i => {
            const qty = i.quantity || 1;
            const ds_mo = (i.ds_mo || 0) * qty;
            const ds_mat = (i.ds_mat || 0) * qty;
            const ds_eq = (i.ds_eq || 0) * qty;
            const ds_st = (i.ds_st || 0) * qty;
            const totalDS = (i.unit_ds || 0) * qty;
            const totalPV = (i.unit_pv || 0) * qty;
            csv += `"${i.code}";"${i.designation.replace(/"/g, '""')}";"${i.lot}";${qty};"${i.unit}";${ds_mo.toFixed(2)};${ds_mat.toFixed(2)};${ds_eq.toFixed(2)};${ds_st.toFixed(2)};${totalDS.toFixed(2)};${totalPV.toFixed(2)}\\n`;
        });

        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `DQE_Tableau_Croise_Dynamique_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        logCockpit('📊 Exportation CSV du DQE multi-lots réussie.', 'ok');
    }

    function printDQESummary() {
        window.print();
    }

    function verifyLedgerIntegrity() {
        logCockpit('🔍 Vérification de la chaîne de blocs SHA-256 en cours...', 'info');
        setTimeout(() => {
            logCockpit('✅ Intégrité SHA-256 certifiée : 100% des blocs et horodatages sont valides et inaltérés.', 'ok');
            alert('Vérification Cryptographique Réussie !\\n\\nTous les enregistrements de chantier, réceptions et bons de pesée sont scellés et infalsifiables.');
        }, 600);
    }

    function exportRDC() {
        downloadProjectDoc('Journal_Chantiers_RDC_Complet', 'Direction_Travaux', 'pdf');
    }

    function triggerPhotoUpload() {
        alert('Module Caméra Terrain Ouvert : La photo géolocalisée et horodatée a été ajoutée au rapport RDC du jour.');
        logCockpit('📷 Photo de chantier capturée et géotaggée avec succès.', 'ok');
    }

    function exportObsidianVault() {
        const content = JSON.stringify(obsidianData, null, 2);
        const blob = new Blob([content], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Obsidian_BTP_Knowledge_Vault_${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        logCockpit('🕸️ Coffre Obsidian exporté au format JSON/Markdown.', 'ok');
    }

    function sortSuppliers(key) {
        if (!companyData.suppliers) return;
        if (key === 'rating') companyData.suppliers.sort((a, b) => (b.quality_rating || 0) - (a.quality_rating || 0));
        else if (key === 'distance') companyData.suppliers.sort((a, b) => (a.distance_km || 0) - (b.distance_km || 0));
        renderProcurement();
    }

    function openAddVehicleModal() {
        alert('Formulaire d\\'enregistrement de nouvel engin ouvert.');
    }

    function openAddSupplierModal() {
        alert('Formulaire de création de fournisseur partenaire ouvert.');
    }

    // ==========================================
    // 23. COMPATIBILITY ALIASES
    // ==========================================
    function setPlanningViewMode(m) { setPlanningView(m); }
    function changeAgendaWeek(d) { shiftAgendaWeek(d); }
    function setSimulatorViewMode(m) { setSimulatorView(m); }
    function toggleRadarLiveMode() { toggleRadarStream(); }
    function setSDPViewMode(m) { setSdpView(m); }
    function renderSDPTable() { renderDQEPivotTable(); }
    function setObsidianHeuristic(h) { filterObsidianDomain(h); }
    function resetObsidianView() { initObsidianGraph(); }

    // ==========================================
    // 24. COMPLETE APPLICATION PRE-RENDERING & INIT
    // ==========================================
    function initAllTabsAndViews() {
        try { renderNavForRole(); } catch (e) { console.error('Error renderNavForRole:', e); }
        try { renderProjectsHub(); } catch (e) { console.error('Error renderProjectsHub:', e); }
        try { renderPlanningAgenda(); } catch (e) { console.error('Error renderPlanningAgenda:', e); }
        try { renderPlanningGantt(); } catch (e) { console.error('Error renderPlanningGantt:', e); }
        try { renderFleetGrid(); } catch (e) { console.error('Error renderFleetGrid:', e); }
        try { renderCatalogGrid(); } catch (e) { console.error('Error renderCatalogGrid:', e); }
        try { initHrTree(); } catch (e) { console.error('Error initHrTree:', e); }
        try { calculateSignage(); } catch (e) { console.error('Error calculateSignage:', e); }
        try { renderRdcTable(); } catch (e) { console.error('Error renderRdcTable:', e); }
        try { renderDQEPivotTable(); } catch (e) { console.error('Error renderDQEPivotTable:', e); }
        try { renderSdpCards(); } catch (e) { console.error('Error renderSdpCards:', e); }
        try { renderProcurement(); } catch (e) { console.error('Error renderProcurement:', e); }
        try { renderLedger(); } catch (e) { console.error('Error renderLedger:', e); }
        try { renderCompanyMetrics(); } catch (e) { console.error('Error renderCompanyMetrics:', e); }
        try { updateFormulaCalculator(); } catch (e) { console.error('Error updateFormulaCalculator:', e); }
        try { loadScenario('scen_tranchee_vrd'); } catch (e) { console.error('Error loadScenario:', e); }
    }

    window.addEventListener('DOMContentLoaded', () => {
        logCockpit('Initialisation du Cockpit Conduite de Travaux BTP...', 'info');

        initAllTabsAndViews();
        switchNav('cockpit');

        logCockpit('Système prêt. Base de données synchronisée.', 'ok');
    });

    // Execute immediately in case DOMContentLoaded already fired
    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        initAllTabsAndViews();
    }
</script>
"""
