#!/usr/bin/env python3
"""Prepare one non-destructive EDIT audio track for the existing FFmpeg mux fallback.

Consumes an explicit local source and creates a new WAV with timeline-aligned silence.
No network access, no source mutation, no overwrite, no implicit model downloads.
"""
import argparse
import json
import math
import shutil
import subprocess
from pathlib import Path


def prepare_audio(source, output, *, offset, in_point, volume, duration):
    values = (offset, in_point, volume, duration)
    if not all(math.isfinite(v) for v in values):
        raise ValueError("Audio parameters must be finite")
    if not (0 <= offset <= 36000 and 0 <= in_point <= 36000 and
            0 <= volume <= 1 and 0 < duration <= 120):
        raise ValueError("Audio parameters outside EDIT limits")
    source, output = Path(source).resolve(), Path(output).resolve()
    if not source.is_file() or output.exists() or source == output:
        raise ValueError("Source must exist; output must be a new file")
    if output.suffix.lower() != ".wav":
        raise ValueError("Output must be WAV")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("Local ffmpeg and ffprobe required")
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0",
         "-show_entries", "stream=codec_type", "-of", "json", str(source)],
        capture_output=True, text=True, check=True, timeout=30)
    if not any(s.get("codec_type") == "audio" for s in json.loads(probe.stdout).get("streams", [])):
        raise ValueError("Input contains no audio stream")
    # Build a full-duration timeline, including silence before/after the source.
    # atrim removes source time before IN, asetpts resets timestamps, adelay positions
    # the clip, apad fills the remainder, final atrim caps exactly at project end.
    delay_ms = round(offset * 1000)
    filters = (
        f"atrim=start={in_point:.6f},asetpts=PTS-STARTPTS,"
        f"volume={volume:.6f},adelay={delay_ms}:all=1,"
        f"apad,atrim=end={duration:.6f},asetpts=PTS-STARTPTS"
    )
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-n",
           "-i", str(source), "-af", filters, "-vn", "-ac", "2",
           "-ar", "48000", "-c:a", "pcm_s16le", str(output)]
    try:
        subprocess.run(cmd, check=True, timeout=180)
        if not output.is_file() or output.stat().st_size <= 44:
            raise RuntimeError("Prepared audio is missing or empty")
    except (OSError, RuntimeError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        output.unlink(missing_ok=True)
        raise
    return output


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--offset", required=True, type=float)
    p.add_argument("--in-point", required=True, type=float)
    p.add_argument("--volume", required=True, type=float)
    p.add_argument("--duration", required=True, type=float)
    args = p.parse_args()
    print(prepare_audio(args.source, args.output, offset=args.offset,
                        in_point=args.in_point, volume=args.volume, duration=args.duration))


if __name__ == "__main__":
    main()
