# 👓 ÉTUDE — Lunettes IA à affichage : MemoMind, concurrence, open source & DIY

> 8 octobre 2026 · branche `arena/93b54a79-monorepo`
> Demande : auditer les lunettes **MemoMind**, la concurrence, et trouver les **versions open source / faites maison** (affichages similaires) via YouTube/Reddit. Contexte : le Life Hub cherche son interface « vie réelle » (PC · tel · **réel**).

---

## 1. 🎯 MemoMind One (XGIMI) — la fiche

| Élément | Détail |
|---|---|
| Produit | **MemoMind One** — lunettes IA **sans caméra** de la marque MemoMind (groupe **XGIMI**, spécialiste projecteurs) |
| Affichage | **Double Micro-LED** 640×350, **2000 nits**, FOV 25°, 30 Hz, image flottante jusqu'à 5 m |
| Audio/contrôle | Harman AudioEFX open-ear, 3 micros, bouton + voix + gestes de tête |
| Poids / batterie | 46,6 g (magnésium-alu, titane beta, acétate) · **16 h** d'usage mixte |
| Fonctions IA (Memo+) | AI Recorder (sous-titres + résumés), traduction temps réel (texte+audio), navigation, Idea Notes, teleprompter — 8 fonctions sans abonnement au lancement |
| Prix | Kickstarter été 2026 : **399 $** (MSRP 599 $) ; 499 $ avec verres ZEISS ; 6 mois de Memo+ inclus |
| Compat | iOS, Android, HarmonyOS ; BLE bridge |

