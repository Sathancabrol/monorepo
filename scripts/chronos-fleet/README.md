# Chronos Fleet — routeur IA local multi-appareils

Prototype technique v0.1, **100 % local, sans fournisseur payant**, préparé pour la tour Windows, le portable Windows, le Samsung A17 et le Redmi Note 13. Aucune connexion aux appareils de l'utilisateur n'a été réalisée dans cette livraison. **Le routage de la tour est activé dans la configuration proposée ; les trois autres nœuds sont déclarés mais désactivés, jusqu'aux vérifications réseau.**

## Ce que fait réellement le prototype

- Serveur HTTP **uniquement sur `127.0.0.1:18888`** : `GET /health`, `GET /v1/models`, `POST /v1/chat/completions` (y compris SSE streaming).
- Route `cronos-local` pour les modèles de niveau `agent` (tour, portable) ; route `cronos-light` pour les modèles légers (téléphones d'abord, puis PC en repli).
- Transmet un appel d'outil **uniquement** à un nœud marqué `supports_tools: true`. Une capacité déclarée doit d'abord être testée réellement.
- Réessaie sur un autre nœud après erreur réseau/429/5xx **avant** le début d'une réponse. Ne peut pas migrer un flux SSE déjà commencé ; cette limite est volontaire pour éviter un faux succès ou la duplication des actions.
- N'appelle aucune API cloud et ne crée ni tâche Kanban ni nouvelle branche Watchtower.
- Configuration JSON ; clés de serveur distant lues dans des variables d'environnement, jamais enregistrées dans Git.

## Installation minimale sur la tour Windows (PowerShell)

Exécuter depuis le dossier extrait :

```powershell
# 1. Voir l'état actuel sans changer Hermes, les modèles ou le Kanban
powershell -NoProfile -ExecutionPolicy Bypass -File .\diagnostic.ps1

# 2. Vérifier que le modèle local existant répond
ollama list
Invoke-RestMethod http://127.0.0.1:11434/api/tags

# 3. Lancer le routeur local
py -3 .\fleet_router.py --config .\fleet.json
```

Dans un **deuxième PowerShell** :

```powershell
Invoke-RestMethod http://127.0.0.1:18888/health
$body = @{model='cronos-local'; stream=$false; messages=@(@{role='user';content='Réponds OK'})} | ConvertTo-Json -Depth 6
Invoke-RestMethod http://127.0.0.1:18888/v1/chat/completions -Method POST -ContentType 'application/json' -Body $body
```

Le lancement du routeur **ne modifie aucune configuration Hermes**. Il reste actif tant que sa console est ouverte. Après vérification, créer éventuellement une tâche planifiée Windows *distincte* pour le relancer à l'ouverture de session.

## Raccordement à Hermes, après le test local

Sur la tour, ouvrir `hermes -p cronoslocal model` et choisir un **Custom endpoint** :

- URL : `http://127.0.0.1:18888/v1`
- Modèle : `cronos-local`
- Clé : vide (boucle locale 127.0.0.1)

Pour `cronos` (worker Kanban réel), le modèle principal peut rester un fournisseur gratuit que tu as effectivement testé. Dans `hermes -p cronos fallback`, ajouter la route locale **avec** `provider: custom`, `model: cronos-local`, `base_url: http://127.0.0.1:18888/v1`. Elle ne nécessite aucun abonnement et doit pouvoir répondre lorsque les quotas cloud sont épuisés. Vérifier par `hermes -p cronos fallback check --live`. Vérifier **aussi** `hermes -p cronoslocal fallback check --live` si une chaîne distincte existe.

Si tu préfères rendre Hermes entièrement indépendant du cloud, choisis `cronos-local` en **modèle principal** du profil `cronos` ; les autres modèles gratuits deviennent optionnels. Mais le Qwen3 4B actuel a des limites importantes pour les longues tâches autonomes de programmation : il faut valider sa capacité à manipuler les outils et le Kanban avant de lui confier les modifications.

Ne jamais copier/coller un fichier complet `config.yaml` par-dessus un profil existant. Sauvegarder, puis modifier uniquement les champs concernés. Les profils sont séparés (`default`, `cronos`, `cronoslocal`).

## Ajout du portable

Sur le portable, installer/démarrer Ollama **uniquement s'il n'est pas déjà présent**, puis charger et tester un modèle compatible avec les outils (ex. `qwen3:4b`, à ajuster selon les performances). Donner accès à son serveur **seulement sur le LAN privé ou via un réseau VPN fermé** ; Ollama en HTTP ne doit pas être exposé à Internet. Dans `fleet.json`, renseigner son adresse IP privée réelle, son modèle réellement installé, passer `private_network_confirmed` et `enabled` à `true` **après** test de `/v1/models` depuis la tour. Les adresses `192.168.1.50/51/52` sont des exemples, **pas des adresses détectées**.

Si le portable n'est pas allumé, le routeur passe au nœud suivant de sa catégorie ; il ne « transfère » pas la mémoire GPU d'une machine vers l'autre. Deux modèles 4B sur deux cartes graphiques différentes peuvent traiter des demandes indépendantes, mais **ne deviennent pas magiquement un modèle 8B plus performant**.

## Ajout Samsung / Redmi via Termux

La procédure ne réinstalle pas `llama.cpp` déjà présent :

```sh
# Sur chaque téléphone, à adapter avec le chemin GGUF et l'IP Wi-Fi réelle
bash termux-serve.sh /chemin/vers/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf 8084 192.168.1.X
```

Sur le Redmi utiliser un port distinct (8085 proposé). Le script crée une clé HTTP **locale et confidentielle** dans `~/.config/cronos-fleet/llama-key` si nécessaire. Copier cette clé dans la variable d'environnement `CRONOS_SAMSUNG_KEY` ou `CRONOS_REDMI_KEY` **sur la tour** (ne pas l'inscrire dans `fleet.json` ni Git). Choisir dans `fleet.json` le véritable identifiant de modèle retourné par `GET /v1/models` et activer les nœuds après vérification. Restreindre l'accès Wi-Fi aux appareils de confiance ; pour fonctionner hors du domicile, préférer un VPN privé, jamais un port public ouvert.

