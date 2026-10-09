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

# ------------------------------------------------------- 7.5 système agentique
agents = api("GET", "/api/agents")
verifier(agents["total"] == 22, f"22 agents spécialisés ({agents['total']})")
verifier(len(agents["cycle"]) == 6, "le cycle tient en 6 phases")

cas_routes = {
    "rédige le compte rendu de la réunion": "writer",
    "il faut un planning pour la Frange Sud": "pm",
    "combien coûte la phase 1 ?": "analyst",
    "vérifie si ce prestataire est immatriculé": "osint",
    "quelles sources pour la cartographie du territoire ?": "geo",
    "peut-on utiliser cette licence en public ?": "jurist",
}
for texte, attendu in cas_routes.items():
    r = api("POST", "/api/agents/router", {"texte": texte})
    verifier(r["resultats"] and r["resultats"][0]["id"] == attendu,
             f"routage « {texte[:38]}… » → {attendu}")

# une exécution complète : six phases, un document, une trace consignée
avant = api("GET", "/api/agents/historique")["total"]
r = api("POST", "/api/agents/executer",
        {"demande": "Établir le planning de la Frange Sud", "format": "md"})
verifier("document" in r and r["document"]["taille"] > 300,
         "une demande produit un document réel")
verifier(len(r["tache"]["phases"]) == 6, "les six phases sont toutes tracées")
verifier(all(p["statut"] in ("ok", "vide") for p in r["tache"]["phases"]),
         "aucune phase en échec")
apres = api("GET", "/api/agents/historique")["total"]
verifier(apres == avant + 1, "l'exécution est consignée dans l'historique")

# le contexte d'une réunion alimente le document produit
sessions = api("GET", "/api/meeting")["sessions"]
if sessions:
    sid = sessions[0]["id"]
    r2 = api("POST", "/api/agents/executer",
             {"demande": "Rédiger le compte rendu de la réunion",
              "reunion_id": sid, "format": "md"})
    verifier(r2["tache"]["phases"][0]["detail"] != "",
             "le compte rendu d'une réunion existante est produit")

# ------------------------------------------------------- 7.6 chat avec le patron
c = api("POST", "/api/chat/conversations", {"titre": "test scénario"})
cid = c["conversation"]["id"]
m = api("POST", f"/api/chat/conversations/{cid}/messages",
        {"texte": "Rédige le compte rendu de la réunion"})
verifier(m["message"]["role"] == "patron"
         and m["message"].get("patron") == "SOL ☉",
         "le chat ne répond que par le patron (SOL ☉)")
verifier(m["message"].get("agent") == "writer",
         "le patron a délégué au bon agent (writer)")
verifier(bool(m["message"].get("document")), "le chat produit un document téléchargeable")
verifier(len(m["message"].get("phases", [])) == 6, "le chat expose les 6 phases")
conv = api("GET", f"/api/chat/conversations/{cid}")
verifier(len(conv["messages"]) == 2, "l'historique conserve les 2 messages")
verifier(len(api("GET", "/api/chat/conversations")["conversations"]) >= 1,
         "les conversations sont listées")

# ------------------------------------------- 7.6b système solaire (le patron délègue)
etat = api("GET", "/api/agents/systeme")
verifier(etat["patron"]["nom"] == "SOL ☉", "le patron est SOL ☉")
verifier(len(etat["agents"]) == 22, "les 22 agents sont des planètes")
verifier(all(a["etat"] in ("travaille", "repos") for a in etat["agents"]),
         "chaque planète a un état (travaille / repos)")

# tâche hors périmètre → le patron crée un sous-agent
m2 = api("POST", f"/api/chat/conversations/{cid}/messages",
         {"texte": "Analyse la salinité des eaux du bassin de Thau "
                   "et la réglementation conchylicole applicable"})
verifier(bool(m2["message"].get("sous_agent")),
         "le patron crée un sous-agent quand la tâche dépasse le périmètre")
sa = m2["message"]["sous_agent"]
verifier(sa["parent"] and sa["domaine"], "le sous-agent a un parent et un domaine")
sous = api("GET", "/api/agents/sousagents")
verifier(sous["total"] >= 1, "le sous-agent est enregistré (une lune de plus)")

# réutilisation : même domaine → pas de doublon
m3 = api("POST", f"/api/chat/conversations/{cid}/messages",
         {"texte": "La salinité du bassin de Thau et les conchyliculteurs"})
sous2 = api("GET", "/api/agents/sousagents")
verifier(sous2["total"] == sous["total"],
         "le patron réutilise le sous-agent existant (pas de doublon)")

