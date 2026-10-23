import unittest
from src.queue import build_queue

class QueueTests(unittest.TestCase):
    def test_deduplication(self):
        x = {"title": "Ejemplo", "url": "https://example.org/a"}
        q = build_queue({"candidates": [x, x]})
        self.assertEqual(len(q["items"]), 1)
        self.assertFalse(q["items"][0]["publishable"])
    def test_invalid(self):
        self.assertEqual(build_queue({"candidates": [{"title": "X", "url": "http://invalid"}]})["items"], [])
    def test_empty(self):
        self.assertEqual(build_queue({})["items"], [])
