"""Genera un informe de revisión; nunca emite un veredicto político automático."""
import json
from pathlib import Path
from src.desbulotizador import evaluate
from src.source_audit import audit_sources

def build_report(case):
    base = evaluate(case)
    sources = case.get("sources", [])
    audit = audit_sources(sources if isinstance(sources, list) else [])
    return {
        "project": "desBULOtizador",
        "publication_allowed": False,
        "status": "blocked" if base["status"] == "blocked" or audit else "pending_human_fact_check",
        "claim": case.get("claim", ""),
        "source_audit": audit,
        "evaluation": base,
        "disclaimer": "Las citas y dominios no prueban por sí solos una afirmación.",
    }


def build_pipeline_report(dossiers):
    """Summarize live research candidates without producing a factual verdict."""
    cases = dossiers.get("dossiers", [])
    if not isinstance(cases, list):
        raise ValueError("Invalid dossier collection")
    pending = []
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("Invalid dossier")
        for claim in case.get("claims", []):
            pending.append({"dossier_id": case.get("id"),
                            "claim": claim["text"],
                            "source_url": case.get("source_url"),
                            "status": "unverified",
                            "publication_allowed": False})
    return {"project": "desBULOtizador", "status": "pending_human_fact_check",
            "publication_allowed": False, "pending_claims": pending,
            "disclaimer": "Candidatos sin verificación editorial; no son bulos demostrados."}

if __name__ == "__main__":
    dossiers = json.loads(Path("output/dossiers.json").read_text(encoding="utf-8"))
    report = build_pipeline_report(dossiers)
    Path("output").mkdir(exist_ok=True)
    Path("output/report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": report["status"], "publication_allowed": False}))
