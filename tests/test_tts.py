import json
import tempfile
import unittest
from pathlib import Path
from src.tts import synthesize

class TTSTests(unittest.IsolatedAsyncioTestCase):
    async def test_rejects_unsafe_plan_before_network(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "plan.json"
            p.write_text(json.dumps({"public_upload_allowed": True, "script": "hola"}))
            with self.assertRaises(ValueError):
                await synthesize(str(p), str(Path(d) / "voice.mp3"))
