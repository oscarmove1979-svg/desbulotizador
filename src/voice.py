"""Preparación de narración: no usa servicios ni claves de pago."""
import json
from pathlib import Path

def narration_plan(report):
    if report.get("publication_allowed") is not False:
        raise ValueError("Unsafe report")
    pending = report.get("pending_claims", [])
    if not isinstance(pending, list):
        raise ValueError("Invalid pending claims")
    for record in pending:
        if not isinstance(record, dict) or record.get("publication_allowed") is not False or record.get("status") != "unverified":
            raise ValueError("Unsafe research claim")
    count = len(pending)
    script = ("desBULOtizador. Se han detectado " + str(count) +
              " afirmaciones para investigar. Ninguna ha sido verificada y "
              "no se publicará ningún desmentido sin comprobar las fuentes."
              if count else "desBULOtizador. No se han encontrado afirmaciones "
              "para investigar en esta ejecución. Esta es una prueba técnica.")
    return {
        "language": "es-ES",
        "style": "periodismo explicativo, pausado y natural",
        "script": script,
        "voice_generated": False,
        "editorial_approval": False,
        "public_upload_allowed": False
    }

if __name__ == "__main__":
    report = json.loads(Path("output/report.json").read_text(encoding="utf-8"))
    plan = narration_plan(report)
    Path("output/voice_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
