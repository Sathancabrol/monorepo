# OLYMPUS Studio — accès Samsung en prévisualisation privée

Cette procédure fonctionne avec la branche `feat/olympus-mobile-preview-20261113`, **pas** avec le ZIP v0.2.5 existant tant que la PR n'est pas intégrée.

## Pourquoi un proxy séparé ?

Le serveur Studio `server.mjs` refuse correctement tout hôte différent de `localhost:8787`.
Ne pas remplacer son écoute `127.0.0.1` par `0.0.0.0` : il possède des API de contrôle local (dont ComfyUI).

`scripts/mobile-preview.mjs` écoute aussi exclusivement sur `127.0.0.1` (port 8788).
Il expose seulement la page et les scripts/styles autorisés, et `GET /api/health`.
Il refuse les autres API, les flux OBS et **toutes** les requêtes POST : les moteurs du PC restent inaccessibles depuis le téléphone.

## Installation simplifiée : ZIP GitHub Actions

Après validation de la PR sur GitHub Actions, ouvrir la dernière exécution verte du workflow `OLYMPUS Studio — smoke tests` correspondant à cette branche, télécharger l'artefact `olympus-studio-preview`, décompresser entièrement le ZIP sur la tour Windows, puis double-cliquer **`LANCER_MOBILE.bat`**.
Ce lanceur ouvre **deux consoles** (Studio sur 8787 et passerelle sur 8788) ; elles doivent rester ouvertes.
Installer ensuite Tailscale sur PC et Android, et dans PowerShell lancer `tailscale serve --bg 8788` puis `tailscale serve status`. Ouvrir l'URL HTTPS privée indiquée sur Android.
Ceci ne rend pas encore Chronos pilotable depuis le téléphone.

## Étapes Windows — premier test (alternative Git)

1. Installer Node.js 20+ si nécessaire. Installer Tailscale sur Windows et Android. Connecter les deux machines au **même tailnet privé**.
2. Depuis PowerShell, récupérer la branche de cette PR :

   ```powershell
   git clone --branch feat/olympus-mobile-preview-20261113 --single-branch https://github.com/Sathancabrol/monorepo.git
   cd monorepo/projects/olympus-studio
   ```

   Si le dépôt est déjà local, utiliser un dossier/working tree séparé pour ne pas écraser de modifications en cours.
3. Dans un premier PowerShell : `npm start`. Vérifier `http://127.0.0.1:8787` sur la tour.
4. Dans un deuxième PowerShell : `node scripts/mobile-preview.mjs`.
5. Dans un troisième PowerShell : `tailscale serve --bg 8788`, puis `tailscale serve status`.
   Si demandé, autoriser HTTPS et MagicDNS pour le tailnet. **Ne jamais exécuter `tailscale funnel`** pour ce service.
6. Sur Android, Tailscale connecté, ouvrir l'URL privée `https://<nom-machine>.<tailnet>.ts.net/` affichée par la commande.

Les trois programmes doivent rester actifs : Studio, le proxy et Tailscale. Ce prototype n'installe pas de service Windows.

## État et limites

- **Prévisualisation uniquement** : navigation/interface et certaines opérations purement navigateur.
- **Non disponible depuis le mobile** : génération ComfyUI, streaming OBS, commandes Hermes/Chronos, modifications serveur.
- Les médias et projets stockés en IndexedDB sur Android sont **distincts** de ceux enregistrés dans le navigateur de la tour. Pas de synchronisation inter-appareils à ce stade.
- HTTPS via Tailscale est important pour l'accès caméra/micro depuis Android, mais la compatibilité A/V mobile doit encore être testée.
- La connexion future à Chronos nécessite un backend authentifié dédié, des permissions fines et un journal d'actions. **Ne pas exposer directement Hermes Dashboard ou ses API internes.**
- Un accès par `http://192.168.x.x:8787` n'est pas pris en charge volontairement.
- Stopper le partage : `tailscale serve --https=443 off` (vérifier `tailscale serve status`, la syntaxe dépend de la version installée).

## Vérification

Dans `projects/olympus-studio` : `npm test`. Le fichier `tests/mobile-preview.test.mjs` simule le serveur Studio et prouve que le proxy ne transmet pas d'actions POST ni de fichiers privés.


## Caméra d'un téléphone visible sur la tour et les autres téléphones (prototype)

La fonction « + Webcam » d'origine reste **strictement locale**. Pour partager volontairement le flux :

1. Ouvrir **la même version mise à jour d'OLYMPUS** sur les trois appareils : tour sur `http://127.0.0.1:8788`, téléphones sur l'adresse Tailscale HTTPS. Ne pas utiliser le port 8787 pour les fonctions collaboratives.
2. Sur le Samsung, descendre au panneau **CAMÉRAS · APPAREILS CONNECTÉS**. Renseigner éventuellement le nom et cliquer sur **Diffuser ma caméra**, puis autoriser Android.
3. Sur la tour et le Redmi, ouvrir le même panneau, patienter environ 2 secondes : une vignette distante actualisée apparaît. Cliquer sur **Ajouter à ma scène LIVE** pour dessiner la caméra dans le Canvas de cette session.
4. Sur le Samsung, **■ Arrêter la diffusion** stoppe la capture. Une déconnexion silencieuse supprime le flux côté serveur après 12 secondes sans nouvelle image.

Limites de cette étape : JPEG en mémoire RAM (max 640×360, environ 4 images/s), **sans audio**, sans persistance, **pas un transport WebRTC 30 images/s**. Les images voyagent via le serveur Windows déjà protégé par Tailscale (pas de service cloud obligatoire). La qualité et la latence réelles restent à tester sur Windows/Android. Le partage ne se fait jamais automatiquement par le bouton Webcam d'origine, et s'arrête lorsque le navigateur ou Android interrompt sa capture en arrière-plan.

Ce mode ne synchronise **pas** la composition, les fichiers IndexedDB ou les agents Chronos : chaque appareil garde sa scène. Le bouton « Ajouter à ma scène LIVE » agit seulement sur la scène du navigateur concerné. Ne pas activer Funnel et ne pas ouvrir de port sur la box.

**Actualiser les fichiers locaux** après publication de cette version : dans `%USERPROFILE%\olympus-mobile-test`, effectuer `git pull --ff-only` sur la branche `feat/olympus-mobile-preview-20261113` après avoir fermé les deux consoles de serveur, puis double-cliquer `projects\olympus-studio\LANCER_MOBILE.bat`. Les nouvelles routes ne seront pas présentes tant que les anciens processus Node.js tournent.
