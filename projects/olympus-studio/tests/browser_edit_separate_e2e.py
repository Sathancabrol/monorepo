"""E2E Chromium des deux sorties de secours EDIT sur HTTP réel.

Fixture entièrement synthétique. Vérifie WAV octet-identique et WebM vidéo seule
avec ffprobe; ne prétend pas valider l'export A/V ni Windows.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import time
from playwright.sync_api import sync_playwright

ROOT = Path(os.environ.get("OLYMPUS_TEST_ROOT", Path(__file__).resolve().parents[1]))
PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
    "AAAADUlEQVQIHWP4z8DwHwAFgAI/ScL/nwAAAABJRU5ErkJggg=="
)


def main():
    with tempfile.TemporaryDirectory(prefix="olympus-edit-separate-") as tmp:
        temp = Path(tmp)
        tone = temp / "fixture-440.wav"
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
            "-i", "sine=frequency=440:sample_rate=48000", "-t", "2",
            "-c:a", "pcm_s16le", str(tone)
        ], check=True, timeout=30)
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        server = subprocess.Popen(
            ["node", "server.mjs"], cwd=ROOT,
            env={**os.environ, "OLYMPUS_PORT": str(port)},
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        )
        try:
            for _ in range(100):
                if server.poll() is not None:
                    raise RuntimeError("Studio HTTP server exited")
                try:
                    with socket.create_connection(("127.0.0.1", port), timeout=.2):
                        break
                except OSError:
                    time.sleep(.1)
            else:
                raise RuntimeError("Studio HTTP server timeout")
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=["--no-sandbox", "--autoplay-policy=no-user-gesture-required"],
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
                        "name": "fixture.png", "mimeType": "image/png", "buffer": PNG
                    })
                    page.get_by_text("fixture.png", exact=True).first.wait_for()
                    page.locator("#fileMedia").set_input_files(str(tone))
                    page.locator('[data-space="EDIT"]').first.click()
                    choice = page.get_by_role("combobox", name="Choisir une piste audio")
                    choice.locator("option", has_text="fixture-440.wav").wait_for(state="attached")
                    choice.select_option(label="fixture-440.wav")
                    page.get_by_role("button", name="+ Clip").click()
                    duration = page.locator(".layer-row input[title='Durée en secondes']").first
                    duration.wait_for()
                    duration.fill("1.5")
                    duration.dispatch_event("change")
                    page.get_by_role("button", name="Ajouter / remplacer piste").click()
                    page.locator('[aria-label="Audio Départ projet (s)"]').wait_for()
                    # Real HTTP Chromium UI contract: active audio settings must drive
                    # the deterministic FFmpeg fallback, not merely a pure JS helper.
                    for label, value in [
                        ("Audio Départ projet (s)", "0.5"),
                        ("Audio IN source (s)", "0.25"),
                        ("Audio Volume (0–1)", "0.6"),
                    ]:
                        field = page.get_by_role("spinbutton", name=label)
                        field.fill(value)
                        field.dispatch_event("change")
                    guide_button = page.locator("#editFfmpegGuideButton")
                    guide_button.click()
                    assert page.locator("#editFfmpegGuide").is_visible()
                    command = page.locator("#editFfmpegCommand").inner_text()
                    for expected in (
                        "--offset 0.500000", "--in-point 0.250000",
                        "--volume 0.600000", "--duration 1.500000",
                        '--audio "audio_prepare.wav"', "--av-report",
                    ):
                        assert expected in command, (expected, command)
                    assert "CHEMIN_AUDIO_SOURCE" in command
                    assert "ffmpeg_mux_fallback.py" in command
                    assert '-an "montage.webm"' not in command
                    assert "MediaRecorder A/V reste expérimental" in page.locator("#editFfmpegGuide").inner_text()
                    guide_button.click()
                    assert page.locator("#editFfmpegGuide").is_hidden()
                    with page.expect_download(timeout=15000) as audio_info:
                        page.locator("#editAudioSource").click()
                    audio = audio_info.value
                    assert audio.suggested_filename.endswith(".wav"), audio.suggested_filename
                    audio_path = temp / "downloaded.wav"
                    audio.save_as(audio_path)
                    assert hashlib.sha256(audio_path.read_bytes()).digest() == hashlib.sha256(tone.read_bytes()).digest(), "WAV source was altered"
                    with page.expect_download(timeout=30000) as video_info:
                        page.locator("#editVideoOnly").click()
                    video = video_info.value
                    assert "video-only" in video.suggested_filename
                    video_path = temp / "video-only.webm"
                    video.save_as(video_path)
                    assert video_path.stat().st_size > 1500
                    streams = json.loads(subprocess.run([
                        "ffprobe", "-v", "error", "-show_streams", "-of", "json",
                        str(video_path)
                    ], capture_output=True, text=True, check=True, timeout=20).stdout)["streams"]
                    assert any(s.get("codec_type") == "video" and s.get("codec_name") in ("vp8", "vp9") for s in streams), streams
                    assert not any(s.get("codec_type") == "audio" for s in streams), streams
                    assert not errors, errors
                    print("EDIT separate exports verified: WAV SHA256 matches, WebM video-only codecs:", streams)
                finally:
                    browser.close()
        finally:
            server.terminate()
            try:
                server.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.communicate(timeout=5)


if __name__ == "__main__":
    main()
