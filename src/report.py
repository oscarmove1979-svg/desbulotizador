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

if __name__ == "__main__":
    case = json.loads(Path("examples/case.json").read_text(encoding="utf-8"))
    report = build_report(case)
    Path("output").mkdir(exist_ok=True)
    Path("output/report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": report["status"], "publication_allowed": False}))
