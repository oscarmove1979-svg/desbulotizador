"""Registro explícito de fuentes: procedencia no equivale a veracidad."""
from urllib.parse import urlsplit

PRIMARY_SOURCE_DOMAINS = {
    "boe.es": "Boletín Oficial del Estado",
    "ine.es": "Instituto Nacional de Estadística",
    "congreso.es": "Congreso de los Diputados",
    "senado.es": "Senado de España",
    "bde.es": "Banco de España",
    "airef.es": "Autoridad Independiente de Responsabilidad Fiscal",
    "tribunalconstitucional.es": "Tribunal Constitucional",
}

def classify_source(url):
    parsed = urlsplit(url) if isinstance(url, str) else None
    if (not parsed or parsed.scheme != "https" or not parsed.hostname
            or parsed.username or parsed.password):
        return {"kind": "unknown", "authority": None, "fact_verified": False}
    host = parsed.hostname.lower().removeprefix("www.")
    for domain, authority in PRIMARY_SOURCE_DOMAINS.items():
        if host == domain or host.endswith("." + domain):
            return {"kind": "institutional_primary_source", "authority": authority,
                    "fact_verified": False}
    return {"kind": "unclassified_source", "authority": None, "fact_verified": False}
