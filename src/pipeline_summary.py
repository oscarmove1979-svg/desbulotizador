"""Resumen verificable de la ejecución; no concede autorización editorial."""
import json
from pathlib import Path

def summarize_status(voice, video, metrics):
    return {
        "video_rendered": bool(video.get("technical_pass")),
        "video_has_audio": bool(voice.get("narrated_video_valid")),
        "voice_status": voice.get("voice_status", "unknown"),
        "voice_error": voice.get("error_type"),
        "candidates": metrics.get("candidate_count", 0),
        "dossiers": metrics.get("dossier_count", 0),
        "claims_pending_review": metrics.get("claims_pending_review", 0),
        "evidence_records": metrics.get("evidence_records", 0),
        "source_errors": metrics.get("source_errors", 0),
        "verified_claims": 0,
        "youtube_upload_enabled": False,
        "ready_for_publication": False
    }

if __name__ == "__main__":
    out = Path("output")
    def read(name):
        return json.loads((out / name).read_text(encoding="utf-8"))
    result = summarize_status(read("voice_status.json"), read("video_quality.json"), read("metrics.json"))
    (out / "pipeline_summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["## desBULOtizador — ejecución", "",
             f"- Vídeo técnico correcto: {result['video_rendered']}",
             f"- Narración: {result['voice_status']}",
             f"- Vídeo narrado válido: {result['video_has_audio']}",
             f"- Candidatos: {result['candidates']}",
             f"- Expedientes: {result['dossiers']}",
             f"- Afirmaciones pendientes: {result['claims_pending_review']}",
             f"- Evidencias registradas: {result['evidence_records']}",
             f"- Errores de fuentes: {result['source_errors']}",
             "- Publicación: BLOQUEADA"]
    import os
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as fp:
            fp.write("\n".join(lines) + "\n")
    print(json.dumps(result, ensure_ascii=False))
