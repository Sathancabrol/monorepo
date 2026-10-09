import re
from pathlib import Path

TARGET = Path("/home/user/monorepo/projects/btp-conduite-travaux/template.html")

with open(TARGET, "r", encoding="utf-8") as f:
    text = f.read()

# Replace JavaScript functions for Planning, Catalog detail sheet, OPBTP canvas, SDP, Obsidian Heuristics, Schemas, Procurement CRUD, and Ledger

# Find section between "// TAB 3: PROJECTS HUB & ARCHIVES" and "// TAB 5: WATCH TOWER"
idx_hub_start = text.find("// TAB 3: PROJECTS HUB & ARCHIVES")
idx_sim_start = text.find("// ==========================================\n    // WATCH TOWER : 2D VUE SATELLITE & 3D GRILLE XYZ")

if idx_hub_start == -1 or idx_sim_start == -1:
    print("Error locating hub/sim markers in template.html")
    exit(1)

new_hub_and_plan_js = """// TAB 3: PROJECTS HUB & ARCHIVES
    let planningViewMode = 'task'; // 'task', 'time', 'team', 'machine'

    function renderProjectsHub(filter) {
        const container = document.getElementById('projects-hub-content');
        const btnActive = document.getElementById('btn-hub-active');
        const btnArchived = document.getElementById('btn-hub-archived');
        if (!container) return;

        if (btnActive) btnActive.classList.toggle('active', filter === 'active');
        if (btnArchived) btnArchived.classList.toggle('active', filter === 'archived');

        if (filter === 'active') {
            const projects = companyData.projects || [];
            container.innerHTML = projects.map(p => `
                <div class="project-card project-card-clickable" onclick="openProjectDetailsModal('${p.id}')">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.4rem;">
                        <div>
                            <div style="font-weight:800; font-size:0.95rem; color:var(--text-main);">${p.name}</div>
                            <div style="font-size:0.75rem; color:var(--cyan); font-family:var(--font-mono);">${p.client} — ${p.location}</div>
                        </div>
                        <span class="card-badge" style="color:var(--emerald);">${p.statut}</span>
                    </div>
                    <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.6rem;">
                        <b>Phase Actuelle :</b> <span style="color:var(--cyan);">${p.phase_actuelle}</span><br>
                        <b>Conducteur :</b> ${p.conducteur} | <b>Chef :</b> ${p.chef_chantier}
                    </div>
                    <div style="background:var(--bg); padding:0.6rem; border-radius:6px; font-size:0.72rem; display:grid; grid-template-columns:1fr 1fr; gap:0.4rem; margin-bottom:0.6rem;">
                        <div>Budget : <b>${p.budget_total.toLocaleString('fr-FR')} €</b></div>
                        <div>Dépensé : <b>${p.depense_reelle.toLocaleString('fr-FR')} €</b></div>
                        <div>Avancement : <b style="color:var(--emerald);">${p.avancement_physique_pct}%</b></div>
                        <div>Marge Estimée : <b style="color:var(--cyan);">+${p.marge_estimee_pct}%</b></div>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; gap:0.4rem;">
                        <span style="font-size:0.7rem; color:var(--amber);">⚠️ ${p.risques_aipr || 'DICT validée'}</span>
                        <button class="btn-primary" style="font-size:0.7rem; padding:0.3rem 0.6rem;" onclick="event.stopPropagation(); openProjectDetailsModal('${p.id}')">
                            🔍 Voir Fiche Complète
                        </button>
                    </div>
                </div>
            `).join('');
        } else {
            const archives = companyData.archived_projects || [];
            container.innerHTML = archives.map(a => `
                <div class="project-card project-card-clickable" onclick="openProjectDetailsModal('${a.id}')">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.4rem;">
                        <div>
                            <div style="font-weight:800; font-size:0.95rem; color:var(--text-main);">${a.name}</div>
                            <div style="font-size:0.75rem; color:var(--cyan); font-family:var(--font-mono);">${a.client}</div>
                        </div>
                        <span class="card-badge" style="color:var(--cyan);">Archivé & Clôturé</span>
                    </div>
                    <div style="background:var(--bg); padding:0.6rem; border-radius:6px; font-size:0.72rem; display:grid; grid-template-columns:1fr 1fr; gap:0.4rem; margin:0.6rem 0;">
                        <div>Montant Final DGD : <b>${a.montant_final.toLocaleString('fr-FR')} €</b></div>
                        <div>Marge Réelle : <b style="color:var(--emerald);">+${a.marge_reelle}%</b></div>
                        <div>Date Réception : <b>${a.date_reception}</b></div>
                        <div>Statut GPA : <b style="color:var(--cyan);">${a.gpa_status}</b></div>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:0.7rem; color:var(--emerald);">✅ ${a.doe_status}</span>
                        <button class="btn-secondary" style="font-size:0.7rem; padding:0.3rem 0.6rem;" onclick="event.stopPropagation(); openProjectDetailsModal('${a.id}')">
                            📄 Dossier DOE & Bilan
                        </button>
                    </div>
                </div>
            `).join('');
        }
    }

    function openProjectDetailsModal(projectId) {
        let p = (companyData.projects || []).find(proj => proj.id === projectId);
        let isArchived = false;
        if (!p) {
            p = (companyData.archived_projects || []).find(proj => proj.id === projectId);
            isArchived = true;
        }
        if (!p) return;

        const content = document.getElementById('project-details-content');
        if (!content) return;

        content.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1rem; border-bottom:1px solid var(--border); padding-bottom:0.8rem;">
                <div>
                    <h3 style="font-size:1.3rem; font-weight:800; color:var(--cyan); margin-bottom:0.2rem;">📁 ${p.name}</h3>
                    <div style="font-size:0.8rem; color:var(--text-muted); font-family:var(--font-mono);">${p.client} — ${p.location || 'Hérault / Gard'}</div>
                </div>
                <div style="display:flex; align-items:center; gap:0.5rem;">
                    <span class="card-badge" style="color:${isArchived ? 'var(--cyan)' : 'var(--emerald)'};">${p.statut || 'Clôturé & Livré'}</span>
                    <button class="btn-secondary" style="padding:0.25rem 0.6rem;" onclick="closeModal('modal-project-details')">✕</button>
                </div>
            </div>

            <!-- 6 KPI Blocks -->
            <div class="grid-3" style="gap:0.6rem; margin-bottom:1rem;">
                <div style="background:var(--bg); padding:0.7rem; border-radius:8px; border:1px solid var(--border);">
                    <div style="font-size:0.7rem; color:var(--text-muted);">Budget Total / Marché :</div>
                    <div style="font-size:1.15rem; font-weight:800; color:var(--text-main);">${(p.budget_total || p.montant_final || 750000).toLocaleString('fr-FR')} €</div>
                </div>
                <div style="background:var(--bg); padding:0.7rem; border-radius:8px; border:1px solid var(--border);">
                    <div style="font-size:0.7rem; color:var(--text-muted);">Dépenses Engagées :</div>
                    <div style="font-size:1.15rem; font-weight:800; color:var(--cyan);">${(p.depense_reelle || p.montant_final * 0.85).toLocaleString('fr-FR')} €</div>
                </div>
                <div style="background:var(--bg); padding:0.7rem; border-radius:8px; border:1px solid var(--border);">
                    <div style="font-size:0.7rem; color:var(--text-muted);">Marge Prévue / Réelle :</div>
                    <div style="font-size:1.15rem; font-weight:800; color:var(--emerald);">+${p.marge_estimee_pct || p.marge_reelle || 14.2}%</div>
                </div>
                <div style="background:var(--bg); padding:0.7rem; border-radius:8px; border:1px solid var(--border);">
                    <div style="font-size:0.7rem; color:var(--text-muted);">Avancement Physique :</div>
                    <div style="font-size:1.15rem; font-weight:800; color:var(--amber);">${p.avancement_physique_pct || 100}%</div>
                </div>
                <div style="background:var(--bg); padding:0.7rem; border-radius:8px; border:1px solid var(--border);">
                    <div style="font-size:0.7rem; color:var(--text-muted);">Indicateur Coût (CPI) :</div>
                    <div style="font-size:1.15rem; font-weight:800; color:var(--emerald);">${p.kpis ? p.kpis.cpi : '1.08'} (Favorable)</div>
                </div>
                <div style="background:var(--bg); padding:0.7rem; border-radius:8px; border:1px solid var(--border);">
                    <div style="font-size:0.7rem; color:var(--text-muted);">Indicateur Délais (SPI) :</div>
                    <div style="font-size:1.15rem; font-weight:800; color:var(--cyan);">${p.kpis ? p.kpis.spi : '1.02'} (Dans les temps)</div>
                </div>
            </div>

            <!-- Detailed Team, Equipment and AIPR Risks -->
            <div class="grid-2" style="gap:0.8rem; margin-bottom:1rem;">
                <div style="background:var(--bg); padding:0.8rem; border-radius:8px; border:1px solid var(--border); font-size:0.75rem; line-height:1.8;">
                    <div style="font-weight:800; color:var(--cyan); margin-bottom:0.4rem;">👷‍♂️ Encadrement & Ressources Humaines :</div>
                    <div>Conducteur de Travaux : <b>${p.conducteur || 'Sylvain CABROL'}</b></div>
                    <div>Chef de Chantier Référent : <b>${p.chef_chantier || 'Alain MARTIN'}</b></div>
                    <div>Effectif Compagnons sur Site : <b>${p.ouvriers_sur_place || 8} ouvriers</b></div>
                    <div>Engins Lourds Affectés : <b>${p.machines_sur_place || 4} machines</b></div>
                    <div>Dates du Chantier : <b>${p.date_debut || '2026-05-15'} → ${p.date_fin_prevue || p.date_reception || '2026-10-30'}</b></div>
                </div>

                <div style="background:var(--bg); padding:0.8rem; border-radius:8px; border:1px solid var(--border); font-size:0.75rem; line-height:1.8;">
                    <div style="font-weight:800; color:var(--amber); margin-bottom:0.4rem;">⚠️ Risques Réseaux & Sécurité Chantier (AIPR) :</div>
                    <div>Sensibilité Réseaux : <b>${p.risques_aipr || 'DICT Classe A Concessionnaires'}</b></div>
                    <div>Phase Actuelle : <b>${p.phase_actuelle || 'Ouvrage Réceptionné sans réserve'}</b></div>
                    <div>Prochaine Étape Critique : <b>Essai d\\'étanchéité & Clôture DGD</b></div>
                    <div>Garantie de Parfait Achèvement : <b>${p.gpa_status || 'En cours (0 réclamation)'}</b></div>
                </div>
            </div>

            <!-- Complete Project Documents & Downloads Table -->
            <div style="background:var(--bg); padding:0.8rem; border-radius:8px; border:1px solid var(--border); margin-bottom:1rem;">
                <div style="font-weight:800; color:var(--text-main); font-size:0.85rem; margin-bottom:0.6rem;">📚 Dossier Contractuel & Technique Téléchargeable :</div>
                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:0.5rem;">
                    <button class="btn-secondary" style="font-size:0.72rem; justify-content:flex-start; padding:0.4rem;" onclick="alert('Téléchargement du CCTP Lot Voirie / Réseaux (.pdf)')">
                        📄 CCTP & Prescriptions Techniques
                    </button>
                    <button class="btn-secondary" style="font-size:0.72rem; justify-content:flex-start; padding:0.4rem;" onclick="alert('Téléchargement du Bordereau des Prix Unitaires BPU (.xls)')">
                        📊 BPU & Détail Quantitatif Estimatif
                    </button>
                    <button class="btn-secondary" style="font-size:0.72rem; justify-content:flex-start; padding:0.4rem;" onclick="alert('Téléchargement des Plans de Récolement IFC 4.3 & DWG (.dwg)')">
                        📐 Plans d\\'Exécution IFC 4.3 / DWG
                    </button>
                    <button class="btn-secondary" style="font-size:0.72rem; justify-content:flex-start; padding:0.4rem;" onclick="alert('Téléchargement des Récépissés DICT & Arrêtés de Voirie (.pdf)')">
                        ⚡ Récépissés DICT & Arrêtés Circulation
                    </button>
                    <button class="btn-secondary" style="font-size:0.72rem; justify-content:flex-start; padding:0.4rem;" onclick="alert('Téléchargement de l\\'Ordre de Service OS N°1 (.pdf)')">
                        📑 Ordre de Service (OS N°1)
                    </button>
                    <button class="btn-secondary" style="font-size:0.72rem; justify-content:flex-start; padding:0.4rem;" onclick="alert('Téléchargement du Dossier des Ouvrages Exécutés DOE SI 022 (.pdf)')">
                        📦 DOE SI 022 & PV de Réception
                    </button>
                </div>
            </div>

            <!-- Quick Navigation Action Bar -->
            <div style="display:flex; justify-content:flex-end; gap:0.6rem; flex-wrap:wrap;">
                <button class="btn-secondary" style="font-size:0.75rem;" onclick="closeModal('modal-project-details'); switchNav('planning');">
                    📅 Ouvrir dans le Planning Gantt
                </button>
                <button class="btn-secondary" style="font-size:0.75rem;" onclick="closeModal('modal-project-details'); switchNav('sdp');">
                    💰 Voir Sous-Détail de Prix (SDP)
                </button>
                <button class="btn-primary" style="font-size:0.75rem;" onclick="closeModal('modal-project-details'); switchNav('simulator');">
                    🛰️ Visualiser dans Watch Tower 3D
                </button>
            </div>
        `;

        openModal('modal-project-details');
    }

    // TAB 4: PLANNING GANTT MULTI-VIEWS
    function setPlanningViewMode(mode, btn) {
        planningViewMode = mode;
        document.querySelectorAll('#planning-view-bar button').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
        const badge = document.getElementById('planning-view-badge');
        if (badge) {
            const labels = {
                'task': 'Vue par Tâche (Gantt standard)',
                'time': 'Vue Temporelle (Mois / Trimestres)',
                'team': 'Vue par Équipe / Conducteur',
                'machine': 'Vue par Engin Affecté'
            };
            badge.innerText = labels[mode] || 'Vue Active';
        }
        renderPlanningTable();
    }

    function renderPlanningTable() {
        const table = document.getElementById('planning-gantt-table');
        if (!table) return;

        const tasks = companyData.planning_tasks || [];

        if (planningViewMode === 'task') {
            table.innerHTML = `
                <thead>
                    <tr style="color:var(--cyan); border-bottom:1px solid var(--border); text-align:left;">
                        <th style="padding:6px 8px;">Chantier</th>
                        <th style="padding:6px 8px;">Tâche d'Exécution VRD</th>
                        <th style="padding:6px 8px;">Période</th>
                        <th style="padding:6px 8px; width:220px;">Avancement Gantt</th>
                        <th style="padding:6px 8px;">Statut</th>
                        <th style="padding:6px 8px;">Responsable</th>
                    </tr>
                </thead>
                <tbody>
                    ${tasks.map(t => `
                        <tr style="border-bottom:1px solid rgba(51,65,85,0.3); color:var(--text-main);">
                            <td style="padding:6px 8px; font-weight:700; color:var(--cyan);">${t.project}</td>
                            <td style="padding:6px 8px;">${t.task}</td>
                            <td style="padding:6px 8px; font-family:var(--font-mono); font-size:0.7rem; color:var(--text-muted);">${t.start} → ${t.end}</td>
                            <td style="padding:6px 8px;">
                                <div style="display:flex; align-items:center; gap:0.5rem;">
                                    <div style="flex:1; height:8px; background:var(--bg); border-radius:4px; overflow:hidden; border:1px solid var(--border);">
                                        <div style="width:${t.progress}%; height:100%; background:${t.progress === 100 ? 'var(--emerald)' : (t.progress > 0 ? 'var(--cyan)' : 'var(--border)')};"></div>
                                    </div>
                                    <span style="font-family:var(--font-mono); font-size:0.7rem; width:32px;">${t.progress}%</span>
                                </div>
                            </td>
                            <td style="padding:6px 8px;">
                                <span class="card-badge" style="color:${t.status === 'Terminé' ? 'var(--emerald)' : (t.status === 'En cours' ? 'var(--amber)' : 'var(--text-muted)')};">
                                    ${t.status}
                                </span>
                            </td>
                            <td style="padding:6px 8px; font-weight:700;">${t.lead}</td>
                        </tr>
                    `).join('')}
                </tbody>
            `;
        } else if (planningViewMode === 'team') {
            const teams = [
                { lead: "A. Martin (Chef Ch. Alès)", role: "Terrassement & Enrobés", tasks: tasks.filter(t => t.lead.includes("Martin")) },
                { lead: "M. Gomez (Chef Ch. Sète)", role: "VRD & Réseaux Profonds", tasks: tasks.filter(t => t.lead.includes("Gomez")) },
                { lead: "K. Benali (Chef d'Équipe)", role: "Pose Fonte & Assainissement", tasks: tasks.filter(t => t.lead.includes("Benali")) },
                { lead: "S. Lacombe / S. Cabrol", role: "Contrôles OPR & Clôture DGD", tasks: tasks.filter(t => t.lead.includes("Cabrol") || t.lead.includes("Lacombe")) }
            ];

            table.innerHTML = `
                <thead>
                    <tr style="color:var(--cyan); border-bottom:1px solid var(--border); text-align:left;">
                        <th style="padding:6px 8px;">Équipe / Responsable</th>
                        <th style="padding:6px 8px;">Spécialité</th>
                        <th style="padding:6px 8px;">Tâches Affectées</th>
                        <th style="padding:6px 8px;">Charge Globale</th>
                    </tr>
                </thead>
                <tbody>
                    ${teams.map(tm => {
                        const totalProg = tm.tasks.length ? Math.round(tm.tasks.reduce((acc, x) => acc + x.progress, 0) / tm.tasks.length) : 0;
                        return `
                            <tr style="border-bottom:1px solid rgba(51,65,85,0.3); color:var(--text-main);">
                                <td style="padding:8px; font-weight:800; color:var(--cyan);">${tm.lead}</td>
                                <td style="padding:8px; color:var(--text-muted);">${tm.role}</td>
                                <td style="padding:8px;">
                                    ${tm.tasks.map(t => `<div style="margin-bottom:3px;">• <b>${t.project}</b> : ${t.task} (${t.progress}%)</div>`).join('')}
                                </td>
                                <td style="padding:8px;">
                                    <div style="font-weight:700; color:${totalProg === 100 ? 'var(--emerald)' : 'var(--amber)'};">${totalProg}% complété</div>
                                </td>
                            </tr>
                        `;
                    }).join('')}
                </tbody>
            `;
        } else if (planningViewMode === 'machine') {
            const machineTasks = [
                { machine: "🚜 Pelle Chenilles Liebherr 24t", project: "Giratoire RD906 Alès", current: "Pose Bordures & Caniveaux CC1", next: "Terrassement giratoire nord", horametre: "2 418 h" },
                { machine: "🔨 Compacteur Bomag BW213", project: "Giratoire RD906 Alès", current: "Compactage GNT 0/31.5 (EV2>80)", next: "Piste cyclable Montpellier", horametre: "1 430 h" },
                { machine: "🛣️ Finisseur Dynapac SD2500", project: "Giratoire RD906 Alès", current: "En attente enrobé BBSG 0/10", next: "Enrobés RD906 Alès", horametre: "980 h" },
                { machine: "🛸 Drone DJI Matrice 350 RTK", project: "ZAC Littoral Sète", current: "Relevé LiDAR Tranchée ZAC", next: "Orthophoto Pézenas", horametre: "142 h" },
                { machine: "🦾 Exosquelette HAPO BTP (x2)", project: "Centre Ancien Pézenas", current: "Manutention bordures & fonte", next: "Pose bordures Alès", horametre: "520 h" },
                { machine: "🤖 Robot Husqvarna DXR 300", project: "ZAC Littoral Sète", current: "Sciage d'enrobé tranchée gaz", next: "Démolition chambre télécom", horametre: "890 h" }
            ];

            table.innerHTML = `
                <thead>
                    <tr style="color:var(--cyan); border-bottom:1px solid var(--border); text-align:left;">
                        <th style="padding:6px 8px;">Engin / Matériel</th>
                        <th style="padding:6px 8px;">Chantier Affecté</th>
                        <th style="padding:6px 8px;">Mission Actuelle</th>
                        <th style="padding:6px 8px;">Prochaine Étape Planning</th>
                        <th style="padding:6px 8px;">Horamètre</th>
                    </tr>
                </thead>
                <tbody>
                    ${machineTasks.map(m => `
                        <tr style="border-bottom:1px solid rgba(51,65,85,0.3); color:var(--text-main);">
                            <td style="padding:8px; font-weight:800; color:var(--text-main);">${m.machine}</td>
                            <td style="padding:8px; color:var(--cyan);">${m.project}</td>
                            <td style="padding:8px; color:var(--emerald);">${m.current}</td>
                            <td style="padding:8px; color:var(--text-muted);">${m.next}</td>
                            <td style="padding:8px; font-family:var(--font-mono); font-weight:700;">${m.horametre}</td>
                        </tr>
                    `).join('')}
                </tbody>
            `;
        } else {
            // Temporal view (Months & Quarters)
            const quarters = [
                { q: "T2 2026 (Mai - Juin)", desc: "Installation chantiers, DICT, terrassements généraux et PST chaux (Alès & Sète)", prog: 100 },
                { q: "T3 2026 (Juil - Sept)", desc: "Couches de fondation GNT 0/31.5, pose collecteurs DN400 sous nappe, bordures T2", prog: 85 },
                { q: "T4 2026 (Oct - Déc)", desc: "Enrobés BBSG 0/10 à chaud, épreuves hydrostatiques, réceptions OPR & DOE SI 022", prog: 20 },
                { q: "T1 2027 (Jan - Mars)", desc: "Clôtures DGD, levée des réserves et suivi GPA 1 an (0 sinistre)", prog: 0 }
            ];

            table.innerHTML = `
                <thead>
                    <tr style="color:var(--cyan); border-bottom:1px solid var(--border); text-align:left;">
                        <th style="padding:6px 8px;">Période / Trimestre</th>
                        <th style="padding:6px 8px;">Jalons Clés & Travaux Programmés</th>
                        <th style="padding:6px 8px; width:250px;">Avancement Global</th>
                    </tr>
                </thead>
                <tbody>
                    ${quarters.map(q => `
                        <tr style="border-bottom:1px solid rgba(51,65,85,0.3); color:var(--text-main);">
                            <td style="padding:8px; font-weight:800; color:var(--cyan);">${q.q}</td>
                            <td style="padding:8px; color:var(--text-muted);">${q.desc}</td>
                            <td style="padding:8px;">
                                <div style="display:flex; align-items:center; gap:0.5rem;">
                                    <div style="flex:1; height:8px; background:var(--bg); border-radius:4px; overflow:hidden; border:1px solid var(--border);">
                                        <div style="width:${q.prog}%; height:100%; background:${q.prog === 100 ? 'var(--emerald)' : (q.prog > 0 ? 'var(--cyan)' : 'var(--border)')};"></div>
                                    </div>
                                    <span style="font-family:var(--font-mono); font-size:0.7rem; width:32px;">${q.prog}%</span>
                                </div>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            `;
        }
    }
"""

text = text[:idx_hub_start] + new_hub_and_plan_js + text[idx_sim_start:]

with open(TARGET, "w", encoding="utf-8") as f:
    f.write(text)

print("Applied Projects Hub and Multi-View Planning JS successfully!")
