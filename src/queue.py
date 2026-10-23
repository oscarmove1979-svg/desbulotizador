"""Cola de investigación sin afirmar falsedades ni publicar."""
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

def normalize(candidate):
    url = str(candidate.get("url", "")).strip()
    title = str(candidate.get("title", "")).strip()
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username
            or parsed.password or not title):
        return None
    return {"id": hashlib.sha256(url.encode()).hexdigest()[:16],
            "title": title[:500], "url": url,
            "state": "candidate_unverified", "publishable": False}

def build_queue(discovery):
    queue = []
    seen = set()
    for raw in discovery.get("candidates", []):
        item = normalize(raw)
        if item and item["id"] not in seen:
            seen.add(item["id"])
            queue.append(item)
    return {"items": queue, "publication_enabled": False}

if __name__ == "__main__":
    raw = json.loads(Path("output/discovery.json").read_text(encoding="utf-8"))
    Path("output/queue.json").write_text(json.dumps(build_queue(raw), ensure_ascii=False, indent=2), encoding="utf-8")
