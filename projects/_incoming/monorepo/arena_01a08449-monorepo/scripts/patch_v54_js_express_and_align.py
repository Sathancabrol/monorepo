#!/usr/bin/env python3
"""
Patch v54: Add calculateDevisExpress, exportDevisExpressPDF, and safety crisis alignment
"""

import re

with open("scripts/section_js_part3.py", "r", encoding="utf-8") as f:
    js_text = f.read()

# Update openSafetyEmergencySimulator and renderCrisisScenario
old_sim_func = """function openSafetyEmergencySimulator() {
        openModal('safety-emergency-modal');
    }"""

new_sim_func = """function openSafetyEmergencySimulator() {
        openModal('safety-crisis-modal');
        renderCrisisScenario('gaz');
    }"""

if old_sim_func in js_text:
    js_text = js_text.replace(old_sim_func, new_sim_func)

# Align safety-crisis-body to support safety-crisis-modal-body
js_text = js_text.replace(
    "const body = document.getElementById('safety-crisis-body');",
    "const body = document.getElementById('safety-crisis-body') || document.getElementById('safety-crisis-modal-body');"
)

# Append Devis Express functions
v54_express_js = r"""

    /* ========================================================================== */
    /* V54: EXPRESS VRD & EARTHWORK COST ESTIMATOR ENGINE                         */
    /* ========================================================================== */
    function calculateDevisExpress() {
        const lenVoirie = parseFloat(document.getElementById('exp-voirie-len')?.value || 350);
        const widthVoirie = parseFloat(document.getElementById('exp-voirie-width')?.value || 6.5);
        const epGnt = parseFloat(document.getElementById('exp-gnt-ep')?.value || 25);
        const epEnr = parseFloat(document.getElementById('exp-enr-ep')?.value || 6);
        const lenEp = parseFloat(document.getElementById('exp-ep-len')?.value || 350);
        const nbRegards = parseFloat(document.getElementById('exp-regards-nb')?.value || 9);
        const lenBordures = parseFloat(document.getElementById('exp-bordures-len')?.value || 700);
        const nbCand = parseFloat(document.getElementById('exp-cand-nb')?.value || 14);

        const surfaceVoirie = lenVoirie * widthVoirie; // m2
        const volTerr = surfaceVoirie * ((epGnt + epEnr + 10) / 100); // m3
        const tonnesGnt = surfaceVoirie * (epGnt / 100) * 2.20; // tonnes
        const tonnesEnr = surfaceVoirie * (epEnr / 100) * 2.40; // tonnes

        const dsTerr = volTerr * 12.80;
        const dsGnt = tonnesGnt * 24.50;
        const dsEnr = tonnesEnr * 94.00;
        const dsEp = lenEp * 92.00;
        const dsRegards = nbRegards * 780.00;
        const dsBordures = lenBordures * 34.50;
        const dsCand = nbCand * 1280.00;

        const totalDS = dsTerr + dsGnt + dsEnr + dsEp + dsRegards + dsBordures + dsCand;
        const totalFG = totalDS * 0.14; // Frais généraux 14%
        const totalMarge = (totalDS + totalFG) * 0.09; // Marge 9%
        const totalPV = totalDS + totalFG + totalMarge;

        const dsEl = document.getElementById('exp-res-ds');
        const fgEl = document.getElementById('exp-res-fg');
        const margeEl = document.getElementById('exp-res-marge');
        const pvEl = document.getElementById('exp-res-pv');

        if (dsEl) dsEl.textContent = Math.round(totalDS).toLocaleString() + ' € HT';
        if (fgEl) fgEl.textContent = Math.round(totalFG).toLocaleString() + ' € HT';
        if (margeEl) margeEl.textContent = Math.round(totalMarge).toLocaleString() + ' € HT';
        if (pvEl) pvEl.textContent = Math.round(totalPV).toLocaleString() + ' € HT';

        window.lastExpressDevis = {
            surfaceVoirie, volTerr, tonnesGnt, tonnesEnr,
            dsTerr, dsGnt, dsEnr, dsEp, dsRegards, dsBordures, dsCand,
            totalDS, totalFG, totalMarge, totalPV,
            lenVoirie, widthVoirie, epGnt, epEnr, lenEp, nbRegards, lenBordures, nbCand
        };
    }

    function exportDevisExpressPDF() {
        if (!window.lastExpressDevis) calculateDevisExpress();
        const d = window.lastExpressDevis;

        const printWindow = window.open('', '_blank');
        printWindow.document.write(`
            <!DOCTYPE html>
            <html>
            <head>
                <title>Devis Express VRD & Terrassement</title>
                <style>
                    body { font-family: 'Segoe UI', Arial, sans-serif; color: #1e293b; padding: 2rem; }
                    .header { display: flex; justify-content: space-between; border-bottom: 3px solid #0284c7; padding-bottom: 1rem; margin-bottom: 1.5rem; }
                    .title { font-size: 1.4rem; font-weight: 800; color: #0f172a; }
                    table { width: 100%; border-collapse: collapse; margin-top: 1rem; font-size: 0.9rem; }
                    th, td { border: 1px solid #cbd5e1; padding: 8px 12px; }
                    th { background: #f1f5f9; text-align: left; }
                    .num { text-align: right; }
                    .totals { margin-top: 1.5rem; width: 350px; margin-left: auto; font-size: 0.95rem; }
                    .totals table th { background: #e2e8f0; }
                    .badge { display: inline-block; padding: 3px 8px; border-radius: 4px; font-weight: 700; font-size: 0.8rem; background: #e0f2fe; color: #0369a1; }
                </style>
            </head>
            <body>
                <div class="header">
                    <div>
                        <div class="title">DEVIS ESTIMATIF EXPRESS VRD & VOIRIE</div>
                        <div style="font-size: 0.85rem; color: #64748b;">Réf : DEV-EXP-${new Date().getFullYear()}-${Math.floor(1000 + Math.random()*9000)} | Date : ${new Date().toLocaleDateString('fr-FR')}</div>
                    </div>
                    <div style="text-align: right;">
                        <strong>ENTREPRISE TP OCCITANIE</strong><br>
                        <span style="font-size: 0.85rem; color: #64748b;">34200 Sète • Bassin de Thau</span>
                    </div>
                </div>

                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 1rem; margin-bottom: 1rem;">
                    <strong>Hypothèses du Projet :</strong> Linéaire voirie : ${d.lenVoirie} m (Larg. ${d.widthVoirie} m = ${d.surfaceVoirie} m²) • GNT : ${d.epGnt} cm • Enrobé BBSG : ${d.epEnr} cm • Réseau EP : ${d.lenEp} ml (${d.nbRegards} regards) • Bordures T2 : ${d.lenBordures} ml • Éclairage : ${d.nbCand} mâts LED.
                </div>

                <table>
                    <thead>
                        <tr>
                            <th>N°</th>
                            <th>Désignation des Travaux VRD</th>
                            <th class="num">Quantité</th>
                            <th>Unité</th>
                            <th class="num">D.S. Unitaire</th>
                            <th class="num">Déboursé Sec Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>1</td><td>Terrassement et décaissement fond de forme</td><td class="num">${Math.round(d.volTerr)}</td><td>m³</td><td class="num">12,80 €</td><td class="num">${Math.round(d.dsTerr).toLocaleString()} €</td></tr>
                        <tr><td>2</td><td>Fourniture et réglage couche d assise GNT 0/31.5</td><td class="num">${Math.round(d.tonnesGnt)}</td><td>t</td><td class="num">24,50 €</td><td class="num">${Math.round(d.dsGnt).toLocaleString()} €</td></tr>
                        <tr><td>3</td><td>Couche de roulement enrobé à chaud BBSG 0/10</td><td class="num">${Math.round(d.tonnesEnr)}</td><td>t</td><td class="num">94,00 €</td><td class="num">${Math.round(d.dsEnr).toLocaleString()} €</td></tr>
                        <tr><td>4</td><td>Tranchée et pose canalisation EP PVC CR8 DN 300</td><td class="num">${d.lenEp}</td><td>ml</td><td class="num">92,00 €</td><td class="num">${Math.round(d.dsEp).toLocaleString()} €</td></tr>
                        <tr><td>5</td><td>Regards de visite béton Ø1000 avec tampon fonte C250</td><td class="num">${d.nbRegards}</td><td>U</td><td class="num">780,00 €</td><td class="num">${Math.round(d.dsRegards).toLocaleString()} €</td></tr>
                        <tr><td>6</td><td>Pose de bordures T2 sur lit de béton C25/30</td><td class="num">${d.lenBordures}</td><td>ml</td><td class="num">34,50 €</td><td class="num">${Math.round(d.dsBordures).toLocaleString()} €</td></tr>
                        <tr><td>7</td><td>Candélabres d éclairage public LED 50W hauteur 6m</td><td class="num">${d.nbCand}</td><td>U</td><td class="num">1 280,00 €</td><td class="num">${Math.round(d.dsCand).toLocaleString()} €</td></tr>
                    </tbody>
                </table>

                <div class="totals">
                    <table>
                        <tr><th>Déboursé Sec Global (DS) :</th><td class="num"><strong>${Math.round(d.totalDS).toLocaleString()} € HT</strong></td></tr>
                        <tr><th>Frais Généraux (14.0%) :</th><td class="num">${Math.round(d.totalFG).toLocaleString()} € HT</td></tr>
                        <tr><th>Marge Nette & Aléas (9.0%) :</th><td class="num">${Math.round(d.totalMarge).toLocaleString()} € HT</td></tr>
                        <tr style="font-size: 1.1rem; background: #e0f2fe;"><th>PRIX DE VENTE TOTAL :</th><td class="num"><strong style="color: #0284c7;">${Math.round(d.totalPV).toLocaleString()} € HT</strong></td></tr>
                    </table>
                </div>

                <div style="margin-top: 2rem; display: flex; justify-content: space-between; font-size: 0.85rem; color: #64748b; border-top: 1px solid #cbd5e1; padding-top: 1rem;">
                    <div>Validité de l offre : 90 jours</div>
                    <div>Signature & Cachet Entreprise :</div>
                </div>
            </body>
            </html>
        `);
        printWindow.document.close();
        printWindow.focus();
        setTimeout(() => { printWindow.print(); }, 500);
    }
"""

# Inject before closing quote of section_js_part3.py
tq_pos = js_text.rfind('"""')
if tq_pos != -1:
    js_text = js_text[:tq_pos] + v54_express_js + js_text[tq_pos:]
else:
    js_text += v54_express_js

with open("scripts/section_js_part3.py", "w", encoding="utf-8") as f:
    f.write(js_text)

print("scripts/section_js_part3.py successfully updated with v54 express costing engine!")
