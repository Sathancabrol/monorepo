#!/usr/bin/env python3
"""
Patch v65: Comprehensive UI/UX Overhaul
- High-legibility typography (16px base, 14px-18px badges, high-contrast crisp text)
- Prominent Left Flyout Drawer with Muscat Helmet Button [ 🪖 MENU STRATÉGIQUE (21 MODULES) ☰ ]
- Synchronized Top 4X HUD & Breaking News Ticker in single horizontal line
- Quick-Hub 1-Click Sub-Dock
- Full Interactive Company & Account Creation Wizard, Role Selector, and Headcount Slider
"""

import re

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
    <title>BTP Autonomous Command Suite v5.9 — Direction & Conduite de Travaux</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
    <style>
        :root {
            --bg-base: #020617;
            --bg-surface: #0b1120;
            --bg-card: #0f172a;
            --bg-card-alt: #1e293b;
            --bg-card-hover: #1e293b;
            --bg: #090d16;
            --border: #334155;
            --border-light: #475569;
            --border-accent: rgba(56, 189, 248, 0.4);
            --border-emerald: rgba(34, 197, 94, 0.4);
            --border-amber: rgba(245, 158, 11, 0.4);
            --border-rose: rgba(239, 68, 68, 0.4);

            --text-main: #f8fafc;
            --text-primary: #ffffff;
            --text-secondary: #e2e8f0;
            --text-muted: #94a3b8;
            --text-dim: #64748b;

            --cyan: #38bdf8;
            --cyan-glow: rgba(56, 189, 248, 0.25);
            --emerald: #22c55e;
            --amber: #f59e0b;
            --rose: #ef4444;
            --purple: #a855f7;
            --blue: #3b82f6;

            --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            --font-mono: 'JetBrains Mono', Consolas, monospace;

            --radius-sm: 5px;
            --radius-md: 8px;
            --radius-lg: 12px;
            --radius-xl: 16px;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            background: var(--bg-base);
            color: var(--text-main);
            font-family: var(--font-sans);
            font-size: 15px; /* High legibility */
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #020617; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #475569; }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            font-family: var(--font-sans);
            font-size: 0.88rem;
            font-weight: 700;
            padding: 0.5rem 1rem;
            border-radius: var(--radius-md);
            cursor: pointer;
            transition: all 0.18s ease;
            text-decoration: none;
            white-space: nowrap;
        }

        .btn-primary {
            background: linear-gradient(135deg, #0284c7 0%, #06b6d4 100%);
            color: #ffffff;
            border: 1px solid rgba(255,255,255,0.25);
            box-shadow: 0 2px 10px rgba(6, 182, 212, 0.3);
        }
        .btn-primary:hover {
            background: linear-gradient(135deg, #0369a1 0%, #0891b2 100%);
            box-shadow: 0 4px 16px rgba(6, 182, 212, 0.5);
            transform: translateY(-1px);
        }

        .btn-secondary {
            background: #1e293b;
            color: #f8fafc;
            border: 1px solid #475569;
            font-weight: 700;
        }
        .btn-secondary:hover {
            background: #334155;
            color: #38bdf8;
            border-color: #38bdf8;
        }
        .btn-secondary.active {
            background: #0284c7;
            color: #ffffff;
            border-color: #38bdf8;
            box-shadow: 0 2px 8px rgba(2, 132, 199, 0.4);
        }

        .btn-danger {
            background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
            color: #ffffff;
            border: 1px solid rgba(255,255,255,0.2);
        }

        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 1.25rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            position: relative;
        }
        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
            border-bottom: 1px solid rgba(51,65,85,0.6);
            padding-bottom: 0.65rem;
        }
        .card-title {
            font-size: 1.05rem;
            font-weight: 800;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* ========================================== */
        /* 1. TOP 4X STRATEGY COMMAND HUD (SINGLE LINE) */
        /* ========================================== */
        .hud-topbar-4x {
            background: #020617;
            border-bottom: 1px solid rgba(56, 189, 248, 0.35);
            padding: 0.45rem 0.85rem;
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap; /* Single line */
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 9000;
            box-shadow: 0 4px 25px rgba(0, 0, 0, 0.85);
            gap: 0.65rem;
            width: 100%;
            overflow-x: auto;
            overflow-y: hidden;
            scrollbar-width: thin;
        }
        .hud-topbar-4x::-webkit-scrollbar { height: 4px; }
        .hud-topbar-4x::-webkit-scrollbar-thumb { background: rgba(56, 189, 248, 0.4); border-radius: 2px; }

        .drawer-toggle-btn {
            background: linear-gradient(135deg, rgba(217, 119, 6, 0.25) 0%, rgba(180, 83, 9, 0.35) 100%);
            border: 1px solid #f59e0b;
            color: #fef08a;
            padding: 0.45rem 0.85rem;
            border-radius: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
            font-weight: 800;
            transition: all 0.2s ease;
            box-shadow: 0 0 12px rgba(245, 158, 11, 0.3);
            flex-shrink: 0;
            user-select: none;
        }
        .drawer-toggle-btn:hover {
            background: linear-gradient(135deg, rgba(217, 119, 6, 0.45) 0%, rgba(180, 83, 9, 0.55) 100%);
            box-shadow: 0 0 20px rgba(245, 158, 11, 0.6);
            transform: scale(1.03);
            border-color: #fbbf24;
            color: #ffffff;
        }

        .hud-4x-metrics {
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            align-items: center;
            gap: 0.5rem;
            flex: 1;
            justify-content: flex-start;
            overflow-x: auto;
            scrollbar-width: none;
            white-space: nowrap;
        }
        .hud-4x-metrics::-webkit-scrollbar { display: none; }

        .kpi-chip-4x {
            background: rgba(15, 23, 42, 0.95);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 8px;
            padding: 0.35rem 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.6rem;
            cursor: pointer;
            transition: all 0.18s ease;
            flex-shrink: 0;
            user-select: none;
        }
        .kpi-chip-4x:hover {
            border-color: #38bdf8;
            background: rgba(30, 41, 59, 0.95);
            box-shadow: 0 0 14px rgba(56, 189, 248, 0.3);
            transform: translateY(-1px);
        }
        .kpi-chip-4x span:first-child {
            font-size: 1.15rem;
        }
        .kpi-chip-lbl {
            font-size: 0.72rem;
            font-weight: 800;
            color: #cbd5e1;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            display: block;
            line-height: 1.1;
        }
        .kpi-chip-val {
            font-size: 0.95rem;
            font-weight: 900;
            font-family: var(--font-mono);
            line-height: 1.1;
        }
        .kpi-chip-badge {
            font-size: 0.72rem;
            font-weight: 800;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: var(--font-mono);
        }
        .badge-success { background: rgba(34, 197, 94, 0.25); color: #4ade80; border: 1px solid #22c55e; }
        .badge-info { background: rgba(56, 189, 248, 0.25); color: #38bdf8; border: 1px solid #0284c7; }
        .badge-warning { background: rgba(245, 158, 11, 0.25); color: #fbbf24; border: 1px solid #d97706; }

        .hud-account-card {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 100%);
            border: 1px solid #38bdf8;
            padding: 0.35rem 0.85rem;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 0.6rem;
            cursor: pointer;
            transition: all 0.2s ease;
            flex-shrink: 0;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.2);
            user-select: none;
        }
        .hud-account-card:hover {
            background: rgba(2, 132, 199, 0.25);
            box-shadow: 0 0 18px rgba(56, 189, 248, 0.45);
            transform: scale(1.02);
        }

        /* ========================================== */
        /* 2. BREAKING NEWS TICKER BAR & MODES        */
        /* ========================================== */
        .news-ticker-bar {
            background: #020617;
            border-bottom: 1px solid rgba(51, 65, 85, 0.8);
            display: flex;
            align-items: center;
            padding: 0.35rem 0.85rem;
            font-size: 0.85rem;
            gap: 0.75rem;
            overflow: hidden;
            position: sticky;
            top: 50px;
            z-index: 8990;
        }
        .ticker-mode-btns {
            display: flex;
            gap: 4px;
            background: #0b1120;
            padding: 3px;
            border-radius: 6px;
            border: 1px solid var(--border);
            flex-shrink: 0;
        }
        .ticker-mode-btn {
            background: transparent;
            border: none;
            color: #cbd5e1;
            font-size: 0.75rem;
            font-weight: 800;
            padding: 0.25rem 0.6rem;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .ticker-mode-btn:hover {
            color: #ffffff;
            background: rgba(255,255,255,0.1);
        }
        .ticker-mode-btn.active {
            background: #0284c7;
            color: #ffffff;
            box-shadow: 0 0 8px rgba(2, 132, 199, 0.5);
        }
        .ticker-content-track {
            flex: 1;
            overflow: hidden;
            white-space: nowrap;
            position: relative;
        }
        .ticker-text {
            display: inline-block;
            color: #f1f5f9;
            font-weight: 700;
            font-size: 0.88rem;
            animation: tickerSlide 40s linear infinite;
        }
        .ticker-text:hover {
            animation-play-state: paused;
        }
        @keyframes tickerSlide {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }

        /* ========================================== */
        /* 3. QUICK-HUB DOCK (1-CLICK ACCESS SUB-BAR) */
        /* ========================================== */
        .quick-hub-bar {
            background: #040817;
            border-bottom: 1px solid rgba(56, 189, 248, 0.2);
            padding: 0.35rem 0.85rem;
            display: flex;
            align-items: center;
            gap: 0.45rem;
            overflow-x: auto;
            white-space: nowrap;
            scrollbar-width: none;
            position: sticky;
            top: 86px;
            z-index: 8980;
        }
        .quick-hub-bar::-webkit-scrollbar { display: none; }
        .quick-hub-btn {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(51, 65, 85, 0.8);
            color: #e2e8f0;
            font-size: 0.8rem;
            font-weight: 700;
            padding: 0.3rem 0.65rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.15s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
        }
        .quick-hub-btn:hover {
            background: #1e293b;
            color: #38bdf8;
            border-color: #38bdf8;
            transform: translateY(-1px);
        }
        .quick-hub-btn.active {
            background: #0284c7;
            color: #ffffff;
            border-color: #38bdf8;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
        }

        /* ========================================== */
        /* 4. LEFT FLYOUT DRAWER (SLIDING SIDEBAR)   */
        /* ========================================== */
        .sidebar-drawer {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            bottom: 0 !important;
            width: 360px !important;
            max-width: 90vw !important;
            background: #030712 !important;
            border-right: 2px solid rgba(56, 189, 248, 0.4) !important;
            z-index: 999999 !important;
            transform: translateX(-100%);
            transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
            display: flex !important;
            flex-direction: column !important;
            box-shadow: 15px 0 50px rgba(0, 0, 0, 0.95) !important;
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
            background: rgba(2, 6, 23, 0.8) !important;
            backdrop-filter: blur(5px) !important;
            z-index: 999998 !important;
            opacity: 0;
            transition: opacity 0.2s ease !important;
        }
        .sidebar-backdrop.active, .sidebar-backdrop.open {
            display: block !important;
            opacity: 1 !important;
        }

        .drawer-header {
            padding: 1rem 1.25rem;
            background: #020617;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .drawer-title {
            font-size: 1rem;
            font-weight: 900;
            color: #38bdf8;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .drawer-close-btn {
            background: #1e293b;
            border: 1px solid var(--border);
            color: #f8fafc;
            width: 32px;
            height: 32px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 1.1rem;
            font-weight: 800;
        }
        .drawer-close-btn:hover {
            color: #ffffff;
            background: #ef4444;
            border-color: #ef4444;
        }

        .drawer-search-box {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid rgba(51, 65, 85, 0.6);
            background: rgba(15, 23, 42, 0.6);
        }
        .drawer-search-input {
            width: 100%;
            background: #020617;
            border: 1px solid var(--border-light);
            border-radius: 6px;
            padding: 0.5rem 0.75rem;
            font-size: 0.9rem;
            color: #ffffff;
            font-family: inherit;
        }
        .drawer-search-input:focus {
            outline: none;
            border-color: #38bdf8;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
        }

        .drawer-body {
            flex: 1;
            overflow-y: auto;
            padding: 0.85rem 0.75rem;
        }

        .drawer-pillar {
            margin-bottom: 1rem;
        }
        .drawer-pillar-title {
            font-size: 0.78rem;
            font-weight: 900;
            color: #38bdf8;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            padding: 0.4rem 0.6rem;
            display: flex;
            align-items: center;
            gap: 0.4rem;
            border-bottom: 1px solid rgba(56, 189, 248, 0.2);
            margin-bottom: 0.4rem;
        }

        .drawer-nav-item {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            width: 100%;
            padding: 0.6rem 0.85rem;
            background: transparent;
            border: 1px solid transparent;
            border-radius: 8px;
            color: #f1f5f9;
            font-size: 0.92rem;
            font-weight: 700;
            cursor: pointer;
            text-align: left;
            transition: all 0.15s ease;
            margin-bottom: 3px;
        }
        .drawer-nav-item:hover {
            background: rgba(56, 189, 248, 0.15);
            border-color: rgba(56, 189, 248, 0.4);
            color: #38bdf8;
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
        /* 5. TAB PANELS & GENERAL LAYOUT             */
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
            background: rgba(2, 6, 23, 0.88) !important;
            backdrop-filter: blur(6px) !important;
            z-index: 999999 !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 1.5rem !important;
        }
        .modal-backdrop.active, #account-modal.active {
            display: flex !important;
        }

        .modal-box {
            background: #0f172a;
            border: 1px solid var(--border-light);
            border-radius: 14px;
            width: 100%;
            max-width: 860px;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 25px 50px rgba(0,0,0,0.8);
            padding: 1.5rem;
            position: relative;
        }

        .input-group { margin-bottom: 0.85rem; }
        .input-label {
            display: block;
            font-size: 0.82rem;
            font-weight: 800;
            color: #cbd5e1;
            margin-bottom: 0.35rem;
        }
        .input-field {
            width: 100%;
            background: #040711;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 0.55rem 0.75rem;
            color: #ffffff;
            font-size: 0.88rem;
            outline: none;
            font-family: inherit;
        }
        .input-field:focus {
            border-color: var(--cyan);
            box-shadow: 0 0 10px var(--cyan-glow);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
            color: #f1f5f9;
        }
        thead tr {
            background: #020617;
            color: #94a3b8;
            font-weight: 800;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            border-bottom: 2px solid var(--border);
        }
        tbody tr {
            border-bottom: 1px solid rgba(51, 65, 85, 0.6);
            transition: background 0.15s ease;
        }
        tbody tr:hover {
            background: rgba(56, 189, 248, 0.08);
        }
        td {
            padding: 8px 12px;
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
                    <span class="kpi-chip-val" style="color:#4ade80;" id="caisse-balance-top">485 200 €</span>
                </div>
                <span class="kpi-chip-badge badge-success" id="hud-tresorerie-badge">+14.2k€/m</span>
            </div>

            <!-- 2. Chantiers -->
            <div class="kpi-chip-4x" id="hud-chip-chantiers" onclick="window.switchNav('projects_hub', this)" title="Chantiers en cours d'exécution">
                <span>🏗️</span>
                <div>
                    <span class="kpi-chip-lbl">CHANTIERS</span>
                    <span class="kpi-chip-val" style="color:#38bdf8;" id="hud-chantiers-val">4 / 4 Actifs</span>
                </div>
                <span class="kpi-chip-badge badge-info" id="hud-chantiers-badge">3.4 M€</span>
            </div>

            <!-- 3. Flotte Engins -->
            <div class="kpi-chip-4x" id="hud-chip-flotte" onclick="window.switchNav('materiel_depot', this)" title="Disponibilité parc matériel">
                <span>🚜</span>
                <div>
                    <span class="kpi-chip-lbl">FLOTTE TP</span>
                    <span class="kpi-chip-val" style="color:#fbbf24;" id="hud-flotte-val">6 / 6 Dispo</span>
                </div>
                <span class="kpi-chip-badge badge-warning" id="hud-flotte-badge">100% VGP</span>
            </div>

            <!-- 4. Effectif Salarié -->
            <div class="kpi-chip-4x" id="hud-chip-effectif" onclick="window.switchNav('rh_personnel', this)" title="Personnel de chantier">
                <span>👷</span>
                <div>
                    <span class="kpi-chip-lbl">EFFECTIF</span>
                    <span class="kpi-chip-val" style="color:#f8fafc;" id="hud-effectif-val">24 Salariés</span>
                </div>
                <span class="kpi-chip-badge badge-success" id="hud-effectif-badge">100% AIPR</span>
            </div>

            <!-- 5. Sécurité QSE -->
            <div class="kpi-chip-4x" id="hud-chip-securite" onclick="window.switchNav('safety_qse', this)" title="Score Sécurité & Prévention">
                <span>🛡️</span>
                <div>
                    <span class="kpi-chip-lbl">SÉCURITÉ</span>
                    <span class="kpi-chip-val" style="color:#4ade80;" id="hud-qse-val">98.5% Conforme</span>
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
                <span style="font-size:0.88rem; font-weight:900; color:#38bdf8; line-height:1.1;" id="hud-company-name-display">Occitanie TP & VRD ▾</span>
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
                📢 DIRECT EXÉCUTION : Marché Giratoire Barbazan notifié • Réception terrassement Lotissement Aurouer validée • Validation DICT AEP Sète • Aucun accident en cours (QSE 98.5%).
            </span>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- 3. QUICK-HUB DOCK (1-CLICK ACCESS BAR)     -->
    <!-- ========================================== -->
    <div class="quick-hub-bar" id="quick-hub-bar">
        <button class="quick-hub-btn active" onclick="window.switchNav('cockpit', this)">🏛️ Cockpit SIG</button>
        <button class="quick-hub-btn" onclick="window.switchNav('projects_hub', this)">🏗️ Chantiers Hub</button>
        <button class="quick-hub-btn" onclick="window.switchNav('devis_express', this)">📐 Devis Express & SDP</button>
        <button class="quick-hub-btn" onclick="window.switchNav('watchtower', this)">🛰️ Watch Tower 3D</button>
        <button class="quick-hub-btn" onclick="window.switchNav('technique_analyse', this)">🧪 Formules & 2D Enrobés</button>
        <button class="quick-hub-btn" onclick="window.switchNav('safety_qse', this)">🦺 Sécurité QSE & AIPR</button>
        <button class="quick-hub-btn" onclick="window.switchNav('pointage_terrain', this)">👷 Pointage & RDC</button>
        <button class="quick-hub-btn" onclick="window.switchNav('materiel_depot', this)">🚜 Flotte & Dépôt</button>
        <button class="quick-hub-btn" onclick="window.switchNav('company', this)">💶 Trésorerie & Caisse</button>
        <button class="quick-hub-btn" onclick="window.switchNav('rh_personnel', this)">👥 Équipe & RH</button>
        <button class="quick-hub-btn" onclick="window.switchNav('ccag_travaux', this)">⚖️ CCAG & Normes</button>
        <button class="quick-hub-btn" onclick="window.switchNav('obsidian_wiki', this)">🧠 Wiki Base</button>
    </div>

    <!-- ========================================== -->
    <!-- 4. LEFT FLYOUT DRAWER (SLIDING SIDEBAR)    -->
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

        <div style="padding:0.75rem 1rem; background:#020617; border-top:1px solid var(--border); display:flex; justify-content:space-between; align-items:center;">
            <button class="btn btn-primary" style="width:100%;" onclick="window.openAccountModal(); window.toggleSidebarDrawer(false);">👤 Gérer Entreprise / Compte</button>
        </div>
    </aside>

    <!-- MAIN APP CONTAINER -->
    <main class="app-main">
"""
'''
    with open("scripts/section_head_and_styles.py", "w", encoding="utf-8") as f:
        f.write(head_content)
    print("scripts/section_head_and_styles.py rewritten cleanly!")

# ==============================================================================
# 2. UPDATE scripts/section_modals.py
# ==============================================================================
def update_modals():
    with open("scripts/section_modals.py", "r", encoding="utf-8") as f:
        modals_code = f.read()

    # Make sure account-modal has high-contrast styles, clear form fields, and all 4 tabs
    account_modal_markup = r'''
    <!-- ========================================== -->
    <!-- UNIFIED ACCOUNT & IDENTITY MANAGEMENT MODAL-->
    <!-- ========================================== -->
    <div class="modal-backdrop" id="account-modal">
        <div class="modal-box" style="max-width:940px; max-height:90vh; display:flex; flex-direction:column;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; border-bottom:1px solid rgba(56,189,248,0.3); padding-bottom:0.75rem;">
                <div>
                    <h3 style="color:#38bdf8; font-size:1.3rem; font-weight:900; margin:0;" id="account-modal-title">🏢 Gestion du Compte, Entreprise & Rôle Utilisateur</h3>
                    <div style="font-size:0.85rem; color:#cbd5e1;">Connexion, création d'entreprise TP, identification hiérarchique et suppression</div>
                </div>
                <button class="btn btn-secondary" style="padding:0.3rem 0.65rem; font-size:1rem;" onclick="window.closeAccountModal()">✕</button>
            </div>

            <!-- TABS SELECTOR INSIDE MODAL -->
            <div style="display:flex; gap:0.5rem; background:#020617; padding:5px; border-radius:8px; border:1px solid var(--border); margin-bottom:1rem; flex-wrap:wrap;">
                <button class="btn-secondary account-tab-btn active" id="btn-acc-login" onclick="window.setAccountTab('login')">🔑 1. Connexion / Profils</button>
                <button class="btn-secondary account-tab-btn" id="btn-acc-create" onclick="window.setAccountTab('create')">➕ 2. Créer une Entreprise</button>
                <button class="btn-secondary account-tab-btn" id="btn-acc-identity" onclick="window.setAccountTab('identity')">👤 3. Mon Identité & Rôle</button>
                <button class="btn-secondary account-tab-btn" id="btn-acc-delete" onclick="window.setAccountTab('delete')">🗑️ 4. Suppression / Reset</button>
            </div>

            <!-- TAB 1: CONNEXION / PROFILS PRÉCONFIGURÉS -->
            <div class="acc-tab-content" id="acc-tab-login" style="display:block;">
                <div style="font-size:0.88rem; color:#cbd5e1; margin-bottom:0.75rem;">Sélectionnez une entreprise ou un profil de travail actif :</div>
                <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:0.85rem;" id="account-company-presets-grid">
                    <div class="catalog-card" style="cursor:pointer; border:1px solid #38bdf8; background:rgba(15,23,42,0.95); padding:1rem;" onclick="window.loginCompanyProfile('occitanie_tp')">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong style="color:#ffffff; font-size:1rem;">🏢 Occitanie TP & VRD (SAS)</strong>
                            <span class="badge-success" style="padding:2px 6px; border-radius:4px; font-size:0.75rem; font-weight:800;">RECOMMANDÉ</span>
                        </div>
                        <div style="font-size:0.82rem; color:#cbd5e1; margin:0.4rem 0;">PME Régionale Occitanie • Capital 250k€ • Trésorerie 485 200 €</div>
                        <div style="font-size:0.78rem; color:#94a3b8;">4 Chantiers actifs • 24 Salariés • Flotte 6 engins lourds</div>
                        <button class="btn btn-primary" style="margin-top:0.6rem; width:100%;">Se Connecter à cette Entreprise</button>
                    </div>

                    <div class="catalog-card" style="cursor:pointer; border:1px solid var(--border); background:rgba(15,23,42,0.95); padding:1rem;" onclick="window.loginCompanyProfile('artisan_2k')">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong style="color:#ffffff; font-size:1rem;">🚜 Artisan Solo Sud VRD</strong>
                            <span class="badge-warning" style="padding:2px 6px; border-radius:4px; font-size:0.75rem; font-weight:800;">MICRO-TP</span>
                        </div>
                        <div style="font-size:0.82rem; color:#cbd5e1; margin:0.4rem 0;">Artisan indépendant / Micro-entreprise • Trésorerie 2 400 €</div>
                        <div style="font-size:0.78rem; color:#94a3b8;">1 Chantier actif • 1 Salarié • 1 Minipelle + Camionette</div>
                        <button class="btn btn-secondary" style="margin-top:0.6rem; width:100%;">Activer le Profil Artisan</button>
                    </div>

                    <div class="catalog-card" style="cursor:pointer; border:1px solid var(--border); background:rgba(15,23,42,0.95); padding:1rem;" onclick="window.loginCompanyProfile('stagiaire_tp')">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong style="color:#ffffff; font-size:1rem;">🎓 Formation Conduite Travaux</strong>
                            <span class="badge-info" style="padding:2px 6px; border-radius:4px; font-size:0.75rem; font-weight:800;">ÉCOLE</span>
                        </div>
                        <div style="font-size:0.82rem; color:#cbd5e1; margin:0.4rem 0;">Centre de formation TP / Étude de cas • Trésorerie fictive 150k€</div>
                        <div style="font-size:0.78rem; color:#94a3b8;">Cas d'école complets Barbazan & Aurouer guidés</div>
                        <button class="btn btn-secondary" style="margin-top:0.6rem; width:100%;">Charger la Session Formation</button>
                    </div>

                    <div class="catalog-card" style="cursor:pointer; border:1px solid var(--border); background:rgba(15,23,42,0.95); padding:1rem;" onclick="window.loginCompanyProfile('compte_neuf')">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong style="color:#ffffff; font-size:1rem;">✨ Compte Neutre Vierge</strong>
                            <span style="color:#94a3b8; font-size:0.75rem; font-weight:800;">0 DONNÉE</span>
                        </div>
                        <div style="font-size:0.82rem; color:#cbd5e1; margin:0.4rem 0;">Environnement vierge pour démarrage complet personnalisé</div>
                        <div style="font-size:0.78rem; color:#94a3b8;">0 Chantier • 0 Salarié • Trésorerie de base 50 000 €</div>
                        <button class="btn btn-secondary" style="margin-top:0.6rem; width:100%;">Ouvrir Compte Vierge</button>
                    </div>
                </div>
            </div>

            <!-- TAB 2: CRÉATION D'ENTREPRISE -->
            <div class="acc-tab-content" id="acc-tab-create" style="display:none;">
                <form id="create-company-form" onsubmit="window.handleCreateCompany(event)">
                    <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:1rem;">
                        <div class="input-group">
                            <label class="input-label">Raison Sociale / Nom d'Entreprise *</label>
                            <input type="text" class="input-field" id="new-comp-name" placeholder="Ex: Méditerranée Travaux Publics" required>
                        </div>
                        <div class="input-group">
                            <label class="input-label">Forme Juridique *</label>
                            <select class="input-field" id="new-comp-legal">
                                <option value="SAS">SAS - Société par Actions Simplifiée</option>
                                <option value="SARL">SARL - Société à Responsabilité Limitée</option>
                                <option value="EURL">EURL - Entreprise Unipersonnelle</option>
                                <option value="SA">SA - Société Anonyme</option>
                                <option value="ARTISAN">Artisan / Micro-Entreprise TP</option>
                            </select>
                        </div>
                        <div class="input-group">
                            <label class="input-label">Capital Social Initial (€)</label>
                            <input type="number" class="input-field" id="new-comp-capital" value="50000" min="1000">
                        </div>
                        <div class="input-group">
                            <label class="input-label">Trésorerie de Départ (€)</label>
                            <input type="number" class="input-field" id="new-comp-treasury" value="120000" min="0">
                        </div>
                        <div class="input-group">
                            <label class="input-label">Ville du Siège Social / Région</label>
                            <input type="text" class="input-field" id="new-comp-city" value="Sète (Hérault 34)">
                        </div>
                        <div class="input-group">
                            <label class="input-label">Spécialité Principale</label>
                            <select class="input-field" id="new-comp-spec">
                                <option value="vrd">Terrassement, VRD & Voirie</option>
                                <option value="assainissement">Canalisations, Assainissement & AEP</option>
                                <option value="enrobes">Application d'Enrobés & Chaussées</option>
                                <option value="genie_civil">Génie Civil & Ouvrages d'Art</option>
                            </select>
                        </div>
                    </div>

                    <div class="input-group" style="margin-top:0.5rem; background:rgba(2,6,23,0.7); padding:0.85rem; border-radius:8px; border:1px solid var(--border);">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                            <label class="input-label" style="margin:0;">Taille de l'équipe initiale (Effectif Salariés) :</label>
                            <span style="font-weight:900; color:#38bdf8; font-size:1.1rem; font-family:var(--font-mono);" id="new-comp-headcount-disp">12 Salariés</span>
                        </div>
                        <input type="range" style="width:100%; accent-color:#38bdf8;" min="1" max="150" value="12" id="new-comp-headcount-slider" oninput="document.getElementById('new-comp-headcount-disp').textContent = this.value + ' Salariés'">
                    </div>

                    <div style="display:flex; justify-content:flex-end; gap:0.75rem; margin-top:1rem;">
                        <button type="button" class="btn btn-secondary" onclick="window.setAccountTab('login')">Annuler</button>
                        <button type="submit" class="btn btn-primary">🚀 Créer et Activer l'Entreprise</button>
                    </div>
                </form>
            </div>

            <!-- TAB 3: IDENTITÉ & RÔLE -->
            <div class="acc-tab-content" id="acc-tab-identity" style="display:none;">
                <form id="save-identity-form" onsubmit="window.handleSaveUserIdentity(event)">
                    <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:1rem;">
                        <div class="input-group">
                            <label class="input-label">Nom & Prénom de l'utilisateur *</label>
                            <input type="text" class="input-field" id="user-fullname" value="Jean DUPONT" required>
                        </div>
                        <div class="input-group">
                            <label class="input-label">Rôle & Perspective Opérationnelle *</label>
                            <select class="input-field" id="user-role-select" onchange="window.updateRolePreview(this.value)">
                                <option value="direction">👑 Direction & Gérant Entreprise</option>
                                <option value="conduite">👷 Conducteur de Travaux Principal</option>
                                <option value="chef_chantier">🦺 Chef de Chantier / Responsable Terrain</option>
                                <option value="compagnon">🛠️ Compagnon / Poseur / Chef d'équipe</option>
                            </select>
                        </div>
                    </div>

                    <div class="input-group" style="background:rgba(2,6,23,0.7); padding:0.85rem; border-radius:8px; border:1px solid var(--border); margin-top:0.5rem;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                            <label class="input-label" style="margin:0;">Ajustement de l'effectif total sous votre direction :</label>
                            <span style="font-weight:900; color:#4ade80; font-size:1.1rem; font-family:var(--font-mono);" id="user-headcount-display">24 Salariés</span>
                        </div>
                        <input type="range" style="width:100%; accent-color:#22c55e;" min="0" max="150" value="24" id="user-headcount-slider" oninput="window.updateHeadcountSlider(this.value)">
                        <div style="font-size:0.75rem; color:#94a3b8; margin-top:0.35rem;">Masse salariale estimée : <strong id="user-payroll-est" style="color:#ffffff;">84 000 € / mois</strong> (charges incluses)</div>
                    </div>

                    <div style="display:flex; justify-content:flex-end; gap:0.75rem; margin-top:1rem;">
                        <button type="submit" class="btn btn-primary">💾 Sauvegarder mon Profil & Identité</button>
                    </div>
                </form>
            </div>

            <!-- TAB 4: SUPPRESSION / RESET -->
            <div class="acc-tab-content" id="acc-tab-delete" style="display:none;">
                <div style="background:rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.4); padding:1rem; border-radius:8px; margin-bottom:1rem;">
                    <h4 style="color:#f87171; font-weight:800; margin-bottom:0.4rem;">⚠️ Zone Sensible & Réinitialisation</h4>
                    <p style="font-size:0.85rem; color:#fecaca;">Vous pouvez supprimer l'entreprise active ou réinitialiser complètement l'application aux paramètres d'usine.</p>
                </div>
                <div style="display:flex; flex-direction:column; gap:0.75rem;">
                    <button class="btn btn-danger" onclick="window.deleteActiveCompany()">🗑️ Supprimer l'Entreprise Active</button>
                    <button class="btn btn-secondary" style="border-color:#ef4444; color:#f87171;" onclick="window.resetAllDataFactory()">🔄 Réinitialiser Données Usine (Factory Reset)</button>
                </div>
            </div>
        </div>
    </div>
    '''

    # Replace existing account-modal in section_modals.py
    pattern = re.compile(r'<!-- ===+ -->\s*<!-- UNIFIED ACCOUNT & IDENTITY MANAGEMENT MODAL-->[\s\S]*?</div>\s*</div>\s*</div>', re.DOTALL)
    if pattern.search(modals_code):
        modals_code = pattern.sub(account_modal_markup.strip(), modals_code)
    else:
        # If not matched, replace between <div class="modal-backdrop" id="account-modal"> and its matching closure
        old_acc_pos = modals_code.find('id="account-modal"')
        if old_acc_pos != -1:
            div_start = modals_code.rfind('<div class="modal-backdrop"', 0, old_acc_pos)
            # Find matching close
            modals_code = modals_code[:div_start] + account_modal_markup.strip() + modals_code[div_start + 4000:]

    with open("scripts/section_modals.py", "w", encoding="utf-8") as f:
        f.write(modals_code)
    print("scripts/section_modals.py updated with crisp account modal!")

# ==============================================================================
# 3. UPDATE scripts/section_js_part3.py
# ==============================================================================
def update_js_part3():
    with open("scripts/section_js_part3.py", "r", encoding="utf-8") as f:
        js3_code = f.read()

    js_controllers = r'''
    // ==========================================
    // COMPLETE REACTIVE ACCOUNT & UI CONTROLLERS
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
        const s = window.userAccountState;
        
        // 1. Top HUD
        const caisseTop = document.getElementById('caisse-balance-top');
        if (caisseTop) caisseTop.textContent = new Intl.NumberFormat('fr-FR').format(s.treasury) + ' €';

        const hudChantiers = document.getElementById('hud-chantiers-val');
        if (hudChantiers) hudChantiers.textContent = `${s.projectsCount} / ${s.projectsCount} Actifs`;

        const hudFlotte = document.getElementById('hud-flotte-val');
        if (hudFlotte) hudFlotte.textContent = `${s.fleetCount} / ${s.fleetCount} Dispo`;

        const hudEffectif = document.getElementById('hud-effectif-val');
        if (hudEffectif) hudEffectif.textContent = `${s.headcount} Salarié${s.headcount > 1 ? 's' : ''}`;

        const hudQse = document.getElementById('hud-qse-val');
        if (hudQse) hudQse.textContent = `${s.qseScore}% Conforme`;

        const roleBadges = {
            'direction': '👑',
            'conduite': '👷',
            'chef_chantier': '🦺',
            'compagnon': '🛠️'
        };
        const roleLabels = {
            'direction': 'Direction',
            'conduite': 'Conduite',
            'chef_chantier': 'Chef Chantier',
            'compagnon': 'Compagnon'
        };
        const hudUser = document.getElementById('hud-user-identity');
        if (hudUser) hudUser.textContent = `${roleBadges[s.userRole] || '👤'} ${s.userName} (${roleLabels[s.userRole] || 'Direction'})`;

        const hudComp = document.getElementById('hud-company-name-display');
        if (hudComp) hudComp.textContent = `${s.companyName} ▾`;

        // 2. News Ticker
        const ticker = document.getElementById('live-ticker-text');
        if (ticker) {
            ticker.textContent = `📢 ${s.companyName} • Direction : ${s.userName} • Caisse Active : ${new Intl.NumberFormat('fr-FR').format(s.treasury)} € • Effectif : ${s.headcount} salariés • Chantiers : ${s.projectsCount} actifs (Barbazan, Aurouer, Sète).`;
        }
    };

    window.toggleSidebarDrawer = function(forceState) {
        const drawer = document.getElementById('sidebar-drawer');
        const backdrop = document.getElementById('sidebar-backdrop');
        if (!drawer) return;
        const isOpen = drawer.classList.contains('active') || drawer.classList.contains('open');
        const target = (typeof forceState === 'boolean') ? forceState : !isOpen;
        if (target) {
            drawer.classList.add('active', 'open');
            if (backdrop) backdrop.classList.add('active', 'open');
        } else {
            drawer.classList.remove('active', 'open');
            if (backdrop) backdrop.classList.remove('active', 'open');
        }
    };

    window.openAccountModal = function() {
        const modal = document.getElementById('account-modal') || document.getElementById('company-switch-modal');
        if (modal) {
            modal.style.display = 'flex';
            modal.classList.add('active');
            window.setAccountTab('login');
            window.loadAccountFormValues();
        }
    };

    window.closeAccountModal = function() {
        const modal = document.getElementById('account-modal') || document.getElementById('company-switch-modal');
        if (modal) {
            modal.style.display = 'none';
            modal.classList.remove('active');
        }
    };
    window.openCompanySwitchModal = window.openAccountModal;

    window.setAccountTab = function(tabKey) {
        document.querySelectorAll('.account-tab-btn').forEach(b => b.classList.remove('active'));
        const btn = document.getElementById('btn-acc-' + tabKey);
        if (btn) btn.classList.add('active');

        document.querySelectorAll('.acc-tab-content').forEach(c => c.style.display = 'none');
        const tab = document.getElementById('acc-tab-' + tabKey);
        if (tab) tab.style.display = 'block';
    };

    window.loadAccountFormValues = function() {
        const nameInput = document.getElementById('user-fullname');
        const roleSelect = document.getElementById('user-role-select');
        const headSlider = document.getElementById('user-headcount-slider');
        const headDisp = document.getElementById('user-headcount-display');

        if (nameInput) nameInput.value = window.userAccountState.userName;
        if (roleSelect) roleSelect.value = window.userAccountState.userRole;
        if (headSlider) headSlider.value = window.userAccountState.headcount;
        if (headDisp) headDisp.textContent = window.userAccountState.headcount + ' Salariés';
    };

    window.loginCompanyProfile = function(profileKey) {
        const presets = {
            'occitanie_tp': { name: 'Occitanie TP & VRD', treasury: 485200, headcount: 24, projects: 4, fleet: 6 },
            'artisan_2k': { name: 'Artisan Sud VRD', treasury: 2400, headcount: 1, projects: 1, fleet: 1 },
            'stagiaire_tp': { name: 'Formation Conduite Travaux', treasury: 150000, headcount: 8, projects: 2, fleet: 3 },
            'compte_neuf': { name: 'Nouvelle Entreprise TP', treasury: 50000, headcount: 2, projects: 0, fleet: 1 }
        };
        const p = presets[profileKey] || presets['occitanie_tp'];
        window.userAccountState.companyKey = profileKey;
        window.userAccountState.companyName = p.name;
        window.userAccountState.treasury = p.treasury;
        window.userAccountState.headcount = p.headcount;
        window.userAccountState.projectsCount = p.projects;
        window.userAccountState.fleetCount = p.fleet;

        window.updateAllHudAndTickerMetrics();
        window.closeAccountModal();
        if (window.showNotification) window.showNotification(`Entreprise connectée : ${p.name}`, 'success');
    };

    window.handleCreateCompany = function(e) {
        e.preventDefault();
        const name = document.getElementById('new-comp-name')?.value || 'Nouvelle Entreprise TP';
        const treasury = parseFloat(document.getElementById('new-comp-treasury')?.value || 120000);
        const headcount = parseInt(document.getElementById('new-comp-headcount-slider')?.value || 12, 10);

        window.userAccountState.companyName = name;
        window.userAccountState.treasury = treasury;
        window.userAccountState.headcount = headcount;
        window.userAccountState.projectsCount = 1;
        window.userAccountState.fleetCount = Math.max(1, Math.round(headcount / 4));

        window.updateAllHudAndTickerMetrics();
        window.closeAccountModal();
        if (window.showNotification) window.showNotification(`Entreprise "${name}" créée et activée avec succès !`, 'success');
        window.switchNav('cockpit');
    };

    window.handleSaveUserIdentity = function(e) {
        e.preventDefault();
        const name = document.getElementById('user-fullname')?.value || 'Jean DUPONT';
        const role = document.getElementById('user-role-select')?.value || 'direction';
        const headcount = parseInt(document.getElementById('user-headcount-slider')?.value || 24, 10);

        window.userAccountState.userName = name;
        window.userAccountState.userRole = role;
        window.userAccountState.headcount = headcount;

        window.updateAllHudAndTickerMetrics();
        window.closeAccountModal();
        if (window.showNotification) window.showNotification('Identité et rôle enregistrés avec succès !', 'success');
    };

    window.updateHeadcountSlider = function(val) {
        const count = parseInt(val, 10);
        window.userAccountState.headcount = count;
        const disp = document.getElementById('user-headcount-display');
        if (disp) disp.textContent = count + ' Salarié' + (count > 1 ? 's' : '');

        const payroll = document.getElementById('user-payroll-est');
        if (payroll) payroll.textContent = new Intl.NumberFormat('fr-FR').format(count * 3500) + ' € / mois';

        const hudEffectif = document.getElementById('hud-effectif-val');
        if (hudEffectif) hudEffectif.textContent = count + ' Salarié' + (count > 1 ? 's' : '');
    };

    window.deleteActiveCompany = function() {
        if (confirm(`Êtes-vous sûr de vouloir supprimer l'entreprise "${window.userAccountState.companyName}" ?`)) {
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
        document.querySelectorAll('.ticker-mode-btn').forEach(b => b.classList.remove('active'));
        const btn = document.getElementById('ticker-btn-' + mode);
        if (btn) btn.classList.add('active');

        const track = document.getElementById('live-ticker-text');
        if (!track) return;

        const s = window.userAccountState;
        const formattedCaisse = new Intl.NumberFormat('fr-FR').format(s.treasury);

        if (mode === 'general') {
            track.textContent = `📢 GÉNÉRAL : ${s.companyName} • Marché Giratoire Barbazan notifié • Réception terrassement Aurouer validée • DICT AEP Sète conforme.`;
        } else if (mode === 'finance') {
            track.textContent = `💰 FINANCE : Caisse active ${formattedCaisse} € • Situation Chorus Pro n°4 encaissée (+42 500 €) • Déblocage retenue de garantie 5% • Marge moyenne 14.8%.`;
        } else if (mode === 'security') {
            track.textContent = `🚨 SÉCURITÉ & QSE : Alerte météo vent 50 km/h bassin de Thau • Conformité blindage tranchées 100% • Score AIPR 100% • 0 accident sur 365j.`;
        } else if (mode === 'logistics') {
            track.textContent = `🚛 LOGISTIQUE : ${s.fleetCount} engins opérationnels (VGP 100%) • 8 rotations camions 8x4 enrobés BBSG 0/10 • Stock GNT 0/31.5 : 420 Tonnes.`;
        }
    };

    window.filterDrawerItems = function() {
        const input = document.getElementById('drawerSearchInput');
        if (!input) return;
        const filter = input.value.toLowerCase().trim();
        document.querySelectorAll('.drawer-nav-item').forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = (filter === '' || text.includes(filter)) ? 'flex' : 'none';
        });
        document.querySelectorAll('.drawer-pillar').forEach(pillar => {
            const visibleItems = pillar.querySelectorAll('.drawer-nav-item:not([style*="display: none"])');
            pillar.style.display = visibleItems.length > 0 ? 'block' : 'none';
        });
    };
    '''

    # Place in js3_code
    pos_end_script = js3_code.rfind('</script>')
    if pos_end_script != -1:
        js3_code = js3_code[:pos_end_script] + js_controllers + js3_code[pos_end_script:]

    with open("scripts/section_js_part3.py", "w", encoding="utf-8") as f:
        f.write(js3_code)
    print("scripts/section_js_part3.py updated with reactive account logic!")

if __name__ == '__main__':
    update_head_and_styles()
    update_modals()
    update_js_part3()
