import unittest
from src.voice import narration_plan

class VoiceTests(unittest.TestCase):
    def test_plan_is_not_audio(self):
        p = narration_plan({"publication_allowed": False})
        self.assertFalse(p["voice_generated"])
        self.assertEqual(p["language"], "es-ES")
    def test_unsafe_report(self):
        with self.assertRaises(ValueError):
            narration_plan({"publication_allowed": True})

    def test_unsafe_pending_claim(self):
        report = {'publication_allowed':False,'pending_claims':[{'status':'unverified','publication_allowed':True}]}
        with self.assertRaises(ValueError):
            narration_plan(report)

    def test_narration_reflects_pending_count(self):
        claim = {'status':'unverified','publication_allowed':False}
        plan = narration_plan({'publication_allowed':False,'pending_claims':[claim,claim]})
        self.assertIn('2 afirmaciones', plan['script'])
        self.assertFalse(plan['public_upload_allowed'])

    def test_empty_research_narration(self):
        plan = narration_plan({'publication_allowed':False,'pending_claims':[]})
        self.assertEqual(plan['research_claim_count'], 0)
        self.assertIn('No se han encontrado', plan['script'])
        self.assertFalse(plan['editorial_approval'])
