"""Optional Chromium end-to-end smoke for OLYMPUS Studio's sequential EDIT UI.

Development-only requirements: Python Playwright, FFmpeg, and Chromium/Chrome.
Does not use network requests, external accounts, GPUs, paid services or IndexedDB.
Runs the real UI source and its ES modules using in-memory data: URLs because
some isolated browser environments block all HTTP navigation.
"""
from __future__ import annotations

import base64
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
MODULE_IMPORT = re.compile(r"from ['\"](\./[^'\"]+\.js)['\"]")
STYLESHEET = re.compile(r'<link rel="stylesheet" href="/src/([^"]+)"\s*/?>')
MODULE_TAG = re.compile(r'<script type="module" src="[^"]+"\s*></script>')


def bundle_module(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    source = MODULE_IMPORT.sub(
        lambda match: "from '" + bundle_module(path.parent / match.group(1)) + "'",
        source,
    )
    return "data:text/javascript;base64," + base64.b64encode(source.encode()).decode()


def inline_html() -> str:
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    html = STYLESHEET.sub(
        lambda match: "<style>" + (ROOT / "src" / match.group(1)).read_text(encoding="utf-8") + "</style>",
        html,
    )
    return MODULE_TAG.sub("", html)


def create_fixture(path: Path) -> None:
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", "testsrc=size=320x180:rate=24",
            "-t", "2.0", "-c:v", "libvpx-vp9", "-b:v", "450k",
            "-an", "-y", str(path),
        ],
        check=True,
    )


def main() -> None:
    chrome = os.environ.get("OLYMPUS_CHROME") or next(
        (v for cmd in ("chromium", "google-chrome", "chrome") if (v := shutil.which(cmd))),
        None,
    )
    if not chrome:
        raise SystemExit("Chromium/Chrome non trouvé (OLYMPUS_CHROME peut le définir)")

    with tempfile.TemporaryDirectory(prefix="olympus-studio-e2e-") as tmp:
        fixture = Path(tmp) / "source-2s.webm"
        create_fixture(fixture)
        soundtrack = Path(tmp) / "tone-2s.wav"
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000",
            "-t", "2.0", "-c:a", "pcm_s16le", "-y", str(soundtrack),
        ], check=True)
        errors: list[str] = []

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                executable_path=chrome,
                headless=True,
                args=["--no-sandbox", "--autoplay-policy=no-user-gesture-required"],
            )
            try:
                page = browser.new_page(viewport={"width": 1440, "height": 900})
                page.on("pageerror", lambda err: errors.append(str(err)))
                page.set_content(inline_html())
                for script in ("app.js", "obs-panel.js"):
                    page.evaluate("async url => await import(url)", bundle_module(ROOT / "src" / script))

                assert page.locator("[data-space]").count() == 12
                page.locator("#fileMedia").set_input_files(str(fixture))
                page.get_by_text("source-2s.webm", exact=True).first.wait_for(timeout=10000)
                page.locator('[data-space="EDIT"]').click()
                page.get_by_role("button", name="+ Clip").click()
                page.get_by_text("Source : 2.00 s").wait_for(timeout=12000)

                out_field = page.locator('[aria-label^="OUT (s)"]').first
                assert abs(float(out_field.input_value()) - 2) < 0.1
                out_field.fill("5")
                out_field.dispatch_event("change")
                assert "dépasse la durée source" in page.locator("#status").inner_text()

                page.locator("#editSeek").fill("1")
                page.get_by_role("button", name="Diviser au curseur").click()
                assert page.locator('[aria-label^="IN (s)"]').count() == 2
                assert "divisé au curseur" in page.locator("#status").inner_text()

                # The soundtrack is an independent asset, not a new VIDEO/IMAGE LIVE overlay.
                page.locator("#fileMedia").set_input_files(str(soundtrack))
                audio_choice = page.locator('select[aria-label="Choisir une piste audio"] option')
                audio_choice.first.wait_for(timeout=10000)
                page.get_by_role("button", name="Ajouter / remplacer piste").click()
                page.locator('[aria-label="Audio Départ projet (s)"]').wait_for(timeout=10000)
                offset = page.locator('[aria-label="Audio Départ projet (s)"]')
                offset.fill("0.5")
                offset.dispatch_event("change")
                assert page.locator('[aria-label="Audio Départ projet (s)"]').input_value() == "0.5"
                assert page.get_by_role("button", name="Exporter WebM (audio optionnel)").count() == 1
                if errors:
                    raise AssertionError("Erreurs JavaScript : " + " | ".join(errors))
                print("Chromium E2E OK : vidéo 2s, découpe, audio WAV importé, départ 0.5s, 0 JS error (export non validé)")
            finally:
                browser.close()


if __name__ == "__main__":
    main()
