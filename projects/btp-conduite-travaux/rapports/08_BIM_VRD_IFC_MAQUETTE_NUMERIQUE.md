# RAPPORT THÉMATIQUE 08 : BIM INFRASTRUCTURE, FORMATS IFC 4.3, MODIFICATION DE MAQUETTE & JUMEAU NUMÉRIQUE VRD

> **Domaine :** Building Information Modeling (BIM) appliqué aux Travaux Publics, VRD et Génie Civil  
> **Standards & Normes :** OpenBIM buildingSMART (IFC 4.3 ISO 19650 / ISO 16739), LandXML 1.2, BCF (BIM Collaboration Format), Décret Anti-Endommagement & NF P 98-332  
> **Dimensions BIM :** 3D (Géométrie & Réseaux), 4D (Phasage & Planning), 5D (Quantités & Coûts DS/PV), 6D (Bilan Carbone & FDES), 7D (DOE Numérique & Exploitation SI 022)  
> **Date de référence :** 2026  

---

## 1. Fondements du BIM dans les Travaux Publics et VRD (OpenBIM IFC 4.3)

Contrairement au BIM bâtiment traditionnel (centré sur les murs, dalles et portes sous IFC 2x3 ou IFC 4), le **BIM Infrastructure / VRD** s'appuie sur la norme **IFC 4.3 (ISO 16739-1:2024)** qui introduit nativement les entités linéaires et de réseaux :

```
+----------------------------------------------------------------------------------------------------+
|                             HIÉRARCHIE SPATIALE & OBJETS BIM VRD (IFC 4.3)                         |
+====================================================================================================+
| IfcProject ("Aménagement ZAC Barbazan - VRD & Assainissement")                                    |
|   └── IfcSite (Géoréférencement RGF93 / CC43 / NGF-IGN69, Emprise foncière)                        |
|        ├── IfcRoad ("Voie Principale & Voirie Lourde")                                             |
|        │    ├── IfcCourse (Couche de roulement BB 0/10 - 5 cm)                                     |
|        │    ├── IfcCourse (Grave Bitume GB 0/14 - 10 cm)                                           |
|        │    ├── IfcCourse (Grave Non Traitée GNT 0/31.5 - 25 cm)                                  |
|        │    └── IfcKerb (Bordures T2 béton préfabriqué NF EN 1340)                                 |
|        └── IfcDistributionSystem ("Réseau Assainissement EP & EU")                                 |
|             ├── IfcPipeSegment (Tronçon PVC CR8 DN200 / Fonte ductile)                             |
|             │    └── Pset_PipeSegmentPHistory (Pente: 1.2%, Rugosité Ks: 90, Alti FE: 142.35 m)     |
|             ├── IfcDistributionChamberElement (Regard de visite béton DN1000 avec tampon fonte C250)|
|             └── IfcFlowFitting (Coudes, tés, branchements particuliers à 45°)                     |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Les 7 Dimensions du BIM et leur Implémentation Opérationnelle

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   LES 7 DIMENSIONS DU BIM APPLIQUÉES AU VRD                            │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
  │
  ├── 🔹 3D (Spatial & Géométrie) : Modélisation volumique MNT, tranchées de réseaux, canalisations, 
  │     chambres de tirage, profils en long/travers. Détection de clashs (NF P 98-332).
  │
  ├── 🔹 4D (Temps & Phasage) : Association des objets 3D au planning GANTT (WBS). Simulation 
  │     de la cinématique des terrassements et de la pose des réseaux avec délais intempéries.
  │
  ├── 🔹 5D (Coûts & Déboursés) : Extraction automatique des métrés (QTO - Quantity Take-Off) 
  │     vers le Déboursé Sec ($DS$) et Prix de Vente ($PV_{HT} = DS \times K$).
  │
  ├── 🔹 6D (Développement Durable) : Calcul de l'empreinte carbone ($kg\text{ CO}_2\text{e}$) via les 
  │     fiches FDES (Base INIES) pour chaque m³ de béton et tonne d'enrobé.
  │
  └── 🔹 7D (Maintenance & DOE Numérique) : Intégration dans le standard SI 022 pour la GMAO de la 
        collectivité (durée de vie, périodicité de curage, plans de récolement classe A).
```

