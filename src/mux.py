"""Añade audio a la vista previa, sin habilitar publicación."""
import shutil
import subprocess
from pathlib import Path

def add_voice(video="output/preview.mp4", audio="output/voice.mp3",
              output="output/preview_narrated.mp4"):
    if not shutil.which("ffmpeg"):
        raise RuntimeError("FFmpeg no disponible")
    if not Path(video).is_file() or not Path(audio).is_file():
        raise FileNotFoundError("Falta vídeo o audio")
    subprocess.run(["ffmpeg", "-y", "-stream_loop", "-1", "-i", video, "-i", audio,
                    "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                    "-shortest", "-movflags", "+faststart", output],
                   check=True, capture_output=True, text=True, timeout=120)
    if not Path(output).is_file() or Path(output).stat().st_size < 1000:
        raise RuntimeError("Vídeo narrado no generado")
    return output

if __name__ == "__main__":
    print(add_voice())
