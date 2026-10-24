"""Métricas de proceso sin confundir candidatos con bulos."""
import json
from pathlib import Path

def summarize(discovery, queue, dossiers, quality=None):
    candidates = discovery.get("candidates", [])
    if not isinstance(candidates, list):
        candidates = []
    queued = queue.get("items", [])
    if not isinstance(queued, list):
        queued = []
    cases = dossiers.get("dossiers", [])
    if not isinstance(cases, list):
        cases = []
    return {
        "candidate_count": len(candidates),
        "queue_count": len(queued),
        "dossier_count": len(cases),
        "claims_pending_review": sum(len(case.get("claims", [])) for case in cases if isinstance(case, dict) and isinstance(case.get("claims", []), list)),
        "evidence_records": sum(len(matrix.get("evidence", [])) for case in cases if isinstance(case, dict) for matrix in (case.get("evidence_matrices") or []) if isinstance(matrix, dict)),
        "source_errors": len(discovery.get("errors", [])),
        "verified_bulos": 0,
        "videos_published": 0,
        "technical_video_ok": bool((quality or {}).get("technical_pass", False)),
        "publication_allowed": False,
    }

if __name__ == "__main__":
    base = Path("output")
    def read(name):
        return json.loads((base / name).read_text(encoding="utf-8"))
    data = summarize(read("discovery.json"), read("queue.json"), read("dossiers.json"), read("video_quality.json"))
    (base / "metrics.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(data, ensure_ascii=False))
