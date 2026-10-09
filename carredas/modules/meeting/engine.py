"""Moteur de réunion : l'état d'une session et tout ce qu'on peut en tirer.

Principe de fonctionnement pendant une réunion :
    1. quelqu'un parle (ou on tape une note)
    2. `pousser()` enregistre la phrase et lance les extracteurs
    3. les propositions tombent dans un **bac à suggestions**
    4. l'humain accepte d'un clic (ou à la voix) → ça devient décision / action
    5. à tout moment, `generer()` fabrique un document

Le bac à suggestions est volontairement central : un système agentique qui écrit
directement dans le compte rendu est un système qu'on n'ose pas utiliser en
réunion. Ici l'IA propose, l'humain dispose, et rien n'est jamais perdu.
"""

from __future__ import annotations

import datetime as _dt
import threading
import time

from ... import log
from ...store import new_id
from . import extract

COLLECTION = "reunions"

STATUTS = ("brouillon", "en_cours", "suspendu", "close")


def _maintenant() -> str:
    """Heure seule : pour l'affichage dans le fil de la réunion."""
    return _dt.datetime.now().strftime("%H:%M:%S")


def _instant() -> str:
    """Horodatage complet ISO : c'est celui qu'on doit stocker.

    Une décision ou une action doit pouvoir être datée dans l'absolu — sinon
    l'enregistrement canonique n'est pas valide et on perd la possibilité de
    reconstituer une chronologie.
    """
    return _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _session_vide(payload: dict) -> dict:
    now = _dt.datetime.now()
    return {
        "id": payload.get("id") or new_id("reu"),
        "titre": (payload.get("titre") or "Réunion sans titre").strip(),
        "date": payload.get("date") or now.strftime("%Y-%m-%d"),
        "heure": payload.get("heure") or now.strftime("%H:%M"),
        "lieu": payload.get("lieu") or "",
        "type": payload.get("type") or "réunion de travail",
        "contexte": payload.get("contexte") or "",
        "organisme": payload.get("organisme") or "",
        "ordre_du_jour": [str(x).strip() for x in (payload.get("ordre_du_jour") or []) if str(x).strip()],
        "participants": [str(x).strip() for x in (payload.get("participants") or []) if str(x).strip()],
        "statut": payload.get("statut") or "brouillon",
        "transcript": [],
        "notes": [],
        "decisions": [],
        "actions": [],
        "risques": [],
        "questions": [],
        "suggestions": [],
        "budget": [],
        "planning": [],
        "documents": [],
        "sujets": [],
        "compteur": {"segments": 0, "mots": 0},
    }


