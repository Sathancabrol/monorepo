# Fonctionnalités visées pour LAPLACE

**Cible produit :** un assistant personnel disponible dans Discord, avec une mémoire maîtrisée, des modes d’expertise et des capacités d’analyse/génération texte et média. Le 8 octobre 2026, le propriétaire a choisi : commencer par un profil général; proposer l’audio en fichiers puis le live; analyser les photos envoyées puis ajouter une capture locale sur demande; construire analyse et génération par étapes, local d’abord et API externe activée explicitement par capacité. L’analyse ponctuelle d’une image est maintenant disponible si un modèle vision est configuré; la voix, la génération média, les documents et les autres fonctions restent à implémenter.

## État actuel et cible

| Domaine | Dans le MVP | Cible |
|---|---|---|
| Texte | `/parler`, réponses privées par défaut, Ollama local ou API compatible optionnelle. | Garder le même accès simple; étendre par des capacités explicitement activées. |
| Mémoire | Souvenirs privés par ID Discord; souvenirs partagés opt-in et isolés par serveur; corrections versionnées, recherche FTS, export/effacement; archive brute avec rétention. | Mémoire à court/long terme, recherche sémantique facultative, sources traçables, contrôles fins de conservation et import de connaissances choisi par l’utilisateur. |
| Expertise | Prompt général; aucune sélection de spécialité dans Discord. | Commencer par le profil général, puis ajouter des profils/configurations versionnés (instructions, modèles, outils et sources) publiés depuis le futur studio Carré d’As. |
| Analyse/génération | Analyse texte dans `/parler` et image envoyée via `/analyser_image` si `VISION_MODEL` est configuré; pas de génération ni d’analyse audio/vidéo/documents. | Déployer progressivement toutes les modalités; traitement local prioritaire, API externe par capacité après activation explicite. |
| Voix | Pas de STT/TTS ni de connexion vocale Discord. | Audio envoyé + réponse audio en fichier d’abord; salon vocal live ensuite. |
| Caméra / selfie | `/analyser_image` traite une seule image explicitement jointe si le modèle vision est configuré; le bot ne contrôle aucune caméra. | Photo/selfie envoyée d’abord; capture ponctuelle ultérieure via un compagnon local avec confirmation visible. |

## 1. Voix

**Choix confirmé : les deux parcours, dans cet ordre.** Distinguer trois parcours qui n’ont pas les mêmes contraintes :

1. **Entrée audio** : la personne joint un message vocal ou un fichier; LAPLACE le transcrit, comprend la demande et répond d’abord par texte.
2. **Réponse parlée** : l’utilisateur demande une réponse audio; le bot produit un fichier vocal privé. STT/TTS locaux sont préférés si la qualité et les ressources de la machine conviennent.
3. **Conversation live** : LAPLACE rejoint un salon vocal et traite le flux en temps réel. Ce n’est pas inclus automatiquement avec les deux premiers parcours; il faut concevoir latence, permission Discord, arrêt immédiat et consentement des personnes présentes.

**Critères d’acceptation :** limite de taille/durée configurable; message d’erreur sans exposer les détails fournisseur; aucune sauvegarde de l’audio ou de la transcription par défaut; commande d’arrêt visible pour le live; réponses vocales privées lorsque Discord le permet. Tester qualité et latence en français sur la machine cible.

## 2. Selfie, photo et caméra

**Choix confirmé : photo envoyée puis capture locale sur demande.** La première fonctionnalité est implémentée avec `/analyser_image image question` : selfie, photo ou capture d’écran envoyée explicitement avec une question. Elle accepte JPEG, PNG et WebP jusqu’à 8 Mio si un `VISION_MODEL` est configuré. L’image est traitée en mémoire pour cette requête, n’entre ni dans l’archive ni dans les souvenirs, et la réponse est éphémère. Le téléversement Discord initial reste sur Discord; LAPLACE ne supprime pas le fichier source.

Un bot Discord standard ne peut pas simplement activer à distance la caméra selfie du téléphone ou la webcam du PC. Une capture directe nécessiterait une application/compagnon local installé et autorisé sur l’appareil. Ce compagnon devrait montrer clairement que la caméra est active, demander une confirmation à chaque capture et ne transmettre l’image qu’à la demande; pas de surveillance en arrière-plan.

**Critères d’acceptation de l’analyse d’image :** formats/taille bornés; vérification de la signature réelle du fichier et des capacités vision; contrôle d’accès aux pièces jointes; réponse privée; aucune reconnaissance d’identité ou inférence sensible par défaut; aucune conservation de l’image; incertitudes signalées. L’analyse d’image et la génération d’images sont deux fonctions séparées. La veille des modèles de visage, objets/scènes, regard, charge cognitive et IRMf est consignée dans [Recherche — modèles vision, caméra et IRMf](RECHERCHE-MODELES-VISION-IRMf.md); aucun de ces modèles n’est intégré ou sélectionné par cette note.

## 3. Mémoire

