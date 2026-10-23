import unittest
from src.source_audit import audit_sources
from src.report import build_report

class TestAudit(unittest.TestCase):
    def test_no_sources(self):
        self.assertIn("insufficient_distinct_domains", audit_sources([]))
    def test_http_rejected(self):
        s = [{"url": "http://example.com", "publisher": "A", "quote": "c", "accessed_at": "2026-10-23"}]
        self.assertIn("invalid_https_url", audit_sources(s))
    def test_duplicate_domain(self):
        s = [{"url": "https://example.org/a", "publisher": "A", "quote": "c", "accessed_at": "2026-10-23"},
             {"url": "https://example.org/b", "publisher": "B", "quote": "c", "accessed_at": "2026-10-23"}]
        self.assertIn("duplicate_domain", audit_sources(s))
    def test_never_publish(self):
        self.assertFalse(build_report({"claim": "Afirmación de prueba", "sources": []})["publication_allowed"])
