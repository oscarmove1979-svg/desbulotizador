import unittest
from src.guardrails import validate_queue

class GuardrailsTests(unittest.TestCase):
    def test_empty_safe(self):
        self.assertTrue(validate_queue({"publication_enabled": False, "items": []}))
    def test_publication_rejected(self):
        with self.assertRaises(ValueError):
            validate_queue({"publication_enabled": True, "items": []})
    def test_publishable_rejected(self):
        with self.assertRaises(ValueError):
            validate_queue({"publication_enabled": False, "items": [{"publishable": True}]})
