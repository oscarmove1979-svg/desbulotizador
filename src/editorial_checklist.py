"""Genera una lista de comprobacion humana sin veredictos automaticos."""
import json
from pathlib import Path
from urllib.parse import urlsplit

QUESTIONS = (
    "¿La afirmacion reproduce fielmente las palabras originales y su contexto?",
    "¿Se ha localizado la fuente primaria y comprobado su fecha?",
    "¿Las cifras se comparan usando las mismas unidades y periodos?",
    "¿Hay evidencias independientes que puedan contradecir la hipotesis?",
    "¿Se ha distinguido un hecho comprobable de una opinion?",
    "¿Un revisor humano ha validado citas, enlaces y conclusion?",
    "¿El guion refleja incertidumbres y evita acusaciones infundadas?",
)

def build_checklist(report):
    if report.get("publication_allowed") is not False:
        raise ValueError("Report must remain blocked")
    records = report.get("pending_claims")
    if not isinstance(records, list):
        raise ValueError("Invalid pending claims")
    result = []
    for record in records:
        if not isinstance(record, dict) or record.get("status") != "unverified" or record.get("publication_allowed") is not False:
            raise ValueError("Unsafe research item")
        if not isinstance(record.get("claim"), str) or not record["claim"].strip():
            raise ValueError("Missing claim text")
        source = record.get("source_url")
        if not isinstance(source, str):
            raise ValueError("Missing source URL")
        parsed = urlsplit(source)
        if (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password
                or any(ord(ch) < 32 or ord(ch) == 127 for ch in source)):
            raise ValueError("Checklist source must use HTTPS")
        if not isinstance(record.get("dossier_id"), str) or not record["dossier_id"].strip():
            raise ValueError("Missing dossier identifier")
        result.append({"dossier_id":record.get("dossier_id"),"claim":record.get("claim"),"source_url":record.get("source_url"),"questions":[{"question":q,"checked":False} for q in QUESTIONS],"human_approval":False,"verdict":None,"publication_allowed":False})
    return {"project":"desBULOtizador","items":result,"publication_allowed":False,"automated_verdict":False}

if __name__ == "__main__":
    base = Path("output")
    report = json.loads((base/"report.json").read_text(encoding="utf-8"))
    (base/"editorial_checklist.json").write_text(json.dumps(build_checklist(report),ensure_ascii=False,indent=2),encoding="utf-8")
