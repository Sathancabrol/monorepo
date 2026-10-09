#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scénario de bout en bout pour Carré d'As.

Rejoue une réunion entière contre un serveur qui tourne déjà :
création, verbatim, extraction, acceptation, budget, planning, puis génération
de tous les gabarits dans tous les formats — avec vérification de la structure
OPC des .docx et .pptx produits.

Usage :  python3 scripts/test-carre-d-as.py [http://127.0.0.1:8000]
"""

from __future__ import annotations

import io
import json
import sys
import urllib.error
import urllib.request
import zipfile
import xml.etree.ElementTree as ET

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000").rstrip("/")

OK, KO = "  ✓", "  ✗"
echecs = []


def verifier(condition, message, detail=""):
    if condition:
        print(f"{OK} {message}")
    else:
        print(f"{KO} {message}" + (f" — {detail}" if detail else ""))
        echecs.append(message)
    return condition


def api(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method)
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method} {path} → {e.code} : {e.read().decode()[:200]}")


def opc_valide(blob: bytes) -> tuple[bool, str]:
    """Vérifie qu'un paquet OPC (docx/pptx) est cohérent."""
    try:
        z = zipfile.ZipFile(io.BytesIO(blob))
    except Exception as e:
        return False, f"zip illisible : {e}"
    noms = z.namelist()
    for n in noms:
        if n.endswith((".xml", ".rels")):
            try:
                ET.fromstring(z.read(n))
            except Exception as e:
                return False, f"{n} : XML invalide ({e})"
    NS_R = "{http://schemas.openxmlformats.org/package/2006/relationships}"
    for n in noms:
        if not n.endswith(".rels"):
            continue
        base = n.rsplit("_rels/", 1)[0]
        for rel in ET.fromstring(z.read(n)).findall(NS_R + "Relationship"):
            if rel.get("TargetMode") == "External":
                continue
            parties = []
            for seg in (base + rel.get("Target")).split("/"):
                if seg == "..":
                    parties.pop()
                elif seg not in ("", "."):
                    parties.append(seg)
            if "/".join(parties) not in noms:
                return False, f"{n} → cible absente : {rel.get('Target')}"
    NS_T = "{http://schemas.openxmlformats.org/package/2006/content-types}"
    ct = ET.fromstring(z.read("[Content_Types].xml"))
    declares = {o.get("PartName") for o in ct.findall(NS_T + "Override")}
    defauts = {d.get("Extension").lower() for d in ct.findall(NS_T + "Default")}
    for n in noms:
        if n == "[Content_Types].xml":
            continue
        if "/" + n not in declares and n.rsplit(".", 1)[-1].lower() not in defauts:
            return False, f"{n} : ni déclaré ni extension par défaut"
    return True, f"{len(noms)} parties"


print(f"\n=== Scénario Carré d'As — {BASE} ===\n")

# ---------------------------------------------------------------- 0. santé
sante = api("GET", "/api/health")
verifier(sante.get("ok"), "le serveur répond", str(sante))
mods = api("GET", "/api/modules")["modules"]
verifier(all(m.get("charge") for m in mods),
         f"{len(mods)} modules chargés",
         ", ".join(m["id"] for m in mods if not m.get("charge")))

# ------------------------------------------------------------- 1. la réunion
reu = api("POST", "/api/meeting", {
    "titre": "Comité de pilotage — Frange Sud de Frontignan",
    "lieu": "Sète", "date": "2026-10-16", "type": "comité de pilotage",
    "organisme": "Sète Agglopôle Méditerranée",
    "contexte": "Cadrage de l'opération de la Frange Sud, en articulation avec "
                "le SCoT révisé arrêté le 24/02/2026.",
    "ordre_du_jour": ["Avancement de l'étude de faisabilité",
                      "Phasage et enveloppe",
                      "Articulation avec l'enquête publique du SCoT"],
    "participants": ["M. Martin", "Mme Roux", "M. Belkacem"],
})["session"]
rid = reu["id"]
print(f"\n  réunion : {rid}\n")
api("POST", f"/api/meeting/{rid}/statut", {"statut": "en_cours"})

VERBATIM = [
    ("M. Martin", "On décide de lancer l'étude de faisabilité avant fin novembre, "
                  "M. Martin va piloter le sujet."),
    ("Mme Roux", "Il faut chiffrer la phase 1 pour 12 000 euros et consulter les "
                 "services de l'État d'ici le 30/11/2026."),
    ("M. Belkacem", "Attention, il y a un risque de retard sur l'enquête publique "
                    "du SCoT au second semestre 2026."),
    ("M. Martin", "Mme Roux va préparer la note de cadrage pour la semaine prochaine."),
    ("Mme Roux", "On valide le périmètre de 18 hectares et on retient le scénario "
                 "de désimperméabilisation."),
    ("M. Belkacem", "Bon, et sinon il fait beau aujourd'hui."),
]

for loc, txt in VERBATIM:
    r = api("POST", f"/api/meeting/{rid}/segment", {"locuteur": loc, "texte": txt})
    n = len(r.get("suggestions", []))
    print(f"    [{loc:12s}] {n} proposition(s) — {txt[:52]}…")

sugs = api("GET", f"/api/meeting/{rid}/suggestions?statut=attente")["suggestions"]
verifier(len(sugs) >= 4, f"{len(sugs)} suggestions extraites")
verifier(any(s["kind"] == "decision" for s in sugs), "au moins une décision détectée")
verifier(any(s["kind"] == "action" for s in sugs), "au moins une action détectée")
verifier(any(s["kind"] == "risque" for s in sugs), "au moins un risque détecté")
verifier(all(s["kind"] != "question" for s in sugs), "le bavardage est ignoré")
verifier(any(s["responsable"] == "M. Martin" for s in sugs), "responsable « M. Martin » identifié")
verifier(any(s["responsable"] == "Mme Roux" for s in sugs), "responsable « Mme Roux » identifiée")
verifier(any(s["echeance"] == "2026-11-30" for s in sugs), "échéance « fin novembre » → 2026-11-30")
verifier(any(s["montant"] == 12000 for s in sugs), "montant 12 000 € extrait")

# ------------------------------------------------------------ 2. acceptation
for s in sugs:
    api("POST", f"/api/meeting/{rid}/suggestion/{s['id']}/accepter", {})
apres = api("GET", f"/api/meeting/{rid}")["session"]
verifier(len(apres["decisions"]) >= 2, f"{len(apres['decisions'])} décisions retenues")
verifier(len(apres["actions"]) >= 2, f"{len(apres['actions'])} actions retenues")
verifier(len(apres["risques"]) >= 1, f"{len(apres['risques'])} risques retenus")

# ------------------------------------------------------- 3. budget & planning
api("POST", f"/api/meeting/{rid}/budget",
    {"libelle": "Étude de faisabilité", "categorie": "Étude", "quantite": 1,
     "unite": "forfait", "cout_unitaire": 45000, "financeur": "Agglo"})
api("POST", f"/api/meeting/{rid}/budget",
    {"libelle": "Désimperméabilisation", "categorie": "Travaux", "quantite": 180000,
     "unite": "m²", "cout_unitaire": 0.45, "financeur": "Fonds vert"})
api("POST", f"/api/meeting/{rid}/planning",
    {"label": "Étude de faisabilité", "debut": "2026-10-16", "fin": "2026-11-30",
     "responsable": "M. Martin", "avancement": 10})
api("POST", f"/api/meeting/{rid}/planning",
    {"label": "Consultation des PPA", "debut": "2026-11-01", "fin": "2026-12-15",
     "responsable": "Mme Roux", "avancement": 0})
s = api("GET", f"/api/meeting/{rid}")["session"]
total = sum(b["total"] for b in s["budget"])
verifier(abs(total - (45000 + 180000 * 0.45)) < 0.01,
         f"budget total = {total:,.2f} €".replace(",", " "))
verifier(len(s["planning"]) == 2, "2 tâches planifiées")

# --------------------------------------------------------------- 4. documents
GABARITS = api("GET", "/api/meeting/gabarits")["gabarits"]
print()
produits = {}
for g in GABARITS:
    for fmt in g["formats"]:
        r = api("POST", f"/api/meeting/{rid}/generer",
                {"gabarit": g["id"], "format": fmt})
        doc = r["document"]
        produits[doc["nom"]] = doc
        ok, detail = True, ""
        if fmt in ("docx", "pptx"):
            with urllib.request.urlopen(BASE + r["telechargement"], timeout=30) as fh:
                ok, detail = opc_valide(fh.read())
        verifier(ok, f"{g['id']:<13} .{fmt:<5} {doc['taille']:>7} o", detail)

# ------------------------------- 5. les documents sont bien rattachés
apres_docs = api("GET", f"/api/meeting/{rid}")["session"]
verifier(len(apres_docs["documents"]) == len(produits),
         f"{len(apres_docs['documents'])} documents rattachés à la session",
         f"{len(produits)} générés mais {len(apres_docs['documents'])} enregistrés")
verifier(all(d.get("nom") for d in apres_docs["documents"]),
         "chaque document porte un nom de fichier")

# -------------------------------------------------- 6. relecture du contenu
print()
with urllib.request.urlopen(BASE + "/api/fichiers/"
                            + next(n for n in produits if n.endswith(".md")),
                            timeout=30) as fh:
    md = fh.read().decode("utf-8")
verifier("Frange Sud" in md, "le compte rendu cite l'opération")
verifier("Décisions" in md and "Actions à mener" in md,
         "le compte rendu comporte décisions et actions")
verifier("M. Martin" in md, "le compte rendu nomme les responsables")

# ---------------------------------------------------------- 6. autres modules
print()
api("POST", "/api/cognitorium/profils",
    {"nom": "Roux", "prenom": "Camille", "role": "Cheffe de projet",
     "structure": "Sète Agglopôle Méditerranée", "type": "individu"})
verifier(len(api("GET", "/api/cognitorium/profils")["profils"]) >= 1, "profil créé")
api("POST", "/api/carto/points", {"nom": "Frange Sud — îlot A", "lat": 43.44,
                                  "lon": 3.75, "commune": "Frontignan"})
verifier(len(api("GET", "/api/carto/points")["points"]) >= 1, "point cartographié")
api("POST", "/api/prevision/indicateurs", {"id": "population", "valeur": 131000})
api("POST", "/api/prevision/scenario", {"nom": "Report de l'enquête publique",
                                        "horizon": "6 mois", "probabilite": 40,
                                        "impacts": ["Décalage du phasage"]})
r = api("POST", "/api/prevision/generer", {"format": "html"})
verifier(r["document"]["taille"] > 800, "note de prévision générée")
cas = api("POST", "/api/osint/cas", {"titre": "Vérification du prestataire",
                                     "question": "La structure est-elle régulièrement immatriculée ?"})
api("POST", f"/api/osint/cas/{cas['cas']['id']}/preuve",
    {"titre": "Extrait SIRENE", "source": "Annuaire des Entreprises (API)",
     "fiabilite": "A", "contenu": "SIRET actif depuis 2011."})
r = api("POST", f"/api/osint/cas/{cas['cas']['id']}/generer", {"format": "html"})
verifier(r["document"]["taille"] > 600, "note OSINT générée")
# un élément sans source doit être refusé : c'est la règle du module
refuse = False
try:
    api("POST", f"/api/osint/cas/{cas['cas']['id']}/preuve",
        {"titre": "Sans source", "source": ""})
except Exception:
    refuse = True
verifier(refuse, "un élément sans source est refusé")

# ------------------------------------- 7. sources de données et admissibilité
print()
src = api("GET", "/api/carto/sources")
verifier(src["total"] > 25, f"{src['total']} sources de données référencées")
excl = src["resume"]["exclus_collectivite"]
verifier(len(excl) >= 4, f"{len(excl)} sources écartées pour un usage collectivité")
libres = api("GET", "/api/carto/sources?usage=oui")["sources"]
verifier(all(s["usage"] == "oui" for s in libres),
         f"le filtre usage=oui ne renvoie que du présentable ({len(libres)})")

def adm(rec):
    return api("POST", "/api/canonique/valider", rec)

verifier(not adm({"id": "t:1", "type": "mesure", "source": "", "status": "fact",
                  "label": "Débit"})["presentable"],
         "un fait sans source est écarté")
verifier(not adm({"id": "t:2", "type": "mesure", "source": "carto",
                  "status": "fact", "label": "Superficie", "valeur": 42})["presentable"],
         "un chiffre sans unité est écarté")
verifier(not adm({"id": "t:3", "type": "profil", "source": "cognitorium",
                  "status": "fact", "label": "Contact",
                  "note": "06 12 34 56 78 — m.dupont@agglo.fr"})["presentable"],
         "une donnée personnelle est écartée")
ok = adm({"id": "t:4", "type": "mesure", "source": "INPN", "status": "fact",
          "label": "Zones humides", "valeur": 1200, "unite": "ha",
          "observed_at": "2026-09-01T00:00:00"})
verifier(ok["presentable"] and ok["valide"], "un fait sourcé, daté et unité est accepté")

# la règle du fait vérifié (méthode Frontignan) : 2 sources, ou une source officielle
non_croise = adm({"id": "t:5", "type": "mesure", "source": "blog de M. Untel",
                  "status": "fact", "label": "Fréquentation",
                  "valeur": 1200, "unite": "visiteurs"})
verifier(any(p["regle"] == "fait_non_croise" for p in non_croise["problemes"]),
         "un fait sur une seule source privée est signalé")
officiel = adm({"id": "t:6", "type": "mesure", "source": "INSEE", "status": "fact",
                "label": "Population", "valeur": 131000, "unite": "habitants"})
verifier(officiel["presentable"] and not officiel["problemes"],
         "un fait appuyé par une source officielle est accepté")
croise = adm({"id": "t:7", "type": "mesure", "source": "Midi Libre",
              "sources": ["Midi Libre", "agglopole.fr"], "status": "fact",
              "label": "Budget", "valeur": 242, "unite": "M€"})
verifier(croise["presentable"] and not croise["problemes"],
         "un fait croisé sur deux sources est accepté")

mq = api("GET", "/api/canonique/schema")["marqueurs"]
verifier(mq["fact"]["marqueur"] == "✅" and "sources" in mq["fact"]["critere"],
         "le vocabulaire de lecture est aligné sur la méthode Frontignan")

# ------------------------------------------------------------------ 8. bilan
print(f"\n=== {len(produits)} documents produits · "
      f"{len(echecs)} échec(s) ===")
if echecs:
    for e in echecs:
        print(f"   - {e}")
    sys.exit(1)
print("Tout est vert.\n")
