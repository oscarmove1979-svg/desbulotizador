"""Expediente de candidatos, con trazabilidad y sin atribuir falsedad."""
import json
from pathlib import Path
from src.claim_extraction import extract_claims
from src.source_registry import classify_source

def build_dossiers(queue):
    dossiers = []
    for item in queue.get("items", []):
        claims = extract_claims(item.get("title", ""))
        if not claims:
            continue
        dossiers.append({
            "id": item["id"],
            "source_url": item["url"],
            "source_classification": classify_source(item["url"]),
            "source_title": item["title"],
            "claims": claims,
            "review_status": "awaiting_primary_sources",
            "verdict": None,
            "publication_allowed": False
        })
    return {"dossiers": dossiers, "publication_allowed": False}

if __name__ == "__main__":
    queue = json.loads(Path("output/queue.json").read_text(encoding="utf-8"))
    Path("output/dossiers.json").write_text(
        json.dumps(build_dossiers(queue), ensure_ascii=False, indent=2), encoding="utf-8")
