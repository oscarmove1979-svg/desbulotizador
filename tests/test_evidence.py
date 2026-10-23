import unittest
from src.evidence import validate_evidence, evidence_summary

class EvidenceTests(unittest.TestCase):
    def test_complete_record_still_not_verified(self):
        r = {"url":"https://www.boe.es/", "publisher":"BOE",
             "quote":"Texto literal", "accessed_at":"2026-10-23T12:00:00Z",
             "claim_id":"a1"}
        self.assertEqual(validate_evidence(r), [])
        self.assertFalse(evidence_summary([r])["fact_checked"])
    def test_missing_quote(self):
        r = {"url":"https://example.org", "publisher":"X",
             "accessed_at":"bad", "claim_id":"a"}
        self.assertIn("missing_quote", validate_evidence(r))
        self.assertIn("invalid_access_date", validate_evidence(r))
    def test_non_list(self):
        self.assertFalse(evidence_summary(None)["publication_allowed"])
