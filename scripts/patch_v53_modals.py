#!/usr/bin/env python3
"""
Patch v53: Add new modals to scripts/section_modals.py
- modal-add-livraison
- modal-add-intemperie
- modal-safety-quarter-hour
"""

with open("scripts/section_modals.py", "r", encoding="utf-8") as f:
    text = f.read()

new_modals = """
    <!-- ========================================== -->
    <!-- MODAL: AJOUTER BON DE LIVRAISON / PESEE    -->
    <!-- ========================================== -->
    <div id="modal-add-livraison" class="modal-overlay" style="display: none;" onclick="if(event.target===this) closeAddLivraisonModal()">
        <div class="modal-box" style="max-width: 600px;">
            <div class="modal-header">
                <span class="modal-title">🚛 Saisie de Bon de Livraison & Pesée Centrale</span>
                <button class="modal-close-btn" onclick="closeAddLivraisonModal()">&times;</button>
            </div>
            <div class="modal-body">
                <form id="form-add-livraison" onsubmit="saveNewLivraison(event)">
                    <div class="grid-2-col" style="gap: 0.5rem; margin-bottom: 0.5rem;">
                        <div class="input-group">
                            <label class="input-label">N° de Bon de Livraison (BL)</label>
                            <input type="text" class="input-field" id="new-bl-num" required placeholder="Ex: BL-2026-8842">
                        </div>
                        <div class="input-group">
                            <label class="input-label">Date & Heure</label>
                            <input type="datetime-local" class="input-field" id="new-bl-date" required>
                        </div>
                    </div>
                    <div class="grid-2-col" style="gap: 0.5rem; margin-bottom: 0.5rem;">
                        <div class="input-group">
                            <label class="input-label">Fournisseur / Centrale</label>
                            <select class="select-field" id="new-bl-fournisseur">
                                <option value="Colas Midi-Pyrénées (Centrale Saint-Thibéry)">Colas Centrale Saint-Thibéry</option>
                                <option value="Eurovia Occitanie (Centrale Pinet)">Eurovia Centrale Pinet</option>
                                <option value="Carrières GSM Bassin de Thau">Carrières GSM Bassin de Thau</option>
                                <option value="Lafarge Holcim Bétons Sète">Lafarge Holcim Bétons Sète</option>
                                <option value="CEMEX Bétons Agde">CEMEX Bétons Agde</option>
                            </select>
                        </div>
                        <div class="input-group">
                            <label class="input-label">Matériau / Formule</label>
                            <select class="select-field" id="new-bl-materiau">
                                <option value="BBSG 0/10 Classique (Enrobé)">BBSG 0/10 Classique (Enrobé)</option>
                                <option value="BBME 0/10 Module Élevé">BBME 0/10 Module Élevé</option>
                                <option value="GNT 0/31.5 Non Traitée">GNT 0/31.5 Non Traitée</option>
                                <option value="GNT 0/20 Réglage Fin">GNT 0/20 Réglage Fin</option>
                                <option value="Sable 0/4 Sablon Tranchée">Sable 0/4 Sablon Tranchée</option>
                                <option value="Béton C25/30 XF1 Bordures">Béton C25/30 XF1 Bordures</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid-3-col" style="gap: 0.5rem; margin-bottom: 0.5rem;">
                        <div class="input-group">
                            <label class="input-label">Immatriculation Camion</label>
                            <input type="text" class="input-field" id="new-bl-camion" placeholder="Ex: GA-420-TX">
                        </div>
                        <div class="input-group">
                            <label class="input-label">Quantité Pesée (t ou m³)</label>
                            <input type="number" step="0.01" class="input-field" id="new-bl-qte" required placeholder="Ex: 28.40">
                        </div>
                        <div class="input-group">
                            <label class="input-label">Température (°C)</label>
                            <input type="number" step="1" class="input-field" id="new-bl-temp" value="165" placeholder="Ex: 165">
                        </div>
                    </div>
                    <div class="input-group" style="margin-bottom: 1rem;">
                        <label class="input-label">Localisation de Pose sur Chantier</label>
                        <input type="text" class="input-field" id="new-bl-loc" placeholder="Ex: Chaussée Principale Axe 1 - PK 0+150 à PK 0+250">
                    </div>
                    <div style="display: flex; justify-content: flex-end; gap: 0.5rem;">
                        <button type="button" class="btn btn-secondary" onclick="closeAddLivraisonModal()">Annuler</button>
                        <button type="submit" class="btn btn-primary">💾 Enregistrer Bon de Pesée</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL: AJOUTER JOURNEE D'INTEMPERIE        -->
    <!-- ========================================== -->
    <div id="modal-add-intemperie" class="modal-overlay" style="display: none;" onclick="if(event.target===this) closeAddIntemperieModal()">
        <div class="modal-box" style="max-width: 600px;">
            <div class="modal-header">
                <span class="modal-title">🌧️ Déclaration d'Arrêt pour Intempérie (CCAG Art. 18.2.3)</span>
                <button class="modal-close-btn" onclick="closeAddIntemperieModal()">&times;</button>
            </div>
            <div class="modal-body">
                <form id="form-add-intemperie" onsubmit="saveNewIntemperie(event)">
                    <div class="grid-2-col" style="gap: 0.5rem; margin-bottom: 0.5rem;">
                        <div class="input-group">
                            <label class="input-label">Date du Constat</label>
                            <input type="date" class="input-field" id="new-intemp-date" required>
                        </div>
                        <div class="input-group">
                            <label class="input-label">Phénomène Météorologique</label>
                            <select class="select-field" id="new-intemp-type">
                                <option value="Pluie Diluvienne (> 10 mm/j)">Pluie Diluvienne (> 10 mm/j)</option>
                                <option value="Vent Violent / Rafales (> 60 km/h)">Vent Violent / Rafales (> 60 km/h)</option>
                                <option value="Gel Sévère (< -2°C)">Gel Sévère (< -2°C)</option>
                                <option value="Canicule Alerte Orange/Rouge">Canicule Alerte Orange/Rouge</option>
                                <option value="Inondation / Sol Impraticable">Inondation / Sol Impraticable</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid-2-col" style="gap: 0.5rem; margin-bottom: 0.5rem;">
                        <div class="input-group">
                            <label class="input-label">Valeur Mesurée In Situ</label>
                            <input type="text" class="input-field" id="new-intemp-valeur" required placeholder="Ex: 24.5 mm / 24h (Pluvio)">
                        </div>
                        <div class="input-group">
                            <label class="input-label">Chômage CNETP Déclaré</label>
                            <select class="select-field" id="new-intemp-cnetp">
                                <option value="Oui - Indemnisé 100%">Oui - Indemnisé 100%</option>
                                <option value="Non - Travaux de Repli en Atelier">Non - Travaux de Repli en Atelier</option>
                            </select>
                        </div>
                    </div>
                    <div class="input-group" style="margin-bottom: 1rem;">
                        <label class="input-label">Tâches Critiques Directement Bloquées</label>
                        <input type="text" class="input-field" id="new-intemp-taches" required placeholder="Ex: Pose d'enrobés à chaud BBSG 0/10 et compactage GNT">
                    </div>
                    <div style="display: flex; justify-content: flex-end; gap: 0.5rem;">
                        <button type="button" class="btn btn-secondary" onclick="closeAddIntemperieModal()">Annuler</button>
                        <button type="submit" class="btn btn-primary">💾 Valider et Enregistrer</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL: FICHES 1/4H SECURITE OPPBTP         -->
    <!-- ========================================== -->
    <div id="modal-safety-quarter-hour" class="modal-overlay" style="display: none;" onclick="if(event.target===this) closeSafetyQuarterHourModal()">
        <div class="modal-box" style="max-width: 850px; max-height: 90vh; display: flex; flex-direction: column;">
            <div class="modal-header">
                <span class="modal-title">🦺 Module Fiches 1/4 d'Heure Sécurité OPPBTP & Accueil Sécurité</span>
                <button class="modal-close-btn" onclick="closeSafetyQuarterHourModal()">&times;</button>
            </div>
            <div class="modal-body" style="overflow-y: auto; flex: 1;">
                <div style="display: flex; gap: 0.5rem; margin-bottom: 1rem; align-items: center; flex-wrap: wrap;">
                    <span style="font-weight: 700; color: #38bdf8; font-size: 0.85rem;">Thématique 1/4h Sécurité :</span>
                    <select class="select-field" id="safety-theme-select" style="flex: 1; min-width: 280px;" onchange="loadSafetyBriefingContent()">
                        <option value="aipr_gaz_elec">1. Travaux à proximité des réseaux enterrés (AIPR / Gaz / HTA)</option>
                        <option value="blindage_tranchee">2. Risque d'éboulement & Blindage des tranchées (R.4534)</option>
                        <option value="engins_pietons">3. Coactivité et heurts Engins / Piétons sur chantier</option>
                        <option value="elinguage_levage">4. Élingage, Manutention et Levage de blindages/tuyaux</option>
                        <option value="enrobes_brulures">5. Risques chimiques & Brûlures lors de la pose d'enrobés à chaud</option>
                        <option value="bruit_vibrations">6. Prévention des risques liés au Bruit et aux Vibrations engins</option>
                        <option value="canicule_froid">7. Travail par fortes chaleurs (Canicule) et intempéries</option>
                        <option value="accueil_nouveau">8. Fiche d'Accueil Sécurité Nouvel Arrivant & Intérimaire</option>
                    </select>
                    <button class="btn btn-primary" onclick="printSafetyBriefing()">🖨️ Imprimer Fiche Émargée</button>
                </div>

                <div id="safety-briefing-content" style="background: rgba(15,23,42,0.8); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                    <!-- Injected dynamically -->
                </div>

                <div style="background: #020617; border: 1px solid var(--border); border-radius: 8px; padding: 0.75rem;">
                    <div style="font-weight: 700; color: #38bdf8; font-size: 0.85rem; margin-bottom: 0.5rem;">
                        ✍️ Émargement Numérique des Participants à la Session Sécurité
                    </div>
                    <div id="safety-attendees-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 0.4rem; max-height: 140px; overflow-y: auto;">
                        <!-- Injected dynamically -->
                    </div>
                </div>
            </div>
        </div>
    </div>
"""

text += new_modals

with open("scripts/section_modals.py", "w", encoding="utf-8") as f:
    f.write(text)

print("scripts/section_modals.py successfully updated with v53 modals!")
