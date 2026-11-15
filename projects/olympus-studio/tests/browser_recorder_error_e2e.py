"""Chromium regression: MediaRecorder error must not download a partial EDIT WebM.
Synthetic PNG only, real Studio HTTP and browser; no Windows claim.
"""
import base64
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
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]

def main():
    with tempfile.TemporaryDirectory(prefix="olympus-recorder-error-"):
        port = free_port()
        server = subprocess.Popen(
            ["node", "server.mjs"], cwd=ROOT,
            env={**os.environ, "OLYMPUS_PORT": str(port)},
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        )
        try:
            for _ in range(100):
                if server.poll() is not None:
                    raise RuntimeError("Studio server exited")
                try:
                    with socket.create_connection(("127.0.0.1", port), timeout=.2):
                        break
                except OSError:
                    time.sleep(.1)
            else:
                raise RuntimeError("Studio server timeout")
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True, args=["--no-sandbox"])
                try:
                    page = browser.new_page(accept_downloads=True)
                    errors = []
                    downloads = []
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    page.on("download", lambda download: downloads.append(download.suggested_filename))
                    page.add_init_script("""() => {
                        const Native = window.MediaRecorder;
                        window.__stoppedCaptureTracks = 0;
                        const nativeStop = MediaStreamTrack.prototype.stop;
                        MediaStreamTrack.prototype.stop = function(...args) {
                            window.__stoppedCaptureTracks++;
                            return nativeStop.apply(this, args);
                        };
                        window.MediaRecorder = new Proxy(Native, {
                            construct(Target, args) {
                                const recorder = new Target(...args);
                                const start = recorder.start.bind(recorder);
                                recorder.start = (...params) => {
                                    start(...params);
                                    setTimeout(() => {
                                        if (recorder.state === 'recording') {
                                            const event = new Event('error');
                                            Object.defineProperty(event, 'error', {
                                                value: new Error('Synthetic recorder failure')
                                            });
                                            recorder.dispatchEvent(event);
                                        }
                                    }, 100);
                                };
                                return recorder;
                            }
                        });
                    }""")
                    page.goto(f"http://127.0.0.1:{port}/", wait_until="load")
                    page.wait_for_function(
                        "document.querySelectorAll('#navItems [data-space]').length===12"
                    )
                    page.locator("#fileMedia").set_input_files({
                        "name": "recorder-error-fixture.png",
                        "mimeType": "image/png", "buffer": PNG,
                    })
                    page.get_by_text("recorder-error-fixture.png", exact=True).first.wait_for()
                    page.locator('[data-space="EDIT"]').first.click()
                    page.get_by_role("button", name="+ Clip").click()
                    page.get_by_role("button", name="Exporter WebM (audio optionnel)").click()
                    page.locator("#status").get_by_text(
                        "Export storyboard impossible : aucun fichier valide produit",
                        exact=False,
                    ).wait_for(timeout=15000)
                    page.wait_for_function("window.__stoppedCaptureTracks > 0")
                    page.wait_for_timeout(400)
                    assert not downloads, "Failed MediaRecorder produced download: " + repr(downloads)
                    assert not errors, "JavaScript errors: " + repr(errors)
                    print("MediaRecorder synthetic error: no partial WebM, tracks stopped, no JS errors")
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
