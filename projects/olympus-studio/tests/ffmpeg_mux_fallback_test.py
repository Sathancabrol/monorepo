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

    # Real FFmpeg regression: a deliberate audio delay must survive muxing.
    delayed = base / "delayed.webm"
    module.mux(video, audio, delayed, audio_offset=0.25)
    def first_packet_time(path, selector):
        import json
        data = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", selector,
             "-show_packets", "-show_entries", "packet=pts_time",
             "-of", "json", str(path)],
            capture_output=True, text=True, check=True, timeout=30
        )
        packets = json.loads(data.stdout).get("packets", [])
        assert packets, f"No {selector} packets in {path}"
        return float(packets[0]["pts_time"])
    video_start = first_packet_time(delayed, "v:0")
    audio_start = first_packet_time(delayed, "a:0")
    assert 0.15 <= audio_start - video_start <= 0.35, (
        f"Expected +250ms audio delay, got {audio_start-video_start:.3f}s"
    )
    print("FFmpeg fallback: mux, VP9/Opus, overwrite protection and +250ms offset passed")
