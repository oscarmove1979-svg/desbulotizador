"""Motor determinista inicial: solo produce un guion si hay evidencias auditables."""
import json
from pathlib import Path

def evaluate(case):
    claim = str(case.get("claim", "")).strip()
    sources = case.get("sources", [])
    if not claim:
        return {"status": "blocked", "reason": "missing_claim"}
    if not isinstance(sources, list) or len(sources) < 2:
        return {"status": "blocked", "reason": "insufficient_sources"}
    valid = [s for s in sources if isinstance(s, dict) and
             s.get("url", "").startswith("https://") and
             s.get("publisher") and s.get("quote") and s.get("accessed_at")]
    publishers = {s["publisher"].casefold().strip() for s in valid}
    if len(valid) < 2 or len(publishers) < 2:
        return {"status": "blocked", "reason": "sources_not_independent"}
    # La existencia de dos citas NO demuestra la veracidad de la conclusión.
    return {"status": "needs_editorial_verification",
            "claim": claim, "sources": valid,
            "reason": "evidence_requires_independent_fact_check"}

if __name__ == "__main__":
    case = json.loads(Path("examples/case.json").read_text(encoding="utf-8"))
    result = evaluate(case)
    Path("output").mkdir(exist_ok=True)
    Path("output/result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
