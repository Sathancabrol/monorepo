import json
from pathlib import Path

TARGET = Path("/home/user/monorepo/projects/btp-conduite-travaux/template.html")

with open(TARGET, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update tab-safety HTML
old_safety_block = """<div id="tab-safety" class="tab-panel">
        <div class="card">
            <div class="card-header">
                <span class="card-title">⚡ Sécurité des Travaux à Proximité des Réseaux Électriques & Gaz (AIPR)</span>
                <span class="card-badge" style="color:var(--rose);">Réglementation Anti-Endommagement</span>
            </div>
            <div class="grid-2">
                <div style="background:var(--bg-card-alt); padding:1rem; border-radius:8px; border:1px solid var(--border);">
                    <h4 style="font-size:0.85rem; font-weight:800; color:var(--amber); margin-bottom:0.6rem;">🟡 Réseaux Gaz (PEHD / Acier MPB 4 bars)</h4>
                    <ul style="font-size:0.75rem; color:var(--text-muted); line-height:1.7; list-style:inside;">
                        <li><b>Zone d'approche (< 50 cm) :</b> Interdiction formelle du godet à dents. Terrassement manuel ou aspiratrice obligatoire.</li>
                        <li><b>Incertitude Classe A :</b> ± 10 cm pour les réseaux rigides.</li>
                        <li><b>Procédure d'Urgence :</b> Fuite/odeur -> Stop moteurs, évacuation périmètre 100m, Appel Gaz Sécurité <b>0 800 47 33 33</b>.</li>
                    </ul>
                </div>
                <div style="background:var(--bg-card-alt); padding:1rem; border-radius:8px; border:1px solid var(--border);">
                    <h4 style="font-size:0.85rem; font-weight:800; color:var(--rose); margin-bottom:0.6rem;">🔴 Réseaux Électriques (HTA 20 kV / Lignes Aériennes)</h4>
                    <ul style="font-size:0.75rem; color:var(--text-muted); line-height:1.7; list-style:inside;">
                        <li><b>Distances Limites d'Approche (DLA) :</b> 3 mètres pour tension < 50 kV ; 5 mètres pour tension >= 50 kV.</li>
                        <li><b>Habilitations :</b> H0B0 obligatoire pour les personnes travaillant au voisinage.</li>
                        <li><b>Accrochage sous tension :</b> Rester dans la cabine de l'engin, ne jamais sauter au sol (tension de pas). Prévenir Enedis.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>"""

new_safety_block = """<div id="tab-safety" class="tab-panel">
        <!-- Safety Hub Header -->
        <div class="card" style="margin-bottom:1rem; border-left:4px solid var(--rose);">
            <div class="card-header" style="flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span class="card-title">🦺 Guide Opérationnel de Sécurité & Prévention BTP (AIPR & Normes OPBTP)</span>
                    <span class="card-badge" style="color:var(--rose); margin-left:0.5rem;">Zéro Accident Mortel</span>
                </div>
                <div style="display:flex; gap:0.4rem;">
                    <button class="btn-primary" style="font-size:0.72rem; padding:0.35rem 0.65rem; background:#dc2626; border-color:#ef4444;" onclick="alert('🚨 PROTOCOLE URGENCE CHANTIER DÉCLENCHÉ :\\n1. Stopper tous les engins immédiatement\\n2. Périmètre de sécurité 100m\\n3. Appel SAMU (15) ou Pompiers (18)\\n4. Informer le Conducteur de Travaux et CSPS.')">
                        🚨 Déclencher Procédure d'Urgence
                    </button>
                </div>
            </div>
            <p style="font-size:0.78rem; color:var(--text-muted); line-height:1.6; margin-top:0.3rem;">
                Ce guide rassemble l'ensemble des règles obligatoires et des recommandations OPPBTP / INRS applicables sur tous nos chantiers de Voirie, Réseaux Divers et Terrassement.
            </p>
        </div>

        <!-- Safety 6 Pillars Grid -->
        <div class="grid-3" style="gap:1rem; margin-bottom:1rem;">
            <!-- 1. Distances de Sécurité & AIPR -->
            <div class="card" style="border-top:3px solid var(--amber);">
                <div style="font-weight:800; font-size:0.88rem; color:var(--amber); margin-bottom:0.6rem; display:flex; align-items:center; gap:0.4rem;">
                    <span>⚡ 1. Distances de Sécurité DLA & AIPR</span>
                </div>
                <ul style="font-size:0.75rem; color:var(--text-muted); line-height:1.7; list-style:inside;">
                    <li><b>Lignes Aériennes &lt; 50 kV (HTA/BT) :</b> Distance Limite d'Approche (DLA) = <b>3,00 mètres</b>.</li>
                    <li><b>Lignes Aériennes &ge; 50 kV (HTB) :</b> DLA = <b>5,00 mètres</b> infranchissable.</li>
                    <li><b>Fuseaux d'Incertitude Cartographique :</b>
                        <br>&bull; <i>Classe A :</i> &plusmn; 40 cm (rigide &plusmn; 10 cm).
                        <br>&bull; <i>Classe B :</i> &plusmn; 1,50 m (investigations requises).
                        <br>&bull; <i>Classe C :</i> &gt; 1,50 m (tranchées de reconnaissance obligatoires).
                    </li>
                    <li><b>Approche &lt; 50 cm Réseau Gaz :</b> Terrassement mécanique à godet denté strictement interdit &rarr; Terrassement manuel ou aspiratrice.</li>
                </ul>
            </div>

            <!-- 2. Blindage Obligatoire des Tranchées -->
            <div class="card" style="border-top:3px solid var(--cyan);">
                <div style="font-weight:800; font-size:0.88rem; color:var(--cyan); margin-bottom:0.6rem; display:flex; align-items:center; gap:0.4rem;">
                    <span>🛡️ 2. Blindage Obligatoire des Fouilles</span>
                </div>
                <ul style="font-size:0.75rem; color:var(--text-muted); line-height:1.7; list-style:inside;">
                    <li><b>Règle R.4534-24 :</b> Blindage obligatoire pour toute tranchée de <b>profondeur &gt; 1,30 m</b> et de largeur &le; aux 2/3 de la profondeur.</li>
                    <li><b>Types de Blindage Homologués :</b>
                        <br>&bull; <i>Caissons coulissants acier :</i> prof. jusqu'à 4,50 m.
                        <br>&bull; <i>Blindage léger alu (Titan) :</i> réseaux urbains &lt; 2,50 m.
                        <br>&bull; <i>Talutage naturel :</i> pente &le; 1/1 (45°) si emprise suffisante.
                    </li>
                    <li><b>Interdiction d'Accès :</b> Ne jamais descendre au fond d'une fouille non blindée ou en cours de pose de caisson.</li>
                </ul>
            </div>

            <!-- 3. Pack EPI Obligatoire -->
            <div class="card" style="border-top:3px solid var(--emerald);">
                <div style="font-weight:800; font-size:0.88rem; color:var(--emerald); margin-bottom:0.6rem; display:flex; align-items:center; gap:0.4rem;">
                    <span>🦺 3. Pack EPI & Protections Individuelles</span>
                </div>
                <ul style="font-size:0.75rem; color:var(--text-muted); line-height:1.7; list-style:inside;">
                    <li><b>Casque de Chantier (NF EN 397) :</b> Port de la jugulaire obligatoire en bordure de tranchée et sous la flèche d'engin.</li>
                    <li><b>Haute Visibilité (EN ISO 20471) :</b> Gilet ou parka Classe 2 minimum, Classe 3 de nuit ou par temps de brouillard.</li>
                    <li><b>Chaussures de Sécurité (S3 SRC) :</b> Semelle anti-perforation acier/composite et embout 200 Joules.</li>
                    <li><b>Gants de Manutention (EN 388) :</b> Résistance à la coupure niveau D ou F pour pose de bordures et découpe PVC.</li>
                    <li><b>Protections Auditives & Oculaires :</b> Bouchons SNR 28dB lors du découpage de chaussée et lunettes EN 166.</li>
                </ul>
            </div>

            <!-- 4. Angles Morts & Coactivité Engins -->
            <div class="card" style="border-top:3px solid var(--rose);">
                <div style="font-weight:800; font-size:0.88rem; color:var(--rose); margin-bottom:0.6rem; display:flex; align-items:center; gap:0.4rem;">
                    <span>🚜 4. Angles Morts & Trafic Engins</span>
                </div>
                <ul style="font-size:0.75rem; color:var(--text-muted); line-height:1.7; list-style:inside;">
                    <li><b>Rayon de Rotation Pelle :</b> Périmètre d'exclusion de <b>10 mètres</b> autour de la tourelle des pelles &ge; 14T.</li>
                    <li><b>Zone de Recul Camions 8x4 :</b> Ne jamais stationner à l'arrière d'un camion benne en manœuvre. Guidage par le chef d'équipe obligatoire.</li>
                    <li><b>Contact Visuel Pilote :</b> Si vous ne voyez pas les yeux du conducteur dans son rétroviseur, il ne vous voit pas !</li>
                    <li><b>Bips de Recul & Caméras 360° :</b> Vérification quotidienne du fonctionnement des alarmes sonores et radars d'obstacles.</li>
                </ul>
            </div>

            <!-- 5. Risques Chimiques & Enrobés Chauds -->
            <div class="card" style="border-top:3px solid var(--purple);">
                <div style="font-weight:800; font-size:0.88rem; color:var(--purple); margin-bottom:0.6rem; display:flex; align-items:center; gap:0.4rem;">
                    <span>🧪 5. Enrobés Chauds & Risques Chimiques</span>
                </div>
                <ul style="font-size:0.75rem; color:var(--text-muted); line-height:1.7; list-style:inside;">
                    <li><b>Température d'Application (150°C - 170°C) :</b> Risque majeur de brûlures thermiques au troisième degré. Gants cuir manchettes longues obligatoires.</li>
                    <li><b>Émanations d'HAP & Bitume :</b> Se placer systématiquement au vent du finisseur. Masque à cartouche vapeurs A2P3 en cas d'espace confiné.</li>
                    <li><b>Produits de Collage & Émulsion :</b> Port de lunettes étanches lors du répandage à la lance. Rince-œil portatif disponible dans le camion atelier.</li>
                </ul>
            </div>

            <!-- 6. Procédures d'Urgence & Numéros Vitaux -->
            <div class="card" style="border-top:3px solid #dc2626;">
                <div style="font-weight:800; font-size:0.88rem; color:#ef4444; margin-bottom:0.6rem; display:flex; align-items:center; gap:0.4rem;">
                    <span>📞 6. Procédures d'Urgence & Contacts Vitaux</span>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; font-size:0.75rem;">
                    <div style="background:var(--bg); padding:0.5rem; border-radius:6px; border:1px solid var(--border);">
                        <b>🚑 SAMU :</b> <span style="color:#ef4444; font-weight:800;">15</span><br>
                        <b>🚒 Pompiers :</b> <span style="color:#ef4444; font-weight:800;">18</span><br>
                        <b>📱 Urgence UE :</b> <span style="color:#ef4444; font-weight:800;">112</span>
                    </div>
                    <div style="background:var(--bg); padding:0.5rem; border-radius:6px; border:1px solid var(--border);">
                        <b>🔥 Urgence Gaz :</b> <span style="color:var(--amber); font-weight:800;">0 800 47 33 33</span><br>
                        <b>⚡ Enedis Dépannage :</b> <span style="color:var(--cyan); font-weight:800;">09 72 67 50 34</span><br>
                        <b>💧 Urgence Eau :</b> <span style="color:var(--purple); font-weight:800;">04 67 12 34 56</span>
                    </div>
                </div>
                <p style="font-size:0.7rem; color:var(--text-muted); margin-top:0.4rem;">
                    <b>Protocole PAS :</b> Protéger (couper contact, baliser) &rarr; Alerter (préciser PK / adresse exacte) &rarr; Secourir (SST uniquement).
                </p>
            </div>
        </div>
    </div>"""

if old_safety_block in text:
    text = text.replace(old_safety_block, new_safety_block)
    print("Replaced tab-safety HTML!")
else:
    print("old_safety_block NOT found! Replacing by regex...")
    import re
    text = re.sub(r'<div id="tab-safety" class="tab-panel">[\s\S]*?</div>\s*</div>\s*</div>', new_safety_block, text, count=1)

with open(TARGET, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved update_safety_and_catalog.py successfully!")
