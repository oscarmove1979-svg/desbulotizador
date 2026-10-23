import unittest
from src.evidence_matrix import assemble_matrix

class EvidenceMatrixTests(unittest.TestCase):
    def test_sources_never_create_verdict(self):
        matrix = assemble_matrix("Afirmación de prueba", [
            {"url": "https://www.boe.es/a", "publisher": "BOE", "excerpt": "Texto"},
            {"url": "https://www.boe.es/a", "publisher": "BOE"},
            {"url": "http://example.org/insegura"}])
        self.assertEqual(len(matrix["evidence"]), 1)
        self.assertIsNone(matrix["verdict"])
        self.assertFalse(matrix["publication_allowed"])
        self.assertIsNone(matrix["evidence"][0]["contradicts_claim"])
    def test_empty_claim_rejected(self):
        with self.assertRaises(ValueError):
            assemble_matrix("  ", [])

    def test_url_whitespace_deduplicated(self):
        matrix = assemble_matrix('Cifra 2025', [{'url':' https://example.org/a '}, {'url':'https://example.org/a'}])
        self.assertEqual(len(matrix['evidence']), 1)

    def test_sources_must_be_list(self):
        with self.assertRaises(TypeError):
            assemble_matrix('Cifra 2025', None)
