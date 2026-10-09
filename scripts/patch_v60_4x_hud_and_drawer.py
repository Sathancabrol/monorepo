#!/usr/bin/env python3
"""
Patch v60: Complete 4X HUD Topbar, Dynamic Multi-Mode News Ticker,
Collapsible Left Flyout Drawer Sidebar, and Unified Account (Login/Create/Delete/Role/Headcount)
"""

import re

print("Starting Patch v60 UI/UX Transformation...")

# 1. Update scripts/section_head_and_styles.py
with open("scripts/section_head_and_styles.py", "r", encoding="utf-8") as f:
    text = f.read()

# New CSS for 4X Topbar, News Ticker, Drawer Sidebar, and Decluttered Layout
new_drawer_css = """
        /* ========================================== */
        /* 4X GRAND STRATEGY HUD TOPBAR & TICKER      */
        /* ========================================== */
        .hud-topbar-4x {
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
        }

        .hud-brand-group {
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }

        /* 3-BAR / HAMBURGER TRIGGER BUTTON */
        .drawer-toggle-btn {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(56, 189, 248, 0.4);
            color: #38bdf8;
            padding: 0.35rem 0.55rem;
            border-radius: 6px;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 3px;
            width: 34px;
            height: 34px;
            transition: all 0.2s ease;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.15);
        }
        .drawer-toggle-btn:hover {
            background: #0284c7;
            color: #ffffff;
            border-color: #38bdf8;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
            transform: scale(1.05);
        }
        .drawer-toggle-btn span {
            display: block;
            width: 18px;
            height: 2px;
            background: currentColor;
            border-radius: 2px;
            transition: all 0.2s ease;
        }

        .hud-brand-title {
            font-size: 0.85rem;
            font-weight: 900;
            letter-spacing: -0.01em;
            color: #f8fafc;
            line-height: 1.1;
        }
        .hud-brand-subtitle {
            font-size: 0.65rem;
            color: #94a3b8;
            font-weight: 600;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        /* 4X METRIC CHIPS */
        .hud-4x-metrics {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            flex-wrap: wrap;
            flex: 1;
            justify-content: center;
        }

        .kpi-chip-4x {
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid rgba(51, 65, 85, 0.8);
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            display: flex;
            align-items: center;
            gap: 0.45rem;
            font-size: 0.78rem;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
            transition: border-color 0.15s ease;
            cursor: pointer;
        }
        .kpi-chip-4x:hover {
            border-color: #38bdf8;
            background: rgba(30, 41, 59, 0.9);
        }
        .kpi-chip-val {
            font-weight: 800;
            font-family: var(--font-mono);
            letter-spacing: -0.02em;
        }
        .kpi-chip-badge {
            font-size: 0.65rem;
            padding: 1px 4px;
            border-radius: 3px;
            font-weight: 700;
        }

        /* ACCOUNT & PROFILE TRIGGER BUTTON */
        .hud-account-card {
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid rgba(56, 189, 248, 0.4);
            padding: 0.25rem 0.65rem;
            border-radius: 6px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .hud-account-card:hover {
            background: rgba(2, 132, 199, 0.2);
            border-color: #38bdf8;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.25);
        }

        /* BREAKING NEWS TICKER */
        .news-ticker-bar {
            background: #020617;
            border-bottom: 1px solid rgba(51, 65, 85, 0.8);
            display: flex;
            align-items: center;
            padding: 0.25rem 0.8rem;
            font-size: 0.75rem;
            gap: 0.6rem;
            overflow: hidden;
            position: sticky;
            top: 48px;
            z-index: 95;
        }
        .ticker-mode-btns {
            display: flex;
            gap: 2px;
            background: #0b1120;
            padding: 2px;
            border-radius: 4px;
            border: 1px solid var(--border);
            flex-shrink: 0;
        }
        .ticker-mode-btn {
            background: transparent;
            border: none;
            color: #94a3b8;
            font-size: 0.68rem;
            font-weight: 700;
            padding: 0.15rem 0.45rem;
            border-radius: 3px;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .ticker-mode-btn.active {
            background: #0284c7;
            color: #ffffff;
        }
        .ticker-content-track {
            flex: 1;
            overflow: hidden;
            white-space: nowrap;
            position: relative;
        }
        .ticker-text {
            display: inline-block;
            color: #cbd5e1;
            animation: tickerSlide 35s linear infinite;
        }
        .ticker-text:hover {
            animation-play-state: paused;
        }
        @keyframes tickerSlide {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }

        /* ========================================== */
        /* LEFT FLYOUT DRAWER SIDEBAR NAVIGATION      */
        /* ========================================== */
        .sidebar-backdrop {
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(2, 6, 23, 0.7);
            backdrop-filter: blur(4px);
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.25s ease;
        }
        .sidebar-backdrop.active {
            display: block;
            opacity: 1;
        }

        .sidebar-drawer {
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
        }

        .drawer-header {
            padding: 0.85rem 1rem;
            background: #020617;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .drawer-title {
            font-size: 0.85rem;
            font-weight: 800;
            color: #38bdf8;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }
        .drawer-close-btn {
            background: #1e293b;
            border: 1px solid var(--border);
            color: #94a3b8;
            width: 26px;
            height: 26px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 0.85rem;
        }
        .drawer-close-btn:hover {
            color: #ffffff;
            background: #ef4444;
            border-color: #ef4444;
        }

        .drawer-search-box {
            padding: 0.6rem 0.8rem;
            border-bottom: 1px solid rgba(51, 65, 85, 0.5);
            background: rgba(15, 23, 42, 0.4);
        }
        .drawer-search-input {
            width: 100%;
            background: #020617;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 0.35rem 0.6rem;
            font-size: 0.78rem;
            color: #f8fafc;
        }
        .drawer-search-input:focus {
            outline: none;
            border-color: #38bdf8;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25);
        }

        .drawer-body {
            flex: 1;
            overflow-y: auto;
            padding: 0.6rem 0.5rem;
        }

        .drawer-pillar {
            margin-bottom: 0.75rem;
        }
        .drawer-pillar-title {
            font-size: 0.7rem;
            font-weight: 800;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 0.3rem 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }

        .drawer-nav-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            width: 100%;
            padding: 0.45rem 0.65rem;
            background: transparent;
            border: 1px solid transparent;
            border-radius: 6px;
            color: #cbd5e1;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            text-align: left;
            transition: all 0.15s ease;
            margin-bottom: 2px;
        }
        .drawer-nav-item:hover {
            background: rgba(56, 189, 248, 0.08);
            border-color: rgba(56, 189, 248, 0.25);
            color: #38bdf8;
            transform: translateX(2px);
        }
        .drawer-nav-item.active {
            background: linear-gradient(90deg, rgba(2, 132, 199, 0.3) 0%, rgba(6, 182, 212, 0.1) 100%);
            border-color: #38bdf8;
            color: #38bdf8;
            font-weight: 800;
            box-shadow: inset 3px 0 0 #38bdf8;
        }

        .drawer-footer {
            padding: 0.6rem 0.8rem;
            background: #020617;
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.7rem;
        }

        .app-main {
            flex: 1;
            padding: 0.75rem 1rem 5rem 1rem;
            max-width: 1750px;
            margin: 0 auto;
            width: 100%;
        }
"""

