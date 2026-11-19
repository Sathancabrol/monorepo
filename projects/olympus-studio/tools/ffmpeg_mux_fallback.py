#!/usr/bin/env python3
"""Opt-in local FFmpeg fallback for separately exported video and audio.

Does not reconstruct frames lost by MediaRecorder. Never overwrites input/output.
"""
import argparse
import json
import math
import re
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



def mux_png_sequence(frames_dir, audio, output, fps=24, audio_offset=0.0):
    """Encode an explicitly selected numbered PNG sequence with an audio file.

    Inputs are never changed; no implicit directory creation or overwrite.
    """
    if not isinstance(fps, int) or not 1 <= fps <= 60:
        raise ValueError("FPS must be an integer from 1 to 60")
    if not math.isfinite(audio_offset) or abs(audio_offset) > 120:
        raise ValueError("Audio offset must be finite and within ±120 seconds")
    frames_dir, audio, output = map(lambda p: Path(p).resolve(), (frames_dir, audio, output))
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("FFmpeg and ffprobe are required locally")
    if not frames_dir.is_dir() or not audio.is_file():
        raise ValueError("Frame directory and audio file must exist")
    if output.suffix.lower() != ".webm" or output.exists():
        raise ValueError("Output must be a new .webm file")
    if output.parent == frames_dir or output == audio:
        raise ValueError("Output must be outside the input frame directory")
    # Do not follow symlinks out of the explicitly selected export directory.
    entries = list(frames_dir.iterdir())
    if any(p.is_symlink() or not p.is_file() for p in entries):
        raise ValueError("Frame directory must contain only regular PNG files (no links)")
    files = sorted(p.name for p in entries)
    if not files or len(files) > 7200 or any(not re.fullmatch(r"\d{6}\.png", f) for f in files):
        raise ValueError("Expected only 1–7200 numbered PNG frames")
    if files != [f"{i:06d}.png" for i in range(1, len(files) + 1)]:
        raise ValueError("PNG frames must be contiguous from 000001.png")
    if not any(s.get("codec_type") == "audio" for s in probe(audio)):
        raise ValueError("Audio input has no audio stream")
    command = [
        "ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-n",
        "-framerate", str(fps), "-start_number", "1", "-i", str(frames_dir / "%06d.png"),
        "-itsoffset", str(audio_offset), "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libvpx-vp9", "-deadline", "realtime", "-cpu-used", "5",
        "-pix_fmt", "yuv420p", "-c:a", "libopus", "-shortest", str(output)
    ]
    try:
        subprocess.run(command, check=True, timeout=300)
        streams = probe(output)
        if not {"video", "audio"}.issubset({s.get("codec_type") for s in streams}):
            raise RuntimeError("Muxed output lacks video or audio")
        return output
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, RuntimeError, OSError, ValueError):
        output.unlink(missing_ok=True)
        raise


def av_packet_report(path):
    """Measure actual packet endpoints rather than container duration metadata."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_packets",
         "-show_entries", "packet=codec_type,pts_time,duration_time",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True, timeout=30
    )
    packets = json.loads(result.stdout).get("packets", [])
    spans = {}
    for kind in ("video", "audio"):
        selected = [p for p in packets if p.get("codec_type") == kind and p.get("pts_time") is not None]
        if not selected:
            raise ValueError(f"No {kind} packets for A/V report")
        start = min(float(p["pts_time"]) for p in selected)
        end = max(float(p["pts_time"]) + float(p.get("duration_time") or 0) for p in selected)
        spans[kind] = {"start_s": round(start, 4), "end_s": round(end, 4), "packets": len(selected)}
    return {"video": spans["video"], "audio": spans["audio"],
            "end_delta_s": round(spans["video"]["end_s"] - spans["audio"]["end_s"], 4)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, help="Existing video file (mutually exclusive with --frames-dir)")
    parser.add_argument("--frames-dir", type=Path, help="Directory containing 000001.png, 000002.png, ...")
    parser.add_argument("--fps", type=int, default=24, help="PNG sequence frame rate, 1–60")
    parser.add_argument("--audio", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--audio-offset", type=float, default=0.0,
                        help="Shift audio relative to video in seconds (positive = later; max ±120)")
    parser.add_argument("--av-report", action="store_true", help="Print measured A/V packet timing as JSON after export")
    parser.add_argument("--max-end-delta", type=float, default=None,
                        help="Reject output when absolute A/V packet end difference exceeds this many seconds")
    args = parser.parse_args()
    if args.max_end_delta is not None and (not math.isfinite(args.max_end_delta) or args.max_end_delta < 0):
        parser.error("--max-end-delta must be finite and nonnegative")
    if bool(args.video) == bool(args.frames_dir):
        parser.error("Specify exactly one of --video or --frames-dir")
    if args.frames_dir:
        created = mux_png_sequence(args.frames_dir, args.audio, args.output, args.fps, args.audio_offset)
    else:
        created = mux(args.video, args.audio, args.output, args.audio_offset)
    # A path on stdout means a *validated* export, never a rejected candidate.
    report = None
    try:
        if args.av_report or args.max_end_delta is not None:
            report = av_packet_report(created)
            if args.max_end_delta is not None and abs(report["end_delta_s"]) > args.max_end_delta:
                raise RuntimeError(
                    f"A/V end delta {report['end_delta_s']}s exceeds {args.max_end_delta}s; invalid output removed"
                )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError, RuntimeError, OSError):
        created.unlink(missing_ok=True)
        raise
    print(created)
    if args.av_report:
        print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
