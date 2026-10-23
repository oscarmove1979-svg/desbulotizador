"""Validación conservadora de referencias; no determina la verdad."""
from datetime import date
from urllib.parse import urlparse
import ipaddress

def audit_sources(sources):
    findings = []
    seen = set()
    for source in sources:
        if not isinstance(source, dict):
            findings.append("invalid_record")
            continue
        url = str(source.get("url", ""))
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        try:
            ipaddress.ip_address(hostname)
            findings.append("ip_address_not_allowed")
        except ValueError:
            pass
        if parsed.scheme != "https" or not hostname or "." not in hostname or parsed.username:
            findings.append("invalid_https_url")
        if hostname in seen:
            findings.append("duplicate_domain")
        seen.add(hostname)
        if not str(source.get("quote", "")).strip():
            findings.append("missing_quote")
        if not str(source.get("publisher", "")).strip():
            findings.append("missing_publisher")
        try:
            accessed = date.fromisoformat(str(source.get("accessed_at", "")))
            if accessed > date.today():
                findings.append("future_access_date")
        except ValueError:
            findings.append("invalid_access_date")
    if len(seen) < 2:
        findings.append("insufficient_distinct_domains")
    return sorted(set(findings))
