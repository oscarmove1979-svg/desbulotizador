"""Modelo de evidencia: nunca interpreta una URL como prueba suficiente."""
from datetime import datetime
from urllib.parse import urlsplit

def validate_evidence(record):
    errors = []
    if not isinstance(record, dict):
        return ["not_an_object"]
    url = record.get("url", "")
    parts = urlsplit(url) if isinstance(url, str) else None
    if not parts or parts.scheme != "https" or not parts.hostname:
        errors.append("invalid_https_url")
    for key in ("publisher", "quote", "accessed_at", "claim_id"):
        if not isinstance(record.get(key), str) or not record[key].strip():
            errors.append("missing_" + key)
    date = record.get("accessed_at")
    if isinstance(date, str) and date:
        try:
            datetime.fromisoformat(date.replace("Z", "+00:00"))
        except ValueError:
            errors.append("invalid_access_date")
    return errors

def evidence_summary(records):
    if not isinstance(records, list):
        return {"valid_records": 0, "errors": ["records_not_list"],
                "fact_checked": False, "publication_allowed": False}
    errors = []
    valid = 0
    for i, record in enumerate(records):
        problems = validate_evidence(record)
        if problems:
            errors.append({"index": i, "issues": problems})
        else:
            valid += 1
    return {"valid_records": valid, "errors": errors,
            "fact_checked": False, "publication_allowed": False}
