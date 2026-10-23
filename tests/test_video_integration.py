"""Prueba de integración: crea y analiza un MP4 real si FFmpeg está instalado."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from src.video import create_preview
from src.quality_gate import inspect_video

@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),
                     "FFmpeg/FFprobe no instalados")
class VideoIntegrationTests(unittest.TestCase):
    def test_render_and_probe(self):
        with tempfile.TemporaryDirectory() as tmp:
            dossiers = Path(tmp) / "dossiers.json"
            video = Path(tmp) / "preview.mp4"
            dossiers.write_text(json.dumps({"dossiers": []}), encoding="utf-8")
            create_preview(str(dossiers), str(video))
            result = inspect_video(video)
            self.assertTrue(result["technical_pass"])
            self.assertFalse(result["public_upload_allowed"])
            self.assertGreater(video.stat().st_size, 1000)
