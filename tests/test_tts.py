import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys
import types
from src.tts import synthesize

class TTSTests(unittest.IsolatedAsyncioTestCase):
    async def test_rejects_unsafe_plan_before_network(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "plan.json"
            p.write_text(json.dumps({"public_upload_allowed": True, "script": "hola"}))
            with self.assertRaises(ValueError):
                await synthesize(str(p), str(Path(d) / "voice.mp3"))

    async def test_empty_script_rejected_before_import(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "plan.json"
            p.write_text(json.dumps({"public_upload_allowed": False, "script": ""}))
            with self.assertRaises(ValueError):
                await synthesize(str(p), str(Path(d) / "voice.mp3"))

    async def test_network_failure_removes_partial_audio(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "plan.json"
            audio = Path(d) / "voice.mp3"
            p.write_text(json.dumps({"public_upload_allowed": False, "script": "Prueba de voz"}))
            class BrokenVoice:
                def __init__(self, *args):
                    pass
                async def save(self, destination):
                    Path(destination).write_bytes(b"partial")
                    raise RuntimeError("offline")
            fake = types.SimpleNamespace(Communicate=BrokenVoice)
            with patch.dict(sys.modules, {"edge_tts": fake}):
                with self.assertRaises(RuntimeError):
                    await synthesize(str(p), str(audio))
            self.assertFalse(audio.exists())
