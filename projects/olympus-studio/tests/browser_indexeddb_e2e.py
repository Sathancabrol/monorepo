"""Real-origin Chromium E2E: persistent media, split clips, portable roundtrip.

Run from Studio root: python tests/browser_indexeddb_e2e.py
Requires playwright + Chromium; no cloud, user media, or Windows claim.
"""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import socket
import subprocess
import time

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def wait_for_server(port, proc):
    for _ in range(80):
        if proc.poll() is not None:
            raise RuntimeError("Le serveur Node a quitté avant le test")
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError("Le serveur local n'a pas démarré")


def main():
    chrome = os.environ.get("OLYMPUS_CHROME") or next(
        (v for cmd in ("chromium", "google-chrome", "chrome") if (v := shutil.which(cmd))),
        None,
    )
    port = free_port()
    proc = subprocess.Popen(
        ["node", "server.mjs"],
        cwd=ROOT,
        env={**os.environ, "OLYMPUS_PORT": str(port)},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    try:
        wait_for_server(port, proc)
        with sync_playwright() as playwright:
            options = {"headless": True, "args": ["--no-sandbox"]}
            if chrome:
                options["executable_path"] = chrome
            browser = playwright.chromium.launch(**options)
            try:
                context = browser.new_context(accept_downloads=True)
                page = context.new_page()
                page.goto(f"http://127.0.0.1:{port}/", wait_until="load")
                # Real UI path: import a tiny PNG through the file picker, then
                # verify the persisted record after a full browser reload.
                # This complements direct store API checks below.
                import base64
                png = base64.b64decode(
                    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
                    "AAAADUlEQVQIHWP4z8DwHwAFgAI/ScL/nwAAAABJRU5ErkJggg=="
                )
                page.locator("#fileMedia").set_input_files({
                    "name": "olympus-ui-fixture.png",
                    "mimeType": "image/png",
                    "buffer": png,
                })
                page.get_by_text("olympus-ui-fixture.png", exact=True).first.wait_for(timeout=10000)
                ui_asset = page.evaluate("""async () => {
                  const store = await import('/src/media-store.js');
                  const db = await store.openMediaDB();
                  try {
                    const assets = await store.listMedia(db);
                    const item = assets.find(x=>x.name==='olympus-ui-fixture.png');
                    if (!item) throw Error('UI import absent from IndexedDB');
                    return {id:item.id,size:item.blob.size};
                  } finally { db.close(); }
                }""")
                assert ui_asset["size"] == len(png)
                # UI portable export: the layer must be referenced and the
                # original media embedded exactly once, not only stored in DB.
                with page.expect_download(timeout=15000) as download_info:
                    page.locator("#btnPortable").click()
                download = download_info.value
                assert download.suggested_filename.startswith("olympus-portable-")
                import json
                portable = json.loads(Path(download.path()).read_text(encoding="utf-8"))
                assert portable["format"] == "olympus-studio-project"
                assert portable["portable"] is True
                assert len(portable["embeddedAssets"]) == 1
                assert portable["embeddedAssets"][0]["id"] == ui_asset["id"]
                assert any(
                    layer.get("id") == ui_asset["id"]
                    for scene in portable["scenes"]
                    for layer in scene["layers"]
                ), "UI media layer absent from exported project"
                # Simulate loss of the local media vault. A portable import
                # must restore the original bytes and the visible scene.
                page.evaluate("""async id => {
                  const store = await import('/src/media-store.js');
                  const db = await store.openMediaDB();
                  try { await store.deleteMedia(db,id); } finally { db.close(); }
                }""", ui_asset["id"])
                page.reload(wait_until="load")
                page.locator("#fileProject").set_input_files(str(download.path()))
                page.locator("#status").get_by_text(
                    "Projet chargé", exact=False
                ).wait_for(timeout=10000)
                assert page.locator("#layers").get_by_text(
                    "olympus-ui-fixture.png", exact=False
                ).count() > 0, "Restored image not visible in UI layers"
                restored_ui = page.evaluate("""async ({id,size}) => {
                  const store = await import('/src/media-store.js');
                  const db = await store.openMediaDB();
                  try {
                    const record = await store.getMedia(db,id);
                    if (!record || record.blob.size!==size) throw Error('Portable UI media missing');
                    const bytes = new Uint8Array(await record.blob.arrayBuffer());
                    return Array.from(bytes);
                  } finally { db.close(); }
                }""", ui_asset)
                assert restored_ui == list(png), "Portable UI changed media bytes"
                page.reload(wait_until="load")
                ui_check = page.evaluate("""async ({id,size}) => {
                  const store = await import('/src/media-store.js');
                  const db = await store.openMediaDB();
                  try {
                    const item = await store.getMedia(db,id);
                    if (!item || item.blob.size!==size) throw Error('UI asset lost after reload');
                    return true;
                  } finally { await store.deleteMedia(db,id); db.close(); }
                }""", ui_asset)
                assert ui_check, "Le média importé via l'interface ne survit pas au rechargement"
                result = page.evaluate("""async () => {
                  const store = await import('/src/media-store.js');
                  const storyboard = await import('/src/storyboard.js');
                  const db = await store.openMediaDB();
                  const id = 'e2e-' + Date.now() + '-' + Math.random().toString(36).slice(2);
                  const bytes = new Uint8Array([26, 45, 0, 255, 10, 67]);
                  const blob = new Blob([bytes], {type:'video/webm'});
                  await store.putMedia(db, {id, name:'fixture.webm', type:'video/webm', blob});
                  const first = await store.getMedia(db, id);
                  if (!first || first.blob.size !== bytes.length) throw Error('put/get IndexedDB');
                  db.close();
                  return {id, expected:Array.from(bytes)};
                }""")
                # A real navigation is essential: memory-only mocks would pass falsely.
                page.reload(wait_until="load")
                check = page.evaluate("""async ({id,expected}) => {
                  const store = await import('/src/media-store.js');
                  const sb = await import('/src/storyboard.js');
                  const db = await store.openMediaDB();
                  try {
                    const record = await store.getMedia(db,id);
                    if (!record) throw Error('Media lost after reload');
                    const data = Array.from(new Uint8Array(await record.blob.arrayBuffer()));
                    if (JSON.stringify(data)!==JSON.stringify(expected)) throw Error('Blob bytes changed');
                    // Two segments share ONE media asset; exporting must not duplicate it.
                    const clips = sb.splitVideoClip({id:'left',kind:'video',assetId:id,inPoint:0,outPoint:2,duration:2},1,'right');
                    if (clips[0].outPoint !== clips[1].inPoint || clips[1].outPoint !== 2) throw Error('Split boundaries changed');
                    const refs = sb.referencedAssetIds([],clips);
                    if (refs.length!==1 || refs[0]!==id) throw Error('Split asset dedup failed');
                    const packed = await store.exportPortableAssets([record]);
                    if (packed.length!==1) throw Error('Portable duplicate');
                    const restored = store.importPortableAsset(packed[0]);
                    const restoredBytes = Array.from(new Uint8Array(await restored.blob.arrayBuffer()));
                    if (JSON.stringify(restoredBytes)!==JSON.stringify(expected)) throw Error('Portable mismatch');
                    return {origin:location.origin,clips:clips.length,assets:packed.length,bytes:restoredBytes.length};
                  } finally {
                    await store.deleteMedia(db,id);
                    db.close();
                  }
                }""", result)
                assert check["clips"] == 2 and check["assets"] == 1
                # The Portable roundtrip must also survive a second real navigation
                # and a fresh IndexedDB transaction, not just an in-memory Blob.
                restored = page.evaluate("""async ({id,expected}) => {
                  const store = await import('/src/media-store.js');
                  const db = await store.openMediaDB();
                  try {
                    const source = new Blob([new Uint8Array(expected)], {type:'video/webm'});
                    const exported = await store.exportPortableAssets([
                      {id, name:'fixture.webm', type:'video/webm', blob:source}
                    ]);
                    const imported = store.importPortableAsset(exported[0]);
                    await store.putMedia(db, imported);
                    return {size: imported.size};
                  } finally { db.close(); }
                }""", result)
                assert restored["size"] == len(result["expected"])
                page.reload(wait_until="load")
                after_second_reload = page.evaluate("""async ({id,expected}) => {
                  const store = await import('/src/media-store.js');
                  const db = await store.openMediaDB();
                  try {
                    const media = await store.getMedia(db,id);
                    if (!media) throw Error('Portable restore lost after reload');
                    const bytes = Array.from(new Uint8Array(await media.blob.arrayBuffer()));
                    if (JSON.stringify(bytes)!==JSON.stringify(expected))
                      throw Error('Portable restore changed bytes');
                    return {persisted: true, bytes: bytes.length};
                  } finally {
                    await store.deleteMedia(db,id);
                    db.close();
                  }
                }""", result)
                assert after_second_reload["persisted"]
                print("Chromium HTTP + IndexedDB E2E OK:", check, after_second_reload)
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
