# Lancer Carré d'As maintenant — 3 étapes

## Windows

1. **Python** installé ([python.org](https://www.python.org/downloads/),
   cochez « Add Python to PATH » à l'installation).
2. **Double-cliquez** sur `Carrer d'As.bat` à la racine du dossier.
3. Le navigateur s'ouvre sur **http://127.0.0.1:8000** — c'est prêt.

## Linux / macOS

```bash
python3 main.py --serve --port 8000
# puis ouvrir http://127.0.0.1:8000
```

## Ce que vous obtenez immédiatement

| Fonction | Où |
|---|---|
| 💬 **Chat avec le patron** (SOL ☉) | Rail → Chat |
| ☉ **Système solaire** — voir les agents travailler | Rail → Solaire |
| ✺ **Constellation** — objets d'intérêt, planétaire, agentique | Rail → Heuristique |
| 🎨 **Changer le thème / le fond** | Dans le chat : « change le thème en océan », « crée un thème sunset, fond #2A1810 » — ou Système → Configuration |
| 📋 Réunion : récap, planning, budget, présentation | Rail → Réunion |
| ▦ Cartographie · ◍ Cognitorium · ◷ Prévision · ⌘ OSINT | Rail → Features |
| ⬢ Agents (22 spécialistes) | Rail → Features |

## Enrichir par le chat (le patron applique en direct)

```
« change le thème en jour »              → thème clair, immédiat
« mets un fond bleu profond »            → fond #0A1E38, immédiat
« crée un thème sunset, fond #2A1810, accent #FF8C42 »
                                         → thème perso créé + appliqué
« rédige le compte rendu de la réunion » → document .md produit
```

Le changement est **visible immédiatement** : dites « oui garde-le » pour
valider, ou demandez un ajustement.

## Les données

Tout est local, dans `.carredas-data/` (à côté du code). Rien ne sort
du poste. Sauvegarde : Système → « Sauvegarder les données ».

## Mise à jour

`python main.py --verif-maj` pour vérifier, `--maj` pour appliquer,
`--annuler-maj` pour revenir en arrière. Canal **git** par défaut.

## Le .exe (une seule fichier, one-click comme GobboNet)

À venir : `pyinstaller` pour produire un exécutable autonome
(Windows d'abord). En attendant, le `.bat` + Python suffisent.
