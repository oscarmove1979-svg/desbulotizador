"""Matriz de evidencias: evita conclusiones automáticas."""
from datetime import datetime, timezone
from urllib.parse import urlsplit

def assemble_matrix(claim, sources):
    if not isinstance(claim, str) or not claim.strip():
        raise ValueError("Afirmación obligatoria")
    if not isinstance(sources, list):
        raise TypeError("Las fuentes deben ser una lista")
    records = []
    seen = set()
    for source in sources:
        if not isinstance(source, dict):
            continue
        url = str(source.get("url", ""))
        parsed = urlsplit(url)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            continue
        if url in seen:
            continue
        seen.add(url)
        records.append({
            "url": url,
            "publisher": str(source.get("publisher", "")).strip(),
            "retrieved_at": source.get("retrieved_at"),
            "excerpt": str(source.get("excerpt", "")).strip()[:1200],
            "supports_claim": None,
            "contradicts_claim": None,
            "human_reviewed": False,
        })
    return {
        "claim": claim.strip(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "evidence": records,
        "status": "requires_manual_fact_check",
        "verdict": None,
        "publication_allowed": False,
    }
