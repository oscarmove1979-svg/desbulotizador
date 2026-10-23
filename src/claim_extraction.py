"""Extracción conservadora de afirmaciones: no infiere veracidad."""
import re

def extract_claims(text):
    if not isinstance(text, str):
        return []
    candidates = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    results = []
    for fragment in candidates:
        fragment = " ".join(fragment.split())
        if len(fragment) < 20 or len(fragment) > 450:
            continue
        if re.search(r"\b\d+(?:[,.]\d+)?\s*%|\b\d{4}\b", fragment):
            results.append({"text": fragment, "verdict": "unverified", "publishable": False})
    return results[:10]
