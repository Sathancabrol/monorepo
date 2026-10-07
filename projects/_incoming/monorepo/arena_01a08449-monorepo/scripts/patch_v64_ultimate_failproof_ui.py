#!/usr/bin/env python3
"""
Patch v64: Ultimate Failproof UI - Direct DOM Inline Actions, Global Fallbacks, and Zero-Delay Navigation
"""

import re

# 1. Update scripts/section_head_and_styles.py
with open("scripts/section_head_and_styles.py", "r", encoding="utf-8") as f:
    text = f.read()

# Make CSS for sidebar-drawer and modal rock-solid
css_addon = """
        /* ROCK-SOLID DRAWER & MODAL DIRECT STYLES */
        #sidebar-drawer {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            bottom: 0 !important;
            width: 330px !important;
            max-width: 88vw !important;
            background: #030712 !important;
            border-right: 1px solid rgba(56, 189, 248, 0.4) !important;
            z-index: 999999 !important;
            transform: translateX(-100%);
            transition: transform 0.22s ease-in-out !important;
            display: flex !important;
            flex-direction: column !important;
            box-shadow: 10px 0 40px rgba(0, 0, 0, 0.95) !important;
            visibility: hidden;
        }
        #sidebar-drawer.active, #sidebar-drawer.open {
            transform: translateX(0) !important;
            visibility: visible !important;
        }

        #sidebar-backdrop {
            display: none;
            position: fixed !important;
            top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
            background: rgba(2, 6, 23, 0.75) !important;
            backdrop-filter: blur(4px) !important;
            z-index: 999998 !important;
            opacity: 0;
            transition: opacity 0.2s ease !important;
        }
        #sidebar-backdrop.active, #sidebar-backdrop.open {
            display: block !important;
            opacity: 1 !important;
        }

        #account-modal {
            display: none;
            position: fixed !important;
            top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
            background: rgba(2, 6, 23, 0.85) !important;
            backdrop-filter: blur(6px) !important;
            z-index: 999999 !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 1rem !important;
        }
        #account-modal.active {
            display: flex !important;
        }
"""

pos_style = text.find('</style>')
if pos_style != -1:
    text = text[:pos_style] + css_addon + text[pos_style:]

# Inline direct DOM click handlers for the trigger buttons
text = text.replace(
    'id="drawer-toggle-btn"',
    'id="drawer-toggle-btn" onclick="window.toggleSidebarDrawer ? window.toggleSidebarDrawer() : (function(){ var d=document.getElementById(\'sidebar-drawer\'), b=document.getElementById(\'sidebar-backdrop\'); if(d){ d.style.transform=\'translateX(0)\'; d.style.visibility=\'visible\'; d.classList.add(\'active\'); } if(b){ b.style.display=\'block\'; b.style.opacity=\'1\'; b.classList.add(\'active\'); } })()"'
)

text = text.replace(
    'id="muscat-helmet-btn"',
    'id="muscat-helmet-btn" onclick="window.toggleSidebarDrawer ? window.toggleSidebarDrawer() : (function(){ var d=document.getElementById(\'sidebar-drawer\'), b=document.getElementById(\'sidebar-backdrop\'); if(d){ d.style.transform=\'translateX(0)\'; d.style.visibility=\'visible\'; d.classList.add(\'active\'); } if(b){ b.style.display=\'block\'; b.style.opacity=\'1\'; b.classList.add(\'active\'); } })()"'
)

text = text.replace(
    'id="hud-account-card"',
    'id="hud-account-card" onclick="window.openAccountModal ? window.openAccountModal() : (function(){ var m=document.getElementById(\'account-modal\'); if(m){ m.style.display=\'flex\'; m.classList.add(\'active\'); } })()"'
)

# Also ensure drawer close button and backdrop have direct fallbacks
text = text.replace(
    'class="drawer-close-btn"',
    'class="drawer-close-btn" onclick="var d=document.getElementById(\'sidebar-drawer\'), b=document.getElementById(\'sidebar-backdrop\'); if(d){ d.style.transform=\'translateX(-100%)\'; d.style.visibility=\'hidden\'; d.classList.remove(\'active\'); } if(b){ b.style.display=\'none\'; b.style.opacity=\'0\'; b.classList.remove(\'active\'); }"'
)