---

## 3. Détection de Clashs & Règles de Voisinage Souterrain (NF P 98-332)

L'un des apports majeurs de la maquette BIM VRD est la **détection automatique des conflits géométriques (Clash Detection)** entre les différents concessionnaires de réseaux :

$$\text{Distance Souterraine Minimale (NF P 98-332)} : \Delta z \ge 0{,}20\text{ m (croisement)} \quad \text{et} \quad \Delta x \ge 0{,}50\text{ m (parallélisme)}$$

| Réseau Croisé | Réseau Croisant | Distance Verticale Mini | Protection Réglementaire |
| :--- | :--- | :--- | :--- |
| **Eaux Usées (Gravitaire)** | Adduction Eau Potable (AEP) | $\ge 0{,}20\text{ m}$ (AEP toujours au-dessus) | Fourreau acier si AEP sous EU |
| **Gaz Haute/Basse Pression** | Électricité BT / HTA | $\ge 0{,}20\text{ m}$ | Grillage avertisseur jaune / rouge |
| **Fibre Optique / Télécom** | Eaux Pluviales (Béton) | $\ge 0{,}20\text{ m}$ | Grillage avertisseur vert |

---

## 4. Algorithme de Modification & Génération de Fichier IFC 4.3

Lorsque l'IA ou le conducteur de travaux modifie un paramètre dans la maquette (diamètre $DN$, cote fil d'eau $Z$, pente $I$), la chaîne algorithmique s'exécute comme suit :

1. **Recalcul Hydraulique Manning-Strickler :**
   $$Q_{max} = K_s \cdot \frac{\pi \cdot D^2}{4} \cdot \left(\frac{D}{4}\right)^{2/3} \cdot I^{1/2}$$
2. **Vérification de la vitesse d'auto-curage :**
   $$0{,}60\text{ m/s} \le V = \frac{Q}{S} \le 3{,}00\text{ m/s}$$
3. **Mise à jour du Déboursé Sec 5D :**
   $$\Delta DS = \Delta L_{tranchée} \times (C_{terrassement} + C_{lit\_pose} + C_{tuyau}(DN) + C_{remblai})$$
4. **Exportation ISO 10303-21 STEP (Fichier `.ifc`) :**
   Génération séquentielle des lignes d'entités IFC avec géométrie B-Rep ou Extrusion solide :
   ```step
   ISO-10303-21;
   HEADER;
   FILE_DESCRIPTION(('ViewDefinition [CoordinationView_V4.3]'),'2;1');
   FILE_NAME('CHANTIER_VRD_AUTONOME.ifc','2026-09-09T10:00:00',('Ingénieur Travaux'),('BTP Autonomous Command'),'IFC4X3_ADD2','BTP-Engine-v2.6','');
   FILE_SCHEMA(('IFC4X3_ADD2'));
   ENDSEC;
   DATA;
   #1=IFCPROJECT('1tw$8e4RH2fB7V0x1L2Z_a',#2,'CHANTIER_BARBAZAN_VRD',$,$,$,$,(#3),#4);
   #10=IFCROAD('2V8jF9bK5D$w8X2M9Q3L_p',#2,'VOIRIE_PRINCIPALE',$,$,#11,$,$,.USERDEFINED.);
   #20=IFCPIPESEGMENT('3X8kG0cL6E$x9Y3N0R4M_q',#2,'TRONCON_EU_DN200',$,$,#21,#22,'PVC_CR8');
   #30=IFCDISTRIBUTIONCHAMBERELEMENT('4Y9lH1dM7F$y0Z4O1S5N_r',#2,'REGARD_VISITE_R1',$,$,#31,#32,.MANHOLE.);
   ENDSEC;
   END-ISO-10303-21;
   ```

---

## 5. Connexion avec le Guidage GPS d'Engins (LandXML & Topcon/Leica 3D)

La maquette BIM éditée s'exporte également au format **LandXML** pour transmission immédiate aux pelles hydrauliques et niveleuses équipées de guidage GNSS 3D :
- Précision d'excavation : $\pm 1{,}5\text{ cm}$
- Réduction du sur-terrassement : $-18\%$ de volume de déblai évacué en décharge
- Zéro piquetage intermédiaire nécessaire sur le chantier.
