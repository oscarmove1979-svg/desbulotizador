import unittest
from src.report import build_pipeline_report

class PipelineReportTests(unittest.TestCase):
    def test_empty(self):
        report = build_pipeline_report({'dossiers':[]})
        self.assertEqual(report['pending_claims'], [])
        self.assertFalse(report['publication_allowed'])
