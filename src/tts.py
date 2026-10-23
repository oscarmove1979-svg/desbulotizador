"""Síntesis experimental en español mediante edge-tts (servicio externo no garantizado)."""
import asyncio
import json
from pathlib import Path

async def synthesize(plan_path="output/voice_plan.json", audio_path="output/voice.mp3"):
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    if plan.get("public_upload_allowed") is not False:
        raise ValueError("La publicación debe estar bloqueada")
    script = plan.get("script", "").strip()
    if not script or len(script) > 2000:
        raise ValueError("Guion vacío o excesivo")
    import edge_tts
    destination = Path(audio_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    await edge_tts.Communicate(script, "es-ES-AlvaroNeural").save(str(destination))
    if destination.stat().st_size < 1000:
        raise RuntimeError("Audio vacío")
    return str(destination)

if __name__ == "__main__":
    print(asyncio.run(synthesize()))