**Sources** : [Gadgeteer](https://the-gadgeteer.com/2026/07/01/memomind-one-ai-glasses-open-preorders-at-399/) · [GizmoCrowd](https://www.gizmocrowd.com/post/memomind-one-smart-glasses-review) · comparatif officiel [vs Even G2](https://www.memo-mind.com/blogs/buyers-guide/how-to-choose-ai-glasses-that-fit-you)

### Revues (honnêteté check)
- **Gizmodo** ([« You Don't Want Smart Glasses That Record Everything You Say »](https://gizmodo.com/you-dont-want-smart-glasses-that-record-everything-you-say-trust-me-2000793058)) : écran net/lumineux, matériel léger et confortable, traduction bluffante — **mais** l'enregistreur permanent est flippant (LED rouge à peine visible), l'assistant vocal est inégal, audio médiocre, méthodes d'entrée insuffisantes.
- YouTube : [« AI Glasses That Remember Everything »](https://www.youtube.com/watch?v=ObfaiS7a0qE) (focus Memo+) · [« Display and NO Camera »](https://www.youtube.com/watch?v=6NITNMjBgY8) (review Kickstarter).

## 2. 🥊 La concurrence (segment « affichage dans le verre »)

| Modèle | Prix | Affichage | Caméra | Poids | Angle |
|---|---|---|---|---|---|
| **MemoMind One** | 399-599 $ | Micro-LED binoculaire 640×350, 2000 nits | ❌ | 46,6 g | 25° |
| **Even Realities G1** | 599 $ | Micro-LED **vert monochrome** 640×200, 1000 nits | ❌ | ~39 g | 25° ([visionxo](https://visionxo.com/products/even-realities-g1)) |
| **Even Realities G2** (+ bague R1) | 599 $+ | Mono 1200 nits | ❌ | 36 g | 27,5° |
| **RayNeo iO** | — | Micro-LED mono waveguide | ❌ | **33 g** | 23,5° |
| **Halliday** | 489 $ | Projection « invisible » | ❌ | — | — |
| **Rokid Glasses** | 599 $ | Double écran | ✅ | — | — |
| **RayNeo X3 Pro** | 1 099 $ | Micro-LED **couleur** + SLAM/6DoF | ✅ 12 MP | 76 g | 30° |
| **Meta Ray-Ban Display** | 799 $ | In-lens + Neural Band (EMG) | ✅ | — | — |
| **Xiaomi AI Glasses** | — | — | ✅ | — | — |

Typologie du marché ([Ai Miracle](https://www.aimiracle.ai/ai-collections/best-ai-smart-glasses/), [Dymesty guide 2026](https://dymesty.com/blogs/articles/glasses-with-display)) : **camera-first** (Meta, Xiaomi) vs **display-first sans caméra** (Even, RayNeo iO, Halliday, MemoMind) — MemoMind se positionne comme le plus lumineux et le moins cher du second groupe.

## 3. 🔓 Open source & fait maison (ce que tu soupçonnais existe bel et bien)

### A. Les plateformes open source sérieuses
| Projet | Ce que c'est | Où |
|---|---|---|
| **[Brilliant Labs Frame](https://www.toolmage.com/en/tool/frame/)** | Lunettes IA **matériel + firmware ouverts sur GitHub** : 39 g, micro-OLED **couleur** 640×400 (prisme), caméra + micro, OS en **Lua**, assistant Noa (GPT-4o/Whisper via téléphone) ; 349 $ ([annonce](https://www.urdesignmag.com/brilliant-labs-frame-smart-glasses/)) | brilliant.xyz / GitHub |
| **[OSSG — Team Open Smart Glasses](https://github.com/Mentra-Community/OpenSourceSmartGlasses)** | Fichiers mécaniques + électroniques + logiciels + guide de construction ; la communauté a depuis lancé **AugmentOS** : un OS unifiant des lunettes commerciales (Even G1, Vuzix Z100) avec app store et SDK | GitHub Mentra-Community |
| **MentraOS** | Écosystème logiciel ouvert multi-appareils, fonctions local-only/offline possibles | mentra.live |
| ⚠️ **OpenGlass** | Piège de nom : l'ancien `BasedHardware/OpenGlass` est **abandonné** (devenu **Omi**, le pendentif) ; l'OpenGlass de 2026 est un projet académique ETH (RISC-V, caméras event-based, [arXiv](https://arxiv.org/html/2606.07431v1)) sans rapport | [synthèse RayNeo](https://www.rayneo.com/blogs/news/open-source-smart-glasses) |

### B. Fait maison — les affichages similaires trouvés via Reddit/YouTube/Hackaday
| Projet | Recette d'affichage | Source |
|---|---|---|
| **Wearables-Telescope** | ESP32 + microdisplay **0,24" 540p** (viewfinder caméra/goggles FPV, ~15-30 $) en vidéo composite + « TelescopeOS » | [GitHub](https://github.com/alex1115alex/Wearables-Telescope) |
| **uGlass** (module AR) | Écran + optique sur lunette ; leçon documentée : **le problème n'est pas l'écran mais l'optique** (FOV + distance focale) | [Hackaday.io](https://hackaday.io/project/167854-uglass-an-ar-module-on-your-glasses) |
| Thread r/arduino « Meta-like sans miroir » | **Plaque beam-splitter** fine = l'option la moins chère ; variantes : écran 1" + réflecteur 45° + lentille Fresnel 3-5× + plastique semi-réfléchissant | [reddit](https://www.reddit.com/r/arduino/comments/1kiaf5z/looking_for_diy_smart_glasses_setup_like_meta/) |
| Thread r/raspberry_pi | Miroirs d'**optique red-dot airsoft** comme combinateur HUD ([vidéo lemlurker](https://www.youtube.com/watch?v=bJNDMVMoOSk)) ; lunettes **Pi Zero** avec hand-tracking, STL + code publiés | [reddit](https://www.reddit.com/r/raspberry_pi/comments/1ki88et/looking_for_diy_display_solutions_for_smart/) |
| Arduino + OLED transparent | Arduino Nano Every + OLED transparent + HC-05 Bluetooth + LiPo (projet lycéen, tuto vidéo) | [Geeky Gadgets](https://www.geeky-gadgets.com/smart-glasses-27-07-2020/) · [tuto YouTube](https://www.youtube.com/watch?v=IpJqzwXWg-k) |
| Google Glass knock-off | Arduino + **OLED SSD1306** (128×64 I²C) → le standard absolu du HUD maison, ~5 $ | [r/arduino](https://www.reddit.com/r/arduino/comments/nclkev/wearable_hud_google_glass_knock_off/) + [multimètre HUD Hackaday](https://hackaday.com/2021/04/18/heads-up-smart-glass-multimeter/) |

**Consensus technique de la communauté** : n'importe quel petit écran (SSD1306 ~5 $, micro-OLED FPV ~20 $, microdisplay 540p ~30 $) fait l'affaire ; **la difficulté réelle = l'optique** (combinateur, distance focale, FOV). Les waveguides des produits commerciaux sont précisément ce qu'on ne peut pas encore facilement DIY — d'où les recettes beam-splitter/red-dot/Fresnel.

## 4. 🧊 Reality check Reddit (contre les revues lustrées)
Retours d'usage **Even G1** après des mois d'utilisation ([r/augmentedreality](https://www.reddit.com/r/augmentedreality/comments/1ov89av/even_g2_and_r1_are_here_smart_glasses_and_ring_by/), [r/EvenRealities](https://www.reddit.com/r/EvenRealities/comments/1krioxm/my_g1_review_after_a_couple_of_weeks/), [daily-use thread](https://www.reddit.com/r/EvenRealities/comments/1p6tmof/are_they_truly_daily_use/)) :
- Bugs persistants non corrigés : un seul écran s'allume, notifs manquées, déconnexions, recharge capricieuse (« ils savent faire du hardware, pas du logiciel »).
- **IA trop lente** (5+ s) → les utilisateurs ressortent le téléphone ; traduction quasi inutilisable hors pièce calme.
- Fatigue oculaire/mal de tête après une demi-journée ; lisibilité en plein soleil nécessitant un clip solaire.
- Point vie privée relevé : envoi de données constant au téléphone.
→ **Leçon pour MemoMind** : produit en crowdfunding = attendre les retours post-livraison ; la fiche technique (2000 nits, 16 h) ne dit rien de la fiabilité logicielle.

## 5. 🧭 Recommandation pour toi (lien Life Hub)
| Profil | Option | Verdict |
|---|---|---|
| **Acheter maintenant** | MemoMind One (399 $, sans caméra, le plus lumineux du segment) | Séduisant sur le papier, mais crowdfunding + écosystème XGIMI fermé + avis Gizmodo mitigés → **attendre les premières livraisons et les retours Reddit** |
| **Bricoler (le plus aligné avec le monorepo)** | **Brilliant Labs Frame** (349 $, tout ouvert, Lua, API) ou DIY **ESP32 + SSD1306 + beam-splitter** (<50 $) | Le Frame peut afficher **directement les données de `/api/life/*`** (agenda, budget, tâches, capture vocale → inbox git) ; le DIY est un excellent projet week-end |
| **Observer** | AugmentOS/MentraOS | La couche logicielle ouverte qui unifie plusieurs lunettes — à surveiller pour ne pas s'enfermer |

💡 **Idée Life Hub** : les lunettes = l'écran « vie réelle » de l'agent — un mode `life glance` qui pousse sur l'affichage : prochaine tâche, notif filtrée par les règles mail-organizer, rappel budget. Le pipeline existe déjà (API → n'importe quel afficheur), il ne manque que le device.

## 6. 📚 Sources
MemoMind : [Gadgeteer](https://the-gadgeteer.com/2026/07/01/memomind-one-ai-glasses-open-preorders-at-399/) · [GizmoCrowd](https://www.gizmocrowd.com/post/memomind-one-smart-glasses-review) · [memo-mind.com comparatif](https://www.memo-mind.com/blogs/buyers-guide/how-to-choose-ai-glasses-that-fit-you) · [Gizmodo](https://gizmodo.com/you-dont-want-smart-glasses-that-record-everything-you-say-trust-me-2000793058) · reviews YouTube [1](https://www.youtube.com/watch?v=ObfaiS7a0qE) [2](https://www.youtube.com/watch?v=6NITNMjBgY8)
Concurrence : [Ai Miracle top 2026](https://www.aimiracle.ai/ai-collections/best-ai-smart-glasses/) · [visionxo G1](https://visionxo.com/products/even-realities-g1) · [Dymesty guide](https://dymesty.com/blogs/articles/glasses-with-display)
Open source : [RayNeo — synthèse open-source glasses](https://www.rayneo.com/blogs/news/open-source-smart-glasses) · [Brilliant Labs Frame](https://www.toolmage.com/en/tool/frame/) · [urdesignmag Frame](https://www.urdesignmag.com/brilliant-labs-frame-smart-glasses/) · [OSSG GitHub](https://github.com/Mentra-Community/OpenSourceSmartGlasses) · [OpenGlass ETH arXiv](https://arxiv.org/html/2606.07431v1)
DIY/Reddit/YouTube : [Telescope GitHub](https://github.com/alex1115alex/Wearables-Telescope) · [uGlass Hackaday](https://hackaday.io/project/167854-uglass-an-ar-module-on-your-glasses) · [r/arduino beam-splitter](https://www.reddit.com/r/arduino/comments/1kiaf5z/looking_for_diy_smart_glasses_setup_like_meta/) · [r/raspberry_pi displays](https://www.reddit.com/r/raspberry_pi/comments/1ki88et/looking_for_diy_display_solutions_for_smart/) · [Geeky Gadgets Arduino OLED](https://www.geeky-gadgets.com/smart-glasses-27-07-2020/) · [tuto YouTube 2019](https://www.youtube.com/watch?v=IpJqzwXWg-k) · [r/arduino SSD1306 HUD](https://www.reddit.com/r/arduino/comments/nclkev/wearable_hud_google_glass_knock_off/) · [HUD multimètre Hackaday](https://hackaday.com/2021/04/18/heads-up-smart-glass-multimeter/)
Reality check : [r/augmentedreality G2](https://www.reddit.com/r/augmentedreality/comments/1ov89av/even_g2_and_r1_are_here_smart_glasses_and_ring_by/) · [r/EvenRealities G1](https://www.reddit.com/r/EvenRealities/comments/1krioxm/my_g1_review_after_a_couple_of_weeks/) · [daily use](https://www.reddit.com/r/EvenRealities/comments/1p6tmof/are_they_truly_daily_use/)
