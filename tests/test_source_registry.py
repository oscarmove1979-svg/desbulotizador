import unittest
from src.source_registry import classify_source

class SourceRegistryTests(unittest.TestCase):
    def test_official_source_not_fact_checked(self):
        result = classify_source("https://www.boe.es/diario_boe/")
        self.assertEqual(result["kind"], "institutional_primary_source")
        self.assertFalse(result["fact_verified"])
    def test_prevent_suffix_spoofing(self):
        result = classify_source("https://boe.es.attacker.example/claim")
        self.assertEqual(result["kind"], "unclassified_source")
    def test_reject_http(self):
        self.assertEqual(classify_source("http://www.ine.es/")["kind"], "unknown")
