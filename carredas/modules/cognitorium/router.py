"""Routes du module Cognitorium : profils + état de l'art.

Deux choses vivent ici :
  * les **profils** — individus, structures, partenaires. Un profil est une fiche
    volontairement sobre : ce qu'on sait, d'où ça vient, quand on l'a vérifié.
    Rien de plus. C'est le module « personnel » du projet, et il alimente les
    participants d'une réunion.
  * les **références** — l'état de l'art. L'indexeur sait parcourir les dossiers
    déjà dans le dépôt (COGNITORIUM, psychologie, mémoires) pour en faire une
    bibliothèque interrogeable.
"""

from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path

from ...httpsrv import Response
from ...store import new_id, slug

PREFIX = "/api/cognitorium"
TYPES = ("individu", "structure", "partenaire")


def _norm(t: str) -> str:
    return re.sub(r"\s+", " ", str(t or "")).strip().lower()


def canonique(store, config=None):
    """Profils d'individus, structures et partenaires."""
    from ...core import canonical
    return [canonical.depuis_profil(p) for p in store.all("profils")]


def register(router, ctx):
    store = ctx["store"]
    broadcast = ctx.get("broadcast") or (lambda *a, **k: None)

    # ------------------------------------------------------------------ profils
    @router.get(PREFIX + "/profils")
    def lister(req):
        q = _norm(req.q("q"))
        type_ = req.q("type") or ""
        out = []
        for p in store.all("profils"):
            if type_ and p.get("type") != type_:
                continue
            if q and q not in _norm(" ".join([
                    p.get("nom", ""), p.get("prenom", ""), p.get("structure", ""),
                    p.get("role", ""), " ".join(p.get("tags") or [])])):
                continue
            out.append(p)
        return {"profils": out, "total": len(out)}

    @router.post(PREFIX + "/profils")
    def creer(req):
        p = req.json()
        t = p.get("type") or "individu"
        if t not in TYPES:
            return Response.error(f"type invalide : {t}", 400)
        if not (p.get("nom") or "").strip() and not (p.get("prenom") or "").strip():
            return Response.error("nom ou prénom obligatoire", 400)
        pid = p.get("id") or new_id(t[:3])
        rec = {
            "id": pid, "type": t,
            "nom": (p.get("nom") or "").strip(), "prenom": (p.get("prenom") or "").strip(),
            "role": (p.get("role") or "").strip(),
            "structure": (p.get("structure") or "").strip(),
            "commune": (p.get("commune") or "").strip(),
            "courriel": (p.get("courriel") or "").strip(),
            "telephone": (p.get("telephone") or "").strip(),
            "tags": [str(x) for x in (p.get("tags") or []) if str(x).strip()],
            "notes": p.get("notes") or [],
            "liens": p.get("liens") or [],
            "verifie_le": p.get("verifie_le") or "",
            "confiance": p.get("confiance") or "à vérifier",
            "cree_le": _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        }
        store.put("profils", pid, rec)
        broadcast("cognitorium", {"kind": "profil", "nom": f"{rec['prenom']} {rec['nom']}".strip()})
        return {"profil": rec}

    @router.get(PREFIX + "/profils/:pid")
    def lire(req, pid):
        p = store.get("profils", pid)
        if not p:
            return Response.not_found("profil inconnu")
        # ce qu'on sait de cette personne dans les réunions
        lieux = []
        for s in store.all("reunions"):
            if any(pid == x or _norm(x) == _norm(f"{p.get('prenom','')} {p.get('nom','')}")
                   for x in (s.get("participants") or [])):
                lieux.append({"id": s.get("id"), "titre": s.get("titre"),
                              "date": s.get("date")})
            for a in (s.get("actions") or []):
                if _norm(a.get("responsable", "")) == _norm(f"{p.get('prenom','')} {p.get('nom','')}"):
                    lieux.append({"id": s.get("id"), "titre": s.get("titre"),
                                  "date": s.get("date"), "action": a.get("texte")})
        return {"profil": p, "apparitions": lieux}

    @router.put(PREFIX + "/profils/:pid")
    def maj(req, pid):
        if not store.get("profils", pid):
            return Response.not_found("profil inconnu")
        patch = {k: v for k, v in (req.json() or {}).items() if k != "id"}
        return {"profil": store.update("profils", pid, patch)}

    @router.delete(PREFIX + "/profils/:pid")
    def supprimer(req, pid):
        return {"ok": store.delete("profils", pid)}

    @router.post(PREFIX + "/profils/:pid/notes")
    def ajouter_note(req, pid):
        p = store.get("profils", pid)
        if not p:
            return Response.not_found("profil inconnu")
        body = (req.json() or {})
        p.setdefault("notes", []).append({
            "t": _dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "texte": (body.get("texte") or "").strip(),
            "source": body.get("source") or "saisie",
        })
        store.put("profils", pid, p)
        return {"profil": p}

    # --------------------------------------------------------------- références
    @router.get(PREFIX + "/references")
    def refs(req):
        q = _norm(req.q("q"))
        domaine = req.q("domaine") or ""
        out = []
        for r in store.all("references"):
            if domaine and r.get("domaine") != domaine:
                continue
            if q and q not in _norm(" ".join([
                    r.get("titre", ""), r.get("resume", ""),
                    r.get("auteurs", ""), " ".join(r.get("mots_cles") or [])])):
                continue
            out.append(r)
        return {"references": out, "total": len(out)}

    @router.post(PREFIX + "/references")
    def ajouter_ref(req):
        p = req.json()
        rid = p.get("id") or new_id("ref")
        rec = {
            "id": rid,
            "titre": (p.get("titre") or "").strip() or "Sans titre",
            "auteurs": p.get("auteurs") or "",
            "annee": p.get("annee") or "",
            "domaine": p.get("domaine") or "général",
            "type": p.get("type") or "document",
            "source": p.get("source") or "saisie",
            "url": p.get("url") or "",
            "chemin": p.get("chemin") or "",
            "resume": p.get("resume") or "",
            "mots_cles": [str(x) for x in (p.get("mots_cles") or []) if str(x).strip()],
            "statut": p.get("statut") or "à lire",
            "confiance": p.get("confiance") or "",
            "taille": p.get("taille") or 0,
            "cree_le": _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        }
        store.put("references", rid, rec)
        return {"reference": rec}

    @router.delete(PREFIX + "/references/:rid")
    def supprimer_ref(req, rid):
        return {"ok": store.delete("references", rid)}

    # ------------------------------------------------------------------ indexeur
    @router.post(PREFIX + "/indexer")
    def indexer(req):
        """Parcourt un dossier du dépôt et en fait des références interrogeables."""
        p = req.json() or {}
        racine = Path(p.get("racine") or ".")
        if not racine.is_absolute():
            racine = Path(__file__).resolve().parents[3] / racine
        if not racine.exists():
            return Response.error(f"dossier introuvable : {racine}", 404)
        exts = {".pdf", ".md", ".txt", ".html", ".htm", ".json", ".csv",
                ".doc", ".docx", ".xls", ".xlsm", ".pptx"}
        domaine = p.get("domaine") or racine.name
        maxi = int(p.get("max") or 500)
        ajoutees, maj = 0, 0
        existants = {r.get("chemin"): r for r in store.all("references")}
        for f in sorted(racine.rglob("*")):
            if ajoutees + maj >= maxi:
                break
            if not f.is_file() or f.suffix.lower() not in exts:
                continue
            if any(x.startswith((".", "_")) for x in f.parts):
                continue
            try:
                rel = str(f.relative_to(Path(__file__).resolve().parents[3]))
            except Exception:
                rel = str(f)
            if rel in existants:
                maj += 1
                continue
            titre = re.sub(r"[_\-]+", " ", f.stem).strip()
            store.put("references", new_id("ref"), {
                "id": new_id("ref"), "titre": titre[:180], "auteurs": "",
                "annee": "", "domaine": domaine, "type": f.suffix.lstrip(".").lower(),
                "source": "indexeur", "url": "", "chemin": rel, "resume": "",
                "mots_cles": [domaine], "statut": "à lire", "confiance": "",
                "taille": f.stat().st_size,
                "cree_le": _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            })
            ajoutees += 1
        return {"ajoutees": ajoutees, "deja_presentes": maj,
                "racine": str(racine), "domaine": domaine,
                "total": len(store.all("references"))}

    # ------------------------------------------------------------------ recherche
    @router.get(PREFIX + "/recherche")
    def recherche(req):
        """Recherche transverse : profils, références, réunions."""
        q = _norm(req.q("q"))
        if len(q) < 2:
            return {"resultats": []}
        out = []
        for p in store.all("profils"):
            blob = _norm(" ".join([p.get("nom", ""), p.get("prenom", ""),
                                   p.get("structure", ""), p.get("role", "")]))
            if q in blob:
                out.append({"type": "profil", "id": p["id"],
                            "titre": f"{p.get('prenom','')} {p.get('nom','')}".strip()
                                     or p.get("structure", ""),
                            "detail": p.get("role") or p.get("structure") or ""})
        for r in store.all("references"):
            if q in _norm(r.get("titre", "") + " " + r.get("resume", "")):
                out.append({"type": "reference", "id": r["id"],
                            "titre": r.get("titre", ""),
                            "detail": r.get("chemin") or r.get("url") or ""})
        for s in store.all("reunions"):
            if q in _norm(s.get("titre", "")):
                out.append({"type": "reunion", "id": s["id"],
                            "titre": s.get("titre", ""),
                            "detail": s.get("date", "")})
        return {"resultats": out[:60], "total": len(out)}

    # ---------------------------------------------------------- annuaire réunion
    @router.get(PREFIX + "/annuaire")
    def annuaire(req):
        """Noms à proposer comme participants, avec leur structure."""
        vus = {}
        for s in store.all("reunions"):
            for x in (s.get("participants") or []):
                vus.setdefault(str(x).strip(), 0)
                vus[str(x).strip()] += 1
        out = [{"nom": n, "reunions": c, "profil": _trouver_profil(store, n)}
               for n, c in sorted(vus.items(), key=lambda kv: -kv[1])]
        for p in store.all("profils"):
            nom = f"{p.get('prenom','')} {p.get('nom','')}".strip()
            if nom and nom not in vus:
                out.append({"nom": nom, "reunions": 0, "profil": p["id"]})
        return {"annuaire": out}

    def _trouver_profil(store, nom):
        for p in store.all("profils"):
            if _norm(f"{p.get('prenom','')} {p.get('nom','')}") == _norm(nom):
                return p["id"]
            if p.get("structure") and _norm(p["structure"]) == _norm(nom):
                return p["id"]
        return None
