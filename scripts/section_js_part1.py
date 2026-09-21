# -*- coding: utf-8 -*-

def get_js_part1():
    return r"""<script>
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
        client: p.client || 'Maître d\'Ouvrage Public',
        ownership: p.ownership || '🏢 Notre Entreprise (En cours)',
        location: p.location || 'Occitanie (34)',
        budget: Number(p.budget_total || p.budget || 500000),
        budget_used: Number(p.depense_reelle || p.budget_used || (p.budget_total || 500000) * 0.72),
        progress: Number(p.avancement_physique_pct || p.progress || 50),
        delai_consomme_pct: Number(p.delai_consomme_pct || 48),
        status: p.statut || p.status || 'En cours',
        manager: p.conducteur || p.manager || 'Sylvain CABROL',
        site_chief: p.chef_chantier || p.site_chief || 'Alain MARTIN',
        start: p.date_debut || p.start || '2026-05-15',
        end: p.date_fin_prevue || p.end || '2026-10-30',
        timeline_steps: p.timeline_steps || [
            { step: 1, name: "DICT & Piquetage 7 Couleurs", date: "15/05/2026", progress: 100, status: "Terminé", lot: "Lot 01" },
            { step: 2, name: "Terrassement en déblai & Purge", date: "10/06/2026", progress: 100, status: "Terminé", lot: "Lot 01" },
            { step: 3, name: "Pose Assainissement EU/EP", date: "15/07/2026", progress: 100, status: "Terminé", lot: "Lot 02" },
            { step: 4, name: "Fourreaux Réseaux Secs", date: "15/08/2026", progress: 80, status: "En cours", lot: "Lot 04" },
            { step: 5, name: "Pose Bordures & Caniveaux", date: "10/09/2026", progress: 60, status: "En cours", lot: "Lot 03" },
            { step: 6, name: "Couche de Roulement BBSG", date: "15/10/2026", progress: 10, status: "À venir", lot: "Lot 03" },
            { step: 7, name: "Réception OPR / DGD", date: "30/10/2026", progress: 0, status: "À venir", lot: "Clôture" }
        ],
        assigned_machinery: p.assigned_machinery || [
            { name: "Pelle Liebherr R924 (24t)", type: "Terrassement", status: "Actif" },
            { name: "Camion 8x4 Scania", type: "Transport", status: "Actif" }
        ],
        assigned_tools: p.assigned_tools || [
            { name: "Laser Canalisateur Piper 200", type: "Topographie" },
            { name: "Scie Diamant Stihl TS800", type: "Découpe" }
        ],
        assigned_materials: p.assigned_materials || [
            { name: "Grave GNT 0/31.5 Classe A", qty: "4 200 tonnes", supplier: "Carrières du Languedoc" },
            { name: "Bordures Béton T2 NF", qty: "850 ml", supplier: "Bétons Occitanie" }
        ],
        lots_breakdown: p.lots_breakdown || [
            {
                lot: '01',
                name: 'Terrassement & Déblais',
                budget: (p.budget_total || 500000) * 0.25,
                progress: 100,
                status: 'Terminé',
                tech_steps: [
                    "Décapage terre végétale épaisseur 20cm au scraper.",
                    "Déblais grande masse en pleine masse à la pelle 24t.",
                    "Traitement de sol à la chaux vive 2% (portance EV2 >= 50 MPa).",
                    "Évacuation déblais en décharge agréée ISDI avec BSD."
                ],
                admin_steps: [
                    "Récépissés DICT conformes (GRDF, Enedis, Orange).",
                    "Arrêté municipal de restriction de circulation (30 km/h).",
                    "Plan Particulier de Sécurité et Santé (PPSPS) validé.",
                    "Procès-Verbal de réception de plateforme terrassement."
                ]
            },
            {
                lot: '02',
                name: 'Assainissement & Eaux Pluviales',
                budget: (p.budget_total || 500000) * 0.35,
                progress: Math.min(100, Math.round((p.avancement_physique_pct || 75) * 0.9)),
                status: 'En cours',
                tech_steps: [
                    "Tranchée 1.80m avec blindage continu et lit de pose sable 4/10.",
                    "Pose au laser des tuyaux béton armé Ø400 135A (pente 1.5%).",
                    "Regards préfabriqués 1000x1000 avec cunettes hydrauliques.",
                    "Remblaiement par couches 30cm GNT 0/31.5 au pilonneur."
                ],
                admin_steps: [
                    "Agrément des fournitures par la Maîtrise d'Œuvre.",
                    "Rapport d'épreuve d'étanchéité à l'air/eau Fascicule 70.",
                    "Rapport d'inspection télévisée (ITV) caméra HD.",
                    "Plans de récolement DAO levés en classe A."
                ]
            },
            {
                lot: '03',
                name: 'Voirie, Bordures & Chaussée',
                budget: (p.budget_total || 500000) * 0.2,
                progress: Math.min(100, Math.round((p.avancement_physique_pct || 75) * 0.6)),
                status: 'En cours',
                tech_steps: [
                    "Couche de fondation GNT 0/31.5 ép. 25cm au rouleau V5.",
                    "Pose sur semelle béton C25/30 de 850 ml bordures T2.",
                    "Coulage îlot central en béton désactivé décoratif 6/10.",
                    "Application BBSG 0/10 à 160°C au finisseur grande largeur."
                ],
                admin_steps: [
                    "Rapport d'essais à la plaque Terrameter (EV2 > 120 MPa).",
                    "Essais de compacité par laboratoire COFRAC.",
                    "Contrôle d'uni longitudinal et transversal.",
                    "Dossier des Ouvrages Exécutés (DOE) remis à la MOE."
                ]
            },
            {
                lot: '04',
                name: 'Réseaux Secs & Éclairage',
                budget: (p.budget_total || 500000) * 0.2,
                progress: Math.min(100, Math.round((p.avancement_physique_pct || 75) * 0.7)),
                status: 'En cours',
                tech_steps: [
                    "Fourreaux TPC Ø110 rouge, vert et jaune sous trottoir.",
                    "Grillage avertisseur normé 20cm au-dessus des gaines.",
                    "Massifs béton armé 1.00m x 1.00m pour 12 candélabres LED.",
                    "Raccordement au coffret télégestion."
                ],
                admin_steps: [
                    "Contrôle d'isolement par organisme APAVE.",
                    "Attestation de raccordement Enedis.",
                    "Conformité Consuel pour éclairage public."
                ]
            }
        ],
        docs: [
            { name: 'CCTP_Voirie_Réseaux', type: 'pdf' },
            { name: 'BPU_DQE_Signé', type: 'pdf' },
            { name: 'Plan_Implantation_DAO', type: 'dwg' },
            { name: 'DICT_Récépissés_Valides', type: 'pdf' },
            { name: 'PGCSPS_Sécurité', type: 'pdf' }
        ]
    }));

    // GLOBAL APP STATE
    let currentPerspective = 'patron';
    let currentNav = 'cockpit';
    let caisseBalance = 485200;
    let planningViewMode = 'agenda_week';
    let currentAgendaWeekOffset = 0;
    let simulatorViewMode = 'radar';
    let isRadarLive = true;
    let is4DSimPlaying = false;
    let sim4DInterval = null;
    let currentScenarioId = 'scen_tranchee_vrd';
    let activeScenarioStepIdx = 0;
    let fleetFilter = 'all';
    let fleetPresentationMode = 'grid';
    let catalogFilter = 'all';
    let catalogPresentationMode = 'grid';
    let obsidianHeuristic = 'all';
    let sdpViewMode = 'dqe_tcd';
    let showSdpFormulas = false;
    let showCashflowFormulas = false;
    let activeGisLayer = 'dict';
    let activeProjectModalId = 'projet_ales';
    let activeProjectModalLotIdx = 0;
    let radarCanvas, radarCtx, radarAnimId;
    let cameraRotX = 30, cameraRotY = -45, cameraZoom = 1.0;
    let isDragging3D = false, lastMouseX = 0, lastMouseY = 0;
    let webcamStream = null;
    let currentMapFilter = 'all';
    let mapZoom = 1.0, mapPanX = 0, mapPanY = 0;
    let isDraggingMap = false, lastMapMouseX = 0, lastMapMouseY = 0;
    let selectedMapPoint = null;

    // ==========================================
    // 2. TECHNICAL SVG VECTOR ILLUSTRATIONS
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
        if (id.includes('bordure') || id.includes('mat_05') || id.includes('mat_06') || id.includes('mat_07')) {
            return `<svg viewBox="0 0 260 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
                <polygon points="40,95 170,95 220,50 90,50" fill="#94a3b8" stroke="#cbd5e1" stroke-width="2"/>
                <polygon points="40,95 170,95 170,125 40,125" fill="#64748b" stroke="#334155" stroke-width="2"/>
                <polygon points="170,95 220,50 220,80 170,125" fill="#475569" stroke="#1e293b" stroke-width="2"/>
                <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Bordure Béton T2 / A2 / I2 NF</text>
            </svg>`;
        } else if (id.includes('tampon') || id.includes('fonte') || id.includes('mat_11') || id.includes('mat_12')) {
            return `<svg viewBox="0 0 260 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
                <rect x="45" y="15" width="170" height="110" rx="8" fill="#1e293b" stroke="#475569" stroke-width="2"/>
                <circle cx="130" cy="70" r="42" fill="#0f172a" stroke="#94a3b8" stroke-width="3"/>
                <text x="112" y="74" fill="#facc15" font-family="system-ui" font-weight="900" font-size="10">D 400</text>
                <text x="15" y="15" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Tampon Fonte D400 PAM Rexel</text>
            </svg>`;
        } else if (id.includes('tuyau') || id.includes('mat_13') || id.includes('mat_14') || id.includes('mat_15')) {
            return `<svg viewBox="0 0 260 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
                <rect x="50" y="45" width="170" height="45" rx="4" fill="#334155" stroke="#0284c7" stroke-width="2"/>
                <rect x="25" y="38" width="30" height="58" rx="5" fill="#1e293b" stroke="#0284c7" stroke-width="2"/>
                <text x="70" y="72" fill="#38bdf8" font-family="JetBrains Mono" font-size="10" font-weight="800">FONTE / PVC CR8</text>
                <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Tuyau Assainissement</text>
            </svg>`;
        } else if (id.includes('laser') || id.includes('piper') || id.includes('tool_01') || id.includes('tool_02')) {
            return `<svg viewBox="0 0 260 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
                <rect x="35" y="45" width="120" height="45" rx="8" fill="#dc2626" stroke="#991b1b" stroke-width="2"/>
                <circle cx="155" cy="67" r="22" fill="#1e293b" stroke="#dc2626" stroke-width="2"/>
                <circle cx="155" cy="67" r="7" fill="#10b981"/>
                <line x1="160" y1="67" x2="240" y2="67" stroke="#10b981" stroke-width="2"/>
                <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Laser Canalisateur Piper 200</text>
            </svg>`;
        } else if (id.includes('scie') || id.includes('stihl') || id.includes('tool_03') || id.includes('pilonneuse') || id.includes('tool_04')) {
            return `<svg viewBox="0 0 260 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
                <rect x="40" y="55" width="80" height="35" rx="5" fill="#ea580c" stroke="#c2410c" stroke-width="2"/>
                <circle cx="175" cy="72" r="35" fill="#475569" stroke="#94a3b8" stroke-width="2"/>
                <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Découpeuse Diamant Stihl TS800</text>
            </svg>`;
        } else if (id.includes('epi') || id.includes('casque') || id.includes('gilet') || id.includes('sig') || id.includes('mat_01') || id.includes('mat_02')) {
            return `<svg viewBox="0 0 260 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
                <path d="M 40 55 C 40 30 95 30 95 55 Z" fill="#facc15" stroke="#ca8a04" stroke-width="2"/>
                <path d="M 120 40 L 180 40 L 195 105 L 105 105 Z" fill="#facc15" stroke="#eab308" stroke-width="2"/>
                <line x1="115" y1="70" x2="185" y2="70" stroke="#f8fafc" stroke-width="5"/>
                <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Pack EPI Normé BTP Classe 3</text>
            </svg>`;
        } else {
            return `<svg viewBox="0 0 260 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
                <rect x="40" y="40" width="180" height="60" rx="6" fill="#1e293b" stroke="#06b6d4" stroke-width="2"/>
                <circle cx="130" cy="70" r="18" fill="#06b6d4" fill-opacity="0.2"/>
                <text x="130" y="75" fill="#f8fafc" font-size="14" text-anchor="middle">📦</text>
                <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Fourniture / Matériau TP</text>
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
            { id: 'cockpit', label: '🎛️ Cockpit & SIG' },
            { id: 'company', label: '🏢 Entreprise & Caisse' },
            { id: 'depot', label: '🏭 Dépôt & Entrepôt' },
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
            { id: 'benchmark', label: '📊 Benchmark & Inventaire' },
            { id: 'obsidian', label: '📚 Base Obsidian' },
            { id: 'schemas', label: '📐 Technique & Analyse' },
            { id: 'procurement', label: '🛒 Fournisseurs' },
            { id: 'ledger', label: '⛓️ Ledger SHA-256' },
            { id: 'docs', label: '📚 Dossiers Réglementaires' },
            { id: 'archives', label: '🗄️ Archives & GED' }
        ],
        'conduite': [
            { id: 'cockpit', label: '🎛️ Cockpit' },
            { id: 'projects_hub', label: '📁 Chantiers en Cours' },
            { id: 'depot', label: '🏭 Dépôt & Entrepôt' },
            { id: 'planning', label: '📅 Planning & Agenda' },
            { id: 'simulator', label: '🛰️ Watch Tower' },
            { id: 'fleet', label: '🚜 Flotte & Dispatch' },
            { id: 'catalog', label: '🛒 Commandes Matériaux' },
            { id: 'hr', label: '👷 Équipes & RH' },
            { id: 'opbtp', label: '🦺 Signalétique OPBTP' },
            { id: 'safety', label: '🛡️ Sécurité & AIPR' },
            { id: 'rdc', label: '📋 Journal RDC' },
            { id: 'sdp', label: '💰 Sous-Détails & DQE' },
            { id: 'benchmark', label: '📊 Benchmark Prix' },
            { id: 'obsidian', label: '📚 Base Obsidian' },
            { id: 'schemas', label: '📐 Technique & Analyse' },
            { id: 'procurement', label: '🛒 Fournisseurs' },
            { id: 'docs', label: '📚 Dossiers Réglementaires' },
            { id: 'archives', label: '🗄️ Archives & GED' }
        ],
        'compagnon': [
            { id: 'compagnon_mobile', label: '📱 Mode Terrain & Mon Planning' },
            { id: 'depot', label: '🏭 Dépôt Matériel' },
            { id: 'planning', label: '📅 Planning Général' },
            { id: 'opbtp', label: '🦺 Balisage OPBTP' },
            { id: 'safety', label: '🛡️ Règles Sécurité' },
            { id: 'rdc', label: '📋 Saisie RDC' },
            { id: 'schemas', label: '📐 Technique' },
            { id: 'docs', label: '📚 Dossiers' },
            { id: 'archives', label: '🗄️ Archives' }
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

        try {
            if (tabId === 'cockpit') setTimeout(initCockpitOsmMap, 50);
            if (tabId === 'company') renderCompanyCashflowTable();
            if (tabId === 'depot') {
                setTimeout(() => {
                    initDepotCanvas();
                    renderDepotInventory();
                }, 50);
            }
            if (tabId === 'projects_hub') renderProjectsHub();
            if (tabId === 'planning') {
                if (planningViewMode.startsWith('agenda')) renderPlanningAgenda();
                else renderPlanningGantt();
            }
            if (tabId === 'compagnon_mobile') renderCompagnonPlanning();
            if (tabId === 'fleet') renderFleetGrid();
            if (tabId === 'catalog') renderCatalogGrid();
            if (tabId === 'obsidian') {
                setTimeout(() => {
                    renderObsidianFolderTree();
                    initObsidianGraph();
                }, 50);
            }
            if (tabId === 'simulator') {
                setTimeout(() => {
                    init3DCanvas();
                    initWatchtowerRadar();
                    renderWatchtowerActors();
                    drawStepVisual(activeScenarioStepIdx);
                }, 50);
            }
            if (tabId === 'hr') {
                setTimeout(() => {
                    initHrTree();
                    renderHrPartners();
                }, 50);
            }
            if (tabId === 'sdp') {
                if (sdpViewMode === 'dqe_tcd') renderDQEPivotTable();
                else if (sdpViewMode === 'cards') renderSdpCards();
                else renderEnterprisePriceComparison();
            }
            if (tabId === 'benchmark') {
                renderBenchmarkTable();
                renderInventoryTable();
                renderTeamsBenchmarkTable();
            }
            if (tabId === 'opbtp') {
                updateOpbtpSubdomainOptions();
                calculateSignage();
            }
            if (tabId === 'safety') {
                setTimeout(() => {
                    updateAiprPhaseDetails();
                    setAiprSituation('gaz');
                }, 50);
            }
            if (tabId === 'rdc') renderRdcTable();
            if (tabId === 'schemas') {
                updateFormulaCalculator();
                renderTaskSheet();
                setTimeout(initCompactageCutCanvas, 50);
            }
            if (tabId === 'procurement') {
                renderProcurement();
                setTimeout(initSuppliersMap, 50);
            }
            if (tabId === 'ledger') renderLedger();
            if (tabId === 'docs') renderRegulatoryDocs();
            if (tabId === 'archives') renderArchives();
        } catch (e) {
            console.error('Error switching tab to ' + tabId + ':', e);
        }
    }

    function scrollNav(offset) {
        const dock = document.getElementById('main-nav-dock');
        if (dock) dock.scrollBy({ left: offset, behavior: 'smooth' });
    }

    function openModal(id) { document.getElementById(id)?.classList.add('active'); }
    function closeModal(id) { document.getElementById(id)?.classList.remove('active'); }

    function toggleTacticalWheel() {
        document.getElementById('tactical-wheel-menu')?.classList.toggle('active');
    }

    function quickAction(actionId) {
        toggleTacticalWheel();
        switchNav(actionId);
    }

    function downloadProjectDoc(docName, projName, fileType) {
        const content = `=== DOSSIER OFFICIEL BTP ===\nChantier : ${projName || 'Travaux Publics'}\nDocument : ${docName}\nFormat : ${fileType || 'PDF'}\nDate : ${new Date().toISOString()}\nCertification SHA-256 : ${Math.random().toString(36).substring(2)}\n\nConforme aux prescriptions CCTP et normes NF/EN.`;
        const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${(projName || 'Chantier').replace(/\s+/g, '_')}_${docName.replace(/\s+/g, '_')}.${fileType || 'pdf'}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        logCockpit(`📥 Téléchargement direct initié : ${docName} pour ${projName}.`, 'ok');
    }

    function downloadDoc(docName) {
        downloadProjectDoc(docName, 'Dossier_CCTP_Global', 'md');
    }

    // ==========================================
    // 5. COCKPIT GIS / OPENSTREETMAP INTERACTIVE MAP
    // ==========================================
    let activeRenderedMapPoints = [];

    function initCockpitOsmMap() {
        const canvas = document.getElementById('cockpit-osm-map-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const w = canvas.parentElement.clientWidth || 700;
        const h = canvas.parentElement.clientHeight || 420;
        canvas.width = w;
        canvas.height = h;

        canvas.onmousedown = (e) => {
            const rect = canvas.getBoundingClientRect();
            const mx = e.clientX - rect.left;
            const my = e.clientY - rect.top;

            let clicked = null;
            for (const pt of activeRenderedMapPoints) {
                if (Math.hypot(pt.drawX - mx, pt.drawY - my) < 18) {
                    clicked = pt;
                    break;
                }
            }

            if (clicked) {
                selectCockpitMapPoint(clicked);
            } else {
                isDraggingMap = true;
                lastMapMouseX = e.clientX;
                lastMapMouseY = e.clientY;
            }
        };

        window.onmouseup = () => { isDraggingMap = false; };

        canvas.onmousemove = (e) => {
            if (isDraggingMap) {
                mapPanX += e.clientX - lastMapMouseX;
                mapPanY += e.clientY - lastMapMouseY;
                lastMapMouseX = e.clientX;
                lastMapMouseY = e.clientY;
                renderCockpitOsmMap();
            }
        };

        canvas.onwheel = (e) => {
            e.preventDefault();
            const factor = e.deltaY < 0 ? 1.1 : 0.9;
            mapZoom = Math.max(0.6, Math.min(3.0, mapZoom * factor));
            renderCockpitOsmMap();
        };

        renderCockpitOsmMap();
    }

    function getFilteredMapPoints() {
        const list = companyData.map_locations || [];
        if (currentMapFilter === 'all') return list;
        return list.filter(p => p.category === currentMapFilter);
    }

    function getScreenCoord(lat, lng, w, h) {
        // High-precision geographic projection centered on Occitanie (43.70° N, 3.65° E)
        const centerLat = 43.70;
        const centerLng = 3.65;
        const scaleX = (w / 1.55) * mapZoom;
        const scaleY = (h / 1.25) * mapZoom;

        const x = (w / 2) + (lng - centerLng) * scaleX + mapPanX;
        const y = (h / 2) - (lat - centerLat) * scaleY + mapPanY;
        return { x, y };
    }

    function renderCockpitOsmMap() {
        const canvas = document.getElementById('cockpit-osm-map-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const w = canvas.width;
        const h = canvas.height;

        ctx.fillStyle = '#060a12';
        ctx.fillRect(0, 0, w, h);

        // Grid Lines (Lambert 93 / WGS84 coordinates)
        ctx.strokeStyle = '#0f172a';
        ctx.lineWidth = 1;
        for (let x = 0; x < w; x += 40) {
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
        }
        for (let y = 0; y < h; y += 40) {
            ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
        }

        // --- 1. ACCURATE OCCITANIE COASTLINE & WATER BODIES ---
        // Mediterranean Sea
        const pCamargue = getScreenCoord(43.45, 4.45, w, h);
        const pPalavas = getScreenCoord(43.53, 3.93, w, h);
        const pFrontignan = getScreenCoord(43.45, 3.75, w, h);
        const pSete = getScreenCoord(43.40, 3.69, w, h);
        const pAgde = getScreenCoord(43.28, 3.50, w, h);
        const pValras = getScreenCoord(43.24, 3.29, w, h);
        const pLeucate = getScreenCoord(42.90, 3.03, w, h);

        ctx.fillStyle = 'rgba(6, 182, 212, 0.12)';
        ctx.beginPath();
        ctx.moveTo(pLeucate.x, pLeucate.y);
        ctx.lineTo(pValras.x, pValras.y);
        ctx.lineTo(pAgde.x, pAgde.y);
        ctx.lineTo(pSete.x, pSete.y);
        ctx.lineTo(pFrontignan.x, pFrontignan.y);
        ctx.lineTo(pPalavas.x, pPalavas.y);
        ctx.lineTo(pCamargue.x, pCamargue.y);
        ctx.lineTo(w + 50, h + 50);
        ctx.lineTo(-50, h + 50);
        ctx.closePath();
        ctx.fill();
        ctx.strokeStyle = 'rgba(6, 182, 212, 0.4)';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Étang de Thau (Between Sète and Balaruc/Mèze)
        const pThau = getScreenCoord(43.43, 3.62, w, h);
        ctx.fillStyle = 'rgba(6, 182, 212, 0.25)';
        ctx.beginPath();
        ctx.ellipse(pThau.x, pThau.y, 24 * mapZoom, 12 * mapZoom, -0.4, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = 'rgba(6, 182, 212, 0.5)';
        ctx.stroke();
        ctx.fillStyle = '#38bdf8';
        ctx.font = '8px monospace';
        ctx.fillText('Étang de Thau', pThau.x - 22, pThau.y + 3);

        // --- 2. CEVENNES RELIEF / MOUNTAINS ---
        const pCevennes = getScreenCoord(44.25, 3.60, w, h);
        ctx.fillStyle = 'rgba(148, 163, 184, 0.08)';
        ctx.beginPath();
        ctx.arc(pCevennes.x, pCevennes.y, 50 * mapZoom, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#64748b';
        ctx.font = 'italic 9px system-ui';
        ctx.fillText('⛰️ Massif des Cévennes', pCevennes.x - 45, pCevennes.y);

        // --- 3. MAJOR TRANSPORT ARTERIES (A9, A750, N106, D613) ---
        const pAles = getScreenCoord(44.1284, 4.0833, w, h);
        const pNimes = getScreenCoord(43.8367, 4.3600, w, h);
        const pMontpellier = getScreenCoord(43.6108, 3.8767, w, h);
        const pBeziers = getScreenCoord(43.3442, 3.2158, w, h);
        const pPezenas = getScreenCoord(43.4600, 3.4230, w, h);
        const pNarbonne = getScreenCoord(43.1833, 3.0000, w, h);

        // Autoroute A9 (La Languedocienne)
        ctx.strokeStyle = '#f59e0b';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(pNimes.x, pNimes.y);
        ctx.lineTo(pMontpellier.x, pMontpellier.y);
        ctx.lineTo(pSete.x - 5, pSete.y - 10);
        ctx.lineTo(pBeziers.x, pBeziers.y);
        ctx.lineTo(pNarbonne.x, pNarbonne.y);
        ctx.stroke();

        // Route Nationale N106 (Alès - Nîmes)
        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.moveTo(pAles.x, pAles.y);
        ctx.lineTo(pNimes.x, pNimes.y);
        ctx.stroke();

        // Autoroute A750 / A75 (Gignac - Pézenas - Béziers)
        ctx.strokeStyle = '#10b981';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(pMontpellier.x, pMontpellier.y);
        ctx.lineTo(pPezenas.x, pPezenas.y);
        ctx.lineTo(pBeziers.x, pBeziers.y);
        ctx.stroke();

        // City Dots & Names
        const cities = [
            { name: "MONTPELLIER", pt: pMontpellier },
            { name: "NÎMES", pt: pNimes },
            { name: "ALÈS", pt: pAles },
            { name: "SÈTE", pt: pSete },
            { name: "BÉZIERS", pt: pBeziers },
            { name: "PÉZENAS", pt: pPezenas }
        ];
        cities.forEach(c => {
            ctx.fillStyle = '#64748b';
            ctx.beginPath(); ctx.arc(c.pt.x, c.pt.y, 3, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#94a3b8'; ctx.font = 'bold 8px system-ui';
            ctx.fillText(c.name, c.pt.x + 5, c.pt.y - 4);
        });

        // --- 4. ANTI-COLLISION CLUSTERING & SPIDERFYING PINS ---
        const rawPoints = getFilteredMapPoints();
        const clusters = [];

        rawPoints.forEach(pt => {
            const screen = getScreenCoord(pt.lat, pt.lng, w, h);
            let cl = clusters.find(c => Math.hypot(c.cx - screen.x, c.cy - screen.y) < 26);
            if (!cl) {
                cl = { cx: screen.x, cy: screen.y, pts: [] };
                clusters.push(cl);
            }
            cl.pts.push({ ...pt, screenX: screen.x, screenY: screen.y });
        });

        activeRenderedMapPoints = [];

        clusters.forEach(cl => {
            const n = cl.pts.length;
            if (n === 1) {
                const p = cl.pts[0];
                p.drawX = cl.cx;
                p.drawY = cl.cy;
                activeRenderedMapPoints.push(p);
            } else {
                // Multiple points close to each other -> Disperse radially
                const radius = Math.min(38, 20 + n * 4);
                cl.pts.forEach((p, idx) => {
                    const angle = (idx / n) * Math.PI * 2 - Math.PI / 2;
                    p.drawX = cl.cx + Math.cos(angle) * radius;
                    p.drawY = cl.cy + Math.sin(angle) * radius;

                    // Leader dashed line from actual location to dispersed pin
                    ctx.strokeStyle = 'rgba(148, 163, 184, 0.4)';
                    ctx.lineWidth = 1;
                    ctx.setLineDash([2, 2]);
                    ctx.beginPath();
                    ctx.moveTo(cl.cx, cl.cy);
                    ctx.lineTo(p.drawX, p.drawY);
                    ctx.stroke();
                    ctx.setLineDash([]);

                    activeRenderedMapPoints.push(p);
                });

                // Center origin hub dot
                ctx.fillStyle = '#64748b';
                ctx.beginPath();
                ctx.arc(cl.cx, cl.cy, 3, 0, Math.PI * 2);
                ctx.fill();
            }
        });

        // Draw all dispersed pins with ZERO overlap
        activeRenderedMapPoints.forEach(pt => {
            const posX = pt.drawX;
            const posY = pt.drawY;

            // Pulsing Ring
            ctx.strokeStyle = pt.color || '#38bdf8';
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.arc(posX, posY, 13, 0, Math.PI * 2);
            ctx.stroke();

            // Pin Center Circle
            ctx.fillStyle = pt.color || '#38bdf8';
            ctx.beginPath();
            ctx.arc(posX, posY, 9, 0, Math.PI * 2);
            ctx.fill();

            // Emoji Icon
            ctx.font = '11px system-ui';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(pt.icon || '📍', posX, posY);

            // Label Text with Background Pill
            const label = pt.name;
            ctx.font = 'bold 8.5px system-ui';
            ctx.textAlign = 'left';
            ctx.textBaseline = 'alphabetic';
            const txtWidth = ctx.measureText(label).width;

            ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
            ctx.fillRect(posX + 12, posY - 8, txtWidth + 6, 12);
            ctx.strokeStyle = 'rgba(51, 65, 85, 0.6)';
            ctx.lineWidth = 0.8;
            ctx.strokeRect(posX + 12, posY - 8, txtWidth + 6, 12);

            ctx.fillStyle = '#f8fafc';
            ctx.fillText(label, posX + 15, posY + 1);
        });

        ctx.textAlign = 'left';
        ctx.textBaseline = 'alphabetic';
    }

    function filterCockpitMap(category, btn) {
        currentMapFilter = category;
        document.querySelectorAll('.map-filter-btn').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
        renderCockpitOsmMap();
    }

    function zoomCockpitMap(factor) {
        mapZoom = Math.max(0.6, Math.min(3.0, mapZoom * factor));
        renderCockpitOsmMap();
    }

    function resetCockpitMap() {
        mapZoom = 1.0;
        mapPanX = 0;
        mapPanY = 0;
        renderCockpitOsmMap();
    }

    function selectCockpitMapPoint(pt) {
        selectedMapPoint = pt;
        const bCat = document.getElementById('pin-badge-cat');
        const bName = document.getElementById('pin-name-val');
        const bDesc = document.getElementById('pin-desc-val');
        const bMetrics = document.getElementById('pin-metrics-box');

        if (bCat) bCat.textContent = (pt.category || 'ENTITÉ TP').toUpperCase();
        if (bName) bName.textContent = pt.name;
        if (bDesc) bDesc.textContent = pt.desc || pt.ownership || 'Point stratégique opérationnel du réseau BTP Occitanie.';

        if (bMetrics) {
            if (pt.category === 'chantier') {
                bMetrics.innerHTML = `
                    <div>Budget Initial : <strong style="color: #f8fafc;">${(pt.budget_ini || 500000).toLocaleString('fr-FR')} €</strong></div>
                    <div>Budget Utilisé : <strong style="color: var(--emerald);">${(pt.budget_used || 350000).toLocaleString('fr-FR')} €</strong></div>
                    <div>Avancement : <strong style="color: #38bdf8;">${pt.progress || 50}%</strong></div>
                    <div>Chef de Chantier : <strong>${pt.chef || 'A. Martin'}</strong></div>
                `;
            } else if (pt.category === 'marche_public_ref') {
                bMetrics.innerHTML = `
                    <div>Type de Marché : <strong style="color: #a855f7;">DCE Public Réel</strong></div>
                    <div>Budget Réalisé : <strong style="color: var(--emerald);">${(pt.budget_used || 900000).toLocaleString('fr-FR')} €</strong></div>
                    <div>Statut : <strong style="color: var(--emerald);">Achevé (100%)</strong></div>
                    <div>Rôle : <strong>Étalon Cadences & Prix</strong></div>
                `;
            } else if (pt.category === 'fournisseur') {
                bMetrics.innerHTML = `
                    <div>Produit Fourni : <strong style="color: #ec4899;">${pt.product || 'Matériaux'}</strong></div>
                    <div>Distance Siège : <strong>${pt.distance || '10 km'}</strong></div>
                    <div>Contrat-Cadre : <strong style="color: var(--emerald);">Agréé 2026</strong></div>
                    <div>Délai Livraison : <strong>H+2 sur site</strong></div>
                `;
            } else if (pt.category === 'depot') {
                bMetrics.innerHTML = `
                    <div>Valeur Stock : <strong style="color: var(--amber);">${pt.stock_val || '300 000 €'}</strong></div>
                    <div>Téléphone : <strong>${pt.contact || '04 67 00 00 00'}</strong></div>
                    <div>Horaires : <strong>06h30 - 18h00</strong></div>
                    <div>Atelier Engins : <strong style="color: var(--emerald);">Opérationnel</strong></div>
                `;
            } else {
                bMetrics.innerHTML = `
                    <div>Responsable : <strong style="color: #38bdf8;">${pt.leader || pt.rep || 'Contact'}</strong></div>
                    <div>Canal Radio : <strong style="color: var(--amber);">${pt.radio || 'Canal TP'}</strong></div>
                    <div>Statut : <strong style="color: var(--emerald);">En Poste Actif</strong></div>
                    <div>Localisation : <strong>Occitanie</strong></div>
                `;
            }
        }

        renderCockpitOsmMap();
    }

    // ==========================================
    // 5b. MULTI-ENTERPRISE PROFILES SWITCHER
    // ==========================================
    let currentCompanyProfile = 'occitanie_tp';

    const companyProfiles = {
        'occitanie_tp': {
            id: 'occitanie_tp',
            name: 'Occitanie TP & VRD SAS',
            type: 'PME Établie Régionale',
            caisse: 485200,
            bfr: 142800,
            capital: '500 000 €',
            siren: '849 321 654',
            desc: 'Entreprise générale de VRD et terrassement en Occitanie. Flotte complète 6 engins, marchés publics Alès, Sète, Pézenas, Montpellier.',
            projects_count: 4,
            fleet_count: 6,
            effectif_count: 24,
            margin: 14.2
        },
        'compte_neuf': {
            id: 'compte_neuf',
            name: 'Nouvelle Entreprise TP (Démarrage Zéro)',
            type: 'Compte Vierge / Typique',
            caisse: 0,
            bfr: 0,
            capital: '10 000 €',
            siren: '912 456 789',
            desc: 'Profil vierge sans fond ni chantier engagé. Idéal pour configurer et chiffrer une nouvelle entreprise TP à partir d\'une page blanche.',
            projects_count: 0,
            fleet_count: 0,
            effectif_count: 1,
            margin: 0
        },
        'stagiaire_tp': {
            id: 'stagiaire_tp',
            name: 'Stagiaire TP & Conduite de Travaux (Études M4-L)',
            type: 'Dossiers de Cours & Formation',
            caisse: 150000,
            bfr: 45000,
            capital: '150 000 €',
            siren: '775 889 123',
            desc: 'Simulation basée sur les cours et dossiers réels du repo : DCE Giratoire Barbazan M4-L, Lotissement Aurouer 2021, Déviation Noé, fiches de tâches et ratios FNTP.',
            projects_count: 3,
            fleet_count: 3,
            effectif_count: 9,
            margin: 12.8
        },
        'artisan_2k': {
            id: 'artisan_2k',
            name: 'Artisan TP Sud VRD (Perso 2k€ + Bureau + EPI)',
            type: 'Amorçage Artisanal 2 000 €',
            caisse: 2000,
            bfr: 1800,
            capital: '2 000 €',
            siren: '883 456 123',
            desc: 'Démarrage avec 2 000 € de capital, bureau loué en pépinière, lot complet d\'EPI certifiés (Casques, gilets Cl.2, chaussures S3), outillage laser et réfection tranchée.',
            projects_count: 1,
            fleet_count: 0,
            effectif_count: 2,
            margin: 18.5
        }
    };

    function switchCompanyProfile(profileId) {
        const prof = companyProfiles[profileId] || companyProfiles['occitanie_tp'];
        currentCompanyProfile = profileId;
        caisseBalance = prof.caisse;

        // Update active badges in modal
        document.querySelectorAll('.company-profile-card').forEach(c => {
            c.classList.remove('active');
            c.style.border = '1px solid rgba(51,65,85,0.8)';
        });
        const activeCard = document.getElementById('prof-card-' + profileId);
        if (activeCard) {
            activeCard.classList.add('active');
            activeCard.style.border = '2px solid var(--cyan)';
        }

        ['occitanie_tp', 'compte_neuf', 'stagiaire_tp', 'artisan_2k'].forEach(id => {
            const badge = document.getElementById('prof-active-badge-' + id);
            if (badge) badge.style.display = (id === profileId) ? 'inline-block' : 'none';
        });

        // Update Top HUD
        const topName = document.getElementById('active-company-name-top');
        const topCaisse = document.getElementById('caisse-balance-top');
        const compCaisse = document.getElementById('company-caisse-val');
        const kpiTreasury = document.getElementById('kpi-treasury-val');

        if (topName) topName.textContent = prof.name + ' ▾';
        if (topCaisse) topCaisse.textContent = prof.caisse.toLocaleString('fr-FR') + ' €';
        if (compCaisse) compCaisse.textContent = prof.caisse.toLocaleString('fr-FR') + ' €';
        if (kpiTreasury) kpiTreasury.textContent = prof.caisse.toLocaleString('fr-FR') + ' €';

        logCockpit('🏢 Profil entreprise activé : ' + prof.name, 'ok');
        closeModal('company-switch-modal');

        // Re-render active views
        try {
            if (currentNav === 'cockpit') renderCockpitOsmMap();
            if (currentNav === 'company') renderCompanyCashflowTable();
            if (currentNav === 'projects_hub') renderProjectsHub();
            if (currentNav === 'fleet') renderFleetGrid();
            if (currentNav === 'hr') { initHrTree(); renderHrPartners(); }
            if (currentNav === 'benchmark') { renderBenchmarkTable(); renderInventoryTable(); renderTeamsBenchmarkTable(); }
        } catch (e) {
            console.error('Error re-rendering after company profile switch:', e);
        }
    }

    // ==========================================
    // 6. COMPANY CASHFLOW TCD TABLE & FORMULAS
    // ==========================================
    function toggleCashflowFormulas() {
        showCashflowFormulas = !showCashflowFormulas;
        const box = document.getElementById('cashflow-formulas-box');
        if (box) box.style.display = showCashflowFormulas ? 'block' : 'none';
    }

    let cashflowSortKey = 'date';
    let cashflowSortAsc = false;

    function sortCashflowTable(key) {
        if (key === cashflowSortKey) {
            cashflowSortAsc = !cashflowSortAsc;
        } else {
            cashflowSortKey = key;
            cashflowSortAsc = true;
        }
        renderCompanyCashflowTable();
    }

    function renderCompanyCashflowTable() {
        const tbody = document.getElementById('company-cashflow-tbody') || document.getElementById('company-cashflow-table-body');
        if (!tbody) return;

        const txs = companyData.cashflow_transactions || [];
        const sorted = [...txs].sort((a, b) => {
            let valA = a[cashflowSortKey] !== undefined ? a[cashflowSortKey] : '';
            let valB = b[cashflowSortKey] !== undefined ? b[cashflowSortKey] : '';
            if (cashflowSortKey === 'amount') { valA = a.amount || 0; valB = b.amount || 0; }
            if (typeof valA === 'string') {
                return cashflowSortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
            }
            return cashflowSortAsc ? (valA - valB) : (valB - valA);
        });

        tbody.innerHTML = sorted.map(t => {
            const isPositive = t.amount > 0;
            const amtColor = isPositive ? 'var(--emerald)' : '#fb7185';
            const amtSign = isPositive ? '+' : '';
            return `
                <tr style="border-top: 1px solid rgba(51,65,85,0.4);">
                    <td style="padding: 0.55rem; font-family: 'JetBrains Mono'; color: #94a3b8;">${t.date}</td>
                    <td style="padding: 0.55rem;"><span class="badge ${isPositive ? 'badge-success' : 'badge-warning'}">${t.type}</span></td>
                    <td style="padding: 0.55rem; font-weight: 700; color: #f8fafc;">${t.label}</td>
                    <td style="padding: 0.55rem; text-align: right; font-weight: 800; font-family: 'JetBrains Mono'; color: ${amtColor};">${amtSign}${t.amount.toLocaleString('fr-FR')} €</td>
                    <td style="padding: 0.55rem; text-align: center;"><span class="badge badge-success">${t.status}</span></td>
                </tr>
            `;
        }).join('');
    }

    // ==========================================
    // 7. PROJECTS HUB & OWNERSHIP COMPARISON
    // ==========================================
    let currentProjectFilter = 'all';

    function filterProjectsHub(f, btn) {
        currentProjectFilter = f;
        document.querySelectorAll('.project-filter-btn').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
        renderProjectsHub();
    }

    function renderProjectsHub() {
        const grid = document.getElementById('projects-grid');
        if (!grid) return;

        const projects = companyData.projects || [];
        const filtered = projects.filter(p => {
            if (currentProjectFilter === 'internal') return !p.ownership.includes('DCE');
            if (currentProjectFilter === 'dce_ref') return p.ownership.includes('DCE');
            return true;
        });

        grid.innerHTML = filtered.map(p => `
            <div class="card" style="border: 1px solid rgba(51,65,85,0.8); background: rgba(15,23,42,0.95); display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
                        <div>
                            <div style="display: flex; gap: 0.4rem; align-items: center; margin-bottom: 4px;">
                                <span class="badge badge-info" style="font-size: 0.7rem; font-family: 'JetBrains Mono';">${p.id}</span>
                                <span class="badge badge-warning" style="font-size: 0.65rem;">${p.ownership || '🏢 Notre Entreprise'}</span>
                            </div>
                            <h3 style="font-size: 1.15rem; font-weight: 800; color: #f8fafc;">${p.name}</h3>
                            <div style="font-size: 0.8rem; color: #94a3b8;">📍 ${p.location} • MOA: <strong>${p.client}</strong></div>
                        </div>
                        <span class="badge badge-success">${p.status}</span>
                    </div>

                    <!-- FINANCIAL VS PHYSICAL PROGRESS DOUBLE JAUGE -->
                    <div style="margin: 0.75rem 0; background: rgba(30,41,59,0.5); padding: 0.6rem; border-radius: 6px;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #94a3b8; margin-bottom: 3px;">
                            <span>Avancement Physique : <strong style="color:#38bdf8;">${p.progress}%</strong></span>
                            <span>Budget Consommé : <strong style="color:var(--emerald);">${(p.budget_used || p.budget * 0.7).toLocaleString('fr-FR')} € / ${(p.budget).toLocaleString('fr-FR')} € (${Math.round(((p.budget_used || p.budget * 0.7) / p.budget) * 100)}%)</strong></span>
                        </div>
                        <div class="progress-bar-bg" style="height: 8px;">
                            <div class="progress-bar-fill" style="width: ${p.progress}%;"></div>
                        </div>
                    </div>

                    <!-- KEY METRICS -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; background: rgba(30,41,59,0.5); padding: 0.6rem; border-radius: 6px; font-size: 0.75rem; margin-bottom: 0.75rem;">
                        <div><span style="color: #64748b;">Conducteur:</span> <strong>${p.manager}</strong></div>
                        <div><span style="color: #64748b;">Chef Chantier:</span> <strong>${p.site_chief}</strong></div>
                        <div><span style="color: #64748b;">Délai Consommé:</span> <strong>${p.delai_consomme_pct || 75}%</strong></div>
                        <div><span style="color: #64748b;">Livraison:</span> <strong>${p.end}</strong></div>
                    </div>

                    <!-- ASSIGNED ASSETS PILLS -->
                    <div style="margin-bottom: 0.75rem;">
                        <div style="font-size: 0.7rem; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 4px;">Engins & Outillage Mobilisés :</div>
                        <div style="display: flex; flex-wrap: wrap; gap: 0.3rem;">
                            ${(p.assigned_machinery || []).map(m => `<span class="badge badge-warning" style="font-size: 0.65rem;">🚜 ${m.name}</span>`).join('')}
                            ${(p.assigned_tools || []).map(t => `<span class="badge badge-info" style="font-size: 0.65rem;">⚙️ ${t.name}</span>`).join('')}
                        </div>
                    </div>
                </div>

                <div>
                    <!-- DOWNLOADABLE PIECES -->
                    <div style="font-size: 0.7rem; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 4px;">Dossier Marché Téléchargeable :</div>
                    <div style="display: flex; flex-wrap: wrap; gap: 0.3rem; margin-bottom: 1rem;">
                        ${(p.docs || []).map(d => `
                            <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="downloadProjectDoc('${d.name}', '${p.name}', '${d.type}')">
                                📄 ${d.name} (.${d.type})
                            </button>
                        `).join('')}
                    </div>

                    <div style="display: flex; gap: 0.5rem; border-top: 1px solid rgba(51,65,85,0.5); padding-top: 0.75rem;">
                        <button class="btn btn-primary" style="flex: 1; font-size: 0.85rem;" onclick="openProjectModal('${p.id}')">🔍 Fiche Complète, SIG & Lots</button>
                        <button class="btn btn-secondary" style="font-size: 0.85rem;" onclick="switchNav('planning')">📅 Planning</button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    function openProjectModal(projectId) {
        activeProjectModalId = projectId;
        activeProjectModalLotIdx = 0;
        const project = (companyData.projects || []).find(p => p.id === projectId) || (companyData.projects || [])[0];
        if (!project) return;

        const body = document.getElementById('project-modal-body');
        if (!body) return;

        body.innerHTML = `
            <!-- HEADER -->
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.25rem; border-bottom: 1px solid rgba(51,65,85,0.7); padding-bottom: 0.75rem;">
                <div>
                    <div style="display:flex; gap:0.4rem; align-items:center; margin-bottom:4px;">
                        <span class="badge badge-info" style="font-size: 0.75rem; font-family: 'JetBrains Mono';">${project.id}</span>
                        <span class="badge badge-warning" style="font-size: 0.7rem;">${project.ownership || '🏢 Notre Entreprise'}</span>
                    </div>
                    <h2 style="font-size: 1.4rem; font-weight: 900; color: #38bdf8; margin-top: 2px;">${project.name}</h2>
                    <div style="font-size: 0.85rem; color: #94a3b8;">📍 ${project.location} • Client : <strong>${project.client}</strong> • Budget Initial : <strong>${(project.budget).toLocaleString('fr-FR')} € HT</strong></div>
                </div>
                <div style="text-align: right;">
                    <span class="badge badge-success" style="font-size: 0.85rem;">Statut : ${project.status}</span>
                    <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">Budget Utilisé : <strong style="color:var(--emerald);">${(project.budget_used || project.budget * 0.7).toLocaleString('fr-FR')} €</strong></div>
                </div>
            </div>

            <!-- 1. BARRE DE PROGRESSION DU CHANTIER / LIGNE TEMPORELLE AVEC NOEUDS ÉTAPES -->
            <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(51,65,85,0.8); border-radius: 8px; padding: 1.25rem; margin-bottom: 1.25rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1rem;">
                    <div style="font-size: 0.85rem; font-weight: 800; color: #f8fafc; text-transform: uppercase;">
                        ⏳ Progression Chronologique & Nœuds d'Étapes VRD
                    </div>
                    <span class="badge badge-success" style="font-size: 0.8rem;">Avancement Physique : ${project.progress}%</span>
                </div>

                <!-- HORIZONTAL NODE TIMELINE -->
                <div style="position: relative; padding: 1.5rem 0.5rem 0.5rem; overflow-x: auto;">
                    <div style="position: absolute; top: 38px; left: 30px; right: 30px; height: 4px; background: rgba(51,65,85,0.8); z-index: 1;">
                        <div style="height: 100%; width: ${project.progress}%; background: linear-gradient(90deg, #10b981, #38bdf8); border-radius: 2px;"></div>
                    </div>

                    <div style="display: flex; justify-content: space-between; position: relative; z-index: 2; min-width: 650px;">
                        ${(project.timeline_steps || []).map((st, idx) => {
                            const isDone = st.progress === 100;
                            const isInProgress = st.progress > 0 && st.progress < 100;
                            const nodeBg = isDone ? '#10b981' : (isInProgress ? '#38bdf8' : '#1e293b');
                            const nodeBorder = isDone ? '#059669' : (isInProgress ? '#0284c7' : '#475569');
                            const nodeTextColor = isDone ? '#0f172a' : '#f8fafc';
                            return `
                                <div style="display: flex; flex-direction: column; align-items: center; width: 90px; text-align: center;">
                                    <div style="width: 32px; height: 32px; border-radius: 50%; background: ${nodeBg}; border: 3px solid ${nodeBorder}; color: ${nodeTextColor}; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 0.85rem; box-shadow: 0 0 10px rgba(0,0,0,0.5);">
                                        ${isDone ? '✓' : st.step}
                                    </div>
                                    <div style="font-size: 0.72rem; font-weight: 800; color: ${isInProgress ? '#38bdf8' : '#f8fafc'}; margin-top: 8px; line-height: 1.2;">
                                        ${st.name}
                                    </div>
                                    <div style="font-size: 0.65rem; color: #94a3b8; margin-top: 2px;">${st.date}</div>
                                    <span class="badge ${isDone ? 'badge-success' : (isInProgress ? 'badge-info' : 'badge-warning')}" style="font-size: 0.6rem; padding: 1px 4px; margin-top: 4px;">
                                        ${st.progress}%
                                    </span>
                                </div>
                            `;
                        }).join('')}
                    </div>
                </div>
            </div>

            <!-- 2. SATELLITE & MULTI-LAYER GIS MAP CANVAS -->
            <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(51,65,85,0.8); border-radius: 8px; padding: 1rem; margin-bottom: 1.25rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
                    <div>
                        <div style="font-size: 0.85rem; font-weight: 800; color: #38bdf8; text-transform: uppercase;">
                            🗺️ SIG Chantier : Image Satellite HD & Calques Réglementaires
                        </div>
                        <div style="font-size: 0.75rem; color: #94a3b8;">Délimitation géoréférencée, réseaux DICT classe A et simulation 3D/4D</div>
                    </div>

                    <!-- GIS LAYER BUTTONS -->
                    <div style="display: flex; gap: 0.3rem; flex-wrap: wrap;">
                        <button class="btn-secondary gis-layer-btn ${activeGisLayer === 'dict' ? 'active' : ''}" onclick="switchGisLayer('dict')">⚡ DICT Réseaux</button>
                        <button class="btn-secondary gis-layer-btn ${activeGisLayer === 'satellite' ? 'active' : ''}" onclick="switchGisLayer('satellite')">🛰️ Satellite HD</button>
                        <button class="btn-secondary gis-layer-btn ${activeGisLayer === 'osm' ? 'active' : ''}" onclick="switchGisLayer('osm')">🗺️ Cadastre / OSM</button>
                        <button class="btn-secondary gis-layer-btn ${activeGisLayer === '3d' ? 'active' : ''}" onclick="switchGisLayer('3d')">📐 3D Isométrique</button>
                        <button class="btn-secondary gis-layer-btn ${activeGisLayer === 'ar' ? 'active' : ''}" onclick="switchGisLayer('ar')">🥽 AR / VR</button>
                        <button class="btn-secondary gis-layer-btn ${activeGisLayer === 'pov' ? 'active' : ''}" onclick="switchGisLayer('pov')">📹 POV Chantier</button>
                    </div>
                </div>

                <!-- GIS CANVAS CONTAINER -->
                <div style="height: 280px; background: #000; border: 1px solid rgba(56,189,248,0.4); border-radius: 6px; position: relative; overflow: hidden;">
                    <canvas id="project-gis-canvas" style="width: 100%; height: 100%;"></canvas>
                    
                    <!-- LAYER INFO HUD OVERLAY -->
                    <div id="gis-layer-hud" style="position: absolute; bottom: 8px; left: 8px; background: rgba(15,23,42,0.9); padding: 4px 10px; border-radius: 4px; font-family: 'JetBrains Mono'; font-size: 0.75rem; color: #38bdf8; border: 1px solid rgba(56,189,248,0.3);">
                        CALQUE : DICT RÉSEAUX (GAZ MPB • ÉLEC HTA • AEP • FIBRE)
                    </div>
                    <div style="position: absolute; top: 8px; right: 8px; background: rgba(15,23,42,0.9); padding: 4px 8px; border-radius: 4px; font-family: 'JetBrains Mono'; font-size: 0.7rem; color: var(--emerald);">
                        GPS: 44.1284° N, 4.0833° E • Précision RTK ±1cm
                    </div>
                </div>
            </div>

            <!-- 3. ASSIGNED ASSETS (ENGINS, OUTILLAGE, MATÉRIAUX) -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; margin-bottom: 1.25rem;">
                <div style="background: rgba(15,23,42,0.7); border: 1px solid rgba(51,65,85,0.6); padding: 0.75rem; border-radius: 8px;">
                    <div style="font-size: 0.8rem; font-weight: 800; color: var(--amber); margin-bottom: 0.5rem;">🚜 Machines & Engins Assignés</div>
                    <div style="display: flex; flex-direction: column; gap: 0.35rem;">
                        ${(project.assigned_machinery || []).map(m => `
                            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; background: rgba(30,41,59,0.6); padding: 4px 8px; border-radius: 4px;">
                                <span>${m.name}</span>
                                <span class="badge badge-warning" style="font-size: 0.65rem;">${m.type}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div style="background: rgba(15,23,42,0.7); border: 1px solid rgba(51,65,85,0.6); padding: 0.75rem; border-radius: 8px;">
                    <div style="font-size: 0.8rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.5rem;">⚙️ Petit Outillage & Lasers</div>
                    <div style="display: flex; flex-direction: column; gap: 0.35rem;">
                        ${(project.assigned_tools || []).map(t => `
                            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; background: rgba(30,41,59,0.6); padding: 4px 8px; border-radius: 4px;">
                                <span>${t.name}</span>
                                <span class="badge badge-info" style="font-size: 0.65rem;">${t.type}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div style="background: rgba(15,23,42,0.7); border: 1px solid rgba(51,65,85,0.6); padding: 0.75rem; border-radius: 8px;">
                    <div style="font-size: 0.8rem; font-weight: 800; color: var(--emerald); margin-bottom: 0.5rem;">🧱 Matériaux & Consommables Livrés</div>
                    <div style="display: flex; flex-direction: column; gap: 0.35rem;">
                        ${(project.assigned_materials || []).map(mat => `
                            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; background: rgba(30,41,59,0.6); padding: 4px 8px; border-radius: 4px;">
                                <span>${mat.name}</span>
                                <span style="color: var(--emerald); font-weight: 700;">${mat.qty}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>

            <!-- 4. LOTS BREAKDOWN & TECHNICAL/ADMINISTRATIVE EXECUTION STEPS -->
            <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(51,65,85,0.8); border-radius: 8px; padding: 1.25rem;">
                <div style="font-size: 0.85rem; font-weight: 800; color: #f8fafc; text-transform: uppercase; margin-bottom: 0.75rem;">
                    📑 Décomposition des Lots du Marché & Fiches d'Exécution
                </div>

                <!-- LOT SELECTOR TABS -->
                <div style="display: flex; gap: 0.4rem; margin-bottom: 1rem; flex-wrap: wrap;">
                    ${(project.lots_breakdown || []).map((lot, idx) => `
                        <button class="btn-secondary project-lot-tab-btn ${idx === activeProjectModalLotIdx ? 'active' : ''}" onclick="selectProjectModalLot(${idx})">
                            Lot ${lot.lot} : ${lot.name} (${lot.progress}%)
                        </button>
                    `).join('')}
                </div>

                <!-- SELECTED LOT DETAILS -->
                <div id="project-lot-content-area">
                    <!-- Populated dynamically by selectProjectModalLot() -->
                </div>
            </div>
        `;

        openModal('project-details-modal');
        setTimeout(() => {
            renderGisCanvas();
            selectProjectModalLot(0);
        }, 50);
    }

    function switchGisLayer(layerName) {
        activeGisLayer = layerName;
        document.querySelectorAll('.gis-layer-btn').forEach(b => b.classList.remove('active'));
        const activeBtn = Array.from(document.querySelectorAll('.gis-layer-btn')).find(b => b.textContent.toLowerCase().includes(layerName));
        if (activeBtn) activeBtn.classList.add('active');

        const hud = document.getElementById('gis-layer-hud');
        if (hud) {
            if (layerName === 'dict') hud.textContent = 'CALQUE : DICT RÉSEAUX (GAZ MPB • ÉLEC HTA • AEP • FIBRE)';
            if (layerName === 'satellite') hud.textContent = 'CALQUE : IMAGERIE SATELLITE HD OCCITANIE 10CM/PX';
            if (layerName === 'osm') hud.textContent = 'CALQUE : OPENSTREETMAP / PARCELLAIRE CADASTRE DGI';
            if (layerName === '3d') hud.textContent = 'CALQUE : MNT MODÈLE NUMÉRIQUE DE TERRAIN 3D LIDAR';
            if (layerName === 'ar') hud.textContent = 'CALQUE : RÉALITÉ AUGMENTÉE (AR) RÉSEAUX ENTERRÉS';
            if (layerName === 'pov') hud.textContent = 'CALQUE : POV CAMÉRA CHANTIER PTZ TEMPS RÉEL';
        }

        renderGisCanvas();
    }

    function renderGisCanvas() {
        const canvas = document.getElementById('project-gis-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const w = canvas.parentElement.clientWidth || 700;
        const h = canvas.parentElement.clientHeight || 280;
        canvas.width = w;
        canvas.height = h;

        if (activeGisLayer === 'satellite') {
            ctx.fillStyle = '#1c2826';
            ctx.fillRect(0, 0, w, h);
            for (let i = 0; i < 60; i++) {
                ctx.fillStyle = i % 2 === 0 ? 'rgba(34, 56, 45, 0.4)' : 'rgba(50, 40, 30, 0.3)';
                ctx.fillRect(Math.random() * w, Math.random() * h, Math.random() * 80 + 20, Math.random() * 80 + 20);
            }
        } else if (activeGisLayer === 'osm') {
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(0, 0, w, h);
            ctx.strokeStyle = '#334155';
            ctx.lineWidth = 1;
            for (let x = 40; x < w; x += 80) {
                ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
            }
            for (let y = 30; y < h; y += 60) {
                ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
            }
        } else {
            ctx.fillStyle = '#090d16';
            ctx.fillRect(0, 0, w, h);
        }

        // Draw Site Boundary Polygon
        ctx.strokeStyle = '#eab308';
        ctx.lineWidth = 3;
        ctx.setLineDash([8, 4]);
        ctx.beginPath();
        ctx.moveTo(w * 0.15, h * 0.25);
        ctx.lineTo(w * 0.75, h * 0.2);
        ctx.lineTo(w * 0.85, h * 0.75);
        ctx.lineTo(w * 0.25, h * 0.85);
        ctx.closePath();
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = 'rgba(234, 179, 8, 0.08)';
        ctx.fill();

        ctx.fillStyle = '#eab308';
        ctx.font = 'bold 11px system-ui';
        ctx.fillText('🚧 EMPRISE CHANTIER AUTORISÉE', w * 0.18, h * 0.32);

        // Draw DICT Networks
        if (activeGisLayer === 'dict' || activeGisLayer === 'ar' || activeGisLayer === 'satellite') {
            ctx.strokeStyle = '#eab308';
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(w * 0.1, h * 0.5);
            ctx.lineTo(w * 0.9, h * 0.5);
            ctx.stroke();
            ctx.fillStyle = '#eab308';
            ctx.fillText('⚡ GAZ MPB PEHD Ø110 (Piquetage J+1)', w * 0.45, h * 0.48);

            ctx.strokeStyle = '#ef4444';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(w * 0.2, h * 0.15);
            ctx.lineTo(w * 0.8, h * 0.85);
            ctx.stroke();
            ctx.fillStyle = '#ef4444';
            ctx.fillText('🔴 HTA 20kV ENEDIS', w * 0.6, h * 0.7);

            ctx.strokeStyle = '#0284c7';
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(w * 0.15, h * 0.7);
            ctx.lineTo(w * 0.85, h * 0.35);
            ctx.stroke();
            ctx.fillStyle = '#38bdf8';
            ctx.fillText('💧 AEP Fonte Ø150', w * 0.2, h * 0.65);
        }

        // Machinery Marker
        ctx.fillStyle = '#f59e0b';
        ctx.beginPath();
        ctx.arc(w * 0.48, h * 0.4, 8, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 10px monospace';
        ctx.fillText('🚜 Pelle R924 (RTK)', w * 0.5, h * 0.39);

        // North Arrow
        ctx.fillStyle = '#38bdf8';
        ctx.beginPath();
        ctx.moveTo(w - 25, 25);
        ctx.lineTo(w - 30, 45);
        ctx.lineTo(w - 20, 45);
        ctx.closePath();
        ctx.fill();
        ctx.fillText('N', w - 28, 20);
    }

    function selectProjectModalLot(lotIdx) {
        activeProjectModalLotIdx = lotIdx;
        document.querySelectorAll('.project-lot-tab-btn').forEach((b, i) => {
            b.classList.toggle('active', i === lotIdx);
        });

        const project = (companyData.projects || []).find(p => p.id === activeProjectModalId) || (companyData.projects || [])[0];
        const lot = (project.lots_breakdown || [])[lotIdx];
        const area = document.getElementById('project-lot-content-area');
        if (!lot || !area) return;

        area.innerHTML = `
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div style="background: rgba(30,41,59,0.7); border: 1px solid rgba(56,189,248,0.4); padding: 1rem; border-radius: 6px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.6rem;">
                        <span style="font-weight: 800; color: #38bdf8; font-size: 0.85rem;">🔧 Étapes d'Exécution Techniques & Tolérances</span>
                        <span class="badge badge-info" style="font-size:0.65rem;">Lot ${lot.lot}</span>
                    </div>
                    <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.8rem; color: #cbd5e1; line-height: 1.6;">
                        ${(lot.tech_steps || []).map(st => `<li>${st}</li>`).join('')}
                    </ul>
                </div>

                <div style="background: rgba(30,41,59,0.7); border: 1px solid rgba(16,185,129,0.4); padding: 1rem; border-radius: 6px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.6rem;">
                        <span style="font-weight: 800; color: var(--emerald); font-size: 0.85rem;">📋 Démarches Administratives & Réglementaires</span>
                        <span class="badge badge-success" style="font-size:0.65rem;">Conformité MOE/MOA</span>
                    </div>
                    <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.8rem; color: #cbd5e1; line-height: 1.6;">
                        ${(lot.admin_steps || []).map(st => `<li>${st}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
    }

    // ==========================================
    // 8. AI AGENTS HUB MODAL
    // ==========================================
    function openAiAgentModal() {
        const body = document.getElementById('employee-modal-body');
        if (!body) return;

        const agents = companyData.ai_agents || [];
        body.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; border-bottom: 1px solid rgba(51,65,85,0.7); padding-bottom: 0.75rem;">
                <div>
                    <span class="badge badge-success" style="font-size: 0.75rem;">Système Multi-Agents Autonomes TP</span>
                    <h2 style="font-size: 1.3rem; font-weight: 900; color: var(--emerald); margin-top: 4px;">🤖 Hub d'Intelligence Artificielle & Recommandations Temps Réel</h2>
                </div>
                <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem;" onclick="closeModal('employee-detail-modal')">✕</button>
            </div>

            <div style="display: flex; flex-direction: column; gap: 0.75rem; max-height: 480px; overflow-y: auto;">
                ${agents.map(a => `
                    <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(56,189,248,0.3); border-left: 4px solid ${a.color || '#38bdf8'}; border-radius: 6px; padding: 0.85rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                            <span style="font-weight: 800; font-size: 0.95rem; color: ${a.color || '#38bdf8'};">🤖 ${a.name}</span>
                            <span class="badge badge-success" style="font-size: 0.65rem;">${a.status || 'Actif'}</span>
                        </div>
                        <div style="font-size: 0.8rem; color: #cbd5e1; margin-bottom: 6px;">${a.desc}</div>
                        <div style="background: rgba(30,41,59,0.6); padding: 0.5rem; border-radius: 4px; font-size: 0.75rem; color: #facc15;">
                            💡 <strong>Recommandation Active :</strong> ${a.recommendation || 'Paramètres nominaux optimaux.'}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

        openModal('employee-detail-modal');
    }

    // ==========================================
    // 9. PLANNING ENGINE (AGENDA & GANTT & COMPAGNON)
    // ==========================================
    function setPlanningViewMode(mode) {
        planningViewMode = mode;
        document.querySelectorAll('.planning-mode-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('btn-plan-' + mode)?.classList.add('active');

        const agendaView = document.getElementById('planning-agenda-view');
        const ganttView = document.getElementById('planning-gantt-view');
        if (mode === 'agenda_week') {
            if (agendaView) agendaView.style.display = 'block';
            if (ganttView) ganttView.style.display = 'none';
            renderPlanningAgenda();
        } else {
            if (agendaView) agendaView.style.display = 'none';
            if (ganttView) ganttView.style.display = 'block';
            renderPlanningGantt();
        }
    }

    function changeAgendaWeek(delta) {
        currentAgendaWeekOffset += delta;
        renderPlanningAgenda();
    }

    function resetAgendaWeek() {
        currentAgendaWeekOffset = 0;
        renderPlanningAgenda();
    }

    const agendaTeamsData = [
        {
            team_id: 'team_a',
            team_name: 'Équipe VRD A (Mamadou Traoré)',
            chief: 'Mamadou TRAORÉ',
            site: 'Giratoire RD906 Alès',
            size: 5,
            schedule: [
                { id: 'tsk_101', day: 'Lundi', task: 'Pose bordures T2 Giratoire Alès', project: 'Giratoire RD906 Alès', color: '#0284c7', hours: '07h30 - 16h30', volume: '120 ml', progress: 100, team: 'M. Traoré + 4 ouvriers', gear: 'Pelle Liebherr R924, Laser Piper 200', safety: 'Port gants anti-coupure et chaussures S3.' },
                { id: 'tsk_102', day: 'Mardi', task: 'Calage béton C25/30 semelle bordures', project: 'Giratoire RD906 Alès', color: '#0284c7', hours: '07h30 - 16h30', volume: '24 m³', progress: 85, team: 'M. Traoré + 4 ouvriers', gear: 'Camion Toupie, Aiguille vibrante', safety: 'Lunettes de protection projection laitance.' },
                { id: 'tsk_103', day: 'Mercredi', task: 'Terrassement tranchée assainissement EP', project: 'Giratoire RD906 Alès', color: '#eab308', hours: '07h30 - 16h30', volume: '45 ml (prof 2.20m)', progress: 60, team: 'M. Traoré + Pelleur', gear: 'Pelle Liebherr R924, Caisson blindage', safety: 'Blindage obligatoire dès 1.30m (R4534).' },
                { id: 'tsk_104', day: 'Jeudi', task: 'Pose collecteur Béton 135A Ø400', project: 'Giratoire RD906 Alès', color: '#eab308', hours: '07h30 - 16h30', volume: '30 ml', progress: 30, team: 'M. Traoré + Poseur', gear: 'Laser canalisateur Piper 200', safety: 'Vérification absence de réseau gaz sous tension.' },
                { id: 'tsk_105', day: 'Vendredi', task: 'Remblaiement GNT 0/31.5 & Compactage', project: 'Giratoire RD906 Alès', color: '#10b981', hours: '07h30 - 15h30', volume: '60 m³', progress: 0, team: 'M. Traoré + 3 ouvriers', gear: 'Pilonneuse Wacker, Compacteur Bomag', safety: 'Protection auditive 85dB obligatoire.' }
            ]
        },
        {
            team_id: 'team_b',
            team_name: 'Équipe Réseaux Secs B (Karim Benali)',
            chief: 'Karim BENALI',
            site: 'ZAC Littoral Sète',
            size: 4,
            schedule: [
                { id: 'tsk_201', day: 'Lundi', task: 'Aiguillage fourreaux TPC Ø110 Fibre', project: 'ZAC Littoral Sète', color: '#10b981', hours: '08h00 - 16h30', volume: '350 ml', progress: 100, team: 'K. Benali + 3 ouvriers', gear: 'Aiguille fibre 150m, Compresseur', safety: 'Balisage chantier mobile classe A.' },
                { id: 'tsk_202', day: 'Mardi', task: 'Tirage câbles éclairage public LED', project: 'ZAC Littoral Sète', color: '#10b981', hours: '08h00 - 16h30', volume: '180 ml', progress: 90, team: 'K. Benali + 3 ouvriers', gear: 'Dérouleuse touret', safety: 'Habilitation électrique H0B0 requise.' },
                { id: 'tsk_203', day: 'Mercredi', task: 'Scellement massifs candélabres 1.00m', project: 'ZAC Littoral Sète', color: '#38bdf8', hours: '08h00 - 16h30', volume: '8 massifs', progress: 50, team: 'K. Benali + 3 ouvriers', gear: 'Mini-pelle Mecalac 6MCR', safety: 'Manutention élingues conformes CMU 1T.' },
                { id: 'tsk_204', day: 'Jeudi', task: 'Raccordement coffret télégestion C100', project: 'ZAC Littoral Sète', color: '#38bdf8', hours: '08h00 - 16h30', volume: '2 armoires', progress: 20, team: 'K. Benali', gear: 'Valise électricien normée', safety: 'Cadenassage consignation BT.' },
                { id: 'tsk_205', day: 'Vendredi', task: 'Essais diélectriques & Récolement DAO', project: 'ZAC Littoral Sète', color: '#c084fc', hours: '08h00 - 15h30', volume: '1 dossier', progress: 0, team: 'K. Benali + Topographe', gear: 'Contrôleur Fluke, Canne GPS RTK', safety: 'Contrôle APAVE validé.' }
            ]
        },
        {
            team_id: 'team_c',
            team_name: 'Équipe Enrobés C (Patrick Durand)',
            chief: 'Patrick DURAND',
            site: 'Centre Ancien Pézenas',
            size: 6,
            schedule: [
                { id: 'tsk_301', day: 'Lundi', task: 'Rabotage enrobés existants prof 5cm', project: 'Centre Ancien Pézenas', color: '#f59e0b', hours: '07h00 - 16h00', volume: '1 200 m²', progress: 100, team: 'P. Durand + 5 ouvriers', gear: 'Raboteuse Wirtgen 1m, Camion 8x4', safety: 'Arrosage anti-poussière continue.' },
                { id: 'tsk_302', day: 'Mardi', task: 'Application émulsion d\'accrochage C65B4', project: 'Centre Ancien Pézenas', color: '#f59e0b', hours: '07h00 - 16h00', volume: '1 200 m²', progress: 100, team: 'P. Durand + 2 ouvriers', gear: 'Bouille d\'émulsion automatique', safety: 'Masque à cartouche vapeurs bitume.' },
                { id: 'tsk_303', day: 'Mercredi', task: 'Mise en œuvre BBSG 0/10 à 160°C', project: 'Centre Ancien Pézenas', color: '#ef4444', hours: '06h30 - 16h30', volume: '180 tonnes', progress: 75, team: 'P. Durand + 5 ouvriers', gear: 'Finisseur Vögele, Compacteur Tandem', safety: 'Vêtements thermiques et gants haute T°.' },
                { id: 'tsk_304', day: 'Jeudi', task: 'Compactage de finition & Joints chanfrein', project: 'Centre Ancien Pézenas', color: '#ef4444', hours: '07h00 - 16h00', volume: '1 200 m²', progress: 40, team: 'P. Durand + 3 ouvriers', gear: 'Compacteur vibrant Bomag BW 120', safety: 'Contrôle température thermomètre IR.' },
                { id: 'tsk_305', day: 'Vendredi', task: 'Nettoyage balayeuse & Libération voie', project: 'Centre Ancien Pézenas', color: '#10b981', hours: '07h00 - 14h00', volume: '1 site', progress: 0, team: 'P. Durand + 2 ouvriers', gear: 'Balayeuse aspiratrice Ravo', safety: 'Dépose de la signalisation OPBTP.' }
            ]
        },
        {
            team_id: 'team_topo',
            team_name: 'Cellule Topo (David Lemoine)',
            chief: 'David LEMOINE',
            site: 'Voie Verte Montpellier',
            size: 2,
            schedule: [
                { id: 'tsk_401', day: 'Lundi', task: 'Implantation bornes GPS RTK Voie Verte', project: 'Voie Verte Montpellier', color: '#c084fc', hours: '08h00 - 16h30', volume: '12 bornes', progress: 100, team: 'D. Lemoine + 1 aide', gear: 'Canne GPS RTK Leica', safety: 'Gilet classe 3 et casque obligatoire.' },
                { id: 'tsk_402', day: 'Mardi', task: 'Vol drone photogrammétrie MNT bassin', project: 'Voie Verte Montpellier', color: '#c084fc', hours: '08h00 - 16h30', volume: '1 mission', progress: 100, team: 'D. Lemoine', gear: 'Drone DJI Matrice RTK', safety: 'Protocole DGAC & zone sécurisée.' },
                { id: 'tsk_403', day: 'Mercredi', task: 'Contrôle altimétrique pentes noues', project: 'Voie Verte Montpellier', color: '#38bdf8', hours: '08h00 - 16h30', volume: '450 ml', progress: 70, team: 'D. Lemoine', gear: 'Niveau optique Leica NA2', safety: 'Tolérance ±5mm respectée.' },
                { id: 'tsk_404', day: 'Jeudi', task: 'Levé de récolement classe A réseaux', project: 'Voie Verte Montpellier', color: '#38bdf8', hours: '08h00 - 16h30', volume: '1 dossier', progress: 30, team: 'D. Lemoine', gear: 'GPS Leica GS18 T', safety: 'Marquage piquetage vérifié.' },
                { id: 'tsk_405', day: 'Vendredi', task: 'Compilation DAO et export format IFC', project: 'Voie Verte Montpellier', color: '#10b981', hours: '08h00 - 15h30', volume: '1 maquette', progress: 0, team: 'D. Lemoine', gear: 'Station DAO Covadis', safety: 'DOE prêt pour MOE.' }
            ]
        }
    ];

    function renderPlanningAgenda() {
        const container = document.getElementById('planning-agenda-view');
        if (!container) return;

        const projFilter = document.getElementById('planning-project-select')?.value || 'all';
        const teamFilter = document.getElementById('planning-team-select')?.value || 'all';

        const filteredTeams = agendaTeamsData.filter(t => {
            if (teamFilter !== 'all' && t.team_id !== teamFilter) return false;
            return true;
        });

        const days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi'];
        const baseDate = new Date(2026, 4, 18 + currentAgendaWeekOffset * 7);
        const weekDates = days.map((d, i) => {
            const dt = new Date(baseDate);
            dt.setDate(dt.getDate() + i);
            return `${d} ${dt.getDate().toString().padStart(2, '0')}/${(dt.getMonth() + 1).toString().padStart(2, '0')}`;
        });

        container.innerHTML = `
            <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(51,65,85,0.7); border-radius: 8px; overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; min-width: 900px;">
                    <thead>
                        <tr style="background: rgba(30,41,59,0.9); color: #94a3b8; font-size: 0.8rem; text-align: center;">
                            <th style="padding: 0.75rem; text-align: left; width: 220px;">ÉQUIPE & EFFECTIF</th>
                            ${weekDates.map(wd => `<th style="padding: 0.75rem; width: 180px; border-left: 1px solid rgba(51,65,85,0.5);">${wd}</th>`).join('')}
                        </tr>
                    </thead>
                    <tbody>
                        ${filteredTeams.map(t => `
                            <tr style="border-top: 1px solid rgba(51,65,85,0.5);">
                                <td style="padding: 0.75rem; vertical-align: top; background: rgba(30,41,59,0.3);">
                                    <div style="font-weight: 800; font-size: 0.85rem; color: #38bdf8;">${t.team_name}</div>
                                    <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 2px;">Chef: <strong>${t.chief}</strong></div>
                                    <span class="badge badge-success" style="font-size: 0.65rem; margin-top: 4px;">👥 ${t.size} Compagnons</span>
                                </td>
                                ${days.map((d, dayIdx) => {
                                    const tsk = (t.schedule || []).find(s => s.day === d);
                                    if (!tsk) return `<td style="padding: 0.5rem; border-left: 1px solid rgba(51,65,85,0.5); background: rgba(15,23,42,0.4); text-align: center; color: #64748b; font-size: 0.75rem;">Repos / Transfert</td>`;
                                    
                                    if (projFilter !== 'all' && !tsk.project.toLowerCase().includes(projFilter.replace('projet_', ''))) {
                                        return `<td style="padding: 0.5rem; border-left: 1px solid rgba(51,65,85,0.5); background: rgba(15,23,42,0.4); text-align: center; color: #64748b; font-size: 0.75rem;">Autre chantier</td>`;
                                    }

                                    return `
                                        <td style="padding: 0.5rem; border-left: 1px solid rgba(51,65,85,0.5); vertical-align: top;">
                                            <div onclick="openTaskDetailModal('${tsk.id}', '${t.team_id}', ${dayIdx})" style="background: rgba(15,23,42,0.95); border: 1px solid ${tsk.color}; border-left: 4px solid ${tsk.color}; border-radius: 6px; padding: 0.5rem; cursor: pointer; transition: transform 0.15s, box-shadow 0.15s;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.5)';" onmouseout="this.style.transform='none'; this.style.boxShadow='none';">
                                                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 3px;">
                                                    <span style="font-size: 0.65rem; font-family: 'JetBrains Mono'; color: ${tsk.color}; font-weight: 700;">${tsk.hours}</span>
                                                    <span class="badge badge-info" style="font-size: 0.6rem; padding: 1px 4px;">${tsk.progress}%</span>
                                                </div>
                                                <div style="font-size: 0.75rem; font-weight: 800; color: #f8fafc; line-height: 1.25; margin-bottom: 4px;">
                                                    ${tsk.task}
                                                </div>
                                                <div style="font-size: 0.68rem; color: #94a3b8; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                                                    📍 ${tsk.project}
                                                </div>
                                                <div style="margin-top: 4px; display: flex; justify-content: space-between; font-size: 0.65rem; color: #64748b;">
                                                    <span>Vol: ${tsk.volume}</span>
                                                    <span style="color: #38bdf8;">🔍 Inspecter</span>
                                                </div>
                                            </div>
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

    // COMPAGNON DEDICATED DIRECT PLANNING RENDERER
    function renderCompagnonPlanning() {
        const container = document.getElementById('compagnon-planning-container');
        if (!container) return;

        const teamSelect = document.getElementById('compagnon-team-select');
        const teamId = teamSelect ? teamSelect.value : 'team_a';
        const team = agendaTeamsData.find(t => t.team_id === teamId) || agendaTeamsData[0];

        const siteLabel = document.getElementById('compagnon-current-site');
        if (siteLabel) siteLabel.textContent = team.site;

        const todayTask = (team.schedule || [])[0]; // Monday / Today
        const nextTasks = (team.schedule || []).slice(1);

        container.innerHTML = `
            <!-- TODAY'S ACTIVE MISSION -->
            <div style="background: rgba(15,23,42,0.95); border: 2px solid #38bdf8; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; box-shadow: 0 4px 15px rgba(56,189,248,0.15);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                    <span class="badge badge-success" style="font-size:0.75rem;">🚀 MA MISSION DU JOUR (${todayTask.day})</span>
                    <span style="font-family:'JetBrains Mono'; font-weight:700; color:#38bdf8; font-size:0.8rem;">${todayTask.hours}</span>
                </div>
                <h3 style="font-size:1.15rem; font-weight:900; color:#f8fafc; margin-bottom:0.4rem;">${todayTask.task}</h3>
                <div style="font-size:0.8rem; color:#94a3b8; margin-bottom:0.6rem;">📍 Chantier : <strong>${todayTask.project}</strong> • Objectif : <strong style="color:var(--emerald);">${todayTask.volume}</strong></div>

                <div style="background:rgba(30,41,59,0.6); padding:0.6rem; border-radius:6px; font-size:0.75rem; margin-bottom:0.75rem;">
                    <div>🚜 <strong>Engins & Outils :</strong> ${todayTask.gear}</div>
                    <div style="margin-top:2px; color:#facc15;">🦺 <strong>Sécurité AIPR :</strong> ${todayTask.safety}</div>
                </div>

                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <button class="btn btn-primary" style="font-size:0.8rem;" onclick="openTaskDetailModal('${todayTask.id}', '${team.team_id}', 0)">🔍 Détails & Pointer Avancement</button>
                    <span class="badge badge-info" style="font-size:0.75rem;">Avancement : ${todayTask.progress}%</span>
                </div>
            </div>

            <!-- WEEKLY UPCOMING SCHEDULE -->
            <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(51,65,85,0.7); border-radius: 8px; padding: 0.85rem;">
                <div style="font-size:0.8rem; font-weight:800; color:#94a3b8; text-transform:uppercase; margin-bottom:0.5rem;">📅 Suite du Planning cette Semaine (${team.team_name}) :</div>
                <div style="display:flex; flex-direction:column; gap:0.4rem;">
                    ${nextTasks.map((tsk, idx) => `
                        <div onclick="openTaskDetailModal('${tsk.id}', '${team.team_id}', ${idx+1})" style="background:rgba(30,41,59,0.5); border-left:3px solid ${tsk.color}; padding:0.5rem 0.75rem; border-radius:4px; display:flex; justify-content:space-between; align-items:center; cursor:pointer;">
                            <div>
                                <span style="font-weight:800; font-size:0.8rem; color:#f8fafc;">${tsk.day} : ${tsk.task}</span>
                                <div style="font-size:0.7rem; color:#94a3b8;">${tsk.hours} • ${tsk.volume}</div>
                            </div>
                            <span class="badge ${tsk.progress === 100 ? 'badge-success' : 'badge-warning'}" style="font-size:0.65rem;">${tsk.progress}%</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    function openTaskDetailModal(taskId, teamId, dayIdx) {
        let foundTask = null;
        let foundTeam = null;

        for (const tm of agendaTeamsData) {
            const t = (tm.schedule || []).find(s => s.id === taskId);
            if (t) {
                foundTask = t;
                foundTeam = tm;
                break;
            }
        }

        if (!foundTask) return;

        const body = document.getElementById('task-modal-body');
        if (!body) return;

        body.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; border-bottom: 1px solid rgba(51,65,85,0.7); padding-bottom: 0.75rem;">
                <div>
                    <span class="badge badge-info" style="font-family: 'JetBrains Mono'; font-size: 0.75rem;">ID: ${foundTask.id} • ${foundTask.day}</span>
                    <h2 style="font-size: 1.3rem; font-weight: 900; color: #38bdf8; margin-top: 4px;">${foundTask.task}</h2>
                    <div style="font-size: 0.85rem; color: #94a3b8;">📍 Chantier : <strong>${foundTask.project}</strong></div>
                </div>
                <div style="text-align: right;">
                    <span class="badge badge-warning" style="font-size: 0.8rem;">Horaires : ${foundTask.hours}</span>
                    <div style="font-size: 0.8rem; color: var(--emerald); font-weight: 700; margin-top: 4px;">Objectif : ${foundTask.volume}</div>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.25rem;">
                <div style="background: rgba(30,41,59,0.6); padding: 0.75rem; border-radius: 6px; border: 1px solid rgba(51,65,85,0.6);">
                    <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 700;">ÉQUIPE AFFECTÉE</div>
                    <div style="font-size: 0.95rem; font-weight: 800; color: #f8fafc; margin-top: 2px;">${foundTeam ? foundTeam.team_name : 'Équipe VRD'}</div>
                    <div style="font-size: 0.8rem; color: #cbd5e1; margin-top: 4px;">Personnel : ${foundTask.team}</div>
                </div>

                <div style="background: rgba(30,41,59,0.6); padding: 0.75rem; border-radius: 6px; border: 1px solid rgba(51,65,85,0.6);">
                    <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 700;">ENGINS & OUTILLAGE DÉPLOYÉS</div>
                    <div style="font-size: 0.85rem; font-weight: 800; color: var(--amber); margin-top: 2px;">🚜 ${foundTask.gear}</div>
                    <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px;">Vérification VGP & calage laser OK</div>
                </div>
            </div>

            <!-- SAFETY & OPBTP INSTRUCTIONS -->
            <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.4); padding: 0.85rem; border-radius: 6px; margin-bottom: 1.25rem;">
                <div style="font-size: 0.8rem; font-weight: 800; color: #ef4444; margin-bottom: 4px;">🦺 Consignes Sécurité & AIPR Spécifiques à la Tâche :</div>
                <div style="font-size: 0.85rem; color: #f8fafc;">${foundTask.safety}</div>
            </div>

            <!-- INTERACTIVE PROGRESS SLIDER -->
            <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.7); padding: 1rem; border-radius: 6px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.85rem; font-weight: 800; color: #f8fafc;">Ajustement de l'Avancement Réel :</span>
                    <span style="font-size: 1rem; font-weight: 900; color: var(--emerald); font-family: 'JetBrains Mono';" id="task-modal-progress-val">${foundTask.progress}%</span>
                </div>
                <input type="range" min="0" max="100" value="${foundTask.progress}" class="input-field" style="width: 100%; cursor: pointer;" oninput="document.getElementById('task-modal-progress-val').textContent = this.value + '%'; foundTask.progress = parseInt(this.value); if (currentNav === 'compagnon_mobile') renderCompagnonPlanning(); else renderPlanningAgenda();">
            </div>
        `;

        openModal('task-details-modal');
    }

    function renderPlanningGantt() {
        const container = document.getElementById('planning-gantt-view');
        if (!container) return;

        const projects = companyData.projects || [];
        const weeks = Array.from({ length: 12 }, (_, i) => `S${i + 20}`);

        container.innerHTML = `
            <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(51,65,85,0.7); border-radius: 8px; padding: 1rem; overflow-x: auto;">
                <div style="font-size: 0.85rem; font-weight: 800; color: #38bdf8; margin-bottom: 1rem; text-transform: uppercase;">
                    📊 Chronogramme Gantt Consolidé (Mai - Octobre 2026)
                </div>

                <div style="min-width: 800px;">
                    <div style="display: grid; grid-template-columns: 240px repeat(12, 1fr); gap: 4px; margin-bottom: 8px; font-size: 0.75rem; font-weight: 800; color: #94a3b8; text-align: center;">
                        <div style="text-align: left;">CHANTIER & LOTS</div>
                        ${weeks.map(w => `<div style="background: rgba(30,41,59,0.8); padding: 4px 0; border-radius: 4px;">${w}</div>`).join('')}
                    </div>

                    ${projects.map((p, idx) => {
                        const startCol = (idx * 2) + 1;
                        const spanCols = Math.min(12 - startCol, 6);
                        return `
                            <div style="display: grid; grid-template-columns: 240px repeat(12, 1fr); gap: 4px; margin-bottom: 8px; align-items: center; font-size: 0.75rem;">
                                <div style="font-weight: 700; color: #f8fafc; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                                    ${p.name}
                                </div>
                                <div style="grid-column: ${startCol + 1} / span ${spanCols}; background: linear-gradient(90deg, #0284c7, #10b981); height: 26px; border-radius: 4px; display: flex; align-items: center; justify-content: space-between; padding: 0 8px; color: #fff; font-weight: 800; font-size: 0.7rem; box-shadow: 0 2px 6px rgba(0,0,0,0.3);">
                                    <span>${p.progress}%</span>
                                    <span>${p.end}</span>
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `;
    }
"""
