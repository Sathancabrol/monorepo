"""Admissibilité : ce que le système a le droit d'affirmer.

Deux niveaux, et la distinction est tout l'objet de ce fichier.

`valider()` (dans canonical.py) vérifie la **forme** : l'enregistrement est-il
bien construit ? `admissible()` vérifie le **droit** : a-t-on le droit de
présenter ça comme un fait ?

Les règles viennent de deux endroits du dépôt, pas d'une invention :

- `projects/HCSM/specs/data-schema.md` — contrat V1, dont le validateur est
  implémenté (`projects/HCSM/validator/`) : une observation ne porte jamais de
  champ d'estimation, un score nu est rejeté, aucun identifiant civil.
- `projects/watchtower/audit/RND-PROPOSITIONS-2026.md` §6, anti-pattern n°7 :
  « cacher une réponse invalide en corrigeant le JSON à la volée : la tour doit
  afficher *pourquoi* elle n'est pas sûre, sinon elle devient une machine à
  convictions ».

Transposées ici, ces règles protègent la réunion du 16 octobre : ce qui sera
montré à une collectivité doit pouvoir justifier chacun de ses chiffres, et
refuser de le faire quand c'est impossible.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------- motifs de PII
# Volontairement simples et lisibles : mieux vaut un faible rappel explicable
# qu'une heuristique opaque. Une commune de 131 000 habitants produit des
# adresses, des téléphones et des courriels ; aucun ne doit finir dans un
# enregistrement.
MOTIFS_PII = [
    ("courriel", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("téléphone", re.compile(r"(?:\+33|0)\s?[1-9](?:[\s.\-]?\d{2}){4}")),
    ("n° de sécurité sociale",
     re.compile(r"\b[12]\d{2}(?:0[1-9]|1[0-2])(?:2[AB]|\d{2})\d{3}\d{3}(?:\s?\d{2})?\b")),
    ("IBAN", re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")),
    ("carte bancaire", re.compile(r"\b(?:\d{4}[\s\-]?){3}\d{4}\b")),
]

# Champs qui transforment une observation en estimation : interdits sur un fait.
CHAMPS_ESTIMATION = ("estimation", "projection", "prevision", "score_estime",
                     "valeur_estimee", "extrapolation")

# Producteurs publics : une seule de ces sources suffit à porter un fait.
# C'est le second terme du critère Frontignan — « croisé ≥ 2 sources
# indépendantes, OU source officielle primaire ».
SOURCES_OFFICIELLES = (
    "insee", "ign", "inpn", "mnhn", "georisques", "brgm", "meteo-france",
    "meteo france", "geoportail", "etalab", "dgfip", "sirene", "cerema",
    "ifremer", "dreal", "ddtm", "prefecture", "agglomeration", "agglo",
    "smbt", "agence de l'eau", "open-meteo", "copernicus", "usgs", "nasa",
    "inpi", "legifrance", "journal officiel", "anses", "santé publique france",
)

BLOQUANT = "bloquant"
SIGNALEMENT = "signalement"


def _sources(rec: dict) -> list[str]:
    """Toutes les sources citées, sous forme de chaînes minuscules."""
    out = []
    s = rec.get("source")
    if isinstance(s, str) and s.strip():
        out.append(s.strip().lower())
    for x in (rec.get("sources") or []):
        if isinstance(x, str) and x.strip():
            out.append(x.strip().lower())
    # dédoublonnage en conservant l'ordre
    return list(dict.fromkeys(out))


def _officielle(sources: list[str], liste=None) -> bool:
    # la liste est enrichissable dans la config de l'OS
    # (admissibilite.sources_officielles) sans redeployer
    motifs = liste if liste else SOURCES_OFFICIELLES
    return any(any(o in s for o in motifs) for s in sources)


def _texte(rec) -> str:
    """Tout ce qui est texte dans l'enregistrement, pour y chercher du PII."""
    out = []
    for k, v in rec.items():
        if isinstance(v, str):
            out.append(f"{k}={v}")
        elif isinstance(v, (list, tuple)):
            out.extend(str(x) for x in v if isinstance(x, str))
    return "\n".join(out)


