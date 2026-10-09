# -*- coding: utf-8 -*-
"""Extraction déterministe (sans modèle) depuis une prise de parole.

C'est le **plancher de service** : quoi qu'il arrive — pas de réseau, pas de GPU,
pas de clé d'API, modèle indisponible — ce module doit sortir quelque chose
d'exploitable. Le modèle, quand il est là, vient *enrichir* ce résultat, jamais
le remplacer.

Sortie : une liste de suggestions
    {"id", "kind": "decision|action|risque|question",
     "texte", "responsable", "echeance", "montant", "confiance", "source"}
"""

from __future__ import annotations

import datetime as _dt
import re
import unicodedata

# ------------------------------------------------------------------ marqueurs

DECISION = [
    r"on décide", r"il est décidé", r"décision\s*:", r"on valide", r"on retient",
    r"on acte", r"acté", r"on approuve", r"approuvé", r"adopté", r"on adopte",
    r"il est convenu", r"on part sur", r"on est d'accord", r"accord pour",
    r"validé", r"on confirme", r"entériné", r"arbitrage\s*:", r"tranché",
]
ACTION = [
    r"il faut", r"il faudra", r"il faudrait", r"on doit", r"on devra",
    r"on va devoir", r"à faire", r"je vais", r"je vais devoir", r"tu vas",
    r"nous allons", r"on va", r"prévoir", r"préparer", r"envoyer", r"rédiger",
    r"relancer", r"contacter", r"chiffrer", r"consulter", r"déposer",
    r"vérifier", r"mettre à jour", r"organiser", r"convoquer", r"transmettre",
    r"commander", r"réceptionner", r"programmer", r"planifier", r"solliciter",
    r"saisir", r"notifier", r"publier", r"recueillir", r"mobiliser",
]
RISQUE = [
    r"risque", r"problème", r"bloqué", r"blocage", r"attention", r"vigilance",
    r"danger", r"alerte", r"retard", r"litige", r"contentieux", r"réserve",
    r"point dur", r"sous réserve", r"à surveiller", r"fragile",
]
QUESTION = [r"\?", r"^comment\b", r"^pourquoi\b", r"^qui\b", r"^quand\b",
            r"^qu'est-ce", r"^est-ce que"]

MOIS = {
    "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5,
    "juin": 6, "juillet": 7, "août": 8, "aout": 8, "septembre": 9, "octobre": 10,
    "novembre": 11, "décembre": 12, "decembre": 12,
}
JOURS = {"lundi": 0, "mardi": 1, "mercredi": 2, "jeudi": 3, "vendredi": 4,
         "samedi": 5, "dimanche": 6}
_MOIS_RX = r"(?:janvier|février|fevrier|mars|avril|mai|juin|juillet|août|aout|septembre|octobre|novembre|décembre|decembre)"

_RE_MONTANT = re.compile(
    r"(?P<n>\d{1,3}(?:[ \u00a0]\d{3})*(?:[.,]\d{1,2})?|\d+(?:[.,]\d{1,2})?)\s*"
    r"(?P<u>k€|ke|m€|me|millions?\s*d['’]euros?|millier?s?\s*d['’]euros?|€|euros?)",
    re.I)


def _norm(t: str) -> str:
    t = unicodedata.normalize("NFKC", str(t or ""))
    return re.sub(r"\s+", " ", t.replace("\u00a0", " ")).strip()


def memo(s: str) -> str:
    """Phrase courte, nettoyée, présentable dans un document."""
    s = _norm(s)
    if not s:
        return ""
    s = re.sub(r"^(du coup|donc|alors|en fait|bon|voilà|eh bien|ben)\s+", "", s, flags=re.I)
    s = s[0].upper() + s[1:] if s else s
    if len(s) > 240:
        s = s[:237].rsplit(" ", 1)[0] + "…"
    if s and s[-1] not in ".!?:;":
        s += "."
    return s


# -------------------------------------------------------------------- échéance


