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

    def test_invalid_claim_object(self):
        case = {'publication_allowed':False,'verdict':None,'claims':[None],'evidence_matrices':[{}]}
        with self.assertRaises(ValueError):
            validate_artifacts({'publication_allowed':False,'dossiers':[case]}, {'public_upload_allowed':False}, {'publication_allowed':False})

    def test_invalid_matrix(self):
        case = dict(publication_allowed=False, verdict=None, claims=[dict(text='Dato 2025',publishable=False,verdict='unverified')], evidence_matrices=[None])
        with self.assertRaises(ValueError):
            validate_artifacts(dict(publication_allowed=False,dossiers=[case]), dict(public_upload_allowed=False), dict(publication_allowed=False))

    def test_report_claim_cannot_be_publishable(self):
        report = {'publication_allowed':False,'pending_claims':[{'status':'unverified','publication_allowed':True}]}
        with self.assertRaises(ValueError):
            validate_artifacts({'publication_allowed':False,'dossiers':[]}, {'public_upload_allowed':False}, report)
