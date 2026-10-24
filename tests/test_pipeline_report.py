import unittest
from src.report import build_pipeline_report

class PipelineReportTests(unittest.TestCase):
    def test_empty(self):
        report = build_pipeline_report({'dossiers':[]})
        self.assertEqual(report['pending_claims'], [])
        self.assertFalse(report['publication_allowed'])

    def test_candidate_report(self):
        sample = dict(id='abc', source_url='https://example.org', claims=[dict(text='Dato 2025')])
        report = build_pipeline_report(dict(dossiers=[sample]))
        self.assertEqual(report['pending_claims'][0]['status'], 'unverified')

    def test_invalid_claim_is_skipped(self):
        with self.assertRaises(ValueError):
            build_pipeline_report({'dossiers':[{'claims':[None]}]})

    def test_empty_status(self):
        self.assertEqual(build_pipeline_report({'dossiers':[]})['status'], 'no_claims_found')

    def test_invalid_claim_collection_is_rejected(self):
        with self.assertRaises(ValueError):
            build_pipeline_report({'dossiers':[{'claims':None}]})
