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
    # Verify the actual exported signal, not merely a non-silent Opus track.
    # A 440 Hz synthetic WAV is imported through EDIT; unexpected routing
    # (e.g. system audio or silence) must fail the E2E assertion.
    import array
    pcm = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0",
         "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
        capture_output=True, check=True, timeout=30,
    ).stdout
    samples = array.array("h")
    samples.frombytes(pcm)
    assert len(samples) > 8000, ("Audio decoded too short", len(samples))
    # Count positive-going zero crossings in the central 0.5 s, away from
    # encoder priming and fade edges. At 8 kHz, 440 Hz yields ~220 crossings.
    middle = len(samples) // 2
    window = samples[middle-2000:middle+2000]
    crossings = sum(a <= 0 < b for a, b in zip(window, window[1:]))
    frequency_hz = crossings * 2  # 0.5 second window
    assert 400 <= frequency_hz <= 480, ("Wrong exported audio frequency", frequency_hz)
    return {"video": video[0]["codec_name"], "audio": audio[0]["codec_name"],
            "start_offset_s": round(vs-aus, 3), "end_offset_s": round(ve-aue, 3),
            "mean_db": float(match.group(1)), "tone_hz": frequency_hz, "bytes": path.stat().st_size}


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
                    audio_choice.locator("option", has_text="synthetic-440hz.wav").wait_for(state="attached")
                    # Native <option> is hidden in headless Chromium: wait for DOM attachment, not visibility.
                    audio_choice.select_option(label="synthetic-440hz.wav")
                    page.get_by_role("button", name="+ Clip").click()
                    page.locator(".layer-row input[title='Durée en secondes']").first.wait_for()
                    duration = page.locator(".layer-row input[title='Durée en secondes']").first
                    duration.fill("2.5")
                    duration.dispatch_event("change")
                    page.get_by_role("button", name="Ajouter / remplacer piste").click()
                    page.locator('[aria-label="Audio Départ projet (s)"]').wait_for()
                    # E2E Portable via real UI: preserve EDIT clips and audio,
                    # not only the LIVE scene. The image and WAV must be embedded
                    # once each, then restored after a real page navigation.
                    with page.expect_download(timeout=15000) as portable_info:
                        page.locator("#btnPortable").click()
                    portable_download = portable_info.value
                    portable_path = Path(temp) / "edit-project-portable.json"
                    portable_download.save_as(portable_path)
                    project = json.loads(portable_path.read_text(encoding="utf-8"))
                    assert project["format"] == "olympus-studio-project"
                    assert project["portable"] is True
                    assert len(project["clips"]) == 1, project["clips"]
                    clip_before = project["clips"][0]
                    assert abs(float(clip_before["duration"]) - 2.5) < 0.01
                    audio_before = project["editAudioTrack"]
                    assert audio_before and audio_before["enabled"], audio_before
                    embedded_ids = [asset["id"] for asset in project["embeddedAssets"]]
                    assert len(embedded_ids) == len(set(embedded_ids)) == 2, embedded_ids
                    assert clip_before["assetId"] in embedded_ids
                    assert audio_before["assetId"] in embedded_ids
                    page.reload(wait_until="load")
                    page.locator("#fileProject").set_input_files(str(portable_path))
                    page.locator("#status").get_by_text("Projet chargé", exact=False).wait_for(timeout=10000)
                    with page.expect_download(timeout=15000) as restored_info:
                        page.locator("#btnPortable").click()
                    restored_path = Path(temp) / "edit-project-restored.json"
                    restored_info.value.save_as(restored_path)
                    restored = json.loads(restored_path.read_text(encoding="utf-8"))
                    assert restored["clips"] == project["clips"], "EDIT clips changed after reload"
                    assert restored["editAudioTrack"] == audio_before, "Audio settings changed after reload"
                    assert {a["id"] for a in restored["embeddedAssets"]} == set(embedded_ids)
                    page.locator('[data-space="EDIT"]').first.click()
                    page.locator('[aria-label="Audio Départ projet (s)"]').wait_for()
                    assert not errors, "JS errors after Portable reload: " + " | ".join(errors)
                    assert not errors, "JS errors before export: " + " | ".join(errors)
                    with page.expect_download(timeout=25000) as download_info:
                        page.get_by_role("button", name="Exporter WebM (audio optionnel)").click()
                        # A04: adding a clip while MediaRecorder is active must not mutate the timeline.
                        page.locator("#status").get_by_text("Export vidéo + piste audio en cours", exact=False).wait_for(timeout=10000)
                        page.get_by_role("button", name="+ Clip").click()
                        page.locator("#status").get_by_text("Arrêter export EDIT avant ajout de clip", exact=False).wait_for(timeout=5000)
                        # The existing audio track must also be immutable while recording.
                        # This exercises the real UI guard; a deferred-load race needs
                        # a separate deterministic interception test.
                        page.get_by_role("button", name="Ajouter / remplacer piste").click()
                        page.locator("#status").get_by_text("Arrêter export EDIT avant modification de la piste", exact=False).wait_for(timeout=5000)
                    download = download_info.value
                    assert download.suggested_filename.endswith(".webm")
                    output = Path(temp) / "studio-edit-export.webm"
                    download.save_as(output)
                    assert output.stat().st_size > 1500
                    assert not errors, "JS errors during export: " + " | ".join(errors)
                    print("EDIT UI A/V export:", inspect_export(output))
                    with page.expect_download(timeout=15000) as locked_info:
                        page.locator("#btnPortable").click()
                    locked_path = Path(temp) / "export-locked-project.json"
                    locked_info.value.save_as(locked_path)
                    locked = json.loads(locked_path.read_text(encoding="utf-8"))
                    assert locked["clips"] == restored["clips"], "Export-time clip insertion mutated the project"
                    assert locked["editAudioTrack"] == restored["editAudioTrack"]
                    # A02: split two segments of one real video source through EDIT,
                    # then round-trip Portable and verify deduplicated media.
                    video_path = Path(temp) / "synthetic-video.webm"
                    subprocess.run(
                        ["ffmpeg", "-hide_banner", "-loglevel", "error",
                         "-f", "lavfi", "-i", "color=c=blue:s=160x90:r=15",
                         "-t", "2", "-c:v", "libvpx", "-b:v", "200k",
                         "-an", "-y", str(video_path)], check=True, timeout=30,
                    )
                    page.locator("#fileMedia").set_input_files(str(video_path))
                    video_select = page.get_by_role("combobox", name="Choisir un média du coffre")
                    video_select.locator("option", has_text="synthetic-video.webm").wait_for(state="attached")
                    video_select.select_option(label="synthetic-video.webm")
                    page.get_by_role("button", name="+ Clip").click()
                    # The preceding image lasts 2.5s; split the video at 1s local.
                    # Wait for the UI to include the newly added video in timeline duration.
                    # Filling a range while max is still 2.5 raises "Malformed value".
                    page.wait_for_function(
                        "() => Number(document.querySelector('#editSeek')?.max) >= 4.45",
                        timeout=10000,
                    )
                    page.locator("#editSeek").fill("3.5")
                    page.locator("#editSeek").dispatch_event("input")
                    page.get_by_role("button", name="Diviser au curseur").click()
                    # A04: exercise actual undo/redo buttons, not just history helpers.
                    # The split must undo to one video clip and redo to two while
                    # preserving the original source asset and audio track.
                    def portable_snapshot(filename):
                        with page.expect_download(timeout=15000) as snapshot_info:
                            page.locator("#btnPortable").click()
                        target = Path(temp) / filename
                        snapshot_info.value.save_as(target)
                        return json.loads(target.read_text(encoding="utf-8"))

                    page.locator("#editUndo").wait_for(state="visible")
                    assert page.locator("#editUndo").is_enabled(), "Split must be undoable"
                    page.locator("#editUndo").click()
                    undone = portable_snapshot("split-undone.json")
                    undone_video = [c for c in undone["clips"] if c["kind"] == "video"]
                    assert len(undone_video) == 1, undone["clips"]
                    assert page.locator("#editRedo").is_enabled(), "Undo must enable redo"
                    page.locator("#editRedo").click()
                    redone = portable_snapshot("split-redone.json")
                    redone_video = [c for c in redone["clips"] if c["kind"] == "video"]
                    assert len(redone_video) == 2, redone["clips"]
                    assert redone_video[0]["assetId"] == redone_video[1]["assetId"]
                    assert redone["editAudioTrack"] == undone["editAudioTrack"]
                    assert {a["id"] for a in redone["embeddedAssets"]} == {a["id"] for a in undone["embeddedAssets"]}
                    # A04: audio parameter changes are reversible through real UI.
                    # New edits after undo must invalidate the redo branch.
                    volume = page.locator('[aria-label="Audio Volume (0–1)"]')
                    volume.wait_for()
                    original_volume = float(redone["editAudioTrack"]["volume"])
                    assert abs(original_volume - 1.0) < 0.001
                    volume.fill("0.35")
                    volume.dispatch_event("change")
                    changed = portable_snapshot("audio-volume-changed.json")
                    assert abs(float(changed["editAudioTrack"]["volume"]) - 0.35) < 0.001
                    page.locator("#editUndo").click()
                    audio_undone = portable_snapshot("audio-volume-undone.json")
                    assert audio_undone["editAudioTrack"] == redone["editAudioTrack"]
                    assert audio_undone["clips"] == redone["clips"]
                    page.locator("#editRedo").click()
                    audio_redone = portable_snapshot("audio-volume-redone.json")
                    assert audio_redone["editAudioTrack"] == changed["editAudioTrack"]
                    page.locator("#editUndo").click()
                    # A distinct new volume edit invalidates the abandoned 0.35 redo.
                    volume = page.locator('[aria-label="Audio Volume (0–1)"]')
                    volume.fill("0.6")
                    volume.dispatch_event("change")
                    assert not page.locator("#editRedo").is_enabled(), "New edit must clear redo"
                    final_audio = portable_snapshot("audio-volume-branched.json")
                    assert abs(float(final_audio["editAudioTrack"]["volume"]) - 0.6) < 0.001
                    assert final_audio["clips"] == redone["clips"]
                    # A04: title and order changes must undo/redo without media mutation.
                    before_title = portable_snapshot("before-title.json")
                    title_input = page.locator('input[placeholder="Titre incrusté"]').first
                    title_input.fill("Titre E2E A04")
                    title_input.dispatch_event("change")
                    titled = portable_snapshot("titled.json")
                    assert titled["clips"][0]["title"] == "Titre E2E A04"
                    page.locator("#editUndo").click()
                    assert portable_snapshot("title-undone.json")["clips"] == before_title["clips"]
                    page.locator("#editRedo").click()
                    assert portable_snapshot("title-redone.json")["clips"] == titled["clips"]
                    # Second clip moves to first position; the same IDs and audio remain.
                    assert page.locator('input[placeholder="Titre incrusté"]').count() == 3
                    page.locator('input[placeholder="Titre incrusté"]').nth(1).locator("..").locator('button[title="Monter"]').click()
                    reordered = portable_snapshot("reordered.json")
                    assert reordered["clips"][0]["id"] == titled["clips"][1]["id"]
                    assert reordered["clips"][1]["id"] == titled["clips"][0]["id"]
                    assert reordered["editAudioTrack"] == titled["editAudioTrack"]
                    page.locator("#editUndo").click()
                    assert portable_snapshot("order-undone.json")["clips"] == titled["clips"]
                    page.locator("#editRedo").click()
                    order_redone = portable_snapshot("order-redone.json")
                    assert order_redone["clips"] == reordered["clips"]
                    assert {a["id"] for a in order_redone["embeddedAssets"]} == {a["id"] for a in titled["embeddedAssets"]}
                    print("EDIT title/order undo/redo UI: clips, audio and media preserved")
                    print("EDIT audio undo/redo UI: volume restored and redo invalidated")
                    assert not errors, "JS errors during undo/redo: " + " | ".join(errors)
                    print("EDIT undo/redo UI: split restored, audio and source preserved")
                    with page.expect_download(timeout=15000) as split_info:
                        page.locator("#btnPortable").click()
                    split_path = Path(temp) / "split-portable.json"
                    split_info.value.save_as(split_path)
                    split_project = json.loads(split_path.read_text(encoding="utf-8"))
                    video_clips = [c for c in split_project["clips"] if c["kind"] == "video"]
                    assert len(video_clips) == 2, split_project["clips"]
                    assert video_clips[0]["id"] != video_clips[1]["id"]
                    assert video_clips[0]["assetId"] == video_clips[1]["assetId"]
                    assert abs(float(video_clips[0]["outPoint"]) - float(video_clips[1]["inPoint"])) < 0.1
                    assert all(0.1 <= float(c["duration"]) <= 2 for c in video_clips)
                    media_ids = [a["id"] for a in split_project["embeddedAssets"]]
                    assert len(media_ids) == len(set(media_ids)) == 3, media_ids
                    page.reload(wait_until="load")
                    page.locator("#fileProject").set_input_files(str(split_path))
                    page.locator("#status").get_by_text("Projet chargé", exact=False).wait_for(timeout=10000)
                    with page.expect_download(timeout=15000) as again_info:
                        page.locator("#btnPortable").click()
                    again_path = Path(temp) / "split-restored.json"
                    again_info.value.save_as(again_path)
                    again = json.loads(again_path.read_text(encoding="utf-8"))
                    assert again["clips"] == split_project["clips"], "Split clips changed after Portable reload"
                    assert again["editAudioTrack"] == split_project["editAudioTrack"]
                    # A04: importing a project must not allow undo into a previous session.
                    page.locator('[data-space="EDIT"]').first.click()
                    page.locator("#editUndo").wait_for(state="visible")
                    assert not page.locator("#editUndo").is_enabled(), "Undo history leaked across project reload"
                    assert not page.locator("#editRedo").is_enabled(), "Redo history leaked across project reload"
                    assert {a["id"] for a in again["embeddedAssets"]} == set(media_ids)
                    assert not errors, "JS errors during video split roundtrip: " + " | ".join(errors)
                    print("EDIT split Portable: two segments, one source, three unique media")

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
