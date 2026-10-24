import unittest
from src.editorial_checklist import build_checklist

class EditorialChecklistTests(unittest.TestCase):
    def test_questions_are_unchecked(self):
        record={"dossier_id":"x","claim":"Dato 2025","source_url":"https://example.org","status":"unverified","publication_allowed":False}
        result=build_checklist({"publication_allowed":False,"pending_claims":[record]})
        item=result["items"][0]
        self.assertFalse(item["human_approval"])
        self.assertIsNone(item["verdict"])
        self.assertTrue(all(not q["checked"] for q in item["questions"]))
        self.assertFalse(result["publication_allowed"])

    def test_unsafe_report_is_rejected(self):
        with self.assertRaises(ValueError):
            build_checklist({"publication_allowed":True,"pending_claims":[]})

    def test_empty_report(self):
        self.assertEqual(build_checklist({"publication_allowed":False,"pending_claims":[]})["items"],[])

    def test_missing_claim_rejected(self):
        record={"dossier_id":"x","claim":"","source_url":"https://example.org","status":"unverified","publication_allowed":False}
        with self.assertRaises(ValueError):
            build_checklist({"publication_allowed":False,"pending_claims":[record]})

    def test_insecure_source_rejected(self):
        record={"dossier_id":"x","claim":"Dato 2025","source_url":"http://example.org","status":"unverified","publication_allowed":False}
        with self.assertRaises(ValueError):
            build_checklist({"publication_allowed":False,"pending_claims":[record]})
