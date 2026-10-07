#!/usr/bin/env python3
"""
Patch v62: Bulletproof Topbar, Muscat Helmet, Flyout Drawer, and Account Modal Controllers
"""

import re

# 1. Update scripts/section_head_and_styles.py
with open("scripts/section_head_and_styles.py", "r", encoding="utf-8") as f:
    text = f.read()

# Ensure high z-index and clean styles for drawer, backdrop and modals in CSS
bulletproof_css = """
        /* ========================================== */
        /* BULLETPROOF DRAWER, BACKDROP & MODAL CSS   */
        /* ========================================== */
        .sidebar-drawer {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            bottom: 0 !important;
            width: 330px !important;
            max-width: 88vw !important;
            background: #030712 !important;
            border-right: 1px solid rgba(56, 189, 248, 0.4) !important;
            z-index: 999999 !important;
            transform: translateX(-100%) !important;
            transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
            display: flex !important;
            flex-direction: column !important;
            box-shadow: 10px 0 40px rgba(0, 0, 0, 0.95) !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }
        .sidebar-drawer.active, .sidebar-drawer.open {
            transform: translateX(0) !important;
            visibility: visible !important;
            pointer-events: auto !important;
        }

        .sidebar-backdrop {
            display: none !important;
            position: fixed !important;
            top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
            background: rgba(2, 6, 23, 0.8) !important;
            backdrop-filter: blur(5px) !important;
            z-index: 999998 !important;
            opacity: 0 !important;
            transition: opacity 0.2s ease !important;
            pointer-events: none !important;
        }
        .sidebar-backdrop.active, .sidebar-backdrop.open {
            display: block !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }

        .modal-backdrop, .modal-overlay {
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

        .drawer-toggle-btn, .muscat-helmet-btn, .hud-account-card, .kpi-chip-4x {
            cursor: pointer !important;
            user-select: none !important;
        }
"""

# Replace in section_head_and_styles.py
pos_style_end = text.find('</style>')
if pos_style_end != -1:
    text = text[:pos_style_end] + bulletproof_css + text[pos_style_end:]

# Update the HTML topbar to add explicit IDs on trigger buttons
old_toggle_btn = '<button class="drawer-toggle-btn" id="drawer-toggle-btn" onclick="toggleSidebarDrawer()"'
new_toggle_btn = '<button class="drawer-toggle-btn" id="drawer-toggle-btn" onclick="window.toggleSidebarDrawer()"'
text = text.replace(old_toggle_btn, new_toggle_btn)

old_helmet_btn = '<div class="muscat-helmet-btn" onclick="toggleSidebarDrawer()"'
new_helmet_btn = '<div class="muscat-helmet-btn" id="muscat-helmet-btn" onclick="window.toggleSidebarDrawer()"'
text = text.replace(old_helmet_btn, new_helmet_btn)

old_acc_btn = '<div class="hud-account-card" onclick="openAccountModal()"'
new_acc_btn = '<div class="hud-account-card" id="hud-account-card" onclick="window.openAccountModal()"'
text = text.replace(old_acc_btn, new_acc_btn)

# Bulletproof global head controller script
global_head_controller = """
    <!-- ========================================== -->
    <!-- BULLETPROOF IMMEDIATE GLOBAL CONTROLLERS   -->
    <!-- ========================================== -->
    <script>
    (function() {
        // 1. Sidebar Drawer Controller
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

        // 2. Account Modal Controller
        window.openAccountModal = function() {
            var modal = document.getElementById('account-modal') || document.getElementById('company-switch-modal');
            if (modal) {
                modal.style.display = 'flex';
                if (window.setAccountTab) window.setAccountTab('login');
                if (window.loadAccountFormValues) window.loadAccountFormValues();
            }
        };
        window.closeAccountModal = function() {
            var modal = document.getElementById('account-modal') || document.getElementById('company-switch-modal');
            if (modal) modal.style.display = 'none';
        };
        window.openCompanySwitchModal = window.openAccountModal;

        // 3. Account Tab Switcher
        window.setAccountTab = function(tabKey) {
            document.querySelectorAll('.account-tab-btn').forEach(function(b) { b.classList.remove('active'); });
            var btn = document.getElementById('btn-acc-' + tabKey);
            if (btn) btn.classList.add('active');

            document.querySelectorAll('.acc-tab-content').forEach(function(c) { c.style.display = 'none'; });
            var tab = document.getElementById('acc-tab-' + tabKey);
            if (tab) tab.style.display = 'block';
        };

        // 4. Attach event listeners on DOM ready
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

            // Keyboard shortcut (Escape to close drawer & modals)
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

# Place global_head_controller in section_head_and_styles.py right before </head>
pos_head_end = text.find('</head>')
if pos_head_end != -1:
    text = text[:pos_head_end] + global_head_controller + text[pos_head_end:]

with open("scripts/section_head_and_styles.py", "w", encoding="utf-8") as f:
    f.write(text)

print("scripts/section_head_and_styles.py successfully updated with bulletproof controllers!")
