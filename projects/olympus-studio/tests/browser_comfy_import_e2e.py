"""Chromium E2E: GENERATE -> ComfyUI loopback -> LIBRARY IndexedDB (synthetic PNG).
No external service, Windows or GPU is claimed. Run from project root.
"""
import base64
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import socket
import subprocess
import threading
import time
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
JOB = "12345678-1234-4234-8234-123456789abc"
PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4z8DwHwAFgAI/ScL/nwAAAABJRU5ErkJggg==")
HISTORY = {JOB: {"status": {"completed": True, "status_str": "success"}, "outputs": {"3": {"images": [{"filename": "comfy-fixture.png", "subfolder": "renders", "type": "output"}]}}}}

class MockComfy(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_POST(self):
        if self.path != "/prompt":
            self.send_error(404)
            return
        size = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(size))
        assert isinstance(payload["prompt"], dict)
        self.respond(json.dumps({"prompt_id": JOB}).encode())

    def do_GET(self):
        if self.path == "/history/" + JOB:
            self.respond(json.dumps(HISTORY).encode())
        elif self.path.startswith("/view?"):
            from urllib.parse import parse_qs, urlsplit
            query = parse_qs(urlsplit(self.path).query)
            assert query.get("filename") == ["comfy-fixture.png"]
            assert query.get("type") == ["output"]
            self.respond(PNG, "image/png")
        else:
            self.send_error(404)

    def respond(self, data, mime="application/json"):
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]

def main():
    try:
        mock = ThreadingHTTPServer(("127.0.0.1", 8188), MockComfy)
    except OSError as exc:
        if getattr(exc, "errno", None) in (98, 10048):
            print("SKIP: ComfyUI port 8188 already occupied; do not interfere")
            return
        raise
    thread = threading.Thread(target=mock.serve_forever, daemon=True)
    thread.start()
    port = free_port()
    server = subprocess.Popen(["node", "server.mjs"], cwd=ROOT,
        env={**os.environ, "OLYMPUS_PORT": str(port)}, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    try:
        for _ in range(100):
            if server.poll() is not None:
                raise RuntimeError("Studio server exited")
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                    break
            except OSError:
                time.sleep(0.1)
        else:
            raise RuntimeError("Studio server startup timed out")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            try:
                page = browser.new_page()
                errors = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.goto(f"http://127.0.0.1:{port}/")
                page.wait_for_function("document.querySelectorAll('#navItems [data-space]').length === 12")
                page.locator('[data-space="GENERATE"]').first.click()
                page.get_by_role("button", name="Envoyer à ComfyUI local").click()
                page.get_by_role("button", name="Vérifier le dernier job").click()
                page.locator('[data-comfy-output="0"]').wait_for()
                page.locator('[data-comfy-output="0"]').click()
                page.locator("#status").get_by_text("Résultat ComfyUI importé", exact=False).wait_for(timeout=15000)
                page.get_by_text("comfy-fixture.png", exact=True).first.wait_for()
                data = page.evaluate("""async () => {
                  const db = await new Promise((resolve,reject) => {
                    const req=indexedDB.open('olympus-studio-assets');
                    req.onsuccess=()=>resolve(req.result); req.onerror=()=>reject(req.error);
                  });
                  const tx=db.transaction('assets','readonly'); const items=await new Promise((resolve,reject)=>{const q=tx.objectStore('assets').getAll();q.onsuccess=()=>resolve(q.result);q.onerror=()=>reject(q.error);}); db.close(); const entry=items.find(x=>x.name==='comfy-fixture.png'||x.filename==='comfy-fixture.png'); return {count:items.length,entry:entry?{size:entry.blob?.size,type:entry.blob?.type}:null};
                }""")
                assert data["entry"] and data["entry"]["size"] == len(PNG), ("IndexedDB output missing or wrong bytes", data)
                page.reload()
                persisted = page.evaluate("""async () => {
                  const db = await new Promise((resolve,reject)=>{const r=indexedDB.open('olympus-studio-assets');r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error);});
                  const tx=db.transaction('assets','readonly');
                  const rows=await new Promise((resolve,reject)=>{const q=tx.objectStore('assets').getAll();q.onsuccess=()=>resolve(q.result);q.onerror=()=>reject(q.error);});
                  db.close();return rows.map(r=>({name:r.name,size:r.blob?.size}));
                }""")
                assert any(x["name"] == "comfy-fixture.png" and x["size"] == len(PNG) for x in persisted), persisted
                assert not errors, errors
                print("ComfyUI GENERATE -> LIBRARY Chromium E2E: PASS (mock server, reload, IndexedDB)")
            finally:
                browser.close()
    finally:
        server.terminate()
        try: server.wait(timeout=5)
        except subprocess.TimeoutExpired: server.kill()
        mock.shutdown()
        mock.server_close()

if __name__ == "__main__":
    main()
