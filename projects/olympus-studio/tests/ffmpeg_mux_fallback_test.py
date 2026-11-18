#!/usr/bin/env python3
"""Exercise the actual FFmpeg fallback using two independent synthetic streams."""
import importlib.util
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("mux_fallback", ROOT / "tools" / "ffmpeg_mux_fallback.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)
    video, audio, output = (base / n for n in ("video.webm", "audio.wav", "combined.webm"))
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi", "-i",
                    "testsrc2=size=160x90:rate=15:duration=1.5",
                    "-c:v", "libvpx", "-an", str(video)], check=True, timeout=60)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi", "-i",
                    "sine=frequency=440:sample_rate=48000:duration=1.5",
                    "-c:a", "pcm_s16le", str(audio)], check=True, timeout=60)
    assert module.mux(video, audio, output) == output.resolve()
    streams = module.probe(output)
    assert any(s.get("codec_type") == "video" and s.get("codec_name") == "vp9" for s in streams)
    assert any(s.get("codec_type") == "audio" and s.get("codec_name") == "opus" for s in streams)
    assert video.stat().st_size > 0 and audio.stat().st_size > 0
    try:
        module.mux(video, audio, output)
    except ValueError as exc:
        assert "overwrite" in str(exc)
    else:
        raise AssertionError("Existing output should be protected")
    print("FFmpeg fallback: mux, VP9/Opus, and overwrite protection passed")
