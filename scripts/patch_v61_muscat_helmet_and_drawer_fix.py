#!/usr/bin/env python3
"""
Patch v61: Muscat Helmet Logo, Single-Row Horizontal 4X HUD, and Bulletproof Flyout Drawer Engine
"""

import re

# 1. Update scripts/section_head_and_styles.py
with open("scripts/section_head_and_styles.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace CSS rules for hud-topbar-4x and sidebar-drawer
old_hud_css = """.hud-topbar-4x {
            background: linear-gradient(180deg, #020617 0%, #0b1120 100%);
            border-bottom: 1px solid rgba(56, 189, 248, 0.25);
            padding: 0.4rem 0.8rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7);
            gap: 0.75rem;
            flex-wrap: wrap;
        }"""

new_hud_css = """.hud-topbar-4x {
            background: #020617;
            border-bottom: 1px solid rgba(56, 189, 248, 0.25);
            padding: 0.35rem 0.65rem;
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap; /* Single horizontal line along window */
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 9000;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7);
            gap: 0.5rem;
            width: 100%;
            overflow-x: auto;
            overflow-y: hidden;
            scrollbar-width: thin;
            scrollbar-color: rgba(56, 189, 248, 0.2) transparent;
        }
        .hud-topbar-4x::-webkit-scrollbar { height: 3px; }
        .hud-topbar-4x::-webkit-scrollbar-thumb { background: rgba(56, 189, 248, 0.3); border-radius: 2px; }

        .muscat-helmet-btn {
            background: rgba(217, 119, 6, 0.15);
            border: 1px solid rgba(245, 158, 11, 0.4);
            border-radius: 6px;
            padding: 2px 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 0 10px rgba(245, 158, 11, 0.2);
            flex-shrink: 0;
        }
        .muscat-helmet-btn:hover {
            background: rgba(217, 119, 6, 0.3);
            border-color: #f59e0b;
            box-shadow: 0 0 15px rgba(245, 158, 11, 0.5);
            transform: scale(1.05);
        }"""

if old_hud_css in text:
    text = text.replace(old_hud_css, new_hud_css)
else:
    print("Warning: old_hud_css exact string not found, updating via regex")
    text = re.sub(
        r'\.hud-topbar-4x\s*\{[^}]*\}',
        new_hud_css,
        text
    )

# Replace .hud-4x-metrics to never wrap
old_metrics_css = """.hud-4x-metrics {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            flex-wrap: wrap;
            flex: 1;
            justify-content: center;
        }"""

new_metrics_css = """.hud-4x-metrics {
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap; /* Single line */
            align-items: center;
            gap: 0.4rem;
            flex: 1;
            justify-content: flex-start;
            overflow-x: auto;
            scrollbar-width: none;
            white-space: nowrap;
        }
        .hud-4x-metrics::-webkit-scrollbar { display: none; }
        .kpi-chip-4x {
            flex-shrink: 0;
            white-space: nowrap;
        }
        .hud-account-card {
            flex-shrink: 0;
            white-space: nowrap;
        }"""

if old_metrics_css in text:
    text = text.replace(old_metrics_css, new_metrics_css)
else:
    text = re.sub(
        r'\.hud-4x-metrics\s*\{[^}]*\}',
        new_metrics_css,
        text
    )

# Bulletproof Sidebar Drawer CSS
old_drawer_css_rule = """.sidebar-drawer {
            position: fixed;
            top: 0;
            left: 0;
            bottom: 0;
            width: 320px;
            max-width: 85vw;
            background: #040817;
            border-right: 1px solid rgba(56, 189, 248, 0.3);
            z-index: 1001;
            transform: translateX(-100%);
            transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            flex-direction: column;
            box-shadow: 10px 0 30px rgba(0, 0, 0, 0.8);
        }
        .sidebar-drawer.active {
            transform: translateX(0);
        }"""

new_drawer_css_rule = """.sidebar-drawer {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            bottom: 0 !important;
            width: 330px !important;
            max-width: 88vw !important;
            background: #030712 !important;
            border-right: 1px solid rgba(56, 189, 248, 0.35) !important;
            z-index: 99999 !important;
            transform: translateX(-100%) !important;
            transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
            display: flex !important;
            flex-direction: column !important;
            box-shadow: 10px 0 35px rgba(0, 0, 0, 0.9) !important;
            pointer-events: none;
        }
        .sidebar-drawer.active, .sidebar-drawer.open {
            transform: translateX(0) !important;
            pointer-events: auto !important;
        }
        .sidebar-backdrop {
            display: none;
            position: fixed !important;
            top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
            background: rgba(2, 6, 23, 0.75) !important;
            backdrop-filter: blur(4px) !important;
            z-index: 99998 !important;
            opacity: 0;
            transition: opacity 0.2s ease !important;
        }
        .sidebar-backdrop.active, .sidebar-backdrop.open {
            display: block !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }"""

if old_drawer_css_rule in text:
    text = text.replace(old_drawer_css_rule, new_drawer_css_rule)
else:
    text = re.sub(
        r'\.sidebar-drawer\s*\{[\s\S]*?\.sidebar-drawer\.active\s*\{[^}]*\}',
        new_drawer_css_rule,
        text
    )

# Now update the HTML markup of the top header:
# Replace brand title with Muscat Hard Hat Logo + 3 bars toggle button!
old_brand_html = """        <!-- LEFT: DRAWER TRIGGER & BRAND -->
        <div class="hud-brand-group">
            <button class="drawer-toggle-btn" id="drawer-toggle-btn" onclick="toggleSidebarDrawer()" title="Ouvrir le menu de navigation (Volant latéral)">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <div>
                <div class="hud-brand-title">⚡ BTP AUTONOMOUS COMMAND <span style="font-size:0.7rem; color:var(--cyan);">v5.8</span></div>
                <div class="hud-brand-subtitle">SYSTÈME STRATÉGIQUE & OPÉRATIONNEL VRD</div>
            </div>
        </div>"""

new_brand_html = """        <!-- LEFT: 3-BARS TOGGLE & MUSCAT HARD HAT LOGO (SANS TEXTE ENCOMBRANT) -->
        <div class="hud-brand-group">
            <button class="drawer-toggle-btn" id="drawer-toggle-btn" onclick="toggleSidebarDrawer()" title="Ouvrir le volant de navigation">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <div class="muscat-helmet-btn" onclick="toggleSidebarDrawer()" title="Menu Stratégique VRD & Terrassement">
                <!-- SVG CASQUE DE CHANTIER COULEUR MUSCAT (GOLDEN AMBER / FRONTIGNAN HUE) -->
                <svg viewBox="0 0 36 32" width="30" height="26">
                    <defs>
                        <linearGradient id="muscatGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#fbbf24"/>
                            <stop offset="50%" stop-color="#d97706"/>
                            <stop offset="100%" stop-color="#92400e"/>
                        </linearGradient>
                        <filter id="muscatGlow" x="-20%" y="-20%" width="140%" height="140%">
                            <feDropShadow dx="0" dy="1" stdDeviation="1.5" flood-color="#d97706" flood-opacity="0.7"/>
                        </filter>
                    </defs>
                    <!-- Helmet Dome -->
                    <path d="M 5 21 C 5 9 11 3 18 3 C 25 3 31 9 31 21 Z" fill="url(#muscatGrad)" filter="url(#muscatGlow)"/>
                    <!-- Central Reinforcing Rib -->
                    <path d="M 16 3 C 16 3 18 2 20 3 L 20 21 L 16 21 Z" fill="#fef08a" opacity="0.6"/>
                    <!-- Helmet Rim / Visor Base -->
                    <path d="M 2 21 C 2 19 34 19 34 21 C 34 24 2 24 2 21 Z" fill="#b45309" stroke="#fef08a" stroke-width="0.6"/>
                    <!-- Front Cap Lip -->
                    <path d="M 1 22 L 35 22 L 34 24 L 2 24 Z" fill="#78350f"/>
                </svg>
            </div>
        </div>"""

text = text.replace(old_brand_html, new_brand_html)

# Add immediate inline JavaScript right after the drawer to guarantee 100% instant reactivity
inline_drawer_script = """
    <!-- IMMEDIATE DRAWER CONTROLLER SCRIPT (100% RELIABLE EXECUTION) -->
    <script>
    window.toggleSidebarDrawer = function(forceState) {
        var drawer = document.getElementById('sidebar-drawer');
        var backdrop = document.getElementById('sidebar-backdrop');
        if (!drawer) return;
        var isOpen = drawer.classList.contains('active');
        var target = (typeof forceState === 'boolean') ? forceState : !isOpen;
        if (target) {
            drawer.classList.add('active');
            if (backdrop) backdrop.classList.add('active');
        } else {
            drawer.classList.remove('active');
            if (backdrop) backdrop.classList.remove('active');
        }
    };
    document.addEventListener('DOMContentLoaded', function() {
        var btn = document.getElementById('drawer-toggle-btn');
        if (btn) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                window.toggleSidebarDrawer();
            });
        }
        var backdrop = document.getElementById('sidebar-backdrop');
        if (backdrop) {
            backdrop.addEventListener('click', function() {
                window.toggleSidebarDrawer(false);
            });
        }
    });
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            window.toggleSidebarDrawer(false);
        }
    });
    </script>
"""

# Place inline_drawer_script right after </aside> in section_head_and_styles.py
pos_aside_close = text.find('</aside>')
if pos_aside_close != -1:
    text = text[:pos_aside_close + 8] + inline_drawer_script + text[pos_aside_close + 8:]
    print("Injected inline drawer script!")

with open("scripts/section_head_and_styles.py", "w", encoding="utf-8") as f:
    f.write(text)

print("scripts/section_head_and_styles.py updated successfully for Patch v61!")
