"""Chromium real HTTP/IndexedDB E2E for EDIT manifest import and undo/redo.
Synthetic assets only. Does not claim Windows hardware validation.
Run: python tests/browser_edit_manifest_e2e.py
"""
import base64
import json
import os
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
    with page.expect_download(timeout=15000) as info:
        page.locator("#btnPortable").click()
    path = folder / name
    info.value.save_as(path)
    return json.loads(path.read_text(encoding="utf-8"))

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
                        try { await m.deleteMedia(db, id); } finally { db.close(); }
                    }""", asset)
                    upload_manifest(page, manifest)
                    page.locator("#status").get_by_text(
                        "Import EDIT refusé, montage inchangé", exact=False
                    ).wait_for()
                    assert portable(page, folder, "after-deletion.json")["clips"] == imported["clips"]
                    page.locator("#editUndo").click()
                    page.locator("#status").get_by_text("Montage annulé", exact=False).wait_for()
                    undone = portable(page, folder, "undo.json")
                    assert undone["clips"] == baseline["clips"]
                    page.locator("#editRedo").click()
                    page.locator("#status").get_by_text("Montage rétabli", exact=False).wait_for()
                    redone = portable(page, folder, "redo.json")
                    assert redone["clips"] == imported["clips"]
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
