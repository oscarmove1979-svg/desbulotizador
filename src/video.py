"""Renderiza una tarjeta de estado SIN veredicto usando FFmpeg (sin servicios de pago)."""
import json
import shutil
import subprocess
from pathlib import Path

def create_preview(dossiers_path="output/dossiers.json", destination="output/preview.mp4"):
    if not shutil.which("ffmpeg"):
        raise RuntimeError("FFmpeg no disponible")
    data = json.loads(Path(dossiers_path).read_text(encoding="utf-8"))
    count = len(data.get("dossiers", []))
    if not isinstance(data.get("dossiers"), list):
        raise ValueError("Invalid dossier list")
    if data.get("publication_allowed") is not False:
        raise ValueError("Publication flag must be false")
    # Vista de diagnóstico, no una pieza editorial publicable.
    output = Path(destination)
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-f", "lavfi", "-i",
           "color=c=0x101820:s=720x1280:r=25:d=14",
           "-vf", "drawbox=x=35:y=80:w=650:h=210:color=0x293747:t=fill,"
                  "drawtext=text='desBULOtizador':fontsize=48:fontcolor=white:x=65:y=120,"
                  "drawtext=text='PROTOTIPO - SIN VEREDICTO':fontsize=29:fontcolor=yellow:x=65:y=215,"
                  f"drawtext=text='Expedientes detectados\\: {count}':fontsize=27:fontcolor=white:x=65:y=360",
           "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
           str(output)]
    subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=120)
    return str(output)

if __name__ == "__main__":
    print(create_preview())