# Replace old header & nav-dock CSS with new_drawer_css
pos_style_close = text.find('</style>')
if pos_style_close != -1:
    text = text[:pos_style_close] + new_drawer_css + text[pos_style_close:]
    print("Injected Drawer & 4X Topbar CSS!")

# Replace HTML header and navigation dock in section_head_and_styles.py
old_html_header_and_dock = """    <!-- APP HEADER -->
    <header class="header">
        <div class="brand">
            <div class="brand-logo">⚡</div>
            <div>
                <div class="brand-title">BTP AUTONOMOUS COMMAND <span style="font-size:0.75rem; color:var(--cyan); font-weight:700;">v4.8</span></div>
                <div class="brand-subtitle">SYSTÈME D'EXPLOITATION INTÉGRÉ VRD & TRAVAUX PUBLICS</div>
            </div>
        </div>

        <!-- PERSPECTIVE BAR -->
        <div class="perspective-bar">
            <button class="perspective-btn active" id="btn-persp-patron" onclick="switchPerspective('patron', this)">👑 Direction & Patron</button>
            <button class="perspective-btn" id="btn-persp-conduite" onclick="switchPerspective('conduite', this)">👷‍♂️ Conduite de Travaux</button>
            <button class="perspective-btn" id="btn-persp-compagnon" onclick="switchPerspective('compagnon', this)">🦺 Compagnons Terrain</button>
        </div>

        <!-- HUD ITEMS -->
        <div class="hud-items">
            <div class="hud-pill" id="hud-company-selector" style="border:1px solid var(--cyan); cursor:pointer; background:rgba(6,182,212,0.15);" onclick="openModal('company-switch-modal')" title="Changer de profil d'entreprise">
                <span style="color:var(--cyan);">🏢 Société :</span>
                <b id="active-company-name-top" style="color:#f8fafc;">Occitanie TP & VRD ▾</b>
            </div>
            <div class="hud-pill" id="hud-treasury">
                <span style="color:var(--emerald);">💶 Caisse :</span>
                <b id="caisse-balance-top" style="color:#fff;">485 200 €</b>
            </div>
            <div class="hud-pill">
                <span>⛅ Alès 22°C</span>
            </div>
            <button class="btn-primary" style="font-size:0.72rem; padding:0.3rem 0.6rem;" onclick="runAutopilot()">
                🤖 Pilote Automatique
            </button>
            <button class="btn-secondary" id="btn-voice-toggle" style="font-size:0.72rem; padding:0.3rem 0.6rem;" onclick="toggleVoiceControl()">
                🎙️ Commande Vocale
            </button>
            <button class="btn-danger" style="font-size:0.72rem; padding:0.3rem 0.6rem;" onclick="triggerSimulatedCrisis()">
                🚨 Simuler Crise
            </button>
        </div>
    </header>

    <!-- NAVIGATION DOCK -->
    <div class="nav-dock-container">
        <button class="btn-secondary" style="padding:0.25rem 0.5rem; margin-right:0.3rem;" onclick="scrollNav(-200)">◀</button>
        <nav class="nav-dock" id="main-nav-dock">
            <button class="nav-item active" onclick="switchNav('cockpit', this)">🎛️ Cockpit & SIG</button>
            <button class="nav-item" onclick="switchNav('company', this)">🏢 Entreprise & Caisse</button>
            <button class="nav-item" onclick="switchNav('depot', this)">🏭 Dépôt & Inventaire</button>
            <button class="nav-item" onclick="switchNav('projects_hub', this)">📁 Chantiers & Marchés</button>
            <button class="nav-item" onclick="switchNav('planning', this)">📅 Planning Gantt & Agenda</button>
            <button class="nav-item" onclick="switchNav('simulator', this)">🛰️ Watch Tower 3D</button>
            <button class="nav-item" onclick="switchNav('fleet', this)">🚜 Flotte Engins</button>
            <button class="nav-item" onclick="switchNav('catalog', this)">🛒 Outils & Matériaux</button>
            <button class="nav-item" onclick="switchNav('opbtp', this)">🦺 Signalétique OPBTP</button>
            <button class="nav-item" onclick="switchNav('safety', this)">🛡️ Sécurité & AIPR</button>
            <button class="nav-item" onclick="switchNav('sdp', this)">💰 28 SDP & TCD DQE</button>
            <button class="nav-item" onclick="switchNav('schemas', this)">📐 Technique & Analyse</button>
            <button class="nav-item" onclick="switchNav('procurement', this)">🛒 Fournisseurs</button>
            <button class="nav-item" onclick="switchNav('docs', this)">⚖️ Réglementation, Normes & Outils</button>
            <button class="nav-item" onclick="switchNav('benchmark', this)">📊 Benchmark & Inventaire</button>
            <button class="nav-item" onclick="switchNav('hr', this)">👷 Organigramme RH</button>
            <button class="nav-item" onclick="switchNav('rdc', this)">📋 Rapport RDC</button>
            <button class="nav-item" onclick="switchNav('obsidian', this)">📚 Base Obsidian</button>
            <button class="nav-item" onclick="switchNav('ledger', this)">⛓️ Ledger SHA-256</button>
            <button class="nav-item" onclick="switchNav('archives', this)">🗄️ Archives & GED</button>
        </nav>
        <button class="btn-secondary" style="padding:0.25rem 0.5rem; margin-left:0.3rem;" onclick="scrollNav(200)">▶</button>
    </div>"""

