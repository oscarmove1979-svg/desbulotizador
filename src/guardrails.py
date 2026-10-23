"""Falla de forma segura si la cola habilita publicación."""
import json
from pathlib import Path

def validate_queue(queue):
    if queue.get("publication_enabled") is not False:
        raise ValueError("Publication must remain disabled")
    for item in queue.get("items", []):
        if item.get("publishable") is not False:
            raise ValueError("Unverified candidate cannot be publishable")
        if item.get("state") != "candidate_unverified":
            raise ValueError("Unexpected candidate state")
    return True

if __name__ == "__main__":
    validate_queue(json.loads(Path("output/queue.json").read_text(encoding="utf-8")))
    print("Guardrails: OK")