def parse_echeance(texte: str, ref: _dt.date | None = None) -> str | None:
    """Cherche une échéance en français ; rend une date ISO ou None."""
    ref = ref or _dt.date.today()
    t = " " + _norm(texte).lower() + " "

    m = re.search(rf"(\d{{1,2}})(?:er)?\s+{_MOIS_RX}\s*(\d{{4}})?", t)
    if m:
        j, mo, an = int(m.group(1)), MOIS.get(m.group(2)), m.group(3)
        an = int(an) if an else ref.year
        try:
            d = _dt.date(an, mo, j)
            if d < ref and not m.group(3):
                d = _dt.date(an + 1, mo, j)
            return d.isoformat()
        except Exception:
            pass

    m = re.search(r"(\d{1,2})[/.\-](\d{1,2})(?:[/.\-](\d{2,4}))?", t)
    if m:
        j, mo = int(m.group(1)), int(m.group(2))
        an = m.group(3)
        an = (2000 + int(an)) if an and len(an) == 2 else (int(an) if an else ref.year)
        try:
            d = _dt.date(an, mo, j)
            if d < ref and not m.group(3):
                d = _dt.date(an + 1, mo, j)
            return d.isoformat()
        except Exception:
            pass

    m = re.search(r"(?:sous|dans|d'ici)\s+(\d{1,3})\s*(jour|semaine|mois|an)s?", t)
    if m:
        n, u = int(m.group(1)), m.group(2)
        delta = {"jour": 1, "semaine": 7, "mois": 30, "an": 365}[u] * n
        return (ref + _dt.timedelta(days=delta)).isoformat()

    if re.search(r"\bdemain\b", t):
        return (ref + _dt.timedelta(days=1)).isoformat()
    if re.search(r"\baprès[- ]demain\b", t):
        return (ref + _dt.timedelta(days=2)).isoformat()

    m = re.search(rf"(?:semaine|lundi|mardi|mercredi|jeudi|vendredi)\s+prochain", t)
    if m:
        return (ref + _dt.timedelta(days=7)).isoformat()
    m = re.search(rf"({ '|'.join(JOURS) })\s+prochain", t)
    if m:
        cible = JOURS[m.group(1)]
        avance = (cible - ref.weekday()) % 7 or 7
        return (ref + _dt.timedelta(days=avance + 7)).isoformat()
    m = re.search(rf"\b({'|'.join(JOURS)})\b", t)
    if m:
        cible = JOURS[m.group(1)]
        avance = (cible - ref.weekday()) % 7 or 7
        return (ref + _dt.timedelta(days=avance)).isoformat()

    m = re.search(rf"fin\s+({_MOIS_RX})", t)
    if m:
        mo = MOIS[m.group(1)]
        an = ref.year if mo >= ref.month else ref.year + 1
        dernier = [31, 29 if an % 4 == 0 and (an % 100 or an % 400 == 0) else 28,
                   31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mo - 1]
        return _dt.date(an, mo, dernier).isoformat()

    m = re.search(rf"(?:mi|début)\s+({_MOIS_RX})", t)
    if m:
        mo = MOIS[m.group(1)]
        an = ref.year if mo >= ref.month else ref.year + 1
        return _dt.date(an, mo, 15 if "mi" in m.group(0) else 1).isoformat()

    for mot, delta in (("fin d'année", (12, 31)), ("fin du mois", None)):
        if mot in t:
            if delta:
                return _dt.date(ref.year, 12, 31).isoformat()
            premier_suivant = _dt.date(ref.year + (ref.month == 12), (ref.month % 12) + 1, 1)
            return (premier_suivant - _dt.timedelta(days=1)).isoformat()
    return None


def montants(texte: str) -> list[dict]:
    out = []
    for m in _RE_MONTANT.finditer(_norm(texte)):
        try:
            n = float(m.group("n").replace(" ", "").replace(",", "."))
        except Exception:
            continue
        u = m.group("u").lower()
        if u.startswith(("m€", "me", "million")):
            n *= 1_000_000
        elif u.startswith(("k€", "ke", "millier")):
            n *= 1_000
        if n <= 0:
            continue
        out.append({"montant": round(n, 2), "brut": m.group(0).strip()})
    return out


# -------------------------------------------------------------- responsable


def _connus(participants: list[str]) -> list[str]:
    return [p for p in (participants or []) if p and len(p) > 2]


# Un nom suivi de l'un de ces verbes désigne la personne qui porte l'action.
_VERBE_ACTION = (r"(?:vais|va|vas|doit|dois|devra|devrait|prend|prends|prendra|"
                 r"s'occupe|s'en occupe|se charge|se chargera|pilote|pilotera|"
                 r"porte|portera|prépare|préparera|rédige|rédigera|envoie|enverra|"
                 r"chiffre|chiffrera|anime|animera|suit|suivra|coordonne|"
                 r"coordonnera|transmet|transmettra|vérifie|vérifiera|recueille|"
                 r"mobilise|sollicite|notifie|publie)")


