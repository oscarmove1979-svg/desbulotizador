import unittest
from src.queue import build_queue
from src.dossier import build_dossiers
from src.report import build_pipeline_report
from src.voice import narration_plan
from src.review_board import render_board
from src.safety_audit import validate_artifacts

class PipelineIntegrationTests(unittest.TestCase):
    def test_research_flow_without_network(self):
        discovery = {'candidates':[{'title':'La cifra de 2025 supera la de 2024 en el informe','url':'https://example.org/report'}]}
        queue = build_queue(discovery)
        dossiers = build_dossiers(queue)
        report = build_pipeline_report(dossiers)
        voice = narration_plan(report)
        board = render_board(report)
        self.assertTrue(validate_artifacts(dossiers, voice, report))
        self.assertEqual(len(report['pending_claims']), 1)
        self.assertIn('NO VERIFICADO', board)
        self.assertFalse(voice['public_upload_allowed'])

    def test_empty_research_flow(self):
        dossiers = build_dossiers(build_queue({'candidates':[]}))
        report = build_pipeline_report(dossiers)
        voice = narration_plan(report)
        self.assertTrue(validate_artifacts(dossiers, voice, report))
        self.assertEqual(report['status'], 'no_claims_found')
        self.assertIn('No hay afirmaciones', render_board(report))