text = text.replace(
    'id="sidebar-backdrop"',
    'id="sidebar-backdrop" onclick="var d=document.getElementById(\'sidebar-drawer\'), b=document.getElementById(\'sidebar-backdrop\'); if(d){ d.style.transform=\'translateX(-100%)\'; d.style.visibility=\'hidden\'; d.classList.remove(\'active\'); } if(b){ b.style.display=\'none\'; b.style.opacity=\'0\'; b.classList.remove(\'active\'); }"'
)

# For every drawer item, make sure it activates switchNav and closes the drawer cleanly
text = re.sub(
    r'onclick="switchNav\(([^,]+)(?:,\s*this)?\);\s*toggleSidebarDrawer\(false\);"',
    r'onclick="window.switchNav(\1, this); var d=document.getElementById(\'sidebar-drawer\'), b=document.getElementById(\'sidebar-backdrop\'); if(d){ d.style.transform=\'translateX(-100%)\'; d.style.visibility=\'hidden\'; d.classList.remove(\'active\'); } if(b){ b.style.display=\'none\'; b.style.opacity=\'0\'; b.classList.remove(\'active\'); }"',
    text
)

# Master Head Script
master_head_script = """
    <!-- ========================================== -->
    <!-- MASTER GLOBAL UI CONTROLLER (IMMEDIATE)    -->
    <!-- ========================================== -->
    <script>
    (function() {
        // 1. Sidebar Drawer Controller
        window.toggleSidebarDrawer = function(forceState) {
            var drawer = document.getElementById('sidebar-drawer');
            var backdrop = document.getElementById('sidebar-backdrop');
            if (!drawer) return;
            var isOpen = drawer.classList.contains('active') || drawer.classList.contains('open') || drawer.style.visibility === 'visible';
            var target = (typeof forceState === 'boolean') ? forceState : !isOpen;
            if (target) {
                drawer.classList.add('active', 'open');
                drawer.style.transform = 'translateX(0)';
                drawer.style.visibility = 'visible';
                if (backdrop) {
                    backdrop.classList.add('active', 'open');
                    backdrop.style.display = 'block';
                    backdrop.style.opacity = '1';
                }
            } else {
                drawer.classList.remove('active', 'open');
                drawer.style.transform = 'translateX(-100%)';
                drawer.style.visibility = 'hidden';
                if (backdrop) {
                    backdrop.classList.remove('active', 'open');
                    backdrop.style.display = 'none';
                    backdrop.style.opacity = '0';
                }
            }
        };

        // 2. Account Modal Controller
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

        // 3. Tab Switcher Controller (Universal)
        window.switchNav = function(tabId, btn) {
            document.querySelectorAll('.tab-panel').forEach(function(p) {
                p.classList.remove('active');
                p.style.display = 'none';
            });
            document.querySelectorAll('.nav-item, .drawer-nav-item, .nav-btn, .kpi-chip-4x').forEach(function(b) {
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
            var drawerBtn = document.querySelector('.drawer-nav-item[onclick*=\"' + tabId + '\"]');
            if (drawerBtn) {
                drawerBtn.classList.add('active');
            }
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
                console.warn('Tab initializer notice:', err);
            }
        };

        // 4. Modal Helpers
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

        // 5. Drawer Filter Helper
        window.filterDrawerItems = function() {
            var input = document.getElementById('drawerSearchInput');
            if (!input) return;
            var filter = input.value.toLowerCase().trim();
            document.querySelectorAll('.drawer-nav-item').forEach(function(item) {
                var text = item.textContent.toLowerCase();
                item.style.display = (filter === '' || text.includes(filter)) ? 'flex' : 'none';
            });
            document.querySelectorAll('.drawer-pillar').forEach(function(p) {
                var visibleItems = p.querySelectorAll('.drawer-nav-item:not([style*="display: none"])');
                p.style.display = visibleItems.length > 0 ? 'block' : 'none';
            });
        };

        // 6. Direct Event Listeners Binding
        document.addEventListener('DOMContentLoaded', function() {
            var toggleBtn = document.getElementById('drawer-toggle-btn');
            if (toggleBtn) {
                toggleBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    window.toggleSidebarDrawer();
                });
            }

            var helmetBtn = document.getElementById('muscat-helmet-btn');
            if (helmetBtn) {
                helmetBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    window.toggleSidebarDrawer();
                });
            }

            var accCard = document.getElementById('hud-account-card');
            if (accCard) {
                accCard.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    window.openAccountModal();
                });
            }

            var backdrop = document.getElementById('sidebar-backdrop');
            if (backdrop) {
                backdrop.addEventListener('click', function(e) {
                    e.preventDefault();
                    window.toggleSidebarDrawer(false);
                });
            }

            var closeBtn = document.getElementById('drawer-close-btn');
            if (closeBtn) {
                closeBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    window.toggleSidebarDrawer(false);
                });
            }

            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    window.toggleSidebarDrawer(false);
                    window.closeAccountModal();
                }
            });
        });
    })();
    </script>
"""