new_4x_hud_and_drawer_html = """    <!-- ========================================== -->
    <!-- 4X GRAND STRATEGY TOP HUD BAR             -->
    <!-- ========================================== -->
    <header class="hud-topbar-4x">
        <!-- LEFT: DRAWER TRIGGER & BRAND -->
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
        </div>

        <!-- CENTER: 4X MACRO ENTERPRISE INDICES -->
        <div class="hud-4x-metrics">
            <!-- 1. Trésorerie -->
            <div class="kpi-chip-4x" onclick="switchNav('company')" title="Caisse active & BFR">
                <span>💶</span>
                <div>
                    <span style="font-size:0.65rem; color:#94a3b8; display:block;">TRÉSORERIE</span>
                    <span class="kpi-chip-val text-emerald" id="caisse-balance-top">485 200 €</span>
                </div>
                <span class="kpi-chip-badge badge-success">+14.2k€</span>
            </div>

            <!-- 2. Chantiers -->
            <div class="kpi-chip-4x" onclick="switchNav('projects_hub')" title="Chantiers en cours d'exécution">
                <span>🏗️</span>
                <div>
                    <span style="font-size:0.65rem; color:#94a3b8; display:block;">CHANTIERS</span>
                    <span class="kpi-chip-val text-cyan" id="hud-chantiers-val">4 / 4 Actifs</span>
                </div>
                <span class="kpi-chip-badge badge-info">3.4 M€</span>
            </div>

            <!-- 3. Flotte Engins -->
            <div class="kpi-chip-4x" onclick="switchNav('fleet')" title="Disponibilité parc matériel">
                <span>🚜</span>
                <div>
                    <span style="font-size:0.65rem; color:#94a3b8; display:block;">FLOTTE TP</span>
                    <span class="kpi-chip-val text-amber" id="hud-flotte-val">6 / 6 Dispo</span>
                </div>
                <span class="kpi-chip-badge badge-warning">100% VGP</span>
            </div>

            <!-- 4. Effectif & Équipes -->
            <div class="kpi-chip-4x" onclick="switchNav('hr')" title="Collaborateurs & Compagnons">
                <span>👷</span>
                <div>
                    <span style="font-size:0.65rem; color:#94a3b8; display:block;">EFFECTIF</span>
                    <span class="kpi-chip-val" id="hud-effectif-val" style="color:#f8fafc;">24 Salariés</span>
                </div>
                <span class="kpi-chip-badge badge-info">100% AIPR</span>
            </div>

            <!-- 5. Sécurité QSE -->
            <div class="kpi-chip-4x" onclick="switchNav('safety')" title="Indicateur Sécurité & Prévention">
                <span>🛡️</span>
                <div>
                    <span style="font-size:0.65rem; color:#94a3b8; display:block;">SÉCURITÉ</span>
                    <span class="kpi-chip-val text-emerald" id="hud-qse-val">98.5% Conforme</span>
                </div>
                <span class="kpi-chip-badge badge-success">0 Accident</span>
            </div>

            <!-- 6. Météo Terrain -->
            <div class="kpi-chip-4x" onclick="switchNav('planning')" title="Météo Bassin de Thau / Sète">
                <span>⛅</span>
                <div>
                    <span style="font-size:0.65rem; color:#94a3b8; display:block;">MÉTÉO SÈTE</span>
                    <span class="kpi-chip-val" style="color:#38bdf8;">22°C • Vent 14 km/h</span>
                </div>
            </div>
        </div>

        <!-- RIGHT: ACCOUNT & QUICK ACTIONS -->
        <div style="display:flex; align-items:center; gap:0.4rem;">
            <div class="hud-account-card" onclick="openAccountModal()" title="Gérer le compte, rôle, identité et entreprise">
                <span style="font-size:1.1rem;" id="hud-role-icon">👑</span>
                <div style="text-align:left;">
                    <div style="font-size:0.75rem; font-weight:800; color:#f8fafc;" id="hud-user-name-display">Jean DUPONT</div>
                    <div style="font-size:0.65rem; color:#38bdf8;" id="hud-company-name-display">Occitanie TP ▾</div>
                </div>
            </div>
            <button class="btn-primary" style="font-size:0.72rem; padding:0.3rem 0.55rem;" onclick="runAutopilot()" title="Lancer le cycle autonome de supervision IA">
                🤖 Autopilot
            </button>
            <button class="btn-danger" style="font-size:0.72rem; padding:0.3rem 0.55rem;" onclick="openSafetyEmergencySimulator()" title="Simuler une situation d'urgence ou rupture réseau">
                🚨 Urgence
            </button>
        </div>
    </header>

    <!-- ========================================== -->
    <!-- DYNAMIC BREAKING NEWS TICKER               -->
    <!-- ========================================== -->
    <div class="news-ticker-bar">
        <div class="ticker-mode-btns">
            <button class="ticker-mode-btn active" id="btn-ticker-general" onclick="setTickerMode('general')">📢 Général</button>
            <button class="ticker-mode-btn" id="btn-ticker-finance" onclick="setTickerMode('finance')">💰 Finance</button>
            <button class="ticker-mode-btn" id="btn-ticker-safety" onclick="setTickerMode('safety')">🚨 Sécurité</button>
            <button class="ticker-mode-btn" id="btn-ticker-logistics" onclick="setTickerMode('logistics')">🚛 Logistique</button>
        </div>
        <div class="ticker-content-track">
            <div class="ticker-text" id="live-news-ticker-text">
                🚀 FLASH : Décompte mensuel Chorus Pro validé (+48 500 €) • DICT Sète PK 0+240 purgée sans réserve • 29.4t BBSG 0/10 livrées à 168°C par centrale Saint-Thibéry • Inspection CSPS conforme (100% EPI portés).
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SIDEBAR FLYOUT DRAWER (VOLANT DÉROULANT)   -->
    <!-- ========================================== -->
    <div class="sidebar-backdrop" id="sidebar-backdrop" onclick="toggleSidebarDrawer(false)"></div>
    <aside class="sidebar-drawer" id="sidebar-drawer">
        <!-- DRAWER HEADER -->
        <div class="drawer-header">
            <div class="drawer-title">🧭 Navigation Générale</div>
            <button class="drawer-close-btn" onclick="toggleSidebarDrawer(false)">&times;</button>
        </div>

        <!-- QUICK SEARCH -->
        <div class="drawer-search-box">
            <input type="text" class="drawer-search-input" id="drawer-search-input" placeholder="🔍 Rechercher un onglet, formule, chantier..." oninput="filterDrawerItems(this.value)">
        </div>

        <!-- DRAWER BODY WITH 4 EXECUTIVE PILLARS -->
        <div class="drawer-body" id="drawer-body-container">
            <!-- PÔLE 1: DIRECTION & COMMANDEMENT -->
            <div class="drawer-pillar">
                <div class="drawer-pillar-title">🏛️ I. Direction & Commandement</div>
                <button class="drawer-nav-item active" data-tab="cockpit" onclick="switchNav('cockpit'); toggleSidebarDrawer(false);">
                    <span>🎛️</span> Cockpit & Supervision SIG
                </button>
                <button class="drawer-nav-item" data-tab="company" onclick="switchNav('company'); toggleSidebarDrawer(false);">
                    <span>🏢</span> Entreprise, Trésorerie & BFR
                </button>
                <button class="drawer-nav-item" data-tab="benchmark" onclick="switchNav('benchmark'); toggleSidebarDrawer(false);">
                    <span>📊</span> Benchmark Prix Concurrence
                </button>
                <button class="drawer-nav-item" data-tab="archives" onclick="switchNav('archives'); toggleSidebarDrawer(false);">
                    <span>🗄️</span> Archives Légales & GED
                </button>
                <button class="drawer-nav-item" data-tab="ledger" onclick="switchNav('ledger'); toggleSidebarDrawer(false);">
                    <span>⛓️</span> Registre Blockchain SHA-256
                </button>
            </div>

            <!-- PÔLE 2: CHANTIERS & EXÉCUTION -->
            <div class="drawer-pillar">
                <div class="drawer-pillar-title">🏗️ II. Chantiers & Exécution</div>
                <button class="drawer-nav-item" data-tab="projects_hub" onclick="switchNav('projects_hub'); toggleSidebarDrawer(false);">
                    <span>📁</span> Hub des Chantiers & Marchés
                </button>
                <button class="drawer-nav-item" data-tab="planning" onclick="switchNav('planning'); toggleSidebarDrawer(false);">
                    <span>📅</span> Planning Gantt & Intempéries CCAG
                </button>
                <button class="drawer-nav-item" data-tab="rdc" onclick="switchNav('rdc'); toggleSidebarDrawer(false);">
                    <span>📋</span> Journal RDC & Pesées Centrales
                </button>
                <button class="drawer-nav-item" data-tab="compagnon_mobile" onclick="switchNav('compagnon_mobile'); toggleSidebarDrawer(false);">
                    <span>📱</span> Mode Terrain Compagnon VRD
                </button>
            </div>

            <!-- PÔLE 3: INGÉNIERIE & ÉTUDES DE PRIX -->
            <div class="drawer-pillar">
                <div class="drawer-pillar-title">📐 III. Ingénierie & Études de Prix</div>
                <button class="drawer-nav-item" data-tab="sdp" onclick="switchNav('sdp'); toggleSidebarDrawer(false);">
                    <span>💰</span> 28 SDP, DQE & Devis Express
                </button>
                <button class="drawer-nav-item" data-tab="schemas" onclick="switchNav('schemas'); toggleSidebarDrawer(false);">
                    <span>📐</span> Formules, Hydraulique, GTR & Bruckner
                </button>
                <button class="drawer-nav-item" data-tab="simulator" onclick="switchNav('simulator'); toggleSidebarDrawer(false);">
                    <span>🛰️</span> Watch Tower Jumeau 3D & SIG HD
                </button>
            </div>

            <!-- PÔLE 4: SÉCURITÉ, QSE & MOYENS -->
            <div class="drawer-pillar">
                <div class="drawer-pillar-title">🦺 IV. Sécurité, QSE & Moyens</div>
                <button class="drawer-nav-item" data-tab="safety" onclick="switchNav('safety'); toggleSidebarDrawer(false);">
                    <span>🛡️</span> Sécurité AIPR, DICT & 1/4h
                </button>
                <button class="drawer-nav-item" data-tab="opbtp" onclick="switchNav('opbtp'); toggleSidebarDrawer(false);">
                    <span>🦺</span> Signalétique & Balisage OPPBTP
                </button>
                <button class="drawer-nav-item" data-tab="fleet" onclick="switchNav('fleet'); toggleSidebarDrawer(false);">
                    <span>🚜</span> Flotte Engins & Télémétrie
                </button>
                <button class="drawer-nav-item" data-tab="depot" onclick="switchNav('depot'); toggleSidebarDrawer(false);">
                    <span>🏭</span> Dépôt, Matériaux & Stocks
                </button>
                <button class="drawer-nav-item" data-tab="procurement" onclick="switchNav('procurement'); toggleSidebarDrawer(false);">
                    <span>🛒</span> Fournisseurs & Logistique Thau
                </button>
                <button class="drawer-nav-item" data-tab="hr" onclick="switchNav('hr'); toggleSidebarDrawer(false);">
                    <span>👷</span> Organigramme RH & Équipes
                </button>
                <button class="drawer-nav-item" data-tab="docs" onclick="switchNav('docs'); toggleSidebarDrawer(false);">
                    <span>⚖️</span> Textes Légaux, Normes & CCTG
                </button>
                <button class="drawer-nav-item" data-tab="obsidian" onclick="switchNav('obsidian'); toggleSidebarDrawer(false);">
                    <span>📚</span> Base de Connaissances Obsidian
                </button>
            </div>
        </div>

        <!-- DRAWER FOOTER -->
        <div class="drawer-footer">
            <button class="btn btn-secondary" style="font-size:0.7rem; padding:0.25rem 0.5rem;" onclick="openAccountModal(); toggleSidebarDrawer(false);">
                👤 Mon Compte
            </button>
            <span class="badge badge-success" style="font-size:0.65rem;">🟢 PWA Offline</span>
        </div>
    </aside>"""

text = text.replace(old_html_header_and_dock, new_4x_hud_and_drawer_html)

with open("scripts/section_head_and_styles.py", "w", encoding="utf-8") as f:
    f.write(text)

print("scripts/section_head_and_styles.py updated successfully!")
