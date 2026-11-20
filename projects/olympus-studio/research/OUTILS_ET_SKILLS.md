# Outils et connecteurs examinés — 2026-11-12

## Disponibles et pertinents
- **GitHub connecté** : dépôt utilisateur `Sathancabrol/monorepo`, branche isolée, fichiers et issues; **utilisé pour sauvegarde du travail**.
- **Web / GitHub public** : recherche d'outils et vérification de README/licences, sans copier de code tiers.
- **Skills Vercel** (architecture backend / React / CI / agents) : utiles comme références ponctuelles, mais pas de dépendance à l'hébergement Vercel pour une application locale.
- **Notion** : gestion de suivi possible mais doublon avec GitHub Issues pour les tâches techniques de ce projet; évité à ce stade.
- **Canva / Lovable** : utiles pour maquettes/UI, mais ne remplacent ni libobs, ni l'éditeur NLE, ni le moteur média; ne pas créer de dépendance cloud.
- **OpenReelio agent skills** : https://github.com/openreelio/skills, potentiellement utiles si OpenReelio est retenu. Non installés ou testés ici.
- **OBS/ComfyUI/Blender/FFmpeg** : logiciels locaux externes; aucun connecteur ChatGPT ne prouve qu'ils sont installés sur la tour.

## Automatisation
Tentative de planification nocturne de 7 sessions à 03:00 Europe/Paris du 13 au 19 novembre 2026 : **rejetée** (5 tâches actives / plafond de 5). Aucune tâche existante supprimée. Suivi conservé dans `docs/ROADMAP.md` et GitHub issues #11–15.

## Critère de sélection de chaque brique
- Fonction réelle testable ; **licence de la version ciblée et des modèles**.
- Offline, sans coût forcé ; mémoire VRAM 4-6 Go et RAM 8-16 Go.
- API/CLI exploitable sans surveiller une interface externe à la main.
- Export portable et stockage durable.
- Non intrusif : permissions explicites et aucun enregistrement silencieux.
