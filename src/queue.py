"""Cola de investigación sin afirmar falsedades ni publicar."""
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

def normalize(candidate):
    if not isinstance(candidate, dict):
        return None
    url = candidate.get("url")
    title = candidate.get("title")
    if not isinstance(url, str) or not isinstance(title, str):
        return None
    url = url.strip()
    title = title.strip()
    if len(url) > 2048 or any(ord(ch) < 32 or ord(ch) == 127 for ch in url):
        return None
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
    for raw in (discovery.get("candidates") if isinstance(discovery.get("candidates"), list) else []):
        if not isinstance(raw, dict):
            continue
        item = normalize(raw)
        if item and item["id"] not in seen:
            seen.add(item["id"])
            queue.append(item)
    return {"items": queue, "publication_enabled": False}

if __name__ == "__main__":
    raw = json.loads(Path("output/discovery.json").read_text(encoding="utf-8"))
    Path("output/queue.json").write_text(json.dumps(build_queue(raw), ensure_ascii=False, indent=2), encoding="utf-8")
