"""Métricas de proceso sin confundir candidatos con bulos."""
import json
from pathlib import Path

def summarize(discovery, queue, dossiers, quality=None):
    candidates = discovery.get("candidates", [])
    queued = queue.get("items", [])
    cases = dossiers.get("dossiers", [])
    return {
        "candidate_count": len(candidates),
        "queue_count": len(queued),
        "dossier_count": len(cases),
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
