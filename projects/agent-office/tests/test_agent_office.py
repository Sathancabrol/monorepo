"""Tests agent-office — unittest, stdlib uniquement.
Lancer : python3 -m unittest discover -s tests -v  (depuis projects/agent-office)
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent_office import budget, invoices, marketing, planning, registry  # noqa: E402


class TestBudget(unittest.TestCase):
    def test_summarize_reel(self):
        s = budget.summarize(budget.load_rows())
        self.assertEqual(s["revenus"], 977.10)
        self.assertAlmostEqual(s["lock"], 1088.61, places=2)
        self.assertAlmostEqual(s["restant"], -111.51, places=2)  # le déficit réel

    def test_filtre_mois(self):
        s = budget.summarize(budget.load_rows(), month="2026-10")
        self.assertGreater(s["n"], 0)
        self.assertEqual(budget.summarize(budget.load_rows(), month="1999-01")["n"], 0)


class TestInvoices(unittest.TestCase):
    def test_mentions_legales(self):
        html, txt, total = invoices.build_doc(
            "facture", "Mairie Test", invoices.parse_lines("Analyse|1|900;Deck|1|400"), "F01"
        )
        self.assertIn("293 B du CGI", html)
        self.assertIn("Mairie Test", txt)
        self.assertEqual(total, 1300.0)
        self.assertIn("pénalités", html)


class TestMarketing(unittest.TestCase):
    def test_offres_reelles(self):
        for k in ("O1", "O2", "O3"):
            self.assertIn("<h1>", marketing.onepager(k))
        self.assertIn("J+7", marketing.sequence("O1"))
        self.assertIn("LinkedIn", marketing.post("O3"))


class TestPlanning(unittest.TestCase):
    def test_ics(self):
        ics = planning.build_ics(planning.load(), days=400)
        self.assertIn("BEGIN:VCALENDAR", ics)
        self.assertIn("BEGIN:VEVENT", ics)
        self.assertIn("J+30", ics)  # la révision de mission est planifiée


class TestRegistry(unittest.TestCase):
    def test_collect(self):
        caps = registry.collect()
        self.assertGreaterEqual(len(caps), 8)
        names = {c["name"] for c in caps}
        for attendu in ("budget", "invoices", "marketing", "prospects", "research", "mail", "planning", "registry"):
            self.assertIn(attendu, names)

    def test_selftests(self):
        from agent_office import maildigest, prospects, research
        for m in (budget, invoices, marketing, research, prospects, maildigest, planning):
            self.assertIn("OK", m.selftest())


if __name__ == "__main__":
    unittest.main()
