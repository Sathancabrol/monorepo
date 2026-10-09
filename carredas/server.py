"""Assemblage de l'application : routes du cœur + branches de modules.

Le cœur ne sait rien des modules. Il fournit : la santé, la configuration, la
liste des modules, le téléchargement des fichiers générés, le flux d'événements
(SSE) et le journal. Tout le reste arrive par `modules.load_all`.
"""

from __future__ import annotations

import datetime as _dt
import json
import mimetypes
import queue
import threading
import time
from pathlib import Path

from . import __version__, httpsrv, log, paths
from .httpsrv import Response, Router
from .modules import load_all
from .store import Store

ICI = Path(__file__).resolve().parent


def build(config: dict | None = None, store: Store | None = None,
          verbose: bool = False) -> Router:
    cfg = config or paths.read_config()
    store = store or Store(paths.data_dir())
    log.configure(paths.data_dir() / "journal.jsonl",
                  "debug" if verbose else (cfg.get("journal", {}) or {}).get("niveau", "info"))

    from .llm import LLM
    llm = LLM(cfg)

    router = Router()

    # ----------------------------------------------------------- diffusion SSE
    abonnes: list = []

    def broadcast(canal: str, payload):
        rec = {"canal": canal, "t": _dt.datetime.now().strftime("%H:%M:%S"),
               "ts": time.time()}
        if isinstance(payload, dict):
            rec.update(payload)
        else:
            rec["donnees"] = payload
        for q in list(abonnes):
            try:
                q.put_nowait(rec)
            except Exception:
                pass

    log.on(lambda r: broadcast("journal", r))

    # ------------------------------------------------------------------- santé
    @router.get("/api/health")
    def sante(req):
        return {"ok": True, "version": __version__,
                "horloge": _dt.datetime.now().isoformat(timespec="seconds"),
                "donnees": str(store.root), "modele": llm.status()}

    @router.get("/api/infos")
    def infos(req):
        r = paths.runtime_info()
        r["version"] = __version__
        r["modules"] = [m["id"] for m in ctx["modules"]]
        r["url"] = ctx.get("url") or ""
        return r

    # ----------------------------------------------------------- configuration
    @router.get("/api/config")
    def lire_config(req):
        return {"config": cfg, "defaut": paths.DEFAULT_CONFIG}

    @router.get("/api/themes")
    def themes(req):
        """Les thèmes disponibles + le thème actif + les thèmes personnalisés."""
        import json as _json
        themes_path = paths.ui_dir() / "themes.json"
        try:
            data = _json.loads(themes_path.read_text(encoding="utf-8"))
        except Exception:
            data = {"themes": {}}
        ui = cfg.get("ui") or {}
        perso = ui.get("themes") or {}
        actif = ui.get("theme") or "nuit"
        # le thème actif peut être un thème perso (créé via le chat)
        variables = {}
        if actif in perso:
            variables = (perso[actif] or {}).get("variables") or {}
        elif actif in data["themes"]:
            variables = data["themes"][actif].get("variables") or {}
        # fond : la config (ui.fond) en priorité, puis le thème perso,
        # puis le thème prédéfini
        fond = ui.get("fond") \
            or ((perso.get(actif) or {}).get("fond")) \
            or ((data["themes"].get(actif) or {}).get("fond", ""))
        return {
            "themes": data["themes"],
            "personnalises": perso,
            "actif": actif,
            "fond": fond,
            "variables": variables,
        }

    @router.put("/api/config")
    def ecrire_config(req):
        from .llm import reset as llm_reset
        frag = req.json() or {}
        paths.patch_config(frag)
        # cfg est un dict partagé (ctx["config"] pointe dessus) :
        # clear+update met à jour la référence pour TOUT le monde,
        # y compris les routeurs qui ont capturé config = ctx["config"].
        cfg.clear()
        cfg.update(paths.read_config())
        llm_reset()
        log.info("serveur", "configuration mise à jour")
        return {"config": cfg}

    # ------------------------------------------------- garde-fou d'accès
    # Si un token est configuré (acces.token) et que la requête vient d'une
    # origine distante (Laplace sur téléphone/Discord), le token est exigé.
    # En local (127.0.0.1), jamais de token — l'app reste fluide.
    def _garde_acces(req):
        acces = (cfg.get("acces") or {})
        token = acces.get("token") or ""
        if not token:
            return None  # pas de token configuré = pas de vérification
        if not acces.get("exiger_token_si_distant", True):
            return None
        client = (req.client or "")
        if client in ("127.0.0.1", "::1", "localhost", ""):
            return None  # origine locale : jamais de token
        auth = (req.headers.get("Authorization") or "")
        fourni = auth[7:].strip() if auth.lower().startswith("bearer ") else ""
        if not fourni:
            fourni = req.q("token") or ""
        if fourni != token:
            return Response.error("token d'accès requis (Laplace)", 401)
        return None

    router.garde = _garde_acces

    # ---------------------------------------------------------------- modules
    ctx = {"store": store, "config": cfg, "llm": llm, "broadcast": broadcast,
           "engines": {}, "url": "", "modules": []}

    @router.get("/api/modules")
    def modules(req):
        return {"modules": ctx["modules"], "total": len(ctx["modules"])}

    # ------------------------------------------------- contrat de données partagé
    def _recs_canoniques() -> list:
        """Demande à chaque module ses objets dans la forme commune."""
        recs = []
        for mid, fournir in (ctx.get("canonique") or {}).items():
            try:
                for r in (fournir(store, cfg) or []):
                    r.setdefault("source", mid)
                    recs.append(r)
            except Exception as exc:
                log.warn("canonique", f"{mid} : {exc}")
        return recs

    @router.get("/api/canonique/schema")
    def canon_schema(req):
        from .core import canonical
        return {"schema": canonical.schema(),
                "module_schema": canonical.schema("module.schema.json"),
                "statuts": list(canonical.STATUTS),
                "marqueurs": canonical.MARQUEURS}

    @router.post("/api/canonique/valider")
    def canon_valider(req):
        """Forme d'abord, droit ensuite."""
        from .core import canonical
        from .core import admissibilite
        rec = req.json() or {}
        ok, erreurs = canonical.valider(rec)
        presentable, problemes = admissibilite.admissible(rec, cfg)
        return {"valide": ok, "erreurs": erreurs,
                "presentable": presentable, "problemes": problemes}

    @router.get("/api/canonique/admissibilite")
    def canon_admissibilite(req):
        """Lesquelles de nos données sont montrables à une collectivité.

        La question n'est pas « ai-je raison », c'est « ai-je le droit de
        présenter ça comme un fait ». Un seul motif bloquant suffit.
        """
        from .core import admissibilite
        recs = _recs_canoniques()
        r = admissibilite.filtrer_enregistrements(recs)
        return {
            "total": r["total"],
            "conformes": len(r["conformes"]),
            "bloques": len(r["bloques"]),
            "signalements": len(r["signalements"]),
            "par_regle": r["par_regle"],
            "presentable": r["presentable"],
            "detail": [{"id": x.get("id"), "label": x.get("label"),
                        "problemes": admissibilite.admissible(x, cfg)[1]}
                       for x in (r["bloques"] + r["signalements"])],
        }

    @router.get("/api/canonique")
    def canonique(req):
        """Toutes les données des modules, ramenées à une seule forme.

        C'est la démonstration du contrat : une décision de réunion, une preuve
        d'investigation, un point sur la carte et un profil deviennent le même
        type d'objet — avec leur origine intacte.
        """
        from .core import canonical
        recs = _recs_canoniques()
        valides, erreurs, par_type, par_statut = 0, [], {}, {}
        for r in recs:
            ok, err = canonical.valider(r)
            valides += ok
            if err and len(erreurs) < 20:
                erreurs.append({"id": r.get("id"), "erreurs": err})
            par_type[r.get("type", "?")] = par_type.get(r.get("type", "?"), 0) + 1
            par_statut[r.get("status", "?")] = par_statut.get(r.get("status", "?"), 0) + 1
        complet = req.q("complet") in ("1", "oui", "true")
        return {"total": len(recs), "valides": valides, "erreurs": erreurs,
                "par_type": par_type, "par_statut": par_statut,
                "enregistrements": recs if complet else recs[:60]}

    # ------------------------------------------------------- tableau de bord
    @router.get("/api/tableau")
    def tableau(req):
        """Synthèse inter-modules pour l'écran d'accueil."""
        out = {"reunions": {}, "carto": {}, "prevision": {}, "osint": {}, "profils": {}}
        try:
            eng = ctx["engines"].get("meeting")
            sessions = store.all("reunions")
            en_cours = [s for s in sessions if s.get("statut") == "en_cours"]
            out["reunions"] = {
                "total": len(sessions),
                "en_cours": len(en_cours),
                "en_cours_titre": (en_cours[0].get("titre") if en_cours else ""),
                "actions_ouvertes": sum(
                    len([a for a in (s.get("actions") or []) if a.get("statut") != "fait"])
                    for s in sessions),
                "decisions": sum(len(s.get("decisions") or []) for s in sessions),
                "documents": sum(len(s.get("documents") or []) for s in sessions),
            }
        except Exception:
            pass
        try:
            out["carto"] = {"points": len(store.all("cartopoints")),
                            "vues": len(store.all("cartovues")),
                            "annotations": len(store.all("cartoannot"))}
        except Exception:
            pass
        out["profils"] = {"total": len(store.all("profils")),
                          "references": len(store.all("references"))}
        out["osint"] = {"cas": len(store.all("osintcas")),
                        "preuves": sum(len(c.get("preuves") or [])
                                       for c in store.all("osintcas"))}
        out["prevision"] = {"scenarios": len(store.all("prevscen")),
                            "valeurs": len(store.all("prevvaleurs"))}
        out["documents"] = len(list((store.root / "_" / "documents").glob("*"))
                               ) if (store.root / "_" / "documents").exists() else 0
        return out

    # ------------------------------------------------------------- fichiers
    @router.get("/api/fichiers")
    def liste_fichiers(req):
        d = store.blob_dir("documents")
        out = []
        for p in sorted(d.glob("*"), key=lambda x: -x.stat().st_mtime):
            st = p.stat()
            out.append({"nom": p.name, "taille": st.st_mtime and p.stat().st_size,
                        "maj_le": _dt.datetime.fromtimestamp(st.st_mtime).strftime(
                            "%d/%m/%Y %H:%M"),
                        "url": f"/api/fichiers/{p.name}"})
        return {"fichiers": out[:200]}

    @router.get("/api/fichiers/:nom")
    def telecharger(req, nom):
        p = store.blob_dir("documents") / Path(nom).name
        if not p.exists():
            return Response.not_found("fichier absent")
        telecharger_ = (req.q("dl") or "") in ("1", "oui", "true")
        return Response.file(p, download_name=p.name, inline=not telecharger_)

    @router.delete("/api/fichiers/:nom")
    def supprimer_fichier(req, nom):
        p = store.blob_dir("documents") / Path(nom).name
        if p.exists():
            p.unlink()
            return {"ok": True}
        return Response.not_found("fichier absent")

    # ---------------------------------------------------------- journal & flux
    @router.get("/api/journal")
    def journal(req):
        return {"journal": log.recent(int(req.q("limite", 120)))}

    @router.get("/api/events")
    def events(req, emit):
        q: "queue.Queue" = queue.Queue(maxsize=200)
        abonnes.append(q)
        emit("ouvert", {"abonnes": len(abonnes)})
        try:
            while True:
                try:
                    rec = q.get(timeout=15)
                except queue.Empty:
                    emit("vivant", {"abonnes": len(abonnes)})
                    continue
                emit(rec.get("canal", "message"), rec)
        except Exception:
            pass
        finally:
            if q in abonnes:
                abonnes.remove(q)

    # ------------------------------------------------------------ mise à jour
    @router.get("/api/mise-a-jour")
    def maj(req):
        from . import updater
        return updater.verifier(cfg)

    @router.post("/api/mise-a-jour/appliquer")
    def appliquer(req):
        from . import updater
        p = req.json() or {}
        return updater.appliquer(cfg, version=p.get("version"),
                                 canal=p.get("canal") or cfg.get("mises_a_jour", {}).get("canal", "git"))

    @router.post("/api/mise-a-jour/annuler")
    def annuler(req):
        from . import updater
        return updater.annuler(cfg)

    # ------------------------------------------------------- sauvegarde locale
    @router.post("/api/sauvegarde")
    def sauvegarde(req):
        import shutil
        cible = paths.backups_dir() / f"donnees-{_dt.datetime.now():%Y%m%d-%H%M%S}"
        shutil.copytree(store.root, cible,
                        ignore=shutil.ignore_patterns("_*", "update", "backups"))
        return {"sauvegarde": str(cible)}

    @router.get("/api/sauvegardes")
    def sauvegardes(req):
        d = paths.backups_dir()
        return {"sauvegardes": [{"nom": p.name,
                                 "taille": sum(f.stat().st_size for f in p.rglob("*") if f.is_file())}
                                for p in sorted(d.iterdir()) if p.is_dir()]}

    # ----------------------------------------------------- câblage des modules
    ctx["modules"] = load_all(router, ctx)

    # -------------------------------------------------------------- interface
    # déclarée EN DERNIER : le fourre-tout statique ne doit jamais masquer
    # une route d'API, surtout celles ajoutées par les modules
    router.static("/", ICI / "ui", index="index.html", spa=False)
    log.info("serveur", f"prêt — {len(ctx['modules'])} module(s)")

    return router
