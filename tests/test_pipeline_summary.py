import unittest
from src.pipeline_summary import summarize_status

class SummaryTests(unittest.TestCase):
    def test_successful_audio_never_enables_publication(self):
        r = summarize_status({"voice_status": "success", "narrated_video_valid": True},
                             {"technical_pass": True}, {"candidate_count": 4, "dossier_count": 1})
        self.assertTrue(r["video_has_audio"])
        self.assertFalse(r["ready_for_publication"])
        self.assertFalse(r["youtube_upload_enabled"])
