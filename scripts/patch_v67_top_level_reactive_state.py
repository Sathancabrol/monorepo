#!/usr/bin/env python3
"""
Patch v67: Global Reactive Account State & UI Controllers at Part 1 Header
"""

with open("scripts/section_js_part1.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace 0. GLOBAL EXPORT OF MASTER UI CONTROLLERS with the complete reactive suite
complete_global_suite = r"""
    // ==========================================
    // 0. GLOBAL REACTIVE ACCOUNT STATE & UI CONTROLLERS
    // ==========================================
    window.userAccountState = {
        userName: 'Jean DUPONT',
        userRole: 'direction',
        companyKey: 'occitanie_tp',
        companyName: 'Occitanie TP & VRD',
        treasury: 485200,
        headcount: 24,
        projectsCount: 4,
        fleetCount: 6,
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
            ticker.textContent = '📢 ' + s.companyName + ' • Direction : ' + s.userName + ' • Caisse Active : ' + new Intl.NumberFormat('fr-FR').format(s.treasury) + ' € • Effectif : ' + s.headcount + ' salariés • Chantiers : ' + s.projectsCount + ' actifs (Barbazan, Aurouer, Sète).';
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
            'occitanie_tp': { name: 'Occitanie TP & VRD', treasury: 485200, headcount: 24, projects: 4, fleet: 6 },
            'artisan_2k': { name: 'Artisan Sud VRD', treasury: 2400, headcount: 1, projects: 1, fleet: 1 },
            'stagiaire_tp': { name: 'Formation Conduite Travaux', treasury: 150000, headcount: 8, projects: 2, fleet: 3 },
            'compte_neuf': { name: 'Nouvelle Entreprise TP', treasury: 50000, headcount: 2, projects: 0, fleet: 1 }
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
            track.textContent = '📢 GÉNÉRAL : ' + s.companyName + ' • Marché Giratoire Barbazan notifié • Réception terrassement Aurouer validée • DICT AEP Sète conforme.';
        } else if (mode === 'finance') {
            track.textContent = '💰 FINANCE : Caisse active ' + formattedCaisse + ' € • Situation Chorus Pro n°4 encaissée (+42 500 €) • Déblocage retenue de garantie 5% • Marge moyenne 14.8%.';
        } else if (mode === 'security') {
            track.textContent = '🚨 SÉCURITÉ & QSE : Alerte météo vent 50 km/h bassin de Thau • Conformité blindage tranchées 100% • Score AIPR 100% • 0 accident sur 365j.';
        } else if (mode === 'logistics') {
            track.textContent = '🚛 LOGISTIQUE : ' + s.fleetCount + ' engins opérationnels (VGP 100%) • 8 rotations camions 8x4 enrobés BBSG 0/10 • Stock GNT 0/31.5 : 420 Tonnes.';
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
"""

# Replace in section_js_part1.py
pos_old_section = text.find('// ==========================================')
pos_raw_inventory = text.find('const rawInventoryData = __INVENTORY_JSON__;')

if pos_old_section != -1 and pos_raw_inventory != -1:
    text = text[:pos_old_section] + complete_global_suite + "\n    // ==========================================\n    // 1. DATASETS INJECTION & ROBUST NORMALIZATION\n    // ==========================================\n    " + text[pos_raw_inventory:]

with open("scripts/section_js_part1.py", "w", encoding="utf-8") as f:
    f.write(text)

print("scripts/section_js_part1.py updated with complete global reactive suite!")
