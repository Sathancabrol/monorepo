# -*- coding: utf-8 -*-

def get_js_part1():
    return r"""<script>
    
    // ==========================================
    // 0. GLOBAL REACTIVE ACCOUNT STATE & UI CONTROLLERS
    // ==========================================
    window.userAccountState = {
        userName: 'Romain CARAÏ',
        userRole: 'direction',
        companyKey: 'colas_sete',
        companyName: 'Colas Agence Sète & Bassin de Thau',
        treasury: 1450000,
        headcount: 68,
        projectsCount: 4,
        fleetCount: 14,
        qseScore: 98.5
    };

    window.updateAllHudAndTickerMetrics = function() {
        var s = window.userAccountState;
        
        // 1. Top HUD Metrics
        var caisseTop = document.getElementById('caisse-balance-top');
        if (caisseTop) caisseTop.textContent = new Intl.NumberFormat('fr-FR').format(s.treasury) + ' €';

        var hudChantiers = document.getElementById('hud-chantiers-val');
        if (hudChantiers) hudChantiers.textContent = s.projectsCount + ' / ' + s.projectsCount + ' Actifs';

        var hudFlotte = document.getElementById('hud-flotte-val');
        if (hudFlotte) hudFlotte.textContent = s.fleetCount + ' / ' + s.fleetCount + ' Dispo';

        var hudEffectif = document.getElementById('hud-effectif-val');
        if (hudEffectif) hudEffectif.textContent = s.headcount + ' Salarié' + (s.headcount > 1 ? 's' : '');

        var hudQse = document.getElementById('hud-qse-val');
        if (hudQse) hudQse.textContent = s.qseScore + '% Conforme';

        var roleBadges = {
            'direction': '👑',
            'conduite': '👷',
            'chef_chantier': '🦺',
            'compagnon': '🛠️'
        };
        var roleLabels = {
            'direction': 'Direction',
            'conduite': 'Conduite',
            'chef_chantier': 'Chef Chantier',
            'compagnon': 'Compagnon'
        };
        var hudUser = document.getElementById('hud-user-identity');
        if (hudUser) hudUser.textContent = (roleBadges[s.userRole] || '👤') + ' ' + s.userName + ' (' + (roleLabels[s.userRole] || 'Direction') + ')';

        var hudComp = document.getElementById('hud-company-name-display');
        if (hudComp) hudComp.textContent = s.companyName + ' ▾';

        // 2. News Ticker
        var ticker = document.getElementById('live-ticker-text');
        if (ticker) {
            ticker.textContent = '📢 ' + s.companyName + ' • Direction : ' + s.userName + ' • Caisse Active : ' + new Intl.NumberFormat('fr-FR').format(s.treasury) + ' € • Effectif : ' + s.headcount + ' salariés • Chantiers : ' + s.projectsCount + ' actifs (Quai Richelieu, Voie Verte Thau, Caraussane, RD600).';
        }
    };

    window.toggleSidebarDrawer = function(forceState) {
        var drawer = document.getElementById('sidebar-drawer');
        var backdrop = document.getElementById('sidebar-backdrop');
        if (!drawer) return;
        var isOpen = drawer.classList.contains('active') || drawer.classList.contains('open');
        var target = (typeof forceState === 'boolean') ? forceState : !isOpen;
        if (target) {
            drawer.classList.add('active', 'open');
            if (backdrop) backdrop.classList.add('active', 'open');
        } else {
            drawer.classList.remove('active', 'open');
            if (backdrop) backdrop.classList.remove('active', 'open');
        }
    };

    window.openAccountModal = function() {
        var modal = document.getElementById('account-modal') || document.getElementById('company-switch-modal');
        if (modal) {
            modal.style.display = 'flex';
            modal.classList.add('active');
            window.setAccountTab('login');
            window.loadAccountFormValues();
        }
    };

    window.closeAccountModal = function() {
        var modal = document.getElementById('account-modal') || document.getElementById('company-switch-modal');
        if (modal) {
            modal.style.display = 'none';
            modal.classList.remove('active');
        }
    };
    window.openCompanySwitchModal = window.openAccountModal;

    window.setAccountTab = function(tabKey) {
        document.querySelectorAll('.account-tab-btn').forEach(function(b) { b.classList.remove('active'); });
        var btn = document.getElementById('btn-acc-' + tabKey);
        if (btn) btn.classList.add('active');

        document.querySelectorAll('.acc-tab-content').forEach(function(c) { c.style.display = 'none'; });
        var tab = document.getElementById('acc-tab-' + tabKey);
        if (tab) tab.style.display = 'block';
    };

    window.loadAccountFormValues = function() {
        var nameInput = document.getElementById('user-fullname');
        var roleSelect = document.getElementById('user-role-select');
        var headSlider = document.getElementById('user-headcount-slider');
        var headDisp = document.getElementById('user-headcount-display');

        if (nameInput) nameInput.value = window.userAccountState.userName;
        if (roleSelect) roleSelect.value = window.userAccountState.userRole;
        if (headSlider) headSlider.value = window.userAccountState.headcount;
        if (headDisp) headDisp.textContent = window.userAccountState.headcount + ' Salariés';
    };

    window.loginCompanyProfile = function(profileKey) {
        var presets = {
            'colas_sete': { name: 'Colas Agence Sète & Bassin de Thau', treasury: 1450000, headcount: 68, projects: 3, fleet: 14, role: 'direction', desc: 'Simulation Réelle Major TP / Rétro-Ingénierie Territoriale' },
            'occitanie_tp': {
            id: 'colas_sete',
            name: 'Colas Agence Sète & Bassin de Thau',
            type: 'Établissement Secondaire Major TP (Colas France)',
            siret: '329 338 883 01359',
            capital: '1 500 000 € (Colas Midi Méditerranée SA)',
            siege: 'Zone Industrielle des Eaux Blanches, CS 10098, 34200 Sète',
            caisse: 1450000,
            bfr: 420000,
            ca_annuel: 18500000,
            ca_prev: 22400000,
            margin: 14.8,
            effectif_count: 68,
            fleet_count: 14,
            projects_count: 4,
            safety_status: '98.5% Conforme',
            safety_sub: '0 Incident • CSPS & DICT Validés',
            treasury_sub: 'BFR Couvert : 42 jours d'exploitation',
            projects_sub: 'Quai Richelieu, Voie Verte Thau, Caraussane, RD600',
            effectif_sub: '68 Salariés • AIPR & CACES à jour • Colas Sète',
            desc: 'Établissement Colas Agence de Sète (1052 Av. des Eaux Blanches). Travaux maritimes et portuaires, voiries urbaines, pistes cyclables éco-innovantes Colstab Ostrea® et enrobés spéciaux Colstrong®.',
            
            projects: [
                {
                    id: "p-01",
                    code: "COLAS-SET-2026-01",
                    name: "Port de Sète - Quai Richelieu (Amarrage Drague Hydromer & Colstrong)",
                    type: "internal",
                    ownership: "🏢 Colas Agence Sète (En cours)",
                    badge_type: "Marché Public Actif",
                    loc: "Port de Sète - Quai Richelieu (34200)",
                    location: "Port de Sète - Quai Richelieu (34200)",
                    client: "Région Occitanie / Port Sud de France (Groupement Buesa-Soletanche / Colas)",
                    moe: "BRL Ingénierie / Direction Portuaire",
                    budget: 1850000,
                    spent: 1258000,
                    budget_used: 1258000,
                    progress: 68,
                    status: "En cours",
                    manager: "Romain Caraï",
                    site_chief: "Rémi Bonnefoi",
                    chef: "Rémi Bonnefoi (Chef Établissement: R. Caraï)",
                    workers_count: 12,
                    delai_consomme_pct: 70,
                    start_date: "16/09/2025",
                    end_date: "15/06/2026",
                    end: "15/06/2026",
                    desc: "Aménagement des voiries lourdes de bord à quai pour l'amarrage de la nouvelle drague électrique Hydromer de la Région Occitanie. Application d'enrobés percolés à très haute résistance Colstrong® (procédé breveté Colas avec 1/3 de coquilles d'huîtres recyclées de Thau), bordures T3 d'accostage, raccordement réseaux maritimes et séparateur hydrocarbures.",
                    assigned_machinery: [{ name: "Finisseur Vögele Super 1800-3i" }, { name: "Compacteur Tandem Bomag BW151" }, { name: "Pelle Chenilles 24t Liebherr R924" }],
                    assigned_tools: [{ name: "Centrale mobile percolation Colstrong" }, { name: "Laser de nivellement Piper" }],
                    docs: [{ name: "CCTP_Port_Sete_Richelieu", type: "pdf" }, { name: "Fiche_Technique_Colstrong", type: "pdf" }],
                    lots_breakdown: [
                        { name: "Lot 1 : Terrassement & Purges Quai (3 800 m³)", budget: 380000, progress: 100, ds: 283500, pv: 380000 },
                        { name: "Lot 2 : Assainissement & Séparateur Hydrocarbures", budget: 420000, progress: 85, ds: 313400, pv: 420000 },
                        { name: "Lot 3 : Sous-couche GNT 0/31.5 & Bordures T3", budget: 250000, progress: 75, ds: 186500, pv: 250000 },
                        { name: "Lot 4 : Enrobés Percolés Colstrong aux Coquilles de Thau", budget: 800000, progress: 40, ds: 597000, pv: 800000 }
                    ],
                    steps: [
                        { name: "Piquetage & DICT Maritime validée", progress: 100 },
                        { name: "Terrassement et purge sous nappe", progress: 100 },
                        { name: "Pose collecteur fonte DN300 & séparateur", progress: 85 },
                        { name: "Sous-couche GNT et bordures d'accostage T3", progress: 75 },
                        { name: "Coulage matrice ciment & enrobé percolé Colstrong", progress: 40 }
                    ]
                },
                {
                    id: "p-02",
                    code: "COLAS-SET-2026-02",
                    name: "Voie Verte Bassin de Thau - Piste Cyclable Bouzigues-Sète (Colstab Ostrea)",
                    type: "internal",
                    ownership: "🏢 Colas Agence Sète (En cours)",
                    badge_type: "Marché Public Actif",
                    loc: "Rive Nord Bassin de Thau / Sète - Bouzigues (34)",
                    location: "Rive Nord Bassin de Thau / Sète - Bouzigues (34)",
                    client: "Sète Agglopôle Méditerranée / Ville de Sète",
                    moe: "Direction Aménagement Durable du Territoire Thau",
                    budget: 920000,
                    spent: 772800,
                    budget_used: 772800,
                    progress: 84,
                    status: "Finition",
                    manager: "Sophie Martinez",
                    site_chief: "Jérôme Vidal",
                    chef: "Jérôme Vidal (Conductrice: S. Martinez)",
                    workers_count: 8,
                    delai_consomme_pct: 85,
                    start_date: "03/11/2025",
                    end_date: "30/04/2026",
                    end: "30/04/2026",
                    desc: "Création de 4.2 km de piste cyclable littorale éco-responsable. Mise en œuvre du revêtement innovant Colstab Ostrea® (technologie Colas à base de liant organo-minéral et valorisation conchylicole des coquilles d'huîtres de Thau), stabilisation des berges, passages faune et signalisation touristique.",
                    assigned_machinery: [{ name: "Niveleuse Cat 120M" }, { name: "Compacteur Mixte Bomag BW138" }],
                    assigned_tools: [{ name: "Répandeuse émulsion Colas" }, { name: "Laser rotatif Leica" }],
                    docs: [{ name: "CCTP_VoieVerte_Thau", type: "pdf" }, { name: "Agrément_Colstab_Ostrea", type: "pdf" }],
                    lots_breakdown: [
                        { name: "Lot 1 : Décapage, terrassement & stabilisation talus", budget: 280000, progress: 100, ds: 208000, pv: 280000 },
                        { name: "Lot 2 : Drainage transversal & buses PEHD", budget: 140000, progress: 100, ds: 104000, pv: 140000 },
                        { name: "Lot 3 : Revêtement drainant Colstab Ostrea (14 500 m²)", budget: 420000, progress: 75, ds: 313000, pv: 420000 },
                        { name: "Lot 4 : Signalétique & glissières bois-métal", budget: 80000, progress: 50, ds: 59000, pv: 80000 }
                    ],
                    steps: [
                        { name: "Piquetage environnemental & balisage", progress: 100 },
                        { name: "Terrassement fond de forme & reprofilage talus", progress: 100 },
                        { name: "Couche de forme GNT 0/20 non traitée", progress: 100 },
                        { name: "Application revêtement Colstab Ostrea", progress: 75 },
                        { name: "Pose glissières bois-métal et signalisation", progress: 50 }
                    ]
                },
                {
                    id: "p-03",
                    code: "COLAS-SET-2026-03",
                    name: "Sète Centre - Réseaux & Voiries Rues Caraussane & de Gaulle",
                    type: "internal",
                    ownership: "🏢 Colas Agence Sète (En cours)",
                    badge_type: "Marché Public Actif",
                    loc: "Centre-Ville / Mont Saint-Clair, Sète (34200)",
                    location: "Centre-Ville / Mont Saint-Clair, Sète (34200)",
                    client: "Sète Agglopôle Méditerranée (Cycle de l'Eau) & Ville de Sète",
                    moe: "Bureau d'Études SEIRI / Direction Eau Thau",
                    budget: 1420000,
                    spent: 596400,
                    budget_used: 596400,
                    progress: 42,
                    status: "En cours",
                    manager: "Rémi Bonnefoi",
                    site_chief: "Bruno Dupuis",
                    chef: "Bruno Dupuis (Conducteur: R. Bonnefoi)",
                    workers_count: 9,
                    delai_consomme_pct: 45,
                    start_date: "21/09/2025",
                    end_date: "30/05/2027",
                    end: "30/05/2027",
                    desc: "Mise en séparatif des réseaux pluviaux et eaux usées du bassin versant Mont Saint-Clair (13 ha), raccordement au réservoir Simone Veil réhabilité (1 500 m³), renouvellement conduites fonte DN300/DN600, tranchées blindées urbaines, puis réfection totale voirie en BBSG 0/10 et trottoirs en béton désactivé.",
                    assigned_machinery: [{ name: "Pelle Urbaine Mecalac 12MTX" }, { name: "Minipelle Yanmar SV26" }, { name: "Camion 6x4 bi-benne MAN" }],
                    assigned_tools: [{ name: "Caissons de blindage SBH" }, { name: "Laser Piper 200" }],
                    docs: [{ name: "DICT_Enedis_Sète_Centre", type: "pdf" }, { name: "Plan_Deviation_Circulation", type: "pdf" }],
                    lots_breakdown: [
                        { name: "Lot 1 : Tranchées blindées & Conduite Pluviale DN600", budget: 520000, progress: 60, ds: 388000, pv: 520000 },
                        { name: "Lot 2 : Renouvellement Réseau EU & Branchements AEP", budget: 380000, progress: 45, ds: 283500, pv: 380000 },
                        { name: "Lot 3 : Raccordement Bassin Tampon Simone Veil", budget: 220000, progress: 30, ds: 164000, pv: 220000 },
                        { name: "Lot 4 : Réfection Chaussée BBSG 0/10 & Trottoirs", budget: 300000, progress: 10, ds: 223800, pv: 300000 }
                    ],
                    steps: [
                        { name: "Mise en place déviations & DICT", progress: 100 },
                        { name: "Fouilles blindées Rue de la Caraussane", progress: 60 },
                        { name: "Pose fonte DN600 vers réservoir Simone Veil", progress: 50 },
                        { name: "Branchements particuliers & déconnexion toitures", progress: 40 },
                        { name: "Rabotage et réfection chaussée BBSG 0/10", progress: 10 }
                    ]
                },
                {
                    id: "p-04",
                    code: "COLAS-SET-2026-04",
                    name: "Marché d'Entretien Routier RD600 / RD612 & Liaisons Bassin de Thau",
                    type: "internal",
                    ownership: "🏢 Colas Agence Sète (Accord-cadre)",
                    badge_type: "Marché Public Actif",
                    loc: "Axe Sète - Frontignan - Balaruc - Saint-Thibéry (34)",
                    location: "Axe Sète - Frontignan - Balaruc - Saint-Thibéry (34)",
                    client: "Conseil Départemental de l'Hérault (CD34)",
                    moe: "Direction des Routes et Mobilités 34",
                    budget: 3200000,
                    spent: 960000,
                    budget_used: 960000,
                    progress: 30,
                    status: "En cours",
                    manager: "Romain Caraï",
                    site_chief: "Marc Bellegarde",
                    chef: "Marc Bellegarde (Conducteur: R. Caraï)",
                    workers_count: 14,
                    delai_consomme_pct: 32,
                    start_date: "01/01/2026",
                    end_date: "31/12/2028",
                    end: "31/12/2028",
                    desc: "Accord-cadre triennal à bons de commande pour le rabotage fin 5cm sous circulation de nuit, purges locales, et application d'enrobés très minces BBTM 0/10 et BBSG 0/10 formulés à la centrale Colas Sète - ZI Eaux Blanches avec 30% d'agrégats recyclés.",
                    assigned_machinery: [{ name: "Raboteuse Wirtgen W210i" }, { name: "Finisseur Vögele Super 1800-3i" }, { name: "Compacteur Hamm HD+ 90i" }],
                    assigned_tools: [{ name: "Balisage temporaire autoroutier" }, { name: "Thermomètre infrarouge thermique" }],
                    docs: [{ name: "BPU_Departement_34_Colas", type: "pdf" }, { name: "Formulation_Enrobes_Centrale", type: "pdf" }],
                    lots_breakdown: [
                        { name: "Bon de Commande 1 : Rabotage & BBTM RD600", budget: 950000, progress: 100, ds: 708000, pv: 950000 },
                        { name: "Bon de Commande 2 : Section RD612 Frontignan Plage", budget: 720000, progress: 25, ds: 537000, pv: 720000 },
                        { name: "Bon de Commande 3 : Giratoire ZI Eaux Blanches / Desserte Port", budget: 530000, progress: 0, ds: 395000, pv: 530000 },
                        { name: "Bon de Commande 4 : Purges & Réfection A9 / Bretelle Saint-Thibéry", budget: 1000000, progress: 0, ds: 746000, pv: 1000000 }
                    ],
                    steps: [
                        { name: "Plan de signalisation de nuit validé", progress: 100 },
                        { name: "Rabotage de nuit RD600 22 000 m²", progress: 100 },
                        { name: "Application BBTM 0/10 sous circulation", progress: 65 },
                        { name: "Purges ponctuelles et reconstitution GB4", progress: 25 },
                        { name: "Marquage thermoplastique rétro-réfléchissant", progress: 20 }
                    ]
                }
            ],

            fleet: [
                { id: "ENG-01", name: "Finisseur sur chenilles Vögele Super 1800-3i", cat: "Application Enrobés", type: "Finisseur lourd", brand: "Vögele", loc: "Port de Sète Quai Richelieu", status: "Sur Chantier", val: 320000, price: 320000, hourly_cost: 165, vgp: "01/10/2026", immat: "VOG-1800-3I", fuel: 85, hours: 1420, weight: "19.5t", power: "129 kW", capacity: "Table AB 500 TV (2.55m - 5.00m)", project: "Port de Sète - Quai Richelieu", icon: "🚜" },
                { id: "ENG-02", name: "Raboteuse à froid Wirtgen W210i", cat: "Rabotage Routier", type: "Fraiseuse 2m", brand: "Wirtgen", loc: "Axe RD600 / Frontignan", status: "Sur Chantier", val: 450000, price: 450000, hourly_cost: 210, vgp: "15/11/2026", immat: "WIR-210-I", fuel: 75, hours: 2180, weight: "28.5t", power: "537 kW", capacity: "Tambour 2.00m • Prof. 0-330mm", project: "Marché Entretien RD600", icon: "🚜" },
                { id: "ENG-03", name: "Compacteur Tandem Bomag BW151 AD-5", cat: "Compactage", type: "Cylindre vibrant", brand: "Bomag", loc: "Port de Sète Quai Richelieu", status: "Sur Chantier", val: 85000, price: 85000, hourly_cost: 65, vgp: "05/12/2026", immat: "BOM-151-AD", fuel: 90, hours: 1850, weight: "8.2t", power: "55 kW", capacity: "Largeur billes 1.50m (Asphalt Manager)", project: "Port de Sète - Quai Richelieu", icon: "🚜" },
                { id: "ENG-04", name: "Pelle Chenilles 24t Liebherr R924 G8", cat: "Terrassement Lourd", type: "Pelle Hydraulique", brand: "Liebherr", loc: "Port de Sète Quai Richelieu", status: "Sur Chantier", val: 240000, price: 240000, hourly_cost: 110, vgp: "20/09/2026", immat: "LIE-924-G8", fuel: 80, hours: 2650, weight: "24.5t", power: "129 kW", capacity: "Godet terrassement 1.45 m³ + Ligne BRH", project: "Port de Sète - Quai Richelieu", icon: "🚜" },
                { id: "ENG-05", name: "Pelle Urbaine Mecalac 12MTX", cat: "VRD & Réseaux", type: "Pelle sur pneus polyvalente", brand: "Mecalac", loc: "Sète Centre - Rue Caraussane", status: "Sur Chantier", val: 145000, price: 145000, hourly_cost: 85, vgp: "10/10/2026", immat: "MEC-12-MTX", fuel: 88, hours: 1920, weight: "9.7t", power: "85 kW", capacity: "Bras 3 pièces articulé + Attache rapide", project: "Sète Centre - Caraussane", icon: "🚜" },
                { id: "ENG-06", name: "Niveleuse compacte Caterpillar 120M", cat: "Nivellement", type: "Niveleuse 6x6", brand: "Caterpillar", loc: "Voie Verte Bouzigues-Sète", status: "Sur Chantier", val: 195000, price: 195000, hourly_cost: 95, vgp: "18/11/2026", immat: "CAT-120-M", fuel: 70, hours: 3100, weight: "14.2t", power: "103 kW", capacity: "Lame 3.65m guidée laser 3D", project: "Voie Verte Bassin de Thau", icon: "🚜" },
                { id: "ENG-07", name: "Minipelle Yanmar SV26-1", cat: "Petits Travaux", type: "Minipelle compacte", brand: "Yanmar", loc: "Sète Centre - Simone Veil", status: "Sur Chantier", val: 42000, price: 42000, hourly_cost: 45, vgp: "01/01/2027", immat: "YAN-SV26", fuel: 92, hours: 850, weight: "2.7t", power: "17.6 kW", capacity: "Godets 300, 600 et curage orientable", project: "Sète Centre - Caraussane", icon: "🚜" },
                { id: "ENG-08", name: "Chargeuse sur pneus Volvo L120H", cat: "Manutention Dépôt", type: "Chargeuse", brand: "Volvo", loc: "Centrale Colas Eaux Blanches", status: "Au Dépôt", val: 210000, price: 210000, hourly_cost: 98, vgp: "12/10/2026", immat: "VOL-L120H", fuel: 95, hours: 3400, weight: "20.7t", power: "203 kW", capacity: "Godet grand volume 3.5 m³", project: "Colas Établissement Sète", icon: "🚜" },
                { id: "ENG-09", name: "Camion Bi-Benne 8x4 Scania G450", cat: "Transport", type: "Poids Lourd 32t", brand: "Scania", loc: "Axe Sète - Frontignan", status: "En Rotation", val: 160000, price: 160000, hourly_cost: 75, vgp: "05/11/2026", immat: "SCA-8X4-G450", fuel: 82, hours: 4200, weight: "32t PTAC", power: "331 kW", capacity: "Benne calorifugée 18 m³ (Enrobés & GNT)", project: "Port de Sète - Quai Richelieu", icon: "🚛" },
                { id: "ENG-10", name: "Semi-remorque enrobés calorifugée MAN TGX", cat: "Transport", type: "Tracteur + Semi Benne", brand: "MAN", loc: "Centrale Maguelone - Sète", status: "En Rotation", val: 185000, price: 185000, hourly_cost: 88, vgp: "18/12/2026", immat: "MAN-TGX-SEMI", fuel: 78, hours: 2900, weight: "44t PTRA", power: "368 kW", capacity: "Benne ronde calorifugée 26 tonnes", project: "Marché Entretien RD600", icon: "🚛" }
            ],

            depot_inventory: [
                { id: "DEP-01", name: "Centrale d'enrobage Languedoc Enrobés / Colas (240 t/h)", cat: "Industriel", zone: "centrale", loc: "Site Maguelone / Sète", status: "Opérationnel", val: 2400000, vgp: "Contrôle DREAL OK", icon: "🏭" },
                { id: "DEP-02", name: "Stock GNT 0/31.5 calcaire concassé classe A (1 850 t)", cat: "Granulats", zone: "parc", loc: "Dépôt ZI Eaux Blanches", status: "Disponible", val: 33300, vgp: "NF Granulats", icon: "🧱" },
                { id: "DEP-03", name: "Stock liant spécial bitume modifié polymères Colstrong® (45 t)", cat: "Liants & Bitume", zone: "cuves", loc: "Cuve n°2 Centrale", status: "Disponible", val: 42750, vgp: "NF P 98-150", icon: "🛢️" },
                { id: "DEP-04", name: "Stock coquilles d'huîtres de Thau calibrées et lavées (120 t)", cat: "Éco-Matériaux", zone: "parc", loc: "Alvéole bio-recyclage", status: "Disponible", val: 14400, vgp: "Agrément Thau Agglo", icon: "🦪" },
                { id: "DEP-05", name: "Lot de 8 Caissons de blindage caisson léger SBH", cat: "Sécurité Tranchée", zone: "atelier", loc: "Magasin Sécurité", status: "Disponible", val: 38000, vgp: "VGP R.4534", icon: "🛡️" },
                { id: "DEP-06", name: "Tuyaux Fonte Ductile DN300 & DN600 avec joints express (280 ml)", cat: "Canalisations", zone: "rack", loc: "Zone Réseaux Humides", status: "Disponible", val: 48500, vgp: "NF EN 545", icon: "🚰" }
            ],

            cashflow_transactions: [
                { date: "02/04/2026", type: "Situation Marché", label: "Acompte n°2 - Port de Sète Quai Richelieu (Hydromer)", amount: 340000, status: "Encaissé (Chorus Pro)" },
                { date: "28/03/2026", type: "Situation Marché", label: "Situation n°5 - Voie Verte Bassin de Thau (Colstab)", amount: 165000, status: "Encaissé (Chorus Pro)" },
                { date: "20/03/2026", type: "Paiement Fournisseur", label: "Approvisionnement Bitumes & Liants Spéciaux Colas", amount: -85400, status: "Réglé" },
                { date: "15/03/2026", type: "Salaires", label: "Paie du personnel et charges sociales (68 salariés)", amount: -215000, status: "Débité" }
            ],

            documents: [
                { id: "DOC-COLAS-01", title: "CCTP Quai Richelieu - Aménagement Amarrage Drague Hydromer", cat: "DCE Actif", chantier: "Port de Sète - Quai Richelieu", date: "15/01/2026", format: "PDF", size: "8.4 Mo" },
                { id: "DOC-COLAS-02", title: "Fiche Technique & Avis Technique Procédé Colstrong® Percolé", cat: "Procédés Brevetés", chantier: "Port de Sète - Quai Richelieu", date: "10/02/2026", format: "PDF", size: "3.2 Mo" },
                { id: "DOC-COLAS-03", title: "CCTP Voie Verte Bassin de Thau - Revêtement Colstab Ostrea®", cat: "DCE Actif", chantier: "Voie Verte Bassin de Thau", date: "22/10/2025", format: "PDF", size: "5.7 Mo" },
                { id: "DOC-COLAS-04", title: "DICT Validée & Plan Réseaux Enedis / GRDF Sète Centre", cat: "DICT & Sécurité", chantier: "Sète Centre - Caraussane", date: "18/09/2025", format: "PDF", size: "4.1 Mo" }
            ],

            map_locations: [
                { id: "ch_01", name: "Port de Sète - Quai Richelieu (Hydromer & Colstrong)", category: "chantier", lat: 43.3980, lng: 3.7020, color: "#38bdf8", icon: "🏗️", ownership: "Colas Agence Sète (En cours)", budget_ini: 1850000, budget_used: 1258000, progress: 68, chef: "Rémi Bonnefoi", desc: "Aménagement voiries quai drague Hydromer, enrobés percolés Colstrong aux coquilles d'huîtres de Thau." },
                { id: "ch_02", name: "Voie Verte Bassin de Thau (Bouzigues-Sète Colstab)", category: "chantier", lat: 43.4350, lng: 3.6550, color: "#38bdf8", icon: "🏗️", ownership: "Colas Agence Sète (En cours)", budget_ini: 920000, budget_used: 772800, progress: 84, chef: "Jérôme Vidal", desc: "Création piste cyclable 4.2 km, revêtement drainant Colstab Ostrea® à valorisation conchylicole." },
                { id: "ch_03", name: "Sète Centre - Rues Caraussane & de Gaulle", category: "chantier", lat: 43.4080, lng: 3.6930, color: "#38bdf8", icon: "🏗️", ownership: "Colas Agence Sète (En cours)", budget_ini: 1420000, budget_used: 596400, progress: 42, chef: "Bruno Dupuis", desc: "Séparation pluviale vers réservoir Simone Veil 1 500 m³, fonte DN600, BBSG 0/10 et béton désactivé." },
                { id: "ch_04", name: "Marché Entretien Routier RD600 / RD612", category: "chantier", lat: 43.4380, lng: 3.7250, color: "#38bdf8", icon: "🏗️", ownership: "Colas Agence Sète (Accord-cadre)", budget_ini: 3200000, budget_used: 960000, progress: 30, chef: "Marc Bellegarde", desc: "Rabotage fin 5cm sous circulation de nuit, BBTM 0/10 haute performance centrale Eaux Blanches." },
                { id: "dep_01", name: "Colas Établissement Sète (ZI Eaux Blanches)", category: "depot", lat: 43.4240, lng: 3.7080, color: "#f59e0b", icon: "🏢", stock_val: "1 450 000 €", desc: "Siège agence Colas Sète, parc engins lourds, atelier d'entretien et centrale d'enrobage." },
                { id: "centrale_01", name: "Centrale Languedoc Enrobés / Colas Maguelone", category: "fournisseur", lat: 43.5250, lng: 3.8450, color: "#ec4899", icon: "🏭", product: "BBSG, BBTM, Colstrong & Colstab", desc: "Poste d'enrobage continu 240 t/h alimentant les chantiers de l'Hérault et du littoral." },
                { id: "carriere_01", name: "Carrières GSM Poussan & Villeveyrac", category: "fournisseur", lat: 43.4900, lng: 3.6800, color: "#ec4899", icon: "🏭", product: "GNT 0/31.5 & Enrochements", desc: "Carrière calcaire certifiée NF Granulats pour couches de forme et voiries portuaires." }
            ],

            hr_employees: [
                { id: "EMP-01", name: "Romain CARAÏ", role: "Chef d'Établissement Colas Agence de Sète", cat: "Direction", site: "Siège Agence Sète (Eaux Blanches)", phone: "04 67 46 22 00", email: "romain.carai@colas.com", caces: "AIPR Concepteur • Ingénieur TP", exp: "22 ans", icon: "👑" },
                { id: "EMP-02", name: "Rémi BONNEFOI", role: "Conducteur de Travaux Principal Port & Grands Travaux", cat: "Conduite Travaux", site: "Port de Sète Quai Richelieu", phone: "06 12 34 56 78", email: "remi.bonnefoi@colas.com", caces: "AIPR Encadrant • Spécialité Maritime", exp: "15 ans", icon: "👷‍♂️" },
                { id: "EMP-03", name: "Sophie MARTINEZ", role: "Conductrice de Travaux VRD & Éco-aménagements", cat: "Conduite Travaux", site: "Voie Verte Bassin de Thau", phone: "06 23 45 67 89", email: "sophie.martinez@colas.com", caces: "AIPR Encadrant • Ingénieure Environnement", exp: "11 ans", icon: "👷‍♀️" },
                { id: "EMP-04", name: "Bruno DUPUIS", role: "Chef de Chantier Réseaux Urbains & Séparatif", cat: "Chefs de Chantier", site: "Sète Centre - Caraussane", phone: "06 34 56 78 90", email: "bruno.dupuis@colas.com", caces: "AIPR Encadrant • CATEC Espace Confiné", exp: "18 ans", icon: "🦺" },
                { id: "EMP-05", name: "Jérôme VIDAL", role: "Chef de Chantier Voie Verte & Éco-revêtements", cat: "Chefs de Chantier", site: "Voie Verte Bouzigues-Sète", phone: "06 45 67 89 01", email: "jerome.vidal@colas.com", caces: "CACES R482 Cat B1/C1 • AIPR", exp: "14 ans", icon: "🦺" },
                { id: "EMP-06", name: "Marc BELLEGARDE", role: "Chef de Chantier Application Enrobés & Rabotage", cat: "Chefs de Chantier", site: "Marché Entretien RD600", phone: "06 56 78 90 12", email: "marc.bellegarde@colas.com", caces: "CACES R482 Cat D (Finisseur) & E • AIPR", exp: "19 ans", icon: "🦺" }
            ],

            hr_hierarchy: {
                direction: [{ name: "Romain CARAÏ", role: "Chef d'Établissement Colas Sète", color: "#38bdf8" }],
                conduite: [
                    { name: "Rémi BONNEFOI", role: "Conducteur Principal Port & Caraussane", color: "#0284c7" },
                    { name: "Sophie MARTINEZ", role: "Conductrice VRD Voie Verte & RD600", color: "#0284c7" }
                ],
                chefs: [
                    { name: "Bruno DUPUIS", role: "Chef de Chantier Rues Caraussane & de Gaulle", color: "#10b981" },
                    { name: "Jérôme VIDAL", role: "Chef de Chantier Voie Verte Bouzigues-Sète", color: "#10b981" },
                    { name: "Marc BELLEGARDE", role: "Chef de Chantier Application Enrobés RD600", color: "#10b981" }
                ]
            },

            ai_agents: [
                { id: "agent-port", name: "Agent IA Génie Maritime & Enrobés", avatar: "🚢", role: "Expertise Colstrong", status: "Actif", text: "Port de Sète Quai Richelieu : Formulation du coulis de percolation Colstrong validée avec 33% de coquilles conchylicoles de Thau broyées. Résistance en compression > 85 MPa." },
                { id: "agent-eco", name: "Agent IA Éco-Innovation & Voie Verte", avatar: "🌿", role: "Expertise Colstab Ostrea", status: "Actif", text: "Voie Verte Bouzigues-Sète : Perméabilité mesurée à 4.2x10^-4 m/s. Conforme aux exigences loi sur l'eau et protection de la lagune de Thau." }
            ]
        },
        'compte_neuf': { name: 'Compte Neuf (Mode Initiation Pédagogique)', treasury: 50000, headcount: 2, projects: 0, fleet: 1, role: 'direction', desc: 'Démarrage guidé pas-à-pas' }
        };
        var p = presets[profileKey] || presets['occitanie_tp'];
        window.userAccountState.companyKey = profileKey;
        window.userAccountState.companyName = p.name;
        window.userAccountState.treasury = p.treasury;
        window.userAccountState.headcount = p.headcount;
        window.userAccountState.projectsCount = p.projects;
        window.userAccountState.fleetCount = p.fleet;

        window.updateAllHudAndTickerMetrics();
        window.closeAccountModal();
        if (window.showNotification) window.showNotification('Entreprise connectée : ' + p.name, 'success');
    };

    window.handleCreateCompany = function(e) {
        if (e && e.preventDefault) e.preventDefault();
        var nameInput = document.getElementById('new-comp-name');
        var name = (nameInput && nameInput.value) ? nameInput.value : 'Nouvelle Entreprise TP';
        var treasuryInput = document.getElementById('new-comp-treasury');
        var treasury = (treasuryInput && treasuryInput.value) ? parseFloat(treasuryInput.value) : 120000;
        var headcountInput = document.getElementById('new-comp-headcount-slider');
        var headcount = (headcountInput && headcountInput.value) ? parseInt(headcountInput.value, 10) : 12;

        window.userAccountState.companyName = name;
        window.userAccountState.treasury = treasury;
        window.userAccountState.headcount = headcount;
        window.userAccountState.projectsCount = 1;
        window.userAccountState.fleetCount = Math.max(1, Math.round(headcount / 4));

        window.updateAllHudAndTickerMetrics();
        window.closeAccountModal();
        if (window.showNotification) window.showNotification('Entreprise \"' + name + '\" créée et activée avec succès !', 'success');
        window.switchNav('cockpit');
    };

    window.handleSaveUserIdentity = function(e) {
        if (e && e.preventDefault) e.preventDefault();
        var nameInput = document.getElementById('user-fullname');
        var name = (nameInput && nameInput.value) ? nameInput.value : 'Jean DUPONT';
        var roleSelect = document.getElementById('user-role-select');
        var role = (roleSelect && roleSelect.value) ? roleSelect.value : 'direction';
        var headcountSlider = document.getElementById('user-headcount-slider');
        var headcount = (headcountSlider && headcountSlider.value) ? parseInt(headcountSlider.value, 10) : 24;

        window.userAccountState.userName = name;
        window.userAccountState.userRole = role;
        window.userAccountState.headcount = headcount;

        window.updateAllHudAndTickerMetrics();
        window.closeAccountModal();
        if (window.showNotification) window.showNotification('Identité et rôle enregistrés avec succès !', 'success');
    };

    window.updateHeadcountSlider = function(val) {
        var count = parseInt(val, 10);
        window.userAccountState.headcount = count;
        var disp = document.getElementById('user-headcount-display');
        if (disp) disp.textContent = count + ' Salarié' + (count > 1 ? 's' : '');

        var payroll = document.getElementById('user-payroll-est');
        if (payroll) payroll.textContent = new Intl.NumberFormat('fr-FR').format(count * 3500) + ' € / mois';

        var hudEffectif = document.getElementById('hud-effectif-val');
        if (hudEffectif) hudEffectif.textContent = count + ' Salarié' + (count > 1 ? 's' : '');
    };

    window.deleteActiveCompany = function() {
        if (confirm('Êtes-vous sûr de vouloir supprimer l\'entreprise \"' + window.userAccountState.companyName + '\" ?')) {
            window.loginCompanyProfile('compte_neuf');
            if (window.showNotification) window.showNotification('Entreprise supprimée. Profil réinitialisé.', 'warning');
        }
    };

    window.resetAllDataFactory = function() {
        if (confirm('Réinitialiser l\'intégralité des données et recharger la configuration d\'usine ?')) {
            localStorage.clear();
            location.reload();
        }
    };

    window.setTickerMode = function(mode) {
        document.querySelectorAll('.ticker-mode-btn').forEach(function(b) { b.classList.remove('active'); });
        var btn = document.getElementById('ticker-btn-' + mode);
        if (btn) btn.classList.add('active');

        var track = document.getElementById('live-ticker-text');
        if (!track) return;

        var s = window.userAccountState;
        var formattedCaisse = new Intl.NumberFormat('fr-FR').format(s.treasury);

        if (mode === 'general') {
            track.textContent = '📢 GÉNÉRAL : ' + s.companyName + ' • Chantier Quai Richelieu (Hydromer) : Enrobés percolés Colstrong en cours • Voie Verte Bouzigues-Sète : Revêtement Colstab Ostrea® validé • Séparation Pluvial Caraussane / Simone Veil active • QSE 98.5%.';
        } else if (mode === 'finance') {
            track.textContent = '💰 FINANCE : Caisse active Colas Sète ' + formattedCaisse + ' € • Acompte Port de Sète n°2 encaissé (340 000 € HT) • Facturation Sète Agglopôle Caraussane validée • Dépenses bitume & centrale Eaux Blanches équilibrées.';
        } else if (mode === 'security') {
            track.textContent = '🚨 SÉCURITÉ & QSE : 0 accident en cours (Score 98.5%) • DICT Enedis/GRDF validée Sète Centre • AIPR 100% à jour • Consigne Vent fort / Tramontane appliquée sur le Port de Sète.';
        } else if (mode === 'logistics') {
            track.textContent = '🚛 LOGISTIQUE : ' + s.fleetCount + ' engins opérationnels (VGP 100%) • 18t BBSG 0/10 expédiées depuis la Centrale Languedoc Enrobés • Rotations 8x4 régulées sur RD600.';
        }
    };

    window.filterDrawerItems = function() {
        var input = document.getElementById('drawerSearchInput');
        if (!input) return;
        var filter = input.value.toLowerCase().trim();
        document.querySelectorAll('.drawer-nav-item').forEach(function(item) {
            var text = item.textContent.toLowerCase();
            item.style.display = (filter === '' || text.includes(filter)) ? 'flex' : 'none';
        });
        document.querySelectorAll('.drawer-pillar').forEach(function(pillar) {
            var visibleItems = pillar.querySelectorAll('.drawer-nav-item:not([style*="display: none"])');
            pillar.style.display = visibleItems.length > 0 ? 'block' : 'none';
        });
    };

    
    // ==========================================
    // 4X HEXAGONAL TERRITORY GRID & MARKET EXPLORER
    // ==========================================
    window.toggleCockpitMapView = function(mode) {
        var osmMap = document.getElementById('cockpit-osm-map');
        var hexCont = document.getElementById('cockpit-hex-container');
        var btnSat = document.getElementById('btn-map-satellite');
        var btnHex = document.getElementById('btn-map-hex');
        var title = document.getElementById('cockpit-map-title');

        if (mode === 'hexgrid') {
            if (osmMap) osmMap.style.display = 'none';
            if (hexCont) hexCont.style.display = 'block';
            if (btnSat) btnSat.classList.remove('active');
            if (btnHex) btnHex.classList.add('active');
            if (title) title.innerHTML = '⬡ Vue Stratégique Hexagonale 4X — Contrôle Territoire Thau / Hérault';
            window.renderCockpitHexGrid();
        } else {
            if (osmMap) osmMap.style.display = 'block';
            if (hexCont) hexCont.style.display = 'none';
            if (btnSat) btnSat.classList.add('active');
            if (btnHex) btnHex.classList.remove('active');
            if (title) title.innerHTML = '🗺️ Cartographie SIG des Chantiers & Flotte (Occitanie)';
            if (window.initCockpitOsmMap) window.initCockpitOsmMap();
        }
    };

    window.territoryHexSectors = [
        { id: 'sete_port', name: 'Sète Ville & Port', x: 260, y: 180, control: 'Colas Sète (54%)', activeProjects: 2, dominantActor: 'Colas Agence Sète', infra: 'Dépôt Quai des Moulins • VRD Portuaire', potential: 'Marché Quai Victor Hugo (450k€)' },
        { id: 'frontignan_plant', name: 'Frontignan / La Peyrade', x: 380, y: 120, control: 'Colas Sète (72%)', activeProjects: 1, dominantActor: 'Centrale Enrobés Colas', infra: 'Poste d\'enrobage discontinu 180 t/h • Stock GNT', potential: 'Réseau AEP Plage (620k€)' },
        { id: 'balaruc_nord', name: 'Balaruc / Bassin Nord', x: 240, y: 80, control: 'Eurovia (40%) / Colas (35%)', activeProjects: 1, dominantActor: 'Coactivité Mixte', infra: 'Réseaux thermaux & Piste cyclable', potential: 'Voie Verte Balaruc (280k€)' },
        { id: 'meze_quarry', name: 'Mèze / Carrières GSM', x: 120, y: 140, control: 'Colas Sète (45%) / Eiffage (30%)', activeProjects: 1, dominantActor: 'Carrières GSM Thau', infra: 'Extraction calcaire 0/31.5 • Dépôt granulats', potential: 'Giratoire RD613 (510k€)' },
        { id: 'marseillan_lagune', name: 'Marseillan / Lagune', x: 100, y: 260, control: 'PME Locales (55%)', activeProjects: 0, dominantActor: 'Artisans du Bassin', infra: 'Zone lagunaire protégée • Stations relevage', potential: 'Aménagement Port Tabarka (190k€)' },
        { id: 'agde_littoral', name: 'Agde / Cap d\'Agde', x: 140, y: 360, control: 'Eurovia Méditerranée (50%)', activeProjects: 2, dominantActor: 'Eurovia Agde', infra: 'Centrale Béton CEMEX • Digues Maritimes', potential: 'Réfection Voirie Littorale (340k€)' },
        { id: 'montpellier_ouest', name: 'Montpellier Ouest / A9', x: 420, y: 40, control: 'Eiffage Route (48%)', activeProjects: 3, dominantActor: 'Eiffage Occitanie', infra: 'Échangeur A9/A750 • Carrière GSM Pignan', potential: 'Élargissement Giratoire RD613 (780k€)' }
    ];

    window.renderCockpitHexGrid = function() {
        var viewport = document.getElementById('hex-grid-viewport');
        if (!viewport) return;

        var sectors = window.territoryHexSectors;
        var svgHtml = '<svg viewBox="0 0 540 420" width="100%" height="100%" style="background:#020617;">' +
            '<defs>' +
            '<linearGradient id="hexGradColas" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#d97706" stop-opacity="0.6"/><stop offset="100%" stop-color="#b45309" stop-opacity="0.9"/></linearGradient>' +
            '<linearGradient id="hexGradEurovia" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0284c7" stop-opacity="0.6"/><stop offset="100%" stop-color="#0369a1" stop-opacity="0.9"/></linearGradient>' +
            '<linearGradient id="hexGradPME" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#10b981" stop-opacity="0.6"/><stop offset="100%" stop-color="#047857" stop-opacity="0.9"/></linearGradient>' +
            '<filter id="hexGlow"><feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#38bdf8" flood-opacity="0.5"/></filter>' +
            '</defs>' +
            '<!-- LOGISTIC FLOW LINES -->' +
            '<line x1="380" y1="120" x2="260" y2="180" stroke="#f59e0b" stroke-width="2.5" stroke-dasharray="4,4" opacity="0.8"/>' +
            '<line x1="120" y1="140" x2="260" y2="180" stroke="#10b981" stroke-width="2" stroke-dasharray="3,3" opacity="0.7"/>' +
            '<line x1="380" y1="120" x2="240" y2="80" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4,4" opacity="0.8"/>';

        function getHexPath(cx, cy, r) {
            var pts = [];
            for (var a = 0; a < 6; a++) {
                var rad = (Math.PI / 180) * (60 * a - 30);
                pts.push((cx + r * Math.cos(rad)).toFixed(1) + ',' + (cy + r * Math.sin(rad)).toFixed(1));
            }
            return 'M ' + pts.join(' L ') + ' Z';
        }

        sectors.forEach(function(s) {
            var fill = (s.control.includes('Colas')) ? 'url(#hexGradColas)' : (s.control.includes('Eurovia') ? 'url(#hexGradEurovia)' : 'url(#hexGradPME)');
            svgHtml += '<g style="cursor:pointer;" onclick="window.selectTerritorySector(\'' + s.id + '\')">' +
                '<path d="' + getHexPath(s.x, s.y, 48) + '" fill="' + fill + '" stroke="#38bdf8" stroke-width="1.5" filter="url(#hexGlow)"/>' +
                '<circle cx="' + s.x + '" cy="' + (s.y - 14) + '" r="10" fill="#020617" stroke="#38bdf8" stroke-width="1"/>' +
                '<text x="' + s.x + '" y="' + (s.y - 10) + '" text-anchor="middle" fill="#fef08a" font-size="10" font-weight="900">⬡</text>' +
                '<text x="' + s.x + '" y="' + (s.y + 4) + '" text-anchor="middle" fill="#ffffff" font-size="10" font-weight="800">' + s.name + '</text>' +
                '<text x="' + s.x + '" y="' + (s.y + 18) + '" text-anchor="middle" fill="#cbd5e1" font-size="8" font-weight="700">' + s.control.split(' ')[0] + ' ' + (s.control.split(' ')[1]||'') + '</text>' +
                '</g>';
        });

        svgHtml += '</svg>';
        viewport.innerHTML = svgHtml;
    };

    window.selectTerritorySector = function(sectorId) {
        var s = window.territoryHexSectors.find(function(x) { return x.id === sectorId; });
        if (!s) return;
        var intel = document.getElementById('hex-sector-intel');
        if (!intel) return;

        intel.style.display = 'block';
        intel.innerHTML = '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem; border-bottom:1px solid rgba(56,189,248,0.3); padding-bottom:0.4rem;">' +
            '<strong style="color:#38bdf8; font-size:1rem;">⬡ Intelligence Territoriale : ' + s.name + '</strong>' +
            '<span class="badge-warning" style="padding:2px 6px; border-radius:4px; font-size:0.75rem;">' + s.control + '</span>' +
            '</div>' +
            '<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:0.6rem; font-size:0.82rem; color:#f1f5f9;">' +
            '<div><strong>🏭 Infrastructures :</strong><div style="color:#cbd5e1;">' + s.infra + '</div></div>' +
            '<div><strong>🏗️ Chantiers en cours :</strong><div style="color:#4ade80;">' + s.activeProjects + ' Actifs (' + s.dominantActor + ')</div></div>' +
            '<div><strong>🎯 Opportunité Marché :</strong><div style="color:#fef08a;">' + s.potential + '</div></div>' +
            '</div>' +
            '<div style="margin-top:0.6rem; display:flex; justify-content:flex-end;">' +
            '<button class="btn btn-primary" style="font-size:0.78rem; padding:0.3rem 0.65rem;" onclick="window.openMarketExplorerModal()">🏛️ Explorer les Appels d\'Offres de ce Secteur</button>' +
            '</div>';
    };

    window.openMarketExplorerModal = function() {
        window.openModal('modal-market-explorer');
        window.renderMarketTendersList();
    };

    window.openCreateProjectModal = function() {
        window.openModal('modal-create-project');
    };

    window.publicTendersDataset = [
        {
            id: 'marche_victor_hugo',
            title: 'Réhabilitation Voirie & Eaux Pluviales Avenue Victor Hugo',
            client: 'Ville de Sète (Direction Voirie)',
            budget: 450000,
            duration: '4 Mois',
            location: 'Sète Centre (Quai / Avenue)',
            deadline: '18/11/2026',
            lots: 'Lot 1 : Démolition, Rabotage 5cm, Bordures T2 granit, Enrobé BBSG 0/10 (1 200 t), Canalisations EP Ø400 béton.',
            dce: 'DCE-SETE-VH-2026.pdf (CCTP, BPU, DQE estimatif 450k€)'
        },
        {
            id: 'marche_voie_verte',
            title: 'Création Voie Verte & Piste Cyclable Intercommunale',
            client: 'Sète Agglopôle Méditerranée',
            budget: 280000,
            duration: '2.5 Mois',
            location: 'Balaruc-les-Bains / Thau Nord',
            deadline: '24/11/2026',
            lots: 'Lot Unique : Terrassement meuble, GNT 0/20 compactée (1 800 m²), Enrobé clair drainant / sablé, Signalétique OPPBTP.',
            dce: 'DCE-AGGLO-BALARUC-2026.pdf (Plans profils types, CCTP)'
        },
        {
            id: 'marche_aep_plage',
            title: 'Renouvellement Réseau AEP & Assainissement EU',
            client: 'Ville de Frontignan',
            budget: 620000,
            duration: '5 Mois',
            location: 'Frontignan Plage',
            deadline: '02/12/2026',
            lots: 'Lot 1 : Tranchées sous blindage caisson (R.4534), Tuyaux Fonte Ø200, PVC Assainissement Ø300, Réfection chaussée GNT + BBSG.',
            dce: 'DCE-FRONTIGNAN-AEP-2026.pdf (DICT, Fiches réseaux secs/humides)'
        },
        {
            id: 'marche_giratoire_meze',
            title: 'Aménagement Giratoire d\'Entrée de Ville RD613',
            client: 'Conseil Départemental de l\'Hérault (CD34)',
            budget: 510000,
            duration: '3.5 Mois',
            location: 'Mèze (Carrefour RD613)',
            deadline: '10/12/2026',
            lots: 'Lot 1 : Terrassement déblais/remblais (3 500 m³), Îlot central galets maçonnés, Couche de base GB4 + Roulement BBME 0/10.',
            dce: 'DCE-CD34-MEZE-GIRATOIRE.pdf (Profils en long, étude GTR classe B4)'
        }
    ];

    window.renderMarketTendersList = function() {
        var list = document.getElementById('market-tenders-list');
        if (!list) return;

        var tenders = window.publicTendersDataset;
        var html = '';

        tenders.forEach(function(t) {
            html += '<div class="card" style="margin-bottom:0.85rem; border:1px solid rgba(56,189,248,0.3); background:rgba(15,23,42,0.95); padding:1rem;">' +
                '<div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.5rem;">' +
                '<div>' +
                '<span class="badge-info" style="font-size:0.75rem; padding:2px 6px; border-radius:4px; font-weight:800;">' + t.client + '</span>' +
                '<h4 style="color:#ffffff; font-size:1.05rem; font-weight:900; margin:0.3rem 0;">' + t.title + '</h4>' +
                '<div style="font-size:0.82rem; color:#cbd5e1;">📍 Localisation : ' + t.location + ' • Délai : ' + t.duration + ' • Date Limite Réponse : <strong style="color:#f87171;">' + t.deadline + '</strong></div>' +
                '</div>' +
                '<div style="text-align:right;">' +
                '<span style="font-size:1.15rem; font-weight:900; color:#4ade80; font-family:var(--font-mono);">' + new Intl.NumberFormat('fr-FR').format(t.budget) + ' € HT</span>' +
                '<div style="font-size:0.75rem; color:#94a3b8;">Estimation Maître d\'Ouvrage</div>' +
                '</div>' +
                '</div>' +
                '<div style="background:#020617; border:1px solid var(--border); border-radius:6px; padding:0.6rem; margin:0.6rem 0; font-size:0.82rem; color:#cbd5e1;">' +
                '<strong style="color:#38bdf8;">📋 Consistance des Travaux :</strong> ' + t.lots + '<br>' +
                '<span style="color:#94a3b8; font-size:0.78rem;">📁 Pièces DCE associées : ' + t.dce + '</span>' +
                '</div>' +
                '<div style="display:flex; justify-content:flex-end; gap:0.6rem;">' +
                '<button class="btn btn-secondary" style="font-size:0.8rem; padding:0.35rem 0.75rem;" onclick="window.downloadSimulatedDCE(\'' + t.id + '\')">📄 Télécharger DCE Complet</button>' +
                '<button class="btn btn-primary" style="font-size:0.8rem; padding:0.35rem 0.85rem;" onclick="window.simulateTenderProposal(\'' + t.id + '\')">🎯 Répondre & Générer Offre (Devis Express)</button>' +
                '</div>' +
                '</div>';
        });

        list.innerHTML = html;
    };

    window.downloadSimulatedDCE = function(id) {
        var t = window.publicTendersDataset.find(function(x) { return x.id === id; });
        if (window.showNotification) window.showNotification('Téléchargement du dossier de consultation : ' + (t ? t.title : id), 'info');
    };

    window.simulateTenderProposal = function(id) {
        var t = window.publicTendersDataset.find(function(x) { return x.id === id; });
        if (!t) return;

        window.closeModal('modal-market-explorer');
        window.switchNav('devis_express');
        if (window.showNotification) window.showNotification('DCE "' + t.title + '" importé dans le calculateur Devis Express !', 'success');
    };

    window.handleCreateProject = function(e) {
        if (e && e.preventDefault) e.preventDefault();
        var name = document.getElementById('new-proj-name')?.value || 'Nouveau Chantier';
        var client = document.getElementById('new-proj-client')?.value || 'Ville de Sète';
        var budget = parseFloat(document.getElementById('new-proj-budget')?.value || 350000);

        window.userAccountState.projectsCount = (window.userAccountState.projectsCount || 0) + 1;
        window.updateAllHudAndTickerMetrics();
        window.closeModal('modal-create-project');

        if (window.showNotification) window.showNotification('Chantier "' + name + '" (' + new Intl.NumberFormat('fr-FR').format(budget) + ' €) intégré au Hub avec succès !', 'success');
        window.switchNav('projects_hub');
    };

window.switchNav = function(tabId, btn) {
        document.querySelectorAll('.tab-panel').forEach(function(p) {
            p.classList.remove('active');
            p.style.display = 'none';
        });
        document.querySelectorAll('.nav-item, .drawer-nav-item, .nav-btn, .quick-hub-btn').forEach(function(b) {
            b.classList.remove('active');
        });

        var target = document.getElementById('tab-' + tabId);
        if (target) {
            target.classList.add('active');
            target.style.display = 'block';
        }

        if (btn && btn.classList) {
            btn.classList.add('active');
        }
        var quickBtn = document.querySelector('.quick-hub-btn[onclick*=\"' + tabId + '\"]');
        if (quickBtn) quickBtn.classList.add('active');
        var drawerBtn = document.querySelector('.drawer-nav-item[onclick*=\"' + tabId + '\"]');
        if (drawerBtn) drawerBtn.classList.add('active');

        window.currentNav = tabId;

        try {
            if (tabId === 'cockpit') {
                if (window.renderCockpitAiAgents) window.renderCockpitAiAgents();
                if (window.renderCockpitProjectsSummary) window.renderCockpitProjectsSummary();
                if (window.initCockpitOsmMap) setTimeout(window.initCockpitOsmMap, 50);
            } else if (tabId === 'watchtower') {
                if (window.initWatchtowerMap) setTimeout(window.initWatchtowerMap, 100);
            } else if (tabId === 'projects_hub') {
                if (window.renderProjectsHubList) window.renderProjectsHubList();
            } else if (tabId === 'company') {
                if (window.renderFinancialCards) window.renderFinancialCards();
            } else if (tabId === 'technique_analyse') {
                if (window.initSimulation2DEnrobes) setTimeout(window.initSimulation2DEnrobes, 100);
                if (window.initTalus3DCanvas) setTimeout(window.initTalus3DCanvas, 100);
            } else if (tabId === 'safety_qse') {
                if (window.renderSafetyRecords) window.renderSafetyRecords();
            } else if (tabId === 'pointage_terrain') {
                if (window.renderPointageTeam) window.renderPointageTeam();
            } else if (tabId === 'rdc_pesee') {
                if (window.renderRdcPeseeTable) window.renderRdcPeseeTable();
            } else if (tabId === 'devis_express') {
                if (window.renderExpressCatalog) window.renderExpressCatalog();
            } else if (tabId === 'materiel_depot') {
                if (window.renderInventoryTable) window.renderInventoryTable();
            } else if (tabId === 'fournisseurs') {
                if (window.renderFournisseursTable) window.renderFournisseursTable();
            } else if (tabId === 'rh_personnel') {
                if (window.renderPersonnelTable) window.renderPersonnelTable();
            } else if (tabId === 'ccag_travaux') {
                if (window.renderCcagTree) window.renderCcagTree();
            } else if (tabId === 'obsidian_wiki') {
                if (window.renderObsidianGraph) setTimeout(window.renderObsidianGraph, 100);
            } else if (tabId === 'benchmarking') {
                if (window.renderBenchmarkingCards) window.renderBenchmarkingCards();
            } else if (tabId === 'legal_vault') {
                if (window.renderVaultDocuments) window.renderVaultDocuments();
            } else if (tabId === 'audit_blockchain') {
                if (window.renderBlockchainBlocks) window.renderBlockchainBlocks();
            }
        } catch(err) {
            console.warn('Tab init notice:', err);
        }
    };

    window.openModal = function(id) {
        var m = document.getElementById(id);
        if (m) {
            m.style.display = 'flex';
            m.classList.add('active');
        }
    };

    window.closeModal = function(id) {
        var m = document.getElementById(id);
        if (m) {
            m.style.display = 'none';
            m.classList.remove('active');
        }
    };

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
    const completeDQEItems = syntheseData.dqe_items || [];
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
            { id: 'depot', label: '🏭 Dépôt & Inventaire' },
            { id: 'projects_hub', label: '📁 Chantiers & Marchés' },
            { id: 'planning', label: '📅 Planning Gantt & Agenda' },
            { id: 'simulator', label: '🛰️ Watch Tower 3D' },
            { id: 'fleet', label: '🚜 Flotte Engins' },
            { id: 'catalog', label: '🛒 Outils & Matériaux' },
            { id: 'opbtp', label: '🦺 Signalétique OPBTP' },
            { id: 'safety', label: '🛡️ Sécurité & AIPR' },
            { id: 'sdp', label: '💰 28 SDP & TCD DQE' },
            { id: 'schemas', label: '📐 Technique & Analyse' },
            { id: 'procurement', label: '🛒 Fournisseurs' },
            { id: 'docs', label: '⚖️ Réglementation, Normes & Outils' },
            { id: 'benchmark', label: '📊 Benchmark & Inventaire' },
            { id: 'hr', label: '👷 Organigramme RH' },
            { id: 'rdc', label: '📋 Rapport RDC' },
            { id: 'obsidian', label: '📚 Base Obsidian' },
            { id: 'ledger', label: '⛓️ Ledger SHA-256' },
            { id: 'archives', label: '🗄️ Archives & GED' }
        ],
        'conduite': [
            { id: 'cockpit', label: '🎛️ Cockpit' },
            { id: 'depot', label: '🏭 Dépôt & Inventaire' },
            { id: 'projects_hub', label: '📁 Chantiers en Cours' },
            { id: 'planning', label: '📅 Planning & Agenda' },
            { id: 'simulator', label: '🛰️ Watch Tower' },
            { id: 'fleet', label: '🚜 Flotte & Dispatch' },
            { id: 'catalog', label: '🛒 Commandes Matériaux' },
            { id: 'opbtp', label: '🦺 Signalétique OPBTP' },
            { id: 'safety', label: '🛡️ Sécurité & AIPR' },
            { id: 'sdp', label: '💰 Sous-Détails & DQE' },
            { id: 'schemas', label: '📐 Technique & Analyse' },
            { id: 'procurement', label: '🛒 Fournisseurs' },
            { id: 'docs', label: '⚖️ Réglementation, Normes & Outils' },
            { id: 'benchmark', label: '📊 Benchmark Prix' },
            { id: 'hr', label: '👷 Équipes & RH' },
            { id: 'rdc', label: '📋 Journal RDC' },
            { id: 'obsidian', label: '📚 Base Obsidian' },
            { id: 'archives', label: '🗄️ Archives & GED' }
        ],
        'compagnon': [
            { id: 'compagnon_mobile', label: '📱 Mode Terrain & Mon Planning' },
            { id: 'depot', label: '🏭 Dépôt Matériel' },
            { id: 'planning', label: '📅 Planning Général' },
            { id: 'opbtp', label: '🦺 Balisage OPBTP' },
            { id: 'safety', label: '🛡️ Règles Sécurité' },
            { id: 'schemas', label: '📐 Technique' },
            { id: 'docs', label: '⚖️ Réglementation & Normes' },
            { id: 'rdc', label: '📋 Saisie RDC' },
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

    window.tabAliases = {
        'cockpit': 'cockpit',
        'company': 'company',
        'benchmarking': 'benchmark',
        'benchmark': 'benchmark',
        'legal_vault': 'archives',
        'archives': 'archives',
        'audit_blockchain': 'ledger',
        'ledger': 'ledger',
        'projects_hub': 'projects_hub',
        'projects': 'projects_hub',
        'planning_gantt': 'planning',
        'planning': 'planning',
        'pointage_terrain': 'compagnon_mobile',
        'compagnon_mobile': 'compagnon_mobile',
        'rdc_pesee': 'rdc',
        'rdc': 'rdc',
        'devis_express': 'sdp',
        'sdp': 'sdp',
        'technique_analyse': 'schemas',
        'schemas': 'schemas',
        'watchtower': 'simulator',
        'simulator': 'simulator',
        'safety_qse': 'safety',
        'safety': 'safety',
        'opbtp': 'opbtp',
        'materiel_depot': 'depot',
        'depot': 'depot',
        'fleet': 'fleet',
        'catalog': 'catalog',
        'fournisseurs': 'procurement',
        'procurement': 'procurement',
        'rh_personnel': 'hr',
        'hr': 'hr',
        'ccag_travaux': 'docs',
        'docs': 'docs',
        'obsidian_wiki': 'obsidian',
        'obsidian': 'obsidian'
    };

    function switchNav(rawTabId, btn) {
        const tabId = (window.tabAliases && window.tabAliases[rawTabId]) ? window.tabAliases[rawTabId] : rawTabId;
        
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.drawer-nav-item').forEach(b => b.classList.remove('active'));

        const target = document.getElementById('tab-' + tabId);
        if (target) {
            target.classList.add('active');
        } else {
            console.warn('Tab not found for ID:', tabId, 'raw ID was:', rawTabId);
        }

        if (btn && btn.classList) {
            btn.classList.add('active');
        }

        // Auto close flyout drawer on navigation
        if (typeof window.toggleSidebarDrawer === 'function') {
            window.toggleSidebarDrawer(false);
        }

        currentNav = tabId;

        try {
            if (tabId === 'cockpit') {
                renderCockpitAiAgents();
                renderCockpitProjectsSummary();
                setTimeout(initCockpitOsmMap, 50);
            }
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
                setTimeout(() => {
                    updateOpbtpSubdomainOptions();
                    calculateSignage();
                }, 50);
            }
            if (tabId === 'safety') {
                setTimeout(() => {
                    updateAiprPhaseDetails();
                    setAiprSituation('gaz');
                    renderAiprCanvas();
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
            if (tabId === 'docs') {
                setTimeout(() => {
                    if (typeof renderRegulatoryDocs === 'function') renderRegulatoryDocs();
                }, 50);
            }
            if (tabId === 'archives') {
                setTimeout(() => {
                    if (typeof renderArchives === 'function') renderArchives();
                }, 50);
            }
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

    function resetCockpitMapZoom() {
        resetCockpitMap();
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

    function openSelectedCockpitMapPointModal() {
        if (!selectedMapPoint) {
            alert("Veuillez d'abord cliquer sur un point du réseau territorial sur la carte.");
            return;
        }
        const pt = selectedMapPoint;
        if (pt.category === 'chantier' || pt.category === 'marche_public_ref') {
            if (typeof openProjectDetailsModal === 'function') {
                openProjectDetailsModal(pt.id || (pt.category === 'chantier' ? 'p-01' : 'dce-01'));
            } else {
                switchNav('projects_hub');
            }
        } else if (pt.category === 'depot') {
            switchNav('depot');
            if (typeof openDepotZoneModal === 'function') {
                openDepotZoneModal('all');
            }
        } else if (pt.category === 'fournisseur') {
            switchNav('procurement');
        } else if (pt.category === 'siege') {
            switchNav('company');
        } else {
            alert(`Fiche : ${pt.name}\n${pt.desc || ''}\nLocalisation : Occitanie`);
        }
    }

    // ==========================================
    // 5b. MULTI-ENTERPRISE PROFILES SWITCHER & MASTER DATASETS
    // ==========================================
    let currentCompanyProfile = 'occitanie_tp';

    const companyProfilesData = {
        'occitanie_tp': {
            id: 'occitanie_tp',
            name: 'Occitanie TP & VRD SAS',
            type: 'PME Établie Régionale',
            siret: '849 321 654 00018',
            capital: '500 000 €',
            siege: 'Sète / Montpellier (34)',
            caisse: 485200,
            bfr: 142800,
            ca_annuel: 1850000,
            ca_prev: 4250000,
            margin: 14.2,
            effectif_count: 24,
            fleet_count: 6,
            projects_count: 4,
            safety_status: '100% Conforme',
            safety_sub: '0 Incident • CSPS & DICT Validés',
            treasury_sub: 'BFR Couvert : 42 jours d\'exploitation',
            projects_sub: 'Alès, Sète, Pézenas, Montpellier',
            effectif_sub: '24 Salariés • CACES & AIPR à jour',
            desc: 'Entreprise générale de VRD et terrassement en Occitanie. Flotte lourde de 6 engins, 4 marchés publics en cours, dépôt central de 1200m².',
            
            projects: [
                {
                    id: "p-01",
                    code: "CH-2026-001",
                    name: "Giratoire RD906 Alès & Voie Nouvelle",
                    type: "internal",
                    ownership: "🏢 Notre Entreprise (En cours)",
                    badge_type: "Marché Public Actif",
                    loc: "Alès (30)",
                    location: "Alès (30)",
                    client: "Conseil Départemental du Gard (MOA)",
                    moe: "Cabinet Sud Ingénierie",
                    budget: 845000,
                    spent: 574600,
                    budget_used: 574600,
                    progress: 68,
                    status: "En cours",
                    manager: "Jean-Pierre Fabre",
                    site_chief: "Alain Martin",
                    chef: "Alain Martin (Conducteur: J-P. Fabre)",
                    workers_count: 6,
                    delai_consomme_pct: 70,
                    start_date: "12/01/2026",
                    end_date: "30/06/2026",
                    end: "30/06/2026",
                    desc: "Création d'un giratoire 4 branches RD906, décaissement 4 200 m³, pose de 850 ml de bordures T2/CS2, réseau pluvial béton Ø400 et 1 400 t de BBSG 0/14.",
                    assigned_machinery: [{ name: "Pelle Chenilles 24t Liebherr R924" }, { name: "Camion Benne 8x4 Scania G450" }],
                    assigned_tools: [{ name: "Laser Piper 200" }, { name: "Plaque Bomag BVP" }],
                    docs: [{ name: "CCTP_Ales", type: "pdf" }, { name: "PPSPS_Signe", type: "pdf" }, { name: "Plans_EXE", type: "dwg" }],
                    lots_breakdown: [
                        { name: "Lot 1 : Terrassement & Déblais (4 200 m³)", budget: 210000, progress: 100, ds: 142000, pv: 210000 },
                        { name: "Lot 2 : Assainissement Pluvial Ø400 (620 ml)", budget: 245000, progress: 85, ds: 168000, pv: 245000 },
                        { name: "Lot 3 : Bordures & Caniveaux T2/CS2 (850 ml)", budget: 115000, progress: 60, ds: 78000, pv: 115000 },
                        { name: "Lot 4 : Chaussée BBSG 0/14 & GNT (1 400 t)", budget: 275000, progress: 35, ds: 186000, pv: 275000 }
                    ],
                    steps: [
                        { name: "Piquetage & DICT / AIPR", progress: 100 },
                        { name: "Terrassement général & fond de forme", progress: 100 },
                        { name: "Pose collecteur pluvial Ø400", progress: 85 },
                        { name: "Pose bordures T2 et îlots", progress: 60 },
                        { name: "Enrobé BBSG 0/14 de roulement", progress: 0 }
                    ]
                },
                {
                    id: "p-02",
                    code: "CH-2026-002",
                    name: "Réseau Assainissement EU/EP & AEP Quai d'Alger",
                    type: "internal",
                    ownership: "🏢 Notre Entreprise (En cours)",
                    badge_type: "Marché Public Actif",
                    loc: "Sète (34)",
                    location: "Sète (34)",
                    client: "Sète Agglopôle Méditerranée",
                    moe: "Direction des Eaux du Bassin de Thau",
                    budget: 420000,
                    spent: 176400,
                    budget_used: 176400,
                    progress: 42,
                    status: "En cours",
                    manager: "Sophie Martinez",
                    site_chief: "Bruno Dupuis",
                    chef: "Bruno Dupuis (Conductrice: S. Martinez)",
                    workers_count: 4,
                    delai_consomme_pct: 45,
                    start_date: "01/02/2026",
                    end_date: "15/07/2026",
                    end: "15/07/2026",
                    desc: "Renouvellement en site maritime sensible du collecteur Fonte DN400 sous nappe avec caissons de blindage et rabattement de nappe par pointes filtrantes.",
                    assigned_machinery: [{ name: "Compacteur Tandem Bomag BW120" }, { name: "Mecalac 12MTX" }],
                    assigned_tools: [{ name: "Laser Piper 200" }, { name: "Pompe de rabattement" }],
                    docs: [{ name: "PAQ_Sète", type: "pdf" }, { name: "Note_Calcul_Blindage", type: "pdf" }],
                    lots_breakdown: [
                        { name: "Lot 1 : Rabattement de nappe & Blindage", budget: 120000, progress: 70, ds: 82000, pv: 120000 },
                        { name: "Lot 2 : Pose Canalisation Fonte DN400 (450 ml)", budget: 210000, progress: 45, ds: 145000, pv: 210000 },
                        { name: "Lot 3 : Réfection chaussée quai maritime", budget: 90000, progress: 10, ds: 61000, pv: 90000 }
                    ],
                    steps: [
                        { name: "Installation chantier & pompage", progress: 100 },
                        { name: "Fouille blindée sous nappe", progress: 60 },
                        { name: "Pose Fonte DN400 & branchements", progress: 40 },
                        { name: "Remblai GNT & Réfection quai", progress: 0 }
                    ]
                },
                {
                    id: "p-03",
                    code: "CH-2026-003",
                    name: "Aménagement Zone Artisanale & Plateforme Voirie",
                    type: "internal",
                    ownership: "🏢 Notre Entreprise (En cours)",
                    badge_type: "Marché Public Actif",
                    loc: "Pézenas (34)",
                    location: "Pézenas (34)",
                    client: "Communauté de Communes Hérault Méditerranée",
                    moe: "Territoires & Projets 34",
                    budget: 310000,
                    spent: 263500,
                    budget_used: 263500,
                    progress: 85,
                    status: "Finition",
                    manager: "Jean-Pierre Fabre",
                    site_chief: "Christian Lambert",
                    chef: "Christian Lambert",
                    workers_count: 3,
                    delai_consomme_pct: 88,
                    start_date: "15/11/2025",
                    end_date: "15/04/2026",
                    end: "15/04/2026",
                    desc: "Viabilisation de 14 parcelles artisanales, réseau pluvial bassin de rétention, bordures hautes A2 et voirie lourde 12t/essieu.",
                    assigned_machinery: [{ name: "Télescopique Manitou MT625" }],
                    assigned_tools: [{ name: "Niveau Optique Leica" }, { name: "Scie Thermique Stihl" }],
                    docs: [{ name: "CCTP_Pezenas", type: "pdf" }, { name: "Plan_Masse_ZA", type: "dwg" }],
                    lots_breakdown: [
                        { name: "Lot 1 : Plateforme & VRD Primaires", budget: 180000, progress: 100, ds: 124000, pv: 180000 },
                        { name: "Lot 2 : Bassin d'orage & Enrochement", budget: 75000, progress: 90, ds: 51000, pv: 75000 },
                        { name: "Lot 3 : Couche de roulement & Signalisation", budget: 55000, progress: 60, ds: 37000, pv: 55000 }
                    ],
                    steps: [
                        { name: "Terrassement & réseaux EU/EP", progress: 100 },
                        { name: "Bordures A2 et trottoirs", progress: 100 },
                        { name: "Bassin d'orage enroché", progress: 90 },
                        { name: "Enrobés & récolement EXE", progress: 50 }
                    ]
                },
                {
                    id: "p-04",
                    code: "CH-2026-004",
                    name: "Piste Cyclable & Réseaux Secs Tram Ligne 5",
                    type: "internal",
                    ownership: "🏢 Notre Entreprise (En cours)",
                    badge_type: "Marché Public Actif",
                    loc: "Montpellier (34)",
                    location: "Montpellier (34)",
                    client: "Montpellier Méditerranée Métropole / TaM",
                    moe: "Ingérop Conseil",
                    budget: 275000,
                    spent: 41250,
                    budget_used: 41250,
                    progress: 15,
                    status: "Démarrage",
                    manager: "Sophie Martinez",
                    site_chief: "David Roux",
                    chef: "David Roux",
                    workers_count: 4,
                    delai_consomme_pct: 18,
                    start_date: "01/03/2026",
                    end_date: "30/09/2026",
                    end: "30/09/2026",
                    desc: "Aménagement de 1.8 km de voie verte cyclable le long de la ligne 5 de tramway, pose de chambres de tirage L2T et 3 600 ml de fourreaux TPC Ø110/Ø160.",
                    assigned_machinery: [{ name: "Camionnette Atelier Renault Master" }],
                    assigned_tools: [{ name: "Aiguille de tirage 150m" }, { name: "Laser Rotatif" }],
                    docs: [{ name: "CCTP_Tram5", type: "pdf" }, { name: "Profils_Travers", type: "pdf" }],
                    lots_breakdown: [
                        { name: "Lot 1 : Terrassement & Décapage 1.8km", budget: 85000, progress: 35, ds: 58000, pv: 85000 },
                        { name: "Lot 2 : Réseaux Secs & Éclairage L2T", budget: 110000, progress: 10, ds: 75000, pv: 110000 },
                        { name: "Lot 3 : Enrobé grenaillé & Bordures T2", budget: 80000, progress: 0, ds: 54000, pv: 80000 }
                    ],
                    steps: [
                        { name: "Piquetage & Décapage terre végétale", progress: 40 },
                        { name: "Tranchée réseaux secs & chambres L2T", progress: 15 },
                        { name: "Grave non traitée & Bordures", progress: 0 },
                        { name: "Revêtement grenaillé et plantations", progress: 0 }
                    ]
                }
            ],

            fleet: [
                { id: "ENG-001", name: "Pelle Chenilles 24t Liebherr R924", cat: "Engin Lourd", type: "Pelle sur chenilles", brand: "Liebherr", loc: "Chantier Alès (RD906)", status: "Sur Chantier", val: 185000, price: 185000, hourly_cost: 95, vgp: "14/10/2026", immat: "CH-924-LB", fuel: 78, hours: 2840, weight: "24t", power: "129 kW", capacity: "1.4 m³", project: "Giratoire RD906 Alès", icon: "🚜" },
                { id: "ENG-002", name: "Pelleteuse Urbaine Mecalac 12MTX", cat: "Engin Lourd", type: "Pelle sur pneus", brand: "Mecalac", loc: "Dépôt Central Sète", status: "Disponible", val: 125000, price: 125000, hourly_cost: 80, vgp: "05/11/2026", immat: "MC-120-TX", fuel: 92, hours: 1420, weight: "10t", power: "85 kW", capacity: "0.8 m³", project: "Dépôt Sète", icon: "🚜" },
                { id: "ENG-003", name: "Camion Benne 8x4 Scania G450", cat: "Poids Lourd", type: "Camion benne 32t", brand: "Scania", loc: "Dépôt Central Sète", status: "Disponible", val: 145000, price: 145000, hourly_cost: 75, vgp: "22/12/2026", immat: "SC-450-TP", fuel: 65, hours: 3950, weight: "32t", power: "331 kW", capacity: "18 t", project: "Dépôt Sète", icon: "🚛" },
                { id: "ENG-004", name: "Compacteur Tandem Bomag BW120", cat: "Engin Lourd", type: "Compacteur vibrant", brand: "Bomag", loc: "Chantier Sète (Quai)", status: "Sur Chantier", val: 45000, price: 45000, hourly_cost: 45, vgp: "18/09/2026", immat: "BG-120-AD", fuel: 84, hours: 960, weight: "2.7t", power: "25 kW", capacity: "1.20 m", project: "Quai d'Alger Sète", icon: "🚜" },
                { id: "ENG-005", name: "Camionnette Atelier Renault Master", cat: "Utilitaire", type: "Fourgon atelier", brand: "Renault", loc: "Dépôt Central Sète", status: "Disponible", val: 38000, price: 38000, hourly_cost: 30, vgp: "30/08/2026", immat: "RN-380-AT", fuel: 90, hours: 1800, weight: "3.5t", power: "110 kW", capacity: "12 m³", project: "Dépôt Sète", icon: "🚐" },
                { id: "ENG-006", name: "Télescopique Manitou MT625", cat: "Engin Lourd", type: "Chariot tout-terrain", brand: "Manitou", loc: "Chantier Pézenas (ZA)", status: "Sur Chantier", val: 62000, price: 62000, hourly_cost: 55, vgp: "11/12/2026", immat: "MN-625-TP", fuel: 70, hours: 1230, weight: "4.8t", power: "55 kW", capacity: "2.5 t", project: "ZA Pézenas", icon: "🚜" }
            ],

            depot_inventory: [
                { id: "ENG-001", name: "Pelle Chenilles 24t Liebherr R924", cat: "Engin Lourd", zone: "parking", loc: "Parc Engins - P1", status: "Sur Chantier Alès", val: 185000, vgp: "14/10/2026", icon: "🚜" },
                { id: "ENG-002", name: "Pelleteuse Urbaine Mecalac 12MTX", cat: "Engin Lourd", zone: "parking", loc: "Parc Engins - P2", status: "Au Dépôt", val: 125000, vgp: "05/11/2026", icon: "🚜" },
                { id: "ENG-003", name: "Camion Benne 8x4 Scania G450", cat: "Poids Lourd", zone: "parking", loc: "Parc Engins - P3", status: "Au Dépôt", val: 145000, vgp: "22/12/2026", icon: "🚛" },
                { id: "ENG-004", name: "Compacteur Tandem Bomag BW120", cat: "Engin Lourd", zone: "parking", loc: "Parc Engins - P4", status: "Sur Chantier Sète", val: 45000, vgp: "18/09/2026", icon: "🚜" },
                { id: "MAT-001", name: "Grave GNT 0/31.5A Non Traitée", cat: "Granulat", zone: "casiers", loc: "Casier Extérieur n°1", status: "Stock : 65 Tonnes", val: 1170, vgp: "Conforme NF", icon: "🧱" },
                { id: "MAT-002", name: "Sable de Pose 0/4 Alluvionnaire", cat: "Granulat", zone: "casiers", loc: "Casier Extérieur n°2", status: "Stock : 45 Tonnes", val: 990, vgp: "Conforme NF", icon: "🏖️" },
                { id: "MAT-003", name: "Enrobé à Froid Noir en Seaux (25kg)", cat: "Enrobé", zone: "casiers", loc: "Casier Extérieur n°3", status: "Stock : 40 Seaux (1t)", val: 880, vgp: "Utilisable", icon: "🛢️" },
                { id: "CAN-001", name: "Tuyaux Fonte Intégral DN400 (L=6m)", cat: "Canalisation", zone: "racks", loc: "Rack Extérieur R1", status: "Stock : 180 ml", val: 19800, vgp: "Certifié AEP", icon: "🪵" },
                { id: "CAN-002", name: "Tubes PVC Assainissement CR8 Ø200", cat: "Canalisation", zone: "racks", loc: "Rack Extérieur R2", status: "Stock : 120 ml", val: 3240, vgp: "NF EN 1401", icon: "🪵" },
                { id: "OUT-001", name: "Laser de Canalisateur Piper 200", cat: "Topographie", zone: "atelier", loc: "Atelier - Armoire A1", status: "Au Dépôt (Chargé)", val: 3800, vgp: "Étalonné 2026", icon: "🔴" },
                { id: "OUT-002", name: "Scie Thermique à Sol Stihl TS800", cat: "Petit Outillage", zone: "atelier", loc: "Atelier - Étagère B2", status: "Au Dépôt (Révisée)", val: 1650, vgp: "02/08/2026", icon: "🪚" },
                { id: "OUT-003", name: "Plaque Vibrante 100kg Bomag BVP", cat: "Compactage", zone: "atelier", loc: "Atelier - Zone Sol", status: "Au Dépôt", val: 2400, vgp: "12/09/2026", icon: "🔨" },
                { id: "ADM-001", name: "Station Totale Robotisée Leica TS16", cat: "Topographie", zone: "bureaux", loc: "Bureaux CT - Salle DAO", status: "Au Dépôt", val: 22000, vgp: "Certifié Topo", icon: "📐" },
                { id: "ADM-002", name: "Drone DJI Matrice 300 RTK + LiDAR", cat: "Aérien", zone: "bureaux", loc: "Bureaux CT - Mallette", status: "Prêt au Vol", val: 18500, vgp: "DGAC Validé", icon: "🛰️" },
                { id: "ENV-001", name: "Séparateur Hydrocarbures 10 L/s", cat: "Environnement", zone: "lavage", loc: "Aire de Lavage - Dalle", status: "En Service (Vidangé)", val: 8500, vgp: "Conforme 2026", icon: "🚿" }
            ],

            cashflow_transactions: [
                { date: "18/04/2026", type: "Situation MOA", label: "Acompte Situation n°4 - CD30 Giratoire Alès", amount: 142500, status: "Encaissé" },
                { date: "15/04/2026", type: "Fournisseur", label: "Fourniture Tuyaux Fonte DN400 - PAM Saint-Gobain", amount: -28400, status: "Payé" },
                { date: "10/04/2026", type: "Situation MOA", label: "Acompte Situation n°2 - Sète Agglopôle Quai Alger", amount: 68900, status: "Encaissé" },
                { date: "31/03/2026", type: "Salaires", label: "Masse Salariale 24 Salariés & Charges URSSAF", amount: -112000, status: "Payé" },
                { date: "25/03/2026", type: "Carburant", label: "Approvisionnement GNR Cuve Dépôt 5000L - Total", amount: -7200, status: "Payé" },
                { date: "20/03/2026", type: "Location", label: "Location BRH & Raboteuse de sol - Loxam TP", amount: -6400, status: "Payé" }
            ],

            documents: [
                { id: "DOC-01", title: "PPSPS Alès - Plan Particulier Sécurité & Santé", cat: "Sécurité CSPS", chantier: "Giratoire RD906 Alès", date: "15/01/2026", format: "PDF (Signé)", size: "2.4 Mo" },
                { id: "DOC-02", title: "PAQ Sète - Plan d'Assurance Qualité Assainissement", cat: "Qualité ISO", chantier: "Quai d'Alger Sète", date: "02/02/2026", format: "PDF", size: "3.1 Mo" },
                { id: "DOC-03", title: "DICT Réseau Gaz & Élec Conjointe Pézenas", cat: "Réglementaire", chantier: "ZA Pézenas", date: "10/11/2025", format: "PDF (Récépissé)", size: "1.2 Mo" },
                { id: "DOC-04", title: "CCTP Lot 2 VRD Tram Ligne 5 Montpellier", cat: "Technique MOE", chantier: "Voie Verte Montpellier", date: "20/02/2026", format: "PDF", size: "4.8 Mo" },
                { id: "DOC-05", title: "Plan de Récolement EXE Giratoire Alès (DWG/PDF)", cat: "Topographie", chantier: "Giratoire RD906 Alès", date: "10/04/2026", format: "DWG/PDF", size: "8.5 Mo" }
            ],

            map_locations: [
                { id: "ch_01", name: "Giratoire RD906 Alès", category: "chantier", lat: 44.1284, lng: 4.0833, color: "#38bdf8", icon: "🏗️", ownership: "Interne Entreprise (En cours)", budget_ini: 845000, budget_used: 574600, progress: 68, chef: "Alain Martin", desc: "Giratoire RD906, réseaux pluviaux Ø400 et couche BBSG." },
                { id: "ch_02", name: "Quai d'Alger Sète", category: "chantier", lat: 43.4075, lng: 3.6928, color: "#38bdf8", icon: "🏗️", ownership: "Interne Entreprise (En cours)", budget_ini: 420000, budget_used: 176400, progress: 42, chef: "Bruno Dupuis", desc: "Assainissement maritime sous nappe Fonte DN400." },
                { id: "ch_03", name: "ZA Pézenas Voirie", category: "chantier", lat: 43.4600, lng: 3.4230, color: "#38bdf8", icon: "🏗️", ownership: "Interne Entreprise (En cours)", budget_ini: 310000, budget_used: 263500, progress: 85, chef: "Christian Lambert", desc: "Plateforme artisanale & voirie lourde 12t/essieu." },
                { id: "ch_04", name: "Voie Verte Tram 5 Montpellier", category: "chantier", lat: 43.6108, lng: 3.8767, color: "#38bdf8", icon: "🏗️", ownership: "Interne Entreprise (En cours)", budget_ini: 275000, budget_used: 41250, progress: 15, chef: "David Roux", desc: "Voie cyclable 1.8km et réseaux secs L2T." },
                { id: "dep_01", name: "Dépôt Central Sète Littoral (1200m²)", category: "depot", lat: 43.4150, lng: 3.7100, color: "#f59e0b", icon: "🏢", stock_val: "420 000 €", contact: "04 67 11 22 33", desc: "Bureaux 120m², Atelier 80m², Casiers 140t, Parc 6 engins." },
                { id: "eq_01", name: "Équipe 1 - Terrassement Alès", category: "equipe", lat: 44.1284, lng: 4.0833, color: "#10b981", icon: "👷‍♂️", leader: "A. Martin (6 ouvriers)", radio: "Canal 4 TP", desc: "Pelle Liebherr 24t + Scania 8x4." },
                { id: "eq_02", name: "Équipe 2 - Réseaux Maritimes Sète", category: "equipe", lat: 43.4075, lng: 3.6928, color: "#10b981", icon: "👷‍♂️", leader: "B. Dupuis (4 ouvriers)", radio: "Canal 2 TP", desc: "Blindage & rabattement de nappe." },
                { id: "fourn_01", name: "Carrières du Languedoc", category: "fournisseur", lat: 43.5500, lng: 3.5200, color: "#ec4899", icon: "🏭", product: "GNT 0/31.5 & Concassés", distance: "14 km", desc: "Fournisseur agréé matériaux routiers." },
                { id: "fourn_02", name: "Bétons Occitanie (BPE)", category: "fournisseur", lat: 43.4200, lng: 3.6600, color: "#ec4899", icon: "🏭", product: "Béton C25/30 & Bordures NF", distance: "8 km", desc: "Centrale béton prêt à l'emploi." },
                { id: "fourn_03", name: "PAM Saint-Gobain Canalisation", category: "fournisseur", lat: 43.6500, lng: 3.9000, color: "#ec4899", icon: "🏭", product: "Tuyaux Fonte DN400", distance: "22 km", desc: "Fabricant fontes et raccords AEP." }
            ],

            hr_employees: [
                { id: "HR-001", name: "Jean-Pierre Fabre", role: "Conducteur de Travaux Principal", cat: "Cadre", site: "Chantiers Alès & Pézenas", phone: "06 12 34 56 78", email: "jp.fabre@occitanietp.fr", caces: "AIPR Concepteur • SST", exp: "14 ans", icon: "👷‍♂️" },
                { id: "HR-002", name: "Sophie Martinez", role: "Conductrice de Travaux VRD", cat: "Cadre", site: "Chantiers Sète & Montpellier", phone: "06 23 45 67 89", email: "s.martinez@occitanietp.fr", caces: "AIPR Concepteur • CSPS", exp: "9 ans", icon: "👷‍♀️" },
                { id: "HR-003", name: "Alain Martin", role: "Chef de Chantier Terrassement", cat: "Maîtrise", site: "Chantier Alès (RD906)", phone: "06 34 56 78 90", email: "a.martin@occitanietp.fr", caces: "AIPR Encadrant • CACES R482", exp: "18 ans", icon: "👷‍♂️" },
                { id: "HR-004", name: "Bruno Dupuis", role: "Chef de Chantier Canalisateur", cat: "Maîtrise", site: "Chantier Sète (Quai)", phone: "06 45 67 89 01", email: "b.dupuis@occitanietp.fr", caces: "AIPR Encadrant • CACES A/B", exp: "12 ans", icon: "👷‍♂️" },
                { id: "HR-005", name: "Thibault Blanc", role: "Géomètre-Topographe VRD", cat: "Technicien", site: "Studio DAO & Chantiers", phone: "06 56 78 90 12", email: "t.blanc@occitanietp.fr", caces: "Télépilote Drone DGAC • Topo", exp: "7 ans", icon: "📐" },
                { id: "HR-006", name: "19 Compagnons & Chauffeurs", role: "Maçons VRD, Poseurs, Chauffeurs PL", cat: "Ouvriers", site: "Ensemble des chantiers", phone: "Standard Dépôt", email: "equipe@occitanietp.fr", caces: "CACES R482 A/B/C/F • AIPR Opérateur", exp: "Moyenne 8 ans", icon: "👷‍♂️" }
            ],

            hr_hierarchy: {
                name: "Jean-Pierre Fabre",
                role: "Conducteur de Travaux Principal / Direction Exploitation",
                rank: "direction",
                tel: "06 12 34 56 78",
                aipr: "Concepteur / Encadrant",
                caces: "Tous R482",
                badge: "Direction TP",
                children: [
                    {
                        name: "Antoine Martin",
                        role: "Chef de Chantier Travaux Publics (RD906 Alès)",
                        rank: "chef_chantier",
                        tel: "06 23 45 67 89",
                        aipr: "Encadrant",
                        caces: "R482 Cat B1 / C1",
                        badge: "Chantier Alès",
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
                                role: "Chef d'Équipe Application Enrobés (Pézenas)",
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
                        name: "Sophie Martinez",
                        role: "Conductrice de Travaux VRD (Sète & Montpellier)",
                        rank: "direction",
                        tel: "06 34 56 78 90",
                        aipr: "Concepteur / Encadrant",
                        caces: "AIPR CSPS",
                        badge: "Sète & Tram 5",
                        children: [
                            {
                                name: "Bruno Dupuis",
                                role: "Chef de Chantier Réseaux Maritimes",
                                rank: "chef_chantier",
                                tel: "06 45 67 89 01",
                                aipr: "Encadrant",
                                caces: "R482 Cat A/B",
                                badge: "Quai d'Alger",
                                children: [
                                    { name: "David Roux", role: "Poseur Réseaux Secs & Tramway", rank: "compagnon", tel: "06 78 90 12 34", aipr: "Opérateur", caces: "Habilitation H0B0", badge: "Tram L5" }
                                ]
                            },
                            {
                                name: "Thibault Blanc",
                                role: "Géomètre-Topographe VRD & Télépilote LiDAR",
                                rank: "expert_tech",
                                tel: "06 56 78 90 12",
                                aipr: "Concepteur",
                                caces: "Drone DGAC / GNSS",
                                badge: "Studio DAO / Topo",
                                children: [
                                    { name: "David Lemoine", role: "Technicien DAO / BIM Infra IFC", rank: "compagnon", tel: "06 11 22 33 44", aipr: "Sensibilisé", caces: "Mensura / Covadis", badge: "BIM Infra" }
                                ]
                            }
                        ]
                    }
                ]
            },

            ai_agents: [
                { id: "agent-treso", name: "Agent IA Trésorerie & BFR", avatar: "💰", role: "Finances TP", status: "Optimal", text: "Trésorerie saine (485 200 €). BFR couvert à 42 jours. Situation n°4 Alès (142.5k€) validée par la MOE." },
                { id: "agent-securite", name: "Agent IA Sécurité CSPS / DICT", avatar: "🦺", role: "Prévention", status: "Conforme", text: "0 accident du travail. Tous les PPSPS et récépissés DICT sont validés et archivés." },
                { id: "agent-planning", name: "Agent IA Planning & Cadences", avatar: "📅", role: "Ordonnancement", status: "Dans les temps", text: "Avancement global à 68% sur Alès. Livraison BBSG confirmée pour demain 08h00." }
            ]
        },

        'compte_neuf': {
            id: 'compte_neuf',
            name: 'Nouvelle Entreprise TP (Démarrage Zéro)',
            type: 'Compte Vierge / Typique',
            siret: '912 456 789 00012 (En immatriculation)',
            capital: '10 000 € (Bloqué notaire)',
            siege: 'Montpellier Millénaire (Pépinière)',
            caisse: 0,
            bfr: 0,
            ca_annuel: 0,
            ca_prev: 180000,
            margin: 0,
            effectif_count: 1,
            fleet_count: 0,
            projects_count: 0,
            safety_status: 'En configuration',
            safety_sub: 'Compte Vierge • Prêt pour 1er Marché',
            treasury_sub: '0€ Disponible • Capital souscrit en attente',
            projects_sub: '0 Marché engagé • Lancez votre 1er DCE',
            effectif_sub: '1 Salarié Fondateur • Recrutements ouverts',
            desc: 'Profil vierge sans passif ni engagement. Conçu pour créer, chiffrer et planifier votre entreprise TP étape par étape à partir d\'une page blanche.',

            projects: [],

            fleet: [],

            depot_inventory: [
                { id: "INIT-001", name: "Box de Stockage Loué 30 m²", cat: "Immobilier", zone: "bureaux", loc: "Pépinière d'Entreprises TP", status: "Actif (Loué)", val: 0, vgp: "Bail en cours", icon: "🏢" },
                { id: "INIT-002", name: "Kit de Balisage Urgence (6 cônes K5a + 2 AK5)", cat: "Sécurité", zone: "atelier", loc: "Magasin Outillage", status: "Disponible", val: 350, vgp: "NF Équipement", icon: "🚧" },
                { id: "INIT-003", name: "Caisse à Outils Complète Maçonnerie TP", cat: "Petit Outillage", zone: "atelier", loc: "Établi Mobile", status: "Disponible", val: 450, vgp: "Conforme CE", icon: "🧰" }
            ],

            cashflow_transactions: [
                { date: "01/04/2026", type: "Capital Initial", label: "Dépôt de capital social souscrit (compte bloqué notaire)", amount: 10000, status: "Bloqué Banque" }
            ],

            documents: [
                { id: "DOC-NEW-01", title: "Statuts constitutifs SASU TP & VRD", cat: "Juridique", chantier: "Siège Entreprise", date: "01/04/2026", format: "PDF (Signé)", size: "1.1 Mo" },
                { id: "DOC-NEW-02", title: "Attestation RC Décennale & Responsabilité Civile (En cours)", cat: "Assurance", chantier: "Siège Entreprise", date: "05/04/2026", format: "PDF", size: "0.8 Mo" },
                { id: "DOC-NEW-03", title: "Modèle Vierge Devis Déboursé Sec & Bordereau de Prix", cat: "Chiffrage", chantier: "Modèle Type", date: "10/04/2026", format: "XLSX/PDF", size: "1.5 Mo" }
            ],

            map_locations: [
                { id: "siege_01", name: "Pépinière Entreprises TP (Siège)", category: "siege", lat: 43.6050, lng: 3.9100, color: "#38bdf8", icon: "🏢", ownership: "Siège Social (Création)", budget_ini: 0, budget_used: 0, progress: 0, chef: "Alexandre Durand", desc: "Bureau de démarrage et domiciliation juridique." },
                { id: "fourn_loc", name: "Point P Travaux Publics Montpellier", category: "fournisseur", lat: 43.5900, lng: 3.8800, color: "#ec4899", icon: "🏭", product: "Matériaux VRD & Outillage", distance: "4 km", desc: "Partenaire négoce matériaux pour nouvelles entreprises." },
                { id: "dce_test", name: "DCE Barbazan (Chantier d'Entraînement)", category: "marche_public_ref", lat: 44.1120, lng: 4.0950, color: "#a855f7", icon: "🏛️", ownership: "DCE Référence Étalon", budget_ini: 920000, budget_used: 0, progress: 0, chef: "Support Pédagogique", desc: "Dossier type pour s'entraîner au chiffrage déboursé sec." }
            ],

            hr_employees: [
                { id: "HR-DIR", name: "Alexandre Durand", role: "Président / Conducteur de Travaux", cat: "Direction", site: "Siège & Études de Prix", phone: "06 00 11 22 33", email: "contact@nouvelle-tp.fr", caces: "AIPR Concepteur • Bac+5 TP", exp: "Créateur d'entreprise", icon: "👷‍♂️" }
            ],

            hr_hierarchy: {
                name: "Alexandre Durand",
                role: "Fondateur & Président SASU / Conducteur de Travaux",
                rank: "direction",
                tel: "06 00 11 22 33",
                aipr: "Concepteur",
                caces: "Bac+5 TP & CACES",
                badge: "Fondateur Gérant",
                children: [
                    {
                        name: "Poste à Pourvoir (Recrutement)",
                        role: "Chef de Chantier VRD / Travaux Publics",
                        rank: "chef_chantier",
                        tel: "En cours...",
                        aipr: "Encadrant requis",
                        caces: "R482 Cat B1",
                        badge: "Poste Ouvert",
                        children: [
                            { name: "Poste à Pourvoir", role: "Maçon VRD / Canalisateur Qualifié", rank: "compagnon", tel: "En cours...", aipr: "Opérateur", caces: "Pose Tuyaux", badge: "Poste Ouvert" },
                            { name: "Poste à Pourvoir", role: "Chauffeur Poids Lourds Benne 8x4", rank: "compagnon", tel: "En cours...", aipr: "Sensibilisé", caces: "Permis EC / FIMO", badge: "Poste Ouvert" }
                        ]
                    }
                ]
            },

            ai_agents: [
                { id: "agent-setup", name: "Agent IA Démarrage & Amorçage", avatar: "🚀", role: "Conseil Création", status: "Prêt", text: "Compte vierge prêt. Utilisez le module Technique & Analyse pour chiffrer vos premières fiches de tâches ou lancez un premier appel d'offres." },
                { id: "agent-finances", name: "Agent IA Finances & Trésorerie", avatar: "📊", role: "Gestion BFR", status: "En attente", text: "0€ engagé. Privilégiez la location courte durée d'engins (Kiloutou/Loxam) sur vos 2 premiers chantiers pour préserver le BFR." }
            ]
        },

        'stagiaire_tp': {
            id: 'stagiaire_tp',
            name: 'Stagiaire TP & Conduite de Travaux (Études M4-L & Barbazan)',
            type: 'Dossiers de Cours & Formation',
            siret: '775 889 123 00045 (Formation)',
            capital: '150 000 €',
            siege: 'École Nationale TP / ESTP / ESTPO Occitanie',
            caisse: 150000,
            bfr: 45000,
            ca_annuel: 890000,
            ca_prev: 1200000,
            margin: 12.8,
            effectif_count: 9,
            fleet_count: 3,
            projects_count: 3,
            safety_status: 'Conforme Pédagogique',
            safety_sub: 'Exercices CSPS & Fiches Ratios FNTP',
            treasury_sub: 'Budget d\'Études & DCE en cours',
            projects_sub: 'Giratoire Barbazan, Aurouer, Béziers',
            effectif_sub: '9 Collaborateurs & Stagiaires d\'Étude',
            desc: 'Profil pédagogique basé sur les dossiers réels d\'apprentissage : DCE Giratoire Barbazan M4-L, Lotissement Aurouer 2021, Déviation Noé, fiches de cadences et calculs de prix de revient.',

            projects: [
                {
                    id: "dce-01",
                    code: "DCE-BARBAZAN",
                    name: "Aménagement Giratoire Barbazan (DCE M4-L)",
                    type: "dce_ref",
                    ownership: "🏛️ Marché Public Réel DCE Étalon",
                    badge_type: "Marché Public DCE Référence",
                    loc: "Barbazan-Debat / Tarbes (65)",
                    location: "Barbazan-Debat / Tarbes (65)",
                    client: "Conseil Départemental (Maîtrise d'Ouvrage Publique)",
                    moe: "Direction des Infrastructures & Routes",
                    budget: 920000,
                    spent: 506000,
                    budget_used: 506000,
                    progress: 55,
                    status: "Étude & Exécution",
                    manager: "Michel Tuteur",
                    site_chief: "Éric Lefebvre",
                    chef: "M. Tuteur ESTP (Stagiaire: Éric L.)",
                    workers_count: 5,
                    delai_consomme_pct: 60,
                    start_date: "01/02/2026",
                    end_date: "31/07/2026",
                    end: "31/07/2026",
                    desc: "Dossier de consultation d'apprentissage M4-L : Giratoire 3 branches, déviation Noé, DQE 45 lignes, dimensionnement chaussée GNT 0/31.5 et enrobé BBSG.",
                    assigned_machinery: [{ name: "Pelleteuse 14t Caterpillar 314E" }, { name: "Camion Bi-benne 6x4 MAN TGS" }],
                    assigned_tools: [{ name: "Laser de Canalisateur Piper 100" }, { name: "Niveau Leica Sprinter" }],
                    docs: [{ name: "CCTP_Barbazan", type: "pdf" }, { name: "Memoire_Technique_20_20", type: "pdf" }],
                    lots_breakdown: [
                        { name: "Lot 1 : Terrassement & Déblais (5 400 m³)", budget: 280000, progress: 100, ds: 195000, pv: 280000 },
                        { name: "Lot 2 : Assainissement & Bassin d'orage", budget: 310000, progress: 60, ds: 218000, pv: 310000 },
                        { name: "Lot 3 : Chaussée & Giratoire Béton / Enrobé", budget: 330000, progress: 20, ds: 232000, pv: 330000 }
                    ],
                    steps: [
                        { name: "Étude DCE & Mémoire Technique", progress: 100 },
                        { name: "Piquetage & Balisage Déviation Noé", progress: 100 },
                        { name: "Terrassement & Déblais généraux", progress: 100 },
                        { name: "Pose collecteur pluvial Ø500", progress: 50 },
                        { name: "Bordures T2 & Couche BBSG", progress: 0 }
                    ]
                },
                {
                    id: "dce-02",
                    code: "DCE-AUROUER",
                    name: "Lotissement Résidentiel Les Chênes (Aurouer 2021)",
                    type: "dce_ref",
                    ownership: "🏛️ Marché Public Réel DCE Étalon",
                    badge_type: "Marché Public DCE Référence",
                    loc: "Aurouer (03)",
                    location: "Aurouer (03)",
                    client: "Société d'Aménagement Foncier",
                    moe: "Bureau d'Études VRD Centre",
                    budget: 380000,
                    spent: 304000,
                    budget_used: 304000,
                    progress: 80,
                    status: "En cours",
                    manager: "Michel Tuteur",
                    site_chief: "Laurent Vasseur",
                    chef: "L. Formateur VRD",
                    workers_count: 3,
                    delai_consomme_pct: 82,
                    start_date: "10/10/2025",
                    end_date: "30/04/2026",
                    end: "30/04/2026",
                    desc: "Viabilisation complète de 42 lots pavillonnaires : réseaux EU/EP séparatifs, voirie partagée calcaire et noue paysagère.",
                    assigned_machinery: [{ name: "Compacteur Mixte Hamm HD14" }],
                    assigned_tools: [{ name: "Théodolite Topcon DT-200" }],
                    docs: [{ name: "CCTP_Aurouer", type: "pdf" }, { name: "SOPRE_Dechets", type: "pdf" }],
                    lots_breakdown: [
                        { name: "Lot 1 : Terrassement & Voirie Primaire", budget: 140000, progress: 100, ds: 98000, pv: 140000 },
                        { name: "Lot 2 : Réseaux Eaux Usées & Eau Potable", budget: 150000, progress: 90, ds: 105000, pv: 150000 },
                        { name: "Lot 3 : Finitions & Noues Paysagères", budget: 90000, progress: 45, ds: 62000, pv: 90000 }
                    ],
                    steps: [
                        { name: "Terrassement des voiries", progress: 100 },
                        { name: "Pose tuyaux PVC CR8 Ø200", progress: 100 },
                        { name: "Branchements particuliers", progress: 80 },
                        { name: "Enrobé trottoirs & noues", progress: 40 }
                    ]
                },
                {
                    id: "dce-03",
                    code: "DCE-BEZIERS",
                    name: "Plateforme Logistique & Déboursé Sec (Béziers)",
                    type: "dce_ref",
                    ownership: "🏛️ Projet d'Étude Cadences",
                    badge_type: "Étude de Prix Étalon",
                    loc: "Béziers Ouest (34)",
                    location: "Béziers Ouest (34)",
                    client: "Investisseur Privé Logistique",
                    moe: "Ingénierie BTP Méditerranée",
                    budget: 210000,
                    spent: 52500,
                    budget_used: 52500,
                    progress: 25,
                    status: "En cours",
                    manager: "Michel Tuteur",
                    site_chief: "Paul Ingénieur",
                    chef: "P. Ingénieur TP",
                    workers_count: 3,
                    delai_consomme_pct: 28,
                    start_date: "01/03/2026",
                    end_date: "30/08/2026",
                    end: "30/08/2026",
                    desc: "Plateforme 15 000 m² : calculs de cadences pelles 24t, temps unitaires de compactage et prix de revient déboursé sec.",
                    assigned_machinery: [{ name: "Pelleteuse 14t Caterpillar 314E" }],
                    assigned_tools: [{ name: "Station CAO Mensura" }],
                    docs: [{ name: "Etude_Debourse_Excel", type: "xlsx" }],
                    lots_breakdown: [
                        { name: "Lot 1 : Décapage & Traitement chaux/ciment", budget: 120000, progress: 40, ds: 84000, pv: 120000 },
                        { name: "Lot 2 : Réseau eaux pluviales lourdes", budget: 90000, progress: 0, ds: 62000, pv: 90000 }
                    ],
                    steps: [
                        { name: "Décapage 15 000 m²", progress: 60 },
                        { name: "Traitement de sol chaux", progress: 15 },
                        { name: "Pose collecteurs EP béton", progress: 0 }
                    ]
                }
            ],

            fleet: [
                { id: "ENG-ST01", name: "Pelleteuse 14t Caterpillar 314E", cat: "Engin Didactique", type: "Pelle moyenne", brand: "Caterpillar", loc: "Chantier Barbazan (M4-L)", status: "Sur Chantier", val: 110000, price: 110000, hourly_cost: 75, vgp: "01/10/2026", immat: "CAT-314-E", fuel: 80, hours: 2100, weight: "14t", power: "75 kW", capacity: "0.7 m³", project: "Giratoire Barbazan", icon: "🚜" },
                { id: "ENG-ST02", name: "Compacteur Mixte Hamm HD14", cat: "Engin Didactique", type: "Compacteur mixte", brand: "Hamm", loc: "Chantier Aurouer", status: "Sur Chantier", val: 35000, price: 35000, hourly_cost: 40, vgp: "15/11/2026", immat: "HM-140-TP", fuel: 88, hours: 1250, weight: "4.5t", power: "35 kW", capacity: "1.38 m", project: "Lotissement Aurouer", icon: "🚜" },
                { id: "ENG-ST03", name: "Camion Bi-benne 6x4 MAN TGS", cat: "Poids Lourd", type: "Porteur 26t", brand: "MAN", loc: "Plateforme Béziers", status: "Disponible", val: 95000, price: 95000, hourly_cost: 65, vgp: "05/12/2026", immat: "MAN-626-TP", fuel: 75, hours: 2400, weight: "26t", power: "294 kW", capacity: "14 t", project: "Béziers", icon: "🚛" }
            ],

            depot_inventory: [
                { id: "ST-001", name: "Niveau Numérique Leica Sprinter 250M", cat: "Topographie", zone: "bureaux", loc: "Studio Topo Étudiants", status: "Au Dépôt", val: 2400, vgp: "Calibré 2026", icon: "📐" },
                { id: "ST-002", name: "Théodolite Électronique Topcon DT-200", cat: "Topographie", zone: "bureaux", loc: "Studio Topo Étudiants", status: "Au Dépôt", val: 1800, vgp: "Calibré 2026", icon: "📐" },
                { id: "ST-003", name: "Laser de Canalisateur Piper 100", cat: "Topographie", zone: "atelier", loc: "Magasin didactique", status: "Au Dépôt", val: 2900, vgp: "Étalonné", icon: "🔴" },
                { id: "ST-004", name: "Casier d'Apprentissage GNT 0/31.5 (40t)", cat: "Granulat", zone: "casiers", loc: "Casier d'Essais n°1", status: "Stock : 40 Tonnes", val: 720, vgp: "Conforme NF", icon: "🧱" },
                { id: "ST-005", name: "Station CAO Mensura Genius & Civil 3D", cat: "DAO", zone: "bureaux", loc: "Salle informatique", status: "En service", val: 6500, vgp: "Licence Éducation", icon: "💻" }
            ],

            cashflow_transactions: [
                { date: "15/04/2026", type: "Situation DCE", label: "Acompte Situation n°3 - Giratoire Barbazan DCE", amount: 180000, status: "Encaissé (Simulé)" },
                { date: "10/04/2026", type: "Matériaux", label: "Fourniture GNT 0/31.5A Calcaire - Carrière Cemex", amount: -32400, status: "Payé" },
                { date: "01/04/2026", type: "Location", label: "Location Pelle 14t & Compacteur Hamm HD14", amount: -12500, status: "Payé" },
                { date: "20/03/2026", type: "Subvention", label: "Subvention Région Formation Conduite de Travaux", amount: 14900, status: "Encaissé" }
            ],

            documents: [
                { id: "DOC-DCE-01", title: "CCTP Complet Giratoire Barbazan (DCE M4-L)", cat: "DCE Référence", chantier: "Giratoire Barbazan", date: "12/01/2026", format: "PDF", size: "6.2 Mo" },
                { id: "DOC-DCE-02", title: "Mémoire Technique d'Appel d'Offres VRD (Exemple 20/20)", cat: "Mémoire AO", chantier: "Giratoire Barbazan", date: "20/01/2026", format: "PDF", size: "4.5 Mo" },
                { id: "DOC-DCE-03", title: "Fichier Excel Déboursé Sec & Ratios Temps Unitaires", cat: "Chiffrage", chantier: "Plateforme Béziers", date: "05/03/2026", format: "XLSX", size: "3.1 Mo" },
                { id: "DOC-DCE-04", title: "SOPRE - Schéma Organisationnel Gestion des Déchets", cat: "Environnement", chantier: "Lotissement Aurouer", date: "15/02/2026", format: "PDF", size: "1.9 Mo" }
            ],

            map_locations: [
                { id: "dce_barb", name: "Giratoire Barbazan (DCE M4-L)", category: "marche_public_ref", lat: 44.1120, lng: 4.0950, color: "#a855f7", icon: "🏛️", ownership: "Marché Public Réel DCE Étalon", budget_ini: 920000, budget_used: 506000, progress: 55, chef: "M. Tuteur ESTP", desc: "Dossier consultation de référence, déviation Noé, DQE 45 lignes." },
                { id: "dce_auro", name: "Lotissement Aurouer (DCE Public)", category: "marche_public_ref", lat: 46.6800, lng: 3.3000, color: "#a855f7", icon: "🏛️", ownership: "Marché Public Réel DCE Étalon", budget_ini: 380000, budget_used: 304000, progress: 80, chef: "L. Formateur VRD", desc: "Viabilisation 42 lots et assainissement EU/EP." },
                { id: "dce_beziers", name: "Plateforme Logistique Béziers", category: "chantier", lat: 43.3400, lng: 3.2200, color: "#38bdf8", icon: "🏗️", ownership: "Projet d'Étude Cadences", budget_ini: 210000, budget_used: 52500, progress: 25, chef: "P. Ingénieur TP", desc: "Terrassement grande masse et étude de prix." },
                { id: "centre_forma", name: "Centre de Formation Conduite Travaux", category: "siege", lat: 43.6200, lng: 3.8600, color: "#f59e0b", icon: "🎓", stock_val: "150 000 €", contact: "04 67 99 88 77", desc: "Plateforme pédagogique, studio DAO et parc matériel école." }
            ],

            hr_employees: [
                { id: "HR-TUT", name: "Michel Tuteur", role: "Conducteur de Travaux Principal (Tuteur)", cat: "Encadrement", site: "Chantier Barbazan & École", phone: "06 88 77 66 55", email: "m.tuteur@formation-tp.fr", caces: "AIPR Concepteur • ESTP 1998", exp: "28 ans", icon: "👨‍🏫" },
                { id: "HR-STAG", name: "Éric Lefebvre", role: "Stagiaire Assistant Conducteur de Travaux", cat: "Étudiant", site: "Chantier Barbazan & Aurouer", phone: "06 11 22 33 44", email: "eric.lefebvre@formation-tp.fr", caces: "AIPR Encadrant • En cours", exp: "Licence Pro TP", icon: "👷‍♂️" },
                { id: "HR-CHEF1", name: "Laurent Vasseur", role: "Chef de Chantier Formateur", cat: "Maîtrise", site: "Chantier Aurouer", phone: "06 22 33 44 55", email: "l.vasseur@formation-tp.fr", caces: "AIPR Encadrant • CACES A/B", exp: "16 ans", icon: "👷‍♂️" },
                { id: "HR-COMP4", name: "6 Compagnons en Formation", role: "Maçons VRD & Canalisateurs Apprenants", cat: "Stagiaires", site: "Ensemble des sites didactiques", phone: "Standard Formation", email: "groupe@formation-tp.fr", caces: "CACES R482 • AIPR Opérateur", exp: "Formation active", icon: "👷‍♂️" }
            ],

            hr_hierarchy: {
                name: "Michel Tuteur",
                role: "Conducteur de Travaux Senior (Tuteur Pédagogique)",
                rank: "direction",
                tel: "06 88 77 66 55",
                aipr: "Concepteur / Encadrant",
                caces: "ESTP 1998 • R482",
                badge: "Tuteur Entreprise",
                children: [
                    {
                        name: "Éric Lefebvre",
                        role: "Stagiaire Assistant Conducteur de Travaux",
                        rank: "chef_chantier",
                        tel: "06 11 22 33 44",
                        aipr: "Encadrant (En cours)",
                        caces: "Licence Pro TP",
                        badge: "DCE Barbazan M4-L",
                        children: [
                            {
                                name: "Laurent Vasseur",
                                role: "Chef de Chantier Formateur Application",
                                rank: "chef_equipe",
                                tel: "06 22 33 44 55",
                                aipr: "Encadrant",
                                caces: "R482 Cat A/B",
                                badge: "Chantier Aurouer",
                                children: [
                                    { name: "Groupe 4 Apprenants", role: "Maçons VRD & Canalisateurs Stagiaires", rank: "compagnon", tel: "École TP", aipr: "Opérateur", caces: "CACES R482", badge: "Apprenants TP" }
                                ]
                            }
                        ]
                    },
                    {
                        name: "Céline Dupuy",
                        role: "Formatrice Topographie & Métrés DQE",
                        rank: "expert_tech",
                        tel: "06 33 44 55 66",
                        aipr: "Concepteur",
                        caces: "Leica / Mensura",
                        badge: "Études & Ratios",
                        children: [
                            { name: "2 Techniciens d'Études", role: "Chiffrage Déboursé Sec & Plans EXE", rank: "compagnon", tel: "Studio École", aipr: "Sensibilisé", caces: "DAO Covadis", badge: "Études DCE" }
                        ]
                    }
                ]
            },

            ai_agents: [
                { id: "agent-cours", name: "Agent IA Tuteur Pédagogique", avatar: "🎓", role: "Méthodes & DCE", status: "Actif", text: "DCE Barbazan M4-L ouvert. Vérifiez les cadences théoriques de pose de bordures (40 ml/j) par rapport aux ratios FNTP." },
                { id: "agent-debourse", name: "Agent IA Déboursé Sec & Coefficients", avatar: "📐", role: "Étude de Prix", status: "Vérifié", text: "Le coefficient K = 1.34 appliqué sur le giratoire de Barbazan respecte les frais généraux (14%) et l'aléa chantier (3%)." }
            ]
        },

        'artisan_2k': {
            id: 'artisan_2k',
            name: 'Artisan TP Sud VRD (Perso 2k€ + Bureau + EPI)',
            type: 'Amorçage Artisanal 2 000 €',
            siret: '883 456 123 00019',
            capital: '2 000 €',
            siege: 'Frontignan / Sète (34)',
            caisse: 2000,
            bfr: 1800,
            ca_annuel: 125000,
            ca_prev: 140000,
            margin: 18.5,
            effectif_count: 2,
            fleet_count: 1,
            projects_count: 1,
            safety_status: '100% Équipé EPI',
            safety_sub: 'Casques, Gilets Cl.2, S3, DICT Validée',
            treasury_sub: '2 000 € Disponible • Amorçage Proximité',
            projects_sub: '1 Chantier Actif : Branchement Frontignan',
            effectif_sub: '2 Personnes : Artisan Gérant + 1 Apprenti',
            desc: 'Amorçage artisanal avec 2 000 € de capital, bureau compact loué, lot complet d\'EPI certifiés (Casques, gilets Cl.2, chaussures S3), outillage laser et réfection tranchée.',

            projects: [
                {
                    id: "art-01",
                    code: "ART-2026-01",
                    name: "Branchement Tout-à-l'Égout & Enrobé Allée (Frontignan)",
                    type: "internal",
                    ownership: "🔨 Chantier Artisan Proximité",
                    badge_type: "Chantier Artisan Proximité",
                    loc: "Frontignan Plage (34)",
                    location: "Frontignan Plage (34)",
                    client: "Particulier / Syndic Résidence Les Tamaris",
                    moe: "Artisan TP Sud VRD (Conception & Réalisation)",
                    budget: 18500,
                    spent: 11100,
                    budget_used: 11100,
                    progress: 60,
                    status: "En cours",
                    manager: "Julien Artisan",
                    site_chief: "Julien Artisan",
                    chef: "Julien Artisan (avec Lucas V. Apprenti)",
                    workers_count: 2,
                    delai_consomme_pct: 65,
                    start_date: "08/04/2026",
                    end_date: "24/04/2026",
                    end: "24/04/2026",
                    desc: "Création d'un raccordement assainissement individuel Ø160 PVC CR8 (32 ml), boîte de branchement 400x400 avec tampon fonte C250 et réfection enrobé à chaud 45 m².",
                    assigned_machinery: [{ name: "Fourgonnette Renault Trafic 145 DCI" }, { name: "Mini-Pelle 2.5t Yanmar (Kiloutou)" }],
                    assigned_tools: [{ name: "Laser Spectra LL300" }, { name: "Scie Stihl TS420" }, { name: "Pilonneuse Wacker" }],
                    docs: [{ name: "Devis_Signe_Frontignan", type: "pdf" }, { name: "Facture_Acompte_30", type: "pdf" }],
                    lots_breakdown: [
                        { name: "Lot 1 : Tranchée & Pose PVC CR8 Ø160 (32 ml)", budget: 8500, progress: 100, ds: 5100, pv: 8500 },
                        { name: "Lot 2 : Boîte de branchement & Raccordement EU", budget: 4200, progress: 80, ds: 2400, pv: 4200 },
                        { name: "Lot 3 : Remblai GNT 0/31.5 & Enrobé Noir (45 m²)", budget: 5800, progress: 20, ds: 3600, pv: 5800 }
                    ],
                    steps: [
                        { name: "Traçage DICT & Découpe enrobé", progress: 100 },
                        { name: "Tranchée mini-pelle 2.5t", progress: 100 },
                        { name: "Pose tube PVC Ø160 & lit de sable", progress: 100 },
                        { name: "Boîte siphoïde & essai d'écoulement", progress: 80 },
                        { name: "Compactage GNT & Enrobé à chaud", progress: 20 }
                    ]
                }
            ],

            fleet: [
                { id: "ENG-ART1", name: "Fourgonnette Renault Trafic 145 DCI Atelier", cat: "Utilitaire Aménagé", type: "Fourgonnette artisanale", brand: "Renault", loc: "Chantier Frontignan", status: "En Service", val: 24500, price: 24500, hourly_cost: 25, vgp: "08/11/2026", immat: "TR-145-TP", fuel: 85, hours: 820, weight: "3.0t", power: "107 kW", capacity: "8 m³", project: "Branchement Frontignan", icon: "🚐" },
                { id: "ENG-ART2", name: "Mini-Pelle 2.5t Yanmar SV26 (Location Kiloutou)", cat: "Engin Loué", type: "Mini-pelle urbaine", brand: "Yanmar", loc: "Chantier Frontignan", status: "Sur Chantier", val: 0, price: 0, hourly_cost: 45, vgp: "Contrat Kiloutou", immat: "LOC-KL-25", fuel: 75, hours: 320, weight: "2.6t", power: "18 kW", capacity: "0.08 m³", project: "Branchement Frontignan", icon: "🚜" }
            ],

            depot_inventory: [
                { id: "ART-LOC", name: "Local Artisanal & Bureau Compact (45 m²)", cat: "Immobilier", zone: "bureaux", loc: "Zone Artisanale Frontignan", status: "Loué (450 €/mois)", val: 0, vgp: "Bail 3/6/9", icon: "🏢" },
                { id: "ART-EPI", name: "Lot Complet EPI Certifiés (2 Casques JSP, 4 Gilets Cl.2, 2 Chaussures S3)", cat: "EPI", zone: "bureaux", loc: "Armoire Vestiaire", status: "100% Neuf Conforme", val: 680, vgp: "Conforme EN 397/20345", icon: "🦺" },
                { id: "ART-LZR", name: "Niveau Laser Rotatif Spectra Precision LL300", cat: "Topographie", zone: "atelier", loc: "Coffret Fourgonnette", status: "Opérationnel", val: 1200, vgp: "Calibré 2026", icon: "🔴" },
                { id: "ART-SCI", name: "Découpeuse Thermique Stihl TS420 (Disque 350mm)", cat: "Petit Outillage", zone: "atelier", loc: "Atelier Frontignan", status: "Révisée", val: 1100, vgp: "Conforme CE", icon: "🪚" },
                { id: "ART-PIL", name: "Pilonneuse Wacker Neuson BS50-2plus", cat: "Compactage", zone: "atelier", loc: "Atelier Frontignan", status: "Opérationnelle", val: 1800, vgp: "VGP valide", icon: "🔨" },
                { id: "ART-ENR", name: "Enrobé à Froid Noir en Seaux 25kg (2 Seaux)", cat: "Enrobé", zone: "casiers", loc: "Casier Stockage", status: "Stock : 50 kg", val: 50, vgp: "Prêt à l'emploi", icon: "🛢️" },
                { id: "ART-PEHD", name: "Couronne PEHD Eau Potable Ø32 PN16 (25 ml)", cat: "Canalisation", zone: "racks", loc: "Rack Mural", status: "Stock : 25 ml", val: 85, vgp: "Certifié ACS", icon: "🪵" }
            ],

            cashflow_transactions: [
                { date: "12/04/2026", type: "Acompte Client", label: "Acompte 30% Devis Signé - Résidence Les Tamaris Frontignan", amount: 5550, status: "Encaissé" },
                { date: "09/04/2026", type: "Fournisseur", label: "Achat Lot Complet EPI Professionnels Certifiés (Casques, S3, Gilets)", amount: -680, status: "Payé" },
                { date: "05/04/2026", type: "Loyer Local", label: "Loyer Mensuel Local Artisanal & Bureau 45m²", amount: -450, status: "Payé" },
                { date: "08/04/2026", type: "Location Engin", label: "Location Semaine Mini-Pelle 2.5t Yanmar - Kiloutou TP", amount: -980, status: "Payé" }
            ],

            documents: [
                { id: "DOC-ART-01", title: "Devis n°2026-014 Signé Bon Pour Accord - Branchement Frontignan", cat: "Commercial", chantier: "Frontignan Plage", date: "05/04/2026", format: "PDF (Signé)", size: "0.9 Mo" },
                { id: "DOC-ART-02", title: "Facture Acompte 30% FA-2026-008 (5 550 € TTC)", cat: "Comptabilité", chantier: "Frontignan Plage", date: "08/04/2026", format: "PDF", size: "0.6 Mo" },
                { id: "DOC-ART-03", title: "Attestation Assurance Décennale & Responsabilité Civile Pro (SMA BTP)", cat: "Assurance", chantier: "Siège Frontignan", date: "01/01/2026", format: "PDF", size: "1.4 Mo" },
                { id: "DOC-ART-04", title: "Récépissé DICT Télé-service Guichet Unique (Réseau Eau/Élec)", cat: "Réglementaire", chantier: "Frontignan Plage", date: "02/04/2026", format: "PDF", size: "1.1 Mo" },
                { id: "DOC-ART-05", title: "Livret d'Accueil & Consignes Sécurité Apprenti SST", cat: "Sécurité", chantier: "Atelier Frontignan", date: "15/03/2026", format: "PDF", size: "1.8 Mo" }
            ],

            map_locations: [
                { id: "siege_art", name: "Atelier & Bureau Artisanal (Frontignan)", category: "siege", lat: 43.4470, lng: 3.7550, color: "#38bdf8", icon: "🏢", ownership: "Siège & Atelier Artisanal", budget_ini: 2000, budget_used: 0, progress: 100, chef: "Julien Artisan", desc: "Local 45m², stock outillage laser, EPI et magasin." },
                { id: "ch_art", name: "Chantier Branchement Les Tamaris", category: "chantier", lat: 43.4350, lng: 3.7700, color: "#10b981", icon: "🏗️", ownership: "Chantier Actif Particulier", budget_ini: 18500, budget_used: 11100, progress: 60, chef: "Julien Artisan", desc: "Raccordement EU Ø160 et réfection enrobé 45m²." },
                { id: "fourn_pointp", name: "Point P Travaux Publics Sète", category: "fournisseur", lat: 43.4180, lng: 3.7050, color: "#ec4899", icon: "🏭", product: "Tuyaux PVC, Mortiers, Enrobé froid", distance: "5 km", desc: "Fournisseur négoce de proximité." },
                { id: "fourn_kilo", name: "Kiloutou TP Sète Littoral", category: "fournisseur", lat: 43.4250, lng: 3.7150, color: "#ec4899", icon: "🏭", product: "Location Mini-Pelle & Pilonneuse", distance: "4 km", desc: "Partenaire location matériel avec contrat pro." }
            ],

            hr_employees: [
                { id: "HR-ART", name: "Julien Artisan", role: "Artisan Gérant / Canalisateur Maçon VRD", cat: "Gérant", site: "Chantier Frontignan", phone: "06 77 88 99 00", email: "julien@sudvrd.fr", caces: "AIPR Concepteur & Opérateur • CACES R482 A", exp: "11 ans", icon: "👷‍♂️" },
                { id: "HR-APP", name: "Lucas Vidal", role: "Apprenti CAP Constructeur de Routes", cat: "Apprenti", site: "Chantier Frontignan", phone: "06 12 00 33 44", email: "lucas@sudvrd.fr", caces: "AIPR Opérateur • SST à jour", exp: "1ère année", icon: "👷‍♂️" }
            ],

            hr_hierarchy: {
                name: "Julien Artisan",
                role: "Artisan Gérant / Canalisateur & Maçon VRD",
                rank: "direction",
                tel: "06 77 88 99 00",
                aipr: "Concepteur & Opérateur",
                caces: "R482 Cat A (Mini-pelle)",
                badge: "Artisan Gérant",
                children: [
                    {
                        name: "Lucas Vidal",
                        role: "Apprenti CAP Constructeur de Routes / VRD",
                        rank: "compagnon",
                        tel: "06 12 00 33 44",
                        aipr: "Opérateur (1ère année)",
                        caces: "SST & Prévention BTP",
                        badge: "Apprenti Chantier"
                    }
                ]
            },

            ai_agents: [
                { id: "agent-artisan", name: "Agent IA Artisan & Micro-Chantier", avatar: "🔨", role: "Gestion Proximité", status: "Actif", text: "Chantier Frontignan en bonne voie (60%). Pensez à facturer le solde de 12 950 € dès la fin de l'application de l'enrobé." },
                { id: "agent-epi", name: "Agent IA Sécurité EPI & Outillage", avatar: "🦺", role: "Conformité", status: "100% Conforme", text: "Lot EPI certifié actif. Port du casque JSP et gilet classe 2 validé pour l'apprenti sur la voie publique." }
            ]
        }
    };

    function renderCockpitAiAgents() {
        const list = document.getElementById('cockpit-ai-agents-list');
        if (!list) return;
        const agents = (companyData.ai_agents && companyData.ai_agents.length) ? companyData.ai_agents : [
            { id: "agent-treso", name: "Agent IA Trésorerie & BFR", avatar: "💰", role: "Finances TP", status: "Optimal", text: "Trésorerie sous surveillance active." }
        ];
        list.innerHTML = agents.map(a => `
            <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(56,189,248,0.25); border-radius: 6px; padding: 0.6rem; display: flex; gap: 0.6rem; align-items: flex-start;">
                <div style="font-size: 1.4rem; line-height: 1;">${a.avatar}</div>
                <div style="flex: 1;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.2rem;">
                        <strong style="color: #f8fafc; font-size: 0.78rem;">${a.name}</strong>
                        <span class="badge ${a.status === 'Optimal' || a.status === 'Conforme' || a.status === '100% Conforme' || a.status === '100% Équipé EPI' ? 'badge-success' : 'badge-info'}" style="font-size: 0.65rem;">${a.status}</span>
                    </div>
                    <div style="color: #cbd5e1; font-size: 0.72rem; line-height: 1.35;">${a.text}</div>
                </div>
            </div>
        `).join('');
    }

    function renderCockpitProjectsSummary() {
        const list = document.getElementById('cockpit-projects-summary-list');
        if (!list) return;
        const projects = companyData.projects || [];
        if (projects.length === 0) {
            list.innerHTML = `
                <div style="background: rgba(15,23,42,0.7); border: 1px dashed rgba(51,65,85,0.8); border-radius: 6px; padding: 1rem; text-align: center; color: #94a3b8; font-size: 0.78rem;">
                    <span style="font-size: 1.3rem;">📁</span><br>
                    <strong>Aucun chantier engagé pour ce profil.</strong><br>
                    <span style="font-size: 0.7rem; color: #64748b;">Créez un premier marché ou lancez un devis dans le module Chantiers.</span>
                </div>
            `;
            return;
        }
        list.innerHTML = projects.map(p => `
            <div style="background: rgba(15,23,42,0.8); border: 1px solid var(--border); border-radius: 6px; padding: 0.6rem; display: flex; justify-content: space-between; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 180px;">
                    <div style="font-weight: 700; font-size: 0.78rem; color: #f8fafc; display: flex; align-items: center; gap: 0.4rem;">
                        <span>🏗️</span> ${p.name}
                    </div>
                    <div style="font-size: 0.7rem; color: #94a3b8; margin-top: 0.15rem;">${p.loc || p.location} • Chef : ${p.chef || p.site_chief || 'Non assigné'}</div>
                    <div style="margin-top: 0.35rem; width: 100%; background: #1e293b; height: 6px; border-radius: 3px; overflow: hidden;">
                        <div style="height: 100%; width: ${p.progress}%; background: linear-gradient(90deg, var(--cyan), var(--emerald)); border-radius: 3px;"></div>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.78rem; font-weight: 800; color: var(--emerald);">${p.budget.toLocaleString('fr-FR')} €</div>
                    <div style="font-size: 0.7rem; color: #38bdf8; font-weight: 700;">${p.progress}% achevé</div>
                </div>
            </div>
        `).join('');
    }

    function switchCompanyProfile(profileId) {
        const prof = companyProfilesData[profileId] || companyProfilesData['occitanie_tp'];
        currentCompanyProfile = profileId;
        caisseBalance = prof.caisse;

        // 1. Update companyData master object with profile data
        companyData.company = {
            name: prof.name,
            capital: prof.capital,
            siren: prof.siret,
            siege: prof.siege,
            tresorerie_actuelle: prof.caisse,
            bfr: prof.bfr,
            ca_annuel_prev: prof.ca_prev,
            marge_nette_moyenne: prof.margin
        };
        companyData.projects = (prof.projects || []).map(p => ({
            ...p,
            location: p.loc || p.location,
            budget_used: p.spent || p.budget_used,
            manager: p.manager || (p.chef ? p.chef.split('(')[0].trim() : 'Conducteur TP'),
            site_chief: p.chef || p.site_chief || 'Chef de Chantier',
            delai_consomme_pct: p.delai_consomme_pct || p.progress,
            end: p.end_date || p.end || '30/06/2026',
            assigned_machinery: p.assigned_machinery || [{ name: "Pelle TP", type: "Pelle" }],
            assigned_tools: p.assigned_tools || [{ name: "Laser de chantier", type: "Topo" }],
            docs: p.docs || [{ name: "CCTP", type: "pdf" }]
        }));
        companyData.fleet = (prof.fleet || []).map(v => ({
            ...v,
            brand: v.brand || v.name.split(' ')[0],
            price: v.val || v.price || 50000,
            hourly_cost: v.hourly_cost || 85,
            project: v.project || (v.status.includes('Chantier') ? v.loc : 'Disponible'),
            weight: v.weight || '12t',
            power: v.power || '120 kW',
            capacity: v.capacity || '1.2 m³'
        }));
        companyData.hr_employees = prof.hr_employees || [];
        companyData.hr_hierarchy = prof.hr_hierarchy || null;
        companyData.cashflow_transactions = prof.cashflow_transactions || [];
        companyData.documents = prof.documents || [];
        companyData.map_locations = prof.map_locations || [];
        companyData.ai_agents = prof.ai_agents || [];

        // 2. Update depot inventory
        if (typeof depotInventoryData !== 'undefined' && Array.isArray(depotInventoryData)) {
            depotInventoryData.length = 0;
            (prof.depot_inventory || []).forEach(item => depotInventoryData.push(item));
        }

        // 3. Update modal and quick button styling
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
            const qBtn = document.getElementById('btn-quick-' + id);
            if (qBtn) {
                if (id === profileId) {
                    qBtn.classList.add('active');
                    qBtn.style.border = '2px solid var(--cyan)';
                    qBtn.style.background = 'rgba(56,189,248,0.15)';
                } else {
                    qBtn.classList.remove('active');
                    qBtn.style.border = '1px solid rgba(51,65,85,0.8)';
                    qBtn.style.background = 'rgba(30,41,59,0.5)';
                }
            }
        });

        // 4. Update Top HUD
        const topName = document.getElementById('active-company-name-top');
        const topCaisse = document.getElementById('caisse-balance-top');
        if (topName) topName.textContent = prof.name + ' ▾';
        if (topCaisse) topCaisse.textContent = prof.caisse.toLocaleString('fr-FR') + ' €';

        // 5. Update Cockpit Hero Cards
        const kpiTreasury = document.getElementById('kpi-treasury-val');
        const kpiTreasurySub = document.getElementById('kpi-treasury-sub');
        const kpiProj = document.getElementById('kpi-active-projects-val');
        const kpiProjSub = document.getElementById('kpi-active-projects-sub');
        const kpiEff = document.getElementById('kpi-effectif-val');
        const kpiEffSub = document.getElementById('kpi-effectif-sub');
        const kpiSafe = document.getElementById('kpi-safety-val');
        const kpiSafeSub = document.getElementById('kpi-safety-sub');

        if (kpiTreasury) kpiTreasury.textContent = prof.caisse.toLocaleString('fr-FR') + ' €';
        if (kpiTreasurySub) kpiTreasurySub.textContent = prof.treasury_sub || '';
        if (kpiProj) kpiProj.textContent = (prof.projects || []).length + ' Actif' + ((prof.projects || []).length > 1 ? 's' : '');
        if (kpiProjSub) kpiProjSub.textContent = prof.projects_sub || '';
        if (kpiEff) kpiEff.textContent = prof.effectif_count + ' Salarié' + (prof.effectif_count > 1 ? 's' : '');
        if (kpiEffSub) kpiEffSub.textContent = prof.effectif_sub || '';
        if (kpiSafe) kpiSafe.textContent = prof.safety_status || '100% Validé';
        if (kpiSafeSub) kpiSafeSub.textContent = prof.safety_sub || '';

        // 6. Update Company Tab Info
        const compBadge = document.getElementById('company-profile-badge');
        const compTitle = document.getElementById('company-profile-title');
        const compSub = document.getElementById('company-profile-sub');
        const compCaisse = document.getElementById('company-caisse-val');
        const compCA = document.getElementById('company-ca-val');

        if (compBadge) compBadge.textContent = prof.type;
        if (compTitle) compTitle.textContent = prof.name;
        if (compSub) compSub.textContent = `SIRET : ${prof.siret} • Capital : ${prof.capital} • Siège : ${prof.siege}`;
        if (compCaisse) compCaisse.textContent = prof.caisse.toLocaleString('fr-FR') + ' €';
        if (compCA) compCA.textContent = prof.ca_annuel.toLocaleString('fr-FR') + ' €';

        logCockpit('🏢 Profil entreprise activé : ' + prof.name, 'ok');
        closeModal('company-switch-modal');

        // 7. Trigger complete re-rendering across all modules
        try {
            renderCockpitAiAgents();
            renderCockpitProjectsSummary();
            renderCockpitOsmMap();
            renderCompanyCashflowTable();
            renderProjectsHub();
            renderFleetGrid();
            renderFleetTable();
            renderFleetTelemetryView();
            if (typeof renderDocsTable === 'function') renderDocsTable();
            if (typeof renderDepotInventory === 'function') renderDepotInventory();
            if (typeof initDepotCanvas === 'function') initDepotCanvas();
            if (typeof initHrTree === 'function') initHrTree();
            if (typeof renderHrPartners === 'function') renderHrPartners();
            if (typeof renderPlanningAgenda === 'function' && typeof renderPlanningGantt === 'function') {
                if (planningViewMode.startsWith('agenda')) renderPlanningAgenda();
                else renderPlanningGantt();
            }
            if (typeof renderProcurementOrders === 'function') renderProcurementOrders();
            if (typeof renderSuppliersTable === 'function') renderSuppliersTable();
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
        const grid = document.getElementById('projects-grid') || document.getElementById('projects-hub-grid');
        if (!grid) return;

        const projects = companyData.projects || [];
        const filtered = projects.filter(p => {
            if (currentProjectFilter === 'internal') return !p.ownership.includes('DCE');
            if (currentProjectFilter === 'dce_ref') return p.ownership.includes('DCE');
            return true;
        });

        if (filtered.length === 0) {
            grid.innerHTML = `
                <div style="grid-column: 1 / -1; background: rgba(15,23,42,0.85); border: 2px dashed rgba(51,65,85,0.8); border-radius: 8px; padding: 2.5rem; text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📁</div>
                    <h3 style="color: #f8fafc; font-size: 1.2rem; font-weight: 800; margin-bottom: 0.5rem;">Aucun Marché ni Chantier Engagé</h3>
                    <p style="color: #94a3b8; font-size: 0.85rem; max-width: 500px; margin: 0 auto 1.2rem;">Votre entreprise est configurée en démarrage zéro. Répondez à votre premier appel d'offres ou importez un DCE d'apprentissage pour démarrer votre activité.</p>
                    <div style="display: flex; justify-content: center; gap: 0.5rem; flex-wrap: wrap;">
                        <button class="btn btn-primary" onclick="alert('Formulaire de création de devis déboursé sec ouvert.');">➕ Créer un Nouveau Devis</button>
                        <button class="btn btn-secondary" onclick="switchCompanyProfile('stagiaire_tp')">🎓 Charger les DCE d'apprentissage (Barbazan / Aurouer)</button>
                    </div>
                </div>
            `;
            return;
        }

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

    function openProjectDetailsModal(projectId) {
        openProjectModal(projectId);
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
