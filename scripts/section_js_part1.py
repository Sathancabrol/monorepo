def get_js_part1():
    return """
<script>
    // ==========================================
    // 1. DATASETS INJECTION & ROBUST NORMALIZATION
    // ==========================================
    const rawInventoryData = __INVENTORY_JSON__;
    const rawSyntheseData = __SYNTHESE_JSON__;
    const rawConfrontationData = __CONFRONTATION_JSON__;
    const rawLedgerData = __LEDGER_JSON__;
    const rawReportsData = __REPORTS_JSON__;
    const rawObsidianData = __OBSIDIAN_JSON__;
    const rawCompanyData = __EXTRA_DATA_JSON__;

    const inventoryData = rawInventoryData || {};
    const syntheseData = rawSyntheseData || { dqe_items: [] };
    const confrontationData = rawConfrontationData || {};
    const ledgerData = Array.isArray(rawLedgerData) ? { blocks: rawLedgerData } : (rawLedgerData || { blocks: [] });
    const reportsData = rawReportsData || { rdc_entries: [] };
    const obsidianData = rawObsidianData || { nodes: [], links: [] };
    const companyData = rawCompanyData || {};

    // Normalize projects
    companyData.projects = (companyData.projects || []).map(p => ({
        id: p.id || 'PRJ_01',
        name: p.name || 'Projet BTP',
        client: p.client || 'Maître d\\'Ouvrage Public',
        location: p.location || 'Occitanie (34)',
        budget: Number(p.budget_total || p.budget || 500000),
        progress: Number(p.avancement_physique_pct || p.progress || 50),
        status: p.statut || p.status || 'En cours',
        manager: p.conducteur || p.manager || 'Sylvain CABROL',
        site_chief: p.chef_chantier || p.site_chief || 'Alain MARTIN',
        start: p.date_debut || p.start || '2026-05-15',
        end: p.date_fin_prevue || p.end || '2026-10-30',
        lots: p.lots || [
            { lot: '01', name: 'Terrassement & Déblais', budget: (p.budget_total || 500000) * 0.25, progress: p.avancement_physique_pct || 75, status: 'En cours' },
            { lot: '02', name: 'Assainissement EU/EP', budget: (p.budget_total || 500000) * 0.35, progress: Math.min(100, Math.round((p.avancement_physique_pct || 75) * 0.9)), status: 'En cours' },
            { lot: '03', name: 'Réseaux Secs & Élec', budget: (p.budget_total || 500000) * 0.2, progress: Math.min(100, Math.round((p.avancement_physique_pct || 75) * 0.7)), status: 'En cours' },
            { lot: '04', name: 'Voirie & Enrobés', budget: (p.budget_total || 500000) * 0.2, progress: Math.min(100, Math.round((p.avancement_physique_pct || 75) * 0.4)), status: 'Préparation' }
        ],
        docs: [
            { name: 'CCTP_Voirie_Réseaux', type: 'pdf' },
            { name: 'BPU_DQE_Signé', type: 'pdf' },
            { name: 'Plan_Implantation_DAO', type: 'dwg' },
            { name: 'DICT_Récépissés_Valides', type: 'pdf' },
            { name: 'PGCSPS_Sécurité', type: 'pdf' }
        ]
    }));

    // Normalize fleet
    companyData.fleet = (companyData.fleet || []).map(f => ({
        id: f.id || 'EQ_01',
        name: f.name || 'Engin Chantier',
        type: f.type || 'Engin TP',
        category: f.category || 'excavator',
        status: f.status || f.statut || 'En opération',
        assigned: f.current_project ? f.current_project.replace('projet_', '').toUpperCase() : (f.assigned || 'ZAC des Pins'),
        operator: f.operator || 'M. Lopez',
        hours: Number(f.horametre || f.hours || 1850),
        vgp: f.vgp_date || f.vgp || '2026-11-15',
        caces: f.caces_req || f.caces || 'CACES R482 Cat B1'
    }));

    // Normalize catalog (merge tools + materials)
    const rawCatalog = [
        ...(companyData.materials_catalog || []),
        ...(companyData.tool_catalog || []),
        ...(companyData.catalog || [])
    ];

    if (rawCatalog.length === 0) {
        companyData.catalog = [
            { id: 'mat_01', name: 'Bordures Béton Type T2 (100x20x28 cm)', category: 'materials', supplier: 'Bétons Occitanie', unit_price: 14.50, unit: 'ml', stock: 450, norm: 'NF EN 1340' },
            { id: 'mat_02', name: 'Tampon Fonte Ductile D400 PAM REXEL Ø600', category: 'materials', supplier: 'Saint-Gobain PAM', unit_price: 145.00, unit: 'u', stock: 28, norm: 'NF EN 124 / 400 kN' },
            { id: 'mat_03', name: 'Tuyau Fonte Ductile DN400 Integral (6m)', category: 'materials', supplier: 'Saint-Gobain PAM', unit_price: 115.00, unit: 'ml', stock: 180, norm: 'Fascicule 70-1' },
            { id: 'mat_04', name: 'Grave Non Traitée GNT 0/31.5 Classe A', category: 'materials', supplier: 'Carrières Languedoc', unit_price: 16.50, unit: 'tonne', stock: 1250, norm: 'NF EN 13285' },
            { id: 'tool_01', name: 'Laser Canalisateur Piper 200 Automatique', category: 'tools', supplier: 'Leica Geosystems', unit_price: 45.00, unit: 'jour', stock: 3, norm: 'Précision ±1.5mm' },
            { id: 'tool_02', name: 'Découpeuse Béton Thermique Stihl TS800', category: 'tools', supplier: 'Stihl Pro BTP', unit_price: 35.00, unit: 'jour', stock: 6, norm: 'Disque Ø400 Diamant' },
            { id: 'tool_03', name: 'Pénétromètre Dynamique Léger PANDA', category: 'tools', supplier: 'Sol Solution TP', unit_price: 80.00, unit: 'jour', stock: 2, norm: 'Norme NF P 94-105' },
            { id: 'epi_01', name: 'Pack EPI Haute Visibilité & Casque Réfléchissant', category: 'safety', supplier: 'Protect BTP', unit_price: 85.00, unit: 'kit', stock: 45, norm: 'Classe 3 EN 20471' }
        ];
    } else {
        companyData.catalog = rawCatalog.map((c, idx) => ({
            id: c.id || `mat_${idx + 1}`,
            name: c.name || 'Article BTP',
            category: (c.category && c.category.includes('Engin')) ? 'tools' : (c.category || 'materials'),
            supplier: c.fournisseur || c.supplier || 'Fournisseur Agréé TP',
            unit_price: Number(c.prix_unitaire || (parseFloat((c.tarif_location_jour || '45').replace(/[^0-9.]/g, '')) || 45)),
            unit: c.unit || (c.tarif_location_jour ? 'jour' : 'u'),
            stock: c.stock ? (parseInt(c.stock) || 50) : 50,
            norm: c.norme || c.caces || 'NF EN 1340 / CE'
        }));
    }

    // Normalize suppliers
    if (!companyData.suppliers || companyData.suppliers.length === 0) {
        companyData.suppliers = [
            { id: 'sup_01', name: 'Carrières & Granulats du Languedoc', specialty: 'Grave GNT 0/31.5, Gravillons 4/10', location: 'Frontignan (34)', distance_km: 14, quality_rating: 4.8 },
            { id: 'sup_02', name: 'Bétons Occitanie Méditerranée', specialty: 'Bétons Prêts à l\\'Emploi C25/30 XF1', location: 'Sète / ZI Eaux Blanches', distance_km: 6, quality_rating: 4.9 },
            { id: 'sup_03', name: 'Saint-Gobain PAM Canalisation', specialty: 'Tuyaux Fonte DN400, Tampons D400', location: 'Montpellier / Vendargues', distance_km: 28, quality_rating: 5.0 },
            { id: 'sup_04', name: 'PUM Plastiques Sète', specialty: 'Tubes PVC CR8 Ø200, PEHD Gaz', location: 'Sète / Zone d\\'Activité', distance_km: 4, quality_rating: 4.7 },
            { id: 'sup_05', name: 'Enrobés Bitumineux du Sud (Alès)', specialty: 'Enrobé BBSG 0/10 Classe 3', location: 'Alès / Gard', distance_km: 18, quality_rating: 4.8 }
        ];
    }

    // Normalize HR hierarchy
    companyData.hr_hierarchy = {
        director: { name: "Laurent VIALA", role: "Directeur Général / Gérant TP", cert: "AIPR Concepteur • Ingénieur ESTP" },
        conducteurs: [
            {
                name: "Sylvain CABROL",
                role: "Conducteur de Travaux Principal VRD",
                assigned: ["Giratoire RD906 Alès", "ZAC Littoral Sète"],
                chefs: [
                    { name: "Alain MARTIN", site: "Giratoire RD906 Alès", workers: ["M. Lopez (Pelle 24t)", "R. Garcia (Chargeur)", "P. Durand (Maçon VRD)", "T. Faure (Manoeuvre)"] },
                    { name: "Marc GOMEZ", site: "ZAC Littoral Sète", workers: ["D. Blanc (Mecalac)", "P. Mercier (8x4)", "K. Benali (Canalisateur)", "A. Traoré (Poseur)"] }
                ]
            },
            {
                name: "Sophie LACOMBE",
                role: "Conductrice de Travaux VRD & Aménagements",
                assigned: ["Centre Ancien Pézenas", "Voie Verte Montpellier"],
                chefs: [
                    { name: "Karim BENALI", site: "Centre Ancien Pézenas", workers: ["S. Petit (Minipelle)", "T. Vidal (Hydrocureur)", "N. Roux (Paveur)", "J. Fabre (Manoeuvre)"] },
                    { name: "David LEMOINE", site: "Voie Verte Montpellier", workers: ["F. Dumas (Compacteur)", "M. Giraud (Régleur Enrobé)", "L. Morin (Applicateur)"] }
                ]
            }
        ]
    };

    // RDC entries
    if (!reportsData.rdc_entries || reportsData.rdc_entries.length === 0) {
        reportsData.rdc_entries = [
            { id: 'RDC-0892', project: 'Giratoire RD906 Alès', date: '2026-09-18', chief: 'A. Martin', weather: 'Ensoleillé (24°C)', notes: 'Pose de 85 ml de bordures T2 et calage béton. Aucun aléa.', hours_mo: 35, hours_engins: 14 },
            { id: 'RDC-0891', project: 'ZAC Littoral Sète', date: '2026-09-18', chief: 'M. Gomez', weather: 'Vent modéré (21°C)', notes: 'Blindage tranchée profonde 3.20m et pose 36 ml fonte DN400.', hours_mo: 42, hours_engins: 16 },
            { id: 'RDC-0890', project: 'Centre Ancien Pézenas', date: '2026-09-17', chief: 'S. Lacombe', weather: 'Ensoleillé (25°C)', notes: 'Épreuves de pression collecteur PVC et remblaiement soigné.', hours_mo: 28, hours_engins: 7 }
        ];
    }

    // GLOBAL APP STATE
    let currentPerspective = 'patron';
    let currentNav = 'cockpit';
    let caisseBalance = 485200;
    let planningViewMode = 'agenda_week';
    let currentAgendaWeekOffset = 0;
    let simulatorViewMode = 'radar';
    let isRadarLive = true;
    let currentScenarioId = 'scen_tranchee_vrd';
    let activeScenarioStepIdx = 0;
    let fleetFilter = 'all';
    let catalogFilter = 'all';
    let obsidianHeuristic = 'all';
    let sdpViewMode = 'dqe_tcd';
    let radarCanvas, radarCtx, radarAnimId;
    let cameraRotX = 30, cameraRotY = -45, cameraZoom = 1.0;
    let isDragging3D = false, lastMouseX = 0, lastMouseY = 0;

    // ==========================================
    // 2. TECHNICAL SVG VECTOR ILLUSTRATIONS ENGINE
    // ==========================================
    function getVehicleSVG(typeStr, nameStr) {
        const t = (typeStr + ' ' + (nameStr || '')).toLowerCase();
        if (t.includes('pelle') || t.includes('excavat') || t.includes('cat') || t.includes('liebherr') || t.includes('mecalac') || t.includes('kubota')) {
            return `<svg viewBox="0 0 300 160" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
                <line x1="10" y1="145" x2="290" y2="145" stroke="#334155" stroke-width="2"/>
                <rect x="40" y="115" width="130" height="28" rx="14" fill="#334155" stroke="#0f172a" stroke-width="2"/>
                <circle cx="55" cy="129" r="10" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
                <circle cx="85" cy="129" r="10" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
                <circle cx="115" cy="129" r="10" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
                <circle cx="145" cy="129" r="10" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
                <rect x="50" y="85" width="95" height="32" rx="5" fill="#f59e0b" stroke="#b45309" stroke-width="2"/>
                <path d="M 110 55 L 140 55 L 140 85 L 110 85 Z" fill="#0284c7" fill-opacity="0.7" stroke="#d97706" stroke-width="2"/>
                <path d="M 135 90 L 190 35 L 205 45 L 145 100 Z" fill="#f59e0b" stroke="#b45309" stroke-width="2"/>
                <path d="M 195 40 L 245 95 L 235 102 L 188 47 Z" fill="#f59e0b" stroke="#b45309" stroke-width="2"/>
                <path d="M 240 98 L 270 115 L 260 140 L 232 132 Z" fill="#334155" stroke="#1e293b" stroke-width="2"/>
                <circle cx="118" cy="50" r="3" fill="#ef4444"/>
                <text x="60" y="105" fill="#1e293b" font-family="system-ui" font-weight="900" font-size="10">PELLE HYDRAULIQUE</text>
                <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Pelle Chenilles / Pneus TP</text>
            </svg>`;
        } else if (t.includes('cylindre') || t.includes('compacteur') || t.includes('bomag')) {
            return `<svg viewBox="0 0 300 160" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
                <line x1="10" y1="145" x2="290" y2="145" stroke="#334155" stroke-width="2"/>
                <circle cx="75" cy="115" r="28" fill="#475569" stroke="#0f172a" stroke-width="3"/>
                <circle cx="215" cy="115" r="28" fill="#475569" stroke="#0f172a" stroke-width="3"/>
                <rect x="145" y="75" width="85" height="30" rx="4" fill="#facc15" stroke="#a16207" stroke-width="2"/>
                <rect x="105" y="60" width="40" height="40" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>
                <rect x="100" y="32" width="60" height="5" rx="2" fill="#ca8a04"/>
                <circle cx="130" cy="28" r="3" fill="#f97316"/>
                <text x="150" y="95" fill="#1e293b" font-family="system-ui" font-weight="900" font-size="10">COMPACTEUR</text>
                <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Compacteur Tandem Vibrant V5</text>
            </svg>`;
        } else if (t.includes('camion') || t.includes('8x4') || t.includes('scania') || t.includes('volvo') || t.includes('porteur') || t.includes('hydrocureur')) {
            return `<svg viewBox="0 0 300 160" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
                <line x1="10" y1="145" x2="290" y2="145" stroke="#334155" stroke-width="2"/>
                <rect x="30" y="115" width="235" height="10" fill="#1e293b"/>
                <circle cx="50" cy="130" r="14" fill="#0f172a" stroke="#475569" stroke-width="3"/>
                <circle cx="90" cy="130" r="14" fill="#0f172a" stroke="#475569" stroke-width="3"/>
                <circle cx="195" cy="130" r="14" fill="#0f172a" stroke="#475569" stroke-width="3"/>
                <circle cx="235" cy="130" r="14" fill="#0f172a" stroke="#475569" stroke-width="3"/>
                <path d="M 30 115 L 30 65 L 70 60 L 85 85 L 85 115 Z" fill="#0284c7" stroke="#075985" stroke-width="2"/>
                <path d="M 90 80 L 255 65 L 260 115 L 90 115 Z" fill="#94a3b8" stroke="#475569" stroke-width="2"/>
                <circle cx="55" cy="57" r="3" fill="#f97316"/>
                <text x="115" y="100" fill="#0f172a" font-family="system-ui" font-weight="900" font-size="10">PORTEUR TP 32T</text>
                <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Camion Bi-Benne / Citerne 8x4</text>
            </svg>`;
        } else {
            return `<svg viewBox="0 0 300 160" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
                <line x1="10" y1="145" x2="290" y2="145" stroke="#334155" stroke-width="2"/>
                <rect x="60" y="75" width="180" height="45" rx="6" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
                <circle cx="100" cy="130" r="14" fill="#0f172a" stroke="#94a3b8" stroke-width="3"/>
                <circle cx="200" cy="130" r="14" fill="#0f172a" stroke="#94a3b8" stroke-width="3"/>
                <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Matériel Professionnel TP</text>
            </svg>`;
        }
    }

    function getToolMaterialSVG(itemId, itemName) {
        const id = (itemId + ' ' + (itemName || '')).toLowerCase();
        if (id.includes('bordure') || id.includes('mat_01') || id.includes('mat_02')) {
            return `<svg viewBox="0 0 260 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
                <polygon points="40,95 170,95 220,50 90,50" fill="#94a3b8" stroke="#cbd5e1" stroke-width="2"/>
                <polygon points="40,95 170,95 170,125 40,125" fill="#64748b" stroke="#334155" stroke-width="2"/>
                <polygon points="170,95 220,50 220,80 170,125" fill="#475569" stroke="#1e293b" stroke-width="2"/>
                <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Bordure Béton T2 / A2 NF</text>
            </svg>`;
        } else if (id.includes('tampon') || id.includes('fonte') || id.includes('mat_03') || id.includes('mat_04')) {
            return `<svg viewBox="0 0 260 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
                <rect x="45" y="15" width="170" height="110" rx="8" fill="#1e293b" stroke="#475569" stroke-width="2"/>
                <circle cx="130" cy="70" r="42" fill="#0f172a" stroke="#94a3b8" stroke-width="3"/>
                <text x="112" y="74" fill="#facc15" font-family="system-ui" font-weight="900" font-size="10">D 400</text>
                <text x="15" y="15" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Tampon Fonte D400 PAM</text>
            </svg>`;
        } else if (id.includes('tuyau') || id.includes('mat_05') || id.includes('mat_06')) {
            return `<svg viewBox="0 0 260 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
                <rect x="50" y="45" width="170" height="45" rx="4" fill="#334155" stroke="#0284c7" stroke-width="2"/>
                <rect x="25" y="38" width="30" height="58" rx="5" fill="#1e293b" stroke="#0284c7" stroke-width="2"/>
                <text x="70" y="72" fill="#38bdf8" font-family="JetBrains Mono" font-size="10" font-weight="800">FONTE DN 400</text>
                <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Tuyau Assainissement</text>
            </svg>`;
        } else if (id.includes('laser') || id.includes('piper')) {
            return `<svg viewBox="0 0 260 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
                <rect x="35" y="45" width="120" height="45" rx="8" fill="#dc2626" stroke="#991b1b" stroke-width="2"/>
                <circle cx="155" cy="67" r="22" fill="#1e293b" stroke="#dc2626" stroke-width="2"/>
                <circle cx="155" cy="67" r="7" fill="#10b981"/>
                <line x1="160" y1="67" x2="240" y2="67" stroke="#10b981" stroke-width="2"/>
                <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Laser Canalisateur Piper</text>
            </svg>`;
        } else if (id.includes('scie') || id.includes('stihl')) {
            return `<svg viewBox="0 0 260 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
                <rect x="40" y="55" width="80" height="35" rx="5" fill="#ea580c" stroke="#c2410c" stroke-width="2"/>
                <circle cx="175" cy="72" r="35" fill="#475569" stroke="#94a3b8" stroke-width="2"/>
                <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Découpeuse Diamant Stihl</text>
            </svg>`;
        } else {
            return `<svg viewBox="0 0 260 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
                <rect x="40" y="40" width="180" height="60" rx="6" fill="#1e293b" stroke="#06b6d4" stroke-width="2"/>
                <circle cx="130" cy="70" r="18" fill="#06b6d4" fill-opacity="0.2"/>
                <text x="130" y="75" fill="#f8fafc" font-size="14" text-anchor="middle">📦</text>
                <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Fourniture / Outil TP</text>
            </svg>`;
        }
    }

    // ==========================================
    // 3. LOG & TERMINAL
    // ==========================================
    function logCockpit(msg, type = 'info') {
        const term = document.getElementById('cockpit-terminal');
        if (!term) return;
        const now = new Date().toLocaleTimeString('fr-FR');
        const color = type === 'ok' ? 'var(--emerald)' : (type === 'warn' ? 'var(--amber)' : (type === 'alert' ? 'var(--rose)' : 'var(--cyan)'));
        const el = document.createElement('div');
        el.innerHTML = `<span style="color:#64748b;">[${now}]</span> <span style="color:${color}; font-weight:700;">●</span> ${msg}`;
        term.appendChild(el);
        term.scrollTop = term.scrollHeight;
    }

    // ==========================================
    // 4. ROLES & NAVIGATION DOCK
    // ==========================================
    const roleTabs = {
        'patron': [
            { id: 'cockpit', label: '🎛️ Cockpit' },
            { id: 'company', label: '🏢 Entreprise & Caisse' },
            { id: 'projects_hub', label: '📁 Chantiers & Docs' },
            { id: 'planning', label: '📅 Planning Gantt & Agenda' },
            { id: 'simulator', label: '🛰️ Watch Tower 3D' },
            { id: 'fleet', label: '🚜 Flotte Engins' },
            { id: 'catalog', label: '🛒 Outils & Matériaux' },
            { id: 'hr', label: '👷 Organigramme RH' },
            { id: 'opbtp', label: '🦺 Signalétique OPBTP' },
            { id: 'safety', label: '🛡️ Sécurité AIPR' },
            { id: 'rdc', label: '📋 Rapport RDC' },
            { id: 'sdp', label: '💰 28 SDP & TCD DQE' },
            { id: 'obsidian', label: '🕸️ Graphe Obsidian' },
            { id: 'schemas', label: '📐 Schémas A-Z' },
            { id: 'procurement', label: '🛒 Fournisseurs' },
            { id: 'ledger', label: '⛓️ Ledger SHA-256' },
            { id: 'docs', label: '📚 Rapports CCTP' }
        ],
        'conduite': [
            { id: 'cockpit', label: '🎛️ Cockpit' },
            { id: 'projects_hub', label: '📁 Chantiers en Cours' },
            { id: 'planning', label: '📅 Planning & Agenda' },
            { id: 'simulator', label: '🛰️ Watch Tower' },
            { id: 'fleet', label: '🚜 Flotte & Dispatch' },
            { id: 'catalog', label: '🛒 Commandes Matériaux' },
            { id: 'opbtp', label: '🦺 Signalétique OPBTP' },
            { id: 'safety', label: '🛡️ Sécurité & AIPR' },
            { id: 'rdc', label: '📋 Journal RDC' },
            { id: 'sdp', label: '💰 Sous-Détails & DQE' },
            { id: 'procurement', label: '🛒 Fournisseurs' }
        ],
        'compagnon': [
            { id: 'compagnon_mobile', label: '📱 Mode Terrain Mobile' },
            { id: 'opbtp', label: '🦺 Balisage OPBTP' },
            { id: 'safety', label: '🛡️ Règles Sécurité' },
            { id: 'rdc', label: '📋 Saisie RDC' }
        ]
    };

    function switchPerspective(roleId, btn) {
        currentPerspective = roleId;
        document.querySelectorAll('.perspective-btn').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');

        renderNavForRole();
        const available = roleTabs[roleId] || roleTabs['patron'];
        switchNav(available[0].id);
        logCockpit(`Bascule vers la perspective : ${roleId.toUpperCase()}`, 'info');
    }

    function renderNavForRole() {
        const dock = document.getElementById('main-nav-dock');
        if (!dock) return;
        const tabs = roleTabs[currentPerspective] || roleTabs['patron'];
        dock.innerHTML = tabs.map(t => `
            <button class="nav-item ${t.id === currentNav ? 'active' : ''}" onclick="switchNav('${t.id}', this)">
                ${t.label}
            </button>
        `).join('');
    }

    function switchNav(tabId, btn) {
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));

        const target = document.getElementById('tab-' + tabId);
        if (target) target.classList.add('active');
        if (btn) btn.classList.add('active');

        currentNav = tabId;

        // Auto-render tab contents on switch
        try {
            if (tabId === 'projects_hub') renderProjectsHub();
            if (tabId === 'planning') {
                if (planningViewMode.startsWith('agenda')) renderPlanningAgenda();
                else renderPlanningGantt();
            }
            if (tabId === 'fleet') renderFleetGrid();
            if (tabId === 'catalog') renderCatalogGrid();
            if (tabId === 'obsidian') setTimeout(initObsidianGraph, 50);
            if (tabId === 'simulator') {
                setTimeout(() => {
                    initWatchtowerRadar();
                    drawStepVisual(activeScenarioStepIdx);
                }, 50);
            }
            if (tabId === 'hr') setTimeout(initHrTree, 50);
            if (tabId === 'sdp') {
                if (sdpViewMode === 'dqe_tcd') renderDQEPivotTable();
                else renderSdpCards();
            }
            if (tabId === 'opbtp') calculateSignage();
            if (tabId === 'rdc') renderRdcTable();
            if (tabId === 'procurement') renderProcurement();
            if (tabId === 'ledger') renderLedger();
        } catch (e) {
            console.error('Error switching tab to ' + tabId + ':', e);
        }
    }

    function scrollNav(offset) {
        const dock = document.getElementById('main-nav-dock');
        if (dock) dock.scrollBy({ left: offset, behavior: 'smooth' });
    }

    // MODALS
    function openModal(id) { document.getElementById(id)?.classList.add('active'); }
    function closeModal(id) { document.getElementById(id)?.classList.remove('active'); }

    // TACTICAL WHEEL
    function toggleTacticalWheel() {
        document.getElementById('tactical-wheel-menu')?.classList.toggle('active');
    }

    function quickAction(actionId) {
        toggleTacticalWheel();
        switchNav(actionId);
    }

    // SIMULATED INSTANT FILE DOWNLOADER
    function downloadProjectDoc(docName, projName, fileType) {
        const content = `=== DOCUMENT OFFICIEL BTP ===\\nChantier : ${projName || 'Travaux Publics'}\\nDocument : ${docName}\\nFormat : ${fileType || 'PDF'}\\nDate de génération : ${new Date().toISOString()}\\nCertification d'intégrité SHA-256 : ${Math.random().toString(36).substring(2)}${Math.random().toString(36).substring(2)}\\n\\nCe fichier est conforme aux prescriptions du CCTP Lot Voirie / Réseaux et aux normes NF/EN applicables.`;
        const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${(projName || 'Chantier').replace(/\\s+/g, '_')}_${docName.replace(/\\s+/g, '_')}.${fileType || 'pdf'}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        logCockpit(`📥 Téléchargement direct initié : ${docName} pour ${projName}.`, 'ok');
    }

    function downloadDoc(docName) {
        downloadProjectDoc(docName, 'Dossier_CCTP_Global', 'md');
    }
"""

