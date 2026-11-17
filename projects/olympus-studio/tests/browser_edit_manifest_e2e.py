"""Chromium real HTTP/IndexedDB E2E for EDIT manifest import and undo/redo.
Synthetic assets only. Does not claim Windows hardware validation.
Run: python tests/browser_edit_manifest_e2e.py
"""
import base64
import json
import os
import shutil
from pathlib import Path
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

def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]

def portable(page, folder, name):
    """One attempt only: preserve the actual UI failure instead of retrying it."""
    button = page.locator("#btnPortable")
    try:
        with page.expect_download(timeout=15000) as info:
            button.click()
        path = folder / name
        info.value.save_as(path)
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not payload.get("portable"):
            raise AssertionError(f"{name}: download is not a portable project")
        return payload
    except Exception as exc:
        # The asynchronous IndexedDB/encoding path can fail after the click.
        # Preserve the status and control state to distinguish application
        # rejection from a browser download event that was never emitted.
        diagnostic = {
            "checkpoint": name,
            "error": str(exc),
            "status": page.locator("#status").inner_text(timeout=3000),
            "buttonDisabled": button.is_disabled(timeout=3000),
        }
        (folder / f"{name}.failure.json").write_text(
            json.dumps(diagnostic, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        evidence_dir = os.environ.get("OLYMPUS_MANIFEST_EVIDENCE_DIR")
        if evidence_dir:
            target = Path(evidence_dir)
            target.mkdir(parents=True, exist_ok=True)
            shutil.copy2(folder / f"{name}.failure.json", target / f"{name}.failure.json")
        print("PORTABLE FAILURE:", json.dumps(diagnostic, ensure_ascii=False), flush=True)
        raise

def upload_manifest(page, manifest):
    page.locator("#editManifestFile").set_input_files({
        "name": "edit-interchange.json", "mimeType": "application/json",
        "buffer": json.dumps(manifest).encode("utf-8"),
    })

def main():
    with tempfile.TemporaryDirectory(prefix="olympus-manifest-") as temp:
        folder = Path(temp)
        port = free_port()
        proc = subprocess.Popen(
            ["node", "server.mjs"], cwd=ROOT,
            env={**os.environ, "OLYMPUS_PORT": str(port)},
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        )
        try:
            for _ in range(100):
                if proc.poll() is not None:
                    raise RuntimeError("Studio server exited")
                try:
                    with socket.create_connection(("127.0.0.1", port), timeout=.2):
                        break
                except OSError:
                    time.sleep(.1)
            else:
                raise RuntimeError("Studio server did not start")
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True, args=["--no-sandbox"])
                try:
                    page = browser.new_page(accept_downloads=True)
                    # Explicitly allow repeated automated downloads in this isolated
                    # Chromium context. The manifest E2E deliberately exports many
                    # portable snapshots; Chromium may otherwise suppress later
                    # downloads without a page JavaScript error.
                    cdp = page.context.new_cdp_session(page)
                    cdp.send("Browser.setDownloadBehavior", {
                        "behavior": "allow",
                        "downloadPath": str(folder),
                        "eventsEnabled": True,
                    })
                    errors = []
                    page.on("pageerror", lambda err: errors.append(str(err)))
                    page.goto(f"http://127.0.0.1:{port}/", wait_until="load")
                    page.wait_for_function(
                        "document.querySelectorAll('#navItems [data-space]').length===12"
                    )
                    page.locator("#fileMedia").set_input_files({
                        "name": "manifest-fixture.png", "mimeType": "image/png",
                        "buffer": PNG,
                    })
                    page.get_by_text("manifest-fixture.png", exact=True).first.wait_for()
                    asset = page.evaluate("""async () => {
                        const m = await import('/src/media-store.js');
                        const db = await m.openMediaDB();
                        try {
                            const assets = await m.listMedia(db);
                            const a = assets.find(x => x.name === 'manifest-fixture.png');
                            if (!a) throw Error('Missing IndexedDB fixture');
                            return a.id;
                        } finally { db.close(); }
                    }""")
                    page.locator('[data-space="EDIT"]').first.click()
                    page.get_by_role("button", name="+ Clip").click()
                    baseline = portable(page, folder, "before.json")
                    assert len(baseline["clips"]) == 1
                    manifest = {
                        "schema": "olympus.edit.interchange.v1",
                        "timeUnit": "seconds",
                        "duration": 3,
                        "segments": [
                            {"clipId": "manifest-clip-1", "assetId": asset,
                             "kind": "image", "timelineStart": 0, "duration": 3,
                             "sourceIn": 0, "title": "Imported fixture"}
                        ],
                        "soundtrack": None,
                    }
                    upload_manifest(page, manifest)
                    page.locator("#status").get_by_text(
                        "Manifeste EDIT importé", exact=False
                    ).wait_for()
                    imported = portable(page, folder, "imported.json")
                    assert len(imported["clips"]) == 1
                    assert imported["clips"][0]["id"] == "manifest-clip-1"
                    assert imported["clips"][0]["title"] == "Imported fixture"
                    assert imported["clips"][0]["assetId"] == asset
                    assert len(imported["embeddedAssets"]) == 1
                    # A missing asset must reject the whole operation atomically.
                    missing = json.loads(json.dumps(manifest))
                    missing["segments"][0]["assetId"] = "missing-media-id"
                    upload_manifest(page, missing)
                    page.locator("#status").get_by_text(
                        "Import EDIT refusé, montage inchangé", exact=False
                    ).wait_for()
                    after_missing = portable(page, folder, "after-missing.json")
                    assert after_missing["clips"] == imported["clips"]
                    assert after_missing["editAudioTrack"] == imported["editAudioTrack"]
                    # A record absent from IndexedDB but still present in the
                    # in-memory library must also be rejected.
                    page.evaluate("""async id => {
                        const m = await import('/src/media-store.js');
                        const db = await m.openMediaDB();
                        try {
                            window.__manifestDeletedRecord = await m.getMedia(db, id);
                            if (!window.__manifestDeletedRecord) throw Error('Fixture missing before deletion');
                            await m.deleteMedia(db, id);
                        } finally { db.close(); }
                    }""", asset)
                    upload_manifest(page, manifest)
                    page.locator("#status").get_by_text(
                        "Import EDIT refusé, montage inchangé", exact=False
                    ).wait_for()
                    # Portable export cannot embed a deleted media blob. Restore the
                    # exact IndexedDB record before checking unchanged clips;
                    # the rejected manifest must not have recreated it.
                    page.evaluate("""async id => {
                        const m = await import('/src/media-store.js');
                        const db = await m.openMediaDB();
                        try {
                            if (await m.getMedia(db, id)) throw Error('Rejected import restored deleted asset');
                            await m.putMedia(db, window.__manifestDeletedRecord);
                            delete window.__manifestDeletedRecord;
                        } finally { db.close(); }
                    }""", asset)
                    assert portable(page, folder, "after-deletion.json")["clips"] == imported["clips"]
                    page.locator("#editUndo").click()
                    page.locator("#status").get_by_text("Montage annulé", exact=False).wait_for()
                    undone = portable(page, folder, "undo.json")
                    assert undone["clips"] == baseline["clips"]
                    page.locator("#editRedo").click()
                    page.locator("#status").get_by_text("Montage rétabli", exact=False).wait_for()
                    redone = portable(page, folder, "redo.json")
                    assert redone["clips"] == imported["clips"]
                    # Concurrency: reject a valid manifest while MediaRecorder is
                    # active. A rejected import must not mutate timeline/history
                    # or interrupt the ongoing export.
                    with page.expect_download(timeout=25000) as active_export:
                        page.get_by_role("button", name="Exporter WebM (audio optionnel)").click()
                        page.locator("#status").get_by_text(
                            "Export storyboard vidéo seule en cours", exact=False
                        ).wait_for()
                        upload_manifest(page, manifest)
                        page.locator("#status").get_by_text(
                            "Import refusé pendant export EDIT", exact=False
                        ).wait_for()
                    active_path = folder / "concurrent-export.webm"
                    active_export.value.save_as(active_path)
                    assert active_path.stat().st_size > 0, "Concurrent import interrupted WebM export"
                    after_export = portable(page, folder, "after-concurrent-export.json")
                    assert after_export["clips"] == imported["clips"], "Import mutated EDIT during export"
                    assert after_export["editAudioTrack"] == imported["editAudioTrack"]
                    # Rejected concurrent import must not push a history entry:
                    # the next undo must reach the pre-import baseline directly.
                    page.locator("#editUndo").click()
                    page.locator("#status").get_by_text("Montage annulé", exact=False).wait_for()
                    assert portable(page, folder, "undo-concurrent-rejection.json")["clips"] == baseline["clips"], (
                        "Rejected concurrent manifest inserted an undo history entry"
                    )
                    page.locator("#editRedo").click()
                    page.locator("#status").get_by_text("Montage rétabli", exact=False).wait_for()
                    assert portable(page, folder, "redo-concurrent-rejection.json")["clips"] == imported["clips"], (
                        "Redo after rejected concurrent manifest did not restore the timeline"
                    )
                    # Once MediaRecorder stops, a fresh manifest must be accepted.
                    # This detects a stale export lock and verifies that undo/redo
                    # remain usable after a rejected concurrent import.
                    post_export_manifest = json.loads(json.dumps(manifest))
                    post_export_manifest["segments"][0]["title"] = "Accepted after export"
                    upload_manifest(page, post_export_manifest)
                    page.locator("#status").get_by_text(
                        "Manifeste EDIT importé", exact=False
                    ).wait_for()
                    accepted_after_export = portable(page, folder, "accepted-after-export.json")
                    assert accepted_after_export["clips"][0]["title"] == "Accepted after export"
                    page.locator("#editUndo").click()
                    page.locator("#status").get_by_text("Montage annulé", exact=False).wait_for()
                    assert portable(page, folder, "undo-after-export.json")["clips"] == imported["clips"]
                    page.locator("#editRedo").click()
                    page.locator("#status").get_by_text("Montage rétabli", exact=False).wait_for()
                    assert portable(page, folder, "redo-after-export.json")["clips"] == accepted_after_export["clips"]
                    # A malformed manifest after an export must not corrupt the
                    # recovered editor or insert a spurious undo history entry.
                    malformed_after_export = json.loads(json.dumps(post_export_manifest))
                    malformed_after_export["segments"][0]["assetId"] = "missing-after-export"
                    upload_manifest(page, malformed_after_export)
                    page.locator("#status").get_by_text(
                        "Import EDIT refusé, montage inchangé", exact=False
                    ).wait_for()
                    assert portable(page, folder, "invalid-after-export.json")["clips"] == accepted_after_export["clips"]
                    page.locator("#editUndo").click()
                    page.locator("#status").get_by_text("Montage annulé", exact=False).wait_for()
                    assert portable(page, folder, "undo-invalid-after-export.json")["clips"] == imported["clips"], (
                        "Rejected post-export import created an undo entry"
                    )
                    page.locator("#editRedo").click()
                    page.locator("#status").get_by_text("Montage rétabli", exact=False).wait_for()
                    assert portable(page, folder, "redo-invalid-after-export.json")["clips"] == accepted_after_export["clips"]
                    # Reload destroys all in-memory EDIT state. Re-import the
                    # actual portable download, then verify media and timeline
                    # from a fresh page/IndexedDB connection.
                    page.reload(wait_until="load")
                    page.wait_for_function(
                        "document.querySelectorAll('#navItems [data-space]').length===12"
                    )
                    page.locator("#fileProject").set_input_files(str(folder / "redo.json"))
                    page.locator("#status").get_by_text(
                        "Projet chargé", exact=False
                    ).wait_for()
                    restored = portable(page, folder, "restored-after-navigation.json")
                    assert restored["clips"] == imported["clips"], "EDIT timeline lost on navigation"
                    assert restored["editAudioTrack"] == imported["editAudioTrack"]
                    assert len(restored["embeddedAssets"]) == 1
                    assert restored["embeddedAssets"][0]["id"] == asset
                    assert not errors, "JavaScript errors: " + " | ".join(errors)
                    print("EDIT manifest HTTP/IndexedDB + rejection + undo/redo OK")
                finally:
                    browser.close()
        finally:
            proc.terminate()
            try:
                proc.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.communicate()

if __name__ == "__main__":
    main()