**Important :** un modèle Qwen 0,5B ne peut pas remplacer GPT-6.1 dans une tâche complexe Watchtower. Les téléphones sont exploités pour de très petites requêtes sans outils, pas comme workers développeurs Kanban par défaut. Un service Android peut être interrompu par l'économie de batterie ; régler les permissions d'alimentation localement et mesurer stabilité/température.

## Watchtower : reprise sans recréation

Après l'audit et lorsque `cronos-local` passe un vrai test de génération **et d'appel d'outil** :

```powershell
hermes kanban --board default show t_67b6eb5e --json
hermes kanban --board default runs t_67b6eb5e
hermes kanban --board default log t_67b6eb5e --tail 12000
hermes -p cronos fallback check --live
```

Si M a effectivement un modèle épinglé à GPT-6.1, le retirer **sans créer de tâche** :

```powershell
hermes kanban --board default set-model t_67b6eb5e none
```

Puis, **uniquement si** M est actuellement `blocked`, après vérification des commits/workspaces et de l'absence de worker actif :

```powershell
hermes kanban --board default unblock t_67b6eb5e
hermes kanban --board default dispatch --dry-run
```

Ne pas exécuter un `unblock` automatique quand la tâche est encore `running` ou si des effets de l'essai précédent restent ambigus. Ne pas déclarer le lot M fini avant la recette réelle, et laisser la dépendance vers R telle quelle.

## Contrats et limites

- Le routeur supporte **Chat Completions**, pas l'API OpenAI Responses ou les embeddings. Certains workflows Hermes peuvent donc nécessiter un autre backend.
- Les entrées `cronos-local` / `cronos-light` sont **des routes**, pas de nouveaux modèles. Le routeur remplace le nom par celui du modèle du nœud.
- Aucun service n'est installé, aucune clé exportée, aucune IP de téléphone découverte automatiquement.
- Les capacités de function-calling, l'exécution prolongée, les contextes longs et la sécurité réseau **doivent être testés sur les quatre appareils**.
- Pour éviter des coûts cachés, conserver uniquement des fournisseurs cloud dont la gratuité est vérifiée ; ce routeur lui-même ne les appelle jamais.

### Sources officielles

- Hermes — fallbacks : https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers
- Hermes — Ollama : https://hermes-agent.nousresearch.com/docs/guides/local-ollama-setup
- Hermes — Kanban : https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban
- Ollama — modèle Qwen3 : https://ollama.com/library/qwen3
- llama.cpp serveur : https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md

## Validation

```powershell
py -3 -m unittest -v test_fleet_router.py
py -3 -m py_compile fleet_router.py
```

Tests du dépôt : sélection des nœuds, exclusion du téléphone pour les outils, API OpenAI-compatible en mock, repli effectif après nœud inaccessible, refus explicite d’un appel d’outil sans modèle compatible. **Ne constituent pas** des tests matériels sur les appareils de l'utilisateur.