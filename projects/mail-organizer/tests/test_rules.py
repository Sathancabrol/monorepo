"""Tests du moteur de règles (unittest, stdlib)."""

import json
import unittest
from pathlib import Path

from mail_organizer.rules import (
    MessageMeta,
    Rule,
    classify,
    extract_address,
    normalize,
    top_domains,
)

CONFIG = json.loads(
    (Path(__file__).resolve().parent.parent / "config.example.json").read_text(encoding="utf-8")
)
RULES = [Rule.from_dict(r) for r in CONFIG["rules"] if "folder" in r]
DEFAULT = CONFIG.get("default_folder", "À trier")


def meta(from_addr="", subject="", headers=("received",)):
    return MessageMeta(
        uid=1,
        from_addr=from_addr,
        subject=subject,
        header_names=frozenset(headers),
    )


class TestClassify(unittest.TestCase):
    def test_alerte_securite_google(self):
        m = meta("Google <no-reply@accounts.google.com>", "Alerte de sécurité")
        self.assertEqual(classify(m, RULES, DEFAULT),
                         "Compte et sécurité/Alertes de connexion")

    def test_comptes_lies_google(self):
        m = meta("Google <noreply-accounts@google.com>",
                 "Vous avez partagé certaines données de votre compte Google avec Linear")
        self.assertEqual(classify(m, RULES, DEFAULT),
                         "Compte et sécurité/Comptes liés Google")

    def test_commande_instant_gaming(self):
        m = meta("Instant Gaming <noreply@email.instant-gaming.com>",
                 "Merci pour votre commande #183962675 !")
        self.assertEqual(classify(m, RULES, DEFAULT), "Achats et jeux vidéo")

    def test_facture_impots(self):
        m = meta("DGFiP <ne-pas-repondre@impots.gouv.fr>", "Votre avis d'imposition")
        self.assertEqual(classify(m, RULES, DEFAULT), "Administratif et factures")

    def test_sujet_diplome(self):
        m = meta("Universite <scolarite@univ.fr>", "Votre diplôme est disponible")
        self.assertEqual(classify(m, RULES, DEFAULT), "Administratif et factures")

    def test_polsia(self):
        m = meta("Polsia <system@polsia.com>", "Cognitorium est en ligne")
        self.assertEqual(classify(m, RULES, DEFAULT),
                         "Projets et travail/Polsia - Cognitorium et Mnéoterr")

    def test_newsletter_par_domaine(self):
        m = meta("Exa Team <hello@exa.ai>", "Introducing Exa Snapshot")
        self.assertEqual(classify(m, RULES, DEFAULT), "Newsletters tech et IA")

    def test_newsletter_par_list_unsubscribe(self):
        m = meta("Marketing <promo@inconnu.example>", "Super offre !",
                 headers=("received", "list-unsubscribe"))
        self.assertEqual(classify(m, RULES, DEFAULT), "Newsletters et promotions")

    def test_sous_domaine(self):
        m = meta("X <x@mail.vizard.ai>", "Vizard Academy")
        self.assertEqual(classify(m, RULES, DEFAULT), "Newsletters tech et IA")

    def test_courrier_personnel_par_defaut(self):
        m = meta("Marie Dupont <marie@exemple.fr>", "Déjeuner dimanche ?")
        self.assertEqual(classify(m, RULES, DEFAULT), "À trier")

    def test_priorite_administratif_sur_newsletter(self):
        m = meta("EDF <facture@edf.fr>", "Votre facture",
                 headers=("received", "list-unsubscribe"))
        self.assertEqual(classify(m, RULES, DEFAULT), "Administratif et factures")


class TestHelpers(unittest.TestCase):
    def test_normalize_accents(self):
        self.assertEqual(normalize("Alerte de sécurité"), "alerte de securite")

    def test_extract_address(self):
        self.assertEqual(extract_address('Google <no-reply@accounts.google.com>'),
                         "no-reply@accounts.google.com")

    def test_top_domains(self):
        metas = [meta("a@x.fr"), meta("b@x.fr"), meta("c@y.fr")]
        self.assertEqual(top_domains(metas, 2)[0], ("x.fr", 2))


if __name__ == "__main__":
    unittest.main()
