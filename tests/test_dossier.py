import unittest
from src.dossier import build_dossiers

class DossierTests(unittest.TestCase):
    def test_numeric_claim_stays_unverified(self):
        q = {"items": [{"id": "x", "url": "https://example.org",
                         "title": "La cifra creció un 25 % durante 2025."}]}
        d = build_dossiers(q)
        self.assertEqual(len(d["dossiers"]), 1)
        self.assertIsNone(d["dossiers"][0]["verdict"])
        self.assertFalse(d["dossiers"][0]["publication_allowed"])
    def test_no_numeric_claim(self):
        self.assertEqual(build_dossiers({"items": []})["dossiers"], [])
