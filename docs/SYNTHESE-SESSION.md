# 🧭 SYNTHÈSE DE SESSION — par sujets et domaines

> **Période** : 7-8 octobre 2026 · **Branche** : `arena/93b54a79-monorepo` · 15 tâches enchaînées, 13 docs livrés, 1 projet logiciel expédié.
> Cette page est la carte de tout le travail : chaque domaine, ce qui est décidé, ce qui est ouvert, et comment les domaines se tiennent.

---

## 0. 🗺️ La carte d'ensemble

```
                    ┌──────────────────────────────────────┐
                    │   1. HYGIÈNE DE L'INFORMATION        │
                    │   Gmail trié · filtres · mail-org.   │
                    └────────────────┬─────────────────────┘
                                     ▼
                    ┌──────────────────────────────────────┐
                    │   2. LE LIFE HUB (centre de gravité) │
                    │   app/ + USER/ git-first + agents    │
                    └───┬─────────┬─────────┬─────────┬────┘
                        ▼         ▼         ▼         ▼
              3. PROSPECTIVE   4. MÉDIAS  5. HARDWARE  8. CRÉATION
              2026-2035        & sources  & corps      OUTSIDER
              + tracker scoré  + signal   (lunettes,   (1er grand
                               Shenzhen   serveur)     consommateur
                        ▼                                  du stack)
              6. SYSTÈME IA COMBINÉ ── router L1 · mémoire L2 ·
                                       personas L3 · UI L4
                        ▼
              7. UI MOBIGLAS (design SF : home / HUD / options)
```

**Le fil conducteur de toute la session** : passer de *subir* (boîte mail, algo, abonnements) à *posséder* (données git-first, prédictions scorées, achats rationnels, système IA à soi). C'est la conclusion nº1 de la prospective : **« propriétaire vs locataire de son IA » est le clivage de la décennie** — et chaque livrable applique cette règle.

---

## 1. 📬 Hygiène de l'information
| | |
|---|---|
| **Fait** | Tri complet Gmail (137 messages, 9 labels, inbox vide, **zéro suppression** — règle absolue posée par toi) ; documents copiés dans Drive (« Classement emails » + README) ; 18 recettes de filtres en Google Doc ; **`projects/mail-organizer/`** expédié (19 tests, commit `2f09e8a`) |
| **Décidé** | La boîte de 20 k mails = `nathancabrol@hotmail.fr` → import unique Gmail + redirection Outlook recommandée |
| **Leçon** | « Archiver tout, trier par couches » — ce réflexe resservira partout (icebergs, USER/, tracker) |

## 2. 🏠 Système personnel & Life Hub
| | |
|---|---|
| **Fait** | `docs/FEATURES-INVENTORY.md` (`dde1e2a`) ; `docs/LIFE-HUB.md` (`593ac38`) : audit de 10 suites tout-en-un → **danielmiessler/LifeOS** (19,3k★ MIT) choisi comme socle ; faisabilité vérifiée (bun, gh, parties privées) ; alternatives Notion gardées en plan B |
| **Décidé** | Stratégie « copier-adpter » plutôt que brique par brique ; USER/ markdown git-first |
| **En attente** | **Ta décision d'adoption** — renforcée depuis par le benchmark (§5) : aucun challenger ne couvre budget+planning+mails+mémoire |

## 3. 🔭 Prospective tech 2026-2035
| | |
|---|---|
| **Fait** | `docs/PROSPECTIVE-TECH-2026-2035.md` (`745e3e6`) : année par année, sources datées, confiances 🟢🟡🔴, profils A/B, cartes sauvages, règle anti-vertige (4 signaux trimestriels) |
| **Fait (suite)** | `docs/PROSPECTIVE-TRACKER.md` (`44afa35`) : **24 prédictions rendues falsifiables et scorées**, watchlist des signaux, journal de révisions, 1ʳᵉ revue janvier 2027 |
| **Décidé** | On ne publie pas de « taux de réussite » sous ~20 résolues (leçon anti-grift Predictive History) |

## 4. 📺 Médias, chaînes & confiance des sources
| | |
|---|---|
| **Fait** | `docs/INSPIRATIONS-CHAINES.md` (3 vagues, 15 chaînes, zooms, règle **« signal Shenzhen »**) ; `docs/ANALYSE-YOUTUBE-COMPLETE.md` (`002e8a0`) : catalogues complets, **3 régimes de confiance** (démonstration vérifiable / essai argumenté / conversation non sourcée), pattern objet→système→monde, 5 enseignements actionnables |
| **Décidé** | Vigilance active sur 2 chaînes en dérive (Predictive History → circuit Tucker ; Ordinary Things → éditorial politique) ; Rogan = divertissement, jamais source |

