# -*- coding: utf-8 -*-
"""
Implement full GIS, Satellite, OpenStreetMap, Cadastre, Street View,
Measurement tools, and DICT networks in section_js_part2.py
"""

watchtower_maps_code = r'''
    // ==========================================
    // WATCHTOWER GIS / SATELLITE & MAPS ENGINE
    // ==========================================
    let watchtowerMapLayer = 'satellite'; // 'satellite', 'osm', 'cadastre', 'hybride', 'relief'
    let watchtowerActiveTool = 'pan'; // 'pan', 'measure_dist', 'measure_area', 'profile', 'streetview'
    let watchtowerMapZoom = 1.0;
    let watchtowerMapPanX = 0;
    let watchtowerMapPanY = 0;
    let isDraggingWatchtowerMap = false;
    let lastWtMouseX = 0, lastWtMouseY = 0;
    let watchtowerRotationAngle = 0; // degrees

    // Measurement points storage
    let wtMeasurePoints = [];
    let wtMeasurePoly = [];
    let wtProfilePoints = [];

    // POI Geo registry
    const watchtowerPOIs = {
        'sete_quai': { name: "Sète - Quai de la République", lat: 43.4072, lon: 3.6961, z: 14.8, desc: "Assainissement BA Ø400 & Réfection de Chaussée", type: "chantier", pk: "PK 0+240" },
        'ales_giratoire': { name: "Alès - Giratoire RD906", lat: 44.1280, lon: 4.0830, z: 135.2, desc: "Création de Giratoire 4 Branches & Bordures I1/I2", type: "chantier", pk: "PK 12+800" },
        'beziers_zac': { name: "Béziers - ZAC Ouest", lat: 43.3440, lon: 3.2160, z: 28.5, desc: "Plateforme VRD Commerciale & Bassin Ouvert", type: "chantier", pk: "Lot A3" },
        'frontignan_rd612': { name: "Frontignan - Piste RD612", lat: 43.4470, lon: 3.7550, z: 4.2, desc: "Piste Cyclable Littorale & Bordures P2", type: "chantier", pk: "PK 4+150" },
        'meze_port': { name: "Mèze - Port des Nacres", lat: 43.4280, lon: 3.5960, z: 2.1, desc: "Collecteur Eaux Pluviales Ø600 & Enrobés", type: "chantier", pk: "Bassin Sud" },
        'agde_rn112': { name: "Agde - Entrée Ville RN112", lat: 43.3100, lon: 3.4750, z: 8.4, desc: "Renforcement Structurel GB3 & BBSG 0/10", type: "chantier", pk: "PK 22+000" },
        'depot_sete': { name: "Dépôt & Base Logistique Sète", lat: 43.4150, lon: 3.6800, z: 12.0, desc: "Parc 300m² & Atelier Matériel 120m²", type: "depot", pk: "Site Central" },
        'centrale_pinet': { name: "Centrale Enrobés Pinet", lat: 43.4050, lon: 3.5100, z: 45.0, desc: "Centrale de Fabrication BBSG / GB3", type: "fournisseur", pk: "Z.A. Pinet" },
        'carriere_loupian': { name: "Carrière Calcaire Loupian", lat: 43.4500, lon: 3.6150, z: 82.0, desc: "Extraction GNT 0/31.5 & Concassé Alluvionnaire", type: "carriere", pk: "Carrière Est" },
        'isdi_villeveyrac': { name: "Centre Recyclage ISDI Villeveyrac", lat: 43.5000, lon: 3.6050, z: 95.0, desc: "Mise en Décharge Déblai Inerte & Concassage", type: "isdi", pk: "Site Agréé" }
    };

    let currentWatchtowerPOI = 'sete_quai';

    // Street view 360 state
    let isStreetViewOpen = false;
    let streetViewRotAngle = 0; // horizontal pan
    let isDraggingStreetView = false;
    let lastSvMouseX = 0;

    function setSimulatorViewMode(mode) {
        simulatorViewMode = mode;
        document.querySelectorAll('.sim-view-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('btn-sim-' + mode)?.classList.add('active');

        const mapsCanvas = document.getElementById('watchtower-maps-canvas');
        const view3dCanvas = document.getElementById('watchtower-3d-canvas');
        const radarCanvas = document.getElementById('watchtower-radar-canvas');
        const mapsToolbar = document.getElementById('watchtower-maps-toolbar');
        const dictBar = document.getElementById('watchtower-dict-bar');

        if (mode === 'maps') {
            if (mapsCanvas) mapsCanvas.style.display = 'block';
            if (view3dCanvas) view3dCanvas.style.display = 'none';
            if (radarCanvas) radarCanvas.style.display = 'none';
            if (mapsToolbar) mapsToolbar.style.display = 'flex';
            if (dictBar) dictBar.style.display = 'flex';
            setTimeout(initWatchtowerMaps, 50);
        } else if (mode === '3d') {
            if (mapsCanvas) mapsCanvas.style.display = 'none';
            if (view3dCanvas) view3dCanvas.style.display = 'block';
            if (radarCanvas) radarCanvas.style.display = 'none';
            if (mapsToolbar) mapsToolbar.style.display = 'none';
            if (dictBar) dictBar.style.display = 'none';
            setTimeout(() => {
                init3DCanvas();
                drawStepVisual(activeScenarioStepIdx);
            }, 50);
        } else if (mode === 'radar') {
            if (mapsCanvas) mapsCanvas.style.display = 'none';
            if (view3dCanvas) view3dCanvas.style.display = 'none';
            if (radarCanvas) radarCanvas.style.display = 'block';
            if (mapsToolbar) mapsToolbar.style.display = 'none';
            if (dictBar) dictBar.style.display = 'none';
            setTimeout(initWatchtowerRadar, 50);
        } else if (mode === 'standard') {
            // Split mode
            if (mapsCanvas) {
                mapsCanvas.style.display = 'block';
                mapsCanvas.style.width = '50%';
            }
            if (view3dCanvas) {
                view3dCanvas.style.display = 'block';
                view3dCanvas.style.left = '50%';
                view3dCanvas.style.width = '50%';
            }
            if (radarCanvas) radarCanvas.style.display = 'none';
            if (mapsToolbar) mapsToolbar.style.display = 'flex';
            if (dictBar) dictBar.style.display = 'flex';
            setTimeout(() => {
                initWatchtowerMaps();
                init3DCanvas();
                drawStepVisual(activeScenarioStepIdx);
            }, 50);
        }
    }

    function setWatchtowerMapLayer(layer) {
        watchtowerMapLayer = layer;
        document.querySelectorAll('.map-layer-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('btn-layer-' + layer)?.classList.add('active');
        renderWatchtowerMaps();
        logCockpit(`Watchtower Cartographie : Couche ${layer.toUpperCase()} activée.`, 'info');
    }

    function setWatchtowerTool(tool) {
        watchtowerActiveTool = tool;
        document.querySelectorAll('.map-tool-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('btn-tool-' + tool.replace('_', '-'))?.classList.add('active');

        const readout = document.getElementById('watchtower-measurement-readout');
        if (tool === 'pan') {
            if (readout) readout.textContent = "Outil : Navigation libre (Glisser pour déplacer, molette pour zoomer)";
        } else if (tool === 'measure_dist') {
            if (readout) readout.textContent = "Outil Règle : Cliquez sur la carte pour mesurer la distance linéaire";
        } else if (tool === 'measure_area') {
            if (readout) readout.textContent = "Outil Polygone : Cliquez sur les sommets pour mesurer la surface";
        } else if (tool === 'profile') {
            if (readout) readout.textContent = "Outil Profil : Cliquez sur le point amont puis le point aval";
        } else if (tool === 'streetview') {
            if (readout) readout.textContent = "Street View : Cliquez sur un point de voirie pour ouvrir la caméra 360°";
        }
    }

    function clearWatchtowerMeasurements() {
        wtMeasurePoints = [];
        wtMeasurePoly = [];
        wtProfilePoints = [];
        const readout = document.getElementById('watchtower-measurement-readout');
        if (readout) readout.textContent = "Mesures réinitialisées.";
        renderWatchtowerMaps();
    }

    function flyToWatchtowerPOI(poiKey) {
        const poi = watchtowerPOIs[poiKey];
        if (!poi) return;
        currentWatchtowerPOI = poiKey;
        watchtowerMapPanX = 0;
        watchtowerMapPanY = 0;
        watchtowerMapZoom = 1.35;
        renderWatchtowerMaps();
        logCockpit(`Watchtower Fly-To : Navigation vers ${poi.name} (${poi.pk}).`, 'ok');
    }

    function zoomWatchtowerMap(factor) {
        watchtowerMapZoom = Math.max(0.5, Math.min(4.0, watchtowerMapZoom * factor));
        renderWatchtowerMaps();
    }

    function resetWatchtowerNorth() {
        watchtowerRotationAngle = 0;
        watchtowerMapPanX = 0;
        watchtowerMapPanY = 0;
        renderWatchtowerMaps();
    }

    function initWatchtowerMaps() {
        const canvas = document.getElementById('watchtower-maps-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const w = canvas.parentElement.clientWidth || 800;
        const h = canvas.parentElement.clientHeight || 500;
        canvas.width = w;
        canvas.height = h;

        canvas.onmousedown = (e) => {
            const rect = canvas.getBoundingClientRect();
            const mx = e.clientX - rect.left;
            const my = e.clientY - rect.top;

            if (watchtowerActiveTool === 'pan') {
                isDraggingWatchtowerMap = true;
                lastWtMouseX = e.clientX;
                lastWtMouseY = e.clientY;
            } else if (watchtowerActiveTool === 'measure_dist') {
                wtMeasurePoints.push({ x: mx, y: my });
                updateWatchtowerDistReadout();
                renderWatchtowerMaps();
            } else if (watchtowerActiveTool === 'measure_area') {
                wtMeasurePoly.push({ x: mx, y: my });
                updateWatchtowerAreaReadout();
                renderWatchtowerMaps();
            } else if (watchtowerActiveTool === 'profile') {
                if (wtProfilePoints.length >= 2) wtProfilePoints = [];
                wtProfilePoints.push({ x: mx, y: my });
                updateWatchtowerProfileReadout();
                renderWatchtowerMaps();
            } else if (watchtowerActiveTool === 'streetview') {
                openStreetViewMode(mx, my);
            }
        };

        window.onmouseup = () => { isDraggingWatchtowerMap = false; };

        canvas.onmousemove = (e) => {
            const rect = canvas.getBoundingClientRect();
            const mx = e.clientX - rect.left;
            const my = e.clientY - rect.top;

            if (isDraggingWatchtowerMap && watchtowerActiveTool === 'pan') {
                watchtowerMapPanX += e.clientX - lastWtMouseX;
                watchtowerMapPanY += e.clientY - lastWtMouseY;
                lastWtMouseX = e.clientX;
                lastWtMouseY = e.clientY;
                renderWatchtowerMaps();
            }

            // Update GPS HUD coordinates dynamically
            updateWatchtowerHUDCoords(mx, my, w, h);
        };

        canvas.onwheel = (e) => {
            e.preventDefault();
            const factor = e.deltaY < 0 ? 1.15 : 0.87;
            zoomWatchtowerMap(factor);
        };

        renderWatchtowerMaps();
    }

    function updateWatchtowerHUDCoords(mx, my, w, h) {
        const poi = watchtowerPOIs[currentWatchtowerPOI] || watchtowerPOIs['sete_quai'];
        const hudEl = document.getElementById('watchtower-coords-hud');
        const scaleEl = document.getElementById('watchtower-scale-hud');
        if (!hudEl) return;

        const offsetLat = ((h / 2 - my) / (h * watchtowerMapZoom)) * 0.015;
        const offsetLon = ((mx - w / 2) / (w * watchtowerMapZoom)) * 0.020;

        const curLat = (poi.lat + offsetLat).toFixed(4);
        const curLon = (poi.lon + offsetLon).toFixed(4);
        const l93X = Math.round(772450 + (mx - w/2)*2.5);
        const l93Y = Math.round(6268920 - (my - h/2)*2.5);
        const altZ = (poi.z + Math.sin(mx/50)*1.8).toFixed(1);

        hudEl.innerHTML = `📍 WGS84: <strong>${curLat}° N, ${curLon}° E</strong> • Lambert 93: X=${l93X.toLocaleString()}m, Y=${l93Y.toLocaleString()}m • Alt: <strong>${altZ}m NGF</strong> (${poi.name})`;
        if (scaleEl) {
            const scaleDenom = Math.round(500 / watchtowerMapZoom);
            const scaleMeters = Math.round(50 / watchtowerMapZoom);
            scaleEl.textContent = `Échelle : 1:${scaleDenom} (~${scaleMeters}m)`;
        }
    }

    function updateWatchtowerDistReadout() {
        if (wtMeasurePoints.length < 2) return;
        let totalDistPixels = 0;
        for (let i = 0; i < wtMeasurePoints.length - 1; i++) {
            totalDistPixels += Math.hypot(wtMeasurePoints[i+1].x - wtMeasurePoints[i].x, wtMeasurePoints[i+1].y - wtMeasurePoints[i].y);
        }
        // Conversion factor: 1 pixel ~ (1.2 / zoom) meters
        const meters = (totalDistPixels * (1.2 / watchtowerMapZoom)).toFixed(2);
        const readout = document.getElementById('watchtower-measurement-readout');
        if (readout) {
            readout.innerHTML = `📏 <strong>Distance Mesurée : ${meters} ml</strong> (${wtMeasurePoints.length} points, ${totalDistPixels.toFixed(0)} px)`;
        }
    }

    function updateWatchtowerAreaReadout() {
        if (wtMeasurePoly.length < 3) return;
        let areaPx = 0;
        for (let i = 0; i < wtMeasurePoly.length; i++) {
            const j = (i + 1) % wtMeasurePoly.length;
            areaPx += wtMeasurePoly[i].x * wtMeasurePoly[j].y;
            areaPx -= wtMeasurePoly[j].x * wtMeasurePoly[i].y;
        }
        areaPx = Math.abs(areaPx) / 2;
        const scaleMeterPerPx = (1.2 / watchtowerMapZoom);
        const areaM2 = (areaPx * Math.pow(scaleMeterPerPx, 2)).toFixed(1);
        const ha = (areaM2 / 10000).toFixed(3);
        const readout = document.getElementById('watchtower-measurement-readout');
        if (readout) {
            readout.innerHTML = `📐 <strong>Emprise Surface : ${areaM2} m²</strong> (${ha} ha • ${wtMeasurePoly.length} sommets)`;
        }
    }

    function updateWatchtowerProfileReadout() {
        if (wtProfilePoints.length !== 2) return;
        const p1 = wtProfilePoints[0];
        const p2 = wtProfilePoints[1];
        const distPx = Math.hypot(p2.x - p1.x, p2.y - p1.y);
        const distM = (distPx * (1.2 / watchtowerMapZoom)).toFixed(2);
        const deltaZ = (Math.sin(p2.x/30)*2.4 + 1.8).toFixed(2);
        const pente = ((deltaZ / distM) * 100).toFixed(2);

        const readout = document.getElementById('watchtower-measurement-readout');
        if (readout) {
            readout.innerHTML = `⛰️ <strong>Profil Alti : Dist = ${distM}ml • ΔZ = ${deltaZ}m • Pente = ${pente}%</strong>`;
        }
    }

    function renderWatchtowerMaps() {
        const canvas = document.getElementById('watchtower-maps-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const w = canvas.width;
        const h = canvas.height;
        const cx = w / 2 + watchtowerMapPanX;
        const cy = h / 2 + watchtowerMapPanY;

        ctx.clearRect(0, 0, w, h);

        // 1. BASE MAP LAYER RENDERING
        if (watchtowerMapLayer === 'satellite' || watchtowerMapLayer === 'hybride') {
            renderSatelliteHDLayer(ctx, w, h, cx, cy, watchtowerMapZoom);
        } else if (watchtowerMapLayer === 'osm') {
            renderOSMVectorLayer(ctx, w, h, cx, cy, watchtowerMapZoom);
        } else if (watchtowerMapLayer === 'cadastre') {
            renderCadastreLayer(ctx, w, h, cx, cy, watchtowerMapZoom);
        } else if (watchtowerMapLayer === 'relief') {
            renderReliefTopographicLayer(ctx, w, h, cx, cy, watchtowerMapZoom);
        }

        // 2. DICT NETWORK OVERLAYS (CONCESSIONNAIRES)
        renderDICTNetworks(ctx, cx, cy, watchtowerMapZoom);

        // 3. ACTIVE CHANTIER & POI PINS
        renderWatchtowerPOIPins(ctx, cx, cy, watchtowerMapZoom);

        // 4. MEASUREMENTS OVERLAY
        renderMeasurementOverlay(ctx);

        // 5. COMPASS HUD & SCALE BAR
        renderMapCompassAndScale(ctx, w, h);
    }

    function renderSatelliteHDLayer(ctx, w, h, cx, cy, zoom) {
        // High-fidelity orthophoto simulation with agricultural plots, Mediterranean vegetation, asphalt and water textures
        ctx.fillStyle = '#1e3a29'; // Base deep land green
        ctx.fillRect(0, 0, w, h);

        // Agricultural plots / Vineyards of Bassin de Thau
        const gridSize = 120 * zoom;
        const startX = (cx % gridSize) - gridSize;
        const startY = (cy % gridSize) - gridSize;

        for (let x = startX; x < w + gridSize; x += gridSize) {
            for (let y = startY; y < h + gridSize; y += gridSize) {
                const seed = Math.sin(x * 12.9898 + y * 78.233) * 43758.5453;
                const rand = seed - Math.floor(seed);
                
                if (rand > 0.75) ctx.fillStyle = '#2d4a22'; // Vineyard dark
                else if (rand > 0.5) ctx.fillStyle = '#3c5a2c'; // Field green
                else if (rand > 0.25) ctx.fillStyle = '#5c5438'; // Earth / Dry ground
                else ctx.fillStyle = '#223d24'; // Olive tree forest

                ctx.fillRect(x + 2, y + 2, gridSize - 4, gridSize - 4);

                // Texture stripes for vineyard rows
                ctx.strokeStyle = 'rgba(0,0,0,0.15)';
                ctx.lineWidth = 1;
                ctx.beginPath();
                for (let r = 0; r < gridSize; r += 12 * zoom) {
                    ctx.moveTo(x, y + r);
                    ctx.lineTo(x + gridSize, y + r);
                }
                ctx.stroke();
            }
        }

        // Étang de Thau / Sea water body
        ctx.fillStyle = '#0f3d56';
        ctx.beginPath();
        ctx.arc(cx - 380 * zoom, cy + 280 * zoom, 420 * zoom, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#176585';
        ctx.beginPath();
        ctx.arc(cx - 380 * zoom, cy + 280 * zoom, 390 * zoom, 0, Math.PI * 2);
        ctx.fill();

        // Main Highway & Road Network (Asphalt texture)
        // RD612 / RN112
        ctx.strokeStyle = '#1e293b';
        ctx.lineWidth = 26 * zoom;
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(cx - 400 * zoom, cy - 180 * zoom);
        ctx.quadraticCurveTo(cx, cy - 60 * zoom, cx + 450 * zoom, cy + 220 * zoom);
        ctx.stroke();

        // Road shoulders / Accotements
        ctx.strokeStyle = '#64748b';
        ctx.lineWidth = 2 * zoom;
        ctx.stroke();

        // White Road Stripes
        ctx.strokeStyle = '#f8fafc';
        ctx.lineWidth = 2 * zoom;
        ctx.setLineDash([12 * zoom, 8 * zoom]);
        ctx.stroke();
        ctx.setLineDash([]);

        // Roundabout at Center (Chantier Zone)
        ctx.fillStyle = '#1e293b';
        ctx.beginPath();
        ctx.arc(cx, cy, 55 * zoom, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#cbd5e1';
        ctx.lineWidth = 3 * zoom;
        ctx.stroke();

        // Central Island (Îlot central giratoire)
        ctx.fillStyle = '#22c55e'; // Green island
        ctx.beginPath();
        ctx.arc(cx, cy, 28 * zoom, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#f59e0b'; // Bordures I1
        ctx.lineWidth = 3 * zoom;
        ctx.stroke();

        // Construction Trench & Excavation Pit (Job site details)
        ctx.fillStyle = '#78350f'; // Earth trench
        ctx.fillRect(cx + 80 * zoom, cy - 40 * zoom, 160 * zoom, 18 * zoom);
        ctx.strokeStyle = '#f59e0b'; // Blindage
        ctx.lineWidth = 2 * zoom;
        ctx.strokeRect(cx + 80 * zoom, cy - 40 * zoom, 160 * zoom, 18 * zoom);

        // Job site machinery icons
        // Excavator Liebherr 24t
        ctx.fillStyle = '#f59e0b';
        ctx.fillRect(cx + 120 * zoom, cy - 65 * zoom, 24 * zoom, 16 * zoom);
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(cx + 132 * zoom, cy - 70 * zoom, 10 * zoom, 12 * zoom);

        // Dump truck 8x4
        ctx.fillStyle = '#38bdf8';
        ctx.fillRect(cx + 190 * zoom, cy - 65 * zoom, 32 * zoom, 14 * zoom);

        // Cadastral buildings in neighborhood
        ctx.fillStyle = '#831843'; // Tile roof red
        ctx.fillRect(cx - 180 * zoom, cy - 140 * zoom, 45 * zoom, 35 * zoom);
        ctx.fillRect(cx - 240 * zoom, cy - 120 * zoom, 38 * zoom, 30 * zoom);
        ctx.fillRect(cx - 150 * zoom, cy + 120 * zoom, 50 * zoom, 40 * zoom);
    }

    function renderOSMVectorLayer(ctx, w, h, cx, cy, zoom) {
        ctx.fillStyle = '#f1f5f9'; // OSM land
        ctx.fillRect(0, 0, w, h);

        // Parcels & residential areas
        ctx.fillStyle = '#e2e8f0';
        ctx.fillRect(cx - 300 * zoom, cy - 250 * zoom, 220 * zoom, 180 * zoom);
        ctx.fillRect(cx - 300 * zoom, cy + 50 * zoom, 200 * zoom, 200 * zoom);

        // Green zones / Parks
        ctx.fillStyle = '#dcfce7';
        ctx.fillRect(cx + 100 * zoom, cy + 100 * zoom, 280 * zoom, 220 * zoom);

        // Water Canal / Sea
        ctx.fillStyle = '#bae6fd';
        ctx.beginPath();
        ctx.arc(cx - 380 * zoom, cy + 280 * zoom, 400 * zoom, 0, Math.PI * 2);
        ctx.fill();

        // Primary Highway (Orange OSM style)
        ctx.strokeStyle = '#fb923c';
        ctx.lineWidth = 18 * zoom;
        ctx.beginPath();
        ctx.moveTo(cx - 400 * zoom, cy - 180 * zoom);
        ctx.quadraticCurveTo(cx, cy - 60 * zoom, cx + 450 * zoom, cy + 220 * zoom);
        ctx.stroke();

        // Roundabout
        ctx.fillStyle = '#f8fafc';
        ctx.strokeStyle = '#fb923c';
        ctx.lineWidth = 14 * zoom;
        ctx.beginPath();
        ctx.arc(cx, cy, 45 * zoom, 0, Math.PI * 2);
        ctx.stroke();
        ctx.fill();

        // Building blocks
        ctx.fillStyle = '#cbd5e1';
        ctx.strokeStyle = '#94a3b8';
        ctx.lineWidth = 1;
        ctx.fillRect(cx - 180 * zoom, cy - 140 * zoom, 45 * zoom, 35 * zoom);
        ctx.strokeRect(cx - 180 * zoom, cy - 140 * zoom, 45 * zoom, 35 * zoom);

        // Street names
        ctx.font = `bold ${Math.round(11 * zoom)}px 'Inter', sans-serif`;
        ctx.fillStyle = '#1e293b';
        ctx.fillText("Route Départementale RD612", cx - 180 * zoom, cy - 80 * zoom);
        ctx.fillText("Quai de la République / Giratoire Nord", cx - 60 * zoom, cy + 80 * zoom);
    }

    function renderCadastreLayer(ctx, w, h, cx, cy, zoom) {
        ctx.fillStyle = '#fffbeb'; // Cadastre parchment background
        ctx.fillRect(0, 0, w, h);

        // Cadastral parcel grid
        const pSize = 90 * zoom;
        ctx.strokeStyle = '#d97706';
        ctx.lineWidth = 1.5;

        for (let x = (cx % pSize) - pSize; x < w + pSize; x += pSize) {
            for (let y = (cy % pSize) - pSize; y < h + pSize; y += pSize) {
                ctx.strokeRect(x, y, pSize, pSize);
                
                // Parcel ID text
                ctx.font = `bold ${Math.round(9 * zoom)}px monospace`;
                ctx.fillStyle = '#92400e';
                const parcelNum = Math.abs(Math.round(Math.sin(x + y) * 900 + 100));
                ctx.fillText(`AX ${parcelNum}`, x + 6, y + 16);
            }
        }

        // Roadway public domain reservation
        ctx.fillStyle = 'rgba(56, 189, 248, 0.2)';
        ctx.strokeStyle = '#0284c7';
        ctx.lineWidth = 2 * zoom;
        ctx.beginPath();
        ctx.moveTo(cx - 400 * zoom, cy - 180 * zoom);
        ctx.quadraticCurveTo(cx, cy - 60 * zoom, cx + 450 * zoom, cy + 220 * zoom);
        ctx.stroke();

        ctx.font = `bold ${Math.round(10 * zoom)}px sans-serif`;
        ctx.fillStyle = '#0369a1';
        ctx.fillText("EMPRISE DOMAINE PUBLIC ROUTIER (DP 34)", cx + 100 * zoom, cy + 60 * zoom);
    }

    function renderReliefTopographicLayer(ctx, w, h, cx, cy, zoom) {
        ctx.fillStyle = '#1c1917'; // Dark contour map
        ctx.fillRect(0, 0, w, h);

        // Topographic contour lines
        ctx.strokeStyle = '#78716c';
        ctx.lineWidth = 1;
        for (let r = 40 * zoom; r < 500 * zoom; r += 35 * zoom) {
            ctx.beginPath();
            ctx.arc(cx - 100 * zoom, cy - 50 * zoom, r, 0, Math.PI * 2);
            ctx.stroke();

            // Elevation label
            const zVal = Math.round(10 + r / (20 * zoom));
            ctx.font = `${Math.round(8 * zoom)}px monospace`;
            ctx.fillStyle = '#a8a29e';
            ctx.fillText(`${zVal}m`, cx - 100 * zoom + r - 10, cy - 50 * zoom);
        }

        // Road axis overlay
        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 4 * zoom;
        ctx.beginPath();
        ctx.moveTo(cx - 400 * zoom, cy - 180 * zoom);
        ctx.quadraticCurveTo(cx, cy - 60 * zoom, cx + 450 * zoom, cy + 220 * zoom);
        ctx.stroke();
    }

    function renderDICTNetworks(ctx, cx, cy, zoom) {
        const showGaz = document.getElementById('dict-toggle-gaz')?.checked ?? true;
        const showElec = document.getElementById('dict-toggle-elec')?.checked ?? true;
        const showAep = document.getElementById('dict-toggle-aep')?.checked ?? true;
        const showEu = document.getElementById('dict-toggle-eu')?.checked ?? true;
        const showTelecom = document.getElementById('dict-toggle-telecom')?.checked ?? true;
        const showTraffic = document.getElementById('dict-toggle-traffic')?.checked ?? true;

        // 🟡 GAZ (PEHD Jaune)
        if (showGaz) {
            ctx.strokeStyle = '#eab308';
            ctx.lineWidth = 3 * zoom;
            ctx.beginPath();
            ctx.moveTo(cx - 380 * zoom, cy - 160 * zoom);
            ctx.lineTo(cx + 400 * zoom, cy + 180 * zoom);
            ctx.stroke();
            ctx.fillStyle = '#eab308';
            ctx.font = `bold ${Math.round(8 * zoom)}px monospace`;
            ctx.fillText("GAZ PEHD Ø110 4BAR", cx + 220 * zoom, cy + 120 * zoom);
        }

        // 🔴 ÉLECTRICITÉ (HTA / BT Rouge)
        if (showElec) {
            ctx.strokeStyle = '#ef4444';
            ctx.lineWidth = 3 * zoom;
            ctx.beginPath();
            ctx.moveTo(cx - 350 * zoom, cy - 200 * zoom);
            ctx.lineTo(cx + 420 * zoom, cy + 160 * zoom);
            ctx.stroke();
            ctx.fillStyle = '#ef4444';
            ctx.font = `bold ${Math.round(8 * zoom)}px monospace`;
            ctx.fillText("ENEDIS HTA 20kV", cx - 280 * zoom, cy - 180 * zoom);
        }

        // 🔵 EAU POTABLE (AEP Fonte Bleu)
        if (showAep) {
            ctx.strokeStyle = '#0284c7';
            ctx.lineWidth = 3.5 * zoom;
            ctx.beginPath();
            ctx.moveTo(cx - 320 * zoom, cy - 130 * zoom);
            ctx.lineTo(cx + 380 * zoom, cy + 210 * zoom);
            ctx.stroke();
            ctx.fillStyle = '#0284c7';
            ctx.font = `bold ${Math.round(8 * zoom)}px monospace`;
            ctx.fillText("AEP FONTE Ø150", cx + 50 * zoom, cy + 30 * zoom);
        }

        // 🟤 ASSAINISSEMENT (Béton Ø400 Marron/Orange)
        if (showEu) {
            ctx.strokeStyle = '#ea580c';
            ctx.lineWidth = 5 * zoom;
            ctx.beginPath();
            ctx.moveTo(cx + 80 * zoom, cy - 31 * zoom);
            ctx.lineTo(cx + 240 * zoom, cy - 31 * zoom);
            ctx.stroke();
            // Regards de visite
            ctx.fillStyle = '#7c2d12';
            ctx.beginPath(); ctx.arc(cx + 80 * zoom, cy - 31 * zoom, 6 * zoom, 0, Math.PI * 2); ctx.fill();
            ctx.beginPath(); ctx.arc(cx + 240 * zoom, cy - 31 * zoom, 6 * zoom, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#ea580c';
            ctx.font = `bold ${Math.round(8 * zoom)}px monospace`;
            ctx.fillText("COLLECTEUR BA Ø400", cx + 110 * zoom, cy - 42 * zoom);
        }

        // 🟢 TÉLÉCOM / FIBRE (Vert)
        if (showTelecom) {
            ctx.strokeStyle = '#16a34a';
            ctx.lineWidth = 2.5 * zoom;
            ctx.beginPath();
            ctx.moveTo(cx - 300 * zoom, cy - 110 * zoom);
            ctx.lineTo(cx + 350 * zoom, cy + 230 * zoom);
            ctx.stroke();
            // Chambres L1T
            ctx.fillStyle = '#15803d';
            ctx.fillRect(cx - 100 * zoom, cy + 10 * zoom, 8 * zoom, 8 * zoom);
            ctx.fillStyle = '#16a34a';
            ctx.font = `bold ${Math.round(8 * zoom)}px monospace`;
            ctx.fillText("FIBRE 4xØ45 (L1T)", cx - 180 * zoom, cy - 40 * zoom);
        }

        // 🚦 TRAFIC TEMPS RÉEL (Vert/Orange/Rouge)
        if (showTraffic) {
            ctx.strokeStyle = '#22c55e'; // Fluide
            ctx.lineWidth = 4 * zoom;
            ctx.beginPath();
            ctx.moveTo(cx - 400 * zoom, cy - 190 * zoom);
            ctx.lineTo(cx - 60 * zoom, cy - 70 * zoom);
            ctx.stroke();

            ctx.strokeStyle = '#ef4444'; // Ralentissement travaux
            ctx.beginPath();
            ctx.moveTo(cx - 60 * zoom, cy - 70 * zoom);
            ctx.lineTo(cx + 120 * zoom, cy + 20 * zoom);
            ctx.stroke();
        }
    }

    function renderWatchtowerPOIPins(ctx, cx, cy, zoom) {
        const poi = watchtowerPOIs[currentWatchtowerPOI] || watchtowerPOIs['sete_quai'];

        // Pin marker at center
        ctx.fillStyle = '#ef4444';
        ctx.beginPath();
        ctx.arc(cx, cy, 9 * zoom, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2 * zoom;
        ctx.stroke();

        // Pin label banner
        ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 1.5;
        const textW = ctx.measureText(poi.name).width + 20;
        ctx.fillRect(cx - textW / 2, cy - 42 * zoom, textW, 24 * zoom);
        ctx.strokeRect(cx - textW / 2, cy - 42 * zoom, textW, 24 * zoom);

        ctx.font = `bold ${Math.round(10 * zoom)}px 'Inter', sans-serif`;
        ctx.fillStyle = '#38bdf8';
        ctx.textAlign = 'center';
        ctx.fillText(`📍 ${poi.name}`, cx, cy - 26 * zoom);
        ctx.textAlign = 'left';
    }

    function renderMeasurementOverlay(ctx) {
        // Distance line
        if (wtMeasurePoints.length > 0) {
            ctx.strokeStyle = '#38bdf8';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(wtMeasurePoints[0].x, wtMeasurePoints[0].y);
            for (let i = 1; i < wtMeasurePoints.length; i++) {
                ctx.lineTo(wtMeasurePoints[i].x, wtMeasurePoints[i].y);
            }
            ctx.stroke();

            // Distance pins
            wtMeasurePoints.forEach((pt, i) => {
                ctx.fillStyle = i === 0 ? '#10b981' : '#38bdf8';
                ctx.beginPath();
                ctx.arc(pt.x, pt.y, 6, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 2;
                ctx.stroke();

                ctx.font = 'bold 10px monospace';
                ctx.fillStyle = '#ffffff';
                ctx.fillText(`P${i+1}`, pt.x + 8, pt.y - 8);
            });
        }

        // Polygon area
        if (wtMeasurePoly.length > 0) {
            ctx.fillStyle = 'rgba(56, 189, 248, 0.25)';
            ctx.strokeStyle = '#38bdf8';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(wtMeasurePoly[0].x, wtMeasurePoly[0].y);
            for (let i = 1; i < wtMeasurePoly.length; i++) {
                ctx.lineTo(wtMeasurePoly[i].x, wtMeasurePoly[i].y);
            }
            if (wtMeasurePoly.length > 2) ctx.closePath();
            ctx.fill();
            ctx.stroke();

            wtMeasurePoly.forEach((pt, i) => {
                ctx.fillStyle = '#f59e0b';
                ctx.beginPath();
                ctx.arc(pt.x, pt.y, 5, 0, Math.PI * 2);
                ctx.fill();
            });
        }

        // Profile line
        if (wtProfilePoints.length > 0) {
            ctx.strokeStyle = '#ec4899';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(wtProfilePoints[0].x, wtProfilePoints[0].y);
            if (wtProfilePoints.length === 2) {
                ctx.lineTo(wtProfilePoints[1].x, wtProfilePoints[1].y);
            }
            ctx.stroke();

            wtProfilePoints.forEach((pt, i) => {
                ctx.fillStyle = '#ec4899';
                ctx.beginPath();
                ctx.arc(pt.x, pt.y, 6, 0, Math.PI * 2);
                ctx.fill();
                ctx.font = 'bold 10px monospace';
                ctx.fillStyle = '#ffffff';
                ctx.fillText(i === 0 ? 'AMONT' : 'AVAL', pt.x + 8, pt.y - 8);
            });
        }
    }

    function renderMapCompassAndScale(ctx, w, h) {
        // Compass rose
        const compassX = w - 40;
        const compassY = 60;
        ctx.fillStyle = 'rgba(15,23,42,0.85)';
        ctx.beginPath(); ctx.arc(compassX, compassY, 20, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = 'rgba(56,189,248,0.5)'; ctx.lineWidth = 1.5; ctx.stroke();

        // North needle
        ctx.fillStyle = '#ef4444';
        ctx.beginPath();
        ctx.moveTo(compassX, compassY - 14);
        ctx.lineTo(compassX - 5, compassY);
        ctx.lineTo(compassX + 5, compassY);
        ctx.fill();

        // South needle
        ctx.fillStyle = '#cbd5e1';
        ctx.beginPath();
        ctx.moveTo(compassX, compassY + 14);
        ctx.lineTo(compassX - 5, compassY);
        ctx.lineTo(compassX + 5, compassY);
        ctx.fill();

        ctx.font = 'bold 10px sans-serif';
        ctx.fillStyle = '#ef4444';
        ctx.fillText("N", compassX - 4, compassY - 16);

        // Scale bar
        const barX = 20;
        const barY = h - 35;
        const barW = 80;
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(barX - 4, barY - 14, barW + 8, 20);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(barX, barY, barW / 2, 4);
        ctx.fillStyle = '#38bdf8';
        ctx.fillRect(barX + barW / 2, barY, barW / 2, 4);
        ctx.strokeStyle = '#ffffff';
        ctx.strokeRect(barX, barY, barW, 4);

        ctx.font = 'bold 9px monospace';
        ctx.fillStyle = '#f8fafc';
        const distM = Math.round(50 / watchtowerMapZoom);
        ctx.fillText(`0`, barX - 2, barY - 4);
        ctx.fillText(`${distM}m`, barX + barW - 12, barY - 4);
    }

    // ==========================================
    // STREET VIEW 360° IMMERSIVE VIEWPORT
    // ==========================================
    function openStreetViewMode(mx, my) {
        const overlay = document.getElementById('watchtower-streetview-modal-overlay');
        if (!overlay) return;
        overlay.style.display = 'block';
        isStreetViewOpen = true;

        const canvas = document.getElementById('watchtower-streetview-canvas');
        if (!canvas) return;
        canvas.width = overlay.clientWidth || 800;
        canvas.height = overlay.clientHeight || 500;

        canvas.onmousedown = (e) => {
            isDraggingStreetView = true;
            lastSvMouseX = e.clientX;
        };
        window.onmouseup = () => { isDraggingStreetView = false; };
        window.onmousemove = (e) => {
            if (!isDraggingStreetView || !isStreetViewOpen) return;
            const dx = e.clientX - lastSvMouseX;
            streetViewRotAngle += dx * 0.4;
            lastSvMouseX = e.clientX;
            renderStreetView360();
        };

        renderStreetView360();
        logCockpit("Street View 360° : Caméra sol activée avec succès.", "ok");
    }

    function closeStreetViewMode() {
        const overlay = document.getElementById('watchtower-streetview-modal-overlay');
        if (overlay) overlay.style.display = 'none';
        isStreetViewOpen = false;
    }

    function rotateStreetView(deg) {
        streetViewRotAngle += deg;
        renderStreetView360();
    }

    function renderStreetView360() {
        const canvas = document.getElementById('watchtower-streetview-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const w = canvas.width;
        const h = canvas.height;
        const horizon = h * 0.52;

        ctx.clearRect(0, 0, w, h);

        // 1. SKY GRADIENT
        const skyGrad = ctx.createLinearGradient(0, 0, 0, horizon);
        skyGrad.addColorStop(0, '#0284c7'); // Azure sky
        skyGrad.addColorStop(1, '#bae6fd');
        ctx.fillStyle = skyGrad;
        ctx.fillRect(0, 0, w, horizon);

        // Sun & clouds
        ctx.fillStyle = '#fef08a';
        ctx.beginPath(); ctx.arc(w * 0.75 + (streetViewRotAngle*2 % w), horizon * 0.35, 24, 0, Math.PI * 2); ctx.fill();

        // 2. ASPHALT ROAD & GROUND
        const groundGrad = ctx.createLinearGradient(0, horizon, 0, h);
        groundGrad.addColorStop(0, '#334155');
        groundGrad.addColorStop(1, '#0f172a');
        ctx.fillStyle = groundGrad;
        ctx.fillRect(0, horizon, w, h - horizon);

        // Perspective road markings
        const rotShift = (streetViewRotAngle * 5) % w;
        ctx.fillStyle = '#f8fafc';
        for (let i = 0; i < 6; i++) {
            const rx = (w / 2 + rotShift + i * 160) % (w + 200) - 100;
            ctx.beginPath();
            ctx.moveTo(rx - 10, horizon + 20);
            ctx.lineTo(rx + 10, horizon + 20);
            ctx.lineTo(rx + 40, h);
            ctx.lineTo(rx - 40, h);
            ctx.fill();
        }

        // 3. JOB SITE EXCAVATION TRENCH (LEFT/CENTER)
        const trenchX = (w * 0.3 + rotShift) % (w + 400) - 200;
        ctx.fillStyle = '#451a03'; // Deep trench
        ctx.fillRect(trenchX, horizon + 30, 220, 140);

        // Steel trench shoring box (Blindage Krings jaune)
        ctx.fillStyle = '#eab308';
        ctx.fillRect(trenchX - 10, horizon + 20, 15, 150);
        ctx.fillRect(trenchX + 215, horizon + 20, 15, 150);
        // Struts (Étrésillons)
        ctx.strokeStyle = '#f8fafc';
        ctx.lineWidth = 6;
        ctx.beginPath();
        ctx.moveTo(trenchX, horizon + 50); ctx.lineTo(trenchX + 220, horizon + 50);
        ctx.moveTo(trenchX, horizon + 120); ctx.lineTo(trenchX + 220, horizon + 120);
        ctx.stroke();

        // Concrete pipe BA Ø400 inside trench
        ctx.fillStyle = '#94a3b8';
        ctx.beginPath();
        ctx.arc(trenchX + 110, horizon + 100, 35, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#334155';
        ctx.beginPath();
        ctx.arc(trenchX + 110, horizon + 100, 26, 0, Math.PI * 2);
        ctx.fill();

        // Laser Piper 200 Red Beam
        ctx.strokeStyle = '#ef4444';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(trenchX + 110, horizon + 100);
        ctx.lineTo(trenchX + 450, horizon + 90);
        ctx.stroke();

        // 4. LIEBHERR 24T EXCAVATOR (RIGHT)
        const excX = (w * 0.65 + rotShift) % (w + 400) - 100;
        // Tracks
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(excX, horizon - 10, 130, 35);
        // Cabin
        ctx.fillStyle = '#f59e0b';
        ctx.fillRect(excX + 20, horizon - 75, 80, 65);
        // Glass
        ctx.fillStyle = '#38bdf8';
        ctx.fillRect(excX + 60, horizon - 65, 35, 30);
        // Articulated Boom & Arm
        ctx.strokeStyle = '#f59e0b';
        ctx.lineWidth = 14;
        ctx.beginPath();
        ctx.moveTo(excX + 80, horizon - 50);
        ctx.lineTo(excX + 160, horizon - 130);
        ctx.lineTo(excX + 210, horizon - 40);
        ctx.stroke();
        // Bucket
        ctx.fillStyle = '#334155';
        ctx.fillRect(excX + 200, horizon - 45, 30, 25);

        // 5. WORKERS IN HIGH-VIS VESTS
        const workerX = (w * 0.2 + rotShift) % (w + 400) - 50;
        // Helmet
        ctx.fillStyle = '#facc15';
        ctx.beginPath(); ctx.arc(workerX, horizon - 55, 8, 0, Math.PI * 2); ctx.fill();
        // Vest
        ctx.fillStyle = '#f97316'; // Fluo orange
        ctx.fillRect(workerX - 10, horizon - 45, 20, 30);
        // Legs
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(workerX - 9, horizon - 15, 7, 25);
        ctx.fillRect(workerX + 2, horizon - 15, 7, 25);

        // 6. ROAD SIGNS (AK5 & B14)
        const signX = (w * 0.85 + rotShift) % (w + 400) - 50;
        ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 4;
        ctx.beginPath(); ctx.moveTo(signX, horizon + 80); ctx.lineTo(signX, horizon - 30); ctx.stroke();
        // AK5 Triangle
        ctx.fillStyle = '#eab308'; ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(signX, horizon - 60); ctx.lineTo(signX - 25, horizon - 15); ctx.lineTo(signX + 25, horizon - 15); ctx.closePath();
        ctx.fill(); ctx.stroke();
    }

    function exportWatchtowerMapPNG() {
        const canvas = document.getElementById('watchtower-maps-canvas');
        if (!canvas) return;

        // Render high-res export with legal cartouche
        const expCanvas = document.createElement('canvas');
        expCanvas.width = 1200;
        expCanvas.height = 800;
        const ectx = expCanvas.getContext('2d');

        // Draw map
        ectx.drawImage(canvas, 0, 0, 1200, 720);

        // Cartouche banner at bottom
        ectx.fillStyle = '#0f172a';
        ectx.fillRect(0, 720, 1200, 80);
        ectx.strokeStyle = '#38bdf8';
        ectx.lineWidth = 2;
        ectx.strokeRect(0, 720, 1200, 80);

        const poi = watchtowerPOIs[currentWatchtowerPOI] || watchtowerPOIs['sete_quai'];
        ectx.fillStyle = '#38bdf8';
        ectx.font = "bold 16px 'Inter', sans-serif";
        ectx.fillText(`PLAN DE SITUATION & CARTOGRAPHIE SIG : ${poi.name.toUpperCase()} (${poi.pk})`, 25, 750);

        ectx.fillStyle = '#cbd5e1';
        ectx.font = "12px monospace";
        ectx.fillText(`COORDONNÉES : WGS84 ${poi.lat}° N, ${poi.lon}° E • ÉCHELLE : 1:500 • DATE : ${new Date().toLocaleDateString('fr-FR')}`, 25, 775);
        ectx.fillText(`ENTREPRISE : OCCITANIE TP MÉDITERRANÉE • VISA CONDUCTEUR : VALIDÉ CONFORME (AIPR & DICT)`, 650, 775);

        const link = document.createElement('a');
        link.download = `Plan_Situation_${currentWatchtowerPOI}_${Date.now()}.png`;
        link.href = expCanvas.toDataURL('image/png');
        link.click();
        logCockpit(`Export PNG : Plan de situation ${poi.name} téléchargé avec succès.`, 'ok');
    }
'''

with open('scripts/section_js_part2.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace or inject watchtower_maps_code in section_js_part2.py
# Let's find where setSimulatorViewMode is defined in section_js_part2.py
pos_set_sim = text.find('function setSimulatorViewMode(mode) {')
if pos_set_sim != -1:
    # find where togglePlay4DSimulation ends
    pos_toggle = text.find('// 2D RADAR ANIMATION', pos_set_sim)
    if pos_toggle != -1:
        text = text[:pos_set_sim] + watchtower_maps_code.strip() + "\n\n    " + text[pos_toggle:]
        print("setSimulatorViewMode and Maps engine injected into section_js_part2.py successfully!")
    else:
        print("Warning: 2D RADAR ANIMATION not found, appending to file")
else:
    print("setSimulatorViewMode not found in section_js_part2.py")

with open('scripts/section_js_part2.py', 'w', encoding='utf-8') as f:
    f.write(text)
