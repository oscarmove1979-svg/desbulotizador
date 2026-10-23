"""Comprueba que una narración larga no se corta al final del fondo."""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from src.video import create_preview
from src.mux import add_voice
from src.quality_gate import inspect_video

@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg no disponible")
class MuxIntegrationTests(unittest.TestCase):
    def test_audio_longer_than_video_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            dossier = base / "dossiers.json"
            dossier.write_text(json.dumps({"dossiers": []}), encoding="utf-8")
            video, audio, output = (base / name for name in ("video.mp4", "audio.wav", "narrated.mp4"))
            create_preview(str(dossier), str(video))
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi",
                            "-i", "sine=frequency=440:duration=17", str(audio)],
                           check=True, timeout=60)
            add_voice(str(video), str(audio), str(output))
            checked = inspect_video(output, require_audio=True)
            self.assertGreaterEqual(checked["duration_seconds"], 16)
            self.assertLess(checked["duration_seconds"], 19)
            self.assertFalse(checked["public_upload_allowed"])
