"""Smoke test the actual distributable ZIP, not just the repository tree.

Requires Python 3 and Node >=20. No browser, GPU or external service required.
"""
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "olympus-studio-preview.zip"
REQUIRED = {
    "index.html", "server.mjs", "package.json", "LANCER_OLYMPUS.bat",
    "src/app.js", "src/media-store.js", "src/editor-export.js",
    "src/edit-audio.js", "src/storyboard.js",
    "docs/INTEGRATION_MATRIX_ALPHA.md",
}


def request(url):
    try:
        with urlopen(url, timeout=3) as response:
            return response.status, response.read()
    except HTTPError as exc:
        return exc.code, exc.read()


def main():
    assert ARCHIVE.is_file(), f"Missing distributable: {ARCHIVE}"
    with ZipFile(ARCHIVE) as archive:
        names = set(archive.namelist())
        missing = REQUIRED - names
        assert not missing, f"Missing ZIP files: {sorted(missing)}"
        assert archive.testzip() is None, "ZIP CRC failure"
        with tempfile.TemporaryDirectory(prefix="olympus-alpha-") as temp:
            target = Path(temp).resolve()
            for info in archive.infolist():
                dest = (target / info.filename).resolve()
                assert dest == target or target in dest.parents, "ZIP traversal"
            archive.extractall(target)
            with socket.socket() as sock:
                sock.bind(("127.0.0.1", 0))
                port = sock.getsockname()[1]
            env = dict(os.environ, OLYMPUS_PORT=str(port))
            proc = subprocess.Popen(
                ["node", "server.mjs"], cwd=target, env=env,
                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            )
            try:
                base = f"http://127.0.0.1:{port}"
                for _ in range(50):
                    if proc.poll() is not None:
                        raise AssertionError(f"Server exited early: {proc.returncode}")
                    try:
                        status, body = request(base + "/index.html")
                        if status == 200:
                            break
                    except (URLError, TimeoutError):
                        pass
                    time.sleep(0.1)
                else:
                    raise AssertionError("Packaged HTTP server did not start")
                assert b"<html" in body.lower(), "Invalid HTML"
                status, body = request(base + "/api/health")
                assert status == 200 and json.loads(body)["ok"] is True
                for path in ("/src/app.js", "/src/media-store.js", "/src/editor-export.js"):
                    status, body = request(base + path)
                    assert status == 200 and body, f"Missing served module: {path}"
                for path in ("/server.mjs", "/package.json", "/docs/INTEGRATION_MATRIX_ALPHA.md"):
                    status, _ = request(base + path)
                    assert status in (403, 404), f"Private file exposed: {path} ({status})"
                print("PASS: ZIP integrity, extracted Node HTTP, public modules, private-file isolation")
            finally:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=5)


if __name__ == "__main__":
    main()
