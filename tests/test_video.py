import unittest
from unittest.mock import patch
from src.video import create_preview

class VideoTests(unittest.TestCase):
    @patch("src.video.shutil.which", return_value=None)
    def test_missing_ffmpeg(self, _):
        with self.assertRaises(RuntimeError):
            create_preview()

    @patch("src.video.shutil.which", return_value="/usr/bin/ffmpeg")
    def test_rejects_unsafe_dossiers(self, _):
        import json
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/"dossiers.json"
            source.write_text(json.dumps({"dossiers":[],"publication_allowed":True}),encoding="utf-8")
            with self.assertRaises(ValueError):
                create_preview(str(source),str(Path(folder)/"preview.mp4"))

    @patch("src.video.shutil.which", return_value="/usr/bin/ffmpeg")
    def test_rejects_invalid_dossier_list(self, _):
        import json
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/"dossiers.json"
            source.write_text(json.dumps({"dossiers":{},"publication_allowed":False}),encoding="utf-8")
            with self.assertRaises(ValueError):
                create_preview(str(source),str(Path(folder)/"preview.mp4"))
