"""Preparación de narración: no usa servicios ni claves de pago."""
import json
from pathlib import Path

def narration_plan(report):
    if report.get("publication_allowed") is not False:
        raise ValueError("Unsafe report")
    for record in report.get("pending_claims", []):
        if not isinstance(record, dict) or record.get("publication_allowed") is not False or record.get("status") != "unverified":
            raise ValueError("Unsafe research claim")
    return {
        "language": "es-ES",
        "style": "periodismo explicativo, pausado y natural",
        "script": "desBULOtizador. Esta es una demostración técnica. "
                  "Todavía no se ha verificado ninguna afirmación política.",
        "voice_generated": False,
        "public_upload_allowed": False
    }

if __name__ == "__main__":
    report = json.loads(Path("output/report.json").read_text(encoding="utf-8"))
    plan = narration_plan(report)
    Path("output/voice_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
