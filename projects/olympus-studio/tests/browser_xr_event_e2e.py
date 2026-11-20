"""Chromium E2E for the actual XR UI -> validated local bus -> scene layers.

No webcam, network adapter, or external action is invoked.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from browser_indexeddb_e2e import ROOT, free_port, wait_for_server
import os
import subprocess
from playwright.sync_api import sync_playwright

def main():
    port = free_port()
    proc = subprocess.Popen(["node", "server.mjs"], cwd=ROOT,
        env={**os.environ, "OLYMPUS_PORT": str(port)},
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    try:
        wait_for_server(port, proc)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            try:
                page = browser.new_page()
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.goto(f"http://127.0.0.1:{port}/", wait_until="load")
                page.locator('#navItems [data-space="XR"]').click()
                field = page.get_by_role("textbox", name="Événement XR JSON")
                field.fill('{"type":"detections","items":[{"label":"test-hand","x":0.1,"y":0.2,"w":0.3,"h":0.4}]}')
                page.get_by_role("button", name="Importer détections").click()
                page.get_by_text("Détections XR validées", exact=False).wait_for()
                # The UI must create a real scene layer, not only report success.
                page.locator('#layers').get_by_text("XR · test-hand", exact=False).wait_for()
                before = page.locator('#layers').inner_text()
                page.get_by_role("button", name="Simuler claquement de doigts").click()
                page.get_by_text("Geste XR simulé", exact=False).wait_for()
                # Invalid geometry is rejected before it can create a layer.
                field.fill('{"type":"detections","items":[{"label":"bad","x":0.95,"y":0,"w":0.2,"h":0.2}]}')
                page.get_by_role("button", name="Importer détections").click()
                page.get_by_text("Événement invalide", exact=False).wait_for()
                assert "XR · bad" not in page.locator('#layers').inner_text()
                assert "XR · test-hand" in before
                assert not errors, errors
                print("XR real HTTP/Chromium UI event-bus E2E OK")
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