def trouver_responsable(texte: str, locuteur: str = "", participants=None) -> str | None:
    t = _norm(texte)
    m = re.search(r"@([A-Za-zÀ-ÿ][\wÀ-ÿ'’\- ]{1,30})", t)
    if m:
        return m.group(1).strip(" .,:;")

    for p in _connus(participants):
        nom = re.escape(_norm(p))
        if not re.search(rf"\b{nom}\b", t, re.I):
            continue
        if re.search(rf"{nom}\s+{_VERBE_ACTION}\b", t, re.I):
            return p
        if re.search(rf"(?:confier|confié|confiée|donner|donné|donnée|attribuer|"
                     rf"attribué|attribuée|charger|chargé|chargée)\s+"
                     rf"(?:à|au|aux)\s+{nom}\b", t, re.I):
            return p
        # « X : … » ou « X s'en occupe » en tête de phrase
        if re.search(rf"^{nom}\s*[:,]", t, re.I):
            return p

    if re.search(r"\b(je vais|je m'en occupe|je m'occupe|je prends|je prépare)\b", t, re.I):
        return locuteur or ""
    return ""


# -------------------------------------------------------------- suggestions


def _kind_of(phrase: str) -> tuple[str, float]:
    t = " " + phrase.lower() + " "
    score = {"decision": 0.0, "action": 0.0, "risque": 0.0, "question": 0.0}
    for pat in DECISION:
        if re.search(pat, t):
            score["decision"] += 0.5
    for pat in ACTION:
        if re.search(pat, t):
            score["action"] += 0.35
    for pat in RISQUE:
        if re.search(pat, t):
            score["risque"] += 0.45
    for pat in QUESTION:
        if re.search(pat, t):
            score["question"] += 0.3
    if re.search(r"\d", phrase):
        score["action"] += 0.05
    best = max(score, key=score.get)
    return best, round(min(score[best], 1.0), 2)


# Le point d'une civilité (« M. », « Mme. ») n'est pas une fin de phrase :
# sans cette précaution, « …, M. Martin va piloter » est coupé en deux et le
# responsable part avec le morceau de phrase suivant.
_CIVILITES = r"(?:M|Mme|Mlle|Me|Dr|Pr|MM|Mmes|Mlles|Cie|Ste|Ets)"
_MARQUE_POINT = "\u0001"
_SPLIT = re.compile(r"(?<=[.!?;])\s+|\s+--\s+|\s+•\s+")


def segmenter(texte: str) -> list[str]:
    """Découpe une prise de parole en phrases exploitables."""
    t = _norm(texte)
    if not t:
        return []
    t = re.sub(rf"\b{_CIVILITES}\.", lambda m: m.group(0)[:-1] + _MARQUE_POINT, t)
    parts = _SPLIT.split(t)
    return [p.replace(_MARQUE_POINT, ".").strip(" -–:;,.")
            for p in parts if len(p.strip()) > 2]


def suggerer(texte: str, locuteur: str = "", participants=None,
             ref: _dt.date | None = None, origine: str = "prise") -> list[dict]:
    """Extrait les suggestions d'une prise de parole (ou d'une note)."""
    out = []
    for phrase in segmenter(texte):
        if len(phrase) < 12:
            continue
        kind, conf = _kind_of(phrase)
        if conf <= 0:
            continue
        echeance = parse_echeance(phrase, ref)
        resp = trouver_responsable(phrase, locuteur, participants)
        monts = montants(phrase)
        # une échéance ou un responsable renforce nettement la confiance
        conf = round(min(1.0, conf + (0.2 if echeance else 0) + (0.15 if resp else 0)), 2)
        out.append({
            "kind": kind,
            "texte": memo(phrase),
            "responsable": resp or "",
            "echeance": echeance or "",
            "montant": (monts[0]["montant"] if monts else None),
            "confiance": conf,
            "origine": origine,
            "brut": phrase,
        })
    # dédoublonnage approximatif
    vus, uniq = set(), []
    for s in out:
        k = re.sub(r"[^a-z0-9]", "", s["texte"].lower())[:70]
        if k in vus:
            continue
        vus.add(k)
        uniq.append(s)
    return uniq
