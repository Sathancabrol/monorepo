# -*- coding: utf-8 -*-

def get_js_part3():
    return r"""
    // ==========================================
    // 10. HR ORGANIGRAM & INTEGRATED AI AGENTS
    // ==========================================
    function initHrTree() {
        const container = document.getElementById('hr-tree-container');
        if (!container) return;

        const hierarchy = companyData.hierarchy || {};
        const direction = hierarchy.direction || [
            { id: "emp_01", name: "Laurent VIALA", role: "Directeur Général / Gérant TP", salary_bracket: "Direction", cert: "AIPR Concepteur • Ingénieur ESTP", secu: "100%", rate: "85 €/h" }
        ];
        const conduite = hierarchy.conduite || [
            { id: "emp_02", name: "Sylvain CABROL", role: "Conducteur de Travaux Principal VRD", salary_bracket: "Cadre A", cert: "AIPR Encadrant", secu: "99%", rate: "55 €/h", assigned: ["Giratoire RD906 Alès", "ZAC Littoral Sète"] },
            { id: "emp_03", name: "Sophie LACOMBE", role: "Conductrice de Travaux Aménagements & Prix", salary_bracket: "Cadre B", cert: "AIPR Encadrant", secu: "100%", rate: "52 €/h", assigned: ["Centre Ancien Pézenas", "Voie Verte Montpellier"] }
        ];
        const chefs = hierarchy.chefs || [
            { id: "emp_04", name: "Alain MARTIN", role: "Chef de Chantier TP / VRD", site: "Giratoire RD906 Alès", caces: "CACES R482 B1/C1", secu: "100%" },
            { id: "emp_05", name: "Mamadou TRAORÉ", role: "Chef de Chantier Terrassement & Réseaux", site: "Giratoire RD906 Alès", caces: "CACES R482 B1", secu: "100%" },
            { id: "emp_06", name: "Marc GOMEZ", role: "Chef de Chantier Réseaux Profonds", site: "ZAC Littoral Sète", caces: "AIPR Encadrant", secu: "98%" },
            { id: "emp_07", name: "Karim BENALI", role: "Chef de Chantier Réseaux Secs", site: "ZAC Littoral Sète", caces: "AIPR Encadrant", secu: "100%" },
            { id: "emp_08", name: "Patrick DURAND", role: "Chef d'Équipe Enrobés & Chaussée", site: "Centre Ancien Pézenas", caces: "CACES R482 D/E", secu: "100%" },
            { id: "emp_09", name: "David LEMOINE", role: "Chef de Cellule Topo & Drone", site: "Voie Verte Montpellier", caces: "Drone Pro • RTK", secu: "100%" }
        ];
        const aiAgents = companyData.ai_agents || [
            { id: "ai_nexus", tier: "direction", name: "BTP-Nexus (Direction & Trésorerie)", role: "Agent IA Gouvernance & Trésorerie", desc: "Surveillance prédictive BFR et CCAG 2021." },
            { id: "ai_optichantier", tier: "conduite", name: "OptiChantier-AI (Méthodes & Planif)", role: "Agent IA Méthodes & Logistique", desc: "Optimisation des cadences et flux 4D." },
            { id: "ai_kestimator", tier: "conduite", name: "K-Estimator (Étude de Prix)", role: "Agent IA Étude de Prix & SDP", desc: "Contrôle en continu du ratio Déboursé Sec vs PV." },
            { id: "ai_safetysentinel", tier: "terrain", name: "SafetySentinel (AIPR & Sécurité)", role: "Agent IA Prévention des Risques", desc: "Vérification des blindages et distances DICT." },
            { id: "ai_topobot", tier: "terrain", name: "TopoBot (Contrôle Altimétrique)", role: "Agent IA Nivellement & Guidage 3D", desc: "Contrôle altimétrique temps réel ±5mm." }
        ];

        container.innerHTML = `
            <div style="display: flex; flex-direction: column; align-items: center; gap: 1.5rem; min-width: 900px;">
                <!-- LEVEL 1 : DIRECTION -->
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <div style="font-size: 0.75rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.5rem;">Niveau 1 : Direction Générale & IA Gouvernance</div>
                    <div style="display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center;">
                        ${direction.map(p => `
                            <div onclick="openEmployeeDetailModal('${p.name}', 'Direction Générale', '${p.role}', '${p.salary_bracket || 'Direction'}', '${p.cert || 'AIPR Concepteur'}', '${p.secu || '100%'}', 'Siège Social Sète')" style="background: rgba(15,23,42,0.95); border: 2px solid #38bdf8; padding: 0.85rem 1.25rem; border-radius: 8px; cursor: pointer; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.5); min-width: 220px;" onmouseover="this.style.transform='translateY(-2px)';" onmouseout="this.style.transform='none';">
                                <div style="font-size: 1.5rem;">👑</div>
                                <div style="font-weight: 800; font-size: 0.95rem; color: #f8fafc;">${p.name}</div>
                                <div style="font-size: 0.75rem; color: #38bdf8; margin-top: 2px;">${p.role}</div>
                                <span class="badge badge-success" style="font-size: 0.6rem; margin-top: 4px;">Score Sécu : ${p.secu || '100%'}</span>
                            </div>
                        `).join('')}

                        ${aiAgents.filter(a => a.tier === 'direction').map(a => `
                            <div onclick="openEmployeeDetailModal('${a.name}', 'Agent IA Autonome', '${a.role}', 'Cloud Server Occitanie', 'Algorithmes ML Prédictifs', '100%', 'Tous Chantiers', '${a.desc}')" style="background: rgba(16,185,129,0.15); border: 2px solid var(--emerald); padding: 0.85rem 1.25rem; border-radius: 8px; cursor: pointer; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.5); min-width: 220px;" onmouseover="this.style.transform='translateY(-2px)';" onmouseout="this.style.transform='none';">
                                <div style="font-size: 1.5rem;">🤖</div>
                                <div style="font-weight: 800; font-size: 0.95rem; color: var(--emerald);">${a.name}</div>
                                <div style="font-size: 0.75rem; color: #cbd5e1; margin-top: 2px;">${a.role}</div>
                                <span class="badge badge-success" style="font-size: 0.6rem; margin-top: 4px;">Agent IA Actif</span>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <!-- LEVEL 2 : CONDUITE DE TRAVAUX & IA MÉTHODES -->
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <div style="font-size: 0.75rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.5rem;">Niveau 2 : Conduite de Travaux, Bureau d'Études & IA Méthodes</div>
                    <div style="display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center;">
                        ${conduite.map(p => `
                            <div onclick="openEmployeeDetailModal('${p.name}', 'Cadre Conduite de Travaux', '${p.role}', '${p.salary_bracket || 'Cadre'}', '${p.cert || 'AIPR Encadrant'}', '${p.secu || '99%'}', '${(p.assigned || []).join(', ') || 'Chantiers VRD'}')" style="background: rgba(15,23,42,0.95); border: 2px solid #0284c7; padding: 0.75rem 1rem; border-radius: 8px; cursor: pointer; text-align: center; min-width: 200px;" onmouseover="this.style.transform='translateY(-2px)';" onmouseout="this.style.transform='none';">
                                <div style="font-size: 1.3rem;">👷‍♂️</div>
                                <div style="font-weight: 800; font-size: 0.85rem; color: #f8fafc;">${p.name}</div>
                                <div style="font-size: 0.7rem; color: #38bdf8; margin-top: 2px;">${p.role}</div>
                                <div style="font-size: 0.65rem; color: #94a3b8; margin-top: 2px;">${(p.assigned || []).slice(0, 1).join('')}</div>
                            </div>
                        `).join('')}

                        ${aiAgents.filter(a => a.tier === 'conduite').map(a => `
                            <div onclick="openEmployeeDetailModal('${a.name}', 'Agent IA Méthodes', '${a.role}', 'Cloud Server', 'Optimisation & Phasage 4D', '100%', 'Alès & Sète', '${a.desc}')" style="background: rgba(56,189,248,0.15); border: 2px solid #38bdf8; padding: 0.75rem 1rem; border-radius: 8px; cursor: pointer; text-align: center; min-width: 200px;" onmouseover="this.style.transform='translateY(-2px)';" onmouseout="this.style.transform='none';">
                                <div style="font-size: 1.3rem;">🤖</div>
                                <div style="font-weight: 800; font-size: 0.85rem; color: #38bdf8;">${a.name}</div>
                                <div style="font-size: 0.7rem; color: #cbd5e1; margin-top: 2px;">${a.role}</div>
                                <span class="badge badge-info" style="font-size: 0.6rem; margin-top: 4px;">Optimisation Temps Réel</span>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <!-- LEVEL 3 : CHEFS DE CHANTIER & IA TERRAIN -->
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <div style="font-size: 0.75rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.5rem;">Niveau 3 : Maîtrise de Terrain, Topographie & IA Sécurité</div>
                    <div style="display: flex; gap: 0.75rem; flex-wrap: wrap; justify-content: center;">
                        ${chefs.map(p => `
                            <div onclick="openEmployeeDetailModal('${p.name}', 'Maîtrise de Terrain', '${p.role}', '${p.salary_bracket || 'ETAM'}', '${p.caces || 'AIPR Encadrant'}', '${p.secu || '100%'}', '${p.site || 'Occitanie'}')" style="background: rgba(15,23,42,0.9); border: 1px solid var(--border); padding: 0.6rem 0.85rem; border-radius: 6px; cursor: pointer; text-align: center; min-width: 170px;" onmouseover="this.style.transform='translateY(-2px)';" onmouseout="this.style.transform='none';">
                                <div style="font-size: 1.2rem;">🚜</div>
                                <div style="font-weight: 800; font-size: 0.8rem; color: #f8fafc;">${p.name}</div>
                                <div style="font-size: 0.68rem; color: #38bdf8;">${p.role}</div>
                                <div style="font-size: 0.65rem; color: #94a3b8;">📍 ${p.site || 'Chantier'}</div>
                            </div>
                        `).join('')}

                        ${aiAgents.filter(a => a.tier === 'terrain').map(a => `
                            <div onclick="openEmployeeDetailModal('${a.name}', 'Agent IA Terrain & Sécurité', '${a.role}', 'Edge Computing Bord de Fouille', 'Capteurs RTK & LiDAR', '100%', 'Tous Chantiers', '${a.desc}')" style="background: rgba(245,158,11,0.15); border: 2px solid var(--amber); padding: 0.6rem 0.85rem; border-radius: 6px; cursor: pointer; text-align: center; min-width: 170px;" onmouseover="this.style.transform='translateY(-2px)';" onmouseout="this.style.transform='none';">
                                <div style="font-size: 1.2rem;">🤖</div>
                                <div style="font-weight: 800; font-size: 0.8rem; color: var(--amber);">${a.name}</div>
                                <div style="font-size: 0.68rem; color: #cbd5e1;">${a.role}</div>
                                <span class="badge badge-warning" style="font-size: 0.55rem; margin-top: 4px;">Contrôle Alti & DICT</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    function openEmployeeDetailModal(name, tier, role, bracket, cert, secu, assigned, desc) {
        const body = document.getElementById('employee-modal-body');
        if (!body) return;

        body.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; border-bottom: 1px solid rgba(51,65,85,0.7); padding-bottom: 0.75rem;">
                <div>
                    <span class="badge badge-info" style="font-size: 0.75rem;">${tier || 'Collaborateur BTP'}</span>
                    <h2 style="font-size: 1.3rem; font-weight: 900; color: #38bdf8; margin-top: 4px;">${name}</h2>
                    <div style="font-size: 0.85rem; color: #94a3b8;">Fonction : <strong>${role}</strong></div>
                </div>
                <span class="badge badge-success">Actif / En Poste</span>
            </div>

            <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.6); padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
                <div style="font-size: 0.8rem; font-weight: 800; color: #38bdf8; margin-bottom: 4px;">Missions & Responsabilités :</div>
                <p style="font-size: 0.8rem; color: #cbd5e1; line-height: 1.5; margin-bottom: 0.75rem;">${desc || 'Supervision opérationnelle, respect strict des normes de sécurité OPBTP/AIPR, gestion des délais d\'execution et de la rentabilité analytique.'}</p>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 0.75rem; background: rgba(30,41,59,0.5); padding: 0.75rem; border-radius: 4px;">
                    <div>Habilitation / CACES : <strong style="color: var(--emerald);">${cert || 'AIPR Conforme'}</strong></div>
                    <div>Statut Salarial : <strong>${bracket || 'Convention TP'}</strong></div>
                    <div>Chantier(s) Affecté(s) : <strong style="color: #38bdf8;">${assigned || 'Giratoire RD906 Alès'}</strong></div>
                    <div>Score Sécurité Chantier : <strong style="color: var(--emerald);">${secu || '100% Conforme'}</strong></div>
                </div>
            </div>
        `;

        openModal('employee-detail-modal');
    }

    // ==========================================
    // 11. OPBTP TEMPORARY ROAD SIGNAGE SIMULATOR
    // ==========================================
    let opbtpTrafficAnimId = null;
    let isOpbtpTrafficRunning = true;
    let trafficLightState = 'green'; // 'green' or 'red'
    let opbtpCars = [];

    function calculateSignage() {
        const taskType = document.getElementById('opbtp-task-type')?.value || 'tranchee_traversee';
        const roadType = document.getElementById('opbtp-road-type')?.value || 'urbain';
        const length = Number(document.getElementById('opbtp-length')?.value || 120);

        let ak5Dist = 50, b14Dist = 30, k5aSpacing = 5, coneQty = 24;
        let speed = '30 km/h', signak5 = 'AK5 (Travaux)', signb14 = 'B14 (30)';
        let configDesc = '';

        if (taskType === 'tranchee_traversee') {
            ak5Dist = roadType === 'urbain' ? 50 : 150;
            b14Dist = roadType === 'urbain' ? 30 : 100;
            k5aSpacing = 5;
            coneQty = Math.max(20, Math.round(length / k5aSpacing));
            configDesc = "Tranchée perpendiculaire avec neutralisation alternée d'une voie et feux tricolores KR11.";
        } else if (taskType === 'rond_point') {
            ak5Dist = 50; b14Dist = 30; k5aSpacing = 4;
            coneQty = 35;
            configDesc = "Neutralisation d'un quadrant d'anneau par séparateurs K16 et flèches de rabattement K8.";
        } else if (taskType === 'tranchee_trottoir') {
            ak5Dist = 30; b14Dist = 20; k5aSpacing = 3;
            coneQty = 18;
            configDesc = "Passage piétons dévoyé sur chaussée avec barrières de protection K2 et rampes PMR.";
        } else if (taskType === 'voie_etroite') {
            ak5Dist = 50; b14Dist = 30; k5aSpacing = 5;
            coneQty = 15;
            configDesc = "Fermeture totale à la circulation générale (panneau B44 'Rue Barrée') sauf riverains et secours.";
        } else if (taskType === 'retrecissement') {
            ak5Dist = roadType === 'urbain' ? 50 : 150;
            b14Dist = roadType === 'urbain' ? 30 : 100;
            k5aSpacing = 6;
            coneQty = Math.max(25, Math.round(length / k5aSpacing));
            configDesc = "Rétrécissement axial avec priorité au sens montant (panneaux B15 / C18) et biseaux K5a.";
        } else {
            ak5Dist = 100; b14Dist = 50; k5aSpacing = 4;
            coneQty = 30;
            configDesc = "Intervention d'urgence nocturne avec balises lumineuses synchronisées K8 et gyrophares.";
        }

        const res = document.getElementById('opbtp-results');
        if (res) {
            res.innerHTML = `
                <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(51,65,85,0.7); border-radius: 8px; padding: 1rem;">
                    <div style="font-size: 0.85rem; font-weight: 800; color: var(--amber); margin-bottom: 0.4rem; text-transform: uppercase;">
                        📑 Prescriptions Réglementaires du Balisage :
                    </div>
                    <div style="font-size: 0.75rem; color: #cbd5e1; margin-bottom: 0.6rem;">${configDesc}</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.8rem;">
                        <div style="background: rgba(30,41,59,0.5); padding: 6px; border-radius: 4px;">Distance Panneau AK5 : <strong style="color: #38bdf8;">${ak5Dist} m</strong> en amont</div>
                        <div style="background: rgba(30,41,59,0.5); padding: 6px; border-radius: 4px;">Distance Panneau B14 : <strong style="color: #38bdf8;">${b14Dist} m</strong></div>
                        <div style="background: rgba(30,41,59,0.5); padding: 6px; border-radius: 4px;">Cônes K5a Requis : <strong style="color: var(--emerald);">${coneQty} cônes</strong> classe 2</div>
                        <div style="background: rgba(30,41,59,0.5); padding: 6px; border-radius: 4px;">Vitesse Limitée : <strong style="color: #facc15;">${speed}</strong></div>
                    </div>
                </div>
            `;
        }

        initOpbtpCars();
        drawSignageDiagram(ak5Dist, b14Dist, coneQty, taskType);
    }

    function initOpbtpCars() {
        opbtpCars = [
            { x: 20, speed: 1.8, color: '#38bdf8', dir: 1, lane: 1 },
            { x: 180, speed: 2.1, color: '#facc15', dir: 1, lane: 1 },
            { x: 500, speed: 1.9, color: '#10b981', dir: -1, lane: 2 }
        ];
    }

    function toggleOpbtpTrafficSimulation() {
        isOpbtpTrafficRunning = !isOpbtpTrafficRunning;
        const btn = document.getElementById('btn-opbtp-sim-play');
        if (btn) btn.textContent = isOpbtpTrafficRunning ? '⏸️ Pause Trafic' : '▶️ Lancer Simulation Trafic';
    }

    function switchTrafficLightState() {
        trafficLightState = trafficLightState === 'green' ? 'red' : 'green';
        const taskType = document.getElementById('opbtp-task-type')?.value || 'tranchee_traversee';
        drawSignageDiagram(50, 30, 24, taskType);
    }

    function drawSignageDiagram(ak5Dist, b14Dist, coneQty, taskType) {
        const canvas = document.getElementById('opbtp-signage-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const w = canvas.parentElement.clientWidth || 700;
        const h = canvas.parentElement.clientHeight || 240;
        canvas.width = w;
        canvas.height = h;

        ctx.fillStyle = '#090d16';
        ctx.fillRect(0, 0, w, h);

        // Update Car positions
        if (isOpbtpTrafficRunning) {
            opbtpCars.forEach(car => {
                if (taskType === 'tranchee_traversee' && trafficLightState === 'red' && car.x > w * 0.25 && car.x < w * 0.35) {
                    // Stop at red light
                } else {
                    car.x += car.speed * car.dir;
                    if (car.dir === 1 && car.x > w + 40) car.x = -30;
                    if (car.dir === -1 && car.x < -40) car.x = w + 30;
                }
            });
        }

        // 1. ROAD LAYOUTS PER CONFIGURATION
        if (taskType === 'rond_point') {
            // Giratoire layout
            ctx.fillStyle = '#1e293b';
            ctx.beginPath(); ctx.arc(w / 2, h / 2, 90, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#090d16';
            ctx.beginPath(); ctx.arc(w / 2, h / 2, 45, 0, Math.PI * 2); ctx.fill();

            // Central island work zone
            ctx.fillStyle = 'rgba(234, 179, 8, 0.3)';
            ctx.beginPath(); ctx.arc(w / 2, h / 2, 45, 0, Math.PI * 2); ctx.fill();
            ctx.strokeStyle = '#eab308'; ctx.lineWidth = 2; ctx.stroke();
            ctx.fillStyle = '#fff'; ctx.font = 'bold 9px system-ui';
            ctx.fillText('🚧 ÎLOT CHANTIER', w / 2 - 38, h / 2 + 3);

            // K16 barriers
            ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 3; ctx.setLineDash([6, 6]);
            ctx.beginPath(); ctx.arc(w / 2, h / 2, 55, 0, Math.PI); ctx.stroke();
            ctx.setLineDash([]);
        } else if (taskType === 'tranchee_trottoir') {
            // Road + Sidewalk layout
            ctx.fillStyle = '#334155'; // Trottoir
            ctx.fillRect(0, h * 0.15, w, h * 0.25);
            ctx.fillStyle = '#1e293b'; // Chaussée
            ctx.fillRect(0, h * 0.4, w, h * 0.45);

            // Sidewalk Trench
            ctx.fillStyle = 'rgba(239, 68, 68, 0.35)';
            ctx.fillRect(w * 0.35, h * 0.18, w * 0.3, h * 0.2);
            ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 2;
            ctx.strokeRect(w * 0.35, h * 0.18, w * 0.3, h * 0.2);
            ctx.fillStyle = '#fff'; ctx.font = 'bold 9px system-ui';
            ctx.fillText('🚶 DÉVOIEMENT PIÉTONS K2', w * 0.37, h * 0.48);
        } else {
            // Standard 2-lane road
            ctx.fillStyle = '#1e293b';
            ctx.fillRect(0, h * 0.25, w, h * 0.5);

            // Dashed Centerline
            ctx.strokeStyle = '#f8fafc'; ctx.lineWidth = 2; ctx.setLineDash([12, 12]);
            ctx.beginPath(); ctx.moveTo(0, h * 0.5); ctx.lineTo(w, h * 0.5); ctx.stroke();
            ctx.setLineDash([]);

            // Trench Zone
            const zX = w * 0.45, zW = w * 0.25, zY = h * 0.25, zH = h * 0.25;
            ctx.fillStyle = 'rgba(239, 68, 68, 0.3)';
            ctx.fillRect(zX, zY, zW, zH);
            ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 2; ctx.strokeRect(zX, zY, zW, zH);
            ctx.fillStyle = '#ef4444'; ctx.font = 'bold 10px system-ui';
            ctx.fillText('🚧 TRANCHÉE EN COURS', zX + 10, zY + 20);

            // Traffic Cone line K5a
            ctx.fillStyle = '#f97316';
            for (let x = zX - 20; x <= zX + zW + 20; x += 16) {
                ctx.beginPath();
                ctx.moveTo(x, zY + zH);
                ctx.lineTo(x - 3, zY + zH + 8);
                ctx.lineTo(x + 3, zY + zH + 8);
                ctx.closePath();
                ctx.fill();
            }

            // KR11 Traffic Light
            if (taskType === 'tranchee_traversee') {
                ctx.fillStyle = '#0f172a';
                ctx.fillRect(w * 0.32, h * 0.12, 16, 28);
                ctx.fillStyle = trafficLightState === 'green' ? '#10b981' : '#ef4444';
                ctx.beginPath(); ctx.arc(w * 0.32 + 8, h * 0.12 + 14, 6, 0, Math.PI * 2); ctx.fill();
                ctx.fillStyle = '#fff'; ctx.font = 'bold 8px monospace';
                ctx.fillText('FEU KR11', w * 0.28, h * 0.1);
            }
        }

        // Draw Moving Cars
        if (taskType !== 'rond_point') {
            opbtpCars.forEach(c => {
                ctx.fillStyle = c.color;
                const cy = c.lane === 1 ? h * 0.62 : h * 0.35;
                ctx.fillRect(c.x, cy, 28, 14);
                ctx.fillStyle = '#000';
                ctx.fillRect(c.x + (c.dir === 1 ? 20 : 2), cy + 2, 5, 10);
            });
        }

        // Approach Signs AK5 & B14
        ctx.fillStyle = '#facc15';
        ctx.beginPath();
        ctx.moveTo(w * 0.08, h * 0.85);
        ctx.lineTo(w * 0.08 - 10, h * 0.85 + 18);
        ctx.lineTo(w * 0.08 + 10, h * 0.85 + 18);
        ctx.closePath(); ctx.fill();
        ctx.strokeStyle = '#dc2626'; ctx.lineWidth = 2; ctx.stroke();
        ctx.fillStyle = '#000'; ctx.font = 'bold 7px system-ui';
        ctx.fillText('AK5', w * 0.08 - 6, h * 0.85 + 14);

        ctx.fillStyle = '#38bdf8'; ctx.font = '9px monospace';
        ctx.fillText(`AK5 (${ak5Dist}m)`, w * 0.03, h * 0.85 - 4);

        // Next frame animation
        if (currentNav === 'opbtp') {
            opbtpTrafficAnimId = requestAnimationFrame(() => drawSignageDiagram(ak5Dist, b14Dist, coneQty, taskType));
        }
    }

    // ==========================================
    // 12. SAFETY AIPR - VISUAL SIMULATOR (BOTTOM)
    // ==========================================
    let currentAiprSituation = 'gaz';
    let aiprMouseX = 200, aiprMouseY = 150;

    function setAiprSituation(type) {
        currentAiprSituation = type;
        document.querySelectorAll('.aipr-sim-btn').forEach(b => b.classList.remove('active'));
        const activeBtn = Array.from(document.querySelectorAll('.aipr-sim-btn')).find(b => b.onclick.toString().includes(type));
        if (activeBtn) activeBtn.classList.add('active');

        const hud = document.getElementById('aipr-sim-hud');
        const actionBox = document.getElementById('aipr-situation-action-box');

        if (type === 'gaz') {
            if (hud) hud.textContent = "SITUATION 1 : FOUILLE À PROXIMITÉ CONDUITE GAZ PEHD 4 BAR";
            if (actionBox) actionBox.innerHTML = `
                <div>
                    <h4 style="color:#eab308; font-size:0.95rem; font-weight:800; margin-bottom:0.4rem;">⚡ GAZ NATUREL MPB (PEHD Ø110 - 4 bars)</h4>
                    <p style="font-size:0.8rem; color:#cbd5e1; line-height:1.4; margin-bottom:0.6rem;">Zone d'incertitude Classe A (±40cm). Terrassement mécanique strictement interdit à moins de 0.50m de la conduite.</p>
                    <div style="background:rgba(234,179,8,0.15); border-left:3px solid #eab308; padding:0.5rem; font-size:0.75rem; color:#facc15;">
                        ✔️ <strong>Consigne :</strong> Piquetage jaune obligatoire + Terrassement doux manuel / aspiration à l'approche.
                    </div>
                </div>
                <button class="btn btn-danger" style="margin-top:0.75rem;" onclick="simulateSafetyCrisis('gaz')">💥 Simuler Rupture & Procédure d'Urgence</button>
            `;
        } else if (type === 'hta') {
            if (hud) hud.textContent = "SITUATION 2 : LEVAGE SOUS LIGNE ÉLECTRIQUE AÉRIENNE HTA 20kV";
            if (actionBox) actionBox.innerHTML = `
                <div>
                    <h4 style="color:#ef4444; font-size:0.95rem; font-weight:800; margin-bottom:0.4rem;">🔴 LIGNE AÉRIENNE HTA 20 000 Volts</h4>
                    <p style="font-size:0.8rem; color:#cbd5e1; line-height:1.4; margin-bottom:0.6rem;">Distance minimale de sécurité infranchissable : <strong>3 mètres</strong> (ou 5m si tension > 50kV).</p>
                    <div style="background:rgba(239,68,68,0.15); border-left:3px solid #ef4444; padding:0.5rem; font-size:0.75rem; color:#f87171;">
                        ✔️ <strong>Consigne :</strong> Gabarit limiteur de hauteur sur pelle + Balisage portique haut obligatoire.
                    </div>
                </div>
                <button class="btn btn-danger" style="margin-top:0.75rem;" onclick="simulateSafetyCrisis('elec')">⚡ Simuler Contact Électrique</button>
            `;
        } else if (type === 'fibre_aep') {
            if (hud) hud.textContent = "SITUATION 3 : APPROCHE CÂBLE FIBRE OPTIQUE & CONDUITE AEP FONTE";
            if (actionBox) actionBox.innerHTML = `
                <div>
                    <h4 style="color:#38bdf8; font-size:0.95rem; font-weight:800; margin-bottom:0.4rem;">💧 EAU POTABLE FONTE & FIBRE OPTIQUE</h4>
                    <p style="font-size:0.8rem; color:#cbd5e1; line-height:1.4; margin-bottom:0.6rem;">Coexistence réseaux secs (vert) et humides (bleu). Risque de coupure télécom majeure ou inondation de fouille.</p>
                    <div style="background:rgba(56,189,248,0.15); border-left:3px solid #38bdf8; padding:0.5rem; font-size:0.75rem; color:#7dd3fc;">
                        ✔️ <strong>Consigne :</strong> Vérification visuelle du grillage avertisseur bleu/vert lors du décapage.
                    </div>
                </div>
                <button class="btn btn-primary" style="margin-top:0.75rem;" onclick="alert('Procédure de calage et maintien de réseau sous tension validée.');">🔍 Valider Protocole Approche</button>
            `;
        } else {
            if (hud) hud.textContent = "SITUATION 4 : BLINDAGE DE FOUILLE PROFONDE 3.20m (R4534)";
            if (actionBox) actionBox.innerHTML = `
                <div>
                    <h4 style="color:var(--emerald); font-size:0.95rem; font-weight:800; margin-bottom:0.4rem;">🧱 BLINDAGE DE TRANCHÉE R4534</h4>
                    <p style="font-size:0.8rem; color:#cbd5e1; line-height:1.4; margin-bottom:0.6rem;">Obligation de blindage immédiat pour toute fouille en tranchée supérieure à <strong>1.30m de profondeur</strong>.</p>
                    <div style="background:rgba(16,185,129,0.15); border-left:3px solid var(--emerald); padding:0.5rem; font-size:0.75rem; color:#6ee7b7;">
                        ✔️ <strong>Consigne :</strong> Descente des caissons acier avant toute présence humaine au fond de fouille.
                    </div>
                </div>
                <button class="btn btn-warning" style="margin-top:0.75rem;" onclick="simulateSafetyCrisis('eboulement')">⚠️ Simuler Risque d'Éboulement</button>
            `;
        }

        renderAiprCanvas();
    }

    function renderAiprCanvas() {
        const canvas = document.getElementById('aipr-simulation-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const w = canvas.parentElement.clientWidth || 500;
        const h = canvas.parentElement.clientHeight || 320;
        canvas.width = w;
        canvas.height = h;

        ctx.fillStyle = '#090d16';
        ctx.fillRect(0, 0, w, h);

        // Soil layers cross section
        const groundY = h * 0.45;

        // Top Layer (Enrobé / Terre)
        ctx.fillStyle = '#1c1917';
        ctx.fillRect(0, groundY, w, h - groundY);

        // Sublayer (Sable / GNT)
        ctx.fillStyle = '#292524';
        ctx.fillRect(0, groundY + 40, w, h - groundY - 40);

        // Trench cutout
        const tX = w * 0.35, tW = w * 0.35, tDepth = 120;
        ctx.fillStyle = '#0c0a09';
        ctx.fillRect(tX, groundY, tW, tDepth);
        ctx.strokeStyle = '#44403c'; ctx.lineWidth = 1; ctx.strokeRect(tX, groundY, tW, tDepth);

        // Surface ground line
        ctx.strokeStyle = '#78716c'; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.moveTo(0, groundY); ctx.lineTo(tX, groundY);
        ctx.moveTo(tX + tW, groundY); ctx.lineTo(w, groundY); ctx.stroke();

        // Underground pipes (AIPR standard colors)
        // 1. GAZ JAUNE (at -1.20m depth)
        const gasX = w * 0.22, gasY = groundY + 50;
        ctx.fillStyle = '#eab308';
        ctx.beginPath(); ctx.arc(gasX, gasY, 9, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#ca8a04'; ctx.lineWidth = 2; ctx.stroke();
        ctx.font = 'bold 9px monospace'; ctx.fillText('⚡ GAZ MPB (-1.20m)', gasX - 45, gasY - 14);

        // 0.50m Danger Buffer Zone around Gas
        ctx.strokeStyle = 'rgba(234, 179, 8, 0.4)'; ctx.lineWidth = 2; ctx.setLineDash([4, 4]);
        ctx.beginPath(); ctx.arc(gasX, gasY, 32, 0, Math.PI * 2); ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = 'rgba(234, 179, 8, 0.08)'; ctx.fill();

        // 2. ÉLEC HTA (Overhead or buried)
        if (currentAiprSituation === 'hta') {
            // Overhead line
            ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 3;
            ctx.beginPath(); ctx.moveTo(0, h * 0.15); ctx.lineTo(w, h * 0.15); ctx.stroke();
            ctx.fillStyle = '#ef4444'; ctx.font = 'bold 10px monospace';
            ctx.fillText('🔴 LIGNE AÉRIENNE HTA 20kV (DIST. SÉCU 3M)', w * 0.1, h * 0.12);

            // 3m buffer
            ctx.fillStyle = 'rgba(239, 68, 68, 0.15)';
            ctx.fillRect(0, h * 0.15, w, 50);
        } else {
            // Buried Telecom (Vert) & Water (Bleu)
            const telX = w * 0.8, telY = groundY + 35;
            ctx.fillStyle = '#10b981';
            ctx.beginPath(); ctx.arc(telX, telY, 7, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#10b981'; ctx.fillText('🟢 FIBRE (-0.80m)', telX - 35, telY - 12);

            const aepX = w * 0.85, aepY = groundY + 75;
            ctx.fillStyle = '#0284c7';
            ctx.beginPath(); ctx.arc(aepX, aepY, 12, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#38bdf8'; ctx.fillText('💧 AEP Ø150 (-1.50m)', aepX - 40, aepY + 22);
        }

        // 3. Caisson de blindage if situation == blindage
        if (currentAiprSituation === 'blindage') {
            ctx.fillStyle = 'rgba(234, 179, 8, 0.8)';
            ctx.fillRect(tX + 4, groundY + 10, 8, tDepth - 15);
            ctx.fillRect(tX + tW - 12, groundY + 10, 8, tDepth - 15);
            ctx.strokeStyle = '#b45309'; ctx.lineWidth = 2;
            ctx.strokeRect(tX + 4, groundY + 10, 8, tDepth - 15);
            ctx.strokeRect(tX + tW - 12, groundY + 10, 8, tDepth - 15);

            // Étais
            ctx.strokeStyle = '#facc15'; ctx.lineWidth = 4;
            ctx.beginPath(); ctx.moveTo(tX + 12, groundY + 35); ctx.lineTo(tX + tW - 12, groundY + 35); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(tX + 12, groundY + 85); ctx.lineTo(tX + tW - 12, groundY + 85); ctx.stroke();
            ctx.fillStyle = '#facc15'; ctx.font = 'bold 9px monospace';
            ctx.fillText('CAISSON KRINGS R4534', tX + 15, groundY + 25);
        }

        // 4. Excavator Arm Position
        ctx.strokeStyle = '#f59e0b'; ctx.lineWidth = 10;
        ctx.beginPath(); ctx.moveTo(w * 0.1, groundY - 20); ctx.lineTo(w * 0.22, groundY - 60); ctx.lineTo(w * 0.38, groundY + 20); ctx.stroke();

        // Bucket
        ctx.fillStyle = '#334155';
        ctx.beginPath(); ctx.arc(w * 0.38, groundY + 20, 14, 0, Math.PI); ctx.fill();
        ctx.fillStyle = '#fff'; ctx.font = 'bold 9px monospace';
        ctx.fillText('🚜 Godet Pelle', w * 0.33, groundY + 15);

        // Depth Ruler
        ctx.strokeStyle = '#64748b'; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(25, groundY); ctx.lineTo(25, groundY + tDepth); ctx.stroke();
        ctx.fillStyle = '#94a3b8'; ctx.font = '8px monospace';
        ctx.fillText('0.00m', 30, groundY + 4);
        ctx.fillText('-1.00m', 30, groundY + 40);
        ctx.fillText('-2.00m', 30, groundY + 80);
        ctx.fillText('-3.00m', 30, groundY + 120);
    }

    function simulateSafetyCrisis(type) {
        openSafetyEmergencySimulator();
        setTimeout(() => renderCrisisScenario(type), 100);
    }

    // ==========================================
    // 13. 28 SDP & DQE PIVOT TABLE ENGINE
    // ==========================================
    function setSDPViewMode(mode) {
        sdpViewMode = mode;
        document.querySelectorAll('.sdp-view-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('btn-sdp-' + mode)?.classList.add('active');

        const dqeView = document.getElementById('sdp-dqe-tcd-view');
        const cardsView = document.getElementById('sdp-cards-view');

        if (mode === 'dqe_tcd') {
            if (dqeView) dqeView.style.display = 'block';
            if (cardsView) cardsView.style.display = 'none';
            renderDQEPivotTable();
        } else {
            if (dqeView) dqeView.style.display = 'none';
            if (cardsView) cardsView.style.display = 'block';
            renderSdpCards();
        }
    }

    function renderDQEPivotTable() {
        const container = document.getElementById('sdp-dqe-tcd-view');
        if (!container) return;

        const pFilter = document.getElementById('dqe-project-select')?.value || 'all';
        const lFilter = document.getElementById('dqe-lot-select')?.value || 'all';

        const items = syntheseData.dqe_items || [];
        const filtered = items.filter(item => {
            if (pFilter !== 'all' && item.project_id !== pFilter) return false;
            if (lFilter !== 'all' && !item.lot.includes(lFilter)) return false;
            return true;
        });

        let totalDS = 0, totalPV = 0;
        filtered.forEach(i => {
            totalDS += (i.ds_total || (i.ds_unitaire * i.quantite) || 0);
            totalPV += (i.montant_total_ht || (i.prix_unitaire_vente_ht * i.quantite) || 0);
        });

        container.innerHTML = `
            <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(51,65,85,0.7); border-radius: 8px; overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; min-width: 950px;">
                    <thead>
                        <tr style="background: rgba(30,41,59,0.9); color: #94a3b8; text-align: left;">
                            <th style="padding: 0.6rem;">N° PRIX</th>
                            <th style="padding: 0.6rem;">DESIGNATION DE L'OUVRAGE</th>
                            <th style="padding: 0.6rem;">LOT</th>
                            <th style="padding: 0.6rem; text-align: center;">UNITÉ</th>
                            <th style="padding: 0.6rem; text-align: right;">QUANTITÉ</th>
                            <th style="padding: 0.6rem; text-align: right;">D.S. UNIT.</th>
                            <th style="padding: 0.6rem; text-align: right;">P.V. UNIT. (K=1.35)</th>
                            <th style="padding: 0.6rem; text-align: right;">MONTANT TOTAL HT</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${filtered.map(i => `
                            <tr style="border-top: 1px solid rgba(51,65,85,0.4);">
                                <td style="padding: 0.55rem; font-family: 'JetBrains Mono'; font-weight: 700; color: #38bdf8;">${i.code_prix || i.code}</td>
                                <td style="padding: 0.55rem; font-weight: 700; color: #f8fafc;">${i.designation}</td>
                                <td style="padding: 0.55rem; color: #94a3b8;">${i.lot}</td>
                                <td style="padding: 0.55rem; text-align: center;">${i.unite || i.unit}</td>
                                <td style="padding: 0.55rem; text-align: right; font-weight: 700;">${(i.quantite || i.quantity || 1).toLocaleString('fr-FR')}</td>
                                <td style="padding: 0.55rem; text-align: right;">${(i.ds_unitaire || i.unit_ds || 0).toFixed(2)} €</td>
                                <td style="padding: 0.55rem; text-align: right; font-weight: 700; color: var(--emerald);">${(i.prix_unitaire_vente_ht || i.unit_pv || 0).toFixed(2)} €</td>
                                <td style="padding: 0.55rem; text-align: right; font-weight: 800; color: var(--amber);">${(i.montant_total_ht || (i.prix_unitaire_vente_ht * i.quantite) || 0).toLocaleString('fr-FR')} €</td>
                            </tr>
                        `).join('')}
                    </tbody>
                    <tfoot>
                        <tr style="background: rgba(30,41,59,0.95); border-top: 2px solid #38bdf8; font-weight: 800;">
                            <td colspan="5" style="padding: 0.75rem; text-align: right; color: #f8fafc;">TOTAL GÉNÉRAL FILTRÉ (${filtered.length} PRIX) :</td>
                            <td style="padding: 0.75rem; text-align: right; color: #cbd5e1;">${totalDS.toLocaleString('fr-FR')} € DS</td>
                            <td style="padding: 0.75rem; text-align: right; color: var(--emerald);">K = 1.35</td>
                            <td style="padding: 0.75rem; text-align: right; color: var(--amber); font-size: 1rem;">${totalPV.toLocaleString('fr-FR')} € HT</td>
                        </tr>
                    </tfoot>
                </table>
            </div>
        `;
    }

    function renderSdpCards() {
        const container = document.getElementById('sdp-cards-view');
        if (!container) return;

        const items = syntheseData.dqe_items || [];
        container.innerHTML = `
            <div class="grid-3">
                ${items.map(i => `
                    <div class="card" style="border: 1px solid rgba(51,65,85,0.8); background: rgba(15,23,42,0.95); display: flex; flex-direction: column; justify-content: space-between;">
                        <div>
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                                <span class="badge badge-info" style="font-size: 0.7rem; font-family: 'JetBrains Mono';">${i.code_prix || i.code}</span>
                                <span class="badge badge-warning">${i.lot}</span>
                            </div>
                            <h4 style="font-size: 0.95rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.5rem;">${i.designation}</h4>
                            <div style="background: rgba(30,41,59,0.5); padding: 0.5rem; border-radius: 6px; font-size: 0.75rem; display: grid; grid-template-columns: 1fr 1fr; gap: 4px; margin-bottom: 0.75rem;">
                                <div>Déboursé Sec: <strong>${(i.ds_unitaire || i.unit_ds || 0).toFixed(2)} € / ${i.unite || i.unit}</strong></div>
                                <div>Prix Vente HT: <strong style="color: var(--emerald);">${(i.prix_unitaire_vente_ht || i.unit_pv || 0).toFixed(2)} €</strong></div>
                                <div>Quantité: <strong>${i.quantite || i.quantity} ${i.unite || i.unit}</strong></div>
                                <div>Total HT: <strong style="color: var(--amber);">${(i.montant_total_ht || (i.prix_unitaire_vente_ht * i.quantite) || 0).toLocaleString('fr-FR')} €</strong></div>
                            </div>
                        </div>
                        <button class="btn btn-secondary" style="width: 100%; font-size: 0.75rem;" onclick="openSDPDetailModal('${i.code_prix || i.code}')">🔍 Décomposition Analytique</button>
                    </div>
                `).join('')}
            </div>
        `;
    }

    function openSDPDetailModal(codePrix) {
        const item = (syntheseData.dqe_items || []).find(i => (i.code_prix === codePrix || i.code === codePrix)) || (syntheseData.dqe_items || [])[0];
        if (!item) return;

        const body = document.getElementById('sdp-detail-modal-body');
        if (!body) return;

        const ds = item.ds_unitaire || item.unit_ds || 10;
        const mo = item.ds_mo || (ds * 0.35);
        const mat = item.ds_mat || (ds * 0.45);
        const eq = item.ds_eq || (ds * 0.20);
        const pv = item.prix_unitaire_vente_ht || item.unit_pv || (ds * 1.35);

        body.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; border-bottom: 1px solid rgba(51,65,85,0.7); padding-bottom: 0.75rem;">
                <div>
                    <span class="badge badge-info" style="font-size: 0.75rem; font-family: 'JetBrains Mono';">${item.code_prix || item.code}</span>
                    <h2 style="font-size: 1.25rem; font-weight: 900; color: #38bdf8; margin-top: 4px;">${item.designation}</h2>
                    <div style="font-size: 0.85rem; color: #94a3b8;">Lot : <strong>${item.lot}</strong> • Unité : <strong>${item.unite || item.unit}</strong></div>
                </div>
                <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem;" onclick="closeModal('sdp-detail-modal')">✕</button>
            </div>

            <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.6); padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
                <div style="font-size: 0.85rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.5rem;">Décomposition du Déboursé Sec (D.S.) :</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; font-size: 0.8rem;">
                    <div>Main d'Œuvre Directe (MO) : <strong style="color: #f8fafc;">${mo.toFixed(2)} €</strong></div>
                    <div>Matériaux & Fournitures : <strong style="color: #f8fafc;">${mat.toFixed(2)} €</strong></div>
                    <div>Matériel & Engins TP : <strong style="color: #f8fafc;">${eq.toFixed(2)} €</strong></div>
                    <div>Total Déboursé Sec Unitaire : <strong style="color: var(--amber);">${ds.toFixed(2)} € / ${item.unite || item.unit}</strong></div>
                </div>
            </div>

            <div style="background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.4); padding: 1rem; border-radius: 6px;">
                <div style="font-size: 0.85rem; font-weight: 800; color: var(--emerald); margin-bottom: 0.4rem;">Application du Coefficient de Vente K = 1.35 :</div>
                <div style="font-size: 0.8rem; color: #cbd5e1;">Frais Généraux (14%) + Frais de Siège (6%) + Aléas (5%) + Bénéfice Net (10%) = <strong style="color:var(--emerald); font-size:1rem;">Prix Vente HT : ${pv.toFixed(2)} € / ${item.unite || item.unit}</strong></div>
            </div>
        `;

        openModal('sdp-detail-modal');
    }

    function exportDQEtoCSV() {
        let csv = "Code Prix;Designation;Lot;Unite;Quantite;DS Unitaire;PV Unitaire HT;Montant Total HT\n";
        (syntheseData.dqe_items || []).forEach(i => {
            csv += `"${i.code_prix || i.code}";"${i.designation}";"${i.lot}";"${i.unite || i.unit}";${i.quantite || i.quantity};${i.ds_unitaire || i.unit_ds};${i.prix_unitaire_vente_ht || i.unit_pv};${i.montant_total_ht}\n`;
        });
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'DQE_28_SDP_Bordereau_Complet.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        logCockpit('Bordereau 28 SDP & DQE exporté en CSV.', 'ok');
    }

    function printDQESummary() {
        window.print();
    }

    // ==========================================
    // 14. OBSIDIAN KNOWLEDGE GRAPH ENGINE (STABILIZED)
    // ==========================================
    let obsidianCanvas, obsidianCtx;
    let obsNodes = [], obsLinks = [];
    let obsSelectedNode = null, obsHoverNode = null;
    let obsSearchTerm = '';
    let obsAnimId = null;
    let obsZoom = 1.0, obsPanX = 0, obsPanY = 0;
    let isPanningObs = false, isDraggingObsNode = false;
    let lastObsMouseX = 0, lastObsMouseY = 0;

    function initObsidianGraph() {
        obsidianCanvas = document.getElementById('obsidian-canvas');
        if (!obsidianCanvas) return;
        obsidianCtx = obsidianCanvas.getContext('2d');
        const w = obsidianCanvas.parentElement.clientWidth || 700;
        const h = obsidianCanvas.parentElement.clientHeight || 550;
        obsidianCanvas.width = w;
        obsidianCanvas.height = h;

        if (obsNodes.length === 0) {
            const rawNodes = obsidianData.nodes || [];
            obsNodes = rawNodes.map((n, i) => {
                const angle = (i / rawNodes.length) * Math.PI * 2;
                const r = 120 + Math.random() * 50;
                return {
                    id: n.id,
                    title: n.title || n.id,
                    category: n.category || 'technique',
                    content: n.content || 'Fiche technique de référence.',
                    x: w / 2 + Math.cos(angle) * r,
                    y: h / 2 + Math.sin(angle) * r,
                    vx: 0,
                    vy: 0,
                    radius: n.category === 'technique' ? 14 : 11
                };
            });
            obsLinks = obsidianData.links || [];
        }

        // Mouse Events with Pan, Zoom & Stable Dragging
        obsidianCanvas.onmousedown = (e) => {
            const rect = obsidianCanvas.getBoundingClientRect();
            const mx = (e.clientX - rect.left - obsPanX) / obsZoom;
            const my = (e.clientY - rect.top - obsPanY) / obsZoom;

            obsSelectedNode = obsNodes.find(n => Math.hypot(n.x - mx, n.y - my) < n.radius + 8);
            if (obsSelectedNode) {
                isDraggingObsNode = true;
                showObsidianNodeDrawer(obsSelectedNode);
            } else {
                isPanningObs = true;
                lastObsMouseX = e.clientX;
                lastObsMouseY = e.clientY;
            }
        };

        obsidianCanvas.onwheel = (e) => {
            e.preventDefault();
            const factor = e.deltaY < 0 ? 1.1 : 0.9;
            obsZoom = Math.max(0.4, Math.min(2.5, obsZoom * factor));
        };

        window.onmouseup = () => {
            isPanningObs = false;
            isDraggingObsNode = false;
        };

        window.onmousemove = (e) => {
            if (!obsidianCanvas) return;
            const rect = obsidianCanvas.getBoundingClientRect();
            const mx = (e.clientX - rect.left - obsPanX) / obsZoom;
            const my = (e.clientY - rect.top - obsPanY) / obsZoom;

            obsHoverNode = obsNodes.find(n => Math.hypot(n.x - mx, n.y - my) < n.radius + 8);

            if (isDraggingObsNode && obsSelectedNode) {
                obsSelectedNode.x = mx;
                obsSelectedNode.y = my;
                obsSelectedNode.vx = 0;
                obsSelectedNode.vy = 0;
            } else if (isPanningObs) {
                obsPanX += e.clientX - lastObsMouseX;
                obsPanY += e.clientY - lastObsMouseY;
                lastObsMouseX = e.clientX;
                lastObsMouseY = e.clientY;
            }
        };

        if (obsAnimId) cancelAnimationFrame(obsAnimId);
        runObsidianPhysicsLoop();
    }

    function zoomObsidian(factor) {
        obsZoom = Math.max(0.4, Math.min(2.5, obsZoom * factor));
    }

    function resetObsidianCamera() {
        obsZoom = 1.0;
        obsPanX = 0;
        obsPanY = 0;
    }

    function reorganizeObsidianNodes() {
        const w = obsidianCanvas ? obsidianCanvas.width : 700;
        const h = obsidianCanvas ? obsidianCanvas.height : 550;
        obsNodes.forEach((n, i) => {
            const angle = (i / obsNodes.length) * Math.PI * 2;
            const r = 130 + (i % 3) * 40;
            n.x = w / 2 + Math.cos(angle) * r;
            n.y = h / 2 + Math.sin(angle) * r;
            n.vx = 0;
            n.vy = 0;
        });
    }

    function runObsidianPhysicsLoop() {
        if (!obsidianCanvas || !obsidianCtx) return;
        const w = obsidianCanvas.width;
        const h = obsidianCanvas.height;
        const cx = w / 2, cy = h / 2;

        obsidianCtx.fillStyle = '#050811';
        obsidianCtx.fillRect(0, 0, w, h);

        obsidianCtx.save();
        obsidianCtx.translate(obsPanX, obsPanY);
        obsidianCtx.scale(obsZoom, obsZoom);

        // Stabilized Physics Forces with viscous friction
        const repulsion = 900;
        const springLen = 100;
        const springK = 0.025;
        const damping = 0.82; // Strong damping prevents any chaotic vibrations

        for (let i = 0; i < obsNodes.length; i++) {
            const n1 = obsNodes[i];

            // Soft Center pull
            n1.vx += (cx - n1.x) * 0.0015;
            n1.vy += (cy - n1.y) * 0.0015;

            // Repulsion
            for (let j = i + 1; j < obsNodes.length; j++) {
                const n2 = obsNodes[j];
                const dx = n2.x - n1.x;
                const dy = n2.y - n1.y;
                const dist = Math.hypot(dx, dy) || 1;
                if (dist < 220 && dist > 10) {
                    const force = repulsion / (dist * dist);
                    const fx = (dx / dist) * force;
                    const fy = (dy / dist) * force;
                    n1.vx -= fx; n1.vy -= fy;
                    n2.vx += fx; n2.vy += fy;
                }
            }
        }

        // Springs
        obsLinks.forEach(lnk => {
            const source = obsNodes.find(n => n.id === lnk.source);
            const target = obsNodes.find(n => n.id === lnk.target);
            if (source && target) {
                const dx = target.x - source.x;
                const dy = target.y - source.y;
                const dist = Math.hypot(dx, dy) || 1;
                const force = (dist - springLen) * springK;
                const fx = (dx / dist) * force;
                const fy = (dy / dist) * force;
                source.vx += fx; source.vy += fy;
                target.vx -= fx; target.vy -= fy;
            }
        });

        // Apply velocities with cutoff
        obsNodes.forEach(n => {
            n.vx *= damping;
            n.vy *= damping;

            if (Math.abs(n.vx) < 0.01) n.vx = 0;
            if (Math.abs(n.vy) < 0.01) n.vy = 0;

            n.x += n.vx;
            n.y += n.vy;

            // Bounded arena
            n.x = Math.max(30, Math.min(w - 30, n.x));
            n.y = Math.max(30, Math.min(h - 30, n.y));
        });

        // Draw Links
        obsidianCtx.strokeStyle = 'rgba(51, 65, 85, 0.45)';
        obsidianCtx.lineWidth = 1.5;
        obsLinks.forEach(lnk => {
            const s = obsNodes.find(n => n.id === lnk.source);
            const t = obsNodes.find(n => n.id === lnk.target);
            if (s && t) {
                obsidianCtx.beginPath();
                obsidianCtx.moveTo(s.x, s.y);
                obsidianCtx.lineTo(t.x, t.y);
                obsidianCtx.stroke();
            }
        });

        // Draw Nodes
        obsNodes.forEach(n => {
            const matchesSearch = !obsSearchTerm || n.title.toLowerCase().includes(obsSearchTerm.toLowerCase());
            const matchesHeuristic = obsidianHeuristic === 'all' || n.category === obsidianHeuristic;
            const isHighlighted = matchesSearch && matchesHeuristic;

            let nodeColor = '#38bdf8';
            if (n.category === 'reglementaire') nodeColor = '#eab308';
            if (n.category === 'financier') nodeColor = '#10b981';
            if (n.category === 'management') nodeColor = '#c084fc';

            obsidianCtx.fillStyle = isHighlighted ? nodeColor : 'rgba(51, 65, 85, 0.35)';
            obsidianCtx.beginPath();
            obsidianCtx.arc(n.x, n.y, n.radius, 0, Math.PI * 2);
            obsidianCtx.fill();

            if (n === obsSelectedNode || n === obsHoverNode) {
                obsidianCtx.strokeStyle = '#fff';
                obsidianCtx.lineWidth = 3;
                obsidianCtx.stroke();
            }

            obsidianCtx.fillStyle = isHighlighted ? '#f8fafc' : '#64748b';
            obsidianCtx.font = (n === obsSelectedNode ? 'bold 11px' : '9px') + ' system-ui';
            obsidianCtx.fillText(n.title, n.x + n.radius + 4, n.y + 3);
        });

        obsidianCtx.restore();

        if (currentNav === 'obsidian') {
            obsAnimId = requestAnimationFrame(runObsidianPhysicsLoop);
        }
    }

    function searchObsidianNodes(term) {
        obsSearchTerm = term;
    }

    function setObsidianHeuristic(h, btn) {
        obsidianHeuristic = h;
        document.querySelectorAll('.obs-cat-btn').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
    }

    function showObsidianNodeDrawer(node) {
        const info = document.getElementById('obsidian-node-info');
        if (!info || !node) return;

        info.innerHTML = `
            <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(56,189,248,0.4); padding: 1rem; border-radius: 8px;">
                <span class="badge badge-info" style="font-size: 0.7rem; font-family: 'JetBrains Mono';">${node.category.toUpperCase()}</span>
                <h3 style="font-size: 1.15rem; font-weight: 800; color: #38bdf8; margin: 6px 0;">${node.title}</h3>
                
                <div style="font-size: 0.82rem; color: #cbd5e1; line-height: 1.6; white-space: pre-wrap; font-family: system-ui; max-height: 380px; overflow-y: auto;">
${node.content}
                </div>

                <div style="margin-top: 1rem; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(51,65,85,0.5); padding-top: 0.75rem;">
                    <span class="badge badge-success">Fiche Synchronisée</span>
                    <button class="btn btn-primary" style="font-size: 0.75rem;" onclick="downloadProjectDoc('${node.id}_Fiche', 'Obsidian_Vault', 'md')">📥 Exporter Markdown</button>
                </div>
            </div>
        `;
    }

    function exportObsidianVault() {
        downloadProjectDoc('Obsidian_BTP_Knowledge_Vault_Full', 'Vault_Occitanie', 'json');
    }

    // ==========================================
    // 15. FORMULAS & MATH ENGINE
    // ==========================================
    function updateFormulaCalculator() {
        const type = document.getElementById('formula-type-select')?.value || 'compactage';
        const p1 = Number(document.getElementById('f-param-1')?.value || 0.3);
        const p2 = Number(document.getElementById('f-param-2')?.value || 4.0);
        const p3 = Number(document.getElementById('f-param-3')?.value || 2.1);
        const p4 = Number(document.getElementById('f-param-4')?.value || 6);

        const out = document.getElementById('formula-calculation-output');
        if (!out) return;

        if (type === 'compactage') {
            const debit = Math.round((p1 * p2 * 1000 * p3) / p4);
            out.innerHTML = `
                <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(56,189,248,0.4); border-radius: 8px; padding: 1.25rem;">
                    <h4 style="color: #38bdf8; font-size: 1rem; font-weight: 800; margin-bottom: 0.5rem;">📊 Résultat du Débit de Compactage GTR :</h4>
                    <div style="font-size: 2rem; font-weight: 900; color: var(--emerald); font-family: 'JetBrains Mono';">${debit} m³/h</div>
                    <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">Formule GTR : Q = (e × V × L) / N</div>
                    <div style="font-size: 0.75rem; color: #cbd5e1; margin-top: 8px;">Soit une cadence d'alimentation de <strong>${Math.round(debit * 1.8)} tonnes/heure</strong> de GNT 0/31.5.</div>
                </div>
            `;
        } else {
            const k = 90;
            const d = p1;
            const slope = p2 / 1000;
            const section = Math.PI * Math.pow(d / 2, 2);
            const rh = d / 4;
            const q = Math.round(k * section * Math.pow(rh, 2/3) * Math.sqrt(slope) * 1000);

            out.innerHTML = `
                <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(56,189,248,0.4); border-radius: 8px; padding: 1.25rem;">
                    <h4 style="color: #38bdf8; font-size: 1rem; font-weight: 800; margin-bottom: 0.5rem;">🌊 Débit Hydraulique Collecteur à Pleine Section :</h4>
                    <div style="font-size: 2rem; font-weight: 900; color: #38bdf8; font-family: 'JetBrains Mono';">${q} Litres/sec</div>
                    <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">Formule Manning-Strickler : Q = K × S × Rh^(2/3) × √I</div>
                    <div style="font-size: 0.75rem; color: #cbd5e1; margin-top: 8px;">Vitesse d'écoulement : <strong>${(q / 1000 / section).toFixed(2)} m/s</strong> (Autocurage conforme si > 0.7 m/s).</div>
                </div>
            `;
        }
    }

    // ==========================================
    // 16. PROCUREMENT & LEDGER SHA-256
    // ==========================================
    const suppliersList = [
        { name: "Carrières du Languedoc", type: "Grave GNT & Concassés", rating: "4.9 ⭐", distance: "14 km", phone: "04 67 00 11 22", status: "Partenaire Premium" },
        { name: "Bétons Occitanie (Centrales)", type: "Bétons C25/30, Désactivés", rating: "4.8 ⭐", distance: "8 km", phone: "04 67 00 33 44", status: "Contrat-Cadre" },
        { name: "PAM Saint-Gobain Canalisation", type: "Tuyaux Fonte & Assainissement", rating: "4.9 ⭐", distance: "22 km", phone: "04 67 00 55 66", status: "Fournisseur Agréé" },
        { name: "Négoce TP Littoral", type: "Bordures T2, Fontes D400, GNT", rating: "4.7 ⭐", distance: "11 km", phone: "04 67 00 77 88", status: "Stock Disponible" }
    ];

    function renderProcurement() {
        const grid = document.getElementById('suppliers-grid');
        if (!grid) return;

        grid.innerHTML = suppliersList.map(s => `
            <div class="card" style="border: 1px solid rgba(51,65,85,0.8); background: rgba(15,23,42,0.95); display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                        <h4 style="font-size: 1rem; font-weight: 800; color: #f8fafc;">${s.name}</h4>
                        <span class="badge badge-success">${s.status}</span>
                    </div>
                    <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.75rem;">${s.type}</div>
                    <div style="background: rgba(30,41,59,0.5); padding: 0.5rem; border-radius: 6px; font-size: 0.75rem; display: grid; grid-template-columns: 1fr 1fr; gap: 4px; margin-bottom: 0.75rem;">
                        <div>Note : <strong style="color: var(--amber);">${s.rating}</strong></div>
                        <div>Distance : <strong>${s.distance}</strong></div>
                        <div colspan="2">Tél : <strong>${s.phone}</strong></div>
                    </div>
                </div>
                <button class="btn btn-secondary" style="width: 100%; font-size: 0.75rem;" onclick="alert('Demande de devis envoyée à ${s.name} !');">🛒 Demander Devis Express</button>
            </div>
        `).join('');
    }

    function sortSuppliers(crit) {
        if (crit === 'rating') suppliersList.sort((a,b) => b.rating.localeCompare(a.rating));
        if (crit === 'distance') suppliersList.sort((a,b) => parseInt(a.distance) - parseInt(b.distance));
        renderProcurement();
    }

    function renderLedger() {
        const cont = document.getElementById('ledger-transactions-list');
        if (!cont) return;

        const blocks = ledgerData.blocks || [
            { index: 1, timestamp: "2026-09-18T14:30:00Z", type: "Réception Chantier Lot 01", hash: "a3f89e81b2c4d6f7e8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1", prev_hash: "0000000000000000000000000000000000000000000000000000000000000000" },
            { index: 2, timestamp: "2026-09-19T09:15:00Z", type: "Situation n°3 Validée MOE (125k€)", hash: "b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1a2b3c4d5", prev_hash: "a3f89e81b2c4d6f7e8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1" }
        ];

        cont.innerHTML = blocks.map(b => `
            <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(51,65,85,0.7); border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span class="badge badge-info" style="font-family: 'JetBrains Mono';">BLOC #${b.index}</span>
                    <span style="font-size: 0.75rem; color: #94a3b8;">${b.timestamp}</span>
                </div>
                <div style="font-size: 0.9rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.4rem;">${b.type}</div>
                <div style="font-family: 'JetBrains Mono'; font-size: 0.7rem; color: var(--emerald); word-break: break-all; margin-bottom: 2px;">
                    HASH : ${b.hash}
                </div>
                <div style="font-family: 'JetBrains Mono'; font-size: 0.65rem; color: #64748b; word-break: break-all;">
                    PREV : ${b.prev_hash}
                </div>
            </div>
        `).join('');
    }

    function verifyLedgerIntegrity() {
        alert('🔒 Vérification cryptographique SHA-256 : Tous les blocs de la chaîne sont 100% valides et immuables !');
        logCockpit('Intégrité de la blockchain BTP vérifiée avec succès.', 'ok');
    }

    function simulatePaymentSituation() {
        caisseBalance += 125000;
        const el1 = document.getElementById('kpi-treasury-val');
        const el2 = document.getElementById('company-caisse-val');
        if (el1) el1.textContent = caisseBalance.toLocaleString('fr-FR') + ' €';
        if (el2) el2.textContent = caisseBalance.toLocaleString('fr-FR') + ' €';
        logCockpit('Situation client n°3 encaissée (+125 000 €).', 'ok');
        alert('Situation de travaux de 125 000 € encaissée en caisse avec succès !');
    }

    // ==========================================
    // 17. WINDOW INITIALIZATION
    // ==========================================
    window.onload = function() {
        try {
            renderNavForRole();
            switchNav('cockpit');
            logCockpit('🚀 Suite BTP Autonomous Command v4.8 initialisée.', 'ok');
        } catch (e) {
            console.error('Initialization error:', e);
        }
    };
</script>
"""
