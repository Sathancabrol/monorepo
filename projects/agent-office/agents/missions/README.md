# 📮 Registre des missions agents

Une mission = un fichier `M-NNN-<slug>.md` exécuté par UN agent (fiche dans `projects/agent-office/agents/`).
Statuts : `brouillon` → `en_cours` → `gate` → `terminé` (ou `refusé`).

## Format obligatoire (méthode Jake Van Clief)

```markdown
# Mission M-001 — <agent>
- statut : brouillon
- demandeur : Nathan
- créé le : YYYY-MM-DD

## 1. OUTCOME
Le résultat visible attendu, en une phrase.

## 2. HOW
Outils et étapes autorisés (services agent_office, fichiers, recherche…).

## 3. TOUCH
- Modifiable : <chemins exacts>
- Interdit : <tout le reste, notamment suppressions et envois>

## 4. HUMAN-CHECK
La porte de validation avant « terminé » (test, preview, relecture Nathan…).

## Journal
- YYYY-MM-DD : création.
```

## Règles

1. Une mission ne demande que des capacités déclarées dans la fiche de l'agent.
2. Rien d'irréversible sans HUMAN-CHECK validé (jamais de suppression, jamais d'envoi/publication automatique).
3. Mission terminée = une entrée `update journal` + la preuve dans le fichier de mission.
4. Les missions refusées restent dans le registre avec la raison (mémoire du système).
