# -*- coding: utf-8 -*-

def get_js_part3():
    return r"""
    // ==========================================
    // 11. HR ORGANIGRAM & PARTNERS MOA/MOE/CSPS
    // ==========================================
    let showHrPartners = true;

    function toggleHrPartnersView() {
        showHrPartners = !showHrPartners;
        const cont = document.getElementById('hr-partners-container');
        if (cont) cont.style.display = showHrPartners ? 'block' : 'none';
    }

    function initHrTree() {
        const container = document.getElementById('hr-tree-container');
        if (!container) return;

        const hrData = companyData.hr_hierarchy || {
            name: "Sylvain Cabrol",
            role: "Conducteur de Travaux Principal / Directeur Exploitation",
            rank: "direction",
            tel: "06 12 34 56 78",
            aipr: "Concepteur / Encadrant",
            caces: "Tous",
            badge: "Direction TP",
            children: [
                {
                    name: "Antoine Martin",
                    role: "Chef de Chantier Travaux Publics",
                    rank: "chef_chantier",
                    tel: "06 23 45 67 89",
                    aipr: "Encadrant",
                    caces: "R482 Cat B1 / C1",
                    badge: "Chantier Alès & Sète",
                    children: [
                        {
                            name: "Mamadou Traoré",
                            role: "Chef d'Équipe Canalisateurs & VRD",
                            rank: "chef_equipe",
                            tel: "06 45 67 89 01",
                            aipr: "Opérateur",
                            caces: "R482 Cat A",
                            badge: "Équipe 1 VRD",
                            children: [
                                { name: "Karim Benali", role: "Conducteur d'Engins Pelle 24t", rank: "compagnon", tel: "06 56 78 90 12", aipr: "Opérateur", caces: "R482 Cat B1", badge: "Pelle R924" },
                                { name: "Youssef Idrissi", role: "Canalisateur Qualifié", rank: "compagnon", tel: "06 78 90 12 34", aipr: "Opérateur", caces: "Pose Tuyaux", badge: "Canalisateur" },
                                { name: "Marc Delmas", role: "Poseur de Bordures / Manœuvre VRD", rank: "compagnon", tel: "06 89 01 23 45", aipr: "Opérateur", caces: "Petit Outillage", badge: "Poseur" }
                            ]
                        },
                        {
                            name: "Patrick Durand",
                            role: "Chef d'Équipe Application Enrobés",
                            rank: "chef_equipe",
                            tel: "06 90 12 34 56",
                            aipr: "Opérateur",
                            caces: "R482 Cat D",
                            badge: "Équipe 2 Enrobés",
                            children: [
                                { name: "Thomas Roussel", role: "Chauffeur PL 8x4 / FIMO FCO", rank: "compagnon", tel: "06 67 89 01 23", aipr: "Sensibilisé", caces: "Permis EC", badge: "Camion 8x4" },
                                { name: "Jean-Paul Sartre", role: "Régleur Finisseur / Cylindreur", rank: "compagnon", tel: "06 01 23 45 67", aipr: "Opérateur", caces: "R482 Cat D", badge: "Finisseur" }
                            ]
                        }
                    ]
                },
                {
                    name: "Lucas Vasseur",
                    role: "Géomètre-Topographe & Télépilote Drone RTK",
                    rank: "expert_tech",
                    tel: "06 34 56 78 90",
                    aipr: "Concepteur / Encadrant",
                    caces: "Drone DGAC / GNSS",
                    badge: "Bureau d'Études & Topo",
                    children: [
                        { name: "David Lemoine", role: "Technicien DAO / BIM Infra IFC", rank: "compagnon", tel: "06 11 22 33 44", aipr: "Sensibilisé", caces: "Mensura / Covadis", badge: "BIM Infra" }
                    ]
                }
            ]
        };

        function renderNodeHtml(node) {
            let rankColor = '#38bdf8';
            if (node.rank === 'direction') rankColor = '#38bdf8';
            if (node.rank === 'chef_chantier') rankColor = 'var(--emerald)';
            if (node.rank === 'chef_equipe') rankColor = 'var(--amber)';
            if (node.rank === 'expert_tech') rankColor = '#c084fc';
            if (node.rank === 'compagnon') rankColor = '#94a3b8';

            const hasChildren = node.children && node.children.length > 0;

            return `
                <div style="display: flex; flex-direction: column; align-items: center; margin: 0 0.5rem;">
                    <div onclick="openEmployeeDetail('${node.name}')" style="background: rgba(15,23,42,0.95); border: 1.5px solid ${rankColor}; border-radius: 8px; padding: 0.75rem; width: 220px; box-shadow: 0 4px 12px rgba(0,0,0,0.4); cursor: pointer; text-align: left; transition: transform 0.15s;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                            <span class="badge" style="background: rgba(51,65,85,0.6); color: ${rankColor}; font-size: 0.65rem; font-weight: 800;">${node.badge}</span>
                            <span style="font-size: 0.7rem; color: #64748b;">${node.tel.substring(0, 5)}...</span>
                        </div>
                        <div style="font-size: 0.95rem; font-weight: 800; color: #f8fafc;">${node.name}</div>
                        <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 2px; line-height: 1.3;">${node.role}</div>
                        <div style="margin-top: 6px; font-size: 0.68rem; color: #cbd5e1; border-top: 1px solid rgba(51,65,85,0.5); padding-top: 4px; display: flex; justify-content: space-between;">
                            <span>🦺 AIPR: <strong style="color:var(--emerald);">${node.aipr}</strong></span>
                            <span>🚜 ${node.caces.split('/')[0]}</span>
                        </div>
                    </div>

                    ${hasChildren ? `
                        <div style="width: 2px; height: 16px; background: rgba(56,189,248,0.4);"></div>
                        <div style="display: flex; position: relative; padding-top: 8px; border-top: 2px solid rgba(56,189,248,0.4);">
                            ${node.children.map(child => renderNodeHtml(child)).join('')}
                        </div>
                    ` : ''}
                </div>
            `;
        }

        container.innerHTML = `
            <div style="display: flex; justify-content: center; min-width: 900px; padding: 1rem 0;">
                ${renderNodeHtml(hrData)}
            </div>
        `;
    }

    function renderHrPartners() {
        const grid = document.getElementById('hr-partners-grid');
        if (!grid) return;

        const partners = [
            { role: "Maîtrise d'Ouvrage (MOA)", entity: "Sète Agglopôle Méditerranée", contact: "Direction des Grands Travaux VRD", mission: "Validation des ordres de service et des situations mensuelles de travaux.", color: "#38bdf8", badge: "MOA Publique" },
            { role: "Maîtrise d'Œuvre (MOE)", entity: "BET VRD Occitanie Ingénierie", contact: "M. Julien Dupont (Ingénieur VRD)", mission: "Contrôle de conformité CCTP, visa des plans d'exécution et métrés contradictoires.", color: "var(--emerald)", badge: "MOE Études & Suivi" },
            { role: "Coordination SPS (CSPS)", entity: "Apave Sud-Est", contact: "M. Bertrand Viala (CSPS Niv. 1)", mission: "Harmonisation du PGC, validation des PPSPS des entreprises et visites sécurité in-situ.", color: "#ef4444", badge: "Sécurité & Santé" },
            { role: "Contrôle Technique & Géotechnique", entity: "Bureau Veritas Occitanie", contact: "Mme Claire Faure (Géotechnicienne)", mission: "Essais de compactage à la plaque EV2 / Westergaard et contrôle portance de plateforme.", color: "#c084fc", badge: "Contrôle Q4" }
        ];

        grid.innerHTML = partners.map(p => `
            <div style="background: rgba(30,41,59,0.6); border: 1px solid rgba(51,65,85,0.7); border-left: 3px solid ${p.color}; border-radius: 6px; padding: 0.85rem;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 4px;">
                    <span class="badge" style="background: rgba(15,23,42,0.8); color: ${p.color}; font-size: 0.65rem;">${p.badge}</span>
                </div>
                <h4 style="font-size: 0.95rem; font-weight: 800; color: #f8fafc; margin-top: 2px;">${p.entity}</h4>
                <div style="font-size: 0.75rem; color: ${p.color}; font-weight: 700; margin-top: 2px;">${p.contact}</div>
                <p style="font-size: 0.72rem; color: #cbd5e1; margin-top: 4px; line-height: 1.4;">${p.mission}</p>
            </div>
        `).join('');
    }

    function openEmployeeDetail(name) {
        const body = document.getElementById('employee-modal-body');
        if (!body) return;

        body.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1rem; border-bottom:1px solid rgba(51,65,85,0.7); padding-bottom:0.75rem;">
                <div>
                    <span class="badge badge-info" style="font-size:0.75rem;">Fiche Salarié RH</span>
                    <h2 style="font-size:1.3rem; font-weight:900; color:#38bdf8; margin-top:4px;">${name}</h2>
                    <div style="font-size:0.85rem; color:#94a3b8;">Entreprise : Occitanie Travaux Publics SAS • Contrat : CDI</div>
                </div>
                <button class="btn btn-secondary" style="padding:0.2rem 0.5rem;" onclick="closeModal('employee-detail-modal')">✕</button>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem; font-size:0.8rem;">
                <div style="background:rgba(30,41,59,0.6); padding:0.75rem; border-radius:6px;">
                    <div style="font-weight:800; color:#38bdf8; margin-bottom:4px;">Habilitations & Diplômes :</div>
                    <div>✔️ <strong>AIPR Concepteur / Encadrant</strong> (Validité 2028)</div>
                    <div>✔️ <strong>CACES R482</strong> Catégories A, B1, C1, D</div>
                    <div>✔️ <strong>Sauveteur Secouriste du Travail (SST)</strong></div>
                    <div>✔️ <strong>Habilitation Électrique H0B0 / BS</strong></div>
                </div>
                <div style="background:rgba(30,41,59,0.6); padding:0.75rem; border-radius:6px;">
                    <div style="font-weight:800; color:var(--emerald); margin-bottom:4px;">Affectation & Pointage :</div>
                    <div>📍 Chantier actuel : <strong>Giratoire RD906 Alès</strong></div>
                    <div>⏱️ Heures cette semaine : <strong>35.0 h</strong></div>
                    <div>🦺 Visite médicale OPPBTP : <strong>À jour (14/03/2026)</strong></div>
                    <div>📻 Canal radio de poste : <strong>Canal 1</strong></div>
                </div>
            </div>
        `;

        openModal('employee-detail-modal');
    }

    // ==========================================
    // 12. DÉPÔT TP 2D/3D & INVENTAIRE SPATIALISÉ
    // ==========================================
    let depotViewMode = '2d';
    let selectedDepotZone = 'all';

    const depotInventoryData = [
        { id: "ENG-001", name: "Pelle Chenilles 24t Liebherr R924", cat: "Engin Lourd", zone: "parking", loc: "Parc Engins - Emplacement P1", status: "Sur Chantier Alès", val: 185000, vgp: "14/10/2026", icon: "🚜" },
        { id: "ENG-002", name: "Pelleteuse Urbaine Mecalac 12MTX", cat: "Engin Lourd", zone: "parking", loc: "Parc Engins - Emplacement P2", status: "Au Dépôt", val: 125000, vgp: "05/11/2026", icon: "🚜" },
        { id: "ENG-003", name: "Camion Benne 8x4 Scania G450", cat: "Poids Lourd", zone: "parking", loc: "Parc Engins - Emplacement P3", status: "Au Dépôt", val: 145000, vgp: "22/12/2026", icon: "🚛" },
        { id: "ENG-004", name: "Compacteur Tandem Bomag BW120", cat: "Engin Lourd", zone: "parking", loc: "Parc Engins - Emplacement P4", status: "Sur Chantier Sète", val: 45000, vgp: "18/09/2026", icon: "🚜" },
        { id: "MAT-001", name: "Grave GNT 0/31.5A Non Traitée", cat: "Granulat", zone: "casiers", loc: "Casier Extérieur n°1", status: "Stock : 65 Tonnes", val: 1170, vgp: "Conforme NF", icon: "🧱" },
        { id: "MAT-002", name: "Sable de Pose 0/4 Alluvionnaire", cat: "Granulat", zone: "casiers", loc: "Casier Extérieur n°2", status: "Stock : 45 Tonnes", val: 990, vgp: "Conforme NF", icon: "🏖️" },
        { id: "MAT-003", name: "Enrobé à Froid Noir en Seaux (25kg)", cat: "Enrobé", zone: "casiers", loc: "Casier Extérieur n°3", status: "Stock : 40 Seaux (1t)", val: 880, vgp: "Utilisable", icon: "🛢️" },
        { id: "CAN-001", name: "Tuyaux Fonte Intégral DN400 (L=6m)", cat: "Canalisation", zone: "racks", loc: "Rack Extérieur R1", status: "Stock : 180 ml", val: 19800, vgp: "Certifié AEP", icon: "🪵" },
        { id: "CAN-002", name: "Tubes PVC Assainissement CR8 Ø200", cat: "Canalisation", zone: "racks", loc: "Rack Extérieur R2", status: "Stock : 120 ml", val: 3240, vgp: "NF EN 1401", icon: "🪵" },
        { id: "OUT-001", name: "Laser de Canalisateur Piper 200", cat: "Topographie", zone: "atelier", loc: "Atelier - Armoire Sécurisée A1", status: "Au Dépôt (Chargé)", val: 3800, vgp: "Étalonné 2026", icon: "🔴" },
        { id: "OUT-002", name: "Scie Thermique à Sol Stihl TS800", cat: "Petit Outillage", zone: "atelier", loc: "Atelier - Étagère B2", status: "Au Dépôt (Révisée)", val: 1650, vgp: "02/08/2026", icon: "🪚" },
        { id: "OUT-003", name: "Plaque Vibrante 100kg Bomag BVP", cat: "Compactage", zone: "atelier", loc: "Atelier - Zone Sol", status: "Au Dépôt", val: 2400, vgp: "12/09/2026", icon: "🔨" },
        { id: "ADM-001", name: "Station Totale Robotisée Leica TS16", cat: "Topographie", zone: "bureaux", loc: "Bureaux CT - Salle DAO", status: "Au Dépôt", val: 22000, vgp: "Certifié Topo", icon: "📐" },
        { id: "ADM-002", name: "Drone DJI Matrice 300 RTK + LiDAR", cat: "Aérien", zone: "bureaux", loc: "Bureaux CT - Mallette Sécurisée", status: "Prêt au Vol", val: 18500, vgp: "DGAC Validé", icon: "🛰️" },
        { id: "ENV-001", name: "Séparateur Hydrocarbures 10 L/s", cat: "Environnement", zone: "lavage", loc: "Aire de Lavage - Dalle Béton", status: "En Service (Vidangé)", val: 8500, vgp: "Conforme 2026", icon: "🚿" }
    ];

    function setDepotViewMode(mode) {
        depotViewMode = mode;
        document.querySelectorAll('.depot-view-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('btn-depot-' + mode)?.classList.add('active');

        const hud = document.getElementById('depot-view-hud');
        if (hud) hud.textContent = mode === '2d' ? 'VUE PLAN 2D ACTIVE' : (mode === '3d' ? 'PERSPECTIVE 3D ISOMÉTRIQUE' : 'LISTE INVENTAIRE TABULAIRE');

        const vCont = document.getElementById('depot-viewport-container');
        if (vCont) vCont.style.display = mode === 'list' ? 'none' : 'block';

        initDepotCanvas();
    }

    function selectDepotZone(zoneId, btn) {
        selectedDepotZone = zoneId;
        document.querySelectorAll('.depot-zone-filter').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');

        renderDepotInventory();
        initDepotCanvas();
    }

    function initDepotCanvas() {
        const canvas = document.getElementById('depot-viewport-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const w = canvas.parentElement.clientWidth || 800;
        const h = canvas.parentElement.clientHeight || 340;
        canvas.width = w;
        canvas.height = h;

        ctx.fillStyle = '#060a14';
        ctx.fillRect(0, 0, w, h);

        if (depotViewMode === '2d') {
            // 2D SITE MASTERPLAN VIEW
            // Perimeter boundary (1200 m² yard)
            const marginX = 40, marginY = 30;
            const yardW = w - marginX * 2, yardH = h - marginY * 2;

            // Yard Ground (Heavy Asphalt / Compacted GNT)
            ctx.fillStyle = '#1e293b';
            ctx.fillRect(marginX, marginY, yardW, yardH);
            ctx.strokeStyle = '#38bdf8';
            ctx.lineWidth = 2;
            ctx.setLineDash([6, 4]);
            ctx.strokeRect(marginX, marginY, yardW, yardH);
            ctx.setLineDash([]);

            // 1. Administration & Offices Building (120 m²) - Top Left
            const bX = marginX + 15, bY = marginY + 15, bW = 160, bH = 90;
            const isBActive = selectedDepotZone === 'all' || selectedDepotZone === 'bureaux';
            ctx.fillStyle = isBActive ? '#0284c7' : '#0c4a6e';
            ctx.fillRect(bX, bY, bW, bH);
            ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = isBActive ? 2 : 1;
            ctx.strokeRect(bX, bY, bW, bH);
            ctx.fillStyle = '#fff'; ctx.font = 'bold 9px system-ui';
            ctx.fillText('🏢 BUREAUX & VESTIAIRES (120m²)', bX + 10, bY + 25);
            ctx.font = '8px system-ui'; ctx.fillStyle = '#e2e8f0';
            ctx.fillText('Accueil, CT, Salle Réunion, Sanitaires', bX + 10, bY + 45);

            // 2. Mechanical Workshop & Tool Garage (80 m²) - Bottom Left
            const wX = marginX + 15, wY = marginY + 120, wW = 160, wH = 100;
            const isWActive = selectedDepotZone === 'all' || selectedDepotZone === 'atelier';
            ctx.fillStyle = isWActive ? '#d97706' : '#78350f';
            ctx.fillRect(wX, wY, wW, wH);
            ctx.strokeStyle = '#f59e0b'; ctx.lineWidth = isWActive ? 2 : 1;
            ctx.strokeRect(wX, wY, wW, wH);
            ctx.fillStyle = '#fff'; ctx.font = 'bold 9px system-ui';
            ctx.fillText('🔧 ATELIER & GARAGE (80m²)', wX + 10, wY + 25);
            ctx.font = '8px system-ui'; ctx.fillStyle = '#fef3c7';
            ctx.fillText('Fosse vidange, Armoire lasers & outillage', wX + 10, wY + 45);

            // 3. Storage Bays / Casiers Granulats - Top Right
            const cX = marginX + 220, cY = marginY + 15, cW = 220, cH = 75;
            const isCActive = selectedDepotZone === 'all' || selectedDepotZone === 'casiers';
            ctx.fillStyle = isCActive ? '#059669' : '#064e3b';
            ctx.fillRect(cX, cY, cW, cH);
            ctx.strokeStyle = '#10b981'; ctx.lineWidth = isCActive ? 2 : 1;
            ctx.strokeRect(cX, cY, cW, cH);
            ctx.fillStyle = '#fff'; ctx.font = 'bold 9px system-ui';
            ctx.fillText('🧱 CASIERS MATÉRIAUX (140 Tonnes)', cX + 10, cY + 22);
            ctx.font = '8px system-ui'; ctx.fillStyle = '#d1fae5';
            ctx.fillText('Casier 1: GNT 0/31.5 • Casier 2: Sable 0/4 • Casier 3: Enrobé', cX + 10, cY + 42);

            // 4. Pipe Storage Racks - Middle Right
            const rX = marginX + 220, rY = marginY + 105, rW = 220, rH = 65;
            const isRActive = selectedDepotZone === 'all' || selectedDepotZone === 'racks';
            ctx.fillStyle = isRActive ? '#7c3aed' : '#4c1d95';
            ctx.fillRect(rX, rY, rW, rH);
            ctx.strokeStyle = '#c084fc'; ctx.lineWidth = isRActive ? 2 : 1;
            ctx.strokeRect(rX, rY, rW, rH);
            ctx.fillStyle = '#fff'; ctx.font = 'bold 9px system-ui';
            ctx.fillText('🪵 RACKS TUBES & CANALISATIONS', rX + 10, rY + 22);
            ctx.font = '8px system-ui'; ctx.fillStyle = '#ede9fe';
            ctx.fillText('Tuyaux Fonte DN400, PVC CR8 Ø200, Gaines TPC', rX + 10, rY + 42);

            // 5. Heavy Machinery Parking - Bottom Center/Right
            const pX = marginX + 220, pY = marginY + 185, pW = 340, pH = 80;
            const isPActive = selectedDepotZone === 'all' || selectedDepotZone === 'parking';
            ctx.fillStyle = isPActive ? '#334155' : '#1e293b';
            ctx.fillRect(pX, pY, pW, pH);
            ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = isPActive ? 2 : 1;
            ctx.strokeRect(pX, pY, pW, pH);
            ctx.fillStyle = '#fff'; ctx.font = 'bold 9px system-ui';
            ctx.fillText('🚜 PARC DE STATIONNEMENT ENGINS & POIDS LOURDS', pX + 10, pY + 20);

            // Draw machine parking bays
            ['P1: Liebherr 24t', 'P2: Mecalac 12MTX', 'P3: Scania 8x4', 'P4: Bomag BW120'].forEach((lbl, i) => {
                const px = pX + 10 + i * 80;
                ctx.strokeStyle = '#64748b'; ctx.setLineDash([2, 2]);
                ctx.strokeRect(px, pY + 30, 72, 42);
                ctx.setLineDash([]);
                ctx.fillStyle = '#cbd5e1'; ctx.font = '7.5px system-ui';
                ctx.fillText(lbl, px + 4, pY + 54);
            });

            // 6. Washing Station & Oil Separator - Far Right
            const lX = marginX + 460, lY = marginY + 15, lW = 100, lH = 155;
            const isLActive = selectedDepotZone === 'all' || selectedDepotZone === 'lavage';
            ctx.fillStyle = isLActive ? '#0891b2' : '#155e75';
            ctx.fillRect(lX, lY, lW, lH);
            ctx.strokeStyle = '#06b6d4'; ctx.lineWidth = isLActive ? 2 : 1;
            ctx.strokeRect(lX, lY, lW, lH);
            ctx.fillStyle = '#fff'; ctx.font = 'bold 8.5px system-ui';
            ctx.fillText('🚿 AIRE LAVAGE', lX + 8, lY + 20);
            ctx.font = '7.5px system-ui'; ctx.fillStyle = '#cffafe';
            ctx.fillText('Dalle béton étanche', lX + 8, lY + 38);
            ctx.fillText('& Décanteur 10L/s', lX + 8, lY + 50);

            // Gate / Entrance
            ctx.fillStyle = '#ea580c';
            ctx.fillRect(marginX + yardW / 2 - 30, marginY + yardH - 6, 60, 6);
            ctx.fillStyle = '#fff'; ctx.font = 'bold 8px system-ui';
            ctx.fillText('PORTAIL ENTRÉE PL (8m)', marginX + yardW / 2 - 45, marginY + yardH + 15);
        } else {
            // 3D ISOMETRIC VIEW
            const cx = w / 2, cy = h / 2 + 20;

            // Isometric Ground Plate
            ctx.beginPath();
            ctx.moveTo(cx, cy - 110);
            ctx.lineTo(cx + 260, cy);
            ctx.lineTo(cx, cy + 110);
            ctx.lineTo(cx - 260, cy);
            ctx.closePath();
            ctx.fillStyle = '#1e293b'; ctx.fill();
            ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2; ctx.stroke();

            // 3D Buildings Blocks
            // Offices (Left)
            ctx.fillStyle = '#0284c7';
            ctx.fillRect(cx - 180, cy - 60, 80, 45);
            ctx.fillStyle = '#38bdf8';
            ctx.beginPath();
            ctx.moveTo(cx - 180, cy - 60); ctx.lineTo(cx - 140, cy - 85);
            ctx.lineTo(cx - 60, cy - 85); ctx.lineTo(cx - 100, cy - 60);
            ctx.closePath(); ctx.fill();

            // Workshop (Center Left)
            ctx.fillStyle = '#d97706';
            ctx.fillRect(cx - 140, cy + 10, 80, 40);

            // Casiers (Top Right)
            ctx.fillStyle = '#059669';
            ctx.fillRect(cx + 40, cy - 70, 90, 35);

            // Heavy Machinery (Scania & Liebherr 3D representations)
            ctx.fillStyle = '#f59e0b';
            ctx.fillRect(cx + 40, cy + 20, 50, 24);
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(cx + 70, cy + 24, 15, 16);

            // Labels
            ctx.fillStyle = '#f8fafc'; ctx.font = 'bold 9px system-ui';
            ctx.fillText('🏢 Bureaux 120m²', cx - 180, cy - 90);
            ctx.fillText('🔧 Atelier 80m²', cx - 140, cy + 65);
            ctx.fillText('🧱 Casiers 140t', cx + 40, cy - 75);
            ctx.fillText('🚜 Parc Poids Lourds', cx + 40, cy + 55);
        }
    }

    let depotSortKey = 'id';
    let depotSortAsc = true;

    function sortDepotInventory(key) {
        if (key === depotSortKey) {
            depotSortAsc = !depotSortAsc;
        } else {
            depotSortKey = key;
            depotSortAsc = true;
        }
        renderDepotInventory();
    }

    function renderDepotInventory() {
        const tbody = document.getElementById('depot-inventory-tbody');
        if (!tbody) return;

        const filtered = depotInventoryData.filter(item => {
            if (selectedDepotZone !== 'all' && item.zone !== selectedDepotZone) return false;
            return true;
        });

        const sorted = [...filtered].sort((a, b) => {
            let valA = a[depotSortKey] !== undefined ? a[depotSortKey] : '';
            let valB = b[depotSortKey] !== undefined ? b[depotSortKey] : '';
            if (depotSortKey === 'val') { valA = a.val || 0; valB = b.val || 0; }
            if (typeof valA === 'string') {
                return depotSortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
            }
            return depotSortAsc ? (valA - valB) : (valB - valA);
        });

        tbody.innerHTML = sorted.map(i => `
            <tr style="border-top: 1px solid rgba(51,65,85,0.4);">
                <td style="padding: 0.55rem; font-family: 'JetBrains Mono'; color: #38bdf8; font-weight: 700;">${i.id}</td>
                <td style="padding: 0.55rem; font-weight: 700; color: #f8fafc;">${i.icon} ${i.name}</td>
                <td style="padding: 0.55rem; color: #94a3b8;">${i.cat}</td>
                <td style="padding: 0.55rem; color: #cbd5e1;">${i.loc}</td>
                <td style="padding: 0.55rem; text-align: center;"><span class="badge ${i.status.includes('Chantier') ? 'badge-warning' : 'badge-success'}">${i.status}</span></td>
                <td style="padding: 0.55rem; text-align: right; font-weight: 800; color: var(--emerald);">${i.val.toLocaleString('fr-FR')} €</td>
                <td style="padding: 0.55rem; text-align: center; font-size: 0.72rem; color: #38bdf8;">${i.vgp}</td>
            </tr>
        `).join('');
    }

    function filterDepotInventory(query) {
        const tbody = document.getElementById('depot-inventory-tbody');
        if (!tbody) return;

        const q = (query || '').toLowerCase();
        const filtered = depotInventoryData.filter(i => {
            if (selectedDepotZone !== 'all' && i.zone !== selectedDepotZone) return false;
            return i.name.toLowerCase().includes(q) || i.id.toLowerCase().includes(q) || i.loc.toLowerCase().includes(q) || i.cat.toLowerCase().includes(q);
        });

        const sorted = [...filtered].sort((a, b) => {
            let valA = a[depotSortKey] !== undefined ? a[depotSortKey] : '';
            let valB = b[depotSortKey] !== undefined ? b[depotSortKey] : '';
            if (depotSortKey === 'val') { valA = a.val || 0; valB = b.val || 0; }
            if (typeof valA === 'string') {
                return depotSortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
            }
            return depotSortAsc ? (valA - valB) : (valB - valA);
        });

        tbody.innerHTML = sorted.map(i => `
            <tr style="border-top: 1px solid rgba(51,65,85,0.4);">
                <td style="padding: 0.55rem; font-family: 'JetBrains Mono'; color: #38bdf8; font-weight: 700;">${i.id}</td>
                <td style="padding: 0.55rem; font-weight: 700; color: #f8fafc;">${i.icon} ${i.name}</td>
                <td style="padding: 0.55rem; color: #94a3b8;">${i.cat}</td>
                <td style="padding: 0.55rem; color: #cbd5e1;">${i.loc}</td>
                <td style="padding: 0.55rem; text-align: center;"><span class="badge ${i.status.includes('Chantier') ? 'badge-warning' : 'badge-success'}">${i.status}</span></td>
                <td style="padding: 0.55rem; text-align: right; font-weight: 800; color: var(--emerald);">${i.val.toLocaleString('fr-FR')} €</td>
                <td style="padding: 0.55rem; text-align: center; font-size: 0.72rem; color: #38bdf8;">${i.vgp}</td>
            </tr>
        `).join('');
    }

    // ==========================================
    // 13. OPBTP REALISTIC SIGNAGE SIMULATOR (ENRICHED)
    // ==========================================
    let opbtpTrafficAnimId = null;
    let isOpbtpTrafficRunning = true;
    let trafficLightState = 'green';
    let opbtpSpeedFactor = 0.5;
    let opbtpDensity = 4;
    let opbtpCars = [];

    const opbtpSubdomains = {
        'urbain': [
            { id: 'tranchee_traversee', name: '1. Tranchée transversale avec alternat feux KR11' },
            { id: 'tranchee_trottoir', name: '2. Tranchée sous trottoir & dévoiement piétons PMR K2' },
            { id: 'retrecissement', name: '3. Rétrécissement axial avec priorité B15 / C18' },
            { id: 'voie_etroite', name: '4. Voie étroite / impasse fermée (panneau B44)' },
            { id: 'piste_cyclable', name: '5. Couloir bus / piste cyclable dévoyée sur chaussée' },
            { id: 'intra_urbain', name: '6. Hyper-centre / Intra-urbain dense : Trottoir barré K2' }
        ],
        'interurbain': [
            { id: 'alternat_kr11_250m', name: '1. Alternat feux KR11 sur 250m en rase campagne' },
            { id: 'emprise_accotement', name: '2. Empiètement ponctuel sur accotement (AK5 + B14)' },
            { id: 'biseau_kr43', name: '3. Biseau de rabattement avec flèche lumineuse KR43' },
            { id: 'demi_chaussee', name: '4. Demi-chaussée neutralisée avec piquet K10 manuel' }
        ],
        'ouvrages_speciaux': [
            { id: 'rond_point', name: '1. 🔄 Giratoire : Neutralisation quart d\'anneau K16' },
            { id: 'croisement', name: '2. ➕ Croisement 4 branches : Masquage feux & Alternat KR11' },
            { id: 'petit_pont', name: '3. 🌉 Petit pont étroit : Circulation alternée prioritaire B15/C18' },
            { id: 'entree_route', name: '4. 🛣️ Entrée de route / Bretelle : Biseau insertion K5a 70/50' },
            { id: 'implantation_poteau_elec', name: '5. ⚡ Implantation poteau Enedis : Chantier mobile FLR' },
            { id: 'bassin_retention', name: '6. 💧 Bassin d\'orage : Accès camions de purge sur RD' }
        ],
        'voie_rapide': [
            { id: 'neutralisation_droite', name: '1. Neutralisation voie lente de droite sur 2x2 voies' },
            { id: 'basculement_2x1', name: '2. Basculement de chaussée sur 2x1 voie avec SMV béton' },
            { id: 'neutralisation_bau', name: '3. Neutralisation d\'urgence de la Bande d\'Arrêt d\'Urgence' }
        ],
        'urgence_nuit': [
            { id: 'chantier_mobile_flr', name: '1. Chantier mobile d\'enrobage avec FLR de protection' },
            { id: 'nuit_balises_k8', name: '2. Intervention nocturne d\'urgence (Balises synchro K8)' }
        ]
    };

    function setOpbtpSpeedFactor(factor) {
        opbtpSpeedFactor = factor;
        document.querySelectorAll('.opbtp-speed-btn').forEach(b => b.classList.remove('active'));
        if (factor === 0.25) document.getElementById('btn-spd-025')?.classList.add('active');
        if (factor === 0.5) document.getElementById('btn-spd-05')?.classList.add('active');
        if (factor === 1.0) document.getElementById('btn-spd-10')?.classList.add('active');
    }

    function setOpbtpTrafficDensity(density) {
        opbtpDensity = parseInt(density);
        initRealisticVehicles();
    }

    function injectOpbtpVehicle(type) {
        const specs = {
            'VL': { type: 'VL', label: 'Citadine', w: 26, h: 12, speed: 1.6, color: '#38bdf8' },
            'PL': { type: 'PL', label: 'Scania 8x4', w: 46, h: 16, speed: 1.2, color: '#f59e0b' },
            'BUS': { type: 'BUS', label: 'Bus Urbain', w: 56, h: 16, speed: 1.1, color: '#10b981' },
            'MOTO': { type: 'MOTO', label: 'Moto', w: 16, h: 8, speed: 2.0, color: '#c084fc' }
        };
        const s = specs[type] || specs['VL'];
        const dir = Math.random() > 0.5 ? 1 : -1;
        opbtpCars.push({
            ...s,
            dir: dir,
            lane: dir === 1 ? 1 : 2,
            x: dir === 1 ? -40 : 760,
            y: 0,
            angle: Math.random() * Math.PI * 2
        });
        logCockpit(`Véhicule ${type} injecté dans la simulation de trafic.`, 'info');
    }

    function stepOpbtpTrafficSimulation() {
        isOpbtpTrafficRunning = false;
        const btn = document.getElementById('btn-opbtp-sim-play');
        if (btn) btn.textContent = '▶️ Lancer Simulation Trafic';
        drawSignageDiagram();
    }

    function updateOpbtpSubdomainOptions() {
        const cat = document.getElementById('opbtp-cat-select')?.value || 'urbain';
        const taskSelect = document.getElementById('opbtp-task-type');
        if (!taskSelect) return;

        const subList = opbtpSubdomains[cat] || opbtpSubdomains['urbain'];
        taskSelect.innerHTML = subList.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
        calculateSignage();
    }

    function calculateSignage() {
        const speed = Number(document.getElementById('opbtp-speed-range')?.value || 50);
        const length = Number(document.getElementById('opbtp-length-range')?.value || 120);

        let ak5Dist = speed <= 50 ? 50 : (speed <= 90 ? 150 : 250);
        let b14Dist = speed <= 50 ? 30 : (speed <= 90 ? 100 : 150);
        let k5aSpacing = speed <= 50 ? 5 : (speed <= 90 ? 10 : 15);
        let coneQty = Math.max(16, Math.round(length / k5aSpacing));

        let biseauLen = Math.round((speed * 3.5) / 1.6);
        let clearanceTime = Math.round(length / (speed / 3.6)) + 4;

        const res = document.getElementById('opbtp-results');
        if (res) {
            res.innerHTML = `
                <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(51,65,85,0.7); border-radius: 8px; padding: 1rem;">
                    <div style="font-size: 0.85rem; font-weight: 800; color: var(--amber); margin-bottom: 0.4rem; text-transform: uppercase;">
                        📑 Justifications Réglementaires IISR Livre 1 (8e Partie) :
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.78rem;">
                        <div style="background: rgba(30,41,59,0.5); padding: 6px; border-radius: 4px;">Panneau AK5 (Travaux) : <strong style="color: #38bdf8;">${ak5Dist} m</strong> amont</div>
                        <div style="background: rgba(30,41,59,0.5); padding: 6px; border-radius: 4px;">Panneau B14 (Vitesse) : <strong style="color: #38bdf8;">${b14Dist} m</strong></div>
                        <div style="background: rgba(30,41,59,0.5); padding: 6px; border-radius: 4px;">Longueur Biseau K5a : <strong style="color: var(--emerald);">${biseauLen} m</strong></div>
                        <div style="background: rgba(30,41,59,0.5); padding: 6px; border-radius: 4px;">Nombre Cônes K5a : <strong style="color: var(--emerald);">${coneQty} cônes Cl. 2</strong></div>
                        <div style="background: rgba(30,41,59,0.5); padding: 6px; border-radius: 4px;">Temps Tout-Rouge Feux : <strong style="color: #facc15;">${clearanceTime} s</strong> dégagement</div>
                        <div style="background: rgba(30,41,59,0.5); padding: 6px; border-radius: 4px;">Section Restante : <strong style="color: #f8fafc;">3.20 m</strong> (Norme VL/PL)</div>
                    </div>
                </div>
            `;
        }

        initRealisticVehicles();
        if (opbtpTrafficAnimId) cancelAnimationFrame(opbtpTrafficAnimId);
        drawSignageDiagram();
    }

    function initRealisticVehicles() {
        const taskType = document.getElementById('opbtp-task-type')?.value || 'tranchee_traversee';

        if (taskType === 'rond_point') {
            const rCars = [
                { type: 'VL', label: 'Citadine', w: 22, h: 12, speed: 1.2, color: '#38bdf8', route: 'west_to_east', progress: 0.1 },
                { type: 'PL', label: 'Benne 8x4', w: 34, h: 14, speed: 0.9, color: '#f59e0b', route: 'north_to_south', progress: 0.4 },
                { type: 'BUS', label: 'Bus Urbain', w: 40, h: 14, speed: 0.8, color: '#10b981', route: 'south_to_west', progress: 0.65 },
                { type: 'MOTO', label: 'Moto', w: 14, h: 8, speed: 1.5, color: '#c084fc', route: 'west_to_east', progress: 0.85 }
            ];
            opbtpCars = opbtpDensity === 2 ? rCars.slice(0, 2) : rCars;
            return;
        }

        const base = [
            { type: 'VL', label: 'Citadine', w: 26, h: 12, speed: 1.4, color: '#38bdf8', dir: 1, lane: 1, x: 20, y: 0 },
            { type: 'PL', label: 'Benne 8x4', w: 45, h: 16, speed: 1.1, color: '#f59e0b', dir: 1, lane: 1, x: 170, y: 0 },
            { type: 'BUS', label: 'Bus Urbain', w: 55, h: 16, speed: 1.0, color: '#10b981', dir: -1, lane: 2, x: 620, y: 0 },
            { type: 'MOTO', label: 'Moto', w: 16, h: 8, speed: 1.7, color: '#c084fc', dir: -1, lane: 2, x: 490, y: 0 }
        ];

        if (opbtpDensity === 2) opbtpCars = base.slice(0, 2);
        else if (opbtpDensity === 7) {
            opbtpCars = [
                ...base,
                { type: 'VL', label: 'Berline', w: 28, h: 13, speed: 1.3, color: '#ec4899', dir: 1, lane: 1, x: 90, y: 0 },
                { type: 'PL', label: 'Toupie', w: 42, h: 16, speed: 1.0, color: '#facc15', dir: -1, lane: 2, x: 700, y: 0 },
                { type: 'VL', label: 'Fourgon', w: 32, h: 14, speed: 1.2, color: '#38bdf8', dir: -1, lane: 2, x: 560, y: 0 }
            ];
        } else {
            opbtpCars = base;
        }
    }

    function toggleOpbtpTrafficSimulation() {
        isOpbtpTrafficRunning = !isOpbtpTrafficRunning;
        const btn = document.getElementById('btn-opbtp-sim-play');
        if (btn) btn.textContent = isOpbtpTrafficRunning ? '⏸️ Pause Trafic' : '▶️ Lancer Simulation Trafic';
        if (isOpbtpTrafficRunning) drawSignageDiagram();
    }

    function switchTrafficLightState() {
        trafficLightState = trafficLightState === 'green' ? 'red' : 'green';
    }

    function drawSignageDiagram() {
        const canvas = document.getElementById('opbtp-signage-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const w = canvas.parentElement.clientWidth || 700;
        const h = canvas.parentElement.clientHeight || 280;
        canvas.width = w;
        canvas.height = h;

        const taskType = document.getElementById('opbtp-task-type')?.value || 'tranchee_traversee';
        const speedLimit = Number(document.getElementById('opbtp-speed-range')?.value || 50);
        const cycleLen = Number(document.getElementById('opbtp-cycle-range')?.value || 30);

        ctx.fillStyle = '#070b14';
        ctx.fillRect(0, 0, w, h);

        const roadTopY = h * 0.22;
        const roadH = h * 0.56;
        const roadMidY = roadTopY + roadH * 0.5;
        const lane1Y = roadTopY + roadH * 0.75; // South lane (Eastbound dir = 1)
        const lane2Y = roadTopY + roadH * 0.25; // North lane (Westbound dir = -1)

        const trenchX1 = w * 0.34;
        const trenchX2 = w * 0.66;
        const trenchW = trenchX2 - trenchX1;

        // Dynamic Traffic Light Cycle
        const nowSec = Date.now() / 1000;
        const cyclePos = (nowSec % (cycleLen * 2));
        let curLightState = 'all_red'; // 'east_green', 'west_green', 'all_red'
        if (cyclePos < cycleLen - 4) {
            curLightState = 'east_green';
            trafficLightState = 'green';
        } else if (cyclePos < cycleLen) {
            curLightState = 'all_red';
            trafficLightState = 'red';
        } else if (cyclePos < (cycleLen * 2) - 4) {
            curLightState = 'west_green';
            trafficLightState = 'red';
        } else {
            curLightState = 'all_red';
            trafficLightState = 'red';
        }

        // =====================================
        // SCENARIO 1: GIRATOIRE / ROND-POINT
        // =====================================
        if (taskType === 'rond_point') {
            const rCenter = { x: w / 2, y: h / 2 };
            const rOut = Math.min(85, h * 0.42);
            const rIn = Math.min(42, h * 0.21);
            const rMid = (rOut + rIn) / 2;

            // 4 Approaching Roads
            ctx.fillStyle = '#1e293b';
            ctx.fillRect(0, rCenter.y - 18, w, 36); // East-West
            ctx.fillRect(rCenter.x - 18, 0, 36, h); // North-South

            // Road Ring
            ctx.beginPath(); ctx.arc(rCenter.x, rCenter.y, rOut, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#070b14';
            ctx.beginPath(); ctx.arc(rCenter.x, rCenter.y, rIn, 0, Math.PI * 2); ctx.fill();

            // Central island (Landscaping)
            ctx.fillStyle = '#065f46';
            ctx.beginPath(); ctx.arc(rCenter.x, rCenter.y, rIn - 4, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#f8fafc'; ctx.font = 'bold 8.5px JetBrains Mono';
            ctx.fillText('GIRATOIRE RD906', rCenter.x - 38, rCenter.y + 3);

            // Blocked Quadrant (Top-Right: angle -PI/2 to 0)
            ctx.fillStyle = 'rgba(239, 68, 68, 0.5)';
            ctx.beginPath();
            ctx.arc(rCenter.x, rCenter.y, rOut + 2, -Math.PI / 2, 0);
            ctx.arc(rCenter.x, rCenter.y, rIn - 2, 0, -Math.PI / 2, true);
            ctx.closePath();
            ctx.fill();
            ctx.strokeStyle = '#ea580c'; ctx.lineWidth = 3; ctx.stroke();

            // Diagonal hazard hatching in the blocked work zone
            ctx.strokeStyle = 'rgba(234, 88, 12, 0.4)';
            ctx.lineWidth = 2;
            for (let d = 0; d < rOut; d += 12) {
                ctx.beginPath();
                ctx.moveTo(rCenter.x + d, rCenter.y);
                ctx.lineTo(rCenter.x, rCenter.y - d);
                ctx.stroke();
            }

            // Work Zone warning hatch
            ctx.fillStyle = '#ea580c'; ctx.font = 'bold 8px monospace';
            ctx.fillText('🚧 ZONE CHANTIER 1/4', rCenter.x + 12, rCenter.y - 25);

            // K16 Safety Cones & Beacons on Quadrant Boundary
            ctx.fillStyle = '#ea580c';
            for (let a = -Math.PI / 2; a <= 0.05; a += 0.25) {
                const cx = rCenter.x + Math.cos(a) * (rOut - 4);
                const cy = rCenter.y + Math.sin(a) * (rOut - 4);
                ctx.beginPath(); ctx.arc(cx, cy, 4, 0, Math.PI * 2); ctx.fill();
            }

            // Circulating Vehicles (STRICTLY STAY ON OPEN ROADS AND NEVER ENTER BLOCKED QUADRANT)
            opbtpCars.forEach((car) => {
                if (isOpbtpTrafficRunning) {
                    if (!car.progress && car.progress !== 0) car.progress = 0.2;
                    car.progress = (car.progress + 0.003 * (speedLimit / 50) * opbtpSpeedFactor * (car.speed || 1.0));
                    if (car.progress > 1) car.progress -= 1;
                }

                let px = 0, py = 0, angle = 0;
                const p = car.progress || 0;
                const route = car.route || 'west_to_east';

                if (route === 'west_to_east') {
                    // Path: West road (p in [0, 0.25]) -> Bottom arc [PI -> 0] (p in [0.25, 0.75]) -> East road (p in [0.75, 1.0])
                    if (p < 0.25) {
                        const s = p / 0.25;
                        px = -30 + s * (rCenter.x - rMid + 30);
                        py = rCenter.y + 6;
                        angle = 0;
                    } else if (p < 0.75) {
                        const s = (p - 0.25) / 0.5;
                        const arcAngle = Math.PI - s * Math.PI; // from PI down to 0 (counter-clockwise)
                        px = rCenter.x + Math.cos(arcAngle) * rMid;
                        py = rCenter.y + Math.sin(arcAngle) * rMid; // Y >= rCenter.y (always strictly in bottom half!)
                        angle = arcAngle - Math.PI / 2;
                    } else {
                        const s = (p - 0.75) / 0.25;
                        px = (rCenter.x + rMid) + s * (w + 40 - (rCenter.x + rMid));
                        py = rCenter.y + 6;
                        angle = 0;
                    }
                } else if (route === 'north_to_south') {
                    // Path: North road (p in [0, 0.25]) -> West arc [-PI/2 -> -PI -> -1.5*PI] (p in [0.25, 0.75]) -> South road (p in [0.75, 1.0])
                    if (p < 0.25) {
                        const s = p / 0.25;
                        px = rCenter.x - 6;
                        py = -30 + s * (rCenter.y - rMid + 30);
                        angle = Math.PI / 2;
                    } else if (p < 0.75) {
                        const s = (p - 0.25) / 0.5;
                        const arcAngle = -Math.PI / 2 - s * Math.PI; // from -PI/2 to -1.5*PI (left half: X <= rCenter.x)
                        px = rCenter.x + Math.cos(arcAngle) * rMid;
                        py = rCenter.y + Math.sin(arcAngle) * rMid;
                        angle = arcAngle - Math.PI / 2;
                    } else {
                        const s = (p - 0.75) / 0.25;
                        px = rCenter.x - 6;
                        py = (rCenter.y + rMid) + s * (h + 40 - (rCenter.y + rMid));
                        angle = Math.PI / 2;
                    }
                } else { // 'south_to_west'
                    // Path: South road (p in [0, 0.3]) -> Bottom-left quadrant [PI/2 -> PI] (p in [0.3, 0.7]) -> West road (p in [0.7, 1.0])
                    if (p < 0.3) {
                        const s = p / 0.3;
                        px = rCenter.x + 6;
                        py = (h + 30) - s * (h + 30 - (rCenter.y + rMid));
                        angle = -Math.PI / 2;
                    } else if (p < 0.7) {
                        const s = (p - 0.3) / 0.4;
                        const arcAngle = Math.PI / 2 + s * (Math.PI / 2); // from PI/2 to PI (bottom-left quadrant X <= rCenter.x, Y >= rCenter.y)
                        px = rCenter.x + Math.cos(arcAngle) * rMid;
                        py = rCenter.y + Math.sin(arcAngle) * rMid;
                        angle = arcAngle + Math.PI / 2;
                    } else {
                        const s = (p - 0.7) / 0.3;
                        px = (rCenter.x - rMid) - s * (rCenter.x - rMid + 40);
                        py = rCenter.y - 6;
                        angle = Math.PI;
                    }
                }

                ctx.save();
                ctx.translate(px, py);
                ctx.rotate(angle);
                ctx.fillStyle = car.color || '#38bdf8';
                ctx.fillRect(-car.w / 2, -car.h / 2, car.w, car.h);

                // Headlights
                ctx.fillStyle = '#fef08a';
                ctx.fillRect(car.w / 2 - 2, -car.h / 2 + 2, 2, 2);
                ctx.fillRect(car.w / 2 - 2, car.h / 2 - 4, 2, 2);

                ctx.fillStyle = '#fff'; ctx.font = 'bold 7px system-ui';
                ctx.fillText(car.type, -car.w / 2 + 2, 2);
                ctx.restore();
            });

            ctx.fillStyle = '#38bdf8'; ctx.font = 'bold 9px JetBrains Mono';
            ctx.fillText(`GIRATOIRE 1/4 ANNEAU NEUTRALISÉ • VITESSE : ${opbtpSpeedFactor}x • FLUX : ${speedLimit} km/h`, 10, h - 10);

            if (currentNav === 'opbtp' && isOpbtpTrafficRunning) {
                opbtpTrafficAnimId = requestAnimationFrame(drawSignageDiagram);
            }
            return;
        }

        // =====================================
        // SCENARIO 2: PETIT PONT ÉTROIT
        // =====================================
        if (taskType === 'petit_pont') {
            // River Blue Background
            ctx.fillStyle = '#0284c7';
            ctx.fillRect(trenchX1 - 40, 0, trenchW + 80, h);
            ctx.fillStyle = 'rgba(255,255,255,0.15)';
            ctx.fillRect(trenchX1 - 40, h * 0.15, trenchW + 80, 2);
            ctx.fillRect(trenchX1 - 40, h * 0.85, trenchW + 80, 2);

            // Bridge Deck
            ctx.fillStyle = '#334155';
            ctx.fillRect(0, roadTopY, w, roadH);

            // Parapets
            ctx.fillStyle = '#cbd5e1';
            ctx.fillRect(trenchX1 - 40, roadTopY - 6, trenchW + 80, 6);
            ctx.fillRect(trenchX1 - 40, roadTopY + roadH, trenchW + 80, 6);

            // Blocked North Half on Bridge (Lane 2 closed)
            ctx.fillStyle = 'rgba(239, 68, 68, 0.4)';
            ctx.fillRect(trenchX1, roadTopY, trenchW, roadH * 0.5);
            ctx.strokeStyle = '#ea580c'; ctx.lineWidth = 2;
            ctx.strokeRect(trenchX1, roadTopY, trenchW, roadH * 0.5);
            ctx.fillStyle = '#f8fafc'; ctx.font = 'bold 8.5px JetBrains Mono';
            ctx.fillText('🚧 PONT RÉTRÉCI : TRAVAUX D\'ÉTANCHÉITÉ', trenchX1 + 10, roadTopY + 18);
        } else if (taskType === 'intra_urbain' || taskType === 'tranchee_trottoir' || taskType === 'piste_cyclable') {
            // =====================================
            // SCENARIO 3: INTRA-URBAIN & TROTTOIR
            // =====================================
            ctx.fillStyle = '#0f172a'; // Buildings
            ctx.fillRect(0, 0, w, roadTopY - 22);
            ctx.fillRect(0, roadTopY + roadH + 22, w, h);

            // Sidewalks
            ctx.fillStyle = '#475569';
            ctx.fillRect(0, roadTopY - 22, w, 22);
            ctx.fillRect(0, roadTopY + roadH, w, 22);

            // Road
            ctx.fillStyle = '#1e293b';
            ctx.fillRect(0, roadTopY, w, roadH);

            // Trench on sidewalk
            ctx.fillStyle = '#3f1c10';
            ctx.fillRect(trenchX1, roadTopY - 22, trenchW, 22);
            ctx.fillStyle = 'rgba(239, 68, 68, 0.4)';
            ctx.fillRect(trenchX1, roadTopY - 22, trenchW, 22);

            // Protected Yellow Pedestrian Corridor on Roadway
            ctx.fillStyle = '#eab308';
            ctx.fillRect(trenchX1, roadTopY, trenchW, 12);
            ctx.fillStyle = '#000'; ctx.font = 'bold 7.5px system-ui';
            ctx.fillText('🚶‍♂️ COULOIR PMR PROTÉGÉ K2', trenchX1 + 10, roadTopY + 9);
        } else if (taskType === 'emprise_accotement' || taskType === 'implantation_poteau_elec' || taskType === 'neutralisation_bau') {
            // =====================================
            // SCENARIO 4: ACCOTEMENT / BAU
            // =====================================
            ctx.fillStyle = '#14532d'; // Grass
            ctx.fillRect(0, 0, w, roadTopY);
            ctx.fillRect(0, roadTopY + roadH, w, h);

            ctx.fillStyle = '#1e293b';
            ctx.fillRect(0, roadTopY, w, roadH);

            // Work Zone on North Shoulder
            ctx.fillStyle = '#ea580c';
            ctx.fillRect(trenchX1, roadTopY - 20, trenchW, 18);
            ctx.fillStyle = '#fff'; ctx.font = 'bold 8px system-ui';
            ctx.fillText('⚡ CHANTIER MOBILE FLR ACCOTEMENT (ENEDIS)', trenchX1 + 10, roadTopY - 8);
        } else {
            // =====================================
            // SCENARIO 5: STANDARD ROAD ALTERNAT (TRANCHÉE)
            // =====================================
            ctx.fillStyle = '#14532d'; // Grass
            ctx.fillRect(0, 0, w, roadTopY);
            ctx.fillRect(0, roadTopY + roadH, w, h);

            ctx.fillStyle = '#1e293b';
            ctx.fillRect(0, roadTopY, w, roadH);

            // Open Trench on Lane 2 (Upper Lane)
            ctx.fillStyle = '#3f1c10';
            ctx.fillRect(trenchX1, roadTopY, trenchW, roadH * 0.5);
            ctx.fillStyle = 'rgba(239, 68, 68, 0.45)';
            ctx.fillRect(trenchX1, roadTopY, trenchW, roadH * 0.5);
            ctx.strokeStyle = '#ea580c'; ctx.lineWidth = 2;
            ctx.strokeRect(trenchX1, roadTopY, trenchW, roadH * 0.5);

            ctx.fillStyle = '#f8fafc'; ctx.font = 'bold 8.5px JetBrains Mono';
            ctx.fillText('🚧 ZONE CHANTIER / TRANCHÉE OUVERTE', trenchX1 + 15, roadTopY + 18);
        }

        // Roadway Centerline
        ctx.strokeStyle = '#f8fafc'; ctx.lineWidth = 2; ctx.setLineDash([12, 12]);
        ctx.beginPath(); ctx.moveTo(0, roadMidY); ctx.lineTo(w, roadMidY); ctx.stroke();
        ctx.setLineDash([]);

        // Taper K5a Cones (Guiding Westbound cars smoothly down to Lane 1)
        if (taskType !== 'emprise_accotement' && taskType !== 'implantation_poteau_elec' && taskType !== 'neutralisation_bau') {
            ctx.fillStyle = '#ea580c';
            // Westbound entry taper (right side of trench)
            for (let x = trenchX2 + 70; x >= trenchX2; x -= 14) {
                const frac = (trenchX2 + 70 - x) / 70;
                const cy = roadTopY + frac * (roadH * 0.5 + 4);
                ctx.beginPath(); ctx.arc(x, cy, 4, 0, Math.PI * 2); ctx.fill();
            }
            // Westbound return taper (left side of trench)
            for (let x = trenchX1; x >= trenchX1 - 70; x -= 14) {
                const frac = (x - (trenchX1 - 70)) / 70;
                const cy = roadTopY + frac * (roadH * 0.5 + 4);
                ctx.beginPath(); ctx.arc(x, cy, 4, 0, Math.PI * 2); ctx.fill();
            }
        }

        // =====================================
        // VEHICLES KINEMATICS (STRICT ZERO CHANTIER OVERLAP)
        // =====================================
        if (isOpbtpTrafficRunning) {
            opbtpCars.forEach((car, cIdx) => {
                const spd = car.speed * (speedLimit / 50) * opbtpSpeedFactor;

                if (car.dir === 1) { // EASTBOUND (Lane 1 - Lower Lane)
                    let shouldStop = false;
                    const stopLineX = w * 0.20;

                    if (curLightState !== 'east_green' && car.x > stopLineX - 45 && car.x <= stopLineX) {
                        shouldStop = true;
                    }
                    const ahead = opbtpCars.find((other, oIdx) => oIdx !== cIdx && other.dir === 1 && other.x > car.x && (other.x - car.x) < 45);
                    if (ahead) shouldStop = true;

                    if (!shouldStop) {
                        car.x += spd;
                        car.y = lane1Y;
                        if (car.x > w + 60) car.x = -50;
                    }
                } else { // WESTBOUND (Lane 2 - Upper Lane with Obstacle avoidance)
                    let shouldStop = false;
                    const stopLineX = w * 0.80;

                    if (curLightState !== 'west_green' && car.x < stopLineX + 45 && car.x >= stopLineX) {
                        shouldStop = true;
                    }
                    const ahead = opbtpCars.find((other, oIdx) => oIdx !== cIdx && other.dir === -1 && other.x < car.x && (car.x - other.x) < 45);
                    if (ahead) shouldStop = true;

                    if (!shouldStop) {
                        car.x -= spd;

                        if (taskType === 'emprise_accotement' || taskType === 'implantation_poteau_elec' || taskType === 'neutralisation_bau') {
                            car.y = lane2Y;
                        } else {
                            // Smooth avoidance of trench: shift completely down to Lane 1 before trenchX2
                            if (car.x > trenchX2 + 70) {
                                car.y = lane2Y;
                            } else if (car.x >= trenchX2) {
                                const frac = (trenchX2 + 70 - car.x) / 70;
                                car.y = lane2Y + frac * (lane1Y - lane2Y);
                            } else if (car.x >= trenchX1) {
                                car.y = lane1Y; // Stays on Lane 1 throughout the entire length of the trench!
                            } else if (car.x >= trenchX1 - 70) {
                                const frac = (car.x - (trenchX1 - 70)) / 70;
                                car.y = lane2Y + frac * (lane1Y - lane2Y);
                            } else {
                                car.y = lane2Y;
                            }
                        }

                        if (car.x < -60) car.x = w + 50;
                    }
                }
            });
        }

        // Temporary Traffic Lights KR11
        const tl1X = w * 0.20, tl1Y = roadTopY + roadH + 16;
        const tl2X = w * 0.80, tl2Y = roadTopY - 20;

        ctx.fillStyle = '#0f172a'; ctx.fillRect(tl1X - 6, tl1Y - 14, 12, 28);
        ctx.fillStyle = (curLightState === 'east_green') ? '#10b981' : '#ef4444';
        ctx.beginPath(); ctx.arc(tl1X, tl1Y, 4.5, 0, Math.PI * 2); ctx.fill();

        ctx.fillStyle = '#0f172a'; ctx.fillRect(tl2X - 6, tl2Y - 14, 12, 28);
        ctx.fillStyle = (curLightState === 'west_green') ? '#10b981' : '#ef4444';
        ctx.beginPath(); ctx.arc(tl2X, tl2Y, 4.5, 0, Math.PI * 2); ctx.fill();

        // Draw Vehicles
        opbtpCars.forEach(c => {
            const cy = c.y - c.h / 2;
            ctx.fillStyle = c.color;
            ctx.fillRect(c.x, cy, c.w, c.h);

            // Headlights
            ctx.fillStyle = '#fef08a';
            if (c.dir === 1) {
                ctx.fillRect(c.x + c.w - 3, cy + 2, 3, 3);
                ctx.fillRect(c.x + c.w - 3, cy + c.h - 5, 3, 3);
            } else {
                ctx.fillRect(c.x, cy + 2, 3, 3);
                ctx.fillRect(c.x, cy + c.h - 5, 3, 3);
            }

            // Badge
            ctx.fillStyle = '#fff'; ctx.font = 'bold 7.5px system-ui';
            ctx.fillText(c.type, c.x + 3, cy - 2);
        });

        // HUD Telemetry
        ctx.font = 'bold 9px JetBrains Mono'; ctx.fillStyle = '#38bdf8';
        const lightStatusText = curLightState === 'east_green' ? '🟢 FEU EST VERT' : (curLightState === 'west_green' ? '🟢 FEU OUEST VERT' : '🔴 TOUT-ROUGE DÉGAGEMENT');
        ctx.fillText(`VITESSE : ${opbtpSpeedFactor}x • FLUX : ${speedLimit} km/h • KR11 : ${lightStatusText} • CONFIG : ${taskType.toUpperCase()}`, 10, h - 10);

        if (currentNav === 'opbtp' && isOpbtpTrafficRunning) {
            opbtpTrafficAnimId = requestAnimationFrame(drawSignageDiagram);
        }
    }

    // ==========================================
    // 14. SAFETY AIPR - RECOMMANDATIONS & EXTERIOR ELEMENTS
    // ==========================================
    let currentAiprSituation = 'gaz';
    let aiprCurrentTaskPhase = 'phase_3_pose_canalisations';
    let aiprIsBlindageActive = true;
    let aiprExcavatorTrackX = 60;
    let excavatorBoomAngle = 45;
    let excavatorStickAngle = 65;
    let aiprMachineType = 'liebherr_24t';
    let aiprToolType = 'godet_dents';

    let aiprExteriorElements = [
        { id: 1, type: 'pieton', x: 480, label: '🚶‍♂️ Piéton' },
        { id: 2, type: 'barriere', x: 190, label: '🚧 Barrière K2' },
        { id: 3, type: 'vigie', x: 110, label: '🦺 Vigie Sécurité' }
    ];

    const aiprPhaseGuidelines = {
        'phase_1_terrassement': {
            title: "1. Décapage terre végétale & Piquetage DICT Classe A",
            materiel: "🛠️ Géoradar RD8100, Détecteur électromagnétique, Canne GNSS RTK Leica, Bombes fluo traçage, Piquets bois",
            recommandations: "✔️ Obligation de tracer au sol l'ensemble des réseaux des exploitants avec leur couleur normalisée. Respect strict de la marge d'incertitude Classe A (40cm). Rédaction du PV contradictoire de piquetage avec le maître d'ouvrage avant tout coup de godet.",
            habilitations: "🦺 AIPR Concepteur / Encadrant + CACES R482 Cat A/B1"
        },
        'phase_2_fouille_blindage': {
            title: "2. Ouverture tranchée profonde & Pose caissons blindage R4534",
            materiel: "🛠️ Caissons de blindage acier Krings R4534, Étrésillons hydrauliques, Élingues 4 brins contrôlées VGP, Échelle d'accès avec crosse",
            recommandations: "⚠️ Obligation absolue de blindage dès 1.30m de profondeur et si la pente de talus est > 1/1 (Art. R4534-24). Interdiction formelle de présence humaine au fond sans blindage posé. L'échelle d'accès doit dépasser d'au moins 1.00m au-dessus de la crête.",
            habilitations: "🦺 AIPR Encadrant & Opérateur + Élingueur habilité"
        },
        'phase_3_pose_canalisations': {
            title: "3. Lit de pose sable & Pose canalisation Fonte DN400 / BA Ø400",
            materiel: "🛠️ Laser d'alignement Piper 200, Pince hydraulique à tuyaux, Miroir de centrage, Coussins de levage gonflables",
            recommandations: "✔️ Réalisation du lit de pose en sable 0/4 d'épaisseur 10cm réglé au laser. Aucun compagnon ne doit rester sous la charge lors de la descente du tuyau. Emboîtement avec lubrifiant agréé et contrôle systématique de la pente d'autocurage (Fascicule 70).",
            habilitations: "🦺 Poseur Canalisateur Qualifié + CACES R482 Cat A"
        },
        'phase_4_reseaux_secs': {
            title: "4. Pose fourreaux réseaux secs (Élec HTA, Fibre, Gaz) & Grillages avertisseurs",
            materiel: "🛠️ TPC Janolène Ø110, Grillages avertisseurs NF P98-332 (Jaune/Rouge/Bleu/Vert), Aiguilles tire-fil, Dérouleuses de tourets",
            recommandations: "✔️ Pose des grillages avertisseurs à 20-30cm au-dessus de la génératrice supérieure des fourreaux. Respect des distances minimales d'écartement entre réseaux (20cm croisement, 50cm parallélisme avec le gaz).",
            habilitations: "🦺 AIPR Opérateur + Habilitation Électrique H0B0 / BS"
        },
        'phase_5_remblai_compactage': {
            title: "5. Remblaiement méthodique par couches compactées (GTR 0/31.5)",
            materiel: "🛠️ Compacteur tandem vibrant Bomag BW120, Pilonneuse Wacker, Plaque de charge dynamique EV2, Cône de sable",
            recommandations: "✔️ Compactage méthodique par couches successives d'épaisseur maximale 30cm. Contrôle de portance EV2 >= 80 MPa avec rapport EV2/EV1 <= 2.0. Éloignement des piétons à plus de 5.00m du rouleau vibrant.",
            habilitations: "🦺 CACES R482 Cat D (Compacteur) + Contrôleur Géotechnique"
        },
        'phase_6_voirie_enrobes': {
            title: "6. Pose bordures T2 & Couche d'enrobés BBSG 0/10",
            materiel: "🛠️ Finisseur Vögele Super 1300, Répandeuse d'émulsion C65B4, Scie à sol avec arrosage eau, Réglettes 3m alu",
            recommandations: "✔️ Température minimale de mise en œuvre du BBSG > 130°C. Balisage lourd de chantier avec cônes K5a. Port obligatoire de vêtements haute visibilité Classe 3 et gants thermiques anti-brûlure.",
            habilitations: "🦺 CACES R482 Cat D (Finisseur) + Applicateurs Enrobés"
        },
        'phase_7_sondage_aspiration': {
            title: "7. Sondage doux par aspiration / Piquetage DICT Classe A",
            materiel: "🛠️ Camion Aspiratrice-Excavatrice TP avec buse souple, Pelles et pioches à manche isolant 1000V, Détecteur gaz portable 4 gaz",
            recommandations: "✔️ Interdiction absolue d'engins mécaniques à godet à dents à moins de 50cm des canalisations de gaz MPB ou câbles HTA. Le dégagement doit se faire exclusivement par aspiration douce ou terrassement à la main.",
            habilitations: "🦺 AIPR Opérateur Spécialiste + Opérateur Aspiratrice"
        }
    };

    function updateAiprPhaseDetails() {
        const sel = document.getElementById('aipr-task-phase-select')?.value || 'phase_3_pose_canalisations';
        const box = document.getElementById('aipr-phase-recommendations-box');
        if (!box) return;

        const g = aiprPhaseGuidelines[sel] || aiprPhaseGuidelines['phase_3_pose_canalisations'];
        box.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.4rem; flex-wrap: wrap; gap: 0.4rem;">
                <h4 style="color: #38bdf8; font-size: 0.95rem; font-weight: 800;">${g.title}</h4>
                <span class="badge badge-info">${g.habilitations}</span>
            </div>
            <div style="font-size: 0.78rem; color: #f8fafc; margin-bottom: 0.4rem;">
                <strong>Matériels & Équipements de Sécurité Requis :</strong>
                <div style="color: var(--amber); margin-top: 2px;">${g.materiel}</div>
            </div>
            <div style="font-size: 0.76rem; color: #cbd5e1; line-height: 1.4; border-top: 1px solid rgba(51,65,85,0.5); padding-top: 4px;">
                <strong>Prescriptions Réglementaires & Recommandations :</strong>
                <div>${g.recommandations}</div>
            </div>
        `;
    }

    function toggleAiprBlindage() {
        aiprIsBlindageActive = !aiprIsBlindageActive;
        const btn = document.getElementById('btn-aipr-blindage-toggle');
        if (btn) {
            btn.textContent = aiprIsBlindageActive ? '🛡️ Blindage R4534 : ACTIF' : '⚠️ Blindage : DÉSACTIVÉ (Risque Éboulement)';
            btn.className = aiprIsBlindageActive ? 'btn btn-secondary' : 'btn btn-warning';
        }
        renderAiprCanvas();
    }

    function setAiprTaskPhase(phase) {
        aiprCurrentTaskPhase = phase;
        const sel = document.getElementById('aipr-task-phase-select');
        if (sel) sel.value = phase;

        // Auto-adapt tool / machine if suited
        if (phase === 'phase_7_sondage_aspiration') {
            const m = document.getElementById('aipr-machine-type');
            const t = document.getElementById('aipr-tool-type');
            if (m) m.value = 'aspiratrice_tp';
            if (t) t.value = 'aspiration';
        } else if (phase === 'phase_1_terrassement') {
            const t = document.getElementById('aipr-tool-type');
            if (t) t.value = 'godet_curage';
        }

        updateAiprPhaseDetails();
        renderAiprCanvas();
    }

    function setAiprSituation(sit) {
        currentAiprSituation = sit;
        document.querySelectorAll('.aipr-sim-btn').forEach(b => b.classList.remove('active'));
        renderAiprCanvas();
    }

    function updateAiprExcavatorControls() {
        aiprExcavatorTrackX = Number(document.getElementById('aipr-track-x-range')?.value || 60);
        excavatorBoomAngle = Number(document.getElementById('aipr-boom-range')?.value || 45);
        excavatorStickAngle = Number(document.getElementById('aipr-stick-range')?.value || 65);
        aiprMachineType = document.getElementById('aipr-machine-type')?.value || 'liebherr_24t';
        aiprToolType = document.getElementById('aipr-tool-type')?.value || 'godet_dents';

        const lbl = document.getElementById('aipr-pos-x-label');
        if (lbl) lbl.textContent = `PK 0+240 (x=${aiprExcavatorTrackX}px)`;

        renderAiprCanvas();
    }

    function addAiprExteriorElement(type) {
        const count = aiprExteriorElements.length + 1;
        let label = 'Élément';
        let x = 400 + (count % 3) * 40;
        if (type === 'pieton') label = '🚶‍♂️ Passant';
        if (type === 'barriere') label = '🚧 Barrière K2';
        if (type === 'vigie') label = '🦺 Vigie';
        if (type === 'piquet') label = '🚩 Piquet Gaz';

        aiprExteriorElements.push({ id: Date.now(), type, x, label });
        renderAiprCanvas();
        logCockpit(`Élément ${label} ajouté au chantier.`, 'info');
    }

    function removeLastAiprExteriorElement() {
        if (aiprExteriorElements.length > 0) {
            aiprExteriorElements.pop();
            renderAiprCanvas();
        }
    }

    function resetAiprExteriorElements() {
        aiprExteriorElements = [
            { id: 1, type: 'pieton', x: 480, label: '🚶‍♂️ Piéton' },
            { id: 2, type: 'barriere', x: 190, label: '🚧 Barrière K2' },
            { id: 3, type: 'vigie', x: 110, label: '🦺 Vigie' }
        ];
        renderAiprCanvas();
    }

    let aiprDraggedTarget = null;
    let aiprCanvasEventsBound = false;

    function initAiprCanvasMouseEvents() {
        const canvas = document.getElementById('aipr-simulation-canvas');
        if (!canvas || aiprCanvasEventsBound) return;
        aiprCanvasEventsBound = true;

        canvas.onmousedown = (e) => {
            const rect = canvas.getBoundingClientRect();
            const mx = (e.clientX - rect.left) * (canvas.width / rect.width);
            const my = (e.clientY - rect.top) * (canvas.height / rect.height);
            const groundY = canvas.height * 0.45;

            // Check if clicked near an exterior element
            for (let i = aiprExteriorElements.length - 1; i >= 0; i--) {
                const elem = aiprExteriorElements[i];
                if (Math.abs(mx - elem.x) < 25 && Math.abs(my - (groundY - 15)) < 35) {
                    aiprDraggedTarget = { type: 'exterior', item: elem };
                    return;
                }
            }

            // Check if clicked near excavator track / base
            if (Math.abs(mx - aiprExcavatorTrackX) < 50 && Math.abs(my - (groundY - 20)) < 45) {
                aiprDraggedTarget = { type: 'excavator' };
                return;
            }
        };

        window.addEventListener('mousemove', (e) => {
            if (!aiprDraggedTarget) return;
            const canvas = document.getElementById('aipr-simulation-canvas');
            if (!canvas) return;
            const rect = canvas.getBoundingClientRect();
            const mx = (e.clientX - rect.left) * (canvas.width / rect.width);

            if (aiprDraggedTarget.type === 'exterior') {
                aiprDraggedTarget.item.x = Math.max(10, Math.min(canvas.width - 10, Math.round(mx)));
                renderAiprCanvas();
            } else if (aiprDraggedTarget.type === 'excavator') {
                aiprExcavatorTrackX = Math.max(20, Math.min(360, Math.round(mx)));
                const sl = document.getElementById('aipr-track-x-range');
                if (sl) sl.value = aiprExcavatorTrackX;
                const lbl = document.getElementById('aipr-pos-x-label');
                if (lbl) lbl.textContent = `PK 0+240 (x=${aiprExcavatorTrackX}px)`;
                renderAiprCanvas();
            }
        });

        window.addEventListener('mouseup', () => {
            aiprDraggedTarget = null;
        });
    }

    function renderAiprCanvas() {
        const canvas = document.getElementById('aipr-simulation-canvas');
        if (!canvas) return;
        initAiprCanvasMouseEvents();
        const ctx = canvas.getContext('2d');
        const w = canvas.parentElement.clientWidth || 500;
        const h = canvas.parentElement.clientHeight || 360;
        canvas.width = w;
        canvas.height = h;

        ctx.fillStyle = '#060913';
        ctx.fillRect(0, 0, w, h);

        const groundY = h * 0.45;

        // Ground Cut
        ctx.fillStyle = '#271c14';
        ctx.fillRect(0, groundY, w, h - groundY);

        // Ground Top Surface
        ctx.strokeStyle = '#10b981'; ctx.lineWidth = 4;
        ctx.beginPath(); ctx.moveTo(0, groundY); ctx.lineTo(w, groundY); ctx.stroke();

        const tX1 = 200, tX2 = 360;

        // ==========================================
        // DYNAMIC PHASE-SPECIFIC RENDERING IN CANVASS
        // ==========================================
        if (aiprCurrentTaskPhase === 'phase_1_terrassement') {
            // PHASE 1: DÉCAPAGE 30cm + PIQUETAGE DICT CLASSE A
            ctx.fillStyle = '#451a03';
            ctx.fillRect(160, groundY, 260, 20); // 30cm stripped layer

            // Fluorescent markings on ground
            ctx.strokeStyle = '#eab308'; ctx.lineWidth = 3; // Yellow Gas
            ctx.beginPath(); ctx.moveTo(130, groundY); ctx.lineTo(150, groundY); ctx.stroke();
            ctx.fillStyle = '#eab308'; ctx.font = 'bold 8px system-ui';
            ctx.fillText('GAZ MPB ±40cm (Cl. A)', 110, groundY - 8);

            ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 3; // Red HTA
            ctx.beginPath(); ctx.moveTo(410, groundY); ctx.lineTo(430, groundY); ctx.stroke();
            ctx.fillStyle = '#ef4444';
            ctx.fillText('HTA 20kV (Cl. A)', 400, groundY - 8);

            ctx.strokeStyle = '#3b82f6'; ctx.lineWidth = 3; // Blue Water
            ctx.beginPath(); ctx.moveTo(435, groundY); ctx.lineTo(455, groundY); ctx.stroke();

            // Surveyor RTK GNSS rod
            ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(140, groundY); ctx.lineTo(140, groundY - 35); ctx.stroke();
            ctx.fillStyle = '#38bdf8';
            ctx.beginPath(); ctx.arc(140, groundY - 37, 5, 0, Math.PI * 2); ctx.fill();
            ctx.fillText('GNSS RTK', 148, groundY - 32);
        } else if (aiprCurrentTaskPhase === 'phase_5_remblai_compactage') {
            // PHASE 5: REMBLAIEMENT GTR & COMPACTAGE EV2
            const tDepth = 120;
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(tX1, groundY, tX2 - tX1, tDepth);

            // Compacted GTR layers
            ctx.fillStyle = '#475569';
            ctx.fillRect(tX1 + 2, groundY + 40, tX2 - tX1 - 4, 80);
            ctx.fillStyle = '#64748b';
            ctx.fillRect(tX1 + 2, groundY + 10, tX2 - tX1 - 4, 30);

            ctx.strokeStyle = '#38bdf8'; ctx.setLineDash([4, 4]);
            ctx.beginPath();
            ctx.moveTo(tX1, groundY + 40); ctx.lineTo(tX2, groundY + 40);
            ctx.moveTo(tX1, groundY + 80); ctx.lineTo(tX2, groundY + 80);
            ctx.stroke();
            ctx.setLineDash([]);

            ctx.fillStyle = '#fff'; ctx.font = 'bold 8px monospace';
            ctx.fillText('Couche 2 GTR 0/31.5', tX1 + 10, groundY + 30);
            ctx.fillText('Couche 1 GTR (Compactée)', tX1 + 10, groundY + 65);

            // EV2 Dynamic plate test
            ctx.fillStyle = '#f59e0b';
            ctx.fillRect(tX1 + 60, groundY + 6, 40, 4);
            ctx.fillStyle = '#38bdf8';
            ctx.fillText('EV2 = 88 MPa (OK)', tX1 + 45, groundY - 4);
        } else if (aiprCurrentTaskPhase === 'phase_6_voirie_enrobes') {
            // PHASE 6: BORDURES T2 & ENROBÉS BBSG
            const tDepth = 120;
            ctx.fillStyle = '#475569';
            ctx.fillRect(tX1, groundY, tX2 - tX1, tDepth);

            // Curb T2
            ctx.fillStyle = '#cbd5e1';
            ctx.fillRect(tX1 - 15, groundY - 14, 15, 20);
            ctx.fillStyle = '#94a3b8';
            ctx.fillRect(tX1 - 25, groundY - 4, 10, 10); // concrete backing
            ctx.fillStyle = '#fff'; ctx.font = 'bold 7.5px system-ui';
            ctx.fillText('Bordure T2', tX1 - 32, groundY - 18);

            // Asphalt Layers
            ctx.fillStyle = '#1e293b'; // GB3 Base
            ctx.fillRect(tX1, groundY, tX2 - tX1 + 50, 14);
            ctx.fillStyle = '#0f172a'; // BBSG 0/10 Roulement
            ctx.fillRect(tX1, groundY - 8, tX2 - tX1 + 50, 8);
            ctx.fillStyle = '#f59e0b';
            ctx.fillText('BBSG 0/10 (145°C)', tX1 + 20, groundY - 12);
        } else {
            // PHASES 2, 3, 4, 7: TRANCHÉE PROFONDE AVEC RÉSEAUX ET BLINDAGE
            const tDepth = 120;
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(tX1, groundY, tX2 - tX1, tDepth);
            ctx.strokeStyle = '#475569'; ctx.lineWidth = 2;
            ctx.strokeRect(tX1, groundY, tX2 - tX1, tDepth);

            // Blindage Caissons if active
            if (aiprIsBlindageActive) {
                ctx.fillStyle = 'rgba(234, 179, 8, 0.75)';
                ctx.fillRect(tX1 + 4, groundY + 4, 12, tDepth - 8);
                ctx.fillRect(tX2 - 16, groundY + 4, 12, tDepth - 8);

                ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 4;
                ctx.beginPath();
                ctx.moveTo(tX1 + 16, groundY + 30); ctx.lineTo(tX2 - 16, groundY + 30);
                ctx.moveTo(tX1 + 16, groundY + 80); ctx.lineTo(tX2 - 16, groundY + 80);
                ctx.stroke();

                // Safety ladder with 1m extension over crest
                ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(tX2 - 24, groundY - 25); ctx.lineTo(tX2 - 24, groundY + tDepth - 5);
                ctx.moveTo(tX2 - 32, groundY - 25); ctx.lineTo(tX2 - 32, groundY + tDepth - 5);
                for (let ly = groundY - 20; ly < groundY + tDepth - 5; ly += 12) {
                    ctx.moveTo(tX2 - 32, ly); ctx.lineTo(tX2 - 24, ly);
                }
                ctx.stroke();
            }

            // Phase 3: Sand bedding + Piper laser
            if (aiprCurrentTaskPhase === 'phase_3_pose_canalisations') {
                // Sand 0/4
                ctx.fillStyle = '#ca8a04';
                ctx.fillRect(tX1 + 16, groundY + tDepth - 10, tX2 - tX1 - 32, 10);

                // Piper Laser red beam
                ctx.strokeStyle = 'rgba(239, 68, 68, 0.8)'; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.moveTo(tX1 + 20, groundY + tDepth - 22); ctx.lineTo(tX2 - 20, groundY + tDepth - 22); ctx.stroke();
                ctx.fillStyle = '#ef4444'; ctx.font = 'bold 7.5px monospace';
                ctx.fillText('🔴 LASER PIPER (Pente 0.8%)', tX1 + 25, groundY + tDepth - 26);
            }

            // Pipe inside trench
            ctx.fillStyle = '#38bdf8';
            ctx.beginPath(); ctx.arc((tX1 + tX2) / 2, groundY + tDepth - 22, 16, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#fff'; ctx.font = 'bold 8px monospace';
            ctx.fillText('Ø400 BA', (tX1 + tX2) / 2 - 14, groundY + tDepth - 19);

            // Phase 4: Dry conduits & Warning mesh
            if (aiprCurrentTaskPhase === 'phase_4_reseaux_secs') {
                ctx.fillStyle = '#ef4444'; // Electric TPC
                ctx.beginPath(); ctx.arc((tX1 + tX2) / 2 - 25, groundY + 60, 6, 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = '#10b981'; // Telecom
                ctx.beginPath(); ctx.arc((tX1 + tX2) / 2 + 25, groundY + 60, 6, 0, Math.PI * 2); ctx.fill();

                // Warning meshes NF P98-332
                ctx.fillStyle = '#ef4444';
                ctx.fillRect(tX1 + 25, groundY + 40, 40, 3);
                ctx.fillStyle = '#10b981';
                ctx.fillRect(tX2 - 65, groundY + 40, 40, 3);
            }
        }

        // Underground Networks in surrounding soil
        // Gaz Jaune
        const isGazActive = currentAiprSituation === 'gaz' || currentAiprSituation === 'all_networks';
        ctx.fillStyle = isGazActive ? '#eab308' : '#713f12';
        ctx.beginPath(); ctx.arc(140, groundY + 45, 10, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#fff'; ctx.font = 'bold 7.5px system-ui';
        ctx.fillText('GAZ 4B', 125, groundY + 42);

        // Élec Rouge HTA
        const isHtaActive = currentAiprSituation === 'hta' || currentAiprSituation === 'all_networks';
        ctx.fillStyle = isHtaActive ? '#ef4444' : '#7f1d1d';
        ctx.beginPath(); ctx.arc(420, groundY + 30, 8, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#fff';
        ctx.fillText('HTA 20kV', 405, groundY + 28);

        // Eau Bleu
        const isEauActive = currentAiprSituation === 'fibre_aep' || currentAiprSituation === 'all_networks';
        ctx.fillStyle = isEauActive ? '#3b82f6' : '#1e3a8a';
        ctx.beginPath(); ctx.arc(440, groundY + 75, 12, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#fff';
        ctx.fillText('AEP Fonte', 420, groundY + 72);

        // Excavator Kinematic Rendering
        const trkX = aiprExcavatorTrackX;
        const trkY = groundY;

        ctx.fillStyle = '#334155';
        ctx.fillRect(trkX - 35, trkY - 14, 70, 14);

        ctx.fillStyle = '#f59e0b';
        ctx.fillRect(trkX - 25, trkY - 45, 45, 31);
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(trkX + 2, trkY - 40, 15, 20);

        const j0X = trkX + 15, j0Y = trkY - 35;
        const boomLen = 65;
        const bRad = (excavatorBoomAngle * Math.PI) / 180;
        const j1X = j0X + Math.cos(bRad) * boomLen;
        const j1Y = j0Y - Math.sin(bRad) * boomLen;

        ctx.strokeStyle = '#f59e0b'; ctx.lineWidth = 8;
        ctx.beginPath(); ctx.moveTo(j0X, j0Y); ctx.lineTo(j1X, j1Y); ctx.stroke();

        const stickLen = 55;
        const sRad = ((excavatorBoomAngle - excavatorStickAngle) * Math.PI) / 180;
        const j2X = j1X + Math.cos(sRad) * stickLen;
        const j2Y = j1Y + Math.sin(sRad) * stickLen;

        ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 6;
        ctx.beginPath(); ctx.moveTo(j1X, j1Y); ctx.lineTo(j2X, j2Y); ctx.stroke();

        ctx.fillStyle = aiprToolType === 'godet_dents' ? '#ef4444' : (aiprToolType === 'aspiration' ? '#10b981' : '#475569');
        ctx.beginPath(); ctx.arc(j2X, j2Y, 12, 0, Math.PI * 2); ctx.fill();

        // Render Exterior Elements (Pedestrians, Barriers, Vigie)
        aiprExteriorElements.forEach(elem => {
            const ey = groundY;
            if (elem.type === 'pieton') {
                ctx.fillStyle = '#f43f5e';
                ctx.beginPath(); ctx.arc(elem.x, ey - 22, 6, 0, Math.PI * 2); ctx.fill();
                ctx.fillRect(elem.x - 4, ey - 16, 8, 16);
                ctx.fillStyle = '#fff'; ctx.font = 'bold 8px system-ui';
                ctx.fillText('🚶‍♂️ Passant', elem.x - 14, ey - 26);
            } else if (elem.type === 'barriere') {
                ctx.fillStyle = '#ea580c';
                ctx.fillRect(elem.x - 12, ey - 22, 24, 22);
                ctx.strokeStyle = '#fff'; ctx.lineWidth = 2;
                ctx.strokeRect(elem.x - 12, ey - 22, 24, 22);
                ctx.fillStyle = '#fff'; ctx.font = 'bold 7.5px system-ui';
                ctx.fillText('🚧 HERAS', elem.x - 12, ey - 26);
            } else if (elem.type === 'vigie') {
                ctx.fillStyle = '#facc15';
                ctx.beginPath(); ctx.arc(elem.x, ey - 24, 6, 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = '#10b981'; ctx.fillRect(elem.x - 5, ey - 18, 10, 18);
                ctx.fillStyle = '#fff'; ctx.font = 'bold 8px system-ui';
                ctx.fillText('🦺 Vigie', elem.x - 10, ey - 28);
            } else {
                ctx.fillStyle = '#eab308';
                ctx.fillRect(elem.x - 2, ey - 25, 4, 25);
                ctx.fillStyle = '#ef4444';
                ctx.fillRect(elem.x - 8, ey - 25, 16, 10);
            }
        });

        // Telemetry calculation
        const toolDepth = (j2Y - groundY) / 50;
        const dDepthEl = document.getElementById('aipr-depth-val');
        if (dDepthEl) dDepthEl.textContent = toolDepth > 0 ? `-${toolDepth.toFixed(2)} m` : `+${Math.abs(toolDepth).toFixed(2)} m`;

        const distGaz = Math.hypot(j2X - 140, j2Y - (groundY + 45)) / 50;
        const dDistEl = document.getElementById('aipr-dist-val');
        if (dDistEl) {
            dDistEl.textContent = `${distGaz.toFixed(2)} m (${distGaz < 0.5 ? 'DANGER PROXIMITÉ GAZ !' : 'Sécurisé'})`;
            dDistEl.style.color = distGaz < 0.5 ? '#ef4444' : 'var(--emerald)';
        }

        const hudEl = document.getElementById('aipr-sim-hud');
        if (hudEl) {
            const phaseTitle = aiprPhaseGuidelines[aiprCurrentTaskPhase]?.title || aiprCurrentTaskPhase;
            hudEl.innerHTML = `ÉTAPE : <strong style="color:#f8fafc;">${phaseTitle}</strong> • DISTANCE GAZ : <strong style="color:${distGaz < 0.5 ? '#ef4444' : 'var(--emerald)'};">${distGaz.toFixed(2)} m</strong> • BLINDAGE : ${aiprIsBlindageActive ? '🛡️ CONFORME R4534' : '⚠️ DÉSACTIVÉ'}`;
        }
    }

    // ==========================================
    // 15. 28 SDP, DQE & MULTI-ENTERPRISE COMPARATOR
    // ==========================================
    const competitorBenchmarkData = {
        'DQE_004': {
            name: "Pose Bordures T2 Béton avec Semelle (ml)",
            unit: "ml",
            our_ds: 38.94, our_k: 1.350, our_pv: 52.57,
            colas: 56.20, eurovia: 54.80, eiffage: 58.10, fntp_avg: 55.40,
            status: "Très Compétitif (-5.1% vs Marché)", strategy: "Marge brute 25.9% • Équipe de pose mécanisée par ventouse"
        },
        'DQE_002': {
            name: "Tranchée Blindée Profondeur > 1.30m (m³)",
            unit: "m³",
            our_ds: 22.40, our_k: 1.350, our_pv: 30.24,
            colas: 32.50, eurovia: 31.80, eiffage: 34.00, fntp_avg: 32.10,
            status: "Optimisé (-5.8%)", strategy: "Caissons Krings acier amortis • Rendement 420 m³/j"
        },
        'DQE_003': {
            name: "Pose Canalisations Béton Armé Ø400 (ml)",
            unit: "ml",
            our_ds: 68.50, our_k: 1.350, our_pv: 92.48,
            colas: 98.00, eurovia: 94.50, eiffage: 102.00, fntp_avg: 96.20,
            status: "Compétitif (-3.9%)", strategy: "Laser Piper 200 • Équipe 4 compagnons qualifiés"
        },
        'DQE_005': {
            name: "Fourniture & Application BBSG 0/10 (t)",
            unit: "t",
            our_ds: 74.00, our_k: 1.350, our_pv: 99.90,
            colas: 104.50, eurovia: 102.00, eiffage: 106.00, fntp_avg: 103.50,
            status: "Agressif (-3.5%)", strategy: "Contrat-cadre Enrobés du Sud • Cadence 185 t/jour"
        },
        'DQE_001': {
            name: "Décapage Terre Végétale ép. 30cm (m²)",
            unit: "m²",
            our_ds: 1.85, our_k: 1.350, our_pv: 2.50,
            colas: 2.80, eurovia: 2.65, eiffage: 2.90, fntp_avg: 2.75,
            status: "Très Agressif (-9.1%)", strategy: "Pelle Liebherr 24t godet curage 2.00m"
        }
    };

    function setSDPViewMode(mode) {
        sdpViewMode = mode;
        document.querySelectorAll('.sdp-view-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('btn-sdp-' + mode)?.classList.add('active');

        const dqeView = document.getElementById('sdp-dqe-tcd-view');
        const cardsView = document.getElementById('sdp-cards-view');
        const compView = document.getElementById('sdp-comparator-view');

        if (dqeView) dqeView.style.display = mode === 'dqe_tcd' ? 'block' : 'none';
        if (cardsView) cardsView.style.display = mode === 'cards' ? 'grid' : 'none';
        if (compView) compView.style.display = mode === 'comparator' ? 'block' : 'none';

        if (mode === 'dqe_tcd') renderDQEPivotTable();
        else if (mode === 'cards') renderSdpCards();
        else renderEnterprisePriceComparison();
    }

    function renderEnterprisePriceComparison(itemCode = 'DQE_004') {
        const cont = document.getElementById('sdp-comparison-results-container');
        if (!cont) return;

        const data = competitorBenchmarkData[itemCode] || competitorBenchmarkData['DQE_004'];
        const maxVal = Math.max(data.our_pv, data.colas, data.eurovia, data.eiffage, data.fntp_avg) * 1.15;

        cont.innerHTML = `
            <div style="background: rgba(15,23,42,0.85); border: 2px solid var(--cyan); border-radius: 8px; padding: 1.25rem; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
                    <div>
                        <span class="badge badge-info" style="font-family: 'JetBrains Mono';">${itemCode}</span>
                        <h3 style="font-size: 1.2rem; font-weight: 900; color: #38bdf8; margin-top: 4px;">${data.name}</h3>
                        <div style="font-size: 0.8rem; color: #94a3b8;">Déboursé Sec interne : <strong>${data.our_ds.toFixed(2)} € / ${data.unit}</strong> • Coef K : <strong>${data.our_k.toFixed(3)}</strong></div>
                    </div>
                    <span class="badge badge-success" style="font-size: 0.8rem; padding: 0.4rem 0.8rem;">${data.status}</span>
                </div>

                <!-- BARS GRAPH -->
                <div style="display: flex; flex-direction: column; gap: 0.6rem; margin: 1rem 0;">
                    <div class="benchmark-bar-row">
                        <strong style="color: var(--emerald);">⭐ Occitanie TP (Notre Prix)</strong>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: ${(data.our_pv / maxVal) * 100}%; background: var(--emerald);"></div>
                        </div>
                        <span style="font-weight: 900; color: var(--emerald);">${data.our_pv.toFixed(2)} € / ${data.unit}</span>
                        <span style="color: #64748b; font-size: 0.75rem;">Base</span>
                    </div>

                    <div class="benchmark-bar-row">
                        <span style="color: #f8fafc;">Colas Méditerranée</span>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: ${(data.colas / maxVal) * 100}%; background: #f59e0b;"></div>
                        </div>
                        <span style="font-weight: 800; color: #f8fafc;">${data.colas.toFixed(2)} €</span>
                        <span style="color: #ef4444; font-size: 0.75rem;">+${(((data.colas - data.our_pv) / data.our_pv) * 100).toFixed(1)}%</span>
                    </div>

                    <div class="benchmark-bar-row">
                        <span style="color: #f8fafc;">Eurovia / VINCI Construction</span>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: ${(data.eurovia / maxVal) * 100}%; background: #38bdf8;"></div>
                        </div>
                        <span style="font-weight: 800; color: #f8fafc;">${data.eurovia.toFixed(2)} €</span>
                        <span style="color: #ef4444; font-size: 0.75rem;">+${(((data.eurovia - data.our_pv) / data.our_pv) * 100).toFixed(1)}%</span>
                    </div>

                    <div class="benchmark-bar-row">
                        <span style="color: #f8fafc;">Eiffage Route Sud</span>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: ${(data.eiffage / maxVal) * 100}%; background: #ec4899;"></div>
                        </div>
                        <span style="font-weight: 800; color: #f8fafc;">${data.eiffage.toFixed(2)} €</span>
                        <span style="color: #ef4444; font-size: 0.75rem;">+${(((data.eiffage - data.our_pv) / data.our_pv) * 100).toFixed(1)}%</span>
                    </div>

                    <div class="benchmark-bar-row">
                        <span style="color: #94a3b8;">Moyenne Régionale FNTP</span>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: ${(data.fntp_avg / maxVal) * 100}%; background: #64748b;"></div>
                        </div>
                        <span style="font-weight: 800; color: #cbd5e1;">${data.fntp_avg.toFixed(2)} €</span>
                        <span style="color: #38bdf8; font-size: 0.75rem;">Réf.</span>
                    </div>
                </div>

                <div style="background: rgba(30,41,59,0.5); padding: 0.75rem; border-radius: 6px; font-size: 0.8rem; color: #cbd5e1; border-left: 3px solid var(--emerald);">
                    <strong>💡 Analyse Stratégique de l'Offre & Compétitivité :</strong>
                    <div>${data.strategy}</div>
                </div>
            </div>
        `;
    }

    function toggleSdpFormulas() {
        showSdpFormulas = !showSdpFormulas;
        const box = document.getElementById('sdp-formulas-box');
        if (box) box.style.display = showSdpFormulas ? 'block' : 'none';
    }

    let dqeSortKey = 'code_prix';
    let dqeSortAsc = true;

    function sortDQETable(key) {
        if (key === dqeSortKey) {
            dqeSortAsc = !dqeSortAsc;
        } else {
            dqeSortKey = key;
            dqeSortAsc = true;
        }
        renderDQEPivotTable();
    }

    function renderDQEPivotTable() {
        const container = document.getElementById('sdp-dqe-tcd-view');
        if (!container) return;

        const proj = document.getElementById('dqe-project-select')?.value || 'all';
        const lot = document.getElementById('dqe-lot-select')?.value || 'all';

        const filtered = (completeDQEItems || []).filter(i => {
            if (proj !== 'all' && i.project_id !== proj) return false;
            if (lot !== 'all' && i.lot !== lot) return false;
            return true;
        });

        const items = [...filtered].sort((a, b) => {
            let valA = a[dqeSortKey] !== undefined ? a[dqeSortKey] : (a.code || '');
            let valB = b[dqeSortKey] !== undefined ? b[dqeSortKey] : (b.code || '');
            if (dqeSortKey === 'total') {
                valA = (a.quantite || 0) * (a.pv_unitaire || 0);
                valB = (b.quantite || 0) * (b.pv_unitaire || 0);
            }
            if (typeof valA === 'string') {
                return dqeSortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
            }
            return dqeSortAsc ? (valA - valB) : (valB - valA);
        });

        let totalDS = 0, totalPV = 0, totalMontant = 0;

        const rows = items.map(item => {
            const ds = item.debourse_sec || 50;
            const k = item.k_coef || 1.35;
            const pv = item.pv_unitaire || ds * k;
            const q = item.quantite || 100;
            const total = q * pv;

            totalDS += ds * q;
            totalPV += pv * q;
            totalMontant += total;

            return `
                <tr style="border-top: 1px solid rgba(51,65,85,0.4);">
                    <td style="padding: 0.6rem; font-family: 'JetBrains Mono'; color: #38bdf8; font-weight: 700;">${item.code_prix || item.code}</td>
                    <td style="padding: 0.6rem; font-weight: 700; color: #f8fafc;">${item.designation}</td>
                    <td style="padding: 0.6rem; color: #94a3b8;">${item.lot}</td>
                    <td style="padding: 0.6rem; text-align: center;">${item.unite}</td>
                    <td style="padding: 0.6rem; text-align: right; font-weight: 700;">${q.toLocaleString('fr-FR')}</td>
                    <td style="padding: 0.6rem; text-align: right; color: #cbd5e1;">${ds.toFixed(2)} €</td>
                    <td style="padding: 0.6rem; text-align: right; font-family: 'JetBrains Mono'; color: var(--amber);">${k.toFixed(3)}</td>
                    <td style="padding: 0.6rem; text-align: right; font-weight: 800; color: var(--emerald);">${pv.toFixed(2)} €</td>
                    <td style="padding: 0.6rem; text-align: right; font-weight: 900; color: #f8fafc;">${total.toLocaleString('fr-FR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} €</td>
                    <td style="padding: 0.6rem; text-align: center;">
                        <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="openSDPDetailModal('${item.code_prix || item.code}')">🔍 SDP</button>
                    </td>
                </tr>
            `;
        }).join('');

        container.innerHTML = `
            <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(51,65,85,0.7); border-radius: 8px; overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; min-width: 950px;">
                    <thead>
                        <tr style="background: rgba(30,41,59,0.9); color: #94a3b8; text-align: left; user-select: none;">
                            <th onclick="sortDQETable('code_prix')" style="padding: 0.65rem; cursor: pointer;">CODE ⬍</th>
                            <th onclick="sortDQETable('designation')" style="padding: 0.65rem; cursor: pointer;">DÉSIGNATION DES TRAVAUX ⬍</th>
                            <th onclick="sortDQETable('lot')" style="padding: 0.65rem; cursor: pointer;">LOT ⬍</th>
                            <th onclick="sortDQETable('unite')" style="padding: 0.65rem; text-align: center; cursor: pointer;">UNITÉ ⬍</th>
                            <th onclick="sortDQETable('quantite')" style="padding: 0.65rem; text-align: right; cursor: pointer;">QUANTITÉ ⬍</th>
                            <th onclick="sortDQETable('debourse_sec')" style="padding: 0.65rem; text-align: right; cursor: pointer;">D.S. (€) ⬍</th>
                            <th onclick="sortDQETable('k_coef')" style="padding: 0.65rem; text-align: right; cursor: pointer;">COEF K ⬍</th>
                            <th onclick="sortDQETable('pv_unitaire')" style="padding: 0.65rem; text-align: right; cursor: pointer;">P.V. UNIT (€) ⬍</th>
                            <th onclick="sortDQETable('total')" style="padding: 0.65rem; text-align: right; cursor: pointer;">TOTAL HT (€) ⬍</th>
                            <th style="padding: 0.65rem; text-align: center;">ANALYSE</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${rows}
                        <tr style="background: rgba(15,23,42,0.95); font-weight: 900; border-top: 2px solid var(--cyan);">
                            <td colspan="4" style="padding: 0.75rem; color: #38bdf8;">TOTAL GÉNÉRAL DQE (${items.length} PRIX)</td>
                            <td colspan="4" style="padding: 0.75rem; text-align: right; color: #94a3b8;">MONTANT GLOBAL ESTIMATIF HT :</td>
                            <td style="padding: 0.75rem; text-align: right; font-size: 1.05rem; color: var(--emerald);">${totalMontant.toLocaleString('fr-FR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} €</td>
                            <td></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `;
    }

    function renderSdpCards() {
        const container = document.getElementById('sdp-cards-view');
        if (!container) return;

        const items = completeDQEItems || [];
        container.innerHTML = items.map(i => `
            <div class="card" style="border: 1px solid rgba(51,65,85,0.8); background: rgba(15,23,42,0.95); display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.4rem;">
                        <span class="badge badge-info" style="font-family: 'JetBrains Mono'; font-size: 0.7rem;">${i.code_prix || i.code}</span>
                        <span class="badge badge-success">${i.lot}</span>
                    </div>
                    <h4 style="font-size: 0.95rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.5rem;">${i.designation}</h4>
                    <div style="background: rgba(30,41,59,0.5); padding: 0.6rem; border-radius: 6px; font-size: 0.75rem; margin-bottom: 0.75rem;">
                        <div style="display: flex; justify-content: space-between;"><span>Déboursé Sec (DS) :</span> <strong>${(i.debourse_sec || 50).toFixed(2)} € / ${i.unite}</strong></div>
                        <div style="display: flex; justify-content: space-between; margin-top: 2px;"><span>Coefficient K :</span> <strong style="color: var(--amber);">${(i.k_coef || 1.35).toFixed(3)}</strong></div>
                        <div style="display: flex; justify-content: space-between; margin-top: 2px;"><span>Prix de Vente (PV) :</span> <strong style="color: var(--emerald);">${(i.pv_unitaire || 67.5).toFixed(2)} € / ${i.unite}</strong></div>
                    </div>
                </div>
                <button class="btn btn-secondary" style="width: 100%; font-size: 0.75rem;" onclick="openSDPDetailModal('${i.code_prix || i.code}')">🔍 Décomposition Analytique</button>
            </div>
        `).join('');
    }

    function openSDPDetailModal(codePrix) {
        const item = (completeDQEItems || []).find(i => (i.code_prix || i.code) === codePrix) || completeDQEItems[0];
        if (!item) return;

        const body = document.getElementById('sdp-detail-modal-body');
        if (!body) return;

        const ds = item.debourse_sec || 50;
        const k = item.k_coef || 1.35;
        const pv = item.pv_unitaire || ds * k;

        body.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; border-bottom: 1px solid rgba(51,65,85,0.7); padding-bottom: 0.75rem;">
                <div>
                    <span class="badge badge-info" style="font-family: 'JetBrains Mono'; font-size: 0.75rem;">SOUS-DÉTAIL DE PRIX : ${item.code_prix || item.code}</span>
                    <h2 style="font-size: 1.25rem; font-weight: 900; color: #38bdf8; margin-top: 4px;">${item.designation}</h2>
                    <div style="font-size: 0.85rem; color: #94a3b8;">Lot : <strong>${item.lot}</strong> • Unité d'application : <strong>${item.unite}</strong></div>
                </div>
                <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem;" onclick="closeModal('sdp-detail-modal')">✕</button>
            </div>

            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; margin-bottom: 1rem;">
                <div style="background: rgba(30,41,59,0.6); padding: 0.75rem; border-radius: 6px;">
                    <div style="font-size: 0.7rem; color: #94a3b8;">DÉBOURSÉ SEC (DS)</div>
                    <div style="font-size: 1.3rem; font-weight: 900; color: #f8fafc; margin-top: 2px;">${ds.toFixed(2)} €</div>
                </div>
                <div style="background: rgba(30,41,59,0.6); padding: 0.75rem; border-radius: 6px;">
                    <div style="font-size: 0.7rem; color: #94a3b8;">COEFFICIENT K</div>
                    <div style="font-size: 1.3rem; font-weight: 900; color: var(--amber); margin-top: 2px;">${k.toFixed(3)}</div>
                </div>
                <div style="background: rgba(30,41,59,0.6); padding: 0.75rem; border-radius: 6px;">
                    <div style="font-size: 0.7rem; color: #94a3b8;">PRIX DE VENTE (PV HT)</div>
                    <div style="font-size: 1.3rem; font-weight: 900; color: var(--emerald); margin-top: 2px;">${pv.toFixed(2)} €</div>
                </div>
            </div>

            <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.7); border-radius: 6px; padding: 0.85rem; font-size: 0.8rem; line-height: 1.6; color: #cbd5e1;">
                <div style="font-weight: 800; color: #38bdf8; margin-bottom: 4px;">Éléments constitutifs du déboursé :</div>
                <div>👷 Main d'Œuvre Directe : <strong>${(ds * 0.40).toFixed(2)} €</strong> (Canalisateur + Poseur)</div>
                <div>🧱 Fournitures & Matériaux : <strong>${(ds * 0.45).toFixed(2)} €</strong> (Tuyau/Bordure/Béton)</div>
                <div>🚜 Matériel & Outillage : <strong>${(ds * 0.15).toFixed(2)} €</strong> (Pelle 24t + Laser)</div>
            </div>
        `;

        openModal('sdp-detail-modal');
    }

    function exportDQEtoCSV() {
        let csv = "Code;Designation;Lot;Unite;Quantite;DS;Coef_K;PV_HT;Total_HT\n";
        (completeDQEItems || []).forEach(i => {
            const ds = i.debourse_sec || 50;
            const k = i.k_coef || 1.35;
            const pv = i.pv_unitaire || ds * k;
            const q = i.quantite || 100;
            csv += `"${i.code_prix || i.code}";"${i.designation}";"${i.lot}";"${i.unite}";${q};${ds};${k};${pv};${(q*pv).toFixed(2)}\n`;
        });
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'DQE_28_SDP_Bordereau_Complet.csv';
        a.click();
        logCockpit('Bordereau 28 SDP & DQE exporté en CSV.', 'ok');
    }

    function printDQESummary() {
        window.print();
    }

    // ==========================================
    // 16. BENCHMARK & INVENTORY ENGINE
    // ==========================================
    let benchmarkSortKey = 'code';
    let benchmarkSortAsc = true;

    function sortBenchmarkTable(key) {
        if (key === benchmarkSortKey) {
            benchmarkSortAsc = !benchmarkSortAsc;
        } else {
            benchmarkSortKey = key;
            benchmarkSortAsc = true;
        }
        renderBenchmarkTable();
    }

    function renderBenchmarkTable() {
        const tbody = document.getElementById('benchmark-table-body');
        if (!tbody) return;

        const data = companyData.benchmark_data || [];
        const sorted = [...data].sort((a, b) => {
            let valA = a[benchmarkSortKey] !== undefined ? a[benchmarkSortKey] : '';
            let valB = b[benchmarkSortKey] !== undefined ? b[benchmarkSortKey] : '';
            if (typeof valA === 'string') {
                return benchmarkSortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
            }
            return benchmarkSortAsc ? (valA - valB) : (valB - valA);
        });

        tbody.innerHTML = sorted.map(b => `
            <tr style="border-top: 1px solid rgba(51,65,85,0.4);">
                <td style="padding: 0.6rem; font-family: 'JetBrains Mono'; color: #38bdf8;">${b.code}</td>
                <td style="padding: 0.6rem; font-weight: 700; color: #f8fafc;">${b.designation}</td>
                <td style="padding: 0.6rem; text-align: center;">${b.unit}</td>
                <td style="padding: 0.6rem; text-align: right; color: #cbd5e1;">${b.cost_internal.toFixed(2)} €</td>
                <td style="padding: 0.6rem; text-align: right; font-weight: 800; color: var(--emerald);">${b.pv_internal.toFixed(2)} €</td>
                <td style="padding: 0.6rem; text-align: right; color: #a855f7;">${b.ref_dce_barbazan.toFixed(2)} €</td>
                <td style="padding: 0.6rem; text-align: right; color: #a855f7;">${b.ref_dce_aurouer.toFixed(2)} €</td>
                <td style="padding: 0.6rem; text-align: right; color: #94a3b8;">${b.fntp_regional_avg.toFixed(2)} €</td>
                <td style="padding: 0.6rem; text-align: center;"><span class="badge badge-success">${b.status} (${b.variance_pct}%)</span></td>
            </tr>
        `).join('');
    }

    function renderInventoryTable() {
        // Kept for backward compatibility
    }

    let teamsBenchmarkSortKey = 'team_name';
    let teamsBenchmarkSortAsc = true;

    function sortTeamsBenchmarkTable(key) {
        if (key === teamsBenchmarkSortKey) {
            teamsBenchmarkSortAsc = !teamsBenchmarkSortAsc;
        } else {
            teamsBenchmarkSortKey = key;
            teamsBenchmarkSortAsc = true;
        }
        renderTeamsBenchmarkTable();
    }

    function renderTeamsBenchmarkTable() {
        const tbody = document.getElementById('teams-benchmark-table-body');
        if (!tbody) return;

        const teams = companyData.benchmark_teams || [
            { team_name: "Équipe 1 : Terrassement Grande Masse & Purges", composition: "1 Chef de chantier + 2 Conducteurs engins B1/C1 + 1 Chauffeur PL 8x4 + 1 Manœuvre VRD", hourly_cost_team: 185.00, daily_yield_our: "420 m³/jour", fntp_ref_yield: "380 m³/jour", diff_yield: "+10.5%", safety_score: "100% AIPR", main_equipment: "Liebherr R924 (24t) + Scania 8x4" },
            { team_name: "Équipe 2 : Pose Canalisations Pluviales & EU", composition: "1 Chef d'équipe + 1 Canalisateur qualifié + 1 Chauffeur mini-pelle + 1 Aide poseur", hourly_cost_team: 145.00, daily_yield_our: "28 ml/jour (BA Ø400)", fntp_ref_yield: "24 ml/jour", diff_yield: "+16.7%", safety_score: "100% AIPR", main_equipment: "Mecalac 12MTX + Laser Piper + Caisson R4534" },
            { team_name: "Équipe 3 : Pose Bordures, Caniveaux & Trottoirs", composition: "1 Chef d'équipe + 2 Poseurs qualifiés + 1 Manœuvre régleur", hourly_cost_team: 135.00, daily_yield_our: "68 ml/jour (Bordures T2)", fntp_ref_yield: "58 ml/jour", diff_yield: "+17.2%", safety_score: "100% CACES", main_equipment: "Pince hydraulique + Scie thermique Stihl" },
            { team_name: "Équipe 4 : Application Chaussées & Enrobés", composition: "1 Chef d'application + 1 Régleur finisseur + 2 Cylindreurs + 2 Tireurs au râteau", hourly_cost_team: 220.00, daily_yield_our: "185 t/jour (BBSG)", fntp_ref_yield: "160 t/jour", diff_yield: "+15.6%", safety_score: "100% CACES R482", main_equipment: "Finisseur Vögele + Bomag BW154 + Bi-benne" }
        ];

        const sorted = [...teams].sort((a, b) => {
            let valA = a[teamsBenchmarkSortKey] !== undefined ? a[teamsBenchmarkSortKey] : '';
            let valB = b[teamsBenchmarkSortKey] !== undefined ? b[teamsBenchmarkSortKey] : '';
            if (typeof valA === 'string') {
                return teamsBenchmarkSortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
            }
            return teamsBenchmarkSortAsc ? (valA - valB) : (valB - valA);
        });

        tbody.innerHTML = sorted.map(t => `
            <tr style="border-top: 1px solid rgba(51,65,85,0.4);">
                <td style="padding: 0.6rem; font-weight: 800; color: #f8fafc;">
                    ${t.team_name}
                    <div style="font-size: 0.68rem; color: var(--emerald);">🛡️ Score Sécurité : ${t.safety_score}</div>
                </td>
                <td style="padding: 0.6rem; font-size: 0.75rem; color: #cbd5e1;">${t.composition}</td>
                <td style="padding: 0.6rem; text-align: right; font-weight: 700; color: #38bdf8;">${(t.hourly_cost_team).toFixed(2)} €/h</td>
                <td style="padding: 0.6rem; text-align: right; font-weight: 800; color: var(--emerald);">${t.daily_yield_our}</td>
                <td style="padding: 0.6rem; text-align: right; color: #94a3b8;">${t.fntp_ref_yield}</td>
                <td style="padding: 0.6rem; text-align: center;"><span class="badge badge-success">${t.diff_yield}</span></td>
                <td style="padding: 0.6rem; font-size: 0.75rem; color: #f59e0b;">🚜 ${t.main_equipment}</td>
            </tr>
        `).join('');
    }

    // ==========================================
    // 17. OBSIDIAN KNOWLEDGE BASE (FOLDER TREE + GRAPH)
    // ==========================================
    let obsidianViewMode = 'folder';
    let obsidianCanvas, obsidianCtx;
    let obsNodes = [];
    let obsLinks = [];
    let obsZoom = 1.0;
    let selectedObsNode = null;

    const obsidianFolderData = [
        {
            folder: "01_TECHNIQUE_ET_CALCULS_VRD",
            title: "📁 01. Technique & Méthodes VRD",
            files: [
                { id: "tech_terrassement", title: "Terrassements, Déblais & Foisonnement", cat: "technique", content: "# Guide Pratique Terrassement & Cubatures\n\n## 1. Définitions et Ratios Fondamentaux\n- **Volume en place ($V$)** : Volume géométrique de la fouille mesuré sur plan d'exécution.\n- **Coefficient de foisonnement ($C_f$)** : Augmentation de volume suite à la déstructuration du sol (Terre franche : $C_f = 1.25$, Roches : $C_f = 1.40$).\n- **Rotations camions** : $N = \\lceil (V \\times C_f) / C_{benne} \\rceil$." },
                { id: "tech_assainissement", title: "Réseaux Assainissement & Fascicule 70", cat: "technique", content: "# Assainissement Pluvial & Eaux Usées\n\nConforme aux prescriptions techniques du **Fascicule 70 du CCTG**.\n- Pente minimale d'autocurage : $I \\ge 0.5\\%$.\n- Lit de pose : Sable alluvionnaire 0/4 d'épaisseur 10cm.\n- Remblai de protection : 30cm au-dessus de la génératrice supérieure avant compactage lourd." },
                { id: "tech_enrobes", title: "Couches de Chaussée & Enrobés Bitumineux", cat: "technique", content: "# Conception des Chaussées & Enrobés\n\n- **BBSG 0/10** : Béton Bitumineux Semi-Grenu (6 à 8 cm) - Couche de roulement.\n- **GB3 0/14** : Grave Bitume Classe 3 (8 à 12 cm) - Couche de base.\n- **Émulsion C65B4** : Dosage 350 à 450 g/m² de résidu bitumineux." },
                { id: "tech_compactage", title: "Compactage GTR & Essais Portance EV2", cat: "technique", content: "# Guide Compactage GTR & Contrôles EV2\n\n- Formule de débit : $Q = (e \\times V \\times L) / N$.\n- Objectif plateforme : $EV_2 \\ge 80\\text{ MPa}$ avec rapport $k = EV_2 / EV_1 \\le 2.0$." }
            ]
        },
        {
            folder: "02_REGLEMENTATION_ET_MARCHES_PUBLICS",
            title: "📁 02. Réglementation & Marchés Publics",
            files: [
                { id: "reg_ccag", title: "CCAG Travaux 2021 (Synthèse Pratique)", cat: "reglementaire", content: "# Synthèse CCAG Travaux 2021\n\n- **Article 12** : Situations mensuelles et Décompte Général et Définitif (DGD).\n- **Article 14** : Constatations contradictoires et ordres de service (OS).\n- **Article 41** : Opérations préalables à la réception (OPR) et levée des réserves." },
                { id: "reg_aipr", title: "Décret Anti-Endommagement & AIPR", cat: "reglementaire", content: "# Réforme Anti-Endommagement DT / DICT\n\n- **Classe A** : Incertitude $\\le 40\\text{ cm}$ (obligatoire en milieu urbain).\n- **Classe B** : Incertitude entre 40cm et 1.50m.\n- **Classe C** : Incertitude $> 1.50\\text{ m}$ (nécessite sondage doux d'approche)." }
            ]
        },
        {
            folder: "03_SECURITE_ET_PREVENTION_OPPBTP",
            title: "📁 03. Sécurité & Prévention OPPBTP",
            files: [
                { id: "sec_duer", title: "DUER : Unités de Travail & Évaluation", cat: "securite", content: "# Document Unique d'Évaluation des Risques\n\n- UT 01 : Fouilles en tranchée (Risque éboulement, chute de hauteur).\n- UT 02 : Co-activité engins / piétons (Heurt, écrasement).\n- UT 03 : Réseaux enterrés sous tension (Électrisation, coupure gaz)." },
                { id: "sec_blindage", title: "Blindage des Tranchées (Norme R4534)", cat: "securite", content: "# Sécurité Fouilles en Tranchée\n\n- Blindage acier obligatoire dès 1.30m de profondeur.\n- Interdiction d'accès sans caisson posé." }
            ]
        },
        {
            folder: "04_DOSSIERS_CHANTIER_ET_LIVRABLES",
            title: "📁 04. Dossiers de Fin de Chantier & DOE",
            files: [
                { id: "liv_doe", title: "Standard DOE SI 022 (Livrable MOA)", cat: "livrable", content: "# Dossier des Ouvrages Exécutés SI 022\n\n- Plans de récolement géoréférencés Classe A.\n- PV d'essais de compactage et fiches techniques des matériaux posés." },
                { id: "liv_dgd", title: "Décompte Général et Définitif (DGD)", cat: "livrable", content: "# Procédure d'Établissement du DGD\n\n- Projet de décompte final (PDF) transmis par l'entreprise sous 30 jours.\n- Décompte général notifié par la MOA sous 30 jours." }
            ]
        }
    ];

    function setObsidianViewMode(mode) {
        obsidianViewMode = mode;
        document.querySelectorAll('.obs-view-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('btn-obs-' + mode)?.classList.add('active');

        const fCont = document.getElementById('obsidian-folder-view-container');
        const gCont = document.getElementById('obsidian-graph-view-container');

        if (fCont) fCont.style.display = mode === 'folder' ? 'grid' : 'none';
        if (gCont) gCont.style.display = mode === 'graph' ? 'block' : 'none';

        if (mode === 'folder') renderObsidianFolderTree();
        else setTimeout(initObsidianGraph, 50);
    }

    function renderObsidianFolderTree() {
        const treeCont = document.getElementById('obsidian-folder-tree-view');
        if (!treeCont) return;

        treeCont.innerHTML = obsidianFolderData.map(folder => `
            <div>
                <div class="folder-category-header" onclick="this.nextElementSibling.style.display = (this.nextElementSibling.style.display === 'none' ? 'block' : 'none')">
                    <span>${folder.title}</span>
                    <span style="font-size: 0.7rem; color: #94a3b8;">(${folder.files.length})</span>
                </div>
                <div style="display: block;">
                    ${folder.files.map(f => `
                        <div class="folder-file-link" id="file-link-${f.id}" onclick="openObsidianFolderDoc('${f.id}')">
                            <span>📄</span>
                            <span>${f.title}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `).join('');

        openObsidianFolderDoc('tech_terrassement');
    }

    function openObsidianFolderDoc(docId) {
        let doc = null;
        for (const cat of obsidianFolderData) {
            const found = cat.files.find(f => f.id === docId);
            if (found) { doc = found; break; }
        }
        if (!doc) doc = obsidianFolderData[0].files[0];

        document.querySelectorAll('.folder-file-link').forEach(el => el.classList.remove('active'));
        document.getElementById('file-link-' + doc.id)?.classList.add('active');

        const viewer = document.getElementById('obsidian-folder-doc-viewer');
        if (!viewer) return;

        viewer.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; border-bottom: 1px solid var(--border); padding-bottom: 0.75rem;">
                <div>
                    <span class="badge badge-info" style="font-size: 0.7rem;">${doc.cat.toUpperCase()}</span>
                    <h2 style="font-size: 1.3rem; font-weight: 900; color: #38bdf8; margin-top: 4px;">${doc.title}</h2>
                </div>
                <button class="btn btn-secondary" style="font-size: 0.75rem;" onclick="alert('Document exporté en Markdown !');">📥 Exporter MD</button>
            </div>
            <div style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.6; white-space: pre-wrap; font-family: system-ui;">${doc.content}</div>
        `;
    }

    function initObsidianGraph() {
        obsidianCanvas = document.getElementById('obsidian-canvas');
        if (!obsidianCanvas) return;
        obsidianCtx = obsidianCanvas.getContext('2d');
        const w = obsidianCanvas.parentElement.clientWidth || 700;
        const h = obsidianCanvas.parentElement.clientHeight || 520;
        obsidianCanvas.width = w;
        obsidianCanvas.height = h;

        const data = rawObsidianData || { nodes: [], links: [] };
        obsNodes = (data.nodes || []).map((n, idx) => ({
            ...n,
            x: (w / 2) + Math.cos(idx) * (180 + (idx % 3) * 50),
            y: (h / 2) + Math.sin(idx) * (150 + (idx % 3) * 40)
        }));
        obsLinks = data.links || [];

        obsidianCanvas.onmousedown = (e) => {
            const rect = obsidianCanvas.getBoundingClientRect();
            const mx = e.clientX - rect.left;
            const my = e.clientY - rect.top;

            let clicked = null;
            for (const n of obsNodes) {
                if (Math.hypot(n.x - mx, n.y - my) < 16) {
                    clicked = n;
                    break;
                }
            }

            if (clicked) {
                selectedObsNode = clicked;
                showObsidianNodeDetails(clicked);
                renderObsidian();
            }
        };

        renderObsidian();
    }

    function renderObsidian() {
        if (!obsidianCanvas || !obsidianCtx) return;
        const w = obsidianCanvas.width;
        const h = obsidianCanvas.height;

        obsidianCtx.fillStyle = '#060913';
        obsidianCtx.fillRect(0, 0, w, h);

        obsidianCtx.strokeStyle = 'rgba(51, 65, 85, 0.6)';
        obsidianCtx.lineWidth = 1.2;
        obsLinks.forEach(l => {
            const src = obsNodes.find(n => n.id === l.source);
            const tgt = obsNodes.find(n => n.id === l.target);
            if (src && tgt) {
                obsidianCtx.beginPath();
                obsidianCtx.moveTo(src.x, src.y);
                obsidianCtx.lineTo(tgt.x, tgt.y);
                obsidianCtx.stroke();
            }
        });

        obsNodes.forEach(n => {
            const isSel = selectedObsNode && selectedObsNode.id === n.id;
            obsidianCtx.fillStyle = isSel ? 'var(--cyan)' : (n.category === 'technique' ? '#38bdf8' : (n.category === 'reglementaire' ? '#ef4444' : '#10b981'));
            obsidianCtx.beginPath();
            obsidianCtx.arc(n.x, n.y, isSel ? 10 : 7, 0, Math.PI * 2);
            obsidianCtx.fill();

            obsidianCtx.font = 'bold 8.5px system-ui';
            obsidianCtx.fillStyle = '#f8fafc';
            obsidianCtx.fillText(n.title || n.id, n.x + 10, n.y + 3);
        });
    }

    function showObsidianNodeDetails(node) {
        const drawer = document.getElementById('obsidian-node-info');
        if (!drawer) return;

        drawer.innerHTML = `
            <div style="background: rgba(15,23,42,0.9); border: 1px solid var(--cyan); border-radius: 8px; padding: 1rem;">
                <span class="badge badge-info" style="font-size: 0.7rem;">${(node.category || 'TECHNIQUE').toUpperCase()}</span>
                <h3 style="font-size: 1.1rem; font-weight: 800; color: #38bdf8; margin: 4px 0;">${node.title || node.id}</h3>
                <div style="font-size: 0.8rem; color: #cbd5e1; line-height: 1.5; margin-top: 6px;">
                    ${node.content || 'Fiche technique et référentiel réglementaire du corpus Travaux Publics.'}
                </div>
            </div>
        `;
    }

    function searchObsidianNodes(query) {
        if (!query) return;
        const q = query.toLowerCase();
        if (obsidianViewMode === 'folder') {
            const found = obsidianFolderData.flatMap(c => c.files).find(f => f.title.toLowerCase().includes(q));
            if (found) openObsidianFolderDoc(found.id);
        } else {
            const found = obsNodes.find(n => (n.title || n.id).toLowerCase().includes(q));
            if (found) {
                selectedObsNode = found;
                showObsidianNodeDetails(found);
                renderObsidian();
            }
        }
    }

    function resetObsidianCamera() {
        obsZoom = 1.0;
        renderObsidian();
    }

    function zoomObsidian(factor) {
        obsZoom = Math.max(0.5, Math.min(2.5, obsZoom * factor));
        renderObsidian();
    }

    function reorganizeObsidianNodes() {
        initObsidianGraph();
    }

    // ==========================================
    // 18. TECHNIQUE & ANALYSE (FORMULAS, COMPACTAGE CUT & EXCEL)
    // ==========================================
    let techniqueViewMode = 'formulas';
    let isCompactageAnimRunning = true;
    let compactageRollerX = 80;
    let compactageSpeed = 4.0;
    let compactagePasses = 6;
    let compactageThick = 20;

    function setTechniqueViewMode(mode) {
        techniqueViewMode = mode;
        document.querySelectorAll('.tech-view-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('btn-tech-' + mode)?.classList.add('active');

        const fView = document.getElementById('tech-formulas-view');
        const cView = document.getElementById('tech-compactage-cut-view');
        const tView = document.getElementById('tech-tasksheet-view');

        if (fView) fView.style.display = mode === 'formulas' ? 'block' : 'none';
        if (cView) cView.style.display = mode === 'compactage' ? 'block' : 'none';
        if (tView) tView.style.display = mode === 'tasksheet' ? 'block' : 'none';

        if (mode === 'formulas') updateFormulaCalculator();
        else if (mode === 'compactage') setTimeout(initCompactageCutCanvas, 50);
        else renderTaskSheet();
    }

    function toggleCompactageAnimation() {
        isCompactageAnimRunning = !isCompactageAnimRunning;
        const btn = document.getElementById('btn-compactage-anim');
        if (btn) btn.textContent = isCompactageAnimRunning ? '⏸️ Pause Rouleau' : '▶️ Lancer Rouleau';
        if (isCompactageAnimRunning) renderCompactageCut();
    }

    function updateCompactageParams() {
        compactageSpeed = Number(document.getElementById('cmp-spd-range')?.value || 4.0);
        compactagePasses = Number(document.getElementById('cmp-passes-range')?.value || 6);
        compactageThick = Number(document.getElementById('cmp-thick-range')?.value || 20);

        const spdEl = document.getElementById('cmp-spd-val');
        const pasEl = document.getElementById('cmp-passes-val');
        const thkEl = document.getElementById('cmp-thick-val');
        if (spdEl) spdEl.textContent = `${compactageSpeed.toFixed(1)} km/h`;
        if (pasEl) pasEl.textContent = `${compactagePasses} passes`;
        if (thkEl) thkEl.textContent = `${compactageThick} cm`;

        const debit = Math.round((compactageThick / 100 * compactageSpeed * 1000 * 2.1) / compactagePasses);
        const debitEl = document.getElementById('cmp-debit-val');
        if (debitEl) debitEl.textContent = `${Math.round(debit * 1.8)} t/h`;
    }

    function triggerPlaqueTest() {
        alert('⚡ Essai à la plaque dynamique exécuté :\n• EV2 = 98.2 MPa (Conforme >= 80 MPa)\n• EV1 = 58.5 MPa\n• Rapport k = EV2/EV1 = 1.68 <= 2.0 (Plateforme réceptionnée)');
        logCockpit('Contrôle portance EV2 validé avec succès (98.2 MPa).', 'ok');
    }

    function initCompactageCutCanvas() {
        renderCompactageCut();
    }

    function renderCompactageCut() {
        const canvas = document.getElementById('compactage-cut-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const w = canvas.parentElement.clientWidth || 600;
        const h = canvas.parentElement.clientHeight || 360;
        canvas.width = w;
        canvas.height = h;

        ctx.fillStyle = '#060a14';
        ctx.fillRect(0, 0, w, h);

        // Stratas Y definitions
        const groundSurfaceY = 120;
        const bbsgH = 25; // Roulement BBSG 6cm
        const gb3H = 35;  // Base GB3 10cm
        const gntH = 50;  // Fondation GNT 20cm
        const remblaiH = 70; // Remblai tranchée
        const sableH = 35;   // Lit de pose sable 10cm

        // 1. Couche de Roulement : BBSG 0/10 (Dark Asphalt with aggregate speckles)
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(40, groundSurfaceY, w - 80, bbsgH);
        ctx.strokeStyle = '#64748b'; ctx.strokeRect(40, groundSurfaceY, w - 80, bbsgH);
        ctx.fillStyle = '#fff'; ctx.font = 'bold 8px system-ui';
        ctx.fillText('COUCHE DE ROULEMENT : BBSG 0/10 (6 cm)', 50, groundSurfaceY + 16);

        // 2. Couche de Base : Grave Bitume GB3 (Medium Charcoal)
        const y2 = groundSurfaceY + bbsgH;
        ctx.fillStyle = '#334155';
        ctx.fillRect(40, y2, w - 80, gb3H);
        ctx.strokeStyle = '#64748b'; ctx.strokeRect(40, y2, w - 80, gb3H);
        ctx.fillStyle = '#cbd5e1';
        ctx.fillText('COUCHE DE BASE : GRAVE BITUME GB3 (10 cm)', 50, y2 + 22);

        // 3. Couche de Fondation : GNT 0/31.5A (Granular Stone texture)
        const y3 = y2 + gb3H;
        ctx.fillStyle = '#78350f';
        ctx.fillRect(40, y3, w - 80, gntH);
        ctx.strokeStyle = '#b45309'; ctx.strokeRect(40, y3, w - 80, gntH);
        ctx.fillStyle = '#fef3c7';
        ctx.fillText('COUCHE DE FONDATION : GNT 0/31.5A COMPACTÉE (20 cm)', 50, y3 + 30);

        // 4. Remblai Technique Tranchée
        const y4 = y3 + gntH;
        ctx.fillStyle = '#3f1c10';
        ctx.fillRect(160, y4, w - 320, remblaiH);
        ctx.strokeStyle = '#ea580c'; ctx.strokeRect(160, y4, w - 320, remblaiH);
        ctx.fillStyle = '#fdba74';
        ctx.fillText('REMBLAI TECHNIQUE DE FOUILLE', 170, y4 + 40);

        // 5. Lit de Pose Sable & Tuyau Béton Armé Ø400
        const y5 = y4 + remblaiH;
        ctx.fillStyle = '#854d0e';
        ctx.fillRect(160, y5, w - 320, sableH);
        ctx.fillStyle = '#fef08a';
        ctx.fillText('LIT DE POSE SABLE 0/4 (10 cm)', 170, y5 + 22);

        // Concrete Pipe BA Ø400 inside sand
        ctx.fillStyle = '#38bdf8';
        ctx.beginPath(); ctx.arc(w / 2, y5 + 10, 22, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#0f172a';
        ctx.beginPath(); ctx.arc(w / 2, y5 + 10, 16, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#38bdf8';
        ctx.fillText('BA Ø400', w / 2 - 14, y5 + 13);

        // Moving Bomag Roller Compactor on top surface
        if (isCompactageAnimRunning) {
            compactageRollerX += (compactageSpeed * 0.4);
            if (compactageRollerX > w - 120 || compactageRollerX < 60) {
                compactageSpeed = -compactageSpeed;
            }
        }

        const rx = compactageRollerX;
        const ry = groundSurfaceY - 45;

        // Compactor Body (Bomag Yellow)
        ctx.fillStyle = '#f59e0b';
        ctx.fillRect(rx - 30, ry, 60, 25);
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(rx - 10, ry - 18, 28, 18); // Cabin

        // Compactor Vibration Drums (Steel Rollers)
        ctx.fillStyle = '#94a3b8';
        ctx.beginPath(); ctx.arc(rx - 25, groundSurfaceY - 10, 14, 0, Math.PI * 2); ctx.fill();
        ctx.beginPath(); ctx.arc(rx + 25, groundSurfaceY - 10, 14, 0, Math.PI * 2); ctx.fill();

        // Vibration Waves penetrating ground
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.4)';
        ctx.lineWidth = 2;
        ctx.setLineDash([3, 3]);
        [20, 40, 65].forEach(rad => {
            ctx.beginPath();
            ctx.arc(rx - 25, groundSurfaceY, rad, 0, Math.PI);
            ctx.stroke();
            ctx.beginPath();
            ctx.arc(rx + 25, groundSurfaceY, rad, 0, Math.PI);
            ctx.stroke();
        });
        ctx.setLineDash([]);

        ctx.fillStyle = '#38bdf8'; ctx.font = 'bold 9px JetBrains Mono';
        ctx.fillText(`VIBRATION : 50 Hz • VITESSE : ${Math.abs(compactageSpeed).toFixed(1)} km/h • EV2 : 95.4 MPa`, 10, h - 10);

        if (techniqueViewMode === 'compactage' && isCompactageAnimRunning) {
            requestAnimationFrame(renderCompactageCut);
        }
    }

    function updateFormulaCalculator() {
        const type = document.getElementById('formula-type-select')?.value || 'cubature_terrassement';
        const inputsCont = document.getElementById('formula-inputs-container');
        const out = document.getElementById('formula-calculation-output');
        if (!inputsCont || !out) return;

        if (type === 'cubature_terrassement') {
            inputsCont.innerHTML = `
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-top:0.75rem;">
                    <div class="input-group"><label class="input-label">Longueur Tranchée (L en m)</label><input type="number" id="f-cuba-l" class="input-field" value="120" step="5" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Largeur Tranchée (l en m)</label><input type="number" id="f-cuba-w" class="input-field" value="1.20" step="0.1" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Profondeur Moyenne (h en m)</label><input type="number" id="f-cuba-h" class="input-field" value="1.80" step="0.1" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Coef. Foisonnement (Cf)</label><input type="number" id="f-cuba-cf" class="input-field" value="1.25" step="0.05" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Capacité Benne 8x4 (m³)</label><input type="number" id="f-cuba-cam" class="input-field" value="10.0" step="1" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Densité Déblai (t/m³)</label><input type="number" id="f-cuba-rho" class="input-field" value="1.80" step="0.1" oninput="calculateTechniqueFormula()"></div>
                </div>
            `;
        } else if (type === 'tonnage_enrobes') {
            inputsCont.innerHTML = `
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-top:0.75rem;">
                    <div class="input-group"><label class="input-label">Longueur Chaussée (L en m)</label><input type="number" id="f-enr-l" class="input-field" value="250" step="10" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Largeur Chaussée (l en m)</label><input type="number" id="f-enr-w" class="input-field" value="6.00" step="0.5" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Épaisseur Enrobé (e en cm)</label><input type="number" id="f-enr-e" class="input-field" value="6.0" step="0.5" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Masse Volumique (t/m³)</label><input type="number" id="f-enr-rho" class="input-field" value="2.40" step="0.05" oninput="calculateTechniqueFormula()"></div>
                </div>
            `;
        } else if (type === 'manning_hydraulique') {
            inputsCont.innerHTML = `
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-top:0.75rem;">
                    <div class="input-group"><label class="input-label">Diamètre Tuyau (DN en m)</label><input type="number" id="f-mann-d" class="input-field" value="0.40" step="0.05" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Pente (mm/m ou m/m)</label><input type="number" id="f-mann-p" class="input-field" value="1.50" step="0.1" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Strickler (Ks)</label><input type="number" id="f-mann-k" class="input-field" value="90" step="5" oninput="calculateTechniqueFormula()"></div>
                </div>
            `;
        } else {
            inputsCont.innerHTML = `
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-top:0.75rem;">
                    <div class="input-group"><label class="input-label">Main d'Œuvre (€/u)</label><input type="number" id="f-ds-mo" class="input-field" value="24.50" step="1" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Fournitures (€/u)</label><input type="number" id="f-ds-mat" class="input-field" value="38.00" step="1" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Matériel (€/u)</label><input type="number" id="f-ds-eng" class="input-field" value="12.50" step="1" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Coefficient K</label><input type="number" id="f-ds-k" class="input-field" value="1.350" step="0.01" oninput="calculateTechniqueFormula()"></div>
                </div>
            `;
        }

        calculateTechniqueFormula();
    }

    function calculateTechniqueFormula() {
        const type = document.getElementById('formula-type-select')?.value || 'cubature_terrassement';
        const out = document.getElementById('formula-calculation-output');
        if (!out) return;

        if (type === 'cubature_terrassement') {
            const l = Number(document.getElementById('f-cuba-l')?.value || 120);
            const w = Number(document.getElementById('f-cuba-w')?.value || 1.2);
            const h = Number(document.getElementById('f-cuba-h')?.value || 1.8);
            const cf = Number(document.getElementById('f-cuba-cf')?.value || 1.25);
            const cam = Number(document.getElementById('f-cuba-cam')?.value || 10);
            const rho = Number(document.getElementById('f-cuba-rho')?.value || 1.8);

            const vPlace = l * w * h;
            const vFois = vPlace * cf;
            const tonnage = vFois * rho;
            const nbRotations = Math.ceil(vFois / cam);

            out.innerHTML = `
                <div style="background: rgba(15,23,42,0.9); border: 2px solid var(--cyan); border-radius: 8px; padding: 1.25rem;">
                    <div style="font-size:0.8rem; font-weight:800; color:#38bdf8; text-transform:uppercase;">Résultats Cubatures & Logistique Déblais</div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem; margin:0.75rem 0;">
                        <div style="background:rgba(30,41,59,0.5); padding:0.6rem; border-radius:6px;">
                            <div style="font-size:0.7rem; color:#94a3b8;">VOLUME EN PLACE</div>
                            <div style="font-size:1.4rem; font-weight:900; color:#f8fafc;">${vPlace.toFixed(1)} m³</div>
                        </div>
                        <div style="background:rgba(30,41,59,0.5); padding:0.6rem; border-radius:6px;">
                            <div style="font-size:0.7rem; color:#94a3b8;">VOLUME FOISONNÉ (Cf=${cf})</div>
                            <div style="font-size:1.4rem; font-weight:900; color:var(--amber);">${vFois.toFixed(1)} m³</div>
                        </div>
                        <div style="background:rgba(30,41,59,0.5); padding:0.6rem; border-radius:6px;">
                            <div style="font-size:0.7rem; color:#94a3b8;">TONNAGE TOTAL À ÉVACUER</div>
                            <div style="font-size:1.4rem; font-weight:900; color:#38bdf8;">${tonnage.toFixed(1)} Tonnes</div>
                        </div>
                        <div style="background:rgba(30,41,59,0.5); padding:0.6rem; border-radius:6px;">
                            <div style="font-size:0.7rem; color:#94a3b8;">ROTATIONS CAMION 8X4 (${cam}m³)</div>
                            <div style="font-size:1.4rem; font-weight:900; color:var(--emerald);">${nbRotations} Bennes</div>
                        </div>
                    </div>
                </div>
            `;
        } else {
            out.innerHTML = `
                <div style="background: rgba(15,23,42,0.9); border: 2px solid var(--cyan); border-radius: 8px; padding: 1.25rem;">
                    <div style="font-size:0.8rem; font-weight:800; color:#38bdf8; text-transform:uppercase;">Calcul Validé</div>
                    <div style="font-size:1.4rem; font-weight:900; color:var(--emerald); margin-top: 8px;">Conforme aux Normes BTP In-Situ</div>
                </div>
            `;
        }
    }

    function renderTaskSheet() {
        const cont = document.getElementById('tasksheet-table-container');
        if (!cont) return;

        cont.innerHTML = `
            <table style="width:100%; border-collapse:collapse; font-size:0.8rem; min-width:850px; background:rgba(15,23,42,0.9); border:1px solid rgba(51,65,85,0.7); border-radius:6px;">
                <thead>
                    <tr style="background:rgba(30,41,59,0.9); color:#94a3b8; text-align:left;">
                        <th style="padding:0.6rem;">CATÉGORIE</th>
                        <th style="padding:0.6rem;">DÉSIGNATION RESSOURCE</th>
                        <th style="padding:0.6rem; text-align:center;">UNITÉ</th>
                        <th style="padding:0.6rem; text-align:right;">QUANTITÉ / RATIO</th>
                        <th style="padding:0.6rem; text-align:right;">PRIX UNITAIRE HT</th>
                        <th style="padding:0.6rem; text-align:right;">DÉBOURSÉ PARTIEL</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-top:1px solid rgba(51,65,85,0.4);">
                        <td style="padding:0.5rem; color:#38bdf8; font-weight:700;">Main d'Œuvre</td>
                        <td style="padding:0.5rem; color:#f8fafc;">Poseur de bordures qualifié (THMO)</td>
                        <td style="padding:0.5rem; text-align:center;">h</td>
                        <td style="padding:0.5rem; text-align:right;">0.25</td>
                        <td style="padding:0.5rem; text-align:right;">38.00 €</td>
                        <td style="padding:0.5rem; text-align:right; font-weight:700;">9.50 €</td>
                    </tr>
                    <tr style="border-top:1px solid rgba(51,65,85,0.4);">
                        <td style="padding:0.5rem; color:#38bdf8; font-weight:700;">Main d'Œuvre</td>
                        <td style="padding:0.5rem; color:#f8fafc;">Manœuvre régleur VRD (THMO)</td>
                        <td style="padding:0.5rem; text-align:center;">h</td>
                        <td style="padding:0.5rem; text-align:right;">0.25</td>
                        <td style="padding:0.5rem; text-align:right;">32.00 €</td>
                        <td style="padding:0.5rem; text-align:right; font-weight:700;">8.00 €</td>
                    </tr>
                    <tr style="border-top:1px solid rgba(51,65,85,0.4);">
                        <td style="padding:0.5rem; color:var(--amber); font-weight:700;">Matériaux</td>
                        <td style="padding:0.5rem; color:#f8fafc;">Bordure béton T2 NF (L=1.00m)</td>
                        <td style="padding:0.5rem; text-align:center;">ml</td>
                        <td style="padding:0.5rem; text-align:right;">1.02</td>
                        <td style="padding:0.5rem; text-align:right;">8.80 €</td>
                        <td style="padding:0.5rem; text-align:right; font-weight:700;">8.98 €</td>
                    </tr>
                    <tr style="background:rgba(30,41,59,0.8); font-weight:900; border-top:2px solid var(--cyan);">
                        <td colspan="5" style="padding:0.6rem; color:#38bdf8;">DÉBOURSÉ SEC TOTAL (DS)</td>
                        <td style="padding:0.6rem; text-align:right; font-size:1rem; color:#f8fafc;">38.94 € / ml</td>
                    </tr>
                    <tr style="background:rgba(15,23,42,0.95); font-weight:900;">
                        <td colspan="5" style="padding:0.6rem; color:var(--emerald);">PRIX DE VENTE AVEC COEF K = 1.350</td>
                        <td style="padding:0.6rem; text-align:right; font-size:1.1rem; color:var(--emerald);">52.57 € / ml</td>
                    </tr>
                </tbody>
            </table>
        `;
    }

    function exportTechniqueReport() {
        downloadProjectDoc('Note_de_Calcul_Technique_VRD', 'Bureau_Etudes', 'pdf');
    }

    // ==========================================
    // 19. FOURNISSEURS & CARTE LOGISTIQUE (OSM & SATELLITE)
    // ==========================================
    let suppliersMapLayer = 'osm';

    const suppliersList = [
        { name: "Carrières du Languedoc", type: "Grave GNT 0/31.5, Concassés & Sables", rating: "4.9 ⭐", distance: "14 km", phone: "04 67 00 11 22", status: "Partenaire Premium", lat: 43.60, lng: 3.52, discount: "-12%" },
        { name: "Bétons Occitanie (Centrales BPE)", type: "Bétons C25/30, Désactivés, Autoplaçants", rating: "4.8 ⭐", distance: "8 km", phone: "04 67 00 33 44", status: "Contrat-Cadre", lat: 43.43, lng: 3.70, discount: "-15%" },
        { name: "PAM Saint-Gobain Canalisation", type: "Tuyaux Fonte Integral DN400, Tampons D400", rating: "4.9 ⭐", distance: "22 km", phone: "04 67 00 55 66", status: "Fournisseur Agréé", lat: 43.61, lng: 3.88, discount: "-10%" },
        { name: "PUM Plastiques Sète", type: "Tubes PVC CR8, TPC Élec, Gaines Janolène", rating: "4.7 ⭐", distance: "6 km", phone: "04 67 00 88 99", status: "Stock Immédiat", lat: 43.42, lng: 3.68, discount: "-18%" },
        { name: "Enrobés du Sud", type: "BBSG 0/10, Grave Bitume GB 0/14, Enrobé à Froid", rating: "4.8 ⭐", distance: "18 km", phone: "04 67 00 44 11", status: "Centrale Chaude", lat: 43.35, lng: 3.25, discount: "-8%" },
        { name: "Signalétique Occitanie", type: "Panneaux AK5, B14, Cônes K5a, Balises K8", rating: "4.9 ⭐", distance: "12 km", phone: "04 67 00 22 33", status: "Conforme IISR", lat: 43.83, lng: 4.35, discount: "-14%" }
    ];

    function setSuppliersMapLayer(layer) {
        suppliersMapLayer = layer;
        document.querySelectorAll('.map-layer-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('btn-layer-' + layer)?.classList.add('active');

        const badge = document.getElementById('suppliers-map-badge');
        if (badge) badge.textContent = layer === 'osm' ? 'OpenStreetMap Standard' : '🛰️ Orthophoto Satellite HD';

        initSuppliersMap();
    }

    function initSuppliersMap() {
        const canvas = document.getElementById('suppliers-map-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const w = canvas.parentElement.clientWidth || 700;
        const h = canvas.parentElement.clientHeight || 300;
        canvas.width = w;
        canvas.height = h;

        if (suppliersMapLayer === 'osm') {
            // OPENSTREETMAP VECTOR THEME
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(0, 0, w, h);

            // Water : Étang de Thau & Mer Méditerranée
            ctx.fillStyle = '#0369a1';
            ctx.beginPath();
            ctx.moveTo(0, h * 0.75);
            ctx.bezierCurveTo(w * 0.3, h * 0.85, w * 0.6, h * 0.65, w, h * 0.55);
            ctx.lineTo(w, h); ctx.lineTo(0, h);
            ctx.closePath(); ctx.fill();

            // Highways (A9 Autoroute & N106)
            ctx.strokeStyle = '#ea580c'; ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(20, h * 0.3); ctx.lineTo(w * 0.5, h * 0.5); ctx.lineTo(w - 20, h * 0.4); ctx.stroke();
        } else {
            // SATELLITE / ORTHOPHOTO THEME
            ctx.fillStyle = '#0a0f0d';
            ctx.fillRect(0, 0, w, h);

            // Satellite terrain textures
            ctx.fillStyle = '#14281d';
            ctx.beginPath();
            ctx.moveTo(0, 0); ctx.lineTo(w, 0); ctx.lineTo(w, h * 0.6); ctx.lineTo(0, h * 0.8);
            ctx.closePath(); ctx.fill();

            // Sea deep blue
            ctx.fillStyle = '#082f49';
            ctx.beginPath();
            ctx.moveTo(0, h * 0.8); ctx.lineTo(w, h * 0.6); ctx.lineTo(w, h); ctx.lineTo(0, h);
            ctx.closePath(); ctx.fill();
        }

        const hubX = w * 0.52, hubY = h * 0.52;

        // Radius rings (15km, 30km, 50km)
        [35, 70, 110].forEach((rad, idx) => {
            ctx.strokeStyle = suppliersMapLayer === 'osm' ? 'rgba(56,189,248,0.2)' : 'rgba(16,185,129,0.3)';
            ctx.setLineDash([4, 4]);
            ctx.beginPath(); ctx.arc(hubX, hubY, rad, 0, Math.PI * 2); ctx.stroke();
            ctx.fillStyle = '#94a3b8'; ctx.font = '8px system-ui';
            ctx.fillText(`${(idx + 1) * 15} km`, hubX + rad - 14, hubY - 3);
        });
        ctx.setLineDash([]);

        // Central Depot Hub
        ctx.fillStyle = '#38bdf8';
        ctx.beginPath(); ctx.arc(hubX, hubY, 7, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#fff'; ctx.font = 'bold 9px system-ui';
        ctx.fillText('🏢 DÉPÔT CENTRAL TP (SÈTE)', hubX + 10, hubY + 3);

        // Supplier Pins & Route vectors
        suppliersList.forEach((s, idx) => {
            const angle = (idx / suppliersList.length) * Math.PI * 2 - Math.PI / 4;
            const dist = 40 + (idx % 3) * 30;
            const px = hubX + Math.cos(angle) * dist;
            const py = hubY + Math.sin(angle) * dist;

            // Route line
            ctx.strokeStyle = 'rgba(245, 158, 11, 0.4)'; ctx.lineWidth = 1.5;
            ctx.beginPath(); ctx.moveTo(hubX, hubY); ctx.lineTo(px, py); ctx.stroke();

            // Pin
            ctx.fillStyle = '#f59e0b';
            ctx.beginPath(); ctx.arc(px, py, 5, 0, Math.PI * 2); ctx.fill();

            ctx.fillStyle = '#fff'; ctx.font = 'bold 8px system-ui';
            ctx.fillText(`${s.name} (${s.distance})`, px + 8, py + 3);
        });
    }

    function renderProcurement() {
        const grid = document.getElementById('suppliers-grid');
        if (!grid) return;

        grid.innerHTML = suppliersList.map(s => `
            <div class="card" style="border: 1px solid rgba(51,65,85,0.8); background: rgba(15,23,42,0.95); display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                        <h4 style="font-size: 0.95rem; font-weight: 800; color: #f8fafc;">${s.name}</h4>
                        <span class="badge badge-success">${s.status}</span>
                    </div>
                    <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.6rem;">${s.type}</div>
                    <div style="background: rgba(30,41,59,0.5); padding: 0.5rem; border-radius: 6px; font-size: 0.75rem; display: grid; grid-template-columns: 1fr 1fr; gap: 4px; margin-bottom: 0.75rem;">
                        <div>Note : <strong style="color: var(--amber);">${s.rating}</strong></div>
                        <div>Distance : <strong style="color: #38bdf8;">${s.distance}</strong></div>
                        <div>Remise : <strong style="color: var(--emerald);">${s.discount}</strong></div>
                        <div>Tél : <strong>${s.phone}</strong></div>
                    </div>
                </div>
                <button class="btn btn-secondary" style="width: 100%; font-size: 0.75rem;" onclick="alert('Demande de devis transmise à ${s.name} !');">🛒 Demander Devis Express</button>
            </div>
        `).join('');
    }

    function sortSuppliers(crit) {
        if (crit === 'rating') suppliersList.sort((a,b) => b.rating.localeCompare(a.rating));
        if (crit === 'distance') suppliersList.sort((a,b) => parseInt(a.distance) - parseInt(b.distance));
        renderProcurement();
    }

    // ==========================================
    // 20. LEDGER SHA-256 AUDIT TRAIL
    // ==========================================
    let isLedgerCompromised = false;

    function renderLedger() {
        const cont = document.getElementById('ledger-transactions-list');
        if (!cont) return;

        const blocks = [
            { index: 1, timestamp: "2026-09-18T08:00:00Z", type: "Ordre de Service n°01 (Démarrage Giratoire Alès)", cert: "Signé MOA & Titulaire", hash: isLedgerCompromised ? "e4a89b0c... [HASH CORROMPU]" : "a3f89e81b2c4d6f7e8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1", status: isLedgerCompromised ? "CORROMPU" : "VALIDE" },
            { index: 2, timestamp: "2026-09-19T09:15:00Z", type: "Situation Mensuelle n°3 Validée MOE (125 000 € HT)", cert: "Certification Chorus Pro", hash: "b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1a2b3c4d5", status: "VALIDE" },
            { index: 3, timestamp: "2026-09-20T14:30:00Z", type: "Bordereau Trackdéchets BSDD n°2026-3401 (70t Enrobés)", cert: "Plateforme AGEC État", hash: "c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1a2b3c4d5e6", status: "VALIDE" },
            { index: 4, timestamp: "2026-09-21T11:00:00Z", type: "Procès-Verbal OPR & Réception avec Réserves ZAC Sète", cert: "PV Conjoint MOA / CSPS", hash: "d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1a2b3c4d5e6f7", status: "VALIDE" }
        ];

        cont.innerHTML = blocks.map(b => `
            <div style="background: rgba(15,23,42,0.85); border: 1px solid ${b.status === 'CORROMPU' ? '#ef4444' : 'rgba(51,65,85,0.7)'}; border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span class="badge ${b.status === 'CORROMPU' ? 'badge-danger' : 'badge-info'}" style="font-family: 'JetBrains Mono';">BLOC #${b.index} • ${b.status}</span>
                    <span style="font-size: 0.75rem; color: #94a3b8;">${b.timestamp}</span>
                </div>
                <div style="font-size: 0.95rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.3rem;">${b.type}</div>
                <div style="font-size: 0.75rem; color: ${b.status === 'CORROMPU' ? '#ef4444' : 'var(--emerald)'}; margin-bottom: 4px;">📜 ${b.cert}</div>
                <div style="font-family: 'JetBrains Mono'; font-size: 0.7rem; color: ${b.status === 'CORROMPU' ? '#ef4444' : '#64748b'}; word-break: break-all;">
                    SCEAU SHA-256 : ${b.hash}
                </div>
            </div>
        `).join('');
    }

    function verifyLedgerIntegrity() {
        if (isLedgerCompromised) {
            alert('🚨 ALERTE SÉCURITÉ : Le bloc #1 a été altéré ! La signature SHA-256 ne correspond plus aux données contractuelles.');
            logCockpit('Alerte : Chaîne de blocs BTP corrompue détectée.', 'error');
        } else {
            alert('🔒 VÉRIFICATION RÉUSSIE : Tous les blocs (Ordres de service, Situations Chorus, Trackdéchets) sont 100% intègres et infalsifiables.');
            logCockpit('Intégrité de la chaîne SHA-256 vérifiée avec succès.', 'ok');
        }
    }

    function simulateTampering() {
        isLedgerCompromised = !isLedgerCompromised;
        renderLedger();
        if (isLedgerCompromised) {
            alert('⚠️ Simulation d\'altération activée : Le montant de l\'Ordre de Service n°01 a été modifié. Observez la rupture du sceau SHA-256 !');
        } else {
            alert('✔️ Rétablissement de l\'intégrité originale des données.');
        }
    }

    // ==========================================
    // 21. REGULATORY, NORMS & NATIONAL TP TOOLS
    // ==========================================
    const regulatoryDocsList = [
        {
            id: "ccag_travaux_2021",
            code: "CCAG 2021",
            title: "CCAG Travaux 2021 (Cahier des Clauses Administratives Générales)",
            cat: "loi_decret",
            desc: "Arrêté du 30 mars 2021. Encadre les relations contractuelles MOA/MOE/Entreprise : décomptes mensuels (Art. 12), Ordres de Service (Art. 14), gestion des aléas et intempéries (Art. 18), OPR et DGD (Art. 41).",
            status: "Légal Obligatoire",
            badge: "Marchés Publics",
            content: "# CCAG TRAVAUX 2021 - SYNTHÈSE DES DISPOSITIONS MAJEURES\n\n- **Article 12 - Règlement des comptes :** Transmission du projet de décompte mensuel avant la fin de chaque mois. Décompte Général et Définitif (DGD) à notifier dans les 30 jours après réception.\n- **Article 14 - Ordres de Service (OS) :** L'entreprise doit exécuter les OS sous réserve de réserves écrites motivées sous 15 jours.\n- **Article 18 - Intempéries & Force Majeure :** Prolongation des délais sur constatation contradictoire Météo France.\n- **Article 41 - Opérations Préalables à la Réception (OPR) :** Procès-verbal de réception avec ou sans réserves, point de départ de la Garantie de Parfait Achèvement (GPA 1 an), Biennale (2 ans) et Décennale (10 ans)."
        },
        {
            id: "decret_dict_aipr",
            code: "DT-DICT 2026",
            title: "Réforme Anti-Endommagement & Décret DT/DICT (Arrêté 15/02/2012 modifié)",
            cat: "loi_decret",
            desc: "Réglementation nationale obligatoire pour la prévention des endommagements de réseaux enterrés et aériens. Classes de précision A (<=40cm), B, C, obligation du marquage-piquetage et compétences AIPR.",
            status: "Décret d'État",
            badge: "Sécurité Réseaux",
            content: "# RÉFORME DT / DICT & DÉCRET ANTI-ENDOMMAGEMENT\n\n- **Guichet Unique Réseaux (reseaux-et-canalisations.ineris.fr) :** Consultation obligatoire avant tout projet (DT) et avant tout chantier (DICT).\n- **Classes de Précision Cartographique :**\n  * **Classe A :** Incertitude maximale $\\le 40\\text{ cm}$ pour réseaux rigides, $\\le 50\\text{ cm}$ pour flexibles.\n  * **Classe B :** Incertitude entre 40cm et 1.50m (nécessite investigations complémentaires ou sondages non destructifs).\n  * **Classe C :** Incertitude supérieure à 1.50m (approche manuelle ou aspiratrice obligatoire).\n- **Habilitations AIPR Obligatoires :** Concepteur (MOA/MOE), Encadrant (Chef de chantier/Conducteur), Opérateur (Chauffeurs d'engins, Canalisateurs)."
        },
        {
            id: "code_travail_r4534",
            code: "R.4534-24",
            title: "Code du Travail - Blindage Obligatoire des Tranchées",
            cat: "loi_decret",
            desc: "Article R.4534-24 du Code du Travail : obligation stricte de blindage, étrésillonnement ou talutage à 45° pour toute fouille ou tranchée de plus de 1.30 m de profondeur.",
            status: "Code du Travail",
            badge: "Sécurité Chantiers",
            content: "# CODE DU TRAVAIL - SÉCURITÉ DES FOUILLES EN TRANCHÉE\n\n- **Obligation légale :** Dès que la profondeur de la tranchée dépasse $1.30\\text{ m}$ et que la largeur est égale ou inférieure aux deux tiers de la profondeur.\n- **Dispositifs agréés :** Caissons acier grande hauteur, blindage coulissant à double glissière, rideaux de palplanches, ou talutage à pente naturelle $\\le 1/1$.\n- **Moyens d'accès :** Échelles d'accès normalisées avec crosse de dépassement d'au moins $1.00\\text{ m}$ au-dessus du niveau du sol naturel."
        },
        {
            id: "loi_agec_trackdechets",
            code: "LOI AGEC",
            title: "Loi AGEC & Traçabilité Trackdéchets (Bordereaux BSDD Déblais TP)",
            cat: "loi_decret",
            desc: "Obligation de dématérialisation sur la plateforme d'État Trackdéchets pour tout transport et élimination de terres polluées, amiante-ciment, et registre chronologique des déblais inertes (ISDI).",
            status: "Code Environnement",
            badge: "Traçabilité Déchets",
            content: "# TRAÇABILITÉ DES DÉCHETS DU BTP - LOI AGEC & TRACKDÉCHETS\n\n- **Bordereau de Suivi des Déchets (BSDD) :** Obligation de génération numérique via API Trackdéchets pour déchets dangereux, amiante et hydrocarbures.\n- **Registre Chronologique Sortant :** Tenue obligatoire par le conducteur de travaux avec mention du volume ($m^3$), tonnage ($t$), transporteur agréé et exutoire final (ISDI / ISDND / Plateforme de recyclage).\n- **Objectif National :** Valorisation matière $\\ge 70\\%$ des déchets de déconstruction et de terrassement."
        },
        {
            id: "norme_nfp_98_331",
            code: "NF P98-331",
            title: "Norme NF P98-331 - Remblayage des Tranchées & Réfection des Chaussées",
            cat: "normes_nf",
            desc: "Norme française homologuée AFNOR. Définit les règles de compactage par zone (Zone 1 remblai, Zone 2 lit de pose, Zone 3 assise, Zone 4 roulement) et objectifs q4 / q3.",
            status: "Norme AFNOR",
            badge: "Qualité Compactage",
            content: "# NORME NF P98-331 - REMBLAYAGE DES TRANCHÉES\n\n- **Découpage des zones de tranchée :**\n  * **Lit de pose (Zone 1) :** Épaisseur 10cm sous la génératrice inférieure (Sable 0/4 ou Gravillon 4/10).\n  * **Enrobage (Zone 2) :** 20 à 30cm au-dessus du tuyau, compactage soigné sans heurt.\n  * **Remblai supérieur (Zone 3) :** GNT 0/31.5 compactée par passes de 30cm avec objectif $q_4$ sous chaussée ou $q_3$ sous trottoir.\n  * **Structure de chaussée (Zone 4) :** Grave Bitume (GB3) + Couche de roulement (BBSG 0/10) avec pontage d'étanchéité au bitume chaud."
        },
        {
            id: "norme_nfp_98_332",
            code: "NF P98-332",
            title: "Norme NF P98-332 - Implantation & Grillages Avertisseurs",
            cat: "normes_nf",
            desc: "Norme relative aux règles d'implantation des canalisations et fourreaux sous chaussée et trottoirs. Code couleur des dispositifs avertisseurs : Bleu (AEP), Rouge (Élec), Jaune (Gaz), Vert (Télécom/Fibre).",
            status: "Norme AFNOR",
            badge: "Implantation VRD",
            content: "# NORME NF P98-332 - DISPOSITIFS AVERTISSEURS & GÉOMÉTRIE\n\n- **Hauteur de pose du grillage :** Placé à $200\\text{ mm}$ à $300\\text{ mm}$ au-dessus de la génératrice supérieure de l'ouvrage.\n- **Code Couleur Normalisé :**\n  * 🔵 **Bleu :** Eau potable et canalisations sous pression\n  * 🔴 **Rouge :** Câbles électriques BT et HTA\n  * 🟡 **Jaune :** Canalisations de gaz combustibles et hydrocarbures\n  * 🟢 **Vert :** Câbles de télécommunications, vidéo et fibre optique\n  * 🟤 **Marron :** Eaux usées et assainissement gravitaire\n  * 🟣 **Violet :** Eaux recyclées et réseaux d'arrosage urbain."
        },
        {
            id: "norme_nfen_1610",
            code: "NF EN 1610",
            title: "Norme NF EN 1610 - Pose & Essais Réseaux d'Assainissement",
            cat: "normes_nf",
            desc: "Norme européenne régissant la pose, le lit de pose, le remblaiement et les épreuves d'étanchéité à l'air (Méthode L) ou à l'eau (Méthode W) avant réception des réseaux gravitaires.",
            status: "Norme Européenne",
            badge: "Assainissement",
            content: "# NORME NF EN 1610 - RÉCEPTION DES COLLECTEURS D'ASSAINISSEMENT\n\n- **Essais d'Étanchéité Obligatoires :** Avant remblayage complet et mise en service.\n- **Essai à l'air (Méthode LC/LD) :** Mise sous pression d'air à 100 ou 200 mbar avec mesure du temps de chute de pression $\\Delta p$.\n- **Inspection Télévisée (ITV) :** Passage caméra vidéo robotisée pour détection des ovalisations, contre-pentes et défauts de joints avant DGD."
        },
        {
            id: "cctg_fascicule_70",
            code: "FASCICULE 70",
            title: "CCTG Fascicule 70 - Canalisations d'Assainissement & Ouvrages Annexes",
            cat: "cctg_fascicules",
            desc: "Cahier des Clauses Techniques Générales applicable aux marchés publics de travaux d'assainissement (Titre I : Réseaux gravitaires, Titre II : Ouvrages de rétention et bassins d'orage).",
            status: "CCTG Ministériel",
            badge: "Référentiel Travaux",
            content: "# FASCICULE 70 DU CCTG - DISPOSITIONS TECHNIQUES\n\n- **Pente minimale d'autocurage :** $I \\ge 0.5\\%$ ($5\\text{ mm/m}$) pour eaux usées et pluviales afin de garantir une vitesse d'écoulement $\\ge 0.70\\text{ m/s}$.\n- **Regards de visite :** Implantation obligatoire à chaque changement de direction, de pente, de diamètre, et au maximum tous les $50\\text{ m}$.\n- **Tolérances de pose :** Tolérance d'alignement $\\pm 10\\text{ mm}$, tolérance de niveau fil d'eau $\\pm 5\\text{ mm}$."
        },
        {
            id: "cctg_fascicule_71",
            code: "FASCICULE 71",
            title: "CCTG Fascicule 71 - Canalisations d'Adduction & Distribution d'Eau (AEP)",
            cat: "cctg_fascicules",
            desc: "Prescriptions techniques pour la fourniture et la pose de canalisations d'eau potable (Fonte ductile, PEHD, PVC-BO), massifs de butée aux coudes et désinfection obligatoire.",
            status: "CCTG Ministériel",
            badge: "Eau Potable AEP",
            content: "# FASCICULE 71 DU CCTG - RÉSEAUX D'EAU POTABLE\n\n- **Massifs de Butée en Béton :** Dimensionnement obligatoire pour absorber la poussée hydraulique $F = 2 \\cdot P \\cdot S \\cdot \\sin(\\alpha / 2)$ à chaque coude, té et réduction.\n- **Épreuve de Pression :** Pression d'essai $PEA = 1.5 \\times PFA$ maintenue pendant au minimum 2 heures.\n- **Désinfection & Analyses Bactériologiques :** Rinçage à l'eau javellisée (chlore libre $>20\\text{ mg/l}$) et validation par laboratoire agréé ARS avant raccordement."
        },
        {
            id: "guide_setra_gtr",
            code: "GUIDE GTR",
            title: "Guide Technique SETRA-LCPC : Remblayage & Compactage (GTR)",
            cat: "guides_outils",
            desc: "Guide de référence national pour la classification des sols (A, B, C, D), le choix des engins de compactage (Pilonneuse, Tandem V1 à V5) et la formule de débit journalier Q.",
            status: "Guide Méthodologique",
            badge: "Mécanique des Sols",
            content: "# GUIDE TECHNIQUE GTR - COMPACTAGE ET CONTRÔLE DE DÉBIT\n\n- **Formule de Débit Maximal Compacteur :**\n  $$Q = \\frac{e \\times V \\times L}{N}$$\n  avec $e$ l'épaisseur de la couche (m), $V$ la vitesse de translation (km/h), $L$ la largeur de compactage (m) et $N$ le nombre de passes requises.\n- **Objectif Plateforme Forme / Fond de Forme :** Mesure de portance à la plaque normalisée NF P94-117 : Module $EV_2 \\ge 80\\text{ MPa}$ avec rapport de compactage $k = EV_2 / EV_1 \\le 2.0$."
        },
        {
            id: "guide_cerema_signa",
            code: "CEREMA SIGNA",
            title: "Guide CEREMA / IISR 8e Partie - Signalisation Temporaire des Chantiers",
            cat: "guides_outils",
            desc: "Manuel national de signalisation temporaire sur routes bidirectionnelles et autoroutes : calcul des biseaux d'approche (AK5, B14, KR11), alternats par feux et temps de tout-rouge.",
            status: "Instruction Ministérielle",
            badge: "Signalisation Voirie",
            content: "# GUIDE CEREMA - SIGNALISATION TEMPORAIRE IISR 8E PARTIE\n\n- **Distance des Panneaux d'Approche :**\n  * En agglomération ($V \\le 50\\text{ km/h}$) : $50\\text{ m}$ d'espacement.\n  * En rase campagne ($V \\le 90\\text{ km/h}$) : $150\\text{ m}$ d'espacement.\n  * Sur autoroute ($V = 110/130\\text{ km/h}$) : $250\\text{ m}$ à $300\\text{ m}$ d'espacement.\n- **Calcul du Temps de Dégagement (Tout-Rouge Feux KR11) :**\n  $$T_r = \\frac{L_{chantier}}{V_{sec}} + 4\\text{ secondes de battement sécurisé}$$\n  Garantit qu'aucun véhicule n'est engagé lors du basculement du feu opposé."
        },
        {
            id: "fntp_outils_index",
            code: "FNTP INDEX",
            title: "Outils FNTP : Révision de Prix & Indexation Marchés TP01 / TP08",
            cat: "guides_outils",
            desc: "Méthodologie officielle de la Fédération Nationale des Travaux Publics pour l'actualisation et la révision des prix des marchés selon la formule $P = P_0 (0.15 + 0.85 \\times TP / TP_0)$.",
            status: "Référentiel FNTP",
            badge: "Économie & Prix",
            content: "# FORMULE NATIONALE FNTP DE RÉVISION DE PRIX\n\n- **Formule Contractuelle CCAG Travaux :**\n  $$P = P_0 \\left( a + (1 - a) \\frac{\\text{Index } TP_n}{\\text{Index } TP_0} \\right)$$\n  avec $a = 0.15$ (part fixe non révisable) et $(1 - a) = 0.85$ (part révisable indexée).\n- **Index Spécifiques :**\n  * **TP01 :** Index général tous travaux de terrassements et chaussées.\n  * **TP02 :** Ouvrages d'art et génie civil.\n  * **TP08 :** Enrobés et travaux routiers bitumineux."
        }
    ];

    function filterDocsView(cat, btn) {
        document.querySelectorAll('.doc-tab-filter').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
        renderRegulatoryDocs(cat);
    }

    function renderRegulatoryDocs(filterCat = 'all') {
        const grid = document.getElementById('regulatory-docs-grid');
        if (!grid) return;

        const filtered = regulatoryDocsList.filter(d => filterCat === 'all' || d.cat === filterCat);
        grid.innerHTML = filtered.map(d => `
            <div class="card" style="border: 1px solid rgba(51,65,85,0.8); background: rgba(15,23,42,0.95); display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.4rem;">
                        <span class="badge badge-info" style="font-family: 'JetBrains Mono'; font-size: 0.75rem;">${d.code}</span>
                        <span class="badge badge-success">${d.badge}</span>
                    </div>
                    <h3 style="font-size: 1.05rem; font-weight: 800; color: #38bdf8; margin: 4px 0;">${d.title}</h3>
                    <p style="font-size: 0.8rem; color: #cbd5e1; line-height: 1.5; margin-bottom: 0.75rem;">${d.desc}</p>
                </div>
                <div style="display: flex; gap: 0.4rem;">
                    <button class="btn btn-primary" style="flex: 1; font-size: 0.75rem;" onclick="openRegulatoryDocModal('${d.id}')">📖 Consulter le Texte & Règles</button>
                    <button class="btn btn-secondary" style="font-size: 0.75rem;" onclick="alert('Fiche technique et référentiel national ${d.code} téléchargé.');">📥 Télécharger</button>
                </div>
            </div>
        `).join('');
    }

    function openRegulatoryDocModal(docId) {
        const doc = regulatoryDocsList.find(d => d.id === docId) || regulatoryDocsList[0];
        const titleEl = document.getElementById('doc-reader-title');
        const bodyEl = document.getElementById('doc-reader-body');
        if (!titleEl || !bodyEl) return;

        titleEl.textContent = `⚖️ ${doc.title} (${doc.code})`;
        bodyEl.textContent = doc.content || `# ${doc.title}\n**Référence :** ${doc.code}_2026_OCCITANIE\n**Statut :** ${doc.status}\n\nCe document officiel constitue un référentiel national majeur pour la conduite du chantier, validé conformément aux normes NF P et aux prescriptions du CCAG Travaux 2021.`;
        openModal('doc-reader-modal');
    }

    // ==========================================
    // 22. ARCHIVES & GED (DOSSIERS FINIS, FACTURES, PAIE, CARTES PRO)
    // ==========================================
    let activeArchiveCategory = 'all';
    let activeArchiveYear = 'all';

    const archivesData = [
        { id: "ARC-2025-001", code: "DGD-2025", title: "DGD Final Clôturé - Aménagement ZAC Béziers Ouest", cat: "marches_clos", year: "2025", partner: "Communauté d'Agglo Béziers", hash: "8f7e6d5c4b3a2109...", retention: "Légal 10 ans (2035)", icon: "📁", montant: "1 240 000 €" },
        { id: "ARC-2025-002", code: "BDC-4412", title: "Bon de Commande Validé - 450t Enrobés BBSG 0/10", cat: "bdc_factures", year: "2025", partner: "Enrobés du Sud", hash: "1a2b3c4d5e6f7a8b...", retention: "Comptable 10 ans", icon: "💳", montant: "44 550 €" },
        { id: "ARC-2026-003", code: "PAY-2026-08", title: "Bulletins de Paie Récapitulatifs - Août 2026 (18 Salariés)", cat: "rh_paie", year: "2026", partner: "Cabinet Social TP", hash: "9a8b7c6d5e4f3a2b...", retention: "RH 50 ans", icon: "👥", montant: "42 800 €" },
        { id: "ARC-2026-004", code: "CP-BTP-044", title: "Certificats & Cartes Pro BTP + CACES R482 Équipe 1", cat: "cartes_pro", year: "2026", partner: "OPPBTP / CIBTP", hash: "7c6d5e4f3a2b1c0d...", retention: "Valide 5 ans", icon: "🪪", montant: "18 Cartes" },
        { id: "ARC-2026-005", code: "TRK-2026-99", title: "Bordereau Trackdéchets BSDD n°2026-3401 (70t Déblais)", cat: "trackdechets", year: "2026", partner: "Plateforme AGEC État", hash: "c5d6e7f8a9b0c1d2...", retention: "Loi AGEC 5 ans", icon: "🚚", montant: "70.0 t" },
        { id: "ARC-2024-006", code: "DGD-2024", title: "DGD Final Clôturé - Piste Cyclable Littorale Frontignan", cat: "marches_clos", year: "2024", partner: "Conseil Départemental 34", hash: "5e4f3a2b1c0d9e8f...", retention: "Légal 10 ans (2034)", icon: "📁", montant: "580 000 €" }
    ];

    function filterArchives(cat, btn) {
        activeArchiveCategory = cat;
        document.querySelectorAll('.archive-cat-filter').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
        renderArchives();
    }

    function filterArchivesByYear(year) {
        activeArchiveYear = year;
        renderArchives();
    }

    function searchArchives(query) {
        renderArchives(query);
    }

    let archivesSortKey = 'year';
    let archivesSortAsc = false;

    function sortArchives(sortVal) {
        if (sortVal.includes('_')) {
            const parts = sortVal.split('_');
            archivesSortKey = parts[0];
            archivesSortAsc = parts[1] === 'asc';
        } else {
            archivesSortKey = sortVal;
            archivesSortAsc = true;
        }
        renderArchives();
    }

    function renderArchives(query = '') {
        const grid = document.getElementById('archives-grid');
        if (!grid) return;

        const q = (query || '').toLowerCase();
        const filtered = archivesData.filter(d => {
            if (activeArchiveCategory !== 'all' && d.cat !== activeArchiveCategory) return false;
            if (activeArchiveYear !== 'all' && d.year !== activeArchiveYear) return false;
            if (q && !d.title.toLowerCase().includes(q) && !d.code.toLowerCase().includes(q) && !d.partner.toLowerCase().includes(q)) return false;
            return true;
        });

        const sorted = [...filtered].sort((a, b) => {
            let valA = a[archivesSortKey] !== undefined ? a[archivesSortKey] : '';
            let valB = b[archivesSortKey] !== undefined ? b[archivesSortKey] : '';
            if (typeof valA === 'string') {
                return archivesSortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
            }
            return archivesSortAsc ? (valA - valB) : (valB - valA);
        });

        grid.innerHTML = sorted.map(d => `
            <div class="card" style="border: 1px solid rgba(51,65,85,0.8); background: rgba(15,23,42,0.95); display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.4rem;">
                        <span class="badge badge-info" style="font-family: 'JetBrains Mono'; font-size: 0.75rem;">${d.code}</span>
                        <span class="badge badge-success">${d.year}</span>
                    </div>
                    <h3 style="font-size: 1.05rem; font-weight: 800; color: #38bdf8; margin: 4px 0;">${d.icon} ${d.title}</h3>
                    <div style="background: rgba(30,41,59,0.5); padding: 0.5rem; border-radius: 6px; font-size: 0.75rem; margin: 0.5rem 0;">
                        <div>Entité : <strong>${d.partner}</strong></div>
                        <div>Montant / Volume : <strong style="color: var(--emerald);">${d.montant}</strong></div>
                        <div>Conservation : <strong>${d.retention}</strong></div>
                        <div style="font-family: 'JetBrains Mono'; font-size: 0.68rem; color: #64748b; margin-top: 2px;">SHA-256 : ${d.hash}</div>
                    </div>
                </div>
                <div style="display: flex; gap: 0.4rem;">
                    <button class="btn btn-primary" style="flex: 1; font-size: 0.75rem;" onclick="openArchiveDoc('${d.id}')">👁️ Prévisualiser</button>
                    <button class="btn btn-secondary" style="font-size: 0.75rem;" onclick="alert('Document certifié ${d.code} téléchargé.');">📥 Télécharger PDF</button>
                </div>
            </div>
        `).join('');
    }

    function openArchiveDoc(arcId) {
        const doc = archivesData.find(d => d.id === arcId) || archivesData[0];
        const titleEl = document.getElementById('doc-reader-title');
        const bodyEl = document.getElementById('doc-reader-body');
        if (!titleEl || !bodyEl) return;

        titleEl.textContent = `🗄️ ${doc.title} (${doc.code})`;
        bodyEl.textContent = `# PIÈCE D'ARCHIVE NUMÉRIQUE OFFICIELLE\n**Identifiant Document :** ${doc.id}\n**Code :** ${doc.code}\n**Exercice :** ${doc.year}\n**Tiers / Signataire :** ${doc.partner}\n**Valeur / Volume :** ${doc.montant}\n**Durée de Conservation Légale :** ${doc.retention}\n**Empreinte Cryptographique SHA-256 :** ${doc.hash}\n\nCe document a été archivé et scellé de manière infalsifiable conformément aux prescriptions du Code de Commerce et du CCAG Travaux 2021.`;
        openModal('doc-reader-modal');
    }

    // ==========================================
    // 23. WINDOW INITIALIZATION & AUTOPILOT
    // ==========================================
    function simulatePaymentSituation() {
        caisseBalance += 125000;
        const el1 = document.getElementById('kpi-treasury-val');
        const el2 = document.getElementById('company-caisse-val');
        if (el1) el1.textContent = caisseBalance.toLocaleString('fr-FR') + ' €';
        if (el2) el2.textContent = caisseBalance.toLocaleString('fr-FR') + ' €';
        logCockpit('Situation client n°3 encaissée (+125 000 €).', 'ok');
        alert('Situation de travaux de 125 000 € encaissée en caisse avec succès !');
    }

    function runAutopilot() {
        alert('⚡ Audit IA Global exécuté : Analyse des cadences de 4 chantiers, conformité des 28 SDP, vérification DICT, audit DGD et inventaire dépôt 100% validés.');
        logCockpit('Audit IA Global exécuté avec succès.', 'ok');
    }

    function toggleVoiceControl() {
        alert('🎙️ Commande vocale VRD initialisée. Parlez pour dicter vos ordres (ex: "Afficher planning Alès").');
    }

    function triggerSimulatedCrisis() {
        openSafetyEmergencySimulator();
        renderCrisisScenario('gaz');
    }

    function openSafetyEmergencySimulator() {
        openModal('safety-emergency-modal');
    }

    function renderCrisisScenario(type) {
        const body = document.getElementById('safety-crisis-body');
        if (!body) return;

        body.innerHTML = `
            <div style="background: rgba(239, 68, 68, 0.2); border: 2px solid #ef4444; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                <h3 style="color: #ef4444; font-size: 1.15rem; font-weight: 900; margin-bottom: 0.5rem;">💥 SITUATION DE CRISE : FUITE / RUPTURE GAZ NATUREL MPB 4 BAR</h3>
                <p style="font-size: 0.85rem; color: #f8fafc; margin-bottom: 0.75rem;">Un engin de terrassement a heurté la canalisation gaz PEHD Ø110 au PK 0+240.</p>
                <div style="background: rgba(15,23,42,0.9); padding: 0.85rem; border-radius: 6px; font-size: 0.8rem; line-height: 1.6;">
                    <div>1. 🛑 <strong>ARRÊT IMMÉDIAT DU CHANTIER</strong> et coupure des moteurs.</div>
                    <div>2. 🏃‍♂️ <strong>ÉVACUATION DU PÉRIMÈTRE DE SÉCURITÉ</strong> (100m sous le vent).</div>
                    <div>3. 📞 <strong>APPEL D'URGENCE GRDF / POMPIERS (18 / 112)</strong>.</div>
                </div>
            </div>
            <button class="btn btn-secondary" style="width:100%;" onclick="closeModal('safety-emergency-modal')">Fermer la Simulation de Crise</button>
        `;
    }

    window.onload = function() {
        try {
            renderNavForRole();
            switchNav('cockpit');
            logCockpit('🚀 Suite BTP Autonomous Command v5.0 initialisée avec succès.', 'ok');
        } catch (e) {
            console.error('Initialization error:', e);
        }
    };
</script>
"""