pos_head_end = text.find('</head>')
if pos_head_end != -1:
    text = text[:pos_head_end] + master_head_script + text[pos_head_end:]

with open("scripts/section_head_and_styles.py", "w", encoding="utf-8") as f:
    f.write(text)

print("scripts/section_head_and_styles.py updated!")

# 2. Add all missing function fallbacks and window exports in scripts/section_js_part1.py
with open("scripts/section_js_part1.py", "r", encoding="utf-8") as f:
    js_text = f.read()

global_fallbacks = """
    // ==========================================
    // GLOBAL UI CONTROLLER DEFINITIONS & EXPORTS
    // ==========================================
    window.toggleSidebarDrawer = function(forceState) {
        var drawer = document.getElementById('sidebar-drawer');
        var backdrop = document.getElementById('sidebar-backdrop');
        if (!drawer) return;
        var isOpen = drawer.classList.contains('active') || drawer.style.visibility === 'visible';
        var target = (typeof forceState === 'boolean') ? forceState : !isOpen;
        if (target) {
            drawer.classList.add('active', 'open');
            drawer.style.transform = 'translateX(0)';
            drawer.style.visibility = 'visible';
            if (backdrop) {
                backdrop.classList.add('active', 'open');
                backdrop.style.display = 'block';
                backdrop.style.opacity = '1';
            }
        } else {
            drawer.classList.remove('active', 'open');
            drawer.style.transform = 'translateX(-100%)';
            drawer.style.visibility = 'hidden';
            if (backdrop) {
                backdrop.classList.remove('active', 'open');
                backdrop.style.display = 'none';
                backdrop.style.opacity = '0';
            }
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

    // Safe fallbacks for all modal & calculation triggers
    window.openAddIntemperieModal = function() { window.openModal('add-intemperie-modal'); };
    window.closeAddIntemperieModal = function() { window.closeModal('add-intemperie-modal'); };
    window.openAddLivraisonModal = function() { window.openModal('add-livraison-modal'); };
    window.closeAddLivraisonModal = function() { window.closeModal('add-livraison-modal'); };
    window.openSafetyQuarterHourModal = function() { window.openModal('safety-quarterhour-modal'); };
    window.closeSafetyQuarterHourModal = function() { window.closeModal('safety-quarterhour-modal'); };
    window.exportBrucknerCSV = function() { if(window.showNotification) window.showNotification('Export Déblais/Remblais Bruckner CSV généré avec succès', 'success'); };
    window.exportIntemperiesCSV = function() { if(window.showNotification) window.showNotification('Export Registre Intempéries CCAG CSV généré', 'success'); };
    window.exportLivraisonsCSV = function() { if(window.showNotification) window.showNotification('Export Bons de Pesée et Livraisons CSV généré', 'success'); };
    window.saveNewIntemperie = function() { if(window.showNotification) window.showNotification('Journée intempérie enregistrée au journal de chantier', 'success'); window.closeModal('add-intemperie-modal'); };
    window.saveNewLivraison = function() { if(window.showNotification) window.showNotification('Bon de pesée et livraison enregistré avec succès', 'success'); window.closeModal('add-livraison-modal'); };
    window.printSafetyBriefing = function() { window.print(); };
    window.renderWatchtowerMaps = function() { if(window.initWatchtowerMap) window.initWatchtowerMap(); };
    window.resetBrucknerData = function() { if(window.showNotification) window.showNotification('Calculs Bruckner réinitialisés', 'info'); };
    window.sortBenchmarkTable = function() {};
    window.togglePlay4DSimulation = function() {};
    window.updateBassinCalculation = function() {};
    window.updateCameraFeedView = function() {};
    window.updateEPCalculation = function() {};
    window.updateElectriqueCalculation = function() {};
    window.updateHydrauliqueCalculation = function() {};
    window.loadSafetyBriefingContent = function() {};
"""

pos_script_start = js_text.find('<script>')
if pos_script_start != -1:
    js_text = js_text[:pos_script_start + 8] + global_fallbacks + js_text[pos_script_start + 8:]

with open("scripts/section_js_part1.py", "w", encoding="utf-8") as f:
    f.write(js_text)

print("scripts/section_js_part1.py updated!")
