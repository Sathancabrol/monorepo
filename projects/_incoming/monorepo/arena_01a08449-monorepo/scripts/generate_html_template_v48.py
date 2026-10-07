from pathlib import Path

def write_template():
    target = Path('/home/user/monorepo/projects/btp-conduite-travaux/template.html')
    
    with open(target, 'w', encoding='utf-8') as f:
        # Part 1: HTML Head and Global Styles
        f.write("""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BTP Autonomous Command Suite v4.8 — Direction & Conduite de Travaux</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #030712;
            --bg-card: #0f172a;
            --bg-card-alt: #1e293b;
            --bg: #090d16;
            --border: #334155;
            --border-light: #475569;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --cyan: #06b6d4;
            --cyan-glow: rgba(6, 182, 212, 0.25);
            --emerald: #10b981;
            --amber: #f59e0b;
            --rose: #f43f5e;
            --purple: #a855f7;
            --blue: #3b82f6;
            --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: var(--bg-base);
            color: var(--text-main);
            font-family: var(--font-sans);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #030712; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #475569; }

        .btn-primary {
            background: linear-gradient(135deg, #0284c7, #06b6d4);
            color: #fff;
            font-weight: 700;
            border: 1px solid rgba(255,255,255,0.15);
            padding: 0.45rem 0.9rem;
            border-radius: 6px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.78rem;
            transition: all 0.15s ease;
        }
        .btn-primary:hover {
            box-shadow: 0 0 15px var(--cyan-glow);
            transform: translateY(-1px);
        }
        .btn-secondary {
            background: var(--bg-card);
            color: var(--text-main);
            border: 1px solid var(--border);
            padding: 0.45rem 0.85rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.78rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            transition: all 0.15s ease;
        }
        .btn-secondary:hover {
            border-color: var(--cyan);
            background: #1e293b;
        }
        .btn-secondary.active {
            background: rgba(6,182,212,0.15);
            border-color: var(--cyan);
            color: #38bdf8;
            font-weight: 700;
        }
        .btn-danger {
            background: rgba(244,63,94,0.15);
            border: 1px solid rgba(244,63,94,0.4);
            color: #fb7185;
            padding: 0.4rem 0.75rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .btn-danger:hover { background: rgba(244,63,94,0.3); }

        .card-badge {
            font-size: 0.7rem;
            font-weight: 700;
            font-family: var(--font-mono);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            background: rgba(15,23,42,0.8);
            border: 1px solid var(--border);
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
        }

        .stock-badge-in {
            display: inline-flex; align-items: center; gap: 0.3rem;
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid var(--emerald);
            color: var(--emerald);
            padding: 0.2rem 0.45rem;
            border-radius: 4px;
            font-size: 0.68rem;
            font-weight: 700;
        }
        .stock-badge-out {
            display: inline-flex; align-items: center; gap: 0.35rem;
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid var(--rose);
            color: #fca5a5;
            padding: 0.2rem 0.45rem;
            border-radius: 4px;
            font-size: 0.68rem;
            font-weight: 700;
        }
        .stock-badge-transit {
            display: inline-flex; align-items: center; gap: 0.3rem;
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid var(--amber);
            color: var(--amber);
            padding: 0.2rem 0.45rem;
            border-radius: 4px;
            font-size: 0.68rem;
            font-weight: 700;
        }
        .stock-dot-red {
            width: 8px; height: 8px; border-radius: 50%;
            background: #ef4444;
            display: inline-block;
            box-shadow: 0 0 8px #ef4444;
            animation: pulseRed 1.2s infinite;
        }
        @keyframes pulseRed {
            0% { transform: scale(0.9); opacity: 0.7; }
            50% { transform: scale(1.3); opacity: 1; box-shadow: 0 0 12px #ef4444; }
            100% { transform: scale(0.9); opacity: 0.7; }
        }

        .header {
            background: #0b1329;
            border-bottom: 1px solid var(--border);
            padding: 0.5rem 1rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            position: sticky;
            top: 0;
            z-index: 50;
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        .brand-logo {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            background: linear-gradient(135deg, var(--cyan), #3b82f6);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            box-shadow: 0 0 12px var(--cyan-glow);
        }
        .brand-title {
            font-size: 1rem;
            font-weight: 900;
            letter-spacing: -0.02em;
            color: #fff;
        }
        .brand-subtitle {
            font-size: 0.68rem;
            color: var(--cyan);
            font-family: var(--font-mono);
            font-weight: 700;
        }

        .perspective-bar {
            display: flex;
            align-items: center;
            background: #040711;
            padding: 0.2rem;
            border-radius: 8px;
            border: 1px solid var(--border);
            gap: 0.2rem;
        }
        .perspective-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 0.74rem;
            font-weight: 700;
            padding: 0.35rem 0.75rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .perspective-btn:hover { color: #fff; }
        .perspective-btn.active {
            background: var(--bg-card);
            color: var(--cyan);
            box-shadow: 0 2px 8px rgba(0,0,0,0.4);
            border: 1px solid rgba(6,182,212,0.3);
        }

        .hud-items {
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }
        .hud-pill {
            background: var(--bg-card);
            border: 1px solid var(--border);
            padding: 0.3rem 0.6rem;
            border-radius: 6px;
            font-size: 0.72rem;
            font-family: var(--font-mono);
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .nav-dock-container {
            background: #040711;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            position: sticky;
            top: 53px;
            z-index: 45;
            padding: 0 0.5rem;
        }
        .nav-dock {
            display: flex;
            align-items: center;
            overflow-x: auto;
            gap: 0.3rem;
            padding: 0.4rem 0.2rem;
            scrollbar-width: none;
            flex: 1;
        }
        .nav-dock::-webkit-scrollbar { display: none; }
        .nav-item {
            background: transparent;
            border: 1px solid transparent;
            color: var(--text-muted);
            padding: 0.4rem 0.75rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            cursor: pointer;
            white-space: nowrap;
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            transition: all 0.15s ease;
        }
        .nav-item:hover {
            color: #fff;
            background: rgba(255,255,255,0.04);
        }
        .nav-item.active {
            background: rgba(6,182,212,0.15);
            border-color: rgba(6,182,212,0.4);
            color: var(--cyan);
        }

        .app-main {
            flex: 1;
            padding: 1rem;
            max-width: 1720px;
            margin: 0 auto;
            width: 100%;
        }

        .tab-panel {
            display: none;
            animation: fadeIn 0.2s ease forwards;
        }
        .tab-panel.active { display: block; }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(3px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.25);
            position: relative;
        }
        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.8rem;
            border-bottom: 1px solid rgba(51,65,85,0.4);
            padding-bottom: 0.5rem;
        }
        .card-title {
            font-size: 0.95rem;
            font-weight: 800;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }
        .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
        .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
        .grid-split-40-60 { display: grid; grid-template-columns: 4fr 6fr; gap: 1rem; }
        .grid-split-60-40 { display: grid; grid-template-columns: 6fr 4fr; gap: 1rem; }

        @media (max-width: 1100px) {
            .grid-2, .grid-3, .grid-4, .grid-split-40-60, .grid-split-60-40 {
                grid-template-columns: 1fr;
            }
        }

        .project-card {
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.9rem;
            transition: all 0.2s ease;
        }
        .project-card-clickable {
            cursor: pointer;
        }
        .project-card-clickable:hover {
            border-color: var(--cyan);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(6,182,212,0.15);
        }

        .catalog-card {
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.85rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            transition: all 0.2s ease;
        }
        .catalog-card:hover {
            border-color: var(--cyan);
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.3);
        }

        .modal-backdrop {
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(2, 6, 23, 0.85);
            backdrop-filter: blur(4px);
            z-index: 999;
            align-items: center;
            justify-content: center;
            padding: 1rem;
        }
        .modal-backdrop.active { display: flex; }
        .modal-box {
            background: #0f172a;
            border: 1px solid var(--border-light);
            border-radius: 12px;
            width: 100%;
            max-width: 800px;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
            padding: 1.5rem;
            position: relative;
        }

        .input-group { margin-bottom: 0.75rem; }
        .input-label {
            display: block;
            font-size: 0.72rem;
            font-weight: 700;
            color: var(--text-muted);
            margin-bottom: 0.25rem;
        }
        .input-field {
            width: 100%;
            background: #040711;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 0.45rem 0.65rem;
            color: #fff;
            font-size: 0.78rem;
            outline: none;
            font-family: inherit;
        }
        .input-field:focus {
            border-color: var(--cyan);
            box-shadow: 0 0 10px var(--cyan-glow);
        }

        .obsidian-layout {
            display: grid;
            grid-template-columns: 1fr 340px;
            gap: 1rem;
            height: 600px;
        }
        @media (max-width: 950px) {
            .obsidian-layout { grid-template-columns: 1fr; height: auto; }
        }
        .obsidian-graph-container {
            background: #040711;
            border: 1px solid var(--border);
            border-radius: 8px;
            position: relative;
            overflow: hidden;
            height: 100%;
        }
        .obsidian-hud {
            position: absolute;
            top: 10px; left: 10px; right: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 10;
            flex-wrap: wrap;
            gap: 0.4rem;
        }
        .obsidian-drawer {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 0.8rem;
        }

        .tactical-wheel {
            position: fixed;
            bottom: 25px;
            right: 25px;
            z-index: 90;
        }
        .wheel-btn {
            width: 52px; height: 52px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--cyan), #3b82f6);
            border: 2px solid #fff;
            box-shadow: 0 0 20px var(--cyan-glow);
            color: #fff;
            font-size: 1.4rem;
            display: flex; align-items: center; justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .wheel-btn:hover { transform: scale(1.08) rotate(15deg); }
        .wheel-menu {
            display: none;
            position: absolute;
            bottom: 60px; right: 0;
            background: #0f172a;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 0.5rem;
            width: 220px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            flex-direction: column;
            gap: 0.3rem;
        }
        .wheel-menu.active { display: flex; }
        .wheel-item {
            background: transparent;
            border: none;
            color: var(--text-main);
            padding: 0.4rem 0.6rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            display: flex; align-items: center; gap: 0.5rem;
            cursor: pointer;
            text-align: left;
        }
        .wheel-item:hover { background: rgba(6,182,212,0.15); color: var(--cyan); }
    </style>
</head>
<body>

    <!-- APP HEADER -->
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
            <!-- Populated dynamically based on role -->
        </nav>
        <button class="btn-secondary" style="padding:0.25rem 0.5rem; margin-left:0.3rem;" onclick="scrollNav(200)">▶</button>
    </div>

    <!-- MAIN APP WRAPPER -->
    <main class="app-main">
""")
        print("Header & CSS written.")

if __name__ == '__main__':
    write_template()
