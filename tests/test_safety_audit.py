import unittest
from src.safety_audit import validate_artifacts

class SafetyAuditTests(unittest.TestCase):
    def test_safe(self):
        self.assertTrue(validate_artifacts(
            {"publication_allowed": False, "dossiers": []},
            {"public_upload_allowed": False},
            {"publication_allowed": False}))
    def test_verdict_rejected(self):
        with self.assertRaises(ValueError):
            validate_artifacts(
                {"publication_allowed": False, "dossiers": [
                    {"publication_allowed": False, "verdict": "false"}]},
                {"public_upload_allowed": False},
                {"publication_allowed": False})

    def test_matrix_verdict_rejected(self):
        with self.assertRaises(ValueError):
            validate_artifacts(
                {"publication_allowed": False, "dossiers": [{
                    "publication_allowed": False, "verdict": None,
                    "evidence_matrices": [{"publication_allowed": False, "verdict": "false"}]}]},
                {"public_upload_allowed": False},
                {"publication_allowed": False})

    def test_publishable_claim_rejected(self):
        with self.assertRaises(ValueError):
            validate_artifacts(
                {"publication_allowed": False, "dossiers": [{
                    "publication_allowed": False, "verdict": None,
                    "claims": [{"text": "Cifra de 2025", "verdict": "unverified",
                                "publishable": True}]}]},
                {"public_upload_allowed": False},
                {"publication_allowed": False})

    def test_voice_editorial_approval_rejected(self):
        with self.assertRaises(ValueError):
            validate_artifacts({'publication_allowed':False,'dossiers':[]}, {'public_upload_allowed':False,'editorial_approval':True}, {'publication_allowed':False})
