#!/usr/bin/env python3
"""
Patch v70: Perfect Clean Pro UI - High Legibility, Crisp Typography, Refined 4X HUD, and Sleek Flyout Drawer
"""

# ==============================================================================
# 1. UPDATE scripts/section_head_and_styles.py
# ==============================================================================
def update_head_and_styles():
    head_content = r'''# -*- coding: utf-8 -*-

def get_head_and_styles():
    return r"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BTP Autonomous Command Suite v6.0 — Direction & Conduite de Travaux</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
    <style>
        :root {
            /* HIGH-LEGIBILITY MODERN EXECUTIVE DARK PALETTE */
            --bg-base: #060913;
            --bg-surface: #0c1322;
            --bg-card: #111a2e;
            --bg-card-hover: #16223b;
            --bg-card-alt: #182642;
            --bg-input: #080d1a;
            
            --border: rgba(148, 163, 184, 0.18);
            --border-light: rgba(148, 163, 184, 0.28);
            --border-focus: #38bdf8;
            --border-accent: rgba(56, 189, 248, 0.4);

            --text-main: #f8fafc;
            --text-primary: #ffffff;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --text-dim: #64748b;

            --cyan: #38bdf8;
            --cyan-glow: rgba(56, 189, 248, 0.25);
            --emerald: #10b981;
            --amber: #f59e0b;
            --rose: #f43f5e;
            --purple: #a855f7;
            --blue: #3b82f6;
            --muscat: #d97706;

            --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            --font-mono: 'JetBrains Mono', Consolas, monospace;

            --radius-sm: 6px;
            --radius-md: 9px;
            --radius-lg: 13px;
            --radius-xl: 18px;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            background: var(--bg-base);
            color: var(--text-main);
            font-family: var(--font-sans);
            font-size: 15px;
            line-height: 1.55;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        ::-webkit-scrollbar { width: 7px; height: 7px; }
        ::-webkit-scrollbar-track { background: var(--bg-base); }
        ::-webkit-scrollbar-thumb { background: rgba(148, 163, 184, 0.3); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(148, 163, 184, 0.5); }

        /* BUTTONS */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            font-family: var(--font-sans);
            font-size: 0.88rem;
            font-weight: 700;
            padding: 0.55rem 1.1rem;
            border-radius: var(--radius-md);
            cursor: pointer;
            transition: all 0.18s ease;
            text-decoration: none;
            white-space: nowrap;
            line-height: 1.2;
            border: 1px solid transparent;
        }

        .btn-primary {
            background: linear-gradient(135deg, #0284c7 0%, #0ea5e9 100%);
            color: #ffffff;
            border-color: rgba(255,255,255,0.25);
            box-shadow: 0 2px 10px rgba(2, 132, 199, 0.35);
        }
        .btn-primary:hover {
            background: linear-gradient(135deg, #0369a1 0%, #0284c7 100%);
            box-shadow: 0 4px 16px rgba(2, 132, 199, 0.5);
            transform: translateY(-1px);
        }

        .btn-secondary {
            background: var(--bg-surface);
            color: var(--text-main);
            border-color: var(--border-light);
            font-weight: 700;
        }
        .btn-secondary:hover {
            background: var(--bg-card-hover);
            color: #ffffff;
            border-color: var(--cyan);
            transform: translateY(-1px);
        }
        .btn-secondary.active {
            background: #0284c7;
            color: #ffffff;
            border-color: var(--cyan);
            box-shadow: 0 2px 10px rgba(2, 132, 199, 0.4);
        }

        .btn-danger {
            background: linear-gradient(135deg, #e11d48 0%, #f43f5e 100%);
            color: #ffffff;
            border-color: rgba(255,255,255,0.2);
            box-shadow: 0 2px 8px rgba(225, 29, 72, 0.3);
        }

        /* CARDS */
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 1.35rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
            position: relative;
        }
        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.1rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.75rem;
        }
        .card-title {
            font-size: 1.05rem;
            font-weight: 800;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 0.55rem;
        }

        .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.15rem; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.15rem; }
        .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.15rem; }
        .grid-split-40-60 { display: grid; grid-template-columns: 4fr 6fr; gap: 1.15rem; }
        .grid-split-60-40 { display: grid; grid-template-columns: 6fr 4fr; gap: 1.15rem; }

        @media (max-width: 1150px) {
            .grid-2, .grid-3, .grid-4, .grid-split-40-60, .grid-split-60-40 {
                grid-template-columns: 1fr;
            }
        }

        /* ========================================== */
        /* 1. TOP 4X STRATEGY COMMAND HUD BAR        */
        /* ========================================== */
        .hud-topbar-4x {
            background: rgba(6, 9, 19, 0.95);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(148, 163, 184, 0.16);
            padding: 0.45rem 1rem;
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 9000;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.75);
            gap: 0.75rem;
            width: 100%;
            overflow-x: auto;
            overflow-y: hidden;
            scrollbar-width: thin;
        }
        .hud-topbar-4x::-webkit-scrollbar { height: 3px; }
        .hud-topbar-4x::-webkit-scrollbar-thumb { background: rgba(56, 189, 248, 0.35); }

        .drawer-toggle-btn {
            background: linear-gradient(135deg, rgba(217, 119, 6, 0.25) 0%, rgba(180, 83, 9, 0.35) 100%);
            border: 1px solid rgba(245, 158, 11, 0.6);
            color: #fef08a;
            padding: 0.45rem 0.95rem;
            border-radius: var(--radius-md);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.55rem;
            font-size: 0.9rem;
            font-weight: 800;
            transition: all 0.2s ease;
            box-shadow: 0 0 14px rgba(245, 158, 11, 0.25);
            flex-shrink: 0;
            user-select: none;
        }
        .drawer-toggle-btn:hover {
            background: linear-gradient(135deg, rgba(217, 119, 6, 0.45) 0%, rgba(180, 83, 9, 0.55) 100%);
            border-color: #fbbf24;
            color: #ffffff;
            box-shadow: 0 0 20px rgba(245, 158, 11, 0.5);
            transform: translateY(-1px);
        }

        .hud-4x-metrics {
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            align-items: center;
            gap: 0.55rem;
            flex: 1;
            justify-content: flex-start;
            overflow-x: auto;
            scrollbar-width: none;
            white-space: nowrap;
        }
        .hud-4x-metrics::-webkit-scrollbar { display: none; }

        .kpi-chip-4x {
            background: rgba(17, 26, 46, 0.9);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: var(--radius-md);
            padding: 0.35rem 0.8rem;
            display: flex;
            align-items: center;
            gap: 0.65rem;
            cursor: pointer;
            transition: all 0.18s ease;
            flex-shrink: 0;
            user-select: none;
        }
        .kpi-chip-4x:hover {
            border-color: var(--cyan);
            background: rgba(22, 34, 59, 0.95);
            box-shadow: 0 0 14px rgba(56, 189, 248, 0.25);
            transform: translateY(-1px);
        }
        .kpi-chip-4x span:first-child {
            font-size: 1.15rem;
            line-height: 1;
        }
        .kpi-chip-lbl {
            font-size: 0.72rem;
            font-weight: 800;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: block;
            line-height: 1.1;
        }
        .kpi-chip-val {
            font-size: 0.98rem;
            font-weight: 800;
            font-family: var(--font-mono);
            line-height: 1.15;
            color: #ffffff;
        }
        .kpi-chip-badge {
            font-size: 0.74rem;
            font-weight: 800;
            padding: 2px 7px;
            border-radius: var(--radius-sm);
            font-family: var(--font-mono);
        }
        .badge-success { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.45); }
        .badge-info { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.45); }
        .badge-warning { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.45); }

        .hud-account-card {
            background: linear-gradient(135deg, rgba(17, 26, 46, 0.95) 0%, rgba(22, 34, 59, 0.95) 100%);
            border: 1px solid rgba(56, 189, 248, 0.45);
            padding: 0.35rem 0.95rem;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            gap: 0.65rem;
            cursor: pointer;
            transition: all 0.2s ease;
            flex-shrink: 0;
            box-shadow: 0 0 14px rgba(56, 189, 248, 0.2);
            user-select: none;
        }
        .hud-account-card:hover {
            border-color: #38bdf8;
            background: rgba(2, 132, 199, 0.25);
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.45);
            transform: translateY(-1px);
        }

        /* ========================================== */
        /* 2. BREAKING NEWS TICKER BAR                */
        /* ========================================== */
        .news-ticker-bar {
            background: rgba(12, 19, 34, 0.95);
            border-bottom: 1px solid rgba(148, 163, 184, 0.14);
            display: flex;
            align-items: center;
            padding: 0.35rem 1rem;
            font-size: 0.88rem;
            gap: 0.85rem;
            overflow: hidden;
            position: sticky;
            top: 52px;
            z-index: 8990;
        }
        .ticker-mode-btns {
            display: flex;
            gap: 4px;
            background: var(--bg-input);
            padding: 3px;
            border-radius: var(--radius-sm);
            border: 1px solid var(--border);
            flex-shrink: 0;
        }
        .ticker-mode-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 0.74rem;
            font-weight: 800;
            padding: 0.25rem 0.65rem;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.15s ease;
            letter-spacing: 0.03em;
        }
        .ticker-mode-btn:hover {
            color: #ffffff;
            background: rgba(255,255,255,0.08);
        }
        .ticker-mode-btn.active {
            background: #0284c7;
            color: #ffffff;
            box-shadow: 0 0 10px rgba(2, 132, 199, 0.45);
        }
        .ticker-content-track {
            flex: 1;
            overflow: hidden;
            white-space: nowrap;
            position: relative;
        }
        .ticker-text {
            display: inline-block;
            color: #e2e8f0;
            font-weight: 600;
            font-size: 0.9rem;
            animation: tickerSlide 45s linear infinite;
        }
        .ticker-text:hover {
            animation-play-state: paused;
        }
        @keyframes tickerSlide {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }

        /* ========================================== */
        /* 3. LEFT FLYOUT DRAWER (SLIDING SIDEBAR)   */
        /* ========================================== */
        .sidebar-drawer {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            bottom: 0 !important;
            width: 360px !important;
            max-width: 90vw !important;
            background: #080d1a !important;
            border-right: 1px solid rgba(56, 189, 248, 0.35) !important;
            z-index: 999999 !important;
            transform: translateX(-100%);
            transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
            display: flex !important;
            flex-direction: column !important;
            box-shadow: 20px 0 50px rgba(0, 0, 0, 0.9) !important;
            visibility: hidden;
        }
        .sidebar-drawer.active, .sidebar-drawer.open {
            transform: translateX(0) !important;
            visibility: visible !important;
        }

        .sidebar-backdrop {
            display: none;
            position: fixed !important;
            top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
            background: rgba(3, 7, 18, 0.8) !important;
            backdrop-filter: blur(6px) !important;
            -webkit-backdrop-filter: blur(6px) !important;
            z-index: 999998 !important;
            opacity: 0;
            transition: opacity 0.2s ease !important;
        }
        .sidebar-backdrop.active, .sidebar-backdrop.open {
            display: block !important;
            opacity: 1 !important;
        }

        .drawer-header {
            padding: 1.1rem 1.35rem;
            background: #050812;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .drawer-title {
            font-size: 0.98rem;
            font-weight: 900;
            color: #38bdf8;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .drawer-close-btn {
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-main);
            width: 30px;
            height: 30px;
            border-radius: var(--radius-sm);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 1.1rem;
            font-weight: 800;
            transition: all 0.15s ease;
        }
        .drawer-close-btn:hover {
            color: #ffffff;
            background: #e11d48;
            border-color: #e11d48;
        }

        .drawer-search-box {
            padding: 0.85rem 1.1rem;
            border-bottom: 1px solid var(--border);
            background: rgba(12, 19, 34, 0.6);
        }
        .drawer-search-input {
            width: 100%;
            background: var(--bg-input);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-sm);
            padding: 0.55rem 0.85rem;
            font-size: 0.9rem;
            color: #ffffff;
            font-family: inherit;
            outline: none;
            transition: border-color 0.15s ease;
        }
        .drawer-search-input:focus {
            border-color: var(--cyan);
            box-shadow: 0 0 12px var(--cyan-glow);
        }

        .drawer-body {
            flex: 1;
            overflow-y: auto;
            padding: 1rem 0.85rem;
        }

        .drawer-pillar {
            margin-bottom: 1.2rem;
        }
        .drawer-pillar-title {
            font-size: 0.75rem;
            font-weight: 900;
            color: #38bdf8;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            padding: 0.4rem 0.6rem;
            display: flex;
            align-items: center;
            gap: 0.45rem;
            border-bottom: 1px solid rgba(56, 189, 248, 0.25);
            margin-bottom: 0.45rem;
        }

        .drawer-nav-item {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            width: 100%;
            padding: 0.65rem 0.85rem;
            background: transparent;
            border: 1px solid transparent;
            border-radius: var(--radius-md);
            color: var(--text-secondary);
            font-size: 0.92rem;
            font-weight: 700;
            cursor: pointer;
            text-align: left;
            transition: all 0.15s ease;
            margin-bottom: 3px;
        }
        .drawer-nav-item:hover {
            background: rgba(56, 189, 248, 0.12);
            border-color: rgba(56, 189, 248, 0.3);
            color: #ffffff;
            transform: translateX(3px);
        }
        .drawer-nav-item.active {
            background: linear-gradient(90deg, rgba(2, 132, 199, 0.35) 0%, rgba(6, 182, 212, 0.15) 100%);
            border-color: #38bdf8;
            color: #38bdf8;
            font-weight: 900;
            box-shadow: inset 4px 0 0 #38bdf8;
        }

        /* ========================================== */
        /* 4. MAIN APP CONTAINER & MODALS             */
        /* ========================================== */
        .app-main {
            flex: 1;
            padding: 1.25rem 1.5rem 5rem 1.5rem;
            max-width: 1780px;
            margin: 0 auto;
            width: 100%;
        }

        .tab-panel {
            display: none;
            padding-bottom: 5rem;
            animation: fadeIn 0.2s ease forwards;
        }
        .tab-panel.active { display: block; }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(4px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .modal-backdrop, .modal-overlay {
            display: none;
            position: fixed !important;
            top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
            background: rgba(3, 7, 18, 0.85) !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
            z-index: 999999 !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 1.5rem !important;
        }
        .modal-backdrop.active, #account-modal.active {
            display: flex !important;
        }

        .modal-box {
            background: var(--bg-card);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-xl);
            width: 100%;
            max-width: 860px;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.85);
            padding: 1.6rem;
            position: relative;
        }

        .input-group { margin-bottom: 0.9rem; }
        .input-label {
            display: block;
            font-size: 0.84rem;
            font-weight: 800;
            color: var(--text-secondary);
            margin-bottom: 0.35rem;
        }
        .input-field {
            width: 100%;
            background: var(--bg-input);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-sm);
            padding: 0.6rem 0.85rem;
            color: #ffffff;
            font-size: 0.9rem;
            outline: none;
            font-family: inherit;
            transition: border-color 0.15s ease;
        }
        .input-field:focus {
            border-color: var(--cyan);
            box-shadow: 0 0 10px var(--cyan-glow);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
            color: #f1f5f9;
        }
        thead tr {
            background: var(--bg-surface);
            color: var(--text-muted);
            font-weight: 800;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 2px solid var(--border);
        }
        tbody tr {
            border-bottom: 1px solid var(--border);
            transition: background 0.15s ease;
        }
        tbody tr:hover {
            background: rgba(56, 189, 248, 0.06);
        }
        td {
            padding: 9px 12px;
        }
    </style>
</head>
<body>

    <!-- ========================================== -->
    <!-- 1. TOP 4X STRATEGY COMMAND HUD BAR        -->
    <!-- ========================================== -->
    <header class="hud-topbar-4x">
        <!-- PROMINENT FLYOUT DRAWER BUTTON WITH MUSCAT HELMET -->
        <button class="drawer-toggle-btn" id="drawer-toggle-btn" onclick="window.toggleSidebarDrawer()" title="Ouvrir le menu de navigation (Volant latéral)">
            <span style="font-size:1.25rem;">🪖</span>
            <span>MENU (21 MODULES) ☰</span>
        </button>

        <!-- CENTER: 4X ENTERPRISE MACRO INDICATORS -->
        <div class="hud-4x-metrics">
            <!-- 1. Trésorerie -->
            <div class="kpi-chip-4x" id="hud-chip-tresorerie" onclick="window.switchNav('company', this)" title="Caisse active & BFR">
                <span>💶</span>
                <div>
                    <span class="kpi-chip-lbl">TRÉSORERIE</span>
                    <span class="kpi-chip-val" style="color:#34d399;" id="caisse-balance-top">1 450 000 €</span>
                </div>
                <span class="kpi-chip-badge badge-success" id="hud-tresorerie-badge">+14.2k€/m</span>
            </div>

            <!-- 2. Chantiers -->
            <div class="kpi-chip-4x" id="hud-chip-chantiers" onclick="window.switchNav('projects_hub', this)" title="Chantiers en cours d'exécution">
                <span>🏗️</span>
                <div>
                    <span class="kpi-chip-lbl">CHANTIERS</span>
                    <span class="kpi-chip-val" style="color:#38bdf8;" id="hud-chantiers-val">3 / 3 Actifs</span>
                </div>
                <span class="kpi-chip-badge badge-info" id="hud-chantiers-badge">18.5 M€ CA</span>
            </div>

            <!-- 3. Flotte Engins -->
            <div class="kpi-chip-4x" id="hud-chip-flotte" onclick="window.switchNav('materiel_depot', this)" title="Disponibilité parc matériel">
                <span>🚜</span>
                <div>
                    <span class="kpi-chip-lbl">FLOTTE TP</span>
                    <span class="kpi-chip-val" style="color:#fbbf24;" id="hud-flotte-val">14 / 14 Dispo</span>
                </div>
                <span class="kpi-chip-badge badge-warning" id="hud-flotte-badge">100% VGP</span>
            </div>

            <!-- 4. Effectif Salarié -->
            <div class="kpi-chip-4x" id="hud-chip-effectif" onclick="window.switchNav('rh_personnel', this)" title="Personnel de chantier">
                <span>👷</span>
                <div>
                    <span class="kpi-chip-lbl">EFFECTIF</span>
                    <span class="kpi-chip-val" style="color:#f8fafc;" id="hud-effectif-val">68 Salariés</span>
                </div>
                <span class="kpi-chip-badge badge-success" id="hud-effectif-badge">100% AIPR</span>
            </div>

            <!-- 5. Sécurité QSE -->
            <div class="kpi-chip-4x" id="hud-chip-securite" onclick="window.switchNav('safety_qse', this)" title="Score Sécurité & Prévention">
                <span>🛡️</span>
                <div>
                    <span class="kpi-chip-lbl">SÉCURITÉ</span>
                    <span class="kpi-chip-val" style="color:#34d399;" id="hud-qse-val">98.5% Conforme</span>
                </div>
                <span class="kpi-chip-badge badge-success" id="hud-qse-badge">0 Accid.</span>
            </div>

            <!-- 6. Météo Chantier -->
            <div class="kpi-chip-4x" id="hud-chip-meteo" onclick="window.switchNav('cockpit', this)" title="Conditions météorologiques chantiers">
                <span>⛅</span>
                <div>
                    <span class="kpi-chip-lbl">MÉTÉO LOCALE</span>
                    <span class="kpi-chip-val" style="color:#38bdf8;" id="hud-meteo-val">Sète • 22°C</span>
                </div>
                <span class="kpi-chip-badge badge-info" id="hud-meteo-badge">Vent 14 km/h</span>
            </div>
        </div>

        <!-- RIGHT: UNIFIED ACCOUNT & IDENTITY TRIGGER -->
        <div class="hud-account-card" id="hud-account-card" onclick="window.openAccountModal()" title="Gestionnaire de compte, identité et hiérarchie">
            <span style="font-size:1.15rem;">👤</span>
            <div>
                <span style="font-size:0.75rem; color:#94a3b8; display:block; line-height:1.1;" id="hud-user-identity">👑 Jean DUPONT (Direction)</span>
                <span style="font-size:0.88rem; font-weight:900; color:#38bdf8; line-height:1.1;" id="hud-company-name-display">Colas Agence Sète ▾</span>
            </div>
        </div>
    </header>

    <!-- ========================================== -->
    <!-- 2. BREAKING NEWS TICKER WITH MODES         -->
    <!-- ========================================== -->
    <div class="news-ticker-bar">
        <div class="ticker-mode-btns">
            <button class="ticker-mode-btn active" id="ticker-btn-general" onclick="window.setTickerMode('general')">📢 GÉNÉRAL</button>
            <button class="ticker-mode-btn" id="ticker-btn-finance" onclick="window.setTickerMode('finance')">💰 FINANCE</button>
            <button class="ticker-mode-btn" id="ticker-btn-security" onclick="window.setTickerMode('security')">🚨 SÉCURITÉ</button>
            <button class="ticker-mode-btn" id="ticker-btn-logistics" onclick="window.setTickerMode('logistics')">🚛 LOGISTIQUE</button>
        </div>
        <div class="ticker-content-track">
            <span class="ticker-text" id="live-ticker-text">
                📢 DIRECT EXÉCUTION : Colas Agence Sète • Marché Giratoire Barbazan notifié • Réception terrassement Lotissement Aurouer validée • Validation DICT AEP Sète • QSE 98.5%.
            </span>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- 3. LEFT FLYOUT DRAWER (SLIDING SIDEBAR)    -->
    <!-- ========================================== -->
    <div class="sidebar-backdrop" id="sidebar-backdrop" onclick="window.toggleSidebarDrawer(false)"></div>
    <aside class="sidebar-drawer" id="sidebar-drawer">
        <div class="drawer-header">
            <div class="drawer-title">🪖 Navigation Stratégique (21 Modules)</div>
            <button class="drawer-close-btn" onclick="window.toggleSidebarDrawer(false)">&times;</button>
        </div>

        <div class="drawer-search-box">
            <input type="text" class="drawer-search-input" id="drawerSearchInput" placeholder="🔍 Rechercher un module, calcul, formule..." oninput="window.filterDrawerItems()">
        </div>

        <div class="drawer-body">
            <!-- PÔLE I -->
            <div class="drawer-pillar">
                <div class="drawer-pillar-title">🏛️ Pôle I : Direction & Stratégie</div>
                <button class="drawer-nav-item active" onclick="window.switchNav('cockpit', this); window.toggleSidebarDrawer(false);">🌐 Cockpit SIG & IA Agents</button>
                <button class="drawer-nav-item" onclick="window.switchNav('company', this); window.toggleSidebarDrawer(false);">💶 Entreprise, Caisse & Trésorerie</button>
                <button class="drawer-nav-item" onclick="window.switchNav('benchmarking', this); window.toggleSidebarDrawer(false);">📊 Benchmark & Comparateur Prix</button>
                <button class="drawer-nav-item" onclick="window.switchNav('legal_vault', this); window.toggleSidebarDrawer(false);">🔒 Coffre Légal & Marchés Publics</button>
                <button class="drawer-nav-item" onclick="window.switchNav('audit_blockchain', this); window.toggleSidebarDrawer(false);">⛓️ Registre d'Audit Blockchain</button>
            </div>

            <!-- PÔLE II -->
            <div class="drawer-pillar">
                <div class="drawer-pillar-title">🏗️ Pôle II : Chantiers & Exécution</div>
                <button class="drawer-nav-item" onclick="window.switchNav('projects_hub', this); window.toggleSidebarDrawer(false);">🏗️ Hub Chantiers & Avancement</button>
                <button class="drawer-nav-item" onclick="window.switchNav('planning_gantt', this); window.toggleSidebarDrawer(false);">📅 Planning Gantt 4D & Intempéries</button>
                <button class="drawer-nav-item" onclick="window.switchNav('pointage_terrain', this); window.toggleSidebarDrawer(false);">📱 Mode Terrain Compagnon</button>
                <button class="drawer-nav-item" onclick="window.switchNav('rdc_pesee', this); window.toggleSidebarDrawer(false);">📝 Journal RDC & Pesées Enrobés</button>
            </div>

            <!-- PÔLE III -->
            <div class="drawer-pillar">
                <div class="drawer-pillar-title">📐 Pôle III : Ingénierie & Études de Prix</div>
                <button class="drawer-nav-item" onclick="window.switchNav('devis_express', this); window.toggleSidebarDrawer(false);">📐 28 SDP / DQE / Devis Express</button>
                <button class="drawer-nav-item" onclick="window.switchNav('technique_analyse', this); window.toggleSidebarDrawer(false);">🧪 Formules, Talus 3D & 2D Enrobés</button>
                <button class="drawer-nav-item" onclick="window.switchNav('watchtower', this); window.toggleSidebarDrawer(false);">🛰️ Watch Tower SIG & Cartes HD</button>
            </div>

            <!-- PÔLE IV -->
            <div class="drawer-pillar">
                <div class="drawer-pillar-title">🦺 Pôle IV : Sécurité, Moyens & RH</div>
                <button class="drawer-nav-item" onclick="window.switchNav('safety_qse', this); window.toggleSidebarDrawer(false);">🦺 Sécurité AIPR & 1/4h QSE</button>
                <button class="drawer-nav-item" onclick="window.switchNav('materiel_depot', this); window.toggleSidebarDrawer(false);">🚜 Flotte Engins & Dépôt Stocks</button>
                <button class="drawer-nav-item" onclick="window.switchNav('fournisseurs', this); window.toggleSidebarDrawer(false);">🏢 Fournisseurs & Centrales TP</button>
                <button class="drawer-nav-item" onclick="window.switchNav('rh_personnel', this); window.toggleSidebarDrawer(false);">👥 Équipe Salariés & Compétences</button>
                <button class="drawer-nav-item" onclick="window.switchNav('ccag_travaux', this); window.toggleSidebarDrawer(false);">⚖️ Normes CCTG & Guide CCAG</button>
                <button class="drawer-nav-item" onclick="window.switchNav('obsidian_wiki', this); window.toggleSidebarDrawer(false);">🧠 Base de Connaissances Obsidian</button>
            </div>
        </div>

        <div style="padding:0.85rem 1.1rem; background:#050812; border-top:1px solid var(--border); display:flex; justify-content:space-between; align-items:center;">
            <button class="btn btn-primary" style="width:100%;" onclick="window.openAccountModal(); window.toggleSidebarDrawer(false);">👤 Gérer Entreprise / Compte</button>
        </div>
    </aside>

    <!-- MAIN APP CONTAINER -->
    <main class="app-main">
"""
'''
    with open("scripts/section_head_and_styles.py", "w", encoding="utf-8") as f:
        f.write(head_content)
    print("scripts/section_head_and_styles.py updated!")

if __name__ == '__main__':
    update_head_and_styles()
