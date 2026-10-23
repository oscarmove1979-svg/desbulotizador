"""Bloquea expedientes y planes de voz que habiliten publicación."""
import json
from pathlib import Path

def validate_artifacts(dossiers, voice, report):
    if dossiers.get("publication_allowed") is not False:
        raise ValueError("Dossier publication flag must be false")
    if voice.get("public_upload_allowed") is not False:
        raise ValueError("Voice publication flag must be false")
    if report.get("publication_allowed") is not False:
        raise ValueError("Report publication flag must be false")
    for case in dossiers.get("dossiers", []):
        if case.get("publication_allowed") is not False:
            raise ValueError("Case publication flag must be false")
        if case.get("verdict") is not None:
            raise ValueError("Automated verdict not permitted")
    return True

if __name__ == "__main__":
    base = Path("output")
    def load(name):
        return json.loads((base / name).read_text(encoding="utf-8"))
    validate_artifacts(load("dossiers.json"), load("voice_plan.json"), load("report.json"))
    print("Editorial publication safety: OK")
