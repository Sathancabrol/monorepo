#!/usr/bin/env python3
"""
Patch v66: Export All Global Functions to Window at the Start of JS Execution
"""

with open("scripts/section_js_part1.py", "r", encoding="utf-8") as f:
    text = f.read()

global_init_code = r"""
    // ==========================================
    // 0. GLOBAL EXPORT OF MASTER UI CONTROLLERS
    // ==========================================
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
            if (window.setAccountTab) window.setAccountTab('login');
            if (window.loadAccountFormValues) window.loadAccountFormValues();
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

    window.switchNav = function(tabId, btn) {
        // Hide all tab panels
        document.querySelectorAll('.tab-panel').forEach(function(p) {
            p.classList.remove('active');
            p.style.display = 'none';
        });

        // Deactivate all navigation items & quick-hub buttons
        document.querySelectorAll('.nav-item, .drawer-nav-item, .nav-btn, .quick-hub-btn').forEach(function(b) {
            b.classList.remove('active');
        });

        // Show active tab panel
        var target = document.getElementById('tab-' + tabId);
        if (target) {
            target.classList.add('active');
            target.style.display = 'block';
        }

        // Highlight clicked button
        if (btn && btn.classList) {
            btn.classList.add('active');
        }
        var quickBtn = document.querySelector('.quick-hub-btn[onclick*=\"' + tabId + '\"]');
        if (quickBtn) quickBtn.classList.add('active');
        var drawerBtn = document.querySelector('.drawer-nav-item[onclick*=\"' + tabId + '\"]');
        if (drawerBtn) drawerBtn.classList.add('active');

        window.currentNav = tabId;

        // Trigger tab initializers safely
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

pos_script = text.find('<script>')
if pos_script != -1:
    text = text[:pos_script + 8] + global_init_code + text[pos_script + 8:]

with open("scripts/section_js_part1.py", "w", encoding="utf-8") as f:
    f.write(text)

print("scripts/section_js_part1.py successfully updated with global master controllers!")
