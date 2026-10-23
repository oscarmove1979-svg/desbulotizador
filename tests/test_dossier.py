import unittest
from src.dossier import build_dossiers

class DossierTests(unittest.TestCase):
    def test_numeric_claim_stays_unverified(self):
        q = {"items": [{"id": "x", "url": "https://example.org",
                         "state": "candidate_unverified", "publishable": False,
                         "title": "La cifra creció un 25 % durante 2025."}]}
        d = build_dossiers(q)
        self.assertEqual(len(d["dossiers"]), 1)
        self.assertIsNone(d["dossiers"][0]["verdict"])
        matrix = d["dossiers"][0]["evidence_matrices"][0]
        self.assertEqual(matrix["claim"], d["dossiers"][0]["claims"][0]["text"])
        self.assertIsNone(matrix["verdict"])
        self.assertFalse(d["dossiers"][0]["publication_allowed"])
    def test_no_numeric_claim(self):
        self.assertEqual(build_dossiers({"items": []})["dossiers"], [])

    def test_publishable_candidate_is_not_processed(self):
        item = {'id':'x','url':'https://example.org','title':'La cifra creció 25 % en 2025','state':'candidate_unverified','publishable':True}
        self.assertEqual(build_dossiers({'items':[item]})['dossiers'], [])