def get_js_part1_continued():
    return """
    // ==========================================
    // 5. PROJECTS HUB ENGINE & MODAL
    // ==========================================
    function renderProjectsHub() {
        const grid = document.getElementById('projects-grid');
        if (!grid || !companyData.projects) return;

        grid.innerHTML = companyData.projects.map(p => `
            <div class="card" style="display:flex; flex-direction:column; justify-content:space-between; position:relative; overflow:hidden;">
                <div style="position:absolute; top:0; left:0; width:6px; height:100%; background:${p.status === 'En cours' ? 'var(--emerald)' : (p.status === 'Préparation' ? 'var(--amber)' : 'var(--blue)')};"></div>
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.75rem;">
                        <span class="badge ${p.status === 'En cours' ? 'badge-success' : (p.status === 'Préparation' ? 'badge-warning' : 'badge-info')}">${p.status}</span>
                        <span style="font-family:'JetBrains Mono'; font-weight:700; font-size:1.1rem; color:var(--emerald);">${(p.budget || 500000).toLocaleString()} € HT</span>
                    </div>
                    <h3 style="font-size:1.25rem; font-weight:800; margin-bottom:0.25rem; color:#f8fafc;">${p.name}</h3>
                    <div style="font-size:0.85rem; color:#94a3b8; margin-bottom:1rem;">📍 ${p.location} &nbsp;|&nbsp; 🏢 Client : <strong style="color:#e2e8f0;">${p.client}</strong></div>

                    <div style="margin-bottom:1rem;">
                        <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:0.35rem;">
                            <span style="color:#94a3b8;">Avancement physique</span>
                            <span style="font-family:'JetBrains Mono'; font-weight:700; color:#38bdf8;">${p.progress}%</span>
                        </div>
                        <div class="progress-bar"><div class="progress-fill" style="width:${p.progress}%; background:linear-gradient(90deg, #3b82f6, #06b6d4);"></div></div>
                    </div>

                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; font-size:0.8rem; background:rgba(15,23,42,0.6); padding:0.6rem; border-radius:6px; border:1px solid rgba(51,65,85,0.4); margin-bottom:1rem;">
                        <div><span style="color:#64748b;">Conducteur :</span><br><strong style="color:#f1f5f9;">${p.manager}</strong></div>
                        <div><span style="color:#64748b;">Chef de chantier :</span><br><strong style="color:#f1f5f9;">${p.site_chief || 'Équipe interne'}</strong></div>
                        <div><span style="color:#64748b;">Début :</span><br><span style="font-family:'JetBrains Mono'; color:#cbd5e1;">${p.start}</span></div>
                        <div><span style="color:#64748b;">Fin prév. :</span><br><span style="font-family:'JetBrains Mono'; color:#cbd5e1;">${p.end}</span></div>
                    </div>

                    <div>
                        <div style="font-size:0.75rem; font-weight:700; color:#94a3b8; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.4rem;">Documents d'exécution & CCTP</div>
                        <div style="display:flex; flex-wrap:wrap; gap:0.35rem;">
                            ${(p.docs || []).map(d => `
                                <button class="btn btn-secondary" style="padding:0.25rem 0.6rem; font-size:0.75rem; background:rgba(30,41,59,0.8); border:1px solid rgba(51,65,85,0.7);" onclick="downloadProjectDoc('${d.name.replace(/'/g, "\\\\'")}', '${p.name.replace(/'/g, "\\\\'")}', '${d.type}')">
                                    📄 ${d.name} <span style="opacity:0.6; font-size:0.65rem;">(${d.type.toUpperCase()})</span>
                                </button>
                            `).join('')}
                        </div>
                    </div>
                </div>

                <div style="margin-top:1.25rem; padding-top:0.75rem; border-top:1px solid rgba(51,65,85,0.4); display:flex; gap:0.5rem;">
                    <button class="btn btn-primary" style="flex:1; font-size:0.8rem;" onclick="openProjectModal('${p.id}')">
                        🔍 Fiche Complète & Lots
                    </button>
                    <button class="btn btn-secondary" style="font-size:0.8rem;" onclick="switchNav('planning'); setPlanningProjectFilter('${p.id}');">
                        📅 Planning
                    </button>
                </div>
            </div>
        `).join('');
    }

    function openProjectModal(projectId) {
        const p = (companyData.projects || []).find(x => x.id === projectId) || companyData.projects[0];
        if (!p) return;

        const body = document.getElementById('project-modal-body');
        if (!body) return;

        body.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1.5rem; flex-wrap:wrap; gap:1rem;">
                <div>
                    <span class="badge ${p.status === 'En cours' ? 'badge-success' : 'badge-warning'}">${p.status}</span>
                    <h2 style="font-size:1.75rem; font-weight:900; margin-top:0.35rem; color:#f8fafc;">${p.name}</h2>
                    <p style="color:#94a3b8; font-size:0.9rem;">📍 ${p.location} &nbsp;|&nbsp; Maître d'Ouvrage : <strong style="color:#e2e8f0;">${p.client}</strong></p>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:0.8rem; color:#94a3b8;">Montant du Marché HT</div>
                    <div style="font-size:1.75rem; font-weight:900; color:var(--emerald); font-family:'JetBrains Mono';">${(p.budget || 500000).toLocaleString()} €</div>
                </div>
            </div>

            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:1rem; margin-bottom:1.5rem;">
                <div style="background:rgba(15,23,42,0.8); padding:1rem; border-radius:8px; border:1px solid rgba(51,65,85,0.6);">
                    <div style="font-size:0.75rem; color:#64748b;">CONDUCTEUR DE TRAVAUX</div>
                    <div style="font-weight:700; font-size:1rem; color:#f8fafc; margin-top:0.25rem;">${p.manager}</div>
                </div>
                <div style="background:rgba(15,23,42,0.8); padding:1rem; border-radius:8px; border:1px solid rgba(51,65,85,0.6);">
                    <div style="font-size:0.75rem; color:#64748b;">CHEF DE CHANTIER</div>
                    <div style="font-weight:700; font-size:1rem; color:#f8fafc; margin-top:0.25rem;">${p.site_chief || 'Équipe A'}</div>
                </div>
                <div style="background:rgba(15,23,42,0.8); padding:1rem; border-radius:8px; border:1px solid rgba(51,65,85,0.6);">
                    <div style="font-size:0.75rem; color:#64748b;">PÉRIODE TRAVAUX</div>
                    <div style="font-weight:700; font-size:0.95rem; color:#38bdf8; margin-top:0.25rem; font-family:'JetBrains Mono';">${p.start} ➜ ${p.end}</div>
                </div>
                <div style="background:rgba(15,23,42,0.8); padding:1rem; border-radius:8px; border:1px solid rgba(51,65,85,0.6);">
                    <div style="font-size:0.75rem; color:#64748b;">AVANCEMENT GLOBAL</div>
                    <div style="font-weight:700; font-size:1.2rem; color:var(--emerald); margin-top:0.25rem; font-family:'JetBrains Mono';">${p.progress}%</div>
                </div>
            </div>

            <h3 style="font-size:1.1rem; font-weight:800; color:#38bdf8; margin-bottom:0.75rem;">📦 Lots Techniques & Décomposition</h3>
            <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(51,65,85,0.5); border-radius:8px; overflow:hidden; margin-bottom:1.5rem;">
                <table style="width:100%; border-collapse:collapse; font-size:0.85rem;">
                    <thead>
                        <tr style="background:rgba(30,41,59,0.8); color:#94a3b8; text-align:left;">
                            <th style="padding:0.75rem;">Lot</th>
                            <th style="padding:0.75rem;">Désignation</th>
                            <th style="padding:0.75rem;">Budget Prév.</th>
                            <th style="padding:0.75rem;">Avancement</th>
                            <th style="padding:0.75rem;">Statut</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${(p.lots || [
                            { lot: '01', name: 'Terrassement & Déblais', budget: (p.budget || 500000) * 0.25, progress: p.progress, status: 'En cours' },
                            { lot: '02', name: 'Assainissement EU/EP', budget: (p.budget || 500000) * 0.35, progress: Math.min(100, Math.round(p.progress * 0.9)), status: 'En cours' },
                            { lot: '03', name: 'Réseaux Secs (AEP / Élec / Télécom)', budget: (p.budget || 500000) * 0.2, progress: Math.min(100, Math.round(p.progress * 0.7)), status: 'En cours' },
                            { lot: '04', name: 'Voirie & Enrobés', budget: (p.budget || 500000) * 0.2, progress: Math.min(100, Math.round(p.progress * 0.4)), status: 'Préparation' }
                        ]).map(l => `
                            <tr style="border-top:1px solid rgba(51,65,85,0.3);">
                                <td style="padding:0.75rem; font-weight:700; color:#38bdf8;">Lot ${l.lot}</td>
                                <td style="padding:0.75rem; font-weight:600; color:#f8fafc;">${l.name}</td>
                                <td style="padding:0.75rem; font-family:'JetBrains Mono'; font-weight:700; color:var(--emerald);">${Math.round(l.budget).toLocaleString()} €</td>
                                <td style="padding:0.75rem;">
                                    <div style="display:flex; align-items:center; gap:0.5rem;">
                                        <div class="progress-bar" style="flex:1; height:6px;"><div class="progress-fill" style="width:${l.progress}%; background:#38bdf8;"></div></div>
                                        <span style="font-family:'JetBrains Mono'; font-size:0.75rem;">${l.progress}%</span>
                                    </div>
                                </td>
                                <td style="padding:0.75rem;"><span class="badge ${l.progress >= 90 ? 'badge-success' : 'badge-info'}">${l.status}</span></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>

            <h3 style="font-size:1.1rem; font-weight:800; color:#38bdf8; margin-bottom:0.75rem;">📄 Documents Contractuels & Plans Disponibles</h3>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:0.75rem;">
                ${(p.docs || []).map(d => `
                    <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(51,65,85,0.6); padding:0.85rem; border-radius:8px; display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="font-weight:700; font-size:0.85rem; color:#f8fafc;">${d.name}</div>
                            <div style="font-size:0.75rem; color:#64748b;">Format ${d.type.toUpperCase()} • Validé MOE</div>
                        </div>
                        <button class="btn btn-primary" style="padding:0.35rem 0.6rem; font-size:0.75rem;" onclick="downloadProjectDoc('${d.name.replace(/'/g, "\\\\'")}', '${p.name.replace(/'/g, "\\\\'")}', '${d.type}')">
                            📥 Ouvrir
                        </button>
                    </div>
                `).join('')}
            </div>
        `;
        openModal('project-details-modal');
    }

    // ==========================================
    // 6. PLANNING GANTT & AGENDA ENGINE
    // ==========================================
    function setPlanningView(mode) {
        planningViewMode = mode;
        document.querySelectorAll('.planning-mode-btn').forEach(b => b.classList.remove('active'));
        document.getElementById(`btn-plan-${mode}`)?.classList.add('active');

        const agendaEl = document.getElementById('planning-agenda-view');
        const ganttEl = document.getElementById('planning-gantt-view');
        if (agendaEl) agendaEl.style.display = (mode.startsWith('agenda')) ? 'block' : 'none';
        if (ganttEl) ganttEl.style.display = (mode === 'gantt') ? 'block' : 'none';

        if (mode.startsWith('agenda')) {
            renderPlanningAgenda();
        } else {
            renderPlanningGantt();
        }
    }

    function shiftAgendaWeek(delta) {
        currentAgendaWeekOffset += delta;
        renderPlanningAgenda();
    }

    function resetAgendaWeek() {
        currentAgendaWeekOffset = 0;
        renderPlanningAgenda();
    }

    function setPlanningProjectFilter(projId) {
        const select = document.getElementById('planning-project-select');
        if (select) {
            select.value = projId;
            if (planningViewMode.startsWith('agenda')) renderPlanningAgenda();
            else renderPlanningGantt();
        }
    }

    function renderPlanningAgenda() {
        const container = document.getElementById('planning-agenda-view');
        if (!container) return;

        const projFilter = document.getElementById('planning-project-select')?.value || 'all';
        const teamFilter = document.getElementById('planning-team-select')?.value || 'all';

        const baseDate = new Date(2026, 8, 21); // Monday Sept 21 2026
        baseDate.setDate(baseDate.getDate() + (currentAgendaWeekOffset * 7));

        const dayNames = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi'];
        const weekDays = [];
        for (let i = 0; i < 5; i++) {
            const d = new Date(baseDate);
            d.setDate(baseDate.getDate() + i);
            weekDays.push({
                name: dayNames[i],
                dateStr: d.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit' }),
                fullDate: d
            });
        }

        const teams = [
            { id: 'team_a', name: 'Équipe VRD A (M. Traoré - 6 ouvriers)', icon: '🚜' },
            { id: 'team_b', name: 'Équipe Réseaux Secs B (K. Benali - 4 ouvriers)', icon: '⚡' },
            { id: 'team_c', name: 'Équipe Enrobés & Voirie C (P. Durand - 5 ouvriers)', icon: '🛣️' },
            { id: 'team_topo', name: 'Cellule Topo / Contrôle (D. Lemoine)', icon: '🛰️' }
        ].filter(t => teamFilter === 'all' || t.id === teamFilter);

        const agendaTasks = [
            { teamId: 'team_a', dayIdx: 0, projId: 'projet_ales', projName: 'Giratoire RD906 Alès', task: 'Pose Bordures T2 & Cunette', progress: 85, color: '#0284c7' },
            { teamId: 'team_a', dayIdx: 1, projId: 'projet_ales', projName: 'Giratoire RD906 Alès', task: 'Bétonnage Calage Bordures', progress: 60, color: '#0284c7' },
            { teamId: 'team_a', dayIdx: 2, projId: 'projet_sete', projName: 'ZAC Littoral Sète', task: 'Blindage Tranchée Rue Centrale', progress: 40, color: '#10b981' },
            { teamId: 'team_a', dayIdx: 3, projId: 'projet_sete', projName: 'ZAC Littoral Sète', task: 'Pose Tuyaux Fonte DN400', progress: 20, color: '#10b981' },
            { teamId: 'team_a', dayIdx: 4, projId: 'projet_sete', projName: 'ZAC Littoral Sète', task: 'Remblaiement & Essai Compactage', progress: 0, color: '#10b981' },

            { teamId: 'team_b', dayIdx: 0, projId: 'projet_pezenas', projName: 'Centre Ancien Pézenas', task: 'Tirage Câbles HTA & Fourreaux', progress: 95, color: '#f59e0b' },
            { teamId: 'team_b', dayIdx: 1, projId: 'projet_pezenas', projName: 'Centre Ancien Pézenas', task: 'Raccordement Postes Élec', progress: 80, color: '#f59e0b' },
            { teamId: 'team_b', dayIdx: 2, projId: 'projet_pezenas', projName: 'Centre Ancien Pézenas', task: 'Pose Chambres Télécom L2T', progress: 50, color: '#f59e0b' },
            { teamId: 'team_b', dayIdx: 3, projId: 'projet_ales', projName: 'Giratoire RD906 Alès', task: 'Pose Candelabres Éclairage', progress: 10, color: '#0284c7' },
            { teamId: 'team_b', dayIdx: 4, projId: 'projet_ales', projName: 'Giratoire RD906 Alès', task: 'Contrôle Continuité & Essais', progress: 0, color: '#0284c7' },

            { teamId: 'team_c', dayIdx: 0, projId: 'projet_montpellier', projName: 'Voie Verte Montpellier', task: 'Rabotage Ancien Revêtement', progress: 100, color: '#8b5cf6' },
            { teamId: 'team_c', dayIdx: 1, projId: 'projet_montpellier', projName: 'Voie Verte Montpellier', task: 'Application Couche d’Accrochage', progress: 75, color: '#8b5cf6' },
            { teamId: 'team_c', dayIdx: 2, projId: 'projet_montpellier', projName: 'Voie Verte Montpellier', task: 'Mise en oeuvre BBSG 0/10 (350t)', progress: 30, color: '#8b5cf6' },
            { teamId: 'team_c', dayIdx: 3, projId: 'projet_montpellier', projName: 'Voie Verte Montpellier', task: 'Compactage de Finition & Joints', progress: 0, color: '#8b5cf6' },
            { teamId: 'team_c', dayIdx: 4, projId: 'projet_montpellier', projName: 'Voie Verte Montpellier', task: 'Nettoyage & Levée Réserves', progress: 0, color: '#8b5cf6' },

            { teamId: 'team_topo', dayIdx: 0, projId: 'projet_ales', projName: 'Giratoire RD906 Alès', task: 'Implantation Axes Voirie', progress: 100, color: '#ec4899' },
            { teamId: 'team_topo', dayIdx: 1, projId: 'projet_sete', projName: 'ZAC Littoral Sète', task: 'Relevé Tranchée Ouverte As-Built', progress: 90, color: '#ec4899' },
            { teamId: 'team_topo', dayIdx: 2, projId: 'projet_pezenas', projName: 'Centre Ancien Pézenas', task: 'Géoréférencement Réseaux Classe A', progress: 60, color: '#ec4899' },
            { teamId: 'team_topo', dayIdx: 3, projId: 'projet_montpellier', projName: 'Voie Verte Montpellier', task: 'Contrôle Altimétrique Couche Roulement', progress: 10, color: '#ec4899' },
            { teamId: 'team_topo', dayIdx: 4, projId: 'projet_ales', projName: 'Giratoire RD906 Alès', task: 'Édition Plans de Récolement DAO', progress: 0, color: '#ec4899' }
        ];

        const filteredTasks = agendaTasks.filter(t => projFilter === 'all' || t.projId === projFilter);

        container.innerHTML = `
            <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(51,65,85,0.6); border-radius:10px; overflow-x:auto;">
                <table style="width:100%; border-collapse:collapse; min-width:900px;">
                    <thead>
                        <tr style="background:rgba(30,41,59,0.9); border-bottom:2px solid var(--border);">
                            <th style="padding:1rem; text-align:left; width:220px; color:#cbd5e1; font-weight:800;">ÉQUIPES & RESSOURCES</th>
                            ${weekDays.map(d => `
                                <th style="padding:1rem; text-align:center; color:#f8fafc; font-weight:700; border-left:1px solid rgba(51,65,85,0.4);">
                                    <div>${d.name}</div>
                                    <div style="font-size:0.8rem; font-family:'JetBrains Mono'; color:#38bdf8; font-weight:400; margin-top:2px;">${d.dateStr}</div>
                                </th>
                            `).join('')}
                        </tr>
                    </thead>
                    <tbody>
                        ${teams.map(team => `
                            <tr style="border-bottom:1px solid rgba(51,65,85,0.4);">
                                <td style="padding:1rem; background:rgba(30,41,59,0.4); vertical-align:top;">
                                    <div style="font-weight:800; color:#f8fafc; font-size:0.9rem;">${team.icon} ${team.name}</div>
                                    <div style="font-size:0.75rem; color:#64748b; margin-top:0.25rem;">Affectation & Supervision</div>
                                </td>
                                ${[0, 1, 2, 3, 4].map(dayIdx => {
                                    const tasks = filteredTasks.filter(t => t.teamId === team.id && t.dayIdx === dayIdx);
                                    return `
                                        <td style="padding:0.6rem; vertical-align:top; border-left:1px solid rgba(51,65,85,0.3); background:rgba(15,23,42,0.3);">
                                            ${tasks.length === 0 ? '<div style="font-size:0.75rem; color:#475569; text-align:center; padding:1rem 0;">Aucune tâche</div>' : ''}
                                            ${tasks.map(tsk => `
                                                <div style="background:rgba(30,41,59,0.85); border-left:3px solid ${tsk.color}; border-radius:4px; padding:0.5rem; margin-bottom:0.4rem; box-shadow:0 2px 4px rgba(0,0,0,0.3);">
                                                    <div style="font-size:0.7rem; font-weight:700; color:${tsk.color}; text-transform:uppercase;">${tsk.projName}</div>
                                                    <div style="font-size:0.8rem; font-weight:700; color:#f8fafc; margin:0.2rem 0;">${tsk.task}</div>
                                                    <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.7rem; color:#94a3b8; margin-top:0.3rem;">
                                                        <span>Progression</span>
                                                        <span style="font-family:'JetBrains Mono'; font-weight:700; color:${tsk.progress === 100 ? 'var(--emerald)' : '#38bdf8'};">${tsk.progress}%</span>
                                                    </div>
                                                    <div class="progress-bar" style="height:4px; margin-top:3px;"><div class="progress-fill" style="width:${tsk.progress}%; background:${tsk.color};"></div></div>
                                                </div>
                                            `).join('')}
                                        </td>
                                    `;
                                }).join('')}
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    function renderPlanningGantt() {
        const container = document.getElementById('planning-gantt-view');
        if (!container) return;

        const projFilter = document.getElementById('planning-project-select')?.value || 'all';
        const tasks = [
            { id: 't1', projId: 'projet_ales', proj: 'Giratoire RD906 Alès', task: 'Terrassement en déblai & Purge', start: 1, dur: 3, progress: 100, team: 'Équipe A' },
            { id: 't2', projId: 'projet_ales', proj: 'Giratoire RD906 Alès', task: 'Pose Réseau Assainissement EU', start: 3, dur: 4, progress: 80, team: 'Équipe A' },
            { id: 't3', projId: 'projet_ales', proj: 'Giratoire RD906 Alès', task: 'Pose Fourreaux Réseaux Secs', start: 6, dur: 3, progress: 40, team: 'Équipe B' },
            { id: 't4', projId: 'projet_ales', proj: 'Giratoire RD906 Alès', task: 'Pose Bordures & Trottoirs', start: 8, dur: 4, progress: 15, team: 'Équipe A' },
            { id: 't5', projId: 'projet_ales', proj: 'Giratoire RD906 Alès', task: 'Couche de Forme & Enrobés', start: 11, dur: 3, progress: 0, team: 'Équipe C' },

            { id: 't6', projId: 'projet_sete', proj: 'ZAC Littoral Sète', task: 'Sciage & Démolition Chaussée', start: 1, dur: 2, progress: 100, team: 'Équipe A' },
            { id: 't7', projId: 'projet_sete', proj: 'ZAC Littoral Sète', task: 'Blindage & Pose Fonte DN400', start: 3, dur: 5, progress: 65, team: 'Équipe A' },
            { id: 't8', projId: 'projet_sete', proj: 'ZAC Littoral Sète', task: 'Remblaiement & Essais Dynamiques', start: 7, dur: 3, progress: 20, team: 'Équipe A' },
            { id: 't9', projId: 'projet_sete', proj: 'ZAC Littoral Sète', task: 'Réfection Enrobé à Chaud', start: 9, dur: 3, progress: 0, team: 'Équipe C' },

            { id: 't10', projId: 'projet_pezenas', proj: 'Centre Ancien Pézenas', task: 'Tranchée Commune VRD', start: 2, dur: 4, progress: 90, team: 'Équipe B' },
            { id: 't11', projId: 'projet_pezenas', proj: 'Centre Ancien Pézenas', task: 'Raccordement Haute Tension & Fibre', start: 5, dur: 4, progress: 50, team: 'Équipe B' },
            { id: 't12', projId: 'projet_montpellier', proj: 'Voie Verte Montpellier', task: 'Aménagements Paysagers & Bordures', start: 8, dur: 4, progress: 10, team: 'Équipe C' }
        ].filter(t => projFilter === 'all' || t.projId === projFilter);

        const totalWeeks = 14;

        container.innerHTML = `
            <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(51,65,85,0.6); border-radius:10px; padding:1rem; overflow-x:auto;">
                <div style="min-width:850px;">
                    <div style="display:grid; grid-template-columns: 240px repeat(${totalWeeks}, 1fr); gap:4px; font-weight:800; font-size:0.75rem; color:#94a3b8; margin-bottom:0.75rem; border-bottom:1px solid rgba(51,65,85,0.6); padding-bottom:0.5rem;">
                        <div>TÂCHES / PHASES DE TRAVAUX</div>
                        ${Array.from({ length: totalWeeks }).map((_, i) => `<div style="text-align:center;">S${i + 1}</div>`).join('')}
                    </div>

                    ${tasks.map(t => {
                        const colStart = t.start + 1;
                        const colSpan = t.dur;
                        return `
                            <div style="display:grid; grid-template-columns: 240px repeat(${totalWeeks}, 1fr); gap:4px; align-items:center; margin-bottom:0.6rem; font-size:0.8rem;">
                                <div style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="${t.proj} - ${t.task}">
                                    <strong style="color:#f8fafc;">${t.task}</strong><br>
                                    <span style="font-size:0.7rem; color:#64748b;">${t.proj} • ${t.team}</span>
                                </div>
                                <div style="grid-column: ${colStart} / span ${colSpan};">
                                    <div style="background:rgba(30,41,59,0.9); border:1px solid #38bdf8; border-radius:4px; padding:4px 8px; position:relative; overflow:hidden; box-shadow:0 2px 4px rgba(0,0,0,0.3);">
                                        <div style="position:absolute; top:0; left:0; bottom:0; width:${t.progress}%; background:linear-gradient(90deg, rgba(2,132,199,0.7), rgba(56,189,248,0.9)); z-index:1;"></div>
                                        <div style="position:relative; z-index:2; display:flex; justify-content:space-between; font-size:0.7rem; font-weight:700; color:#ffffff;">
                                            <span>${t.task}</span>
                                            <span style="font-family:'JetBrains Mono';">${t.progress}%</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `;
    }
"""
