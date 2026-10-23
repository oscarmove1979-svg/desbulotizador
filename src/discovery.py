"""Descubrimiento de candidatos desde RSS público; nunca emite veredictos."""
import json
import os
import urllib.request
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_FEEDS = [
    "https://www.boe.es/rss/boe.php",
]

def fetch_feed(url, timeout=12):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("URL HTTPS válida requerida")
    req = urllib.request.Request(url, headers={"User-Agent": "desBULOtizador/0.1 (research prototype)"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        final = urlsplit(response.geturl()) if hasattr(response, "geturl") else parsed
        if final.scheme != "https" or not final.hostname or final.username or final.password:
            raise ValueError("Redirección fuera de HTTPS")
        data = response.read(2_000_001)
        if len(data) > 2_000_000:
            raise ValueError("RSS demasiado grande")
    root = ET.fromstring(data)
    items = []
    for item in root.findall(".//item")[:20]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if title and urlsplit(link).scheme == "https" and urlsplit(link).hostname:
            items.append({"title": title, "url": link, "feed": url})
    atom = "{http://www.w3.org/2005/Atom}"
    for entry in root.findall(f".//{atom}entry")[:20]:
        title = (entry.findtext(f"{atom}title") or "").strip()
        links = entry.findall(f"{atom}link")
        link = next((node.get("href", "") for node in links
                     if node.get("rel", "alternate") == "alternate"
                     and urlsplit(node.get("href", "")).scheme == "https"
                     and urlsplit(node.get("href", "")).hostname), "")
        if title and link:
            items.append({"title": title, "url": link, "feed": url})
    return items

def discover(feeds=None):
    result = {"generated_at": datetime.now(timezone.utc).isoformat(), "candidates": [], "errors": [],
              "note": "Candidatos informativos, NO bulos verificados."}
    for url in (feeds or DEFAULT_FEEDS):
        try:
            result["candidates"].extend(fetch_feed(url))
        except Exception as exc:
            result["errors"].append({"feed": url, "error": type(exc).__name__})
    unique = {entry["url"]: entry for entry in result["candidates"]}
    result["candidates"] = list(unique.values())[:50]
    return result

if __name__ == "__main__":
    feeds = [v.strip() for v in os.getenv("RSS_FEEDS", "").split(",") if v.strip()]
    result = discover(feeds or None)
    Path("output").mkdir(exist_ok=True)
    Path("output/discovery.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Candidatos: {len(result['candidates'])}; errores: {len(result['errors'])}")
