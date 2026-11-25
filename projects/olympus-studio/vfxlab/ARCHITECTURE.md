# Architecture cible
Source (fichier, caméra, écran, scène Studio) → frame partagé → chaîne VFX → preview A/B → programme LIVE / rendu EDIT → sortie locale / OBS / export.
Moteur : Canvas 2D prototype, WebGL2 en priorité pour effets GLSL ; réduction adaptative de résolution ; aucune copie GPU/CPU par frame si évitable. Adaptateurs externes isolés en processus, démarrage explicite. Réutiliser caméra-pool et média IndexedDB du Studio, jamais ouvrir une seconde caméra quand le pool existe.
Contrat proposé `olympus.vfx.v1` : preset {version:1,id,name,effects:[{id,type,enabled,params}],quality:{width,height,fps}}. Chaque effet : paramètres bornés, ordre explicite, déterminisme pour rendu offline (seed/time), dispose(). Sources exposent frame/time/sourceId/consent ; outputs conservent aspect ratio, horodatage et alpha si possible. Pas de nouveau serveur public. Autoriser seulement les ressources nécessaires dans la liste STATIC_FILES du serveur Studio. Le raccord au canvas LIVE/EDIT devra être effectué au niveau du rendu, pas via capture écran.
## États
Prototype autonome : réglages Canvas, import fichier et caméra, PNG. À vérifier par navigateur. WebGL2, audio, export vidéo, OBS, persistence projet, intégration native et MCP : non implémentés.
## Déploiement indépendant
Un repo dédié peut être créé depuis ce sous-dossier via git subtree split ou copie contrôlée. Conserver ici le module canonique jusqu'à décision de migration. Aucun changement de main ni fusion automatique.
