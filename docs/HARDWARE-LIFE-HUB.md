# 🖥 HARDWARE — La pile matérielle du Life Hub (2026)

> 8 octobre 2026 · branche `arena/93b54a79-monorepo`
> Suite de `LUNETTES-IA-ETUDE.md`. Objectif : cartographier le hardware disponible pour chaque rôle du Life Hub (corps · poche · maison · DIY), avec prix vérifiés, options open source et signaux Shenzhen. Règle d'or héritée des échecs du secteur : **un appareil ne doit pas remplacer le smartphone, il doit le compléter.**

---

## 1. 🎙️ Sur le corps — les pendentifs IA (leçon de marché en direct)

Le **Limitless Pendant** (mémoire de réunions) est **arrêté** ; ses utilisateurs migrent ([comparatif post-mortem](https://luci.memories.ai/alternatives/limitless)) — la preuve par l'exemple que le cloud fermé peut éteindre votre appareil.

| Appareil | Prix | Ouvert ? | Capture | Point clé |
|---|---|---|---|---|
| **Omi** ⭐ | ~89-179 $ | ✅ matériel + firmware + app sur GitHub, plugin store | Always-on, 24 h | « Si la boîte disparaît, le code reste » ([classement pendants](https://legendmemory.ai/blogs/the-archive/best-ai-pendant-2026-every-model-compared-and-which-to-buy)) |
| **Plaud NotePin S** | 179 $ + abonn. | ❌ | Press-to-record, précis | Le plus mûr, 300 min/mois gratuites puis 99-240 $/an |
| **Bee Pioneer** | 49,99 $ | ❌ (**propriété d'Amazon**) | Ambiante, 7 j batterie | Le moins cher, mais écosystème captif |
| **UMEVO Note Plus** | 149-169 $ | ❌ | 40 h, mode appel par conduction | 140+ langues |

**Leçons Humane/Rabbit** ([analyse des échecs](https://blogviro.com/world-wide/humane-ai-pin-vs-rabbit-r1-why-both-failed/)) : Humane AI Pin **arrêté le 28/02/2025** (surchauffe, abonnement 24 $/mois, voulait remplacer le téléphone) ; **Rabbit R1** survit ([OS3 en 09/2026](https://theaicemetery.com/rabbit-r1/), pas d'abonnement) mais reste niche ([review 2026](https://www.layer3labs.io/gear/reviews/rabbit-r1)). Facteurs d'échec : logiciel inachevé au lancement, batterie, « veut tout faire ».

## 2. 💍 Santé au corps — bagues & bracelets
| Bague | Prix | Abonnement | Batterie | Verdict |
|---|---|---|---|---|
| Oura Ring 4/5 | 299-499 $ | **5,99 $/mois** | 5-9 j | La référence logicielle… tant que tu paies |
| Samsung Galaxy Ring | 234-399 $ | ❌ | ~7 j | Android only |
| **RingConn Gen 2** ⭐ | 299 $ | ❌ | **10-12 j** | Le champion sans abonnement |
| **Amazfit Helio Ring** | **110-150 $** | ❌ | 4 j | L'entrée de gamme sérieuse |

Sources : [Gabellioni](https://gabellioni.com/best-smart-rings/) · [The Gadgeteer](https://the-gadgeteer.com/2026/05/23/best-smart-rings-health-fitness-sleep-tracking/) · [RestGadgets](https://restgadgets.com/best-smart-rings-for-sleep-tracking-2026/)
→ Pour le Life Hub : l'important n'est pas la marque mais **l'export des données** (RingConn/Amazfit exportent ; Oura verrouille derrière l'abonnement).

## 3. 🏠 À la maison — le serveur du Life Hub (mini PC & IA locale)

### Palier serveur ([vecosys](https://www.vecosys.com/best-mini-pc-home-lab-dev-environment-2026/), [minipclab](https://minipclab.com/blog/best-mini-pc-for-home-server), [mindset&megabytes](https://mindsetandmegabytes.com/best-mini-pc-home-server/))
| Machine | Prix | Idle | Rôle Life Hub |
|---|---|---|---|
| Beelink EQ12/S12 (N100/N95) | ~150 $ | 6 W | Nœud Docker minimal |
| **Beelink MINI S13 / EQ14 (N150)** ⭐ | ~170-220 $ | 6-8 W | **Tout le stack `app/` + mail-organizer + sauvegarde git** |
| GMKtec K8 / GEEKOM A8 (Ryzen 7 8845HS) | ~350-400 $ | ~15 W | Proxmox + Vikunja + n8n + petits LLM sur iGPU |
| Beelink SER9 Max (Ryzen AI 9 365) | ~550 $ | — | Charges IA avec **NPU intégré** |
| Stacks complets chiffrés | 190-720 $ | — | HA seul → HA+caméras → +IA locale 8B ([promptquorum](https://www.promptquorum.com/smart-home/best-hardware-for-local-smart-home)) |

### Palier IA locale ([clawbox](https://clawbox.com/blog/2026-04-03-self-hosted-ai-hardware-guide-2026), [newegg](https://www.newegg.com/insider/best-ai-pc-builds-for-running-local-llms-in-2026/), [guide VRAM](https://www.kunalganglani.com/blog/running-local-llms-2026-hardware-setup-guide), [guide 2026](https://www.kunalganglani.com/blog/ai-hardware-complete-guide))
| Option | Perf | Coût 3 ans | Notes |
|---|---|---|---|
| **Pi 5 + Hailo-10H M.2** | Qwen2-1.5B, **serveur compatible OpenAI** `/v1/chat/completions` ([hailo-llm-server](https://github.com/marco-tinkerer/hailo-llm-server)) | ~173 $ + NPU | Mini-assistant local branchable sur `/api/life/*` |
| **Jetson Orin Nano** | 67 TOPS, 22-45 tok/s (modèles 1-4B) | ~367 $ | Le meilleur rapport edge-AI |
| RTX 4060 Ti **16 GB** | 7B-13B Q4 | build 600-900 $ | L'entrée « vrai LLM local » |
| RTX 4090 24 GB | 32B Q4 | ~1 599 $ la carte | Palier sérieux |
| **Apple Silicon 64-128 GB** | Modèles >32B, **69+ tok/s en MLX** | $$$ | La mémoire unifiée bat le multi-GPU à budget égal |
| RTX 3090 d'occasion | 24 GB | stack 1 400-1 700 $ | L'astuce budget du stack complet |

## 4. 🔩 DIY & signal Shenzhen — les briques à quelques euros ([ESP32 2026](https://www.lst-iot.com/esp32-development-boards-explained-which-one-should-you-buy-in-2026/), [ComponentIndex](https://componentindex.net/blog/best-esp32-boards-2026/))
| Carte | Prix | Usage Life Hub |
|---|---|---|
| ESP32-C3 Super Mini | **~2 $** | Capteurs/boutons (RISC-V) |
| ESP32-S3 DevKitC | ~7 $ | Le polyvalent 2026 (instructions vectorielles IA) |
| **Seeed XIAO ESP32-S3 Sense** ⭐ | 15-40 $ | **Caméra + micro + SD** format timbre-poste = le pendentif Omi fait maison |
| TTGO T-Display | ~8 $ | **Écran intégré** = HUD de poche / proto-lunettes |
| LilyGO T-Beam | ~25 $ | GPS + LoRa (terrain, rando, vélo) |
| Achat direct Shenzhen | **0,99-10 $/module** ([Accio](https://www.accio.ai/find-product/esp32-dev-module-board)) | La source du signal : générique = prix effondré |

→ La boucle avec `LUNETTES-IA-ETUDE.md` : un HUD maison = XIAO ou TTGO + optique beam-splitter + `/api/life/*` en BLE.

## 5. 🧭 Recommandations de stack

### Profil A — ingénieur Paris (budget ~1 000-1 500 $)
1. **Maison** : mini PC N150 (~200 $) pour `app/` + git + mail-organizer 24/7 → Ryzen 7 (~400 $) si Proxmox/Vikunja/n8n.
2. **IA locale** : commencer sur iGPU/Ryzen AI ; monter en Pi 5+Hailo (~100 $ de plus) pour un assistant OpenAI-compatible **100 % hors cloud** — cohérent avec la souveraineté git-first.
3. **Corps** : bague sans abonnement (RingConn 299 $ ou Amazfit 110 $) + pendentif **Omi** (179 $) ou **DIY XIAO Sense** (~40 $) → captures → transcription → `data/life/inbox/`.
4. **Yeux** : Brilliant Frame (349 $, tout ouvert) ou HUD DIY — pas de MemoMind avant les retours post-livraison.

### Profil B — 2 000 $ (validation de la prospective)
Smartphone déjà possédé + **Amazfit Helio (110 $) + EQ12 d'occasion (~120 $) + 2-3 ESP32 (~15 $)** = **~250 $** pour l'équivalent fonctionnel du stack complet. Le reste passe en énergie/résilience. La déflation Shenzhen rend l'accès quasi universel — la différence A/B se joue sur l'orchestration, pas le matériel.

### Anti-achats (leçons 2024-2026)
- Tout appareil « qui remplace le téléphone » (Humane).
- Tout wearable cloud fermé à abonnement obligatoire (risque Limitless).
- Le hardware présenté uniquement en salon sans dispo réelle (règle de Shenzhen).

## 6. 📚 Sources
Pendentifs : [alternatives Limitless](https://luci.memories.ai/alternatives/limitless) · [umevo comparatif](https://www.umevo.ai/blogs/ume-all-posts/limitless-vs-bee-vs-omi-the-wearable-ai-showdown) · [legendmemory classement](https://legendmemory.ai/blogs/the-archive/best-ai-pendant-2026-every-model-compared-and-which-to-buy) · [échecs Humane/Rabbit](https://blogviro.com/world-wide/humane-ai-pin-vs-rabbit-r1-why-both-failed/) · [Rabbit R1 statut](https://theaicemetery.com/rabbit-r1/) · [review R1 2026](https://www.layer3labs.io/gear/reviews/rabbit-r1)
Bagues : [Gabellioni](https://gabellioni.com/best-smart-rings/) · [The Gadgeteer](https://the-gadgeteer.com/2026/05/23/best-smart-rings-health-fitness-sleep-tracking/) · [RestGadgets](https://restgadgets.com/best-smart-rings-for-sleep-tracking-2026/)
Mini PC/serveur : [vecosys](https://www.vecosys.com/best-mini-pc-home-lab-dev-environment-2026/) · [minipclab](https://minipclab.com/blog/best-mini-pc-for-home-server) · [mindset&megabytes](https://mindsetandmegabytes.com/best-mini-pc-home-server/) · [promptquorum stacks](https://www.promptquorum.com/smart-home/best-hardware-for-local-smart-home)
IA locale : [clawbox](https://clawbox.com/blog/2026-04-03-self-hosted-ai-hardware-guide-2026) · [newegg builds](https://www.newegg.com/insider/best-ai-pc-builds-for-running-local-llms-in-2026/) · [guide VRAM](https://www.kunalganglani.com/blog/running-local-llms-2026-hardware-setup-guide) · [guide complet](https://www.kunalganglani.com/blog/ai-hardware-complete-guide) · [hailo-llm-server GitHub](https://github.com/marco-tinkerer/hailo-llm-server)
ESP32/Shenzhen : [lst-iot familles ESP32](https://www.lst-iot.com/esp32-development-boards-explained-which-one-should-you-buy-in-2026/) · [ComponentIndex](https://componentindex.net/blog/best-esp32-boards-2026/) · [Accio prix Shenzhen](https://www.accio.ai/find-product/esp32-dev-module-board)