## 5. 🔧 Hardware, corps & achats
| | |
|---|---|
| **Fait** | `docs/LUNETTES-IA-ETUDE.md` (`91d49bd`) : MemoMind One = attendre ; concurrents display-first ; open source Brilliant Frame ; DIY ESP32 sur `/api/life/*` |
| **Fait** | `docs/HARDWARE-LIFE-HUB.md` (`a667404`) : carte matériel par rôle (corps/maison/IA locale/DIY), piles Profil A (~1 000-1 500 $) vs B (~250 $), anti-achats (Humane etc.) |
| **Décidé** | Règle d'achat Shenzhen : générique là-bas ⇒ chute de prix sous 12-18 mois ⇒ fenêtre ; confirmée par 8 ans de catalogue Strange Parts/Canoopsy |

## 6. 🤖 Système IA combiné
| | |
|---|---|
| **Fait** | `docs/BENCHMARK-HARNESS-2026.md` (`18a395c`) : radar de 16 projets nés avr→oct 2026, audit des 3 derniers (**second-brain-os** 1 010★ MIT, **AgentVerse-OS** 977★ Apache, **Amethyst** FastAPI/MIT) — matrice vs LifeOS |
| **Fait** | `docs/SYSTEME-COMBINE-IA.md` (`8ed9a46`) : identification GobboNet / SillyTavern / AIRouter→**LiteLLM** / « poko-poki »→**Portkey (hypothèse)** ; verdict : le système complet n'existe pas → **construction 4 couches** (L1 router · L2 mémoire retrieval · L3 personas Tavern v2 · L4 UI), ~1 semaine |
| **En attente** | Confirmation du nom du projet « enterprise » (Portkey ?) |

## 7. 🪟 Interface & design SF
| | |
|---|---|
| **Fait** | `docs/UI-MOBIGLAS.md` (`1854ba2`) : cahier des charges design — home à 9 tuiles-widgets diégétiques, HUD 3 niveaux (dont mode lunettes), options façon LCARS ; bibliothèque d'inspiration sourcée (mobiGlas design notes, Dead Space, JARVIS, Her, Pip-Boy, anti-pattern Cyberpunk) ; standards empruntés au genre harness : cartes Tavern v2 + endpoint OpenAI-compatible |
| **En attente** | Feu vert construction (PWA `app/`, tuiles, vue options) |

## 8. 🎮 Création — OUTSIDER (ouvert aujourd'hui)
| | |
|---|---|
| **Fait** | Réception de la discussion game design (RAW 46 — économie et société surnaturelle, univers *Supernatural*) ; création du chantier `projects/outsider/` : README studio, docs RAW + Société cachée formalisée, stubs PHENOMENON_ENGINE/WORLD_STATE, roster d'agents + prompts |
| **Décidé** | Principe canon : *« tout ce qui existe dans le canon et qui peut être systématisé doit devenir potentiellement systémique »* ; monde qui tourne sans le joueur ; progression = connaissance (NG+) |
| **En attente** | PHENOMENON_ENGINE.md et WORLD_STATE.md (prochaines étapes du chantier) |

---

## 9. ⏳ Décisions ouvertes (dans l'ordre logique)
1. **Adoption LifeOS** (le benchmark a renforcé le oui) → débloque les phases 1-2.
2. **Nom du projet « enterprise »** (Portkey ou autre ?) → ajuste la couche L1.
3. **Lancement construction** : routeur L1 + UI mobiGlas PWA.
4. **Outsider** : enchaîner sur PHENOMENON_ENGINE + WORLD_STATE.
5. **Serveur maison** : re-benchmark AgentVerse-OS à l'achat (revue tracker T1 2027).

## 10. 📚 Index rapide des livrables
`docs/LIFE-HUB.md` · `docs/FEATURES-INVENTORY.md` · `docs/PROSPECTIVE-TECH-2026-2035.md` · `docs/PROSPECTIVE-TRACKER.md` · `docs/INSPIRATIONS-CHAINES.md` · `docs/ANALYSE-YOUTUBE-COMPLETE.md` · `docs/LUNETTES-IA-ETUDE.md` · `docs/HARDWARE-LIFE-HUB.md` · `docs/BENCHMARK-HARNESS-2026.md` · `docs/SYSTEME-COMBINE-IA.md` · `docs/UI-MOBIGLAS.md` · `projects/mail-organizer/` · `projects/outsider/`
