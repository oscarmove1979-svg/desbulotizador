import unittest
from src.safety_audit import validate_artifacts

class MatrixConsistencyTests(unittest.TestCase):
    def test_missing_matrix(self):
        dossier = {'publication_allowed': False, 'verdict': None, 'claims': [{'text':'2025 data','verdict':'unverified','publishable':False}], 'evidence_matrices': []}
        with self.assertRaises(ValueError):
            validate_artifacts({'publication_allowed':False,'dossiers':[dossier]}, {'public_upload_allowed':False}, {'publication_allowed':False})

    def test_wrong_matrix_claim(self):
        dossier = {'publication_allowed': False, 'verdict': None, 'claims': [{'text':'2025 data','verdict':'unverified','publishable':False}], 'evidence_matrices': [{'claim':'other text','publication_allowed':False,'verdict':None}]}
        with self.assertRaises(ValueError):
            validate_artifacts({'publication_allowed':False,'dossiers':[dossier]}, {'public_upload_allowed':False}, {'publication_allowed':False})
