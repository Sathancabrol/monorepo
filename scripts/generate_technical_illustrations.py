# Generator for high quality technical SVG illustrations for BTP vehicles, tools and materials

def get_vehicle_svg(vehicle_type, name=""):
    v_type = vehicle_type.lower()
    
    if "pelle" in v_type or "excavat" in v_type or "320" in v_type:
        # Tracked Heavy Excavator (Pelle sur chenilles 24T)
        return """<svg viewBox="0 0 300 180" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
            <defs>
                <linearGradient id="yellowBody" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#fbbf24"/>
                    <stop offset="100%" stop-color="#d97706"/>
                </linearGradient>
                <linearGradient id="darkMetal" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#475569"/>
                    <stop offset="100%" stop-color="#1e293b"/>
                </linearGradient>
            </defs>
            <!-- Ground Line -->
            <line x1="10" y1="165" x2="290" y2="165" stroke="#334155" stroke-width="2"/>
            <!-- Tracks (Chenilles) -->
            <rect x="40" y="130" width="130" height="30" rx="15" fill="url(#darkMetal)" stroke="#0f172a" stroke-width="2"/>
            <circle cx="55" cy="145" r="11" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
            <circle cx="85" cy="145" r="11" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
            <circle cx="115" cy="145" r="11" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
            <circle cx="145" cy="145" r="11" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
            <line x1="40" y1="130" x2="170" y2="130" stroke="#94a3b8" stroke-dasharray="4,4"/>
            <line x1="40" y1="160" x2="170" y2="160" stroke="#94a3b8" stroke-dasharray="4,4"/>
            <!-- Turret / Chassis -->
            <rect x="50" y="95" width="100" height="36" rx="6" fill="url(#yellowBody)" stroke="#b45309" stroke-width="2"/>
            <rect x="52" y="100" width="30" height="26" rx="4" fill="#1e293b"/>
            <!-- Counterweight -->
            <path d="M 50 95 L 35 105 L 35 125 L 50 131 Z" fill="#b45309"/>
            <!-- Operator Cabin -->
            <path d="M 115 65 L 145 65 L 145 95 L 115 95 Z" fill="#0284c7" fill-opacity="0.7" stroke="#0369a1" stroke-width="2"/>
            <rect x="110" y="60" width="40" height="38" rx="4" fill="none" stroke="#d97706" stroke-width="3"/>
            <circle cx="130" cy="78" r="5" fill="#f8fafc"/>
            <!-- Main Boom (Flèche principale) -->
            <path d="M 140 100 L 195 40 L 210 50 L 150 110 Z" fill="url(#yellowBody)" stroke="#b45309" stroke-width="2"/>
            <circle cx="145" cy="105" r="4" fill="#1e293b"/>
            <!-- Hydraulic Cylinder (Vérin de flèche) -->
            <line x1="148" y1="112" x2="180" y2="75" stroke="#94a3b8" stroke-width="5"/>
            <line x1="180" y1="75" x2="195" y2="55" stroke="#cbd5e1" stroke-width="3"/>
            <!-- Stick / Arm (Balancier) -->
            <path d="M 200 45 L 250 105 L 240 112 L 192 52 Z" fill="url(#yellowBody)" stroke="#b45309" stroke-width="2"/>
            <circle cx="198" cy="48" r="4" fill="#1e293b"/>
            <!-- Bucket Cylinder (Vérin de godet) -->
            <line x1="195" y1="58" x2="225" y2="92" stroke="#94a3b8" stroke-width="4"/>
            <!-- Digging Bucket (Godet rétro à dents) -->
            <path d="M 245 108 L 275 125 L 265 155 L 235 145 Z" fill="#334155" stroke="#1e293b" stroke-width="2"/>
            <!-- Bucket Teeth (Dents de godet) -->
            <polygon points="275,125 285,130 278,135" fill="#f59e0b"/>
            <polygon points="272,135 282,140 274,145" fill="#f59e0b"/>
            <polygon points="268,145 278,150 265,155" fill="#f59e0b"/>
            <circle cx="245" cy="110" r="3" fill="#fbbf24"/>
            <!-- Safety AIPR & Beacon Light -->
            <circle cx="120" cy="56" r="3" fill="#ef4444"/>
            <text x="60" y="118" fill="#1e293b" font-family="system-ui" font-weight="900" font-size="11">CAT 320 GC</text>
            <text x="15" y="25" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700">Pelle sur Chenilles 24T</text>
        </svg>"""
        
    elif "cylindre" in v_type or "compacteur" in v_type or "bomag" in v_type:
        # Vibratory Roller Compactor (Cylindre tandem vibrant)
        return """<svg viewBox="0 0 300 180" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
            <defs>
                <linearGradient id="bomagYellow" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#facc15"/>
                    <stop offset="100%" stop-color="#ca8a04"/>
                </linearGradient>
                <linearGradient id="drumSteel" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#94a3b8"/>
                    <stop offset="50%" stop-color="#475569"/>
                    <stop offset="100%" stop-color="#1e293b"/>
                </linearGradient>
            </defs>
            <line x1="10" y1="165" x2="290" y2="165" stroke="#334155" stroke-width="2"/>
            <!-- Front Steel Drum (Bille avant) -->
            <circle cx="75" cy="130" r="32" fill="url(#drumSteel)" stroke="#0f172a" stroke-width="3"/>
            <circle cx="75" cy="130" r="14" fill="#334155" stroke="#cbd5e1" stroke-width="2"/>
            <!-- Rear Steel Drum (Bille arrière) -->
            <circle cx="215" cy="130" r="32" fill="url(#drumSteel)" stroke="#0f172a" stroke-width="3"/>
            <circle cx="215" cy="130" r="14" fill="#334155" stroke="#cbd5e1" stroke-width="2"/>
            <!-- Articulated Chassis Frame -->
            <path d="M 75 130 L 110 115 L 140 115 L 140 135 L 75 130 Z" fill="#334155"/>
            <path d="M 145 115 L 215 115 L 215 135 L 145 135 Z" fill="#334155"/>
            <circle cx="142" cy="125" r="5" fill="#facc15"/> <!-- Articulation pivot -->
            <!-- Engine Body -->
            <rect x="150" y="85" width="85" height="32" rx="4" fill="url(#bomagYellow)" stroke="#a16207" stroke-width="2"/>
            <rect x="195" y="90" width="35" height="15" fill="#1e293b" rx="2"/>
            <!-- Exhaust Pipe -->
            <line x1="220" y1="85" x2="220" y2="65" stroke="#475569" stroke-width="3"/>
            <!-- Operator Platform & ROPS Canopy -->
            <rect x="110" y="70" width="45" height="45" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>
            <path d="M 105 40 L 165 40 L 160 70 L 110 70 Z" fill="none" stroke="#facc15" stroke-width="3"/>
            <rect x="100" y="36" width="70" height="6" rx="2" fill="#ca8a04"/>
            <!-- Steering wheel & operator -->
            <circle cx="125" cy="60" r="5" fill="#f8fafc"/>
            <line x1="130" y1="68" x2="135" y2="78" stroke="#cbd5e1" stroke-width="2"/>
            <!-- Beacon light -->
            <circle cx="135" cy="32" r="3" fill="#f97316"/>
            <text x="155" y="105" fill="#1e293b" font-family="system-ui" font-weight="900" font-size="10">BOMAG BW 120</text>
            <text x="15" y="25" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700">Compacteur Tandem Vibrant</text>
        </svg>"""

    elif "camion" in v_type or "8x4" in v_type or "scania" in v_type or "volvo" in v_type:
        # Heavy Tipper Dump Truck 8x4 (Camion Benne 8x4)
        return """<svg viewBox="0 0 300 180" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
            <defs>
                <linearGradient id="scaniaBlue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#0284c7"/>
                    <stop offset="100%" stop-color="#0369a1"/>
                </linearGradient>
                <linearGradient id="tipperSilver" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#cbd5e1"/>
                    <stop offset="100%" stop-color="#64748b"/>
                </linearGradient>
            </defs>
            <line x1="10" y1="165" x2="290" y2="165" stroke="#334155" stroke-width="2"/>
            <!-- 8x4 Chassis Beam -->
            <rect x="30" y="130" width="235" height="12" fill="#1e293b" stroke="#0f172a"/>
            <!-- 4 Axles Wheels (4 essieux) -->
            <!-- Front Steering Axle 1 & 2 -->
            <circle cx="50" cy="146" r="16" fill="#0f172a" stroke="#475569" stroke-width="3"/>
            <circle cx="50" cy="146" r="6" fill="#94a3b8"/>
            <circle cx="95" cy="146" r="16" fill="#0f172a" stroke="#475569" stroke-width="3"/>
            <circle cx="95" cy="146" r="6" fill="#94a3b8"/>
            <!-- Rear Drive Axle 3 & 4 (Jumelés) -->
            <circle cx="195" cy="146" r="16" fill="#0f172a" stroke="#475569" stroke-width="3"/>
            <circle cx="195" cy="146" r="6" fill="#94a3b8"/>
            <circle cx="235" cy="146" r="16" fill="#0f172a" stroke="#475569" stroke-width="3"/>
            <circle cx="235" cy="146" r="6" fill="#94a3b8"/>
            <!-- Cab (Cabine Scania) -->
            <path d="M 30 130 L 30 70 L 70 65 L 85 90 L 85 130 Z" fill="url(#scaniaBlue)" stroke="#075985" stroke-width="2"/>
            <!-- Windshield & Side Window -->
            <path d="M 35 73 L 65 69 L 78 90 L 35 90 Z" fill="#38bdf8" fill-opacity="0.6" stroke="#0284c7"/>
            <!-- Headlights & Grille -->
            <rect x="26" y="112" width="6" height="12" fill="#facc15" rx="2"/>
            <line x1="30" y1="100" x2="30" y2="125" stroke="#e2e8f0" stroke-width="2"/>
            <!-- Tipper Hydraulic Cylinder (Vérin de benne) -->
            <line x1="95" y1="125" x2="110" y2="95" stroke="#cbd5e1" stroke-width="6"/>
            <!-- Heavy Tipper Body (Benne enrochement acier HARDOX) -->
            <path d="M 90 90 L 255 75 L 260 130 L 90 130 Z" fill="url(#tipperSilver)" stroke="#475569" stroke-width="2"/>
            <!-- Reinforcement Ribs on Tipper -->
            <line x1="125" y1="87" x2="125" y2="130" stroke="#475569" stroke-width="2"/>
            <line x1="165" y1="83" x2="165" y2="130" stroke="#475569" stroke-width="2"/>
            <line x1="205" y1="79" x2="205" y2="130" stroke="#475569" stroke-width="2"/>
            <line x1="245" y1="76" x2="245" y2="130" stroke="#475569" stroke-width="2"/>
            <!-- Orange Flashing Beacon -->
            <circle cx="55" cy="62" r="3" fill="#f97316"/>
            <text x="110" y="115" fill="#0f172a" font-family="system-ui" font-weight="900" font-size="11">SCANIA 8x4 HARDOX 32T</text>
            <text x="15" y="25" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700">Porteur 8x4 Bi-Benne</text>
        </svg>"""

    elif "tractopelle" in v_type or "jcb" in v_type or "4cx" in v_type:
        # Backhoe Loader (Tractopelle Mixte 4CX)
        return """<svg viewBox="0 0 300 180" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
            <line x1="10" y1="165" x2="290" y2="165" stroke="#334155" stroke-width="2"/>
            <!-- 4 Equal Wheels -->
            <circle cx="75" cy="138" r="24" fill="#0f172a" stroke="#f59e0b" stroke-width="3"/>
            <circle cx="75" cy="138" r="8" fill="#f59e0b"/>
            <circle cx="165" cy="138" r="24" fill="#0f172a" stroke="#f59e0b" stroke-width="3"/>
            <circle cx="165" cy="138" r="8" fill="#f59e0b"/>
            <!-- Central Chassis & Cab -->
            <rect x="95" y="90" width="60" height="45" fill="#f59e0b" rx="4"/>
            <path d="M 105 60 L 145 60 L 155 90 L 95 90 Z" fill="#0284c7" fill-opacity="0.6" stroke="#f59e0b" stroke-width="2"/>
            <!-- Front Loader Arms & 4-in-1 Bucket (Godet chargeur avant) -->
            <path d="M 120 105 L 45 110 L 25 130 Z" stroke="#f59e0b" stroke-width="6" fill="none"/>
            <path d="M 15 125 L 35 125 L 30 155 L 10 155 Z" fill="#334155" stroke="#1e293b" stroke-width="2"/>
            <!-- Rear Backhoe Arm (Rétro arrière) -->
            <path d="M 175 115 L 215 70 L 255 115 Z" stroke="#f59e0b" stroke-width="6" fill="none"/>
            <path d="M 255 115 L 275 135 L 260 145 Z" fill="#334155" stroke="#1e293b" stroke-width="2"/>
            <circle cx="125" cy="55" r="3" fill="#f97316"/>
            <text x="102" y="115" fill="#0f172a" font-family="system-ui" font-weight="900" font-size="10">JCB 4CX</text>
            <text x="15" y="25" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700">Tractopelle Mixte 4CX</text>
        </svg>"""

    elif "drone" in v_type or "matrice" in v_type or "dji" in v_type:
        # Topography LiDAR RTK Drone (DJI Matrice 350 RTK)
        return """<svg viewBox="0 0 300 180" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
            <!-- Drone Central Body -->
            <ellipse cx="150" cy="85" rx="35" ry="18" fill="#1e293b" stroke="#06b6d4" stroke-width="2"/>
            <!-- GNSS RTK Antennas -->
            <circle cx="135" cy="65" r="5" fill="#f8fafc" stroke="#06b6d4"/>
            <circle cx="165" cy="65" r="5" fill="#f8fafc" stroke="#06b6d4"/>
            <!-- 4 Carbon Arms -->
            <line x1="125" y1="80" x2="60" y2="55" stroke="#0f172a" stroke-width="6"/>
            <line x1="175" y1="80" x2="240" y2="55" stroke="#0f172a" stroke-width="6"/>
            <line x1="130" y1="90" x2="70" y2="120" stroke="#0f172a" stroke-width="6"/>
            <line x1="170" y1="90" x2="230" y2="120" stroke="#0f172a" stroke-width="6"/>
            <!-- 4 Rotors & Spinning Propellers -->
            <ellipse cx="60" cy="55" rx="35" ry="6" fill="#38bdf8" fill-opacity="0.4" stroke="#0284c7"/>
            <ellipse cx="240" cy="55" rx="35" ry="6" fill="#38bdf8" fill-opacity="0.4" stroke="#0284c7"/>
            <ellipse cx="70" cy="120" rx="35" ry="6" fill="#38bdf8" fill-opacity="0.4" stroke="#0284c7"/>
            <ellipse cx="230" cy="120" rx="35" ry="6" fill="#38bdf8" fill-opacity="0.4" stroke="#0284c7"/>
            <!-- LiDAR Sensor & Gimbal Camera -->
            <rect x="140" y="102" width="20" height="18" fill="#0f172a" rx="3" stroke="#10b981" stroke-width="2"/>
            <circle cx="150" cy="111" r="5" fill="#10b981"/>
            <!-- LiDAR Laser Cone Simulation -->
            <polygon points="150,120 70,175 230,175" fill="#10b981" fill-opacity="0.15"/>
            <line x1="150" y1="120" x2="70" y2="175" stroke="#10b981" stroke-dasharray="3,3"/>
            <line x1="150" y1="120" x2="230" y2="175" stroke="#10b981" stroke-dasharray="3,3"/>
            <text x="15" y="25" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700">Drone Topographique LiDAR RTK</text>
        </svg>"""

    else:
        # Default High-Tech Construction Machine
        return """<svg viewBox="0 0 300 180" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
            <line x1="10" y1="165" x2="290" y2="165" stroke="#334155" stroke-width="2"/>
            <rect x="60" y="90" width="180" height="50" rx="6" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
            <circle cx="100" cy="148" r="16" fill="#0f172a" stroke="#94a3b8" stroke-width="3"/>
            <circle cx="200" cy="148" r="16" fill="#0f172a" stroke="#94a3b8" stroke-width="3"/>
            <rect x="110" y="60" width="80" height="30" fill="#1e293b" stroke="#3b82f6" stroke-width="2"/>
            <text x="15" y="25" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700">Matériel Professionnel TP</text>
        </svg>"""

