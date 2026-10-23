import unittest
from unittest.mock import patch
from src.voice_job import run

class VoiceJobTests(unittest.IsolatedAsyncioTestCase):
    @patch("src.voice_job.synthesize", side_effect=RuntimeError("network"))
    async def test_network_failure_is_explicit(self, _):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as d:
            with patch("src.voice_job.Path", wraps=Path):
                with patch("src.voice_job.synthesize", side_effect=RuntimeError("network")):
                    # The status file is written to output/ in the workflow.
                    result = await run()
        self.assertEqual(result["voice_status"], "failed")
        self.assertFalse(result["publication_allowed"])