Le socle de séparation est déjà implémenté et testé : mémoire privée par utilisateur, mémoire partagée associée à un seul ID de serveur, historique de provenance, correction/suppression, export et effacement. Les souvenirs partagés ne sont pas communs à tous les serveurs par défaut.

Évolutions à évaluer :

- **Épisodique** : événements/conversations récents, avec durée configurable et accès par propriétaire.
- **Sémantique** : faits explicitement retenus et connaissances de documents importés, toujours avec source/date.
- **Court terme** : contexte d’une session de conversation, effaçable sans supprimer les souvenirs durables.
- **Recherche sémantique** : optionnelle, index reconstructible depuis des sources autorisées; garder FTS/repli local.
- **Contrôle** : voir ce qui est retenu, corriger, oublier, exporter, supprimer; proposer la mémorisation avant d’enregistrer une donnée durable.

Les embeddings, fichiers joints et transcriptions ne doivent jamais être créés ni conservés sans politique de consentement et de rétention explicite. Une mémoire durable ne doit pas être présentée comme un fait certain sans son niveau de confiance et sa provenance.

## 4. Profils d’expertise

L’expertise doit être **configurable**, pas une promesse qu’un modèle sait tout. Un profil d’expertise regrouperait :

- rôle/consignes versionnés et limites de compétence;
- fournisseur/modèle et capacités exigées (texte, vision ou audio);
- outils autorisés, niveaux de risque et approbations;
- bases documentaires/sources qu’il a le droit de consulter;
- format de réponse souhaité (résumé, étapes, tableau, rapport avec sources);
- jeux de tests qui doivent réussir avant publication.

**Choix confirmé : commencer par l’assistant général.** Ajouter ensuite, si utile, des profils distincts de recherche/synthèse ou d’analyse de documents/projets; leurs connaissances privées ne sont pas partagées automatiquement avec tous les utilisateurs ou serveurs.

**Critères d’acceptation :** un utilisateur sait quel profil répond; l’administrateur peut modifier et versionner ce profil; les réponses indiquent les sources ou les incertitudes; un changement de modèle/outils n’efface pas l’historique de configuration; un profil non publié reste inaccessible aux utilisateurs.

## 5. Analyse

**Choix confirmé : analyse et génération toutes les deux, avec traitement local par défaut et API externe en opt-in par capacité.** Ordre de développement recommandé :

1. Image jointe : `/analyser_image` traite une image sélectionnée par l’utilisateur avec le modèle vision configuré.
2. Documents téléversés : extraction/OCR, synthèse, questions-réponses et références aux pages/sections.
3. Audio joint : transcription, résumé et extraction d’actions; la transcription n’est pas conservée par défaut.
4. Vidéo : taille/durée plafonnées, transcription audio et échantillonnage d’images-clés; pas d’enregistrement continu.
5. Recherche web : outil distinct avec domaines autorisés, date des sources et liens; ne pas prétendre avoir consulté le web tant que l’outil n’est pas activé.
6. Génération d’images/audio/vidéos : uniquement lorsqu’un fournisseur local compatible est configuré; service externe désactivé jusqu’à opt-in explicite pour cette capacité.

Pour chaque modalité, valider formats/taille/durée, modèle et coût, latence, exposition éventuelle à un fournisseur externe, refus en cas de capacité indisponible et purge des fichiers temporaires après traitement. N’ajouter aucune pièce jointe au prompt ou à la mémoire sans consentement.

## Phasage proposé

1. **v0.2 — mémoire et profil général** : rendre la mémoire inspectable; proposer le profil général et son versionnement; recherche sémantique seulement si modèle local adapté.
2. **v0.3 — analyse d’image** : `/analyser_image` est disponible avec configuration facultative; compléter ensuite l’analyse de documents.
3. **v0.4 — voix asynchrone** : STT sur pièce jointe puis TTS en fichier; comparer les voix françaises sur PC avant de sélectionner le moteur.
4. **v0.5 — génération et temps réel** : ajouter progressivement les générations image/audio/vidéo prises en charge localement; APIs externes opt-in séparément; éprouver vidéo et salon vocal live dans des prototypes distincts.
5. **v0.6 — compagnon caméra et actions locales** : capture selfie ponctuelle sur confirmation; outil navigateur/PC isolé, allowlist, audit; aucun shell libre.

Les versions sont une proposition de séquencement, pas une promesse d’implémentation automatique. Le prochain code multimédia dépend encore de l’OS, de la RAM/VRAM et des modèles réellement installés.

## Choix confirmés et prérequis techniques restants

- **Voix :** audio en fichier et salon vocal live, en commençant par les fichiers.
- **Caméra :** analyse d’une photo envoyée, puis capture ponctuelle par un compagnon local avec confirmation.
- **Expertise :** profil général en premier; profils spécialisés ensuite.
- **Médias :** analyse et génération; modèles locaux d’abord, API externe seulement après activation explicite de la capacité concernée.
- **À mesurer avant de choisir les modèles :** système d’exploitation, RAM/VRAM, modèles installés (`ollama list`), qualité/latence souhaitées et limites de coût. Aucun token ou secret n’est nécessaire pour ces choix.
