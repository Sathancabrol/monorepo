"""Chromium HTTP E2E: real EDIT button/Canvas PNG, mocked user-selected directory.
The File System Access picker and writable handles are simulated; this is NOT
a real OS permission or Windows filesystem test.
"""
import base64
import os
from pathlib import Path
import socket
import subprocess
import time
from playwright.sync_api import sync_playwright

ROOT = Path(os.environ.get("OLYMPUS_TEST_ROOT", Path(__file__).resolve().parents[1]))
PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
    "AAAADUlEQVQIHWP4z8DwHwAFgAI/ScL/nwAAAABJRU5ErkJggg=="
)


def main():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    proc = subprocess.Popen(
        ["node", "server.mjs"], cwd=ROOT,
        env={**os.environ, "OLYMPUS_PORT": str(port)},
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
    )
    try:
        for _ in range(100):
            if proc.poll() is not None:
                raise RuntimeError("HTTP server exited")
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=.2):
                    break
            except OSError:
                time.sleep(.1)
        else:
            raise RuntimeError("HTTP server timeout")
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
            try:
                page = browser.new_page()
                errors = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.goto(f"http://127.0.0.1:{port}/", wait_until="load")
                page.wait_for_function(
                    "document.querySelectorAll('#navItems [data-space]').length === 12"
                )
                page.add_init_script("void 0")  # no filesystem privileges granted
                page.evaluate("""() => {
                  const files = new Map();
                  window.__pngTestFiles = files;
                  window.__pngPickerCalls = 0;
                  window.showDirectoryPicker = async () => {
                    window.__pngPickerCalls++;
                    return {
                      async getFileHandle(name, options = {}) {
                        if (!options.create && !files.has(name))
                          throw new DOMException('Missing', 'NotFoundError');
                        if (options.create && !files.has(name)) files.set(name, null);
                        return {
                          async createWritable() {
                            let pending;
                            return {
                              async write(blob) { pending = blob; },
                              async close() { files.set(name, pending); },
                              async abort() { pending = null; }
                            };
                          }
                        };
                      }
                    };
                  };
                }""")
                page.locator("#fileMedia").set_input_files({
                    "name": "png-sequence-fixture.png",
                    "mimeType": "image/png", "buffer": PNG
                })
                page.get_by_text("png-sequence-fixture.png", exact=True).first.wait_for()
                page.locator('#navItems [data-space="EDIT"]').click()
                page.get_by_role("button", name="+ Clip").click()
                duration = page.locator(".layer-row input[title='Durée en secondes']").first
                duration.wait_for()
                duration.fill("1")
                duration.dispatch_event("change")
                guide_button = page.locator("#editFfmpegGuideButton")
                guide = page.locator("#editFfmpegGuide")
                assert guide.is_hidden()
                assert guide_button.get_attribute("aria-expanded") == "false"
                guide_button.click()
                assert guide.is_visible()
                assert guide_button.get_attribute("aria-expanded") == "true"
                assert "--max-end-delta 0.2" in page.locator("#editFfmpegCommand").inner_text()
                assert "Aucune piste audio active" in guide.inner_text()
                assert "MediaRecorder A/V reste expérimental" in guide.inner_text()
                guide_button.click()
                assert guide.is_hidden()
                assert guide_button.get_attribute("aria-expanded") == "false"
                page.locator("#editPngSequence").click()
                page.locator("#status").get_by_text(
                    "24 PNG exportés", exact=False
                ).wait_for(timeout=30000)
                result = page.evaluate("""async () => {
                  const files = [...window.__pngTestFiles.entries()];
                  const signatures = await Promise.all(files.map(async ([name, blob]) => ({
                    name, type: blob.type, size: blob.size,
                    magic: [...new Uint8Array(await blob.slice(0, 8).arrayBuffer())],
                    decoded: await (async () => {
                      const bitmap = await createImageBitmap(blob);
                      try {
                        const canvas = document.createElement('canvas');
                        canvas.width = bitmap.width;
                        canvas.height = bitmap.height;
                        const ctx = canvas.getContext('2d');
                        ctx.drawImage(bitmap, 0, 0);
                        const pixel = [...ctx.getImageData(0, 0, 1, 1).data];
                        return {width: bitmap.width, height: bitmap.height, pixel};
                      } finally { bitmap.close(); }
                    })()
                  })));
                  return {calls: window.__pngPickerCalls, signatures};
                }""")
                assert result["calls"] == 1
                assert len(result["signatures"]) == 24, result
                assert [s["name"] for s in result["signatures"]] == [
                    f"{i:06d}.png" for i in range(1, 25)
                ]
                assert all(s["type"] == "image/png" and s["size"] > 50 and
                           s["magic"] == [137, 80, 78, 71, 13, 10, 26, 10]
                           and s["decoded"]["width"] > 0 and s["decoded"]["height"] > 0
                           and s["decoded"]["pixel"][3] > 0
                           for s in result["signatures"]), result
                # The second export into the same selected directory must not overwrite.
                page.locator("#editPngSequence").click()
                page.locator("#status").get_by_text(
                    "Output file already exists", exact=False
                ).wait_for(timeout=15000)
                assert page.evaluate("window.__pngTestFiles.size") == 24
                assert not errors, errors
                print("Chromium EDIT PNG UI OK: 24 PNG bitmaps decoded and sampled; collision refused; directory mocked")
            finally:
                browser.close()
    finally:
        proc.terminate()
        try:
            proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate(timeout=5)


if __name__ == "__main__":
    main()
