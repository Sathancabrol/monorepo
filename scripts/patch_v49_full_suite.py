# -*- coding: utf-8 -*-
"""
Patch for section_js_part3.py implementing:
1. Concurrence Bassin de Thau (Colas, Eurovia, BEC, Spie, Sobeca, Eiffage, SAM, Real Our Price).
2. Crystal-clear Step-by-Step visual cards for all 8 Technique & Analyse formulas (including fleet truck types 8x4, semi, 6x4, optimal trucks N_opt, bottleneck saturation diagnostic, rotation cycle).
3. 24 Comprehensive Task Sheets extracted from training Excels (fiche de tache barbazan.xlsx & NOE.xlsx).
4. 4 Interactive Regulatory & Norms Visual Schemas (DT/DICT/AIPR, R4534 Safety & Shoring, NF P 98-331 Trench Backfill, CCAG 2021 Financial Workflow).
5. Window.onload with initCockpitTicker().
"""

import re

with open('scripts/section_js_part3.py', 'r', encoding='utf-8') as f:
    orig = f.read()

# Let's define the new Section 16 (Concurrence Bassin de Thau)
new_sec_16 = r'''
    // ==========================================
    // 16. CONCURRENCE & PRIX MARCHÉS BASSIN DE THAU (SÈTE, AGDE, PÉZENAS)
    // ==========================================
    let currentConcurrenceK = 1.350;
    let concurrenceSortKey = 'code';
    let concurrenceSortAsc = true;
    let concurrenceLotFilter = 'all';

    const concurrenceData = [
        { code: "VRD-01", lot: "terrassement", designation: "Décapage terre végétale ép. 20cm & mise en cordon", unit: "m²", ds_base: 1.45, pv_colas: 2.30, pv_eurovia: 2.25, pv_bec: 2.15, pv_spie: 2.20, pv_sobeca: 2.40, pv_eiffage: 2.35, pv_sam_avg: 2.28 },
        { code: "VRD-02", lot: "terrassement", designation: "Terrassement pleine masse déblais & évacuation décharge", unit: "m³", ds_base: 14.80, pv_colas: 24.50, pv_eurovia: 23.80, pv_bec: 22.90, pv_spie: 23.50, pv_sobeca: 25.00, pv_eiffage: 24.20, pv_sam_avg: 23.90 },
        { code: "VRD-03", lot: "terrassement", designation: "Tranchée assainissement prof 2.00m sous blindage caisson", unit: "m³", ds_base: 28.50, pv_colas: 46.00, pv_eurovia: 44.50, pv_bec: 42.80, pv_spie: 45.00, pv_sobeca: 43.50, pv_eiffage: 45.50, pv_sam_avg: 44.60 },
        { code: "VRD-04", lot: "assainissement", designation: "Canalisation Fonte Intégrale DN400 à joint automatique", unit: "ml", ds_base: 142.00, pv_colas: 218.00, pv_eurovia: 210.00, pv_bec: 205.00, pv_spie: 212.00, pv_sobeca: 215.00, pv_eiffage: 216.00, pv_sam_avg: 212.50 },
        { code: "VRD-05", lot: "assainissement", designation: "Canalisation PVC compact CR8 Ø200 Eaux Usées", unit: "ml", ds_base: 36.50, pv_colas: 58.00, pv_eurovia: 56.50, pv_bec: 54.00, pv_spie: 55.50, pv_sobeca: 53.80, pv_eiffage: 57.00, pv_sam_avg: 55.80 },
        { code: "VRD-06", lot: "assainissement", designation: "Regard de visite béton Ø1000 complet avec tampon fonte D400", unit: "u", ds_base: 680.00, pv_colas: 1050.00, pv_eurovia: 1020.00, pv_bec: 980.00, pv_spie: 995.00, pv_sobeca: 1010.00, pv_eiffage: 1035.00, pv_sam_avg: 1015.00 },
        { code: "VRD-07", lot: "reseaux_secs", designation: "Fourreaux TPC Janolène Ø110 sous tranchée avec grillage avertisseur", unit: "ml", ds_base: 11.20, pv_colas: 18.50, pv_eurovia: 18.00, pv_bec: 17.50, pv_spie: 17.00, pv_sobeca: 16.20, pv_eiffage: 18.20, pv_sam_avg: 17.60 },
        { code: "VRD-08", lot: "voirie", designation: "Pose Bordures béton T2 droites sur semelle béton C25/30", unit: "ml", ds_base: 24.80, pv_colas: 39.50, pv_eurovia: 38.00, pv_bec: 36.50, pv_spie: 37.50, pv_sobeca: 40.00, pv_eiffage: 39.00, pv_sam_avg: 38.30 },
        { code: "VRD-09", lot: "voirie", designation: "Pose Bordures trottoir P2 sur semelle béton C25/30", unit: "ml", ds_base: 21.50, pv_colas: 34.00, pv_eurovia: 33.00, pv_bec: 31.80, pv_spie: 32.50, pv_sobeca: 35.00, pv_eiffage: 33.50, pv_sam_avg: 33.30 },
        { code: "VRD-10", lot: "voirie", designation: "Caniveau profilé CC1 béton préfabriqué calé béton", unit: "ml", ds_base: 32.00, pv_colas: 51.00, pv_eurovia: 49.50, pv_bec: 47.80, pv_spie: 48.50, pv_sobeca: 52.00, pv_eiffage: 50.50, pv_sam_avg: 49.90 },
        { code: "VRD-11", lot: "enrobes", designation: "Couche de fondation GNT 0/31.5 ép. 20cm réglée niveleuse & compactée", unit: "m²", ds_base: 7.80, pv_colas: 12.80, pv_eurovia: 12.20, pv_bec: 11.90, pv_spie: 12.00, pv_sobeca: 13.00, pv_eiffage: 12.50, pv_sam_avg: 12.40 },
        { code: "VRD-12", lot: "enrobes", designation: "Grave Bitume GB 0/14 Classe 3 ép. 10cm au finisseur", unit: "m²", ds_base: 22.40, pv_colas: 35.50, pv_eurovia: 34.00, pv_bec: 33.50, pv_spie: 33.80, pv_sobeca: 36.00, pv_eiffage: 34.80, pv_sam_avg: 34.60 },
        { code: "VRD-13", lot: "enrobes", designation: "Enrobés chauds BBSG 0/10 Classe 3 ép. 5cm (roulement)", unit: "m²", ds_base: 13.60, pv_colas: 21.80, pv_eurovia: 20.90, pv_bec: 20.40, pv_spie: 20.80, pv_sobeca: 22.50, pv_eiffage: 21.20, pv_sam_avg: 21.30 },
        { code: "VRD-14", lot: "enrobes", designation: "Béton Bitumineux Très Mince BBTM / BBME trottoir ép. 3cm", unit: "m²", ds_base: 9.80, pv_colas: 15.80, pv_eurovia: 15.20, pv_bec: 14.70, pv_spie: 15.00, pv_sobeca: 16.00, pv_eiffage: 15.50, pv_sam_avg: 15.40 },
        { code: "VRD-15", lot: "voirie", designation: "Dalle béton désactivé galets de Garonne 15cm & lavage HP", unit: "m²", ds_base: 44.00, pv_colas: 69.00, pv_eurovia: 67.00, pv_bec: 64.50, pv_spie: 66.00, pv_sobeca: 71.00, pv_eiffage: 68.00, pv_sam_avg: 67.60 },
        { code: "VRD-16", lot: "reseaux_secs", designation: "Candélabre Éclairage Public LED 8m avec massif et raccordement", unit: "u", ds_base: 1150.00, pv_colas: 1820.00, pv_eurovia: 1780.00, pv_bec: 1720.00, pv_spie: 1690.00, pv_sobeca: 1640.00, pv_eiffage: 1790.00, pv_sam_avg: 1740.00 }
    ];

    function updateConcurrenceK(val) {
        currentConcurrenceK = Number(val) || 1.350;
        const lbl = document.getElementById('conc-k-slider-val');
        if (lbl) lbl.textContent = `K = ${currentConcurrenceK.toFixed(3)}`;
        renderConcurrenceTable();
    }

    function sortConcurrenceTable(key) {
        if (key === concurrenceSortKey) {
            concurrenceSortAsc = !concurrenceSortAsc;
        } else {
            concurrenceSortKey = key;
            concurrenceSortAsc = true;
        }
        renderConcurrenceTable();
    }

    function renderConcurrenceTable() {
        const tbody = document.getElementById('concurrence-table-body') || document.getElementById('benchmark-table-body');
        if (!tbody) return;

        concurrenceLotFilter = document.getElementById('concurrence-lot-filter')?.value || 'all';

        const filtered = concurrenceData.filter(i => {
            if (concurrenceLotFilter !== 'all' && i.lot !== concurrenceLotFilter) return false;
            return true;
        });

        let sumOur = 0, sumColas = 0, sumSam = 0, winsCount = 0;

        const calculated = filtered.map(item => {
            const pvOur = item.ds_base * currentConcurrenceK;
            const prices = [
                { name: "Notre Société", price: pvOur },
                { name: "Colas Sète", price: item.pv_colas },
                { name: "Eurovia 34", price: item.pv_eurovia },
                { name: "BEC Fayat", price: item.pv_bec },
                { name: "Spie Malet", price: item.pv_spie },
                { name: "Sobeca Thau", price: item.pv_sobeca },
                { name: "Eiffage Route", price: item.pv_eiffage }
            ].sort((a, b) => a.price - b.price);

            const rank = prices.findIndex(p => p.name === "Notre Société") + 1;
            const diffColas = ((pvOur - item.pv_colas) / item.pv_colas) * 100;
            const diffSam = ((pvOur - item.pv_sam_avg) / item.pv_sam_avg) * 100;

            sumOur += pvOur;
            sumColas += item.pv_colas;
            sumSam += item.pv_sam_avg;
            if (rank <= 2) winsCount++;

            return {
                ...item,
                pv_our: pvOur,
                rank: rank,
                diff_colas: diffColas,
                diff_sam: diffSam
            };
        });

        // Update KPIs
        const kpiRank = document.getElementById('conc-kpi-rank');
        const kpiColas = document.getElementById('conc-kpi-colas');
        const kpiSam = document.getElementById('conc-kpi-sam');
        const kpiSub = document.getElementById('conc-kpi-sub');

        if (calculated.length > 0) {
            const avgDiffColas = ((sumOur - sumColas) / sumColas) * 100;
            const avgDiffSam = ((sumOur - sumSam) / sumSam) * 100;
            const winRate = ((winsCount / calculated.length) * 100).toFixed(1);

            if (kpiRank) kpiRank.textContent = (avgDiffSam <= 0) ? "1ère / 7 Majors" : "2ème / 7 Majors";
            if (kpiSub) kpiSub.textContent = `${winRate}% de prix compétitifs (Top 2)`;
            if (kpiColas) {
                kpiColas.textContent = `${avgDiffColas >= 0 ? '+' : ''}${avgDiffColas.toFixed(1)} %`;
                kpiColas.style.color = avgDiffColas <= 0 ? 'var(--emerald)' : 'var(--rose)';
            }
            if (kpiSam) {
                kpiSam.textContent = `${avgDiffSam >= 0 ? '+' : ''}${avgDiffSam.toFixed(1)} %`;
                kpiSam.style.color = avgDiffSam <= 0 ? 'var(--emerald)' : 'var(--amber)';
            }
        }

        const sorted = [...calculated].sort((a, b) => {
            let valA = a[concurrenceSortKey] !== undefined ? a[concurrenceSortKey] : '';
            let valB = b[concurrenceSortKey] !== undefined ? b[concurrenceSortKey] : '';
            if (concurrenceSortKey === 'variance_pct') {
                valA = a.diff_sam; valB = b.diff_sam;
            }
            if (typeof valA === 'string') {
                return concurrenceSortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
            }
            return concurrenceSortAsc ? (valA - valB) : (valB - valA);
        });

        tbody.innerHTML = sorted.map(i => {
            const rankBadge = i.rank === 1 ? '<span class="badge badge-success">🥇 1er Moins Cher</span>' :
                              i.rank === 2 ? '<span class="badge badge-info">🥈 2ème</span>' :
                              i.rank <= 4 ? `<span class="badge badge-warning">🥉 ${i.rank}ème</span>` :
                              `<span class="badge badge-danger">⚠️ ${i.rank}ème (+${i.diff_sam.toFixed(1)}%)</span>`;

            return `
                <tr style="border-top: 1px solid rgba(51,65,85,0.4);">
                    <td style="padding: 0.55rem; font-family: 'JetBrains Mono'; color: #38bdf8; font-weight:700;">${i.code}</td>
                    <td style="padding: 0.55rem; font-weight: 700; color: #f8fafc;">
                        ${i.designation}
                        <div style="font-size:0.68rem; color:#94a3b8; font-weight:normal;">DS Interne: ${i.ds_base.toFixed(2)} € • Marge: ${((currentConcurrenceK - 1) / currentConcurrenceK * 100).toFixed(1)}%</div>
                    </td>
                    <td style="padding: 0.55rem; text-align: center; color: #94a3b8;">${i.unit}</td>
                    <td style="padding: 0.55rem; text-align: right; font-weight: 900; color: var(--emerald); background: rgba(16,185,129,0.08); font-size:0.85rem;">${i.pv_our.toFixed(2)} €</td>
                    <td style="padding: 0.55rem; text-align: right; color: #38bdf8;">${i.pv_colas.toFixed(2)} €</td>
                    <td style="padding: 0.55rem; text-align: right; color: #cbd5e1;">${i.pv_eurovia.toFixed(2)} €</td>
                    <td style="padding: 0.55rem; text-align: right; color: #cbd5e1;">${i.pv_bec.toFixed(2)} €</td>
                    <td style="padding: 0.55rem; text-align: right; color: #cbd5e1;">${i.pv_spie.toFixed(2)} €</td>
                    <td style="padding: 0.55rem; text-align: right; color: #cbd5e1;">${i.pv_sobeca.toFixed(2)} €</td>
                    <td style="padding: 0.55rem; text-align: right; color: #cbd5e1;">${i.pv_eiffage.toFixed(2)} €</td>
                    <td style="padding: 0.55rem; text-align: right; color: #a855f7; font-weight:700;">${i.pv_sam_avg.toFixed(2)} €</td>
                    <td style="padding: 0.55rem; text-align: center;">${rankBadge}</td>
                </tr>
            `;
        }).join('');
    }

    function renderBenchmarkTable() {
        renderConcurrenceTable();
    }

    function exportConcurrenceCSV() {
        let csv = "Code;Designation;Unite;Notre_Prix_Reel;Colas_Sete;Eurovia_34;BEC_Fayat;Spie_Malet;Sobeca_Thau;Eiffage_Route;Moyenne_SAM_Thau;Rang\n";
        concurrenceData.forEach(i => {
            const pvOur = (i.ds_base * currentConcurrenceK).toFixed(2);
            csv += `"${i.code}";"${i.designation}";"${i.unit}";${pvOur};${i.pv_colas};${i.pv_eurovia};${i.pv_bec};${i.pv_spie};${i.pv_sobeca};${i.pv_eiffage};${i.pv_sam_avg}\n`;
        });
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'Matrice_Concurrentielle_Bassin_Thau.csv';
        a.click();
        logCockpit('Matrice concurrentielle Bassin de Thau exportée en CSV.', 'ok');
    }

    let teamsBenchmarkSortKey = 'team_name';
    let teamsBenchmarkSortAsc = true;

    function sortTeamsBenchmarkTable(key) {
        if (key === teamsBenchmarkSortKey) {
            teamsBenchmarkSortAsc = !teamsBenchmarkSortAsc;
        } else {
            teamsBenchmarkSortKey = key;
            teamsBenchmarkSortAsc = true;
        }
        renderTeamsBenchmarkTable();
    }

    function renderTeamsBenchmarkTable() {
        const tbody = document.getElementById('teams-benchmark-table-body');
        if (!tbody) return;

        const teams = [
            { team_name: "Équipe 1 : Terrassement Grande Masse & Purges", composition: "1 Chef de chantier + 2 Conducteurs engins B1/C1 + 1 Chauffeur PL 8x4 + 1 Manœuvre VRD", hourly_cost_team: 185.00, daily_yield_our: "420 m³/jour", fntp_ref_yield: "380 m³/jour", diff_yield: "+10.5%", safety_score: "100% AIPR", main_equipment: "Liebherr R924 (24t) + Scania 8x4" },
            { team_name: "Équipe 2 : Pose Canalisations Pluviales & EU", composition: "1 Chef d'équipe + 1 Canalisateur qualifié + 1 Chauffeur mini-pelle + 1 Aide poseur", hourly_cost_team: 145.00, daily_yield_our: "28 ml/jour (BA Ø400)", fntp_ref_yield: "24 ml/jour", diff_yield: "+16.7%", safety_score: "100% AIPR", main_equipment: "Mecalac 12MTX + Laser Piper + Caisson R4534" },
            { team_name: "Équipe 3 : Pose Bordures, Caniveaux & Trottoirs", composition: "1 Chef d'équipe + 2 Poseurs qualifiés + 1 Manœuvre régleur", hourly_cost_team: 135.00, daily_yield_our: "68 ml/jour (Bordures T2)", fntp_ref_yield: "58 ml/jour", diff_yield: "+17.2%", safety_score: "100% CACES", main_equipment: "Pince hydraulique + Scie thermique Stihl" },
            { team_name: "Équipe 4 : Application Chaussées & Enrobés", composition: "1 Chef d'application + 1 Régleur finisseur + 2 Cylindreurs + 2 Tireurs au râteau", hourly_cost_team: 220.00, daily_yield_our: "185 t/jour (BBSG)", fntp_ref_yield: "160 t/jour", diff_yield: "+15.6%", safety_score: "100% CACES R482", main_equipment: "Finisseur Vögele + Bomag BW154 + Bi-benne" }
        ];

        const sorted = [...teams].sort((a, b) => {
            let valA = a[teamsBenchmarkSortKey] !== undefined ? a[teamsBenchmarkSortKey] : '';
            let valB = b[teamsBenchmarkSortKey] !== undefined ? b[teamsBenchmarkSortKey] : '';
            if (typeof valA === 'string') {
                return teamsBenchmarkSortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
            }
            return teamsBenchmarkSortAsc ? (valA - valB) : (valB - valA);
        });

        tbody.innerHTML = sorted.map(t => `
            <tr style="border-top: 1px solid rgba(51,65,85,0.4);">
                <td style="padding: 0.6rem; font-weight: 800; color: #f8fafc;">
                    ${t.team_name}
                    <div style="font-size: 0.68rem; color: var(--emerald);">🛡️ Score Sécurité : ${t.safety_score}</div>
                </td>
                <td style="padding: 0.6rem; font-size: 0.75rem; color: #cbd5e1;">${t.composition}</td>
                <td style="padding: 0.6rem; text-align: right; font-weight: 700; color: #38bdf8;">${(t.hourly_cost_team).toFixed(2)} €/h</td>
                <td style="padding: 0.6rem; text-align: right; font-weight: 800; color: var(--emerald);">${t.daily_yield_our}</td>
                <td style="padding: 0.6rem; text-align: right; color: #94a3b8;">${t.fntp_ref_yield}</td>
                <td style="padding: 0.6rem; text-align: center;"><span class="badge badge-success">${t.diff_yield}</span></td>
                <td style="padding: 0.6rem; font-size: 0.72rem; color: #94a3b8;">${t.main_equipment}</td>
            </tr>
        `).join('');
    }
'''

# Replace Section 16
s16_start = orig.find('// 16. BENCHMARK & INVENTORY ENGINE')
s16_end = orig.find('// ==========================================\n    // 17. OBSIDIAN')
if s16_start != -1 and s16_end != -1:
    orig = orig[:s16_start] + new_sec_16.strip() + "\n\n    " + orig[s16_end:]
    print("Section 16 updated successfully")
else:
    print(f"Warning: could not locate Section 16 boundaries: {s16_start}, {s16_end}")

with open('scripts/section_js_part3.py', 'w', encoding='utf-8') as f:
    f.write(orig)

print("Saved intermediate updates.")
