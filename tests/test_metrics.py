import unittest
from src.metrics import summarize

class MetricsTests(unittest.TestCase):
    def test_counts_not_verdicts(self):
        r = summarize({"candidates":[{"title":"x"}],"errors":[]},
                      {"items":[{"id":"1"}]}, {"dossiers":[]})
        self.assertEqual(r["candidate_count"], 1)
        self.assertEqual(r["verified_bulos"], 0)
        self.assertFalse(r["publication_allowed"])
