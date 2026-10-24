"""Síntesis experimental en español mediante edge-tts (servicio externo no garantizado)."""
import asyncio
import json
from pathlib import Path

async def synthesize(plan_path="output/voice_plan.json", audio_path="output/voice.mp3"):
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    if plan.get("public_upload_allowed") is not False:
        raise ValueError("La publicación debe estar bloqueada")
    if plan.get("editorial_approval", False) is not False:
        raise ValueError("Aprobación editorial no permitida")
    script = plan.get("script", "").strip()
    if not script or len(script) > 2000:
        raise ValueError("Guion vacío o excesivo")
    import edge_tts
    destination = Path(audio_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        await edge_tts.Communicate(script, "es-ES-AlvaroNeural").save(str(destination))
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    if not destination.exists() or destination.stat().st_size < 1000:
        destination.unlink(missing_ok=True)
        raise RuntimeError("Audio vacío")
    return str(destination)

if __name__ == "__main__":
    print(asyncio.run(synthesize()))
