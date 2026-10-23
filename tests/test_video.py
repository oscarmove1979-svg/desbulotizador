import unittest
from unittest.mock import patch
from src.video import create_preview

class VideoTests(unittest.TestCase):
    @patch("src.video.shutil.which", return_value=None)
    def test_missing_ffmpeg(self, _):
        with self.assertRaises(RuntimeError):
            create_preview()
