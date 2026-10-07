import re
from pathlib import Path

TARGET = Path("/home/user/monorepo/scripts/build_html_dashboard.py")

with open(TARGET, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update loadScenario to call update3DCoordsTable(scenId)
old_load_scenario = """    function loadScenario(scenId) {
        currentScenarioId = scenId;
        currentScenarioStep = 0;
        const scen = companyData.scenarios.find(s => s.id === scenId) || companyData.scenarios[0];
        document.getElementById('sim-scenario-badge').innerText = scen.title.split('.')[0];
        renderScenarioStep();
    }"""

new_load_scenario = """    function loadScenario(scenId) {
        currentScenarioId = scenId;
        currentScenarioStep = 0;
        const scen = companyData.scenarios.find(s => s.id === scenId) || companyData.scenarios[0];
        document.getElementById('sim-scenario-badge').innerText = scen.title.split('.')[0];
        renderScenarioStep();
        update3DCoordsTable(scenId);
    }"""

if old_load_scenario in code:
    code = code.replace(old_load_scenario, new_load_scenario)
    print("Updated loadScenario!")

# 2. Update HR Tree & Fleet functions
old_hr_fleet_block = """    // TAB 8: HR & VEHICLE ORGANIGRAMME (WITH INTERACTIVE DRAG & POPUP)
    let hrCanvas, hrCtx;
    function initHrTree() {
        hrCanvas = document.getElementById('hr-tree-canvas');
        if (!hrCanvas) return;
        const rect = hrCanvas.getBoundingClientRect();
        hrCanvas.width = rect.width * window.devicePixelRatio;
        hrCanvas.height = rect.height * window.devicePixelRatio;
        hrCtx = hrCanvas.getContext('2d');
        hrCtx.scale(window.devicePixelRatio, window.devicePixelRatio);
        drawHrTree();

        hrCanvas.onclick = (e) => {
            const cRect = hrCanvas.getBoundingClientRect();
            const clickX = e.clientX - cRect.left;
            const clickY = e.clientY - cRect.top;
            const w = cRect.width;

            const nodes = [
                { id: 'emp_01', name: 'Laurent VIALA', role: 'Directeur Général', x: w/2, y: 50, type: 'person' },
                { id: 'emp_02', name: 'Sylvain CABROL', role: 'Conducteur Principal', x: w/2, y: 150, type: 'person' },
                { id: 'emp_03', name: 'Alain MARTIN', role: 'Chef Ch. Alès', x: w/4, y: 260, type: 'person' },
                { id: 'emp_04', name: 'Marc GOMEZ', role: 'Chef Ch. Sète', x: w/2, y: 260, type: 'person' },
                { id: 'eq_01', name: 'Pelle Liebherr 24t', role: 'Engin Affecté Alès', x: w/6, y: 380, type: 'vehicle' },
                { id: 'emp_08', name: 'Karim BENALI', role: 'Chef Canalisateurs', x: w/2, y: 380, type: 'person' },
                { id: 'eq_06', name: 'Scania 8x4 Bi-Benne', role: 'Camion Affecté Sète', x: (5*w)/6, y: 380, type: 'vehicle' }
            ];

            const hit = nodes.find(n => Math.abs(n.x - clickX) <= 70 && Math.abs(n.y - clickY) <= 22);
            if (hit) {
                if (hit.type === 'vehicle') openVehicleSheet('eq_01');
                else openEmployeeSheet(hit.id);
            }
        };
    }"""

idx_hr_start = code.find("// TAB 8: HR & VEHICLE ORGANIGRAMME")
idx_hr_end = code.find("// TAB 9: OPBTP SIGNAGE CALCULATOR")

if idx_hr_start != -1 and idx_hr_end != -1:
    new_hr_section = """    // TAB 8: HR & VEHICLE ORGANIGRAMME (WITH INTERACTIVE DRAG & POPUP)
    let hrCanvas, hrCtx;
    function initHrTree() {
        hrCanvas = document.getElementById('hr-tree-canvas');
        if (!hrCanvas) return;
        const rect = hrCanvas.getBoundingClientRect();
        hrCanvas.width = rect.width * window.devicePixelRatio;
        hrCanvas.height = rect.height * window.devicePixelRatio;
        hrCtx = hrCanvas.getContext('2d');
        hrCtx.scale(window.devicePixelRatio, window.devicePixelRatio);
        drawHrTree();

        hrCanvas.onclick = (e) => {
            const cRect = hrCanvas.getBoundingClientRect();
            const clickX = e.clientX - cRect.left;
            const clickY = e.clientY - cRect.top;
            const w = cRect.width;

            const nodes = [
                { id: 'emp_01', name: 'Laurent VIALA', x: w/2, y: 45, type: 'person' },
                { id: 'emp_02', name: 'Sylvain CABROL', x: w/4, y: 140, type: 'person' },
                { id: 'emp_11', name: 'Lucas VASSEUR', x: (3*w)/4, y: 140, type: 'person' },
                { id: 'emp_03', name: 'Alain MARTIN', x: w/6, y: 250, type: 'person' },
                { id: 'emp_04', name: 'Marc GOMEZ', x: w/2, y: 250, type: 'person' },
                { id: 'eq_topo_01', name: 'Leica iCON 70', x: (5*w)/6, y: 250, type: 'vehicle' },
                { id: 'eq_01', name: 'Pelle Liebherr 24t', x: w/10, y: 380, type: 'vehicle' },
                { id: 'eq_drone_01', name: 'DJI Matrice 350', x: (3*w)/10, y: 380, type: 'vehicle' },
                { id: 'emp_12', name: 'Franck ROCHE', x: w/2, y: 380, type: 'person' },
                { id: 'eq_robot_01', name: 'Robot Husqvarna DXR', x: (7*w)/10, y: 380, type: 'vehicle' },
                { id: 'eq_06', name: 'Scania 8x4 Bi-Benne', x: (9*w)/10, y: 380, type: 'vehicle' }
            ];

            const hit = nodes.find(n => Math.abs(n.x - clickX) <= 65 && Math.abs(n.y - clickY) <= 20);
            if (hit) {
                if (hit.type === 'vehicle') openVehicleSheet(hit.id);
                else openEmployeeSheet(hit.id);
            }
        };
    }

    function drawHrTree() {
        if (!hrCtx || !hrCanvas) return;
        const w = hrCanvas.width / window.devicePixelRatio;
        const h = hrCanvas.height / window.devicePixelRatio;
        hrCtx.clearRect(0, 0, w, h);

        const nodes = [
            { id: 'emp_01', name: 'Laurent VIALA', role: 'Directeur Général', x: w/2, y: 45, color: '#06b6d4', icon: '👔', type: 'person' },
            { id: 'emp_02', name: 'Sylvain CABROL', role: 'Conducteur Principal', x: w/4, y: 140, color: '#a855f7', icon: '👷‍♂️', type: 'person' },
            { id: 'emp_11', name: 'Lucas VASSEUR', role: 'Télépilote Drone LiDAR', x: (3*w)/4, y: 140, color: '#06b6d4', icon: '🛸', type: 'person' },
            { id: 'emp_03', name: 'Alain MARTIN', role: 'Chef Ch. Alès', x: w/6, y: 250, color: '#f59e0b', icon: '👷', type: 'person' },
            { id: 'emp_04', name: 'Marc GOMEZ', role: 'Chef Ch. Sète', x: w/2, y: 250, color: '#f59e0b', icon: '👷', type: 'person' },
            { id: 'eq_topo_01', name: 'Leica iCON 70 (3D)', role: 'Guidage Topo RTK', x: (5*w)/6, y: 250, color: '#c084fc', icon: '📐', type: 'vehicle' },
            { id: 'eq_01', name: 'Pelle Liebherr 24t', role: 'Engin Affecté Alès', x: w/10, y: 380, color: '#10b981', icon: '🚜', type: 'vehicle' },
            { id: 'eq_drone_01', name: 'DJI Matrice 350', role: 'Vecteur Drone LiDAR', x: (3*w)/10, y: 380, color: '#06b6d4', icon: '🛸', type: 'vehicle' },
            { id: 'emp_12', name: 'Franck ROCHE', role: 'Poseur Exosquelette HAPO', x: w/2, y: 380, color: '#10b981', icon: '🦾', type: 'person' },
            { id: 'eq_robot_01', name: 'Robot Husqvarna DXR', role: 'Sciage Télécommandé', x: (7*w)/10, y: 380, color: '#f59e0b', icon: '🤖', type: 'vehicle' },
            { id: 'eq_06', name: 'Scania 8x4 Bi-Benne', role: 'Camion Affecté Sète', x: (9*w)/10, y: 380, color: '#38bdf8', icon: '🚛', type: 'vehicle' }
        ];

        // Tree connectors
        hrCtx.strokeStyle = 'rgba(71, 85, 105, 0.6)';
        hrCtx.lineWidth = 1.5;
        hrCtx.beginPath();
        // Direction to Conduite & Drone
        hrCtx.moveTo(w/2, 45); hrCtx.lineTo(w/4, 140);
        hrCtx.moveTo(w/2, 45); hrCtx.lineTo((3*w)/4, 140);
        // Conduite to Chefs
        hrCtx.moveTo(w/4, 140); hrCtx.lineTo(w/6, 250);
        hrCtx.moveTo(w/4, 140); hrCtx.lineTo(w/2, 250);
        hrCtx.moveTo((3*w)/4, 140); hrCtx.lineTo((5*w)/6, 250);
        // Chefs to field equipment & operators
        hrCtx.moveTo(w/6, 250); hrCtx.lineTo(w/10, 380);
        hrCtx.moveTo(w/6, 250); hrCtx.lineTo((3*w)/10, 380);
        hrCtx.moveTo(w/2, 250); hrCtx.lineTo(w/2, 380);
        hrCtx.moveTo(w/2, 250); hrCtx.lineTo((7*w)/10, 380);
        hrCtx.moveTo(w/2, 250); hrCtx.lineTo((9*w)/10, 380);
        hrCtx.stroke();

        // Draw nodes
        nodes.forEach(n => {
            hrCtx.fillStyle = '#0f172a';
            hrCtx.strokeStyle = n.color;
            hrCtx.lineWidth = 2;
            hrCtx.beginPath();
            hrCtx.roundRect(n.x - 65, n.y - 20, 130, 40, 6);
            hrCtx.fill();
            hrCtx.stroke();

            hrCtx.fillStyle = '#fff';
            hrCtx.font = 'bold 10px Plus Jakarta Sans';
            hrCtx.textAlign = 'center';
            hrCtx.fillText(`${n.icon} ${n.name}`, n.x, n.y - 2);

            hrCtx.fillStyle = n.color;
            hrCtx.font = '8px JetBrains Mono';
            hrCtx.fillText(n.role, n.x, n.y + 11);
        });
    }

    function openEmployeeSheet(empId) {
        const emp = companyData.employees.find(e => e.id === empId) || companyData.employees[0];
        const content = document.getElementById('vehicle-sheet-content');
        content.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1rem; border-bottom:1px solid var(--border); padding-bottom:0.6rem;">
                <div>
                    <h3 style="font-size:1.15rem; font-weight:800; color:var(--cyan);">${emp.avatar} ${emp.name}</h3>
                    <div style="font-size:0.75rem; color:var(--text-muted);">${emp.role}</div>
                </div>
                <button class="btn-secondary" style="padding:0.2rem 0.5rem;" onclick="closeModal('modal-vehicle-sheet')">✕</button>
            </div>
            <div class="grid-2" style="margin-bottom:1rem;">
                <div style="background:var(--bg); padding:0.8rem; border-radius:8px; font-size:0.75rem; line-height:1.8;">
                    <div style="font-weight:700; color:var(--cyan); margin-bottom:0.2rem;">👤 Profil & Contrat :</div>
                    <div>Taux Horaire Chargé : <b>${emp.taux_horaire} €/h</b></div>
                    <div>Chantier Actuel : <b>${emp.project}</b></div>
                    <div>Visite Médicale : <b>${emp.visite_med} (Valide)</b></div>
                    <div>Heures Pointées Mois : <b>${emp.heures_mois} h</b></div>
                </div>
                <div style="background:var(--bg); padding:0.8rem; border-radius:8px; font-size:0.75rem; line-height:1.8;">
                    <div style="font-weight:700; color:var(--emerald); margin-bottom:0.2rem;">📜 Certifications & Habilitations :</div>
                    ${emp.habilitations.map(h => `<span class="obsidian-tag-chip" style="margin-right:4px;">${h}</span>`).join('')}
                    <div style="margin-top:0.6rem;">Score Sécurité : <b style="color:var(--emerald);">${emp.secu_score}%</b></div>
                </div>
            </div>
            <div style="display:flex; justify-content:space-between; gap:0.5rem;">
                <button class="btn-secondary" style="font-size:0.75rem;" onclick="alert('Téléchargement du dossier salarié (CV, Contrat, Visite médicale, AIPR).')">📄 Télécharger Dossier / CV</button>
                <button class="btn-primary" style="font-size:0.75rem;" onclick="alert('Pointage d\\'heures validé pour le mois en cours.')">✅ Valider Pointage</button>
            </div>
        `;
        openModal('modal-vehicle-sheet');
    }

    function openAddEntityModal() { openModal('modal-add-vehicle'); }

"""
    code = code[:idx_hr_start] + new_hr_section + code[idx_hr_end:]
    print("Updated HR organigramme section!")

# 3. Update Fleet CRUD section
idx_fleet_start = code.find("// TAB 6: FLEET CRUD")
idx_fleet_end = code.find("// TAB 1: COCKPIT ACTIONS")

if idx_fleet_start != -1 and idx_fleet_end != -1:
    new_fleet_section = """    // TAB 6: FLEET CRUD & FILTERING
    function filterFleet(cat, btn) {
        fleetFilter = cat;
        document.querySelectorAll('#fleet-filter-bar button').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
        renderFleetGrid();
    }

    function renderFleetGrid() {
        const grid = document.getElementById('fleet-cards-grid');
        const select = document.getElementById('dispatch-fleet-select');
        const countDisplay = document.getElementById('hud-fleet-count');
        if (!grid || !select) return;

        const allFleet = companyData.fleet || [];
        const filtered = allFleet.filter(f => {
            if (fleetFilter === 'all') return true;
            if (fleetFilter === 'excavator') return f.category === 'excavator';
            if (fleetFilter === 'drone') return f.category === 'drone';
            if (fleetFilter === 'exosquelette') return f.category === 'exosquelette';
            if (fleetFilter === 'robotique') return f.category === 'robotique' || f.category === 'topo_guidage';
            if (fleetFilter === 'truck') return f.category === 'truck';
            if (fleetFilter === 'compactor') return f.category === 'compactor' || f.category === 'paver';
            return f.category === fleetFilter;
        });

        if (countDisplay) countDisplay.innerText = `${allFleet.length} Unités (${filtered.length} affichées)`;

        select.innerHTML = allFleet.map(f => `
            <option value="${f.id}">${f.icon || '🚜'} ${f.name} (${f.immat})</option>
        `).join('');

        grid.innerHTML = filtered.map(f => `
            <div class="fleet-card" onclick="openVehicleSheet('${f.id}')">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div style="display:flex; align-items:center; gap:0.5rem;">
                        <span style="font-size:1.6rem;">${f.icon || '🚜'}</span>
                        <div>
                            <div style="font-weight:700; font-size:0.85rem; color:var(--text-main);">${f.name}</div>
                            <div style="font-size:0.7rem; color:var(--cyan); font-family:var(--font-mono);">${f.immat} — ${f.type}</div>
                        </div>
                    </div>
                    <span class="card-badge" style="color:var(--emerald);">${f.status}</span>
                </div>
                ${f.tech_specs ? `<div style="font-size:0.68rem; color:var(--text-muted); margin:0.3rem 0; font-style:italic;">${f.tech_specs}</div>` : ''}
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.4rem; font-size:0.7rem; background:var(--bg); padding:0.5rem; border-radius:6px; margin-top:0.3rem;">
                    <div>Horamètre : <b>${f.horametre} h</b></div>
                    <div>Énergie/Batterie : <b>${f.fuel_pct}%</b></div>
                    <div>VGP : <b style="color:var(--emerald);">${f.vgp_status}</b> (${f.vgp_date})</div>
                    <div>Coût Horaire : <b style="color:var(--cyan);">${f.cout_horaire} €/h</b></div>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.72rem; color:var(--text-muted); margin-top:0.4rem;">
                    <span><b>Opérateur / Pilote :</b> ${f.operator}</span>
                    <button class="btn-danger" style="padding:0.2rem 0.5rem; font-size:0.65rem;" onclick="event.stopPropagation(); deleteVehicle('${f.id}')">🗑️ Retirer</button>
                </div>
            </div>
        `).join('');
    }

    function openAddVehicleModal() { openModal('modal-add-vehicle'); }

    function submitAddVehicle() {
        const name = document.getElementById('new-v-name').value.trim();
        const cat = document.getElementById('new-v-cat').value;
        const immat = document.getElementById('new-v-immat').value.trim();
        const horametre = parseInt(document.getElementById('new-v-horametre').value || 0);
        const conso = parseFloat(document.getElementById('new-v-conso').value || 12.0);
        const proj = document.getElementById('new-v-project').value;
        const op = document.getElementById('new-v-operator').value.trim() || 'À affecter';

        if (!name || !immat) {
            alert('Veuillez renseigner au moins le nom et l’immatriculation.');
            return;
        }

        const newVeh = {
            id: 'eq_' + Date.now(),
            name: name,
            type: cat.toUpperCase(),
            category: cat,
            immat: immat,
            horametre: horametre,
            fuel_pct: 100,
            status: "Disponible",
            vgp_date: "2027-04-01",
            vgp_status: "Valide",
            current_project: proj,
            operator: op,
            caces_req: "CACES R482 / Habilitation",
            conso_lh: conso,
            puissance_kw: 100,
            godet_m3: 1.0,
            cout_horaire: 75.0,
            valeur_achat: 150000,
            icon: cat === 'drone' ? '🛸' : (cat === 'exosquelette' ? '🦾' : (cat === 'robotique' ? '🤖' : '🚜'))
        };

        companyData.fleet.push(newVeh);
        renderFleetGrid();
        closeModal('modal-add-vehicle');
        logCockpit(`🚜 Nouvel équipement ${name} (${immat}) ajouté à la flotte.`, 'ok');
        alert(`Équipement ${name} enregistré avec succès !`);
    }

    function deleteVehicle(id) {
        if (!confirm("Êtes-vous sûr de vouloir supprimer cet équipement du parc matériel ?")) return;
        const idx = companyData.fleet.findIndex(f => f.id === id);
        if (idx !== -1) {
            const removed = companyData.fleet.splice(idx, 1)[0];
            renderFleetGrid();
            logCockpit(`🗑️ Équipement ${removed.name} retiré de la flotte.`, 'warn');
        }
    }

    function openVehicleSheet(id) {
        const veh = companyData.fleet.find(f => f.id === id) || companyData.fleet[0];
        const content = document.getElementById('vehicle-sheet-content');
        content.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1rem; border-bottom:1px solid var(--border); padding-bottom:0.6rem;">
                <div style="display:flex; align-items:center; gap:0.6rem;">
                    <span style="font-size:2rem;">${veh.icon || '🚜'}</span>
                    <div>
                        <h3 style="font-size:1.15rem; font-weight:800; color:var(--cyan);">${veh.name}</h3>
                        <div style="font-size:0.75rem; color:var(--text-muted); font-family:var(--font-mono);">${veh.immat} — ${veh.type}</div>
                    </div>
                </div>
                <button class="btn-secondary" style="padding:0.2rem 0.5rem;" onclick="closeModal('modal-vehicle-sheet')">✕</button>
            </div>
            ${veh.tech_specs ? `<div style="background:rgba(6,182,212,0.1); border:1px solid rgba(6,182,212,0.3); padding:0.5rem 0.8rem; border-radius:6px; font-size:0.72rem; color:var(--cyan); margin-bottom:0.8rem;"><b>🚀 Spécifications Techniques :</b> ${veh.tech_specs}</div>` : ''}
            <div class="grid-2" style="margin-bottom:1rem;">
                <div style="background:var(--bg); padding:0.8rem; border-radius:8px; font-size:0.75rem; line-height:1.8;">
                    <div style="font-weight:700; color:var(--cyan); margin-bottom:0.2rem;">📊 Caractéristiques & Énergie :</div>
                    <div>Puissance Moteur : <b>${veh.puissance_kw ? veh.puissance_kw + ' kW' : 'N/A (Ergonomique)'}</b></div>
                    <div>Capacité / Godet / Charge : <b>${veh.godet_m3 ? veh.godet_m3 + ' m³' : 'Système Portatif'}</b></div>
                    <div>Consommation Moyenne : <b>${veh.conso_lh ? veh.conso_lh + ' L/h (GNR)' : 'Électrique / Passif'}</b></div>
                    <div>Coût Horaire Chargé : <b>${veh.cout_horaire || 75.0} €/h</b></div>
                    <div>Valeur d'Achat : <b>${(veh.valeur_achat || 120000).toLocaleString('fr-FR')} €</b></div>
                </div>
                <div style="background:var(--bg); padding:0.8rem; border-radius:8px; font-size:0.75rem; line-height:1.8;">
                    <div style="font-weight:700; color:var(--emerald); margin-bottom:0.2rem;">🛡️ Suivi VGP & Réglementation :</div>
                    <div>Horamètre Total : <b>${veh.horametre} heures</b></div>
                    <div>Niveau Énergie / Batterie : <b>${veh.fuel_pct}%</b></div>
                    <div>Contrôle VGP : <b style="color:var(--emerald);">${veh.vgp_status}</b> (${veh.vgp_date})</div>
                    <div>Opérateur / Télépilote : <b>${veh.operator}</b></div>
                    <div>Habilitation Requise : <b>${veh.caces_req}</b></div>
                </div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; gap:0.5rem; flex-wrap:wrap;">
                <button class="btn-secondary" style="font-size:0.75rem;" onclick="refuelVehicle('${veh.id}')">⚡ Recharger / Plein Carburant (100%)</button>
                <button class="btn-primary" style="font-size:0.75rem;" onclick="closeModal('modal-vehicle-sheet'); quickAction('simulator');">🛰️ Visualiser dans Watch Tower 3D</button>
            </div>
        `;
        openModal('modal-vehicle-sheet');
    }

    function refuelVehicle(id) {
        const veh = companyData.fleet.find(f => f.id === id);
        if (veh) {
            veh.fuel_pct = 100;
            renderFleetGrid();
            openVehicleSheet(id);
            logCockpit(`⛽ Plein de carburant / recharge effectué pour l'équipement ${veh.name}.`, 'ok');
            alert(`Plein / Recharge validé pour ${veh.name} (100%).`);
        }
    }

    function executeDispatch() {
        const fleetId = document.getElementById('dispatch-fleet-select').value;
        const dest = document.getElementById('dispatch-dest-select').value;
        const item = companyData.fleet.find(f => f.id === fleetId);
        if (item) {
            item.current_project = dest;
            renderFleetGrid();
            logCockpit(`🚚 Équipement ${item.name} transféré vers ${dest}.`, 'ok');
            alert(`Transfert validé : ${item.name} est maintenant affecté à ${dest}.`);
        }
    }

"""
    code = code[:idx_fleet_start] + new_fleet_section + code[idx_fleet_end:]
    print("Updated Fleet section!")

with open(TARGET, "w", encoding="utf-8") as f:
    f.write(code)

print("Saved build_html_dashboard.py successfully!")
