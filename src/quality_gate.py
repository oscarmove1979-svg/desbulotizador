"""Inspección técnica del MP4 sin implicar aprobación editorial."""
import json
import subprocess
from pathlib import Path

def inspect_video(path):
    path = Path(path)
    if not path.is_file() or path.stat().st_size < 1000:
        raise ValueError("Missing or empty video")
    cmd = ["ffprobe", "-v", "error", "-show_entries",
           "stream=codec_type,width,height:format=duration",
           "-of", "json", str(path)]
    info = json.loads(subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=30).stdout)
    video = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
    duration = float(info.get("format", {}).get("duration", 0))
    if not video or video.get("width") != 720 or video.get("height") != 1280 or not 1 <= duration <= 120:
        raise ValueError("Invalid video characteristics")
    return {"technical_pass": True, "editorial_pass": False,
            "public_upload_allowed": False, "duration_seconds": duration}

if __name__ == "__main__":
    result = inspect_video("output/preview.mp4")
    Path("output/video_quality.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(result)
