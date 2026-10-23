import unittest
from unittest.mock import patch
from src.voice_job import run

class VoiceJobTests(unittest.IsolatedAsyncioTestCase):
    @patch("src.voice_job.synthesize", side_effect=RuntimeError("network"))
    async def test_network_failure_is_explicit(self, _):
        result = await run()
        self.assertEqual(result["voice_status"], "failed")
        self.assertFalse(result["narrated_video_valid"])
        self.assertFalse(result["publication_allowed"])
