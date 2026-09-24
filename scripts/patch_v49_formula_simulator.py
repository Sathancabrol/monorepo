# -*- coding: utf-8 -*-
"""
Patch for updateFormulaCalculator & calculateTechniqueFormula in section_js_part3.py
Provides visual step-by-step cards, truck fleet configurations, and clear math formatting.
"""

new_formula_calc_code = r'''
    function updateFormulaCalculator() {
        const type = document.getElementById('formula-type-select')?.value || 'cubature_terrassement';
        const inputsCont = document.getElementById('formula-inputs-container');
        if (!inputsCont) return;

        if (type === 'cubature_terrassement') {
            inputsCont.innerHTML = `
                <div style="background: rgba(30,41,59,0.5); padding: 0.75rem; border-radius: 6px; border: 1px solid rgba(51,65,85,0.6); margin-top: 0.75rem;">
                    <div style="font-size: 0.8rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.5rem;">🚜 1. Dimensions de la Fouille / Tranchée & Nature du Sol</div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem;">
                        <div class="input-group"><label class="input-label">Longueur Tranchée (L en m)</label><input type="number" id="f-cuba-l" class="input-field" value="120" step="5" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Largeur Tranchée (l en m)</label><input type="number" id="f-cuba-w" class="input-field" value="1.20" step="0.1" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Profondeur Moyenne (h en m)</label><input type="number" id="f-cuba-h" class="input-field" value="1.80" step="0.1" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Coef. Foisonnement (Cf)</label><input type="number" id="f-cuba-cf" class="input-field" value="1.25" step="0.05" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Densité Déblai (t/m³)</label><input type="number" id="f-cuba-rho" class="input-field" value="1.80" step="0.1" oninput="calculateTechniqueFormula()"></div>
                    </div>
                </div>

                <div style="background: rgba(30,41,59,0.5); padding: 0.75rem; border-radius: 6px; border: 1px solid rgba(51,65,85,0.6); margin-top: 0.75rem;">
                    <div style="font-size: 0.8rem; font-weight: 800; color: var(--emerald); margin-bottom: 0.5rem;">🚜 2. Caractéristiques de la Pelle Excavatrice</div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem;">
                        <div class="input-group"><label class="input-label">Volume Godet (Vg en m³)</label><input type="number" id="f-cuba-vg" class="input-field" value="0.90" step="0.05" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Temps Cycle Godet (Tc en s)</label><input type="number" id="f-cuba-tc" class="input-field" value="22" step="1" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Remplissage Godet (kr %)</label><input type="number" id="f-cuba-kr" class="input-field" value="90" step="5" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Efficience Pelle (kf %)</label><input type="number" id="f-cuba-kf" class="input-field" value="85" step="5" oninput="calculateTechniqueFormula()"></div>
                    </div>
                </div>

                <div style="background: rgba(30,41,59,0.5); padding: 0.75rem; border-radius: 6px; border: 1px solid rgba(51,65,85,0.6); margin-top: 0.75rem;">
                    <div style="font-size: 0.8rem; font-weight: 800; color: var(--amber); margin-bottom: 0.5rem;">🚛 3. Flotte de Transport & Rotation Camions</div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem;">
                        <div class="input-group" style="grid-column: span 2;">
                            <label class="input-label">Type de Camion & Capacité Utile</label>
                            <select id="f-cuba-cam-type" class="input-field" onchange="calculateTechniqueFormula()">
                                <option value="14.0|8x4 Bi-benne 26t">Camion 8x4 Bi-benne (14.0 m³ foisonnés / 26t)</option>
                                <option value="20.0|Semi-remorque 32t">Semi-remorque Benne TP (20.0 m³ foisonnés / 32t)</option>
                                <option value="10.0|Camion 6x4 19t">Camion 6x4 Benne (10.0 m³ foisonnés / 19t)</option>
                                <option value="6.0|Camion 4x2 10t">Camion 4x2 Bi-benne urbain (6.0 m³ foisonnés / 10t)</option>
                            </select>
                        </div>
                        <div class="input-group"><label class="input-label">Nombre de Camions Affectés (N)</label><input type="number" id="f-cuba-nb-cam" class="input-field" value="4" min="1" max="20" step="1" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Distance Décharge Aller (D en km)</label><input type="number" id="f-cuba-dist" class="input-field" value="12.0" step="1" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Vitesse Moyenne Trajet (km/h)</label><input type="number" id="f-cuba-spd" class="input-field" value="35" step="5" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Temps Bascule / Décharge (min)</label><input type="number" id="f-cuba-tdump" class="input-field" value="5" step="1" oninput="calculateTechniqueFormula()"></div>
                    </div>
                </div>
            `;
        } else if (type === 'tonnage_enrobes') {
            inputsCont.innerHTML = `
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-top:0.75rem;">
                    <div class="input-group"><label class="input-label">Surface à Revêtir (S en m²)</label><input type="number" id="f-enr-s" class="input-field" value="1200" step="50" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Épaisseur Compactée (e en cm)</label><input type="number" id="f-enr-e" class="input-field" value="5.0" step="0.5" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Masse Volumique Réelle (t/m³)</label><input type="number" id="f-enr-mv" class="input-field" value="2.45" step="0.05" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Perte / Majoration (%)</label><input type="number" id="f-enr-perte" class="input-field" value="3.0" step="0.5" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Dosage Émulsion C65B4 (g/m²)</label><input type="number" id="f-enr-emul" class="input-field" value="500" step="50" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Cadence Finisseur (t/h)</label><input type="number" id="f-enr-cad" class="input-field" value="45" step="5" oninput="calculateTechniqueFormula()"></div>
                </div>
            `;
        } else if (type === 'perimetre_bordures') {
            inputsCont.innerHTML = `
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-top:0.75rem;">
                    <div class="input-group"><label class="input-label">Linéaire Total Bordures (L en ml)</label><input type="number" id="f-bord-l" class="input-field" value="280" step="10" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Largeur Semelle Béton (b en m)</label><input type="number" id="f-bord-w" class="input-field" value="0.30" step="0.05" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Épaisseur Semelle Béton (h en m)</label><input type="number" id="f-bord-h" class="input-field" value="0.15" step="0.05" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Volume Béton Épaulement (m³/ml)</label><input type="number" id="f-bord-ep" class="input-field" value="0.025" step="0.005" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Cadence de Pose (ml/h)</label><input type="number" id="f-bord-cad" class="input-field" value="8.5" step="0.5" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Perte / Casse Bordures (%)</label><input type="number" id="f-bord-casse" class="input-field" value="3.0" step="0.5" oninput="calculateTechniqueFormula()"></div>
                </div>
            `;
        } else if (type === 'manning_hydraulique') {
            inputsCont.innerHTML = `
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-top:0.75rem;">
                    <div class="input-group"><label class="input-label">Diamètre Intérieur (D en mm)</label><input type="number" id="f-man-d" class="input-field" value="400" step="50" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Pente du Collecteur (I en m/m ou %)</label><input type="number" id="f-man-i" class="input-field" value="0.015" step="0.001" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Coef. Strickler (K = 70-90)</label><input type="number" id="f-man-k" class="input-field" value="85" step="5" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Taux de Remplissage (h/D en %)</label><input type="number" id="f-man-fill" class="input-field" value="70" step="5" oninput="calculateTechniqueFormula()"></div>
                </div>
            `;
        } else if (type === 'pente_canalisateur') {
            inputsCont.innerHTML = `
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-top:0.75rem;">
                    <div class="input-group"><label class="input-label">Altitude Radier Amont (Z amont en m)</label><input type="number" id="f-pen-zam" class="input-field" value="45.850" step="0.05" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Altitude Radier Aval (Z aval en m)</label><input type="number" id="f-pen-zav" class="input-field" value="45.220" step="0.05" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Distance Horizontale (L en m)</label><input type="number" id="f-pen-l" class="input-field" value="42.00" step="1" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Longueur Élément Tuyau (l en m)</label><input type="number" id="f-pen-elem" class="input-field" value="3.00" step="0.5" oninput="calculateTechniqueFormula()"></div>
                </div>
            `;
        } else if (type === 'compactage_gtr') {
            inputsCont.innerHTML = `
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-top:0.75rem;">
                    <div class="input-group"><label class="input-label">Épaisseur Couche Compactée (e en cm)</label><input type="number" id="f-cmp-e" class="input-field" value="25" step="5" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Largeur Cylindre Rouleau (L en m)</label><input type="number" id="f-cmp-w" class="input-field" value="1.70" step="0.1" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Vitesse de Translation (V en km/h)</label><input type="number" id="f-cmp-v" class="input-field" value="3.5" step="0.5" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Nombre de Passes Requises (N)</label><input type="number" id="f-cmp-n" class="input-field" value="6" step="1" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Volume Total GNT à Compacter (m³)</label><input type="number" id="f-cmp-vtot" class="input-field" value="450" step="25" oninput="calculateTechniqueFormula()"></div>
                </div>
            `;
        } else if (type === 'revision_tp08') {
            inputsCont.innerHTML = `
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-top:0.75rem;">
                    <div class="input-group"><label class="input-label">Montant Situation HT (P0 en €)</label><input type="number" id="f-rev-p0" class="input-field" value="85000" step="1000" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Part Fixe Non Révisable (a)</label><input type="number" id="f-rev-a" class="input-field" value="0.15" step="0.05" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Indice TP08 Initial (TP08_0)</label><input type="number" id="f-rev-i0" class="input-field" value="122.4" step="0.5" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Indice TP08 du Mois n (TP08_n)</label><input type="number" id="f-rev-in" class="input-field" value="129.8" step="0.5" oninput="calculateTechniqueFormula()"></div>
                </div>
            `;
        } else if (type === 'debourse_sec_k') {
            inputsCont.innerHTML = `
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-top:0.75rem;">
                    <div class="input-group"><label class="input-label">Déboursé Sec Main d'Œuvre (€/u)</label><input type="number" id="f-k-ds-mo" class="input-field" value="12.50" step="0.5" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Déboursé Sec Matériel & Engins (€/u)</label><input type="number" id="f-k-ds-eng" class="input-field" value="4.20" step="0.5" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Déboursé Sec Matériaux (€/u)</label><input type="number" id="f-k-ds-mat" class="input-field" value="18.30" step="0.5" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Frais Généraux d'Entreprise FG (%)</label><input type="number" id="f-k-fg" class="input-field" value="16.0" step="0.5" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Frais Spéciaux de Chantier FC (%)</label><input type="number" id="f-k-fc" class="input-field" value="4.5" step="0.5" oninput="calculateTechniqueFormula()"></div>
                    <div class="input-group"><label class="input-label">Bénéfice & Aléas B&A (%)</label><input type="number" id="f-k-ba" class="input-field" value="5.5" step="0.5" oninput="calculateTechniqueFormula()"></div>
                </div>
            `;
        }

        calculateTechniqueFormula();
    }

    function calculateTechniqueFormula() {
        const type = document.getElementById('formula-type-select')?.value || 'cubature_terrassement';
        const out = document.getElementById('formula-calculation-output');
        if (!out) return;

        if (type === 'cubature_terrassement') {
            const l = Number(document.getElementById('f-cuba-l')?.value || 120);
            const w = Number(document.getElementById('f-cuba-w')?.value || 1.2);
            const h = Number(document.getElementById('f-cuba-h')?.value || 1.8);
            const cf = Number(document.getElementById('f-cuba-cf')?.value || 1.25);
            const rho = Number(document.getElementById('f-cuba-rho')?.value || 1.80);

            const vg = Number(document.getElementById('f-cuba-vg')?.value || 0.90);
            const tc = Number(document.getElementById('f-cuba-tc')?.value || 22);
            const kr = Number(document.getElementById('f-cuba-kr')?.value || 90) / 100;
            const kf = Number(document.getElementById('f-cuba-kf')?.value || 85) / 100;

            const camSelect = document.getElementById('f-cuba-cam-type')?.value || "14.0|8x4 Bi-benne 26t";
            const [camCapStr, camName] = camSelect.split('|');
            const camCap = Number(camCapStr) || 14.0;

            const nbCam = Number(document.getElementById('f-cuba-nb-cam')?.value || 4);
            const dist = Number(document.getElementById('f-cuba-dist')?.value || 12.0);
            const spd = Number(document.getElementById('f-cuba-spd')?.value || 35.0);
            const tdump = Number(document.getElementById('f-cuba-tdump')?.value || 5.0);

            // Step 1: Volumes
            const vPlace = l * w * h;
            const vFois = vPlace * cf;
            const totalTonnage = vFois * rho;

            // Step 2: Excavator actual rate
            // Q_reel = (3600 / Tc) * Vg * kr * kf (m3/h foisonne)
            const qReel = (3600 / tc) * vg * kr * kf;

            // Step 3: Truck rotation cycle
            const tChargeMin = (camCap / qReel) * 60; // minutes
            const tTrajetMin = (2 * dist / (spd || 30)) * 60; // minutes aller-retour
            const tCycleMin = tChargeMin + tTrajetMin + tdump + 3.0; // 3 min maneuvre/attente
            const nOptCamions = (tCycleMin / tChargeMin);
            const isBottleneckCamion = nbCam < nOptCamions;

            // Step 4: Actual site output & duration
            const debitCamions = nbCam * (camCap / (tCycleMin / 60)); // m3/h foisonne
            const debitReelChantier = isBottleneckCamion ? debitCamions : qReel;
            const dureeHeures = vFois / (debitReelChantier || 1);
            const dureeJours = dureeHeures / 7.0;
            const totalRotations = Math.ceil(vFois / camCap);

            out.innerHTML = `
                <div style="background: rgba(15,23,42,0.95); border: 2px solid var(--cyan); border-radius: 8px; padding: 1.25rem;">
                    <div style="font-size:0.85rem; font-weight:800; color:#38bdf8; text-transform:uppercase; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center;">
                        <span>🚜 Note de Calcul Détaillée : Terrassement & Rotation de Transport</span>
                        <span class="badge badge-info">Méthode FNTP / LCPC</span>
                    </div>

                    <!-- STEP 1 -->
                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 1 : Volume en Place & Volume Foisonné à Transporter</span>
                            <span class="badge badge-success">${vFois.toFixed(1)} m³ à évacuer</span>
                        </div>
                        <div class="formula-math-box">
                            V_place = L × l × h = ${l} × ${w} × ${h} = <strong>${vPlace.toFixed(1)} m³ en place</strong><br>
                            V_foisonne = V_place × Cf = ${vPlace.toFixed(1)} × ${cf} = <strong style="color:var(--amber);">${vFois.toFixed(1)} m³ foisonnés</strong> (${totalTonnage.toFixed(1)} tonnes à d = ${rho} t/m³)
                        </div>
                        <div class="formula-var-desc">Le volume foisonné correspond au volume réel que doivent charger la pelle et transporter les camions vers le centre de recyclage.</div>
                    </div>

                    <!-- STEP 2 -->
                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 2 : Débit Réel Net de la Pelle Excavatrice</span>
                            <span class="badge badge-info">${Math.round(qReel)} m³/h</span>
                        </div>
                        <div class="formula-math-box">
                            Q_reel = (3600 / Tc) × Vg × kr × kf<br>
                            Q_reel = (3600 / ${tc}s) × ${vg}m³ × ${(kr*100)}% × ${(kf*100)}% = <strong style="color:var(--emerald);">${qReel.toFixed(1)} m³/heure foisonnés</strong>
                        </div>
                        <div class="formula-var-desc">Prend en compte le temps de cycle godet (${tc}s), le coefficient de remplissage (${(kr*100)}%) et l'efficience de l'opérateur (${(kf*100)}%).</div>
                    </div>

                    <!-- STEP 3 -->
                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 3 : Rotation des Camions (${camName}) & Adéquation Pelle-Transport</span>
                            <span class="badge ${isBottleneckCamion ? 'badge-warning' : 'badge-success'}">${nbCam} camions affectés (Optimum: ${Math.ceil(nOptCamions)})</span>
                        </div>
                        <div class="formula-math-box">
                            • Temps de chargement par camion : T_charge = (${camCap}m³ / ${qReel.toFixed(1)}m³/h) × 60 = <strong>${tChargeMin.toFixed(1)} minutes</strong><br>
                            • Temps de trajet A/R (2 × ${dist}km à ${spd}km/h) : T_trajet = <strong>${tTrajetMin.toFixed(1)} minutes</strong><br>
                            • Temps de cycle complet d'un camion : T_cycle = ${tChargeMin.toFixed(1)} + ${tTrajetMin.toFixed(1)} + ${tdump}min + 3min attente = <strong>${tCycleMin.toFixed(1)} minutes</strong><br>
                            • <strong>Nombre théorique optimal de camions</strong> : N_opt = T_cycle / T_charge = ${tCycleMin.toFixed(1)} / ${tChargeMin.toFixed(1)} = <strong style="color:#38bdf8;">${nOptCamions.toFixed(1)} camions (soit ${Math.ceil(nOptCamions)} camions)</strong>
                        </div>
                        <div class="formula-var-desc" style="margin-top:4px;">
                            ${isBottleneckCamion ?
                                `<span style="color:var(--amber); font-weight:800;">⚠️ Goulot d'Étranglement Transport :</span> Avec ${nbCam} camions pour un besoin de ${Math.ceil(nOptCamions)}, la pelle tournera à ${((nbCam/nOptCamions)*100).toFixed(0)}% de sa capacité et attendra les camions. Débit réel bridé à ${debitReelChantier.toFixed(1)} m³/h.` :
                                `<span style="color:var(--emerald); font-weight:800;">✅ Pelle à 100% de Cadence :</span> Avec ${nbCam} camions pour un besoin de ${Math.ceil(nOptCamions)}, l'évacuation absorbe la totalité du débit de la pelle (${qReel.toFixed(1)} m³/h).`}
                        </div>
                    </div>

                    <!-- STEP 4 -->
                    <div class="formula-calc-step" style="border-left-color: var(--emerald); background: rgba(16,185,129,0.08);">
                        <div class="formula-step-title">
                            <span style="color:var(--emerald);">📌 Étape 4 : Durée Totale d'Exécution & Bilan Chantier</span>
                            <span class="badge badge-success">${totalRotations} rotations</span>
                        </div>
                        <div class="formula-math-box">
                            • Nombre total de rotations à réaliser : N_tours = ${vFois.toFixed(1)} / ${camCap} = <strong>${totalRotations} bennes</strong><br>
                            • Débit effectif réel du chantier : <strong>${debitReelChantier.toFixed(1)} m³/h foisonnés</strong><br>
                            • <strong>Durée totale estimée du terrassement :</strong> T = ${vFois.toFixed(1)}m³ / ${debitReelChantier.toFixed(1)}m³/h = <strong style="font-size:1.05rem; color:var(--emerald);">${dureeHeures.toFixed(1)} heures</strong> (soit <strong style="color:#38bdf8;">${dureeJours.toFixed(2)} jour ouvré</strong> de 7h)
                        </div>
                        <div class="formula-var-desc">Ce délai inclut la rotation réelle des véhicules, les temps de chargement, de transport et de déchargement sur le site de recyclage.</div>
                    </div>
                </div>
            `;
        } else if (type === 'tonnage_enrobes') {
            const s = Number(document.getElementById('f-enr-s')?.value || 1200);
            const e = Number(document.getElementById('f-enr-e')?.value || 5.0);
            const mv = Number(document.getElementById('f-enr-mv')?.value || 2.45);
            const perte = Number(document.getElementById('f-enr-perte')?.value || 3.0);
            const emul = Number(document.getElementById('f-enr-emul')?.value || 500);
            const cad = Number(document.getElementById('f-enr-cad')?.value || 45);

            const vComp = s * (e / 100);
            const tonnageTheorique = vComp * mv;
            const tonnageReel = tonnageTheorique * (1 + perte / 100);
            const nbSemis = Math.ceil(tonnageReel / 25);
            const emulsionKg = s * (emul / 1000);
            const dureePoseH = tonnageReel / (cad || 1);

            out.innerHTML = `
                <div style="background: rgba(15,23,42,0.95); border: 2px solid var(--cyan); border-radius: 8px; padding: 1.25rem;">
                    <div style="font-size:0.85rem; font-weight:800; color:#38bdf8; text-transform:uppercase; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center;">
                        <span>🛣️ Note de Calcul : Tonnage d'Enrobés Chauds BBSG 0/10 & Émulsion</span>
                        <span class="badge badge-info">Norme NF EN 13108-1</span>
                    </div>

                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 1 : Surface & Tonnage Brut Théorique</span>
                            <span class="badge badge-info">${vComp.toFixed(1)} m³ compactés</span>
                        </div>
                        <div class="formula-math-box">
                            • Volume en place : V = S × e = ${s} m² × ${(e/100)} m = <strong>${vComp.toFixed(1)} m³</strong><br>
                            • Masse théorique : M = V × ρ = ${vComp.toFixed(1)} m³ × ${mv} t/m³ = <strong>${tonnageTheorique.toFixed(1)} tonnes</strong>
                        </div>
                    </div>

                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 2 : Commande Centrale & Semi-Remorques Isothermes (25t)</span>
                            <span class="badge badge-success">${Math.round(tonnageReel)} Tonnes à commander</span>
                        </div>
                        <div class="formula-math-box">
                            • Majoration pour pertes et compactage (+${perte}%) : T_commande = ${tonnageTheorique.toFixed(1)} × ${(1+perte/100).toFixed(2)} = <strong style="color:var(--amber);">${tonnageReel.toFixed(1)} tonnes</strong><br>
                            • Nombre de rotations semi-remorques isothermes 25t : N = ${tonnageReel.toFixed(1)} / 25 = <strong style="color:var(--emerald);">${nbSemis} semi-remorques</strong>
                        </div>
                    </div>

                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 3 : Couche d'Accrochage Émulsion C65B4</span>
                            <span class="badge badge-warning">${Math.round(emulsionKg)} kg</span>
                        </div>
                        <div class="formula-math-box">
                            • Émulsion dosée à ${emul} g/m² : Masse = ${s} m² × ${(emul/1000)} kg/m² = <strong>${emulsionKg.toFixed(0)} kg</strong> (soit ~${Math.round(emulsionKg / 1.02)} litres)
                        </div>
                    </div>

                    <div class="formula-calc-step" style="border-left-color: var(--emerald); background: rgba(16,185,129,0.08);">
                        <div class="formula-step-title">
                            <span style="color:var(--emerald);">📌 Étape 4 : Durée d'Application au Finisseur</span>
                            <span class="badge badge-success">${dureePoseH.toFixed(1)} heures</span>
                        </div>
                        <div class="formula-math-box">
                            • Cadence de mise en œuvre : ${cad} t/h<br>
                            • <strong>Temps d'application continue :</strong> T = ${tonnageReel.toFixed(1)} t / ${cad} t/h = <strong style="color:var(--emerald); font-size:1.05rem;">${dureePoseH.toFixed(1)} heures</strong> (soit ${(dureePoseH/7).toFixed(2)} jour de 7h)
                        </div>
                    </div>
                </div>
            `;
        } else if (type === 'perimetre_bordures') {
            const l = Number(document.getElementById('f-bord-l')?.value || 280);
            const w = Number(document.getElementById('f-bord-w')?.value || 0.30);
            const h = Number(document.getElementById('f-bord-h')?.value || 0.15);
            const ep = Number(document.getElementById('f-bord-ep')?.value || 0.025);
            const cad = Number(document.getElementById('f-bord-cad')?.value || 8.5);
            const casse = Number(document.getElementById('f-bord-casse')?.value || 3.0);

            const nbBorduresTheorique = l; // bordures de 1m
            const nbBorduresCommande = Math.ceil(nbBorduresTheorique * (1 + casse / 100));
            const vSemelle = l * w * h;
            const vEpaulement = l * ep;
            const vBetonTotal = (vSemelle + vEpaulement) * 1.05; // 5% perte
            const dureePoseH = l / (cad || 1);

            out.innerHTML = `
                <div style="background: rgba(15,23,42,0.95); border: 2px solid var(--cyan); border-radius: 8px; padding: 1.25rem;">
                    <div style="font-size:0.85rem; font-weight:800; color:#38bdf8; text-transform:uppercase; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center;">
                        <span>📏 Note de Calcul : Bordures T2 / P1, Semelle Béton & Cadence</span>
                        <span class="badge badge-info">Norme NF P 98-305</span>
                    </div>

                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 1 : Quantité de Bordures à Commander</span>
                            <span class="badge badge-success">${nbBorduresCommande} unités (L=1.00m)</span>
                        </div>
                        <div class="formula-math-box">
                            • Linéaire de projet : ${l} ml (éléments de 1.00m)<br>
                            • Majoration pour coupes et chutes (+${casse}%) : <strong>${nbBorduresCommande} bordures</strong> (soit ~${Math.ceil(nbBorduresCommande / 33)} palettes de 33u)
                        </div>
                    </div>

                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 2 : Volume Béton de Calage C25/30</span>
                            <span class="badge badge-warning">${vBetonTotal.toFixed(2)} m³ BPE</span>
                        </div>
                        <div class="formula-math-box">
                            • Volume semelle sous bordure : V_semelle = ${l} × ${w} × ${h} = <strong>${vSemelle.toFixed(2)} m³</strong><br>
                            • Volume solin / épaulement arrière : V_solin = ${l} × ${ep} = <strong>${vEpaulement.toFixed(2)} m³</strong><br>
                            • Volume total à commander (+5% pertes) : V_total = <strong style="color:var(--amber);">${vBetonTotal.toFixed(2)} m³</strong> (~${Math.ceil(vBetonTotal / 7)} camions toupie 7m³)
                        </div>
                    </div>

                    <div class="formula-calc-step" style="border-left-color: var(--emerald); background: rgba(16,185,129,0.08);">
                        <div class="formula-step-title">
                            <span style="color:var(--emerald);">📌 Étape 3 : Temps de Pose de l'Équipe</span>
                            <span class="badge badge-success">${(dureePoseH / 7).toFixed(1)} jours de 7h</span>
                        </div>
                        <div class="formula-math-box">
                            • Cadence moyenne d'une équipe de 2 poseurs : ${cad} ml/heure (soit ~${Math.round(cad * 7)} ml/jour)<br>
                            • <strong>Durée totale de pose :</strong> T = ${l} ml / ${cad} ml/h = <strong style="color:var(--emerald); font-size:1.05rem;">${dureePoseH.toFixed(1)} heures</strong> (soit <strong style="color:#38bdf8;">${(dureePoseH/7).toFixed(2)} jours</strong>)
                        </div>
                    </div>
                </div>
            `;
        } else if (type === 'manning_hydraulique') {
            const dMm = Number(document.getElementById('f-man-d')?.value || 400);
            const d = dMm / 1000;
            const i = Number(document.getElementById('f-man-i')?.value || 0.015);
            const k = Number(document.getElementById('f-man-k')?.value || 85);

            const sectionPleine = (Math.PI * Math.pow(d, 2)) / 4;
            const rhPlein = d / 4;
            const vPlein = k * Math.pow(rhPlein, 2/3) * Math.pow(i, 1/2);
            const qPlein = sectionPleine * vPlein * 1000; // L/s

            const isVitesseOk = vPlein >= 0.6 && vPlein <= 4.0;

            out.innerHTML = `
                <div style="background: rgba(15,23,42,0.95); border: 2px solid var(--cyan); border-radius: 8px; padding: 1.25rem;">
                    <div style="font-size:0.85rem; font-weight:800; color:#38bdf8; text-transform:uppercase; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center;">
                        <span>💧 Note Hydraulique : Formule de Manning-Strickler (Collecteur Ø${dMm})</span>
                        <span class="badge badge-info">Fascicule 70 Titre I</span>
                    </div>

                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 1 : Rayon Hydraulique & Section Mouillée Pleine</span>
                            <span class="badge badge-info">D = ${(d*1000)} mm</span>
                        </div>
                        <div class="formula-math-box">
                            • Section pleine : S = π × D² / 4 = π × ${d}² / 4 = <strong>${sectionPleine.toFixed(4)} m²</strong><br>
                            • Périmètre mouillé : P = π × D = ${(Math.PI * d).toFixed(3)} m<br>
                            • Rayon hydraulique : Rh = D / 4 = ${d} / 4 = <strong>${rhPlein.toFixed(4)} m</strong>
                        </div>
                    </div>

                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 2 : Vitesse d'Écoulement & Vérification Auto-Curage</span>
                            <span class="badge ${isVitesseOk ? 'badge-success' : 'badge-danger'}">${vPlein.toFixed(2)} m/s</span>
                        </div>
                        <div class="formula-math-box">
                            V = K × Rh^(2/3) × I^(1/2) = ${k} × (${rhPlein.toFixed(4)})^(0.667) × (${i})^(0.5) = <strong style="color:var(--emerald);">${vPlein.toFixed(2)} m/s</strong>
                        </div>
                        <div class="formula-var-desc">
                            ${isVitesseOk ?
                                `<span style="color:var(--emerald); font-weight:700;">✅ Vitesse Conforme :</span> La vitesse est comprise entre 0.60 m/s (auto-curage garanti sans dépôt) et 4.00 m/s (absence d'abrasion des parois).` :
                                `<span style="color:var(--rose); font-weight:700;">⚠️ Vitesse Hors Norme :</span> Ajuster la pente du collecteur.`}
                        </div>
                    </div>

                    <div class="formula-calc-step" style="border-left-color: var(--emerald); background: rgba(16,185,129,0.08);">
                        <div class="formula-step-title">
                            <span style="color:var(--emerald);">📌 Étape 3 : Débit Maximal à Pleine Section</span>
                            <span class="badge badge-success">${Math.round(qPlein)} L/s</span>
                        </div>
                        <div class="formula-math-box">
                            Q = S × V = ${sectionPleine.toFixed(4)} m² × ${vPlein.toFixed(2)} m/s = <strong style="color:var(--emerald); font-size:1.05rem;">${(qPlein / 1000).toFixed(3)} m³/s</strong> (soit <strong style="color:#38bdf8;">${qPlein.toFixed(1)} Litres/seconde</strong>)
                        </div>
                    </div>
                </div>
            `;
        } else if (type === 'pente_canalisateur') {
            const zam = Number(document.getElementById('f-pen-zam')?.value || 45.850);
            const zav = Number(document.getElementById('f-pen-zav')?.value || 45.220);
            const l = Number(document.getElementById('f-pen-l')?.value || 42.00);
            const elem = Number(document.getElementById('f-pen-elem')?.value || 3.00);

            const deltaH = zam - zav;
            const pentePourcent = (deltaH / (l || 1)) * 100;
            const penteMmParMetre = (deltaH / (l || 1)) * 1000;
            const deltaHParTuyau = (penteMmParMetre * elem);

            out.innerHTML = `
                <div style="background: rgba(15,23,42,0.95); border: 2px solid var(--cyan); border-radius: 8px; padding: 1.25rem;">
                    <div style="font-size:0.85rem; font-weight:800; color:#38bdf8; text-transform:uppercase; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center;">
                        <span>📐 Note Altimétrie : Calcul de Pente & Calage Laser Canalisateur</span>
                        <span class="badge badge-info">Laser Piper 200</span>
                    </div>

                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 1 : Dénivelée Brute entre Regards</span>
                            <span class="badge badge-info">ΔH = ${deltaH.toFixed(3)} m</span>
                        </div>
                        <div class="formula-math-box">
                            ΔH = Z_amont - Z_aval = ${zam.toFixed(3)} m - ${zav.toFixed(3)} m = <strong style="color:var(--amber);">${deltaH.toFixed(3)} m (${Math.round(deltaH*1000)} mm)</strong>
                        </div>
                    </div>

                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 2 : Pente Réelle en % et mm/m</span>
                            <span class="badge badge-success">${pentePourcent.toFixed(2)} %</span>
                        </div>
                        <div class="formula-math-box">
                            • Pente en % : P = (ΔH / L) × 100 = (${deltaH.toFixed(3)} / ${l}) × 100 = <strong style="color:var(--emerald);">${pentePourcent.toFixed(2)} %</strong><br>
                            • Pente unitaire : P = <strong style="color:#38bdf8;">${penteMmParMetre.toFixed(1)} mm par mètre linéaire</strong>
                        </div>
                    </div>

                    <div class="formula-calc-step" style="border-left-color: var(--emerald); background: rgba(16,185,129,0.08);">
                        <div class="formula-step-title">
                            <span style="color:var(--emerald);">📌 Étape 3 : Calage du Laser Piper & Baisse par Barre de Tuyau</span>
                            <span class="badge badge-success">${deltaHParTuyau.toFixed(1)} mm / tuyau</span>
                        </div>
                        <div class="formula-math-box">
                            • Réglage écran Laser Canalisateur : <strong style="color:#38bdf8;">-${pentePourcent.toFixed(2)} %</strong><br>
                            • Baisse d'altitude par élément de ${elem}m : Δh_tuyau = ${penteMmParMetre.toFixed(1)} mm/m × ${elem}m = <strong style="color:var(--emerald); font-size:1.05rem;">${deltaHParTuyau.toFixed(1)} mm</strong>
                        </div>
                    </div>
                </div>
            `;
        } else if (type === 'compactage_gtr') {
            const e = Number(document.getElementById('f-cmp-e')?.value || 25);
            const w = Number(document.getElementById('f-cmp-w')?.value || 1.70);
            const v = Number(document.getElementById('f-cmp-v')?.value || 3.5);
            const n = Number(document.getElementById('f-cmp-n')?.value || 6);
            const vtot = Number(document.getElementById('f-cmp-vtot')?.value || 450);

            // Q/S = (e * L * V * 1000) / n (m3/h)
            const debitCompacteur = ((e / 100) * w * (v * 1000)) / (n || 1);
            const dureeCompactageH = vtot / (debitCompacteur || 1);

            out.innerHTML = `
                <div style="background: rgba(15,23,42,0.95); border: 2px solid var(--cyan); border-radius: 8px; padding: 1.25rem;">
                    <div style="font-size:0.85rem; font-weight:800; color:#38bdf8; text-transform:uppercase; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center;">
                        <span>🔨 Note Compactage GTR : Débit Q/S & Durée au Rouleau</span>
                        <span class="badge badge-info">Norme NF P 98-736</span>
                    </div>

                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 1 : Débit Pratique du Compacteur Q/S</span>
                            <span class="badge badge-success">${Math.round(debitCompacteur)} m³/h</span>
                        </div>
                        <div class="formula-math-box">
                            Q/S = (e × L × V) / N<br>
                            Q/S = (${(e/100)}m × ${w}m × ${v*1000}m/h) / ${n} passes = <strong style="color:var(--emerald);">${debitCompacteur.toFixed(1)} m³/h</strong>
                        </div>
                    </div>

                    <div class="formula-calc-step" style="border-left-color: var(--emerald); background: rgba(16,185,129,0.08);">
                        <div class="formula-step-title">
                            <span style="color:var(--emerald);">📌 Étape 2 : Durée de Compactage pour ${vtot} m³ de GNT</span>
                            <span class="badge badge-success">${dureeCompactageH.toFixed(1)} heures</span>
                        </div>
                        <div class="formula-math-box">
                            • Volume total à compacter : ${vtot} m³<br>
                            • <strong>Temps machine rouleau vibrant :</strong> T = ${vtot} m³ / ${debitCompacteur.toFixed(1)} m³/h = <strong style="color:var(--emerald); font-size:1.05rem;">${dureeCompactageH.toFixed(1)} heures</strong> (soit ${(dureeCompactageH/7).toFixed(2)} jour de 7h)
                        </div>
                    </div>
                </div>
            `;
        } else if (type === 'revision_tp08') {
            const p0 = Number(document.getElementById('f-rev-p0')?.value || 85000);
            const a = Number(document.getElementById('f-rev-a')?.value || 0.15);
            const i0 = Number(document.getElementById('f-rev-i0')?.value || 122.4);
            const in_val = Number(document.getElementById('f-rev-in')?.value || 129.8);

            const partVariable = (1 - a);
            const coefRevision = a + (partVariable * (in_val / (i0 || 1)));
            const pRevise = p0 * coefRevision;
            const plusValue = pRevise - p0;
            const pctHausse = (coefRevision - 1) * 100;

            out.innerHTML = `
                <div style="background: rgba(15,23,42,0.95); border: 2px solid var(--cyan); border-radius: 8px; padding: 1.25rem;">
                    <div style="font-size:0.85rem; font-weight:800; color:#38bdf8; text-transform:uppercase; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center;">
                        <span>📈 Note Révision de Prix : Formule Paramétrique Index TP08</span>
                        <span class="badge badge-info">CCAG Travaux 2021 Art. 10</span>
                    </div>

                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 1 : Calcul du Coefficient de Révision Cn</span>
                            <span class="badge badge-info">Cn = ${coefRevision.toFixed(4)}</span>
                        </div>
                        <div class="formula-math-box">
                            Cn = ${a} + (1 - ${a}) × (TP08_n / TP08_0)<br>
                            Cn = ${a} + ${(partVariable).toFixed(2)} × (${in_val} / ${i0}) = <strong style="color:var(--emerald);">${coefRevision.toFixed(4)}</strong> (+${pctHausse.toFixed(2)}%)
                        </div>
                    </div>

                    <div class="formula-calc-step" style="border-left-color: var(--emerald); background: rgba(16,185,129,0.08);">
                        <div class="formula-step-title">
                            <span style="color:var(--emerald);">📌 Étape 2 : Montant Révisé & Plus-Value Contractuelle</span>
                            <span class="badge badge-success">+${Math.round(plusValue).toLocaleString('fr-FR')} € HT</span>
                        </div>
                        <div class="formula-math-box">
                            • Montant initial de la situation : ${p0.toLocaleString('fr-FR')} € HT<br>
                            • <strong>Montant révisé à facturer :</strong> P_rev = ${p0} × ${coefRevision.toFixed(4)} = <strong style="color:var(--emerald); font-size:1.05rem;">${pRevise.toLocaleString('fr-FR', {minimumFractionDigits:2, maximumFractionDigits:2})} € HT</strong><br>
                            • Plus-value de révision d'index : <strong style="color:var(--amber);">+${plusValue.toLocaleString('fr-FR', {minimumFractionDigits:2, maximumFractionDigits:2})} € HT</strong>
                        </div>
                    </div>
                </div>
            `;
        } else if (type === 'debourse_sec_k') {
            const dsMO = Number(document.getElementById('f-k-ds-mo')?.value || 12.50);
            const dsEng = Number(document.getElementById('f-k-ds-eng')?.value || 4.20);
            const dsMat = Number(document.getElementById('f-k-ds-mat')?.value || 18.30);
            const fg = Number(document.getElementById('f-k-fg')?.value || 16.0);
            const fc = Number(document.getElementById('f-k-fc')?.value || 4.5);
            const ba = Number(document.getElementById('f-k-ba')?.value || 5.5);

            const dsTotal = dsMO + dsEng + dsMat;
            const totalFraisPct = fg + fc + ba;
            const k = 1 / (1 - (totalFraisPct / 100));
            const pvHT = dsTotal * k;
            const margeBruteEuro = pvHT - dsTotal;

            out.innerHTML = `
                <div style="background: rgba(15,23,42,0.95); border: 2px solid var(--cyan); border-radius: 8px; padding: 1.25rem;">
                    <div style="font-size:0.85rem; font-weight:800; color:#38bdf8; text-transform:uppercase; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center;">
                        <span>💰 Note d'Étude de Prix : Déboursé Sec (DS) & Multiplicateur K</span>
                        <span class="badge badge-info">Méthode FNTP</span>
                    </div>

                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 1 : Déboursé Sec Total Unitaire (DS)</span>
                            <span class="badge badge-info">DS = ${dsTotal.toFixed(2)} € / u</span>
                        </div>
                        <div class="formula-math-box">
                            DS = DS_MO (${dsMO.toFixed(2)}€) + DS_Matériel (${dsEng.toFixed(2)}€) + DS_Matériaux (${dsMat.toFixed(2)}€) = <strong style="color:var(--emerald);">${dsTotal.toFixed(2)} € HT</strong>
                        </div>
                    </div>

                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 2 : Coefficient de Vente K</span>
                            <span class="badge badge-warning">K = ${k.toFixed(3)}</span>
                        </div>
                        <div class="formula-math-box">
                            • Somme des Frais : FG (${fg}%) + FC (${fc}%) + B&A (${ba}%) = <strong>${totalFraisPct.toFixed(1)} % du Prix de Vente</strong><br>
                            • Formule de K : K = 1 / (1 - ${(totalFraisPct/100).toFixed(3)}) = <strong style="color:var(--amber); font-size:1.05rem;">${k.toFixed(3)}</strong>
                        </div>
                    </div>

                    <div class="formula-calc-step" style="border-left-color: var(--emerald); background: rgba(16,185,129,0.08);">
                        <div class="formula-step-title">
                            <span style="color:var(--emerald);">📌 Étape 3 : Prix de Vente Unitaire au BPU / DQE</span>
                            <span class="badge badge-success">PV = ${pvHT.toFixed(2)} € HT</span>
                        </div>
                        <div class="formula-math-box">
                            • <strong>Prix de Vente HT :</strong> PV_HT = DS × K = ${dsTotal.toFixed(2)} € × ${k.toFixed(3)} = <strong style="color:var(--emerald); font-size:1.15rem;">${pvHT.toFixed(2)} € HT / unité</strong><br>
                            • Marge commerciale unitaire brute : <strong style="color:#38bdf8;">+${margeBruteEuro.toFixed(2)} € / unité</strong>
                        </div>
                    </div>
                </div>
            `;
        }
    }
'''

with open('scripts/section_js_part3.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace updateFormulaCalculator and calculateTechniqueFormula
uf_start = text.find('function updateFormulaCalculator()')
uf_end = text.find('// 18.2 DYNAMIC INTERACTIVE TASK SHEETS')
if uf_start != -1 and uf_end != -1:
    text = text[:uf_start] + new_formula_calc_code.strip() + "\n\n    " + text[uf_end:]
    print("Formula calculator upgraded with clear visual step-by-step cards and fleet rotations!")
else:
    print("Error locating formula calculator boundaries")

with open('scripts/section_js_part3.py', 'w', encoding='utf-8') as f:
    f.write(text)
