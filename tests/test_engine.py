import unittest
from src.desbulotizador import evaluate

class TestEngine(unittest.TestCase):
    def test_no_claim(self):
        self.assertEqual(evaluate({})["status"], "blocked")
    def test_no_sources(self):
        self.assertEqual(evaluate({"claim": "Ejemplo"})["status"], "blocked")
    def test_duplicate_publisher(self):
        s = {"url": "https://example.org/a", "publisher": "Agencia A",
             "quote": "Cita de ejemplo", "accessed_at": "2026-10-23"}
        self.assertEqual(evaluate({"claim": "Ejemplo", "sources": [s, s]})["status"], "blocked")
    def test_two_sources_still_require_review(self):
        a = {"url": "https://example.org/a", "publisher": "A", "quote": "Cita", "accessed_at": "2026-10-23"}
        b = dict(a, publisher="B", url="https://example.net/b")
        self.assertEqual(evaluate({"claim": "Ejemplo", "sources": [a, b]})["status"],
                         "needs_editorial_verification")

if __name__ == "__main__":
    unittest.main()