def get_tool_material_svg(item_id, item_name=""):
    i_id = item_id.lower()
    i_name = item_name.lower()

    if "bordure" in i_id or "bordure" in i_name or "mat_01" in i_id or "mat_02" in i_id:
        # Concrete Kerb T2 / A2 (Bordure Béton)
        return """<svg viewBox="0 0 280 160" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
            <!-- Isometric Concrete Kerb T2 Block -->
            <polygon points="50,110 190,110 240,60 100,60" fill="#94a3b8" stroke="#cbd5e1" stroke-width="2"/>
            <polygon points="50,110 190,110 190,145 50,145" fill="#64748b" stroke="#334155" stroke-width="2"/>
            <polygon points="190,110 240,60 240,95 190,145" fill="#475569" stroke="#1e293b" stroke-width="2"/>
            <!-- Chamfer / Chanfrein NF EN 1340 -->
            <polygon points="50,110 70,95 210,95 190,110" fill="#cbd5e1"/>
            <!-- Dimension callouts -->
            <line x1="50" y1="152" x2="190" y2="152" stroke="#06b6d4" stroke-width="1.5"/>
            <text x="100" y="157" fill="#06b6d4" font-family="JetBrains Mono" font-size="9">L = 100 cm</text>
            <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Bordure Béton Type T2 NF</text>
        </svg>"""

    elif "tampon" in i_id or "mat_03" in i_id or "fonte" in i_id:
        # Ductile Iron Manhole Cover D400 (Tampon PAM REXEL D400)
        return """<svg viewBox="0 0 280 160" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
            <!-- Square Frame -->
            <rect x="50" y="20" width="180" height="120" rx="8" fill="#1e293b" stroke="#475569" stroke-width="3"/>
            <!-- Circular Manhole Cover -->
            <circle cx="140" cy="80" r="50" fill="#0f172a" stroke="#94a3b8" stroke-width="3"/>
            <!-- Anti-slip waffle relief pattern -->
            <circle cx="140" cy="80" r="42" fill="none" stroke="#64748b" stroke-width="2" stroke-dasharray="6,4"/>
            <circle cx="140" cy="80" r="30" fill="none" stroke="#64748b" stroke-width="2" stroke-dasharray="4,4"/>
            <text x="120" y="83" fill="#facc15" font-family="system-ui" font-weight="900" font-size="10">D 400</text>
            <text x="110" y="96" fill="#94a3b8" font-family="JetBrains Mono" font-size="7">PAM NF EN 124</text>
            <text x="15" y="15" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Tampon Fonte D400 400kN</text>
        </svg>"""

    elif "tuyau" in i_id or "fonte" in i_name or "mat_05" in i_id:
        # Ductile Iron Pipe DN400 Integral (Tuyau Fonte Assainissement)
        return """<svg viewBox="0 0 280 160" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
            <!-- Pipe Barrel -->
            <rect x="60" y="55" width="180" height="50" rx="4" fill="#334155" stroke="#0284c7" stroke-width="2"/>
            <!-- Socket End (Emboîture) -->
            <rect x="30" y="48" width="35" height="64" rx="6" fill="#1e293b" stroke="#0284c7" stroke-width="3"/>
            <line x1="50" y1="48" x2="50" y2="112" stroke="#ef4444" stroke-width="3"/> <!-- Gasket joint -->
            <!-- Spigot End (Bout uni) -->
            <line x1="240" y1="55" x2="240" y2="105" stroke="#94a3b8" stroke-width="3"/>
            <text x="80" y="85" fill="#38bdf8" font-family="JetBrains Mono" font-size="10" font-weight="800">FONTE DUCTILE DN 400</text>
            <text x="80" y="97" fill="#94a3b8" font-family="JetBrains Mono" font-size="8">Zinc-Alu 400g/m² | Fascicule 70</text>
            <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Tuyau Assainissement Fonte</text>
        </svg>"""

    elif "gaz" in i_id or "pehd" in i_name or "mat_07" in i_id:
        # PEHD Gas Pipe with Yellow Stripe (Tube PEHD Gaz)
        return """<svg viewBox="0 0 280 160" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
            <rect x="30" y="55" width="220" height="50" rx="6" fill="#0f172a" stroke="#eab308" stroke-width="2"/>
            <!-- Yellow Warning Co-extruded Stripe -->
            <rect x="30" y="75" width="220" height="10" fill="#eab308"/>
            <text x="45" y="70" fill="#facc15" font-family="JetBrains Mono" font-size="9" font-weight="800">⚡ GAZ MPB 4 BARS PE100 SDR11 Ø110</text>
            <text x="45" y="98" fill="#94a3b8" font-family="JetBrains Mono" font-size="8">NF EN 1555 / NF 136 GrDF</text>
            <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Tube PEHD Gaz Haute Sécurité</text>
        </svg>"""

    elif "laser" in i_id or "piper" in i_name or "topo" in i_id:
        # Pipe Laser (Laser de canalisation Piper 100)
        return """<svg viewBox="0 0 280 160" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
            <!-- Cast Aluminum Cylindrical Body -->
            <rect x="40" y="55" width="130" height="50" rx="10" fill="#dc2626" stroke="#991b1b" stroke-width="2"/>
            <circle cx="170" cy="80" r="25" fill="#1e293b" stroke="#dc2626" stroke-width="3"/>
            <!-- Green Laser Beam Emission -->
            <circle cx="170" cy="80" r="8" fill="#10b981"/>
            <polygon points="175,80 260,60 260,100" fill="#10b981" fill-opacity="0.3"/>
            <line x1="175" y1="80" x2="260" y2="80" stroke="#10b981" stroke-width="2"/>
            <!-- Digital Display for Grade % -->
            <rect x="65" y="65" width="45" height="20" fill="#022c22" stroke="#10b981" rx="3"/>
            <text x="70" y="79" fill="#10b981" font-family="JetBrains Mono" font-size="10" font-weight="900">+ 1.25%</text>
            <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Laser Canalisateur Piper 100</text>
        </svg>"""

    elif "scie" in i_id or "decoupeuse" in i_id or "stihl" in i_name:
        # Cut-off saw with diamond blade (Découpeuse Stihl TS420)
        return """<svg viewBox="0 0 280 160" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
            <!-- Engine Body Stihl Orange -->
            <rect x="50" y="65" width="90" height="40" rx="6" fill="#ea580c" stroke="#c2410c" stroke-width="2"/>
            <!-- Top Handle & Pull Starter -->
            <path d="M 60 65 L 60 45 L 120 45 L 120 65" fill="none" stroke="#1e293b" stroke-width="5"/>
            <!-- Diamond Blade Guard & Disc -->
            <circle cx="195" cy="85" r="40" fill="#475569" stroke="#94a3b8" stroke-width="2"/>
            <circle cx="195" cy="85" r="12" fill="#0f172a" stroke="#cbd5e1" stroke-width="2"/>
            <path d="M 140 60 L 195 45 L 235 85 L 140 85 Z" fill="#ea580c" stroke="#c2410c"/>
            <text x="60" y="90" fill="#f8fafc" font-family="system-ui" font-weight="900" font-size="10">TS 420 350mm</text>
            <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Découpeuse Thermique Diamant</text>
        </svg>"""

    elif "epi" in i_id or "securite" in i_id or "pack" in i_name:
        # Complete PPE Kit (Pack EPI Chantier)
        return """<svg viewBox="0 0 280 160" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
            <!-- Safety Helmet NF EN 397 -->
            <path d="M 50 65 C 50 35 110 35 110 65 Z" fill="#facc15" stroke="#ca8a04" stroke-width="2"/>
            <line x1="45" y1="65" x2="115" y2="65" stroke="#ca8a04" stroke-width="3"/>
            <!-- Chinstrap (Jugulaire) -->
            <path d="M 55 65 L 80 85 L 105 65" fill="none" stroke="#1e293b" stroke-width="2"/>
            <!-- High-Vis Vest Class 3 -->
            <path d="M 140 45 L 210 45 L 225 115 L 125 115 Z" fill="#facc15" stroke="#eab308" stroke-width="2"/>
            <!-- Reflective Silver Stripes -->
            <line x1="135" y1="75" x2="215" y2="75" stroke="#f8fafc" stroke-width="6"/>
            <line x1="130" y1="95" x2="220" y2="95" stroke="#f8fafc" stroke-width="6"/>
            <line x1="160" y1="45" x2="160" y2="115" stroke="#f8fafc" stroke-width="6"/>
            <line x1="190" y1="45" x2="190" y2="115" stroke="#f8fafc" stroke-width="6"/>
            <!-- S3 Safety Shoes -->
            <rect x="60" y="115" width="40" height="20" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
            <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Pack EPI NF EN ISO 20471</text>
        </svg>"""

    elif "pince" in i_id or "massette" in i_id or "outil" in i_id:
        # Manual Kerb Clamp / Masonry Sledgehammer
        return """<svg viewBox="0 0 280 160" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
            <!-- Sledgehammer Head (Tête de massette) -->
            <rect x="50" y="55" width="55" height="30" rx="3" fill="#334155" stroke="#94a3b8" stroke-width="2"/>
            <line x1="77" y1="55" x2="77" y2="145" stroke="#d97706" stroke-width="8"/>
            <line x1="77" y1="120" x2="77" y2="145" stroke="#1e293b" stroke-width="8"/>
            <!-- Scissor Tongs (Pince à bordures) -->
            <path d="M 150 50 L 190 100 L 230 50" fill="none" stroke="#f59e0b" stroke-width="6"/>
            <path d="M 170 100 L 160 140" fill="none" stroke="#475569" stroke-width="6"/>
            <path d="M 210 100 L 220 140" fill="none" stroke="#475569" stroke-width="6"/>
            <circle cx="190" cy="100" r="5" fill="#f8fafc"/>
            <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Outillage Manuel Chantier</text>
        </svg>"""

    else:
        # Generic Tool / Material Illustration
        return """<svg viewBox="0 0 280 160" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#090d16; border-radius:8px;">
            <rect x="50" y="45" width="180" height="70" rx="8" fill="#1e293b" stroke="#06b6d4" stroke-width="2"/>
            <circle cx="140" cy="80" r="22" fill="#06b6d4" fill-opacity="0.2" stroke="#06b6d4" stroke-width="2"/>
            <text x="140" y="85" fill="#f8fafc" font-size="16" text-anchor="middle">📦</text>
            <text x="15" y="20" fill="#38bdf8" font-family="JetBrains Mono" font-size="9" font-weight="700">Fourniture / Équipement TP</text>
        </svg>"""

print("Technical illustrations module ready.")