def admissible(rec: dict, config: dict | None = None) -> tuple[bool, list[dict]]:
    """Un enregistrement est-il présentable tel quel ?

    Renvoie (présentable, problèmes). Un seul problème `bloquant` suffit à
    interdire la présentation ; un `signalement` doit être affiché avec
    l'enregistrement, jamais à sa place.
    """
    problemes = []

    def ajouter(regle, gravite, message):
        problemes.append({"regle": regle, "gravite": gravite, "message": message})

    statut = rec.get("status") or rec.get("statut") or "unknown"

    # 1. Un fait sans source n'est pas un fait.
    if statut == "fact" and not (rec.get("source") or "").strip():
        ajouter("fait_sans_source", BLOQUANT,
                "présenté comme un fait mais aucune source : c'est au mieux "
                "une opinion, au pire une invention")

    # 1 bis. Le critère du « fait vérifié » (méthode Frontignan) : croisé ≥ 2
    #        sources indépendantes, ou une source officielle primaire.
    #        Une seule source non officielle ne porte pas un fait vérifié.
    sources = _sources(rec)
    cfg_adm = (config or {}).get("admissibilite") or {}
    liste_off = cfg_adm.get("sources_officielles")
    if (statut == "fact" and cfg_adm.get("signaler_fait_non_croise", True)
            and len(sources) < 2 and not _officielle(sources, liste_off)):
        ajouter("fait_non_croise", SIGNALEMENT,
                f"une seule source ({sources[0] if sources else 'aucune'}) et "
                f"aucun producteur public reconnu : le critère du fait vérifié "
                f"demande 2 sources indépendantes ou une source officielle primaire")

    # 2. Une observation ne porte jamais de champ d'estimation.
    presents = [c for c in CHAMPS_ESTIMATION if c in rec]
    if statut == "fact" and presents:
        ajouter("fait_estime", BLOQUANT,
                f"présenté comme un fait mais porte un champ d'estimation "
                f"({', '.join(presents)}) : une estimation n'est pas une "
                f"observation")

    # 3. Un chiffre sans unité est un score nu.
    if isinstance(rec.get("valeur"), (int, float)) and not (rec.get("unite") or "").strip():
        ajouter("score_nu", BLOQUANT,
                "valeur numérique sans unité : un nombre nu se lit comme une "
                "mesure et n'en est pas une")

    # 4. Aucun identifiant civil.
    texte = _texte(rec)
    for nom, motif in MOTIFS_PII:
        if motif.search(texte):
            ajouter("donnee_personnelle", BLOQUANT,
                    f"contient ce qui ressemble à un {nom} : aucune donnée "
                    f"personnelle ne doit entrer dans le registre")

    # 5. Une inférence ou une hypothèse sans base n'est pas recevable.
    if statut in ("inference", "hypothesis") and not (rec.get("source") or "").strip():
        ajouter("inference_sans_base", BLOQUANT,
                f"statut « {statut} » mais aucune source : même une hypothèse "
                f"doit dire d'où elle vient")

    # 6. Ce qui n'est pas un fait doit dire pourquoi.
    #    C'est la règle anti-« machine à convictions » : on n'affiche pas
    #    l'incertitude à la place de la réponse, on l'affiche avec.
    if statut in ("inference", "hypothesis", "unknown"):
        justification = (rec.get("note") or rec.get("justification") or
                         rec.get("pourquoi") or "").strip()
        if not justification:
            ajouter("incertitude_non_expliquee", SIGNALEMENT,
                    f"statut « {statut} » sans explication : le système ne dit "
                    f"pas pourquoi il n'est pas sûr")

    bloque = any(p["gravite"] == BLOQUANT for p in problemes)
    return (not bloque), problemes


def filtrer_enregistrements(enregistrements: list[dict]) -> dict:
    """Passe une liste au crible. Renvoie le tri, pas une note.

    Le but n'est pas de noter les données, c'est de savoir lesquelles on peut
    mettre dans un document remis à une collectivité.
    """
    conformes, bloques, signalements = [], [], []
    for r in enregistrements:
        ok, problemes = admissible(r)
        (conformes if ok else bloques).append(r)
        for p in problemes:
            if p["gravite"] == SIGNALEMENT and r not in signalements:
                signalements.append(r)
    return {
        "total": len(enregistrements),
        "conformes": conformes,
        "bloques": bloques,
        "signalements": signalements,
        "par_regle": _compter(enregistrements),
        "presentable": not bloques,
    }


def _compter(enregistrements: list[dict]) -> dict:
    compte = {}
    for r in enregistrements:
        for p in admissible(r)[1]:
            compte[p["regle"]] = compte.get(p["regle"], 0) + 1
    return compte
