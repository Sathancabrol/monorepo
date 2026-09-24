# -*- coding: utf-8 -*-
"""
Patch section_head_and_styles.py to include Leaflet CSS/JS and styles for Enrobes 2D simulation
"""

with open('scripts/section_head_and_styles.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add Leaflet CDN tags in <head>
old_head = r'''    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap" rel="stylesheet">'''

new_head = r'''    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>'''

if old_head in text:
    text = text.replace(old_head, new_head)
    print("Leaflet CDN added to section_head_and_styles.py")
else:
    print("Warning: old_head not found in section_head_and_styles.py")

# 2. Add extra CSS for Leaflet and Enrobes 2D
extra_css = r'''
        /* LEAFLET CUSTOM DARK STYLING */
        .leaflet-container {
            background: #070a14 !important;
            font-family: var(--font-sans) !important;
        }
        .leaflet-popup-content-wrapper {
            background: #0f172a !important;
            color: #f8fafc !important;
            border: 1px solid rgba(56, 189, 248, 0.4) !important;
            border-radius: 8px !important;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5) !important;
        }
        .leaflet-popup-tip {
            background: #0f172a !important;
            border: 1px solid rgba(56, 189, 248, 0.4) !important;
        }
        .leaflet-control-zoom a {
            background: #1e293b !important;
            color: #38bdf8 !important;
            border-color: #334155 !important;
        }
        .leaflet-control-zoom a:hover {
            background: #334155 !important;
            color: #ffffff !important;
        }

        /* 2D ENROBES SIMULATION STYLES */
        .enrobes-stat-card {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(51, 65, 85, 0.8);
            border-radius: 6px;
            padding: 0.6rem;
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        .enrobes-stat-title {
            font-size: 0.7rem;
            color: #94a3b8;
            font-weight: 700;
            text-transform: uppercase;
        }
        .enrobes-stat-val {
            font-size: 1.05rem;
            font-weight: 800;
            font-family: var(--font-mono);
        }
        .enrobes-pass-legend-item {
            display: flex;
            align-items: center;
            gap: 4px;
            font-size: 0.72rem;
            color: #cbd5e1;
        }
        .enrobes-pass-color-box {
            width: 14px;
            height: 14px;
            border-radius: 3px;
            border: 1px solid rgba(255,255,255,0.2);
        }
'''

pos_style_end = text.find('</style>')
if pos_style_end != -1:
    text = text[:pos_style_end] + extra_css + "\n    " + text[pos_style_end:]
    print("Leaflet & Enrobes 2D styles added!")

with open('scripts/section_head_and_styles.py', 'w', encoding='utf-8') as f:
    f.write(text)
