import unittest
from src.claim_extraction import extract_claims

class ClaimTests(unittest.TestCase):
    def test_numeric(self):
        result = extract_claims("El indicador aumentó un 40 % durante 2025.")
        self.assertEqual(result[0]["verdict"], "unverified")
    def test_no_claim(self):
        self.assertEqual(extract_claims("Hola."), [])
    def test_limit(self):
        self.assertLessEqual(len(extract_claims(("El indicador subió un 20 %. ")*50)), 10)
