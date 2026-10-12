# ROUTAGE — la règle manuelle (une seule, à connaître par cœur)

| Type de requête | Où elle part | Coût | Ce qui sort de la machine |
|---|---|---|---|
| **Sensible** — documents métier TP, dossier de marché, données perso, `prive\` | **Profil `prive`** → Ollama local (`127.0.0.1:11434`) | 0 € | rien |
| **Courante** — résumé, classement, reformulation, extraction de champs, question simple | **Profil par défaut** → OmniRoute (`127.0.0.1:20128`) → palier gratuit | 0 € | le contenu de la requête, chez le fournisseur gratuit d'OmniRoute |
| **Difficile** — spécification, conception, bug qui résiste 3 fois | **Quota payant** (Codex/ChatGPT) — *choix manuel* `/model` dans la session | quota, à réserver | oui, comme aujourd'hui |

## Les 4 règles non négociables

1. **Aucun document sensible sur un palier gratuit.** Un palier gratuit se paie en données : plusieurs
   fournisseurs entraînent sur les prompts. La route locale existe pour ça (étape 3 et 5).
2. **Aucun fournisseur marqué `tos: avoid`** (OmniRoute les exclut de `auto`, et il faut lire pourquoi).
   Même logique que la règle n°3 de `projects/watchtower/AGENTS.md` : on lit le fichier LICENSE/les CGU,
   pas le badge d'un README.
3. **`.env` en 600, jamais commité, jamais dans un prompt.** Les clés se saisissent avec
   `hermes config set NOM_EN_MAJUSCULES valeur` (écrit dans `~/.hermes/.env`).
4. **Aucun port en `0.0.0.0`.** OmniRoute et Ollama restent sur `127.0.0.1` ; pour y accéder depuis un
   autre appareil, on passe par un tunnel, pas par un bind public.

## Hygiène de requête (le vrai poste d'économie)

| Geste | Effet |
|---|---|
| Une tâche = une session, résultat écrit dans le dépôt | rien ne dépend de la fenêtre de 5 h |
| Coller un **extrait** ciblé, pas un fichier entier | divise l'entrée par 5 à 50 |
| Demander un **diff** plutôt qu'un fichier réécrit | sortie plus petite, relecture plus rapide |
| Fixer une longueur de réponse maximale | supprime le remplissage |
| `/compress` à chaque jalon | évite que le contexte relise tout à chaque tour |
| `hermes tools` : désactiver les outils non utilisés | allège **chaque** requête (décisif en local) |
| Décider le modèle **au début** de la session | évite le rechargement plein tarif du cache de prompt |
| `hermes insights --days 7` une fois par semaine | voit ce qui consomme réellement |

## Vérifier où une requête est réellement partie

| Outil | Ce qu'il montre |
|---|---|
| `hermes status` / `hermes config get model.provider` | la route configurée |
| En-tête de réponse OmniRoute `X-OmniRoute-Decision` | stratégie + fournisseur qui ont servi la requête |
| `hermes usage --provider openai-codex --json` | `used_percent` + `resets_at` des fenêtres Session / Weekly |
| `verifier-hermes.ps1 -Quota -Log` | la même chose journalisée dans `quota-log.csv` |
| `/usage` dans une session | le même bloc, sans quitter la conversation |
| `hermes logs` | ce qui a été appelé, et les bascules vers le fallback |

## Boucle de calibration du quota (à tenir 2–3 sessions)

```powershell
.\docs\PARAMETRAGE-HERMES\verifier-hermes.ps1 -Quota -Log     # avant la session
# … une tâche, un résultat écrit dans le dépôt, /compress …
.\docs\PARAMETRAGE-HERMES\verifier-hermes.ps1 -Quota -Log     # après
```

`quota-log.csv` te donne alors le **coût réel d'une spécification** en points de quota hebdomadaire.
C'est ce chiffre qui remplace toutes les estimations (y compris les miennes) dans la répartition
35–40 % specs / 15–20 % bugs / 15 % tampon.
