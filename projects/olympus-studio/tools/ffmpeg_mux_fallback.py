#!/usr/bin/env python3
"""Opt-in local FFmpeg fallback for separately exported video and audio.

Does not reconstruct frames lost by MediaRecorder. Never overwrites input/output.
"""
import argparse
import json
import math
import shutil
import subprocess
from pathlib import Path


def probe(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)],
        capture_output=True, text=True, check=True, timeout=30
    )
    return json.loads(result.stdout).get("streams", [])


def mux(video, audio, output, audio_offset=0.0):
    if not math.isfinite(audio_offset) or abs(audio_offset) > 120:
        raise ValueError('Audio offset must be finite and within ±120 seconds')
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
        "-i", str(video), "-itsoffset", str(audio_offset), "-i", str(audio), "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libvpx-vp9", "-deadline", "realtime", "-cpu-used", "5",
        "-c:a", "libopus", "-shortest", str(output)
    ]
    try:
        subprocess.run(command, check=True, timeout=300)
        streams = probe(output)
        if not {"video", "audio"}.issubset({s.get("codec_type") for s in streams}):
            raise RuntimeError("Muxed output lacks video or audio")
        return output
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, RuntimeError, OSError, ValueError):
        # FFmpeg may leave a truncated output on failure; never present it as a valid export.
        output.unlink(missing_ok=True)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--audio", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--audio-offset", type=float, default=0.0,
                        help="Shift audio relative to video in seconds (positive = later; max ±120)")
    args = parser.parse_args()
    print(mux(args.video, args.audio, args.output, args.audio_offset))


if __name__ == "__main__":
    main()
