"""Bloquea expedientes y planes de voz que habiliten publicación."""
import json
from pathlib import Path

def validate_artifacts(dossiers, voice, report):
    if dossiers.get("publication_allowed") is not False:
        raise ValueError("Dossier publication flag must be false")
    if voice.get("public_upload_allowed") is not False:
        raise ValueError("Voice publication flag must be false")
    if voice.get("editorial_approval", False) is not False:
        raise ValueError("Voice editorial approval must be false")
    if report.get("publication_allowed") is not False:
        raise ValueError("Report publication flag must be false")
    pending = report.get("pending_claims", [])
    if not isinstance(pending, list):
        raise ValueError("Invalid report claims")
    for record in pending:
        if not isinstance(record, dict) or record.get("publication_allowed") is not False or record.get("status") != "unverified":
            raise ValueError("Report claim must remain unverified")
    count = voice.get("research_claim_count")
    if count is not None and (type(count) is not int or count != len(pending)):
        raise ValueError("Narration count mismatch")
    cases = dossiers.get("dossiers", [])
    if not isinstance(cases, list):
        raise ValueError("Dossiers must be a list")
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("Dossier must be an object")
        if case.get("publication_allowed") is not False:
            raise ValueError("Case publication flag must be false")
        if case.get("verdict") is not None:
            raise ValueError("Automated verdict not permitted")
        claims = case.get("claims", [])
        matrices = case.get("evidence_matrices", [])
        if not isinstance(claims, list) or not isinstance(matrices, list):
            raise ValueError("Invalid claim or matrix list")
        if len(claims) != len(matrices):
            raise ValueError("Every claim requires one evidence matrix")
        for claim in claims:
            if not isinstance(claim, dict):
                raise ValueError("Invalid claim object")
            if claim.get("publishable") is not False or claim.get("verdict") != "unverified":
                raise ValueError("Candidate claims must remain unverified")
        for claim, matrix in zip(claims, matrices):
            if not isinstance(matrix, dict):
                raise ValueError("Invalid matrix object")
            if matrix.get("claim") != claim.get("text"):
                raise ValueError("Evidence matrix claim does not match")
            if matrix.get("publication_allowed") is not False or matrix.get("verdict") is not None:
                raise ValueError("Evidence matrix must remain unverified")
    expected = [(case.get("id"), case.get("source_url"), claim.get("text")) for case in cases for claim in case.get("claims", [])]
    actual = [(record.get("dossier_id"), record.get("source_url"), record.get("claim")) for record in pending]
    if len(expected) != len(actual) or sorted(expected, key=repr) != sorted(actual, key=repr):
        raise ValueError("Report claims differ from research dossiers")
    return True

if __name__ == "__main__":
    base = Path("output")
    def load(name):
        return json.loads((base / name).read_text(encoding="utf-8"))
    validate_artifacts(load("dossiers.json"), load("voice_plan.json"), load("report.json"))
    print("Editorial publication safety: OK")
