import unittest
from src.mux import add_voice

class MuxTests(unittest.TestCase):
    def test_missing_inputs(self):
        with self.assertRaises((FileNotFoundError, RuntimeError)):
            add_voice("nonexistent-video.mp4", "nonexistent-audio.mp3", "unused.mp4")
