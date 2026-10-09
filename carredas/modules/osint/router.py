"""Routes du module OSINT.

Trois niveaux, dans cet ordre :
  1. le **registre d'outils** — ce qui existe, ce que ça vaut, sous quelle licence,
     avec quel risque. Rien n'est lancé depuis l'application : on décrit, on
     documente, on prépare la commande, on ne l'exécute jamais en douce.
  2. les **cas** — une investigation = une question, un périmètre, un cadre.
  3. la **chaîne de preuves** — chaque élément collecté porte sa source, sa date,
     son mode de collecte et son niveau de confiance. C'est ce qui distingue une
     note utilisable d'un dossier qu'on ne peut pas défendre.
"""

from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

from ... import docsgen
from ...httpsrv import Response
from ...store import new_id

PREFIX = "/api/osint"
ICI = Path(__file__).parent

FIABILITE = [
    {"id": "A", "nom": "Source officielle / primaire", "exemple": "JOAFE, INSEE, Géorisques, délibération"},
    {"id": "B", "nom": "Source secondaire fiable", "exemple": "presse de référence, rapport institutionnel"},
    {"id": "C", "nom": "Source secondaire à corroborer", "exemple": "agrégateur, base contributive"},
    {"id": "D", "nom": "Source anonyme ou non vérifiée", "exemple": "réseau social, forum"},
    {"id": "X", "nom": "Non évalué", "exemple": "à classer avant restitution"},
]


