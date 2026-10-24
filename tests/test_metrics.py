import unittest
from src.metrics import summarize

class MetricsTests(unittest.TestCase):
    def test_counts_not_verdicts(self):
        r = summarize({"candidates":[{"title":"x"}],"errors":[]},
                      {"items":[{"id":"1"}]}, {"dossiers":[]})
        self.assertEqual(r["candidate_count"], 1)
        self.assertEqual(r["verified_bulos"], 0)
        self.assertFalse(r["publication_allowed"])

    def test_counts_pending_claims_and_evidence(self):
        dossiers = {"dossiers": [{"claims": [{"text": "dato 2025"}],
            "evidence_matrices": [{"evidence": [{"url": "https://example.org"}]}]}]}
        result = summarize({"candidates": [], "errors": []}, {"items": []}, dossiers)
        self.assertEqual(result["claims_pending_review"], 1)
        self.assertEqual(result["evidence_records"], 1)
        self.assertEqual(result["verified_bulos"], 0)

    def test_invalid_collections_do_not_crash(self):
        result = summarize({'candidates':None,'errors':[]}, {'items':None}, {'dossiers':None})
        self.assertEqual(result['candidate_count'], 0)
        self.assertEqual(result['claims_pending_review'], 0)
        self.assertFalse(result['publication_allowed'])

    def test_invalid_nested_evidence(self):
        case = {'claims':None,'evidence_matrices':[None,{'evidence':None}]}
        result = summarize({'candidates':[],'errors':None},{'items':[]},{'dossiers':[case]})
        self.assertEqual(result['evidence_records'], 0)
        self.assertEqual(result['source_errors'], 0)
