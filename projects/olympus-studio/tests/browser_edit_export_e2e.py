"""E2E du véritable bouton EDIT -> WebM/Opus, via HTTP + Chromium.

Données synthétiques uniquement; preuve navigateur Linux, pas essai Windows.
Exécuter depuis projects/olympus-studio: python tests/browser_edit_export_e2e.py
"""
import base64
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import time

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
    "AAAADUlEQVQIHWP4z8DwHwAFgAI/ScL/nwAAAABJRU5ErkJggg=="
)


def port_available():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def inspect_export(path):
    streams = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)],
        capture_output=True, text=True, check=True, timeout=20,
    ).stdout)["streams"]
    video = [s for s in streams if s.get("codec_type") == "video"]
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    assert video and video[0]["codec_name"] in ("vp8", "vp9"), streams
    assert audio and audio[0]["codec_name"] == "opus", streams
    packets = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-show_packets",
         "-show_entries", "packet=stream_index,pts_time,duration_time",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True, timeout=20,
    ).stdout)["packets"]
    def bounds(stream):
        times = [(float(p["pts_time"]), float(p.get("duration_time", 0)))
                 for p in packets if p.get("stream_index") == stream["index"]
                 and "pts_time" in p]
        assert len(times) >= 2, ("Missing encoded packets", stream)
        return min(t for t, _ in times), max(t + d for t, d in times)
    vs, ve = bounds(video[0])
    aus, aue = bounds(audio[0])
    assert 1.0 < ve - vs < 4, (vs, ve)
    assert 1.0 < aue - aus < 4, (aus, aue)
    assert abs(vs - aus) < 0.6, ("A/V start mismatch", vs, aus)
    assert abs(ve - aue) < 0.6, ("A/V end mismatch", ve, aue)
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
         "-map", "0:a:0", "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True, check=True, timeout=30,
    )
    import re
    match = re.search(r"mean_volume:\s*(-?[\d.]+) dB", result.stderr)
    assert match and -60 < float(match.group(1)) < -2, result.stderr[-1200:]
    return {"video": video[0]["codec_name"], "audio": audio[0]["codec_name"],
            "start_offset_s": round(vs-aus, 3), "end_offset_s": round(ve-aue, 3),
            "mean_db": float(match.group(1)), "bytes": path.stat().st_size}


def main():
    with tempfile.TemporaryDirectory(prefix="olympus-edit-av-") as temp:
        tone = Path(temp) / "synthetic-440hz.wav"
        subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
             "-i", "sine=frequency=440:sample_rate=48000", "-t", "3",
             "-c:a", "pcm_s16le", "-y", str(tone)], check=True,
        )
        port = port_available()
        server = subprocess.Popen(
            ["node", "server.mjs"], cwd=ROOT,
            env={**os.environ, "OLYMPUS_PORT": str(port)},
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        )
        try:
            for _ in range(100):
                if server.poll() is not None:
                    raise RuntimeError("Studio server exited before test")
                try:
                    with socket.create_connection(("127.0.0.1", port), timeout=.2):
                        break
                except OSError:
                    time.sleep(.1)
            else:
                raise RuntimeError("Studio server timeout")
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(
                    headless=True, args=["--no-sandbox",
                                         "--autoplay-policy=no-user-gesture-required"]
                )
                try:
                    page = browser.new_page(accept_downloads=True)
                    errors = []
                    page.on("pageerror", lambda e: errors.append(str(e)))
                    page.goto(f"http://127.0.0.1:{port}/", wait_until="load")
                    page.wait_for_function(
                        "document.querySelectorAll('#navItems [data-space]').length === 12"
                    )
                    page.locator("#fileMedia").set_input_files({
                        "name": "synthetic-image.png", "mimeType": "image/png", "buffer": PNG
                    })
                    page.get_by_text("synthetic-image.png", exact=True).first.wait_for()
                    page.locator("#fileMedia").set_input_files(str(tone))
                    # Audio is a library asset, not a LIVE visual layer. Check it in EDIT.
                    page.locator('[data-space="EDIT"]').first.click()
                    audio_choice = page.get_by_role("combobox", name="Choisir une piste audio")
                    audio_choice.locator("option", has_text="synthetic-440hz.wav").wait_for()
                    page.get_by_role("button", name="+ Clip").click()
                    page.locator(".layer-row input[title='Durée en secondes']").first.wait_for()
                    duration = page.locator(".layer-row input[title='Durée en secondes']").first
                    duration.fill("2.5")
                    duration.dispatch_event("change")
                    page.get_by_role("button", name="Ajouter / remplacer piste").click()
                    page.locator('[aria-label="Audio Départ projet (s)"]').wait_for()
                    assert not errors, "JS errors before export: " + " | ".join(errors)
                    with page.expect_download(timeout=25000) as download_info:
                        page.get_by_role("button", name="Exporter WebM (audio optionnel)").click()
                    download = download_info.value
                    assert download.suggested_filename.endswith(".webm")
                    output = Path(temp) / "studio-edit-export.webm"
                    download.save_as(output)
                    assert output.stat().st_size > 1500
                    assert not errors, "JS errors during export: " + " | ".join(errors)
                    print("EDIT UI A/V export:", inspect_export(output))
                finally:
                    browser.close()
        finally:
            server.terminate()
            try:
                server.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.communicate()


if __name__ == "__main__":
    main()