def _lire(nom, defaut=None):
    p = ICI / "data" / nom
    if not p.exists():
        return defaut if defaut is not None else {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return defaut if defaut is not None else {}


def register(router, ctx):
    store = ctx["store"]
    data = _lire("outils.json", {"categories": [], "outils": [], "meta": {}})
    broadcast = ctx.get("broadcast") or (lambda *a, **k: None)

    # -------------------------------------------------------------- registre
    @router.get(PREFIX + "/categories")
    def categories(req):
        out = []
        for c in data.get("categories", []):
            d = dict(c)
            d["nb"] = len([o for o in data.get("outils", []) if o.get("categorie") == c["id"]])
            out.append(d)
        return {"categories": out}

    @router.get(PREFIX + "/outils")
    def outils(req):
        cat = req.q("categorie") or ""
        q = (req.q("q") or "").strip().lower()
        risque = req.q("risque") or ""
        out = []
        for o in data.get("outils", []):
            if cat and o.get("categorie") != cat:
                continue
            if risque and o.get("risque") != risque:
                continue
            if q and q not in (o.get("nom", "") + o.get("description", "") +
                               o.get("usage", "")).lower():
                continue
            out.append(o)
        return {"outils": out, "total": len(out), "meta": data.get("meta", {}),
                "fiabilite": FIABILITE}

    @router.get(PREFIX + "/outils/:oid")
    def outil(req, oid):
        for o in data.get("outils", []):
            if o.get("id") == oid:
                return {"outil": o}
        return Response.not_found("outil inconnu")

    @router.get(PREFIX + "/cadre")
    def cadre(req):
        return {"cadre_legal": data.get("meta", {}).get("cadre_legal", []),
                "fiabilite": FIABILITE}

    # ------------------------------------------------------------------- cas
    @router.get(PREFIX + "/cas")
    def lister_cas(req):
        return {"cas": store.all("osintcas")}

    @router.post(PREFIX + "/cas")
    def creer_cas(req):
        p = req.json()
        cid = p.get("id") or new_id("cas")
        rec = {
            "id": cid,
            "titre": (p.get("titre") or "Investigation sans titre").strip(),
            "question": (p.get("question") or "").strip(),
            "objet": (p.get("objet") or "").strip(),
            "perimetre": (p.get("perimetre") or "").strip(),
            "cadre": (p.get("cadre") or "données publiques uniquement").strip(),
            "statut": p.get("statut") or "ouvert",
            "responsable": (p.get("responsable") or "").strip(),
            "preuves": [],
            "notes": [],
            "cree_le": _dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        store.put("osintcas", cid, rec)
        broadcast("osint", {"kind": "cas", "titre": rec["titre"]})
        return {"cas": rec}

    @router.get(PREFIX + "/cas/:cid")
    def lire_cas(req, cid):
        c = store.get("osintcas", cid)
        return {"cas": c} if c else Response.not_found("cas inconnu")

    @router.put(PREFIX + "/cas/:cid")
    def maj_cas(req, cid):
        if not store.get("osintcas", cid):
            return Response.not_found("cas inconnu")
        return {"cas": store.update("osintcas", cid,
                                    {k: v for k, v in (req.json() or {}).items() if k != "id"})}

    @router.delete(PREFIX + "/cas/:cid")
    def supprimer_cas(req, cid):
        return {"ok": store.delete("osintcas", cid)}

    # --------------------------------------------------------------- preuves
    @router.post(PREFIX + "/cas/:cid/preuve")
    def ajouter_preuve(req, cid):
        c = store.get("osintcas", cid)
        if not c:
            return Response.not_found("cas inconnu")
        p = req.json() or {}
        if not (p.get("source") or "").strip():
            return Response.error("une preuve sans source n'est pas une preuve", 400)
        prev = {
            "id": new_id("prv"),
            "titre": (p.get("titre") or "").strip() or "Élément",
            "contenu": (p.get("contenu") or "").strip(),
            "source": (p.get("source") or "").strip(),
            "url": (p.get("url") or "").strip(),
            "outil": (p.get("outil") or "saisie").strip(),
            "collecte_le": (p.get("collecte_le") or _dt.datetime.now().strftime("%Y-%m-%d %H:%M")),
            "collecte_par": (p.get("collecte_par") or "").strip(),
            "fiabilite": (p.get("fiabilite") or "X").upper(),
            "confiance": (p.get("confiance") or "moyenne"),
            "contredit": (p.get("contredit") or "").strip(),
            "tags": [str(x) for x in (p.get("tags") or []) if str(x).strip()],
        }
        c.setdefault("preuves", []).append(prev)
        store.put("osintcas", cid, c)
        return {"preuve": prev, "cas": c}

    @router.delete(PREFIX + "/cas/:cid/preuve/:pid")
    def supprimer_preuve(req, cid, pid):
        c = store.get("osintcas", cid)
        if not c:
            return Response.not_found("cas inconnu")
        n = len(c.get("preuves") or [])
        c["preuves"] = [x for x in c["preuves"] if x.get("id") != pid]
        store.put("osintcas", cid, c)
        return {"ok": len(c["preuves"]) < n}

    # -------------------------------------------------------- note de synthèse
    @router.post(PREFIX + "/cas/:cid/generer")
    def generer(req, cid):
        c = store.get("osintcas", cid)
        if not c:
            return Response.not_found("cas inconnu")
        p = req.json() or {}
        fmt = (p.get("format") or "html").lower()

        prev = sorted(c.get("preuves") or [], key=lambda x: x.get("collecte_le", ""))
        par_fiab = {}
        for x in prev:
            par_fiab.setdefault(x.get("fiabilite", "X"), []).append(x)

        blocs = [
            {"type": "h2", "texte": "Question posée"},
            {"type": "p", "texte": c.get("question") or c.get("titre")},
            {"type": "kv", "items": [
                ["Objet", c.get("objet") or "—"],
                ["Périmètre", c.get("perimetre") or "—"],
                ["Cadre de collecte", c.get("cadre") or "—"],
                ["Responsable", c.get("responsable") or "—"],
            ]},
        ]
        if prev:
            blocs.append({"type": "h2", "texte": "Éléments recueillis"})
            blocs.append({"type": "table",
                          "entetes": ["Élément", "Source", "Outil", "Collecté le", "Fiabilité"],
                          "lignes": [[x.get("titre", ""), x.get("source", ""),
                                      x.get("outil", ""), x.get("collecte_le", ""),
                                      x.get("fiabilite", "X")] for x in prev]})
            for x in prev:
                if x.get("contenu"):
                    blocs.append({"type": "h3", "texte": x.get("titre", "")})
                    blocs.append({"type": "quote", "texte": x["contenu"]})
                    if x.get("contredit"):
                        blocs.append({"type": "note", "texte": "Élément contradictoire : " + x["contredit"]})
        else:
            blocs.append({"type": "note", "texte": "Aucun élément versé au dossier."})

        if par_fiab:
            blocs.append({"type": "h2", "texte": "Qualité des sources"})
            blocs.append({"type": "ul", "items": [
                f"{k} — {next((f['nom'] for f in FIABILITE if f['id'] == k), k)} : "
                f"{len(v)} élément(s)" for k, v in sorted(par_fiab.items())]})

        blocs.append({"type": "hr"})
        blocs.append({"type": "note",
                      "texte": "Collecte limitée aux données publiques, tracée et horodatée. "
                               "Toute donnée personnelle doit être supprimée dès qu'elle n'est "
                               "plus nécessaire à la finalité poursuivie (RGPD). Document de "
                               "travail — ne constitue pas une preuve au sens judiciaire."})

        doc = {"titre": f"Note — {c.get('titre','')}",
               "sous_titre": "Renseignement de sources ouvertes",
               "meta": {"Cas": c.get("id", ""), "Ouvert le": c.get("cree_le", ""),
                        "Éléments": str(len(prev)), "Statut": c.get("statut", "")},
               "blocs": blocs}

        data_, mime = docsgen.render(fmt, doc)
        nom = f"{_dt.datetime.now():%Y%m%d-%H%M%S}-osint-{c.get('id','')}.{fmt}"
        chemin = store.write_blob(nom, data_, "documents")
        return {"document": {"nom": nom, "fichier": str(chemin), "format": fmt,
                             "mime": mime, "taille": len(data_), "titre": doc["titre"]},
                "telechargement": f"/api/fichiers/{nom}"}

    # ---------------------------------------------------------- tableau de bord
    @router.get(PREFIX + "/tableau")
    def tableau(req):
        cas = store.all("osintcas")
        return {
            "outils": len(data.get("outils", [])),
            "categories": len(data.get("categories", [])),
            "cas_ouverts": len([c for c in cas if c.get("statut") != "clos"]),
            "preuves": sum(len(c.get("preuves") or []) for c in cas),
            "fiabilite": {f["id"]: sum(1 for c in cas for p in (c.get("preuves") or [])
                                       if p.get("fiabilite") == f["id"]) for f in FIABILITE},
        }
