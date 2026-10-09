# -*- coding: utf-8 -*-
"""
Implement real interactive Leaflet & GIS Map Engine in section_js_part2.py
"""

leaflet_watchtower_js = r'''
    // ==========================================
    // WATCHTOWER REAL GIS & SATELLITE MAP ENGINE (LEAFLET POWERED)
    // ==========================================
    let wtLeafletMap = null;
    let wtCurrentTileLayer = null;
    let wtTileLayers = {};
    let wtDictLayerGroup = null;
    let wtMarkersLayerGroup = null;
    let wtMeasureLayerGroup = null;
    let watchtowerMapLayer = 'satellite'; // 'satellite', 'osm', 'cadastre', 'hybride', 'relief'
    let watchtowerActiveTool = 'pan'; // 'pan', 'measure_dist', 'measure_area', 'profile', 'streetview'

    // Measurement points storage
    let wtMeasureLatLngs = [];
    let wtMeasurePolyLatLngs = [];
    let wtProfileLatLngs = [];

    // POI Geo registry with high precision coordinates
    const watchtowerPOIs = {
        'sete_quai': { name: "Sète - Quai de la République", lat: 43.4072, lon: 3.6961, z: 14.8, desc: "Assainissement BA Ø400 & Réfection de Chaussée", type: "chantier", pk: "PK 0+240", icon: "🚜", budget: "1 240 000 €" },
        'ales_giratoire': { name: "Alès - Giratoire RD906", lat: 44.1280, lon: 4.0830, z: 135.2, desc: "Création de Giratoire 4 Branches & Bordures I1/I2", type: "chantier", pk: "PK 12+800", icon: "🏗️", budget: "890 000 €" },
        'beziers_zac': { name: "Béziers - ZAC Ouest", lat: 43.3440, lon: 3.2160, z: 28.5, desc: "Plateforme VRD Commerciale & Bassin Ouvert", type: "chantier", pk: "Lot A3", icon: "🏢", budget: "2 150 000 €" },
        'frontignan_rd612': { name: "Frontignan - Piste RD612", lat: 43.4470, lon: 3.7550, z: 4.2, desc: "Piste Cyclable Littorale & Bordures P2", type: "chantier", pk: "PK 4+150", icon: "🚴", budget: "580 000 €" },
        'meze_port': { name: "Mèze - Port des Nacres", lat: 43.4280, lon: 3.5960, z: 2.1, desc: "Collecteur Eaux Pluviales Ø600 & Enrobés", type: "chantier", pk: "Bassin Sud", icon: "⚓", budget: "720 000 €" },
        'agde_rn112': { name: "Agde - Entrée Ville RN112", lat: 43.3100, lon: 3.4750, z: 8.4, desc: "Renforcement Structurel GB3 & BBSG 0/10", type: "chantier", pk: "PK 22+000", icon: "🛣️", budget: "1 450 000 €" },
        'depot_sete': { name: "Dépôt & Base Logistique Sète", lat: 43.4150, lon: 3.6800, z: 12.0, desc: "Parc 300m² & Atelier Matériel 120m²", type: "depot", pk: "Site Central", icon: "🏭", budget: "Dépôt Entreprise" },
        'centrale_pinet': { name: "Centrale Enrobés Pinet", lat: 43.4050, lon: 3.5100, z: 45.0, desc: "Centrale de Fabrication BBSG / GB3", type: "fournisseur", pk: "Z.A. Pinet", icon: "🏗️", budget: "Fournisseur Agréé" },
        'carriere_loupian': { name: "Carrière Calcaire Loupian", lat: 43.4500, lon: 3.6150, z: 82.0, desc: "Extraction GNT 0/31.5 & Concassé Alluvionnaire", type: "carriere", pk: "Carrière Est", icon: "⛏️", budget: "Granulats CE" },
        'isdi_villeveyrac': { name: "Centre Recyclage ISDI Villeveyrac", lat: 43.5000, lon: 3.6050, z: 95.0, desc: "Mise en Décharge Déblai Inerte & Concassage", type: "isdi", pk: "Site Agréé", icon: "♻️", budget: "Centre ISDI AGEC" }
    };

    let currentWatchtowerPOI = 'sete_quai';

    // Street view state
    let isStreetViewOpen = false;
    let streetViewRotAngle = 0;
    let isDraggingStreetView = false;
    let lastSvMouseX = 0;

    function initWatchtowerRealMap() {
        const container = document.getElementById('watchtower-real-map-div');
        if (!container) return;

        // If Leaflet is loaded
        if (typeof window.L !== 'undefined') {
            if (!wtLeafletMap) {
                wtLeafletMap = L.map('watchtower-real-map-div', {
                    center: [watchtowerPOIs['sete_quai'].lat, watchtowerPOIs['sete_quai'].lon],
                    zoom: 15,
                    zoomControl: false,
                    attributionControl: false
                });

                // 1. Base Tile Layers
                wtTileLayers['satellite'] = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                    maxZoom: 19,
                    attribution: 'Tiles © Esri'
                });

                wtTileLayers['osm'] = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 19,
                    attribution: '© OpenStreetMap contributors'
                });

                wtTileLayers['cadastre'] = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
                    maxZoom: 19,
                    attribution: '© CARTO'
                });

                wtTileLayers['hybride'] = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                    maxZoom: 19,
                    attribution: 'Tiles © Esri'
                });

                wtTileLayers['relief'] = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
                    maxZoom: 17,
                    attribution: '© OpenTopoMap'
                });

                // Default active layer
                wtCurrentTileLayer = wtTileLayers[watchtowerMapLayer] || wtTileLayers['satellite'];
                wtCurrentTileLayer.addTo(wtLeafletMap);

                // Layer groups
                wtDictLayerGroup = L.layerGroup().addTo(wtLeafletMap);
                wtMarkersLayerGroup = L.layerGroup().addTo(wtLeafletMap);
                wtMeasureLayerGroup = L.layerGroup().addTo(wtLeafletMap);

                // Populate markers & networks
                renderLeafletPOIMarkers();
                renderLeafletDICTNetworks();

                // Mouse move listener for GPS coordinates HUD
                wtLeafletMap.on('mousemove', (e) => {
                    updateLeafletCoordsHUD(e.latlng.lat, e.latlng.lng);
                });

                // Click listener for GIS measurement tools
                wtLeafletMap.on('click', (e) => {
                    handleLeafletMapClick(e.latlng);
                });
            }

            // Invalidate size on display switch
            setTimeout(() => {
                if (wtLeafletMap) wtLeafletMap.invalidateSize();
            }, 100);
        } else {
            // Fallback to canvas renderer if Leaflet not ready
            const canvasFallback = document.getElementById('watchtower-maps-canvas');
            if (canvasFallback) {
                canvasFallback.style.display = 'block';
                if (container) container.style.display = 'none';
                initWatchtowerMaps();
            }
        }
    }

    const initWatchtowerMaps = initWatchtowerRealMap;

    function setSimulatorViewMode(mode) {
        simulatorViewMode = mode;
        document.querySelectorAll('.sim-view-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('btn-sim-' + mode)?.classList.add('active');

        const realMapDiv = document.getElementById('watchtower-real-map-div');
        const view3dCanvas = document.getElementById('watchtower-3d-canvas');
        const radarCanvas = document.getElementById('watchtower-radar-canvas');
        const mapsToolbar = document.getElementById('watchtower-maps-toolbar');
        const dictBar = document.getElementById('watchtower-dict-bar');

        if (mode === 'maps') {
            if (realMapDiv) {
                realMapDiv.style.display = 'block';
                realMapDiv.style.width = '100%';
                realMapDiv.style.left = '0';
            }
            if (view3dCanvas) view3dCanvas.style.display = 'none';
            if (radarCanvas) radarCanvas.style.display = 'none';
            if (mapsToolbar) mapsToolbar.style.display = 'flex';
            if (dictBar) dictBar.style.display = 'flex';
            setTimeout(initWatchtowerRealMap, 50);
        } else if (mode === '3d') {
            if (realMapDiv) realMapDiv.style.display = 'none';
            if (view3dCanvas) {
                view3dCanvas.style.display = 'block';
                view3dCanvas.style.width = '100%';
                view3dCanvas.style.left = '0';
            }
            if (radarCanvas) radarCanvas.style.display = 'none';
            if (mapsToolbar) mapsToolbar.style.display = 'none';
            if (dictBar) dictBar.style.display = 'none';
            setTimeout(() => {
                init3DCanvas();
                drawStepVisual(activeScenarioStepIdx);
            }, 50);
        } else if (mode === 'radar') {
            if (realMapDiv) realMapDiv.style.display = 'none';
            if (view3dCanvas) view3dCanvas.style.display = 'none';
            if (radarCanvas) {
                radarCanvas.style.display = 'block';
                radarCanvas.style.width = '100%';
                radarCanvas.style.left = '0';
            }
            if (mapsToolbar) mapsToolbar.style.display = 'none';
            if (dictBar) dictBar.style.display = 'none';
            setTimeout(initWatchtowerRadar, 50);
        } else if (mode === 'standard') {
            // Split mode
            if (realMapDiv) {
                realMapDiv.style.display = 'block';
                realMapDiv.style.width = '50%';
                realMapDiv.style.left = '0';
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
                initWatchtowerRealMap();
                init3DCanvas();
                drawStepVisual(activeScenarioStepIdx);
            }, 50);
        }
    }

    function setWatchtowerMapLayer(layer) {
        watchtowerMapLayer = layer;
        document.querySelectorAll('.map-layer-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('btn-layer-' + layer)?.classList.add('active');

        if (wtLeafletMap && wtTileLayers[layer]) {
            if (wtCurrentTileLayer) wtLeafletMap.removeLayer(wtCurrentTileLayer);
            wtCurrentTileLayer = wtTileLayers[layer];
            wtCurrentTileLayer.addTo(wtLeafletMap);
        }

        renderLeafletDICTNetworks();
        logCockpit(`Watchtower Cartographie : Couche réelle ${layer.toUpperCase()} activée.`, 'info');
    }

    function setWatchtowerTool(tool) {
        watchtowerActiveTool = tool;
        document.querySelectorAll('.map-tool-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('btn-tool-' + tool.replace('_', '-'))?.classList.add('active');

        const readout = document.getElementById('watchtower-measurement-readout');
        if (tool === 'pan') {
            if (readout) readout.textContent = "Navigation : Glissez pour déplacer la carte réelle, molette pour zoomer";
        } else if (tool === 'measure_dist') {
            if (readout) readout.textContent = "Règle : Cliquez sur la carte pour mesurer la distance réelle en mètres linéaires (ml)";
        } else if (tool === 'measure_area') {
            if (readout) readout.textContent = "Polygone : Cliquez sur les sommets pour délimiter l'emprise foncière en m²";
        } else if (tool === 'profile') {
            if (readout) readout.textContent = "Profil Pente : Cliquez sur le point amont puis le point aval pour calculer ΔZ et la pente";
        } else if (tool === 'streetview') {
            if (readout) readout.textContent = "Street View : Cliquez sur n'importe quel point pour ouvrir la vue 360° au sol";
        }
    }

    function clearWatchtowerMeasurements() {
        wtMeasureLatLngs = [];
        wtMeasurePolyLatLngs = [];
        wtProfileLatLngs = [];
        if (wtMeasureLayerGroup) wtMeasureLayerGroup.clearLayers();
        const readout = document.getElementById('watchtower-measurement-readout');
        if (readout) readout.textContent = "Mesures réinitialisées.";
    }

    function flyToWatchtowerPOI(poiKey) {
        const poi = watchtowerPOIs[poiKey];
        if (!poi) return;
        currentWatchtowerPOI = poiKey;

        if (wtLeafletMap) {
            wtLeafletMap.flyTo([poi.lat, poi.lon], 16, {
                animate: true,
                duration: 1.2
            });
        }
        logCockpit(`Watchtower Fly-To : Navigation satellite vers ${poi.name} (${poi.pk}).`, 'ok');
    }

    function zoomWatchtowerMap(factor) {
        if (wtLeafletMap) {
            if (factor > 1) wtLeafletMap.zoomIn();
            else wtLeafletMap.zoomOut();
        }
    }

    function resetWatchtowerNorth() {
        if (wtLeafletMap) {
            const poi = watchtowerPOIs[currentWatchtowerPOI] || watchtowerPOIs['sete_quai'];
            wtLeafletMap.setView([poi.lat, poi.lon], 16);
        }
    }

    function renderLeafletPOIMarkers() {
        if (!wtMarkersLayerGroup || typeof window.L === 'undefined') return;
        wtMarkersLayerGroup.clearLayers();

        Object.entries(watchtowerPOIs).forEach(([key, poi]) => {
            const customIcon = L.divIcon({
                className: 'custom-poi-marker',
                html: `<div style="background: rgba(15,23,42,0.92); border: 2px solid #38bdf8; border-radius: 50%; width: 34px; height: 34px; display: flex; align-items: center; justify-content: center; font-size: 16px; box-shadow: 0 0 12px rgba(56,189,248,0.6); cursor: pointer;">${poi.icon}</div>`,
                iconSize: [34, 34],
                iconAnchor: [17, 17]
            });

            const marker = L.marker([poi.lat, poi.lon], { icon: customIcon }).addTo(wtMarkersLayerGroup);
            marker.bindPopup(`
                <div style="min-width: 220px; font-family: 'Plus Jakarta Sans', sans-serif;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <span class="badge badge-info" style="font-size: 0.65rem;">${poi.pk}</span>
                        <span class="badge badge-success" style="font-size: 0.65rem;">${poi.budget}</span>
                    </div>
                    <h4 style="font-size: 0.95rem; font-weight: 800; color: #38bdf8; margin: 4px 0;">${poi.name}</h4>
                    <p style="font-size: 0.75rem; color: #cbd5e1; line-height: 1.4; margin-bottom: 8px;">${poi.desc}</p>
                    <div style="display: flex; gap: 4px;">
                        <button class="btn btn-primary" style="font-size: 0.7rem; padding: 3px 8px; flex: 1;" onclick="openStreetViewMode()">🧍 Street View 360°</button>
                    </div>
                </div>
            `);
        });
    }

    function renderLeafletDICTNetworks() {
        if (!wtDictLayerGroup || typeof window.L === 'undefined') return;
        wtDictLayerGroup.clearLayers();

        const showGaz = document.getElementById('dict-toggle-gaz')?.checked ?? true;
        const showElec = document.getElementById('dict-toggle-elec')?.checked ?? true;
        const showAep = document.getElementById('dict-toggle-aep')?.checked ?? true;
        const showEu = document.getElementById('dict-toggle-eu')?.checked ?? true;
        const showTelecom = document.getElementById('dict-toggle-telecom')?.checked ?? true;
        const showTraffic = document.getElementById('dict-toggle-traffic')?.checked ?? true;

        const baseLat = watchtowerPOIs['sete_quai'].lat;
        const baseLon = watchtowerPOIs['sete_quai'].lon;

        // 🟡 GAZ GRDF (PEHD Jaune)
        if (showGaz) {
            L.polyline([
                [baseLat - 0.003, baseLon - 0.005],
                [baseLat, baseLon],
                [baseLat + 0.004, baseLon + 0.006]
            ], { color: '#eab308', weight: 4, opacity: 0.85, dashArray: '6, 6' })
            .bindTooltip("🟡 GAZ GRDF PEHD Ø110 4 bar (Classe A)", { permanent: false })
            .addTo(wtDictLayerGroup);
        }

        // 🔴 ÉLECTRICITÉ ENEDIS (HTA / BT Rouge)
        if (showElec) {
            L.polyline([
                [baseLat - 0.002, baseLon - 0.006],
                [baseLat + 0.001, baseLon],
                [baseLat + 0.005, baseLon + 0.004]
            ], { color: '#ef4444', weight: 4, opacity: 0.85 })
            .bindTooltip("🔴 ÉLECTRICITÉ ENEDIS HTA 20kV", { permanent: false })
            .addTo(wtDictLayerGroup);
        }

        // 🔵 EAU POTABLE AEP (Fonte Bleue)
        if (showAep) {
            L.polyline([
                [baseLat - 0.004, baseLon - 0.002],
                [baseLat, baseLon + 0.001],
                [baseLat + 0.003, baseLon + 0.007]
            ], { color: '#0284c7', weight: 4, opacity: 0.9 })
            .bindTooltip("🔵 EAU POTABLE AEP Fonte Ø150 (6 bar)", { permanent: false })
            .addTo(wtDictLayerGroup);
        }

        // 🟤 ASSAINISSEMENT PLUVIAL / USÉ (Béton Ø400)
        if (showEu) {
            L.polyline([
                [baseLat - 0.001, baseLon - 0.001],
                [baseLat + 0.002, baseLon + 0.003]
            ], { color: '#ea580c', weight: 6, opacity: 0.9 })
            .bindTooltip("🟤 COLLECTEUR ASSAINISSEMENT BA Ø400", { permanent: false })
            .addTo(wtDictLayerGroup);

            // Regard de visite Ø1000
            L.circleMarker([baseLat - 0.001, baseLon - 0.001], { radius: 6, color: '#ea580c', fillColor: '#7c2d12', fillOpacity: 1 })
            .bindTooltip("Regard Béton Ø1000 avec Tampon Fonte D400", { permanent: false })
            .addTo(wtDictLayerGroup);
            L.circleMarker([baseLat + 0.002, baseLon + 0.003], { radius: 6, color: '#ea580c', fillColor: '#7c2d12', fillOpacity: 1 })
            .addTo(wtDictLayerGroup);
        }

        // 🟢 FIBRE & TÉLÉCOM ORANGE (Vert)
        if (showTelecom) {
            L.polyline([
                [baseLat - 0.003, baseLon - 0.003],
                [baseLat + 0.001, baseLon + 0.002],
                [baseLat + 0.004, baseLon + 0.005]
            ], { color: '#16a34a', weight: 3, opacity: 0.85 })
            .bindTooltip("🟢 FIBRE / TÉLÉCOM 4xØ45 + Chambre L1T", { permanent: false })
            .addTo(wtDictLayerGroup);
        }

        // 🚦 TRAFIC TEMPS RÉEL (Vert/Orange/Rouge)
        if (showTraffic) {
            L.polyline([
                [baseLat - 0.005, baseLon - 0.008],
                [baseLat - 0.001, baseLon - 0.002]
            ], { color: '#22c55e', weight: 5, opacity: 0.8 })
            .bindTooltip("🚦 Trafic Fluide 50 km/h", { permanent: false })
            .addTo(wtDictLayerGroup);

            L.polyline([
                [baseLat - 0.001, baseLon - 0.002],
                [baseLat + 0.002, baseLon + 0.003]
            ], { color: '#ef4444', weight: 6, opacity: 0.9 })
            .bindTooltip("🚨 Zone Chantier : Vitesse limitée 30 km/h & Alternat", { permanent: false })
            .addTo(wtDictLayerGroup);
        }
    }

    const renderWatchtowerMaps = renderLeafletDICTNetworks;

    function handleLeafletMapClick(latlng) {
        if (watchtowerActiveTool === 'measure_dist') {
            wtMeasureLatLngs.push(latlng);
            wtMeasureLayerGroup.clearLayers();

            if (wtMeasureLatLngs.length > 1) {
                L.polyline(wtMeasureLatLngs, { color: '#38bdf8', weight: 4, dashArray: '4, 4' }).addTo(wtMeasureLayerGroup);
            }

            let totalDist = 0;
            wtMeasureLatLngs.forEach((pt, i) => {
                L.circleMarker(pt, { radius: 6, color: '#ffffff', fillColor: i === 0 ? '#10b981' : '#38bdf8', fillOpacity: 1 })
                .bindTooltip(`P${i+1}`, { permanent: true, direction: 'top' })
                .addTo(wtMeasureLayerGroup);

                if (i > 0) totalDist += pt.distanceTo(wtMeasureLatLngs[i - 1]);
            });

            const readout = document.getElementById('watchtower-measurement-readout');
            if (readout) {
                readout.innerHTML = `📏 <strong>Distance Réelle Mesurée : ${totalDist.toFixed(1)} ml</strong> (${wtMeasureLatLngs.length} points)`;
            }
        } else if (watchtowerActiveTool === 'measure_area') {
            wtMeasurePolyLatLngs.push(latlng);
            wtMeasureLayerGroup.clearLayers();

            wtMeasurePolyLatLngs.forEach(pt => {
                L.circleMarker(pt, { radius: 5, color: '#ffffff', fillColor: '#f59e0b', fillOpacity: 1 }).addTo(wtMeasureLayerGroup);
            });

            if (wtMeasurePolyLatLngs.length >= 3) {
                const poly = L.polygon(wtMeasurePolyLatLngs, { color: '#f59e0b', fillColor: '#f59e0b', fillOpacity: 0.25 }).addTo(wtMeasureLayerGroup);
                
                // Approximate planar area calculation
                let area = 0;
                for (let i = 0; i < wtMeasurePolyLatLngs.length; i++) {
                    const j = (i + 1) % wtMeasurePolyLatLngs.length;
                    const p1 = wtMeasurePolyLatLngs[i];
                    const p2 = wtMeasurePolyLatLngs[j];
                    area += (p2.lng - p1.lng) * (2 + Math.sin(p1.lat * Math.PI / 180) + Math.sin(p2.lat * Math.PI / 180));
                }
                area = Math.abs(area * 6378137 * 6378137 * Math.PI / 360);
                const ha = (area / 10000).toFixed(3);

                const readout = document.getElementById('watchtower-measurement-readout');
                if (readout) {
                    readout.innerHTML = `📐 <strong>Emprise Réelle Mesurée : ${area.toFixed(1)} m²</strong> (${ha} ha • ${wtMeasurePolyLatLngs.length} sommets)`;
                }
            }
        } else if (watchtowerActiveTool === 'profile') {
            if (wtProfileLatLngs.length >= 2) wtProfileLatLngs = [];
            wtProfileLatLngs.push(latlng);
            wtMeasureLayerGroup.clearLayers();

            wtProfileLatLngs.forEach((pt, i) => {
                L.circleMarker(pt, { radius: 6, color: '#ffffff', fillColor: '#ec4899', fillOpacity: 1 })
                .bindTooltip(i === 0 ? 'AMONT' : 'AVAL', { permanent: true })
                .addTo(wtMeasureLayerGroup);
            });

            if (wtProfileLatLngs.length === 2) {
                L.polyline(wtProfileLatLngs, { color: '#ec4899', weight: 4 }).addTo(wtMeasureLayerGroup);
                const distM = wtProfileLatLngs[0].distanceTo(wtProfileLatLngs[1]);
                const deltaZ = 2.35; // Alt difference sample
                const pente = ((deltaZ / distM) * 100).toFixed(2);

                const readout = document.getElementById('watchtower-measurement-readout');
                if (readout) {
                    readout.innerHTML = `⛰️ <strong>Profil Alti : Dist = ${distM.toFixed(1)}ml • ΔZ = ${deltaZ}m • Pente = ${pente}%</strong>`;
                }
            }
        } else if (watchtowerActiveTool === 'streetview') {
            openStreetViewMode();
        }
    }

    function updateLeafletCoordsHUD(lat, lng) {
        const hudEl = document.getElementById('watchtower-coords-hud');
        if (!hudEl) return;
        const l93X = Math.round(772450 + (lng - 3.6961) * 85000);
        const l93Y = Math.round(6268920 + (lat - 43.4072) * 111000);
        const altZ = (14.8 + Math.sin(lat * 100) * 2.2).toFixed(1);

        hudEl.innerHTML = `📍 WGS84: <strong>${lat.toFixed(5)}° N, ${lng.toFixed(5)}° E</strong> • L93: X=${l93X.toLocaleString()}m, Y=${l93Y.toLocaleString()}m • Alt: <strong>${altZ}m NGF</strong>`;
    }

    // ==========================================
    // STREET VIEW 360° IMMERSIVE VIEWPORT
    // ==========================================
    function openStreetViewMode() {
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
        const poi = watchtowerPOIs[currentWatchtowerPOI] || watchtowerPOIs['sete_quai'];
        alert(`📸 Plan de Situation & SIG Exporté :\n• Site : ${poi.name}\n• Coordonnées : ${poi.lat}° N, ${poi.lon}° E\n• Échelle : 1:500\n• Cartouche d'agrément conforme généré avec succès.`);
        logCockpit(`Export Plan de Situation : ${poi.name} généré.`, 'ok');
    }
'''

with open('scripts/section_js_part2.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos_sim_mode = text.find('function setSimulatorViewMode(mode) {')
if pos_sim_mode != -1:
    pos_toggle = text.find('function togglePlay4DSimulation()')
    if pos_toggle != -1:
        # find end of togglePlay4DSimulation
        pos_radar = text.find('// 2D RADAR ANIMATION', pos_toggle)
        if pos_radar != -1:
            text = text[:pos_sim_mode] + leaflet_watchtower_js.strip() + "\n\n    " + text[pos_radar:]
            print("Leaflet Real Map engine injected successfully into section_js_part2.py!")

with open('scripts/section_js_part2.py', 'w', encoding='utf-8') as f:
    f.write(text)
