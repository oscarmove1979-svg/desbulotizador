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
