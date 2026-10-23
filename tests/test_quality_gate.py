import unittest
from src.quality_gate import inspect_video

class QualityTests(unittest.TestCase):
    def test_missing(self):
        with self.assertRaises(ValueError):
            inspect_video("missing-video-file.mp4")