# --------------------------------------------- 7.6c Laplace (IA légère, devices)
etat_l = api("GET", "/api/laplace/etat")
verifier(etat_l["patron"] == "SOL ☉", "Laplace connaît le patron")
verifier(etat_l["memoire_si_utile"] is True,
         "Laplace consulte la mémoire seulement si utile")

# sans mot-clé de rappel → la mémoire n'est PAS consultée
r_sans = api("POST", "/api/laplace/parler",
             {"texte": "Rédige le compte rendu de la réunion", "canal": "web"})
verifier(r_sans["de"] == "SOL ☉", "Laplace transmet au patron")
verifier(r_sans["memoire_consultee"] is False,
         "sans mot-clé de rappel, la mémoire n'est pas consultée")
verifier(bool(r_sans.get("document")), "Laplace rend un document")

# avec un mot-clé de rappel → la mémoire est consultée
r_avec = api("POST", "/api/laplace/parler",
             {"texte": "Retrouve ce qu'on a fait sur la Frange Sud",
              "canal": "web"})
verifier(r_avec["memoire_consultee"] is True,
         "avec un mot-clé de rappel, la mémoire est consultée")
verifier(len(r_avec["memoire"]) >= 1, "la mémoire retourne des entrées")

# consultation mémoire explicite (à la demande)
mem = api("GET", "/api/laplace/memoire?q=Frange%20Sud")
verifier(mem["total"] >= 1, "la mémoire est consultable à la demande")

# --------------------------------------------- 7.6d config : PUT persiste vraiment
cfg_avant = api("GET", "/api/config")["config"]
api("PUT", "/api/config", {"patron": {"seuil_routage": 2.5},
                           "acces": {"token": "test-scenario"}})
cfg_apres = api("GET", "/api/config")["config"]
verifier(cfg_apres["patron"]["seuil_routage"] == 2.5,
         "un PUT /api/config met à jour la config lue ensuite (bug nonlocal corrigé)")
verifier(cfg_apres["acces"]["token"] == "test-scenario",
         "le token d'accès est persisté")
# le patron lit le seuil depuis la config
m_seuil = api("POST", "/api/laplace/parler",
              {"texte": "Bonjour, que peux-tu faire ?", "canal": "web"})
verifier(m_seuil["sous_agent_cree"] is True,
         "avec seuil=2.5, le patron crée un sous-agent même sur un score moyen")
# remise à zéro
api("PUT", "/api/config", {"patron": {"seuil_routage": 1.0},
                           "acces": {"token": ""}})
verifier(api("GET", "/api/config")["config"]["acces"]["token"] == "",
         "la config est remise à zéro après le test")

# ------------------------------------------------- 7.7 constellation (3 systèmes)
sys3 = api("GET", "/api/constellation")
verifier(sys3["total"] == 3, "la constellation expose 3 systèmes")
ids = {s["id"] for s in sys3["systemes"]}
verifier(ids == {"constellation", "planetaire", "agentique"},
         "constellation / planétaire / agentique sont présents")

g_obj = api("GET", "/api/constellation/graphe?systeme=constellation")
verifier(g_obj["meta"]["nb_noeuds"] >= 79,
         f"la constellation embarque l'atlas ({g_obj['meta']['nb_noeuds']} nœuds)")
verifier(any(n["id"] == "frontignan" for n in g_obj["noeuds"]),
         "le nœud Frontignan est dans la constellation")

g_pl = api("GET", "/api/constellation/graphe?systeme=planetaire")
verifier(any(n["type"] == "soleil" for n in g_pl["noeuds"]),
         "le système planétaire a un soleil (Carré d'As)")
verifier(any(n["type"] == "module" for n in g_pl["noeuds"]),
         "le système planétaire a des planètes (les modules)")
verifier(any(n["type"] == "satellite" for n in g_pl["noeuds"]),
         "le système planétaire a des satellites (les objets)")

g_ag = api("GET", "/api/constellation/graphe?systeme=agentique")
verifier(sum(1 for n in g_ag["noeuds"] if n["type"] == "agent") == 22,
         "le système agentique montre les 22 agents")

g_filtre = api("GET", "/api/constellation/graphe?systeme=constellation&type=projet")
verifier(all(n["type"] == "projet" for n in g_filtre["noeuds"]),
         "le filtre par type ne renvoie que ce type")

ds = api("GET", "/api/constellation/dataset/communes")
verifier("communes" in ds.get("key", "") and ds.get("label"),
         "les jeux de données chiffrés de l'atlas sont servis")

# ------------------------------------------------------------------ 8. bilan
print(f"\n=== {len(produits)} documents produits · "
      f"{len(echecs)} échec(s) ===")
if echecs:
    for e in echecs:
        print(f"   - {e}")
    sys.exit(1)
print("Tout est vert.\n")
