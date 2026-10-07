"""Tests de l'encodage UTF-7 modifié (RFC 3501)."""

import unittest

from mail_organizer.imap_utf7 import decode, encode


class TestUtf7(unittest.TestCase):
    def test_ascii_inchange(self):
        self.assertEqual(encode("INBOX"), "INBOX")

    def test_ampersand_litteral(self):
        self.assertEqual(encode("R&D"), "R&-D")
        self.assertEqual(decode("R&-D"), "R&D")

    def test_accents(self):
        encoded = encode("Compte et sécurité/Alertes de connexion")
        self.assertTrue(all(ord(c) < 128 for c in encoded))
        self.assertNotIn("é", encoded)
        self.assertEqual(decode(encoded), "Compte et sécurité/Alertes de connexion")

    def test_boite_de_reception(self):
        name = "Boîte de réception"
        self.assertEqual(decode(encode(name)), name)

    def test_roundtrip_varies(self):
        names = ["À trier", "Étés & hivers", "日本語", "a/b/c", "&", ""]
        for name in names:
            self.assertEqual(decode(encode(name)), name, msg=name)


if __name__ == "__main__":
    unittest.main()
