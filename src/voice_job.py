"""Ejecuta síntesis opcional, registra resultados verificables y no publica."""
import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from src.tts import synthesize
from src.mux import add_voice
from src.quality_gate import inspect_video

async def run():
    status = {"attempted_at": datetime.now(timezone.utc).isoformat(),
              "voice_status": "not_attempted", "narrated_video_valid": False,
              "publication_allowed": False}
    try:
        for stale in ("output/preview_narrated.mp4", "output/voice.mp3"):
            Path(stale).unlink(missing_ok=True)
        await synthesize()
        status["voice_status"] = "audio_generated"
        add_voice()
        checked = inspect_video("output/preview_narrated.mp4", require_audio=True)
        status["narrated_video_valid"] = checked["technical_pass"]
        if not checked["technical_pass"]:
            raise ValueError("Narrated video failed technical validation")
        status["voice_status"] = "success"
        status["duration_seconds"] = checked["duration_seconds"]
        status["editorial_approval"] = False
    except Exception as exc:
        status["voice_status"] = "failed"
        status["narrated_video_valid"] = False
        status["editorial_approval"] = False
        status["error_type"] = type(exc).__name__
        status["error_message"] = str(exc)[:300]
        for partial in ("output/preview_narrated.mp4", "output/voice.mp3"):
            Path(partial).unlink(missing_ok=True)
    finally:
        Path("output").mkdir(exist_ok=True)
        Path("output/voice_status.json").write_text(
            json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
    return status

if __name__ == "__main__":
    print(json.dumps(asyncio.run(run()), ensure_ascii=False))
