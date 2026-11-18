#!/usr/bin/env python3
"""Opt-in local FFmpeg fallback for separately exported video and audio.

Does not reconstruct frames lost by MediaRecorder. Never overwrites input/output.
"""
import argparse
import json
import shutil
import subprocess
from pathlib import Path


def probe(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)],
        capture_output=True, text=True, check=True, timeout=30
    )
    return json.loads(result.stdout).get("streams", [])


def mux(video, audio, output):
    video, audio, output = map(lambda p: Path(p).resolve(), (video, audio, output))
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("FFmpeg and ffprobe are required locally")
    if not video.is_file() or not audio.is_file():
        raise ValueError("Both input files must exist")
    if output.suffix.lower() != ".webm":
        raise ValueError("Output must be a .webm file")
    if output in (video, audio) or output.exists():
        raise ValueError("Refusing to overwrite an existing file")
    if not any(s.get("codec_type") == "video" for s in probe(video)):
        raise ValueError("First input has no video stream")
    if not any(s.get("codec_type") == "audio" for s in probe(audio)):
        raise ValueError("Second input has no audio stream")
    command = [
        "ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-n",
        "-i", str(video), "-i", str(audio), "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libvpx-vp9", "-deadline", "realtime", "-cpu-used", "5",
        "-c:a", "libopus", "-shortest", str(output)
    ]
    subprocess.run(command, check=True, timeout=300)
    streams = probe(output)
    if not {"video", "audio"}.issubset({s.get("codec_type") for s in streams}):
        output.unlink(missing_ok=True)
        raise RuntimeError("Muxed output lacks video or audio")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--audio", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(mux(args.video, args.audio, args.output))


if __name__ == "__main__":
    main()