class MeetingEngine:
    def __init__(self, store, llm=None, cfg=None):
        self.store = store
        self.llm = llm
        self.cfg = cfg or {}
        self._lock = threading.RLock()
        self._listeners = []

    # ------------------------------------------------------------ événements
    def on_event(self, fn):
        self._listeners.append(fn)
        return fn

    def _emit(self, evenement: str, session_id: str, **data):
        # « evt » et non « kind » : la charge utile peut elle-même porter un
        # champ « kind » (décision / action / risque) et écraserait l'événement.
        rec = {"evt": evenement, "session": session_id, "t": _maintenant()}
        rec.update(data)
        for fn in list(self._listeners):
            try:
                fn(rec)
            except Exception:
                pass

    # ------------------------------------------------------------- CRUD base
    def creer(self, payload: dict) -> dict:
        with self._lock:
            s = _session_vide(payload)
            self.store.put(COLLECTION, s["id"], s)
        log.info("meeting", f"session créée : {s['titre']} ({s['id']})")
        self._emit("session", s["id"], titre=s["titre"], statut=s["statut"])
        return s

    def get(self, sid: str) -> dict | None:
        return self.store.get(COLLECTION, sid)

    def liste(self) -> list[dict]:
        rows = self.store.all(COLLECTION)
        for r in rows:
            r["_resume"] = {
                "segments": len(r.get("transcript") or []),
                "decisions": len(r.get("decisions") or []),
                "actions": len(r.get("actions") or []),
                "documents": len(r.get("documents") or []),
            }
        return rows

    def maj(self, sid: str, patch: dict) -> dict | None:
        with self._lock:
            s = self.get(sid)
            if not s:
                return None
            for k, v in (patch or {}).items():
                if k in ("id", "documents", "cree_le"):
                    continue
                s[k] = v
            self.store.put(COLLECTION, sid, s)
        self._emit("maj", sid, statut=s.get("statut"))
        return s

    def statut(self, sid: str, statut: str) -> dict | None:
        if statut not in STATUTS:
            return None
        s = self.maj(sid, {"statut": statut})
        if s:
            log.info("meeting", f"{sid} → {statut}")
            self._emit("statut", sid, statut=statut)
        return s

    def supprimer(self, sid: str) -> bool:
        return self.store.delete(COLLECTION, sid)

    def ajouter_document(self, sid: str, rec: dict) -> dict | None:
        """Attache un document produit à la session.

        Passer par `maj()` ne fonctionnerait pas : elle ignore délibérément le
        champ « documents » pour éviter qu'un simple correctif ne l'écrase.
        """
        with self._lock:
            s = self.get(sid)
            if not s:
                return None
            s.setdefault("documents", []).append(rec)
            self.store.put(COLLECTION, sid, s)
        self._emit("document", sid, titre=rec.get("titre"), format=rec.get("format"))
        return s

    # --------------------------------------------------------------- capture
    def pousser(self, sid: str, texte: str, locuteur: str = "", source: str = "voix",
                enrichir: bool = True) -> dict:
        """Ajoute une prise de parole et rend les suggestions détectées."""
        texte = (texte or "").strip()
        if not texte:
            return {"suggestions": []}
        with self._lock:
            s = self.get(sid)
            if not s:
                return {"erreur": "session inconnue"}
            seg = {"t": _maintenant(), "horodatage": time.time(),
                   "locuteur": locuteur or "", "texte": texte, "source": source}
            s["transcript"].append(seg)
            s["compteur"]["segments"] = len(s["transcript"])
            s["compteur"]["mots"] = sum(
                len(x.get("texte", "").split()) for x in s["transcript"])

            suggestions = extract.suggerer(
                texte, locuteur=locuteur, participants=s.get("participants"),
                origine=source)
            ajoutees = []
            for sug in suggestions:
                if sug["confiance"] < 0.3:
                    continue
                sug["id"] = new_id("sug")
                sug["statut"] = "attente"
                sug["segment"] = seg["t"]
                sug["locuteur"] = locuteur
                s["suggestions"].append(sug)
                ajoutees.append(sug)
            if s["suggestions"] and len(s["suggestions"]) > 400:
                s["suggestions"] = s["suggestions"][-400:]
            self.store.put(COLLECTION, sid, s)

        if enrichir:
            self._enrichir_llm(sid)

        self._emit("segment", sid, locuteur=locuteur, texte=texte[:160],
                   suggestions=len(ajoutees))
        return {"suggestions": ajoutees, "segment": seg}

    def noter(self, sid: str, texte: str) -> dict:
        """Note manuscrite : même traitement, mais confiance plus haute."""
        with self._lock:
            s = self.get(sid)
            if not s:
                return {"erreur": "session inconnue"}
            s["notes"].append({"t": _maintenant(), "texte": (texte or "").strip()})
            suggestions = extract.suggerer(texte, participants=s.get("participants"),
                                           origine="note")
            ajoutees = []
            for sug in suggestions:
                sug["id"] = new_id("sug")
                sug["statut"] = "attente"
                sug["segment"] = _maintenant()
                sug["confiance"] = round(min(1.0, sug["confiance"] + 0.2), 2)
                s["suggestions"].append(sug)
                ajoutees.append(sug)
            self.store.put(COLLECTION, sid, s)
        self._emit("note", sid, texte=(texte or "")[:160], suggestions=len(ajoutees))
        return {"suggestions": ajoutees}

    # ------------------------------------------------------------- suggestions
    def suggestions(self, sid: str, statut: str = "attente") -> list[dict]:
        s = self.get(sid) or {}
        return [x for x in (s.get("suggestions") or [])
                if statut in ("*", "") or x.get("statut") == statut]

    def _trouver_suggestion(self, s: dict, sug_id: str):
        for x in s.get("suggestions") or []:
            if x.get("id") == sug_id:
                return x
        return None

    def accepter(self, sid: str, sug_id: str, patch: dict | None = None) -> dict | None:
        with self._lock:
            s = self.get(sid)
            if not s:
                return None
            sug = self._trouver_suggestion(s, sug_id)
            if not sug:
                return None
            patch = patch or {}
            item = {
                "id": new_id(sug["kind"][:3]),
                "texte": patch.get("texte") or sug["texte"],
                "responsable": patch.get("responsable", sug.get("responsable", "")),
                "echeance": patch.get("echeance", sug.get("echeance", "")),
                "source": sug.get("origine", ""),
                "confiance": sug.get("confiance", 0),
                "cree_le": _instant(),
            }
            if sug["kind"] == "action":
                item["statut"] = "à faire"
                item["montant"] = patch.get("montant", sug.get("montant"))
                s["actions"].append(item)
            elif sug["kind"] == "decision":
                s["decisions"].append(item)
            elif sug["kind"] == "risque":
                s["risques"].append(item)
            else:
                s["questions"].append(item)
            sug["statut"] = "accepte"
            sug["item_id"] = item["id"]
            self.store.put(COLLECTION, sid, s)
        self._emit("accepte", sid, kind=sug["kind"], texte=item["texte"][:120])
        return item

    def refuser(self, sid: str, sug_id: str) -> bool:
        with self._lock:
            s = self.get(sid)
            if not s:
                return False
            sug = self._trouver_suggestion(s, sug_id)
            if not sug:
                return False
            sug["statut"] = "refuse"
            self.store.put(COLLECTION, sid, s)
        self._emit("refuse", sid, sug_id=sug_id)
        return True

    def ajouter_item(self, sid: str, kind: str, payload: dict) -> dict | None:
        with self._lock:
            s = self.get(sid)
            if not s:
                return None
            item = {
                "id": new_id(kind[:3]),
                "texte": (payload.get("texte") or "").strip(),
                "responsable": payload.get("responsable", ""),
                "echeance": payload.get("echeance", ""),
                "source": payload.get("source") or "saisie",
                "confiance": 1.0,
                "cree_le": _instant(),
            }
            if kind == "action":
                item["statut"] = payload.get("statut") or "à faire"
                item["montant"] = payload.get("montant")
                s["actions"].append(item)
            elif kind == "decision":
                s["decisions"].append(item)
            elif kind == "risque":
                s["risques"].append(item)
            elif kind == "question":
                s["questions"].append(item)
            else:
                return None
            self.store.put(COLLECTION, sid, s)
        self._emit("item", sid, kind=kind, texte=item["texte"][:120])
        return item

    def _liste_kind(self, s: dict, kind: str) -> list:
        return {"action": s.get("actions"), "decision": s.get("decisions"),
                "risque": s.get("risques"), "question": s.get("questions")}.get(kind, [])

    def modifier_item(self, sid: str, kind: str, item_id: str, patch: dict):
        with self._lock:
            s = self.get(sid)
            if not s:
                return None
            for it in self._liste_kind(s, kind):
                if it.get("id") == item_id:
                    it.update({k: v for k, v in (patch or {}).items() if k != "id"})
                    self.store.put(COLLECTION, sid, s)
                    return it
        return None

    def supprimer_item(self, sid: str, kind: str, item_id: str) -> bool:
        with self._lock:
            s = self.get(sid)
            if not s:
                return False
            cle = {"action": "actions", "decision": "decisions",
                   "risque": "risques", "question": "questions"}.get(kind)
            if not cle:
                return False
            avant = len(s[cle])
            s[cle] = [x for x in s[cle] if x.get("id") != item_id]
            self.store.put(COLLECTION, sid, s)
            return len(s[cle]) < avant

    # ---------------------------------------------------------- budget/planning
    def ajouter_budget(self, sid: str, ligne: dict) -> dict | None:
        with self._lock:
            s = self.get(sid)
            if not s:
                return None
            qte = float(ligne.get("quantite") or 1)
            pu = float(ligne.get("cout_unitaire") or 0)
            rec = {
                "id": new_id("bud"),
                "libelle": ligne.get("libelle") or "Poste",
                "categorie": ligne.get("categorie") or "Fonctionnement",
                "quantite": qte, "unite": ligne.get("unite") or "forfait",
                "cout_unitaire": pu,
                "total": round(qte * pu, 2),
                "financeur": ligne.get("financeur") or "",
                "source": ligne.get("source") or "saisie",
            }
            s["budget"].append(rec)
            self.store.put(COLLECTION, sid, s)
        self._emit("budget", sid, libelle=rec["libelle"], total=rec["total"])
        return rec

    def supprimer_budget(self, sid: str, ligne_id: str) -> bool:
        with self._lock:
            s = self.get(sid)
            if not s:
                return False
            n = len(s["budget"])
            s["budget"] = [x for x in s["budget"] if x.get("id") != ligne_id]
            self.store.put(COLLECTION, sid, s)
            return len(s["budget"]) < n

    def total_budget(self, s: dict) -> float:
        return round(sum(float(x.get("total") or 0) for x in (s.get("budget") or [])), 2)

    def ajouter_tache(self, sid: str, tache: dict) -> dict | None:
        with self._lock:
            s = self.get(sid)
            if not s:
                return None
            rec = {
                "id": new_id("tch"),
                "label": tache.get("label") or "Tâche",
                "debut": tache.get("debut") or "",
                "fin": tache.get("fin") or "",
                "responsable": tache.get("responsable") or "",
                "avancement": float(tache.get("avancement") or 0),
                "depend": tache.get("depend") or "",
                "jalon": bool(tache.get("jalon")),
            }
            s["planning"].append(rec)
            self.store.put(COLLECTION, sid, s)
        self._emit("planning", sid, label=rec["label"])
        return rec

    def supprimer_tache(self, sid: str, tache_id: str) -> bool:
        with self._lock:
            s = self.get(sid)
            if not s:
                return False
            n = len(s["planning"])
            s["planning"] = [x for x in s["planning"] if x.get("id") != tache_id]
            self.store.put(COLLECTION, sid, s)
            return len(s["planning"]) < n

    # ------------------------------------------------------------ enrichissement
    def _enrichir_llm(self, sid: str) -> None:
        """Le modèle relit les dernières phrases et propose en plus. Jamais bloquant."""
        if not self.llm or self.llm.resolve() == "none":
            return
        try:
            s = self.get(sid)
            if not s:
                return
            derniers = (s.get("transcript") or [])[-12:]
            if len(derniers) < 3:
                return
            texte = "\n".join(f"[{d.get('t','')}] {d.get('locuteur') or '?'} : {d.get('texte','')}"
                              for d in derniers)
            connus = ", ".join(s.get("participants") or []) or "(non précisés)"
            prompt = (
                "Voici les dernières phrases prononcées en réunion.\n\n" + texte +
                "\n\nParticipants connus : " + connus +
                "\n\nRelève ce qui n'est pas encore explicite : toute décision, toute action à "
                "réaliser, tout risque signalé, toute question restée ouverte. "
                "Ignore le bavardage. Pas d'invention.\n"
                'Rends {"decisions": [{"texte","responsable","echeance"}], '
                '"actions": [{"texte","responsable","echeance"}], '
                '"risques": [{"texte"}], "questions": [{"texte"}], "sujets": ["..."]}'
            )
            data = self.llm.json_complete(
                prompt, system="Tu es le secrétaire de séance d'une collectivité française. "
                               "Tu écris en français administratif clair et factuel.",
                schema_hint='{"decisions":[],"actions":[],"risques":[],"questions":[],"sujets":[]}')
            if not data:
                return
            self._integrer_llm(sid, data)
        except Exception as exc:
            log.warn("meeting", f"enrichissement impossible : {exc}")

    def _integrer_llm(self, sid: str, data: dict) -> None:
        with self._lock:
            s = self.get(sid)
            if not s:
                return
            existants = {x["texte"][:60].lower() for x in (s.get("suggestions") or [])}
            ajout = []
            mapping = (("decisions", "decision"), ("actions", "action"),
                       ("risques", "risque"), ("questions", "question"))
            for cle, kind in mapping:
                for obj in (data.get(cle) or []):
                    if not isinstance(obj, dict):
                        continue
                    tx = str(obj.get("texte") or "").strip()
                    if len(tx) < 12:
                        continue
                    if tx[:60].lower() in existants:
                        continue
                    existants.add(tx[:60].lower())
                    ajout.append({
                        "id": new_id("sug"), "kind": kind,
                        "texte": extract.memo(tx),
                        "responsable": str(obj.get("responsable") or ""),
                        "echeance": str(obj.get("echeance") or ""),
                        "montant": None, "confiance": 0.75,
                        "origine": "modele", "statut": "attente",
                        "segment": _maintenant(), "locuteur": "",
                    })
            for sj in (data.get("sujets") or []):
                sj = str(sj).strip()
                if sj and sj not in s["sujets"]:
                    s["sujets"].append(sj)
            if ajout:
                s["suggestions"].extend(ajout)
                self.store.put(COLLECTION, sid, s)
                self._emit("suggestions", sid, combien=len(ajout))
