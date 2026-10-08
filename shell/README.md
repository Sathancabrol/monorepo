# Carré d'As — squelette d'interface (template)

> **Carré d'As est le portail** : il ne refait pas les modules, il les fait **entrer**, les rend **atteignables** et **guidés**.
> Ce dossier est le **squelette UX/UI** : il fonctionne seul, sans dépendance, et sert de **template** à tout le reste.

## Ouvrir

```bash
# le plus simple : double-cliquer sur shell/index.html (aucun serveur requis)

# pour voir aussi les maquettes et les ateliers, servir tout le dépôt :
python3 shell/tools/serve.py            # → http://localhost:8000 (ouvre la page d'accès)
python3 shell/tools/serve.py 9000       # autre port

# ou, au minimum, servir juste le squelette :
python3 -m http.server 8000 --directory shell
```

Tout marche **hors ligne**, en `file://` : le registre est inliné (`assets/registry.js`) et les sons sont **synthétisés** (aucun fichier à télécharger).

## Ce qu'il contient

| Fichier | Rôle |
|---|---|
| `index.html` | **Le squelette** : barre haute, rail, zone de travail, onglets de module, barre d'état, panneau assistant, palette `Ctrl+K`. Contient les **points de montage** commentés (`#slot-<module>`) |
| `assets/tokens.css` | **Le design system** : `Void` (fonds), `Plasticity` (ce qui se construit, cyan `#00E5CC`), `Transfer` (ce qui circule, violet `#9B59B6`), typographie Inter/JetBrains Mono, rythme, ombres, densités, contraste, mouvement réduit. **Hérité du prototype d'origine** (`projects/proto-cognitorium/raw/noeud neurono.html`) |
| `assets/shell.css` | La structure : portail, portes, cartes de module, listes de fonctionnalités, onglets, pastilles d'état, palette, assistant, alerte, impression |
| `assets/registry.js` | **Le registre inliné** (données) : modules, portes, fonctionnalités, sources. Généré — ne pas éditer à la main |
| `assets/shell.js` | Navigation, rendu des vues, palette de commandes, filtres, réglages, raccourcis |
| `assets/assistant.js` | **L'assistant** : moteur de règles (hors ligne, sans clé), parole, écoute, orbe, et branchement **optionnel** d'un modèle local |
| `assets/sounds.js` | **Sons d'interface** synthétisés (Web Audio) + chargement optionnel d'un pack de fichiers |
| `data/modules.json` | Le même registre, en JSON (pour les outils, les tests, le générateur d'installeur) |
| `tools/gen-registry.py` | **La source de vérité** du registre. Modifier ici, puis regénérer |
| `tools/check-sources.py` | Le **contrôle de traçabilité** : vérifie que chaque fonctionnalité est adossée à un fichier réel du dépôt (aujourd'hui : **104/104**) |
| `tools/serve.py` | Servir tout le dépôt en local (`python3 shell/tools/serve.py`) : `/` renvoie vers la page d'accès — squelette, maquettes, ateliers. Bibliothèque standard uniquement |

## Les huit portes

`Accueil · Projets · Documents · Carte · Agents · Explorer · Assistant · Système`

Raccourcis : `Alt+1…8` pour les portes, `Ctrl+K` pour la palette, `/` pour filtrer, `?` pour la recherche, `Échap` pour fermer.

## Brancher un module (le contrat)

1. **Déclarer** ses fonctionnalités dans `tools/gen-registry.py`, puis :
   ```bash
   python3 shell/tools/gen-registry.py
   ```
2. **Monter** son code dans la zone de travail : il expose un point de montage
   ```html
   <section id="slot-btp" data-module="btp"></section>
   ```
   Le shell affiche aujourd'hui un **emplacement réservé** (slot) qui rappelle le contrat :
   `module.json`, identifiant, point de montage, statut, palier, **source dans le dépôt**.
3. **Respecter** le contrat de module : `docs/carre-das/01-CONTRAT-MODULE.md`
   (permissions « rien par défaut », activation à chaud, défaillance isolée, événements, `owns/reads`).

Rien d'autre à modifier : le rail, la palette, les filtres, l'assistant et la barre d'état se mettent à jour **tout seuls** à partir du registre.

## L'assistant (guidage vocal et visuel)

- **Toujours disponible, sans clé, sans réseau** : moteur de règles sur le registre.
- Il **ouvre**, **cherche**, **explique**, **fait le point**, et **se tait** sur demande :
  « ouvre le BTP » · « cherche métrés » · « explique la décroissance » · « où en est le projet » · « silence ».
- **Voix** : sortie par la synthèse du système ; entrée par la reconnaissance vocale du navigateur (Chrome/Edge). Ailleurs, **l'écrit fonctionne toujours**.
- **Modèle local (optionnel)** : renseigner l'adresse d'Ollama (`http://127.0.0.1:11434`) dans **Système**. Si aucun modèle ne répond, l'assistant **le dit** et reste en mode règles.
- **Il ne fait rien sans trace** : chaque action est annoncée dans la conversation et répercutée dans la barre d'état.

## Les sons (et « le morceau dans un repo »)

De base : **synthèse locale** (Web Audio) — `boot`, `open`, `close`, `tick`, `confirm`, `cancel`, `error`, `ping`, `sweep`. Aucun fichier, aucune licence à gérer, fonctionne hors ligne.

Pour utiliser un **vrai pack de sons libres**, l'écosystème en fournit d'excellents, et c'est là qu'on prend « un morceau dans un repo » :

| Source | Licence | Ce qu'on prend |
|---|---|---|
| **uisfx** (`romainsimon/uisfx`) | code **MIT**, audio **CC0**, 936 sons, 78 gestes, 12 styles — dont **« scifi »** : « clean holographic pings and restrained digital shimmer », taillé pour une interface d'IA | le pack `scifi` |
| **soundcn** | **CC0** (700+ sons, installable par la CLI shadcn) | effets ponctuels |
| **UI SFX / Octave / sound_library** | CC0 / libres | alternatives |

Mode d'emploi :
```bash
mkdir -p shell/assets/sfx/scifi
# y déposer open.mp3, close.mp3, tick.mp3, confirm.mp3, cancel.mp3, error.mp3, ping.mp3, sweep.mp3, boot.mp3
```
```js
// dans la console, une seule fois :
CarreSounds.loadPack("scifi");     // mémorisé pour les prochaines visites
```
Le chargement est **facultatif et non bloquant** : si les fichiers ne sont pas là, la synthèse reprend la main.

## Accessibilité (règle non négociable)

- Navigation **complète au clavier**, `:focus-visible` visible partout ;
- **`aria-current`, `aria-pressed`, `role="tablist"`, `aria-live`** sur les zones qui changent ;
- **Densité** confort/dense, **contraste élevé**, **mouvement réduit** (respect de `prefers-reduced-motion`) ;
- Les graphiques et l'arbre auront **toujours un équivalent textuel** (vue liste) — c'est une règle du projet (UX-10, RGAA) ;
- L'audio n'est **jamais** le seul canal : tout son a un équivalent visuel.

## Ce qui n'est pas encore là (honnêtement)

- Les **modules eux-mêmes** : le squelette les appelle, il ne les contient pas encore ;
- La **persistance** (profil, projets, documents) : viendra du Core ;
- L'**installeur Windows** : étape P4 du plan ;
- Le **mode présentation** plein écran : présent dans la palette, à habiller.

Voir `docs/carre-das/07-INVENTAIRE-FONCTIONNALITES.md` pour la liste complète des fonctionnalités et leur origine, et `docs/carre-das/05-REPONSES-AUX-QUESTIONS.md` §2 pour l'ordre de construction.
