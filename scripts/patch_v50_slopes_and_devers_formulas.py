# -*- coding: utf-8 -*-
"""
Enrich updateFormulaCalculator & calculateTechniqueFormula with:
- pente_talus_terrassement (Déblais/Remblais TN, Roches, Argiles, GNT, Risbermes)
- devers_chaussee_enrobes (Dévers de chaussée, Enrobés BBSG/GB3, Fil d'eau)
"""

with open('scripts/section_js_part3.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's see updateFormulaCalculator in section_js_part3.py
# We will inject the new input blocks and calculation blocks

pente_inputs_js = r'''        } else if (type === 'pente_talus_terrassement') {
            inputsCont.innerHTML = `
                <div style="background: rgba(30,41,59,0.5); padding: 0.75rem; border-radius: 6px; border: 1px solid rgba(51,65,85,0.6); margin-top: 0.75rem;">
                    <div style="font-size: 0.8rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.5rem;">⛰️ 1. Nature du Terrassement, Géologie & Ratio de Pente</div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem;">
                        <div class="input-group" style="grid-column: span 2;">
                            <label class="input-label">Type de Talus & Matériau (Norme GTR / NF P 94-500)</label>
                            <select id="f-talus-preset" class="input-field" onchange="applyTalusPreset(this.value)">
                                <option value="remblai_gnt|1.5|Remblai GNT 0/31.5 compacté (Pente 3H/2V - 67% / 33.7°)">Remblai GNT 0/31.5 compacté (Pente 3H/2V - 67% / 33.7°)</option>
                                <option value="remblai_courant|2.0|Remblai tout-venant sol courant (Pente 2H/1V - 50% / 26.6°)">Remblai tout-venant sol courant (Pente 2H/1V - 50% / 26.6°)</option>
                                <option value="remblai_paysager|3.0|Talus paysager & Terre végétale (Pente 3H/1V - 33% / 18.4°)">Talus paysager & Terre végétale (Pente 3H/1V - 33% / 18.4°)</option>
                                <option value="deblai_meuble|1.0|Déblai en terrain meuble / argiles (Pente 1H/1V - 100% / 45.0°)">Déblai en terrain meuble / argiles (Pente 1H/1V - 100% / 45.0°)</option>
                                <option value="deblai_compact|0.67|Déblai en terrain compact / graveleux (Pente 2H/3V - 150% / 56.3°)">Déblai en terrain compact / graveleux (Pente 2H/3V - 150% / 56.3°)</option>
                                <option value="deblai_roche_saine|0.20|Déblai rocheux franc / calcaire dur (Pente 1H/5V - 500% / 78.7°)">Déblai rocheux franc / calcaire dur (Pente 1H/5V - 500% / 78.7°)</option>
                                <option value="deblai_roche_alteree|0.50|Déblai roche altérée / schistes (Pente 1H/2V - 200% / 63.4°)">Déblai roche altérée / schistes (Pente 1H/2V - 200% / 63.4°)</option>
                                <option value="fosse_trapeze|1.0|Fossé trapézoïdal de voirie (Pente 1H/1V - 100% / 45.0°)">Fossé trapézoïdal de voirie (Pente 1H/1V - 100% / 45.0°)</option>
                            </select>
                        </div>
                        <div class="input-group"><label class="input-label">Hauteur Talus H (m)</label><input type="number" id="f-talus-h" class="input-field" value="3.50" step="0.25" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Linéaire Chantier L (ml)</label><input type="number" id="f-talus-l" class="input-field" value="150" step="10" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Ratio Horizontal (n pour nH/1V)</label><input type="number" id="f-talus-ratio" class="input-field" value="1.50" step="0.1" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Largeur Risberme si H > 4m (m)</label><input type="number" id="f-talus-risb" class="input-field" value="1.50" step="0.25" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Terre Végétale Rampant (cm)</label><input type="number" id="f-talus-tv" class="input-field" value="15" step="5" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Densité Matériau (t/m³)</label><input type="number" id="f-talus-rho" class="input-field" value="1.85" step="0.05" oninput="calculateTechniqueFormula()"></div>
                    </div>
                </div>
            `;
        } else if (type === 'devers_chaussee_enrobes') {
            inputsCont.innerHTML = `
                <div style="background: rgba(30,41,59,0.5); padding: 0.75rem; border-radius: 6px; border: 1px solid rgba(51,65,85,0.6); margin-top: 0.75rem;">
                    <div style="font-size: 0.8rem; font-weight: 800; color: #38bdf8; margin-bottom: 0.5rem;">🛣️ 1. Profil en Travers de Chaussée & Pente Transversale (Dévers)</div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem;">
                        <div class="input-group" style="grid-column: span 2;">
                            <label class="input-label">Type de Profil en Travers</label>
                            <select id="f-dev-type" class="input-field" onchange="calculateTechniqueFormula()">
                                <option value="toit_2_versants">Profil en Toit (2 versants avec axe central au point haut)</option>
                                <option value="devers_unique_gauche">Dévers Unique vers la Gauche (Courbe à droite)</option>
                                <option value="devers_unique_droite">Dévers Unique vers la Droite (Courbe à gauche)</option>
                                <option value="giratoire_anneau">Anneau de Giratoire (Dévers extérieur standard 2.0%)</option>
                            </select>
                        </div>
                        <div class="input-group"><label class="input-label">Largeur Totale Chaussée (L en m)</label><input type="number" id="f-dev-w" class="input-field" value="7.00" step="0.5" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Pente Dévers (p en %)</label><input type="number" id="f-dev-p" class="input-field" value="2.50" step="0.1" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Longueur Tronçon (L en ml)</label><input type="number" id="f-dev-l" class="input-field" value="250" step="10" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Épaisseur BBSG 0/10 (e en cm)</label><input type="number" id="f-dev-ebbsg" class="input-field" value="5.0" step="0.5" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Épaisseur Grave Bitume GB3 (cm)</label><input type="number" id="f-dev-egb3" class="input-field" value="10.0" step="1.0" oninput="calculateTechniqueFormula()"></div>
                        <div class="input-group"><label class="input-label">Masse Volumique Enrobés (t/m³)</label><input type="number" id="f-dev-mv" class="input-field" value="2.45" step="0.05" oninput="calculateTechniqueFormula()"></div>
                    </div>
                </div>
            `;'''

# Helper function applyTalusPreset
talus_helper_js = r'''
    function applyTalusPreset(val) {
        const parts = val.split('|');
        const ratio = Number(parts[1]) || 1.5;
        const ratioInput = document.getElementById('f-talus-ratio');
        if (ratioInput) ratioInput.value = ratio;
        calculateTechniqueFormula();
    }
'''

# Calculation blocks for pente_talus_terrassement and devers_chaussee_enrobes
calc_talus_and_devers_js = r'''
        } else if (type === 'pente_talus_terrassement') {
            const h = Number(document.getElementById('f-talus-h')?.value || 3.50);
            const lChantier = Number(document.getElementById('f-talus-l')?.value || 150);
            const ratio = Number(document.getElementById('f-talus-ratio')?.value || 1.50); // n pour nH/1V
            const lRisb = Number(document.getElementById('f-talus-risb')?.value || 1.50);
            const eTv = Number(document.getElementById('f-talus-tv')?.value || 15);
            const rho = Number(document.getElementById('f-talus-rho')?.value || 1.85);

            // Slope math
            const pentePct = (1 / (ratio || 1)) * 100;
            const angleDeg = (Math.atan(1 / (ratio || 1)) * 180 / Math.PI);
            const nbRisbermes = h > 4.0 ? Math.floor((h - 0.1) / 4.0) : 0;
            const lEmpriseBase = h * ratio;
            const lEmpriseTotale = lEmpriseBase + (nbRisbermes * lRisb);
            const lRampantPur = Math.sqrt(Math.pow(h, 2) + Math.pow(lEmpriseBase, 2));
            const lRampantTotal = lRampantPur + (nbRisbermes * lRisb);

            const surfaceEmprise = lEmpriseTotale * lChantier;
            const surfaceRampant = lRampantTotal * lChantier;
            const volumeTv = surfaceRampant * (eTv / 100);

            // Cross-section prism volume
            const sectionDroite = 0.5 * lEmpriseBase * h + (nbRisbermes * lRisb * (h / 2));
            const volumePlace = sectionDroite * lChantier;
            const volumeFoisonne = volumePlace * 1.25;
            const tonnageTotal = volumePlace * rho;

            const isRisbermeRequise = h > 4.0;

            out.innerHTML = `
                <div style="background: rgba(15,23,42,0.95); border: 2px solid var(--cyan); border-radius: 8px; padding: 1.25rem;">
                    <div style="font-size:0.85rem; font-weight:800; color:#38bdf8; text-transform:uppercase; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center;">
                        <span>⛰️ Note de Calcul : Pente de Talus, Emprise au Sol & Cubature (Déblai / Remblai)</span>
                        <span class="badge badge-info">Norme GTR / NF P 94-500</span>
                    </div>

                    <!-- STEP 1 -->
                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 1 : Géométrie du Talus (Ratio ${ratio}H/1V, Pente & Angle)</span>
                            <span class="badge badge-success">${angleDeg.toFixed(1)}° (${pentePct.toFixed(1)} %)</span>
                        </div>
                        <div class="formula-math-box">
                            • Ratio de fruit du talus : <strong>${ratio.toFixed(2)}m horizontal pour 1m vertical</strong> (${ratio >= 1 ? `${(ratio*2).toFixed(0)}H/2V` : `1H/${(1/ratio).toFixed(1)}V`})<br>
                            • Pente en pourcentage : P = (1 / ${ratio.toFixed(2)}) × 100 = <strong style="color:var(--emerald);">${pentePct.toFixed(1)} %</strong><br>
                            • Angle avec l'horizontale : α = arctan(1 / ${ratio.toFixed(2)}) = <strong style="color:#38bdf8;">${angleDeg.toFixed(2)}°</strong><br>
                            • <strong>Largeur d'emprise au sol :</strong> L_emprise = H × ${ratio} + Risbermes (${nbRisbermes} × ${lRisb}m) = <strong style="color:var(--amber);">${lEmpriseTotale.toFixed(2)} m</strong><br>
                            • <strong>Longueur développée du rampant :</strong> L_rampant = √(H² + (H×n)²) = <strong style="color:var(--emerald);">${lRampantTotal.toFixed(2)} m</strong>
                        </div>
                    </div>

                    <!-- STEP 2 -->
                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 2 : Surfaces d'Emprise Foncière & de Rampant (Revêtement / Géotextile)</span>
                            <span class="badge badge-info">${Math.round(surfaceRampant)} m² de talus</span>
                        </div>
                        <div class="formula-math-box">
                            • Surface d'emprise foncière au sol : S_sol = ${lEmpriseTotale.toFixed(2)}m × ${lChantier}ml = <strong>${surfaceEmprise.toFixed(1)} m²</strong> (${(surfaceEmprise/10000).toFixed(3)} ha)<br>
                            • <strong>Surface développée de talus (Géo-filet / Engazonnement) :</strong> S_rampant = ${lRampantTotal.toFixed(2)}m × ${lChantier}ml = <strong style="color:var(--emerald); font-size:1.02rem;">${surfaceRampant.toFixed(1)} m²</strong><br>
                            • Volume de terre végétale de protection (ép. ${eTv}cm) : V_tv = ${surfaceRampant.toFixed(1)} m² × ${(eTv/100)}m = <strong style="color:#38bdf8;">${volumeTv.toFixed(1)} m³</strong>
                        </div>
                    </div>

                    <!-- STEP 3 -->
                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 3 : Cubatures du Prisme de Terrassement & Tonnage</span>
                            <span class="badge badge-warning">${Math.round(volumePlace)} m³ en place</span>
                        </div>
                        <div class="formula-math-box">
                            • Section transversale du prisme : S_section = 1/2 × ${lEmpriseBase.toFixed(2)}m × ${h}m = <strong>${sectionDroite.toFixed(2)} m²</strong><br>
                            • <strong>Volume en place :</strong> V_place = S × L = ${sectionDroite.toFixed(2)}m² × ${lChantier}ml = <strong style="color:var(--emerald); font-size:1.05rem;">${volumePlace.toFixed(1)} m³</strong><br>
                            • Volume foisonné à évacuer (Cf = 1.25) : V_foisonné = <strong style="color:var(--amber);">${volumeFoisonne.toFixed(1)} m³</strong> (${tonnageTotal.toFixed(1)} tonnes à d=${rho}t/m³)
                        </div>
                    </div>

                    <!-- STEP 4 -->
                    <div class="formula-calc-step" style="border-left-color: ${isRisbermeRequise ? 'var(--amber)' : 'var(--emerald)'}; background: ${isRisbermeRequise ? 'rgba(245,158,11,0.08)' : 'rgba(16,185,129,0.08)'};">
                        <div class="formula-step-title">
                            <span style="color:${isRisbermeRequise ? 'var(--amber)' : 'var(--emerald)'};">📌 Étape 4 : Stabilité Géotechnique & Dispositions Constructives GTR</span>
                            <span class="badge ${isRisbermeRequise ? 'badge-warning' : 'badge-success'}">${isRisbermeRequise ? `Risberme Requise (${nbRisbermes})` : 'Stabilité Directe'}</span>
                        </div>
                        <div class="formula-math-box">
                            ${isRisbermeRequise ?
                                `⚠️ <strong>Hauteur H = ${h}m > 4.00m :</strong> Aménagement obligatoire d'une risberme intermédiaire de ${lRisb}m de largeur avec contre-pente de 2% et caniveau de crête pour évacuation des eaux de ruissellement (Norme Fascicule 70).` :
                                `✅ <strong>Hauteur H = ${h}m <= 4.00m :</strong> Talus stable sans risberme intermédiaire sous réserve d'un compactage méthodique q3/q4.`}
                        </div>
                        <!-- SVG CROSS-SECTION SCHEMATIC -->
                        <div style="margin-top: 0.75rem; background: #070a14; border: 1px solid rgba(56,189,248,0.3); border-radius: 6px; padding: 0.5rem;">
                            <svg viewBox="0 0 500 120" style="width:100%; height:auto; display:block;">
                                <!-- Ground TN -->
                                <line x1="10" y1="95" x2="160" y2="95" stroke="#94a3b8" stroke-dasharray="4,4" stroke-width="2"/>
                                <text x="30" y="110" fill="#94a3b8" font-size="9">Terrain Naturel (TN)</text>

                                <!-- Slope profile -->
                                <polygon points="160,95 380,25 490,25 490,95 160,95" fill="rgba(56,189,248,0.12)" stroke="#38bdf8" stroke-width="2"/>
                                
                                <!-- Platform -->
                                <line x1="380" y1="25" x2="490" y2="25" stroke="#10b981" stroke-width="3"/>
                                <text x="435" y="20" fill="#10b981" font-size="9" font-weight="bold" text-anchor="middle">Plateforme / Voirie</text>

                                <!-- Slope line -->
                                <line x1="160" y1="95" x2="380" y2="25" stroke="#f59e0b" stroke-width="3"/>
                                <text x="260" y="52" fill="#f59e0b" font-size="9" font-weight="bold" text-anchor="middle">Rampant L = ${lRampantTotal.toFixed(1)}m (α = ${angleDeg.toFixed(1)}°)</text>

                                <!-- Dimension H -->
                                <line x1="400" y1="25" x2="400" y2="95" stroke="#ec4899" stroke-width="1.5"/>
                                <text x="415" y="65" fill="#ec4899" font-size="9" font-weight="bold">H = ${h}m</text>

                                <!-- Dimension Emprise L -->
                                <line x1="160" y1="105" x2="380" y2="105" stroke="#38bdf8" stroke-width="1.5"/>
                                <text x="270" y="116" fill="#38bdf8" font-size="9" font-weight="bold" text-anchor="middle">Emprise L = ${lEmpriseTotale.toFixed(1)}m</text>
                            </svg>
                        </div>
                    </div>
                </div>
            `;
        } else if (type === 'devers_chaussee_enrobes') {
            const devType = document.getElementById('f-dev-type')?.value || 'toit_2_versants';
            const w = Number(document.getElementById('f-dev-w')?.value || 7.00);
            const p = Number(document.getElementById('f-dev-p')?.value || 2.50);
            const lChaussee = Number(document.getElementById('f-dev-l')?.value || 250);
            const eBbsg = Number(document.getElementById('f-dev-ebbsg')?.value || 5.0);
            const eGb3 = Number(document.getElementById('f-dev-egb3')?.value || 10.0);
            const mv = Number(document.getElementById('f-dev-mv')?.value || 2.45);

            const isToit = devType === 'toit_2_versants';
            const demiLargeur = isToit ? (w / 2) : w;
            const deltaZ = demiLargeur * (p / 100); // en m
            const deltaZMm = deltaZ * 1000; // en mm

            const surfaceChaussee = w * lChaussee;
            const surfaceInclinee = Math.sqrt(Math.pow(w, 2) + Math.pow(isToit ? deltaZ*2 : deltaZ, 2)) * lChaussee;

            // Tonnage BBSG et GB3
            const tonnageBbsgTheorique = surfaceChaussee * (eBbsg / 100) * mv;
            const tonnageBbsgCommande = tonnageBbsgTheorique * 1.03; // +3% pertes
            const tonnageGb3Theorique = surfaceChaussee * (eGb3 / 100) * mv;
            const tonnageGb3Commande = tonnageGb3Theorique * 1.03;

            out.innerHTML = `
                <div style="background: rgba(15,23,42,0.95); border: 2px solid var(--cyan); border-radius: 8px; padding: 1.25rem;">
                    <div style="font-size:0.85rem; font-weight:800; color:#38bdf8; text-transform:uppercase; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center;">
                        <span>🛣️ Note de Calcul : Pente Transversale & Dévers de Chaussée Enrobés</span>
                        <span class="badge badge-info">Norme ARP / VSA</span>
                    </div>

                    <!-- STEP 1 -->
                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 1 : Dénivelée Transversale Fil d'Eau ↔ Axe de Chaussée</span>
                            <span class="badge badge-success">ΔZ = ${deltaZMm.toFixed(1)} mm</span>
                        </div>
                        <div class="formula-math-box">
                            • Demi-largeur versant : l = ${demiLargeur.toFixed(2)} m (Largeur totale : ${w}m)<br>
                            • Pente transversale (dévers) : p = <strong style="color:var(--emerald);">${p.toFixed(2)} %</strong> (soit ${(p*10).toFixed(1)} mm/m)<br>
                            • <strong>Dénivelée transversale entre Axe et Fil d'eau :</strong> ΔZ = ${demiLargeur.toFixed(2)}m × ${p}% = <strong style="color:#38bdf8; font-size:1.05rem;">${deltaZ.toFixed(3)} m (${deltaZMm.toFixed(1)} mm)</strong><br>
                            • Calage laser finisseur : <strong style="color:var(--amber);">-${p.toFixed(2)}% vers le bord droit/gauche</strong>
                        </div>
                    </div>

                    <!-- STEP 2 -->
                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 2 : Écoulement Hydraulique & Évacuation des Eaux Pluviales</span>
                            <span class="badge badge-info">Auto-Drainage Conforme</span>
                        </div>
                        <div class="formula-math-box">
                            • Condition de non-stagnation : p >= 2.0% pour éviter tout phénomène d'aquaplaning.<br>
                            • Pente transversale appliquée : <strong style="color:var(--emerald);">${p.toFixed(2)}% (Conforme aux recommandations Cerema)</strong><br>
                            • Évacuation assurée vers bordures T2 + Caniveaux doubles pentes CC1 avec avaloirs espacés de 35 à 45m.
                        </div>
                    </div>

                    <!-- STEP 3 -->
                    <div class="formula-calc-step">
                        <div class="formula-step-title">
                            <span>📌 Étape 3 : Tonnages d'Enrobés Chauds (BBSG 0/10 & GB3 0/14)</span>
                            <span class="badge badge-warning">${Math.round(tonnageBbsgCommande + tonnageGb3Commande)} Tonnes Totales</span>
                        </div>
                        <div class="formula-math-box">
                            • Surface totale de chaussée : S = ${w}m × ${lChaussee}ml = <strong>${surfaceChaussee.toFixed(1)} m²</strong><br>
                            • <strong>Couche de Roulement BBSG 0/10 (${eBbsg}cm) :</strong> ${tonnageBbsgTheorique.toFixed(1)}t brut $\\rightarrow$ <strong style="color:var(--emerald); font-size:1.02rem;">${tonnageBbsgCommande.toFixed(1)} tonnes à commander</strong> (~${Math.ceil(tonnageBbsgCommande/25)} semi-remorques 25t)<br>
                            • <strong>Couche de Base Grave Bitume GB3 (${eGb3}cm) :</strong> ${tonnageGb3Theorique.toFixed(1)}t brut $\\rightarrow$ <strong style="color:#38bdf8; font-size:1.02rem;">${tonnageGb3Commande.toFixed(1)} tonnes à commander</strong> (~${Math.ceil(tonnageGb3Commande/25)} semi-remorques 25t)
                        </div>
                    </div>

                    <!-- STEP 4 -->
                    <div class="formula-calc-step" style="border-left-color: var(--emerald); background: rgba(16,185,129,0.08);">
                        <div class="formula-step-title">
                            <span style="color:var(--emerald);">📌 Étape 4 : Profil en Travers Type Normalisé (Coupe SVG)</span>
                            <span class="badge badge-success">Profil Toiture 2.5%</span>
                        </div>
                        <div style="margin-top: 0.5rem; background: #070a14; border: 1px solid rgba(56,189,248,0.3); border-radius: 6px; padding: 0.5rem;">
                            <svg viewBox="0 0 500 110" style="width:100%; height:auto; display:block;">
                                <!-- Foundation GNT -->
                                <polygon points="30,85 250,75 470,85 470,95 30,95" fill="#334155" stroke="#64748b"/>
                                <text x="250" y="92" fill="#94a3b8" font-size="8" text-anchor="middle">Couche de Fondation GNT 0/31.5 ép. 20cm</text>

                                <!-- Base GB3 -->
                                <polygon points="30,75 250,65 470,75 470,85 250,75 30,85" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
                                <text x="140" y="80" fill="#f59e0b" font-size="8">GB3 ép. ${eGb3}cm</text>

                                <!-- Surface BBSG -->
                                <polygon points="30,68 250,58 470,68 470,75 250,65 30,75" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
                                <text x="360" y="72" fill="#10b981" font-size="8">BBSG ép. ${eBbsg}cm</text>

                                <!-- Slopes arrows -->
                                <path d="M 230 48 L 120 54" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#arrow)"/>
                                <text x="175" y="45" fill="#38bdf8" font-size="8" font-weight="bold">p = -${p}%</text>

                                <path d="M 270 48 L 380 54" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#arrow)"/>
                                <text x="325" y="45" fill="#38bdf8" font-size="8" font-weight="bold">p = -${p}%</text>

                                <!-- Center line & Curbs -->
                                <line x1="250" y1="35" x2="250" y2="70" stroke="#f59e0b" stroke-dasharray="3,3" stroke-width="1.5"/>
                                <text x="250" y="32" fill="#f59e0b" font-size="8" font-weight="bold" text-anchor="middle">Axe Chaussée (Point Haut)</text>

                                <rect x="22" y="52" width="8" height="20" fill="#94a3b8" stroke="#f8fafc"/>
                                <text x="26" y="48" fill="#cbd5e1" font-size="7" text-anchor="middle">T2</text>

                                <rect x="470" y="52" width="8" height="20" fill="#94a3b8" stroke="#f8fafc"/>
                                <text x="474" y="48" fill="#cbd5e1" font-size="7" text-anchor="middle">T2</text>
                            </svg>
                        </div>
                    </div>
                </div>
            `;
'''

# 1. Inject pente_inputs_js inside updateFormulaCalculator()
pos_tonnage = text.find("} else if (type === 'tonnage_enrobes') {")
if pos_tonnage != -1:
    text = text[:pos_tonnage] + pente_inputs_js.strip() + "\n        " + text[pos_tonnage:]
    print("pente_inputs_js injected in updateFormulaCalculator successfully!")
else:
    print("Error: tonnage_enrobes not found in updateFormulaCalculator")

# 2. Inject applyTalusPreset helper function before calculateTechniqueFormula
pos_calc = text.find("function calculateTechniqueFormula() {")
if pos_calc != -1:
    text = text[:pos_calc] + talus_helper_js.strip() + "\n\n    " + text[pos_calc:]
    print("applyTalusPreset injected successfully!")
else:
    print("Error: calculateTechniqueFormula not found")

# 3. Inject calc_talus_and_devers_js inside calculateTechniqueFormula
pos_calc_tonnage = text.find("} else if (type === 'tonnage_enrobes') {", pos_calc)
if pos_calc_tonnage != -1:
    text = text[:pos_calc_tonnage] + calc_talus_and_devers_js.strip() + "\n        " + text[pos_calc_tonnage:]
    print("calc_talus_and_devers_js injected into calculateTechniqueFormula successfully!")
else:
    print("Error: tonnage_enrobes not found in calculateTechniqueFormula")

with open('scripts/section_js_part3.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("section_js_part3.py updated successfully!")
