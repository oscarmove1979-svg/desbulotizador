import unittest
from src.safety_audit import validate_artifacts

class EvidenceSafetyTests(unittest.TestCase):
    def test_rejects_automatic_evidence_assessment(self):
        claim = {'text':'Dato 2025','verdict':'unverified','publishable':False}
        matrix = {'claim':'Dato 2025','verdict':None,'publication_allowed':False,'evidence':[{'supports_claim':True,'contradicts_claim':None,'human_reviewed':False}]}
        case = {'id':'one','source_url':'https://example.org','publication_allowed':False,'verdict':None,'claims':[claim],'evidence_matrices':[matrix]}
        record = {'dossier_id':'one','source_url':'https://example.org','claim':'Dato 2025','status':'unverified','publication_allowed':False}
        with self.assertRaises(ValueError):
            validate_artifacts({'publication_allowed':False,'dossiers':[case]},{'public_upload_allowed':False},{'publication_allowed':False,'pending_claims':[record]})
