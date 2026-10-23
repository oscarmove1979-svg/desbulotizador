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
