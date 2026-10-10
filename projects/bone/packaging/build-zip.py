#!/usr/bin/env python3
"""Assemble le ZIP Windows : extraire → double-clic INSTALLER.bat."""
from __future__ import annotations

import shutil
import subprocess
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BONE = HERE.parent
DIST = BONE / "dist"
STAGE = DIST / "Bone-Olympus-Install"
ZIP_PATH = DIST / "Bone-Olympus-Install.zip"

PAYLOAD_FILES = [
    "discord_bot.py",
    "persona.py",
    "persona.json",
    "requirements.txt",
    ".env.example",
]


def convert_ico(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        ["convert", str(src), "-define", "icon:auto-resize=256,128,64,48,32,16", str(dest)],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0 or not dest.exists():
        shutil.copy2(src, dest.with_suffix(".png"))


def write_bom(src: Path, dest: Path) -> None:
    text = src.read_text(encoding="utf-8")
    dest.write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))


def main() -> None:
    if STAGE.exists():
        shutil.rmtree(STAGE)
    DIST.mkdir(parents=True, exist_ok=True)
    payload = STAGE / "payload"
    assets = payload / "assets"
    assets.mkdir(parents=True)

    for name in PAYLOAD_FILES:
        shutil.copy2(BONE / name, payload / name)

    png = BONE / "assets" / "bone.png"
    shutil.copy2(png, assets / "bone.png")
    convert_ico(png, assets / "bone.ico")

    write_bom(HERE / "installer.ps1", STAGE / "installer.ps1")
    shutil.copy2(HERE / "INSTALLER.bat", STAGE / "INSTALLER.bat")
    write_bom(HERE / "LIREMOI.txt", STAGE / "LIREMOI.txt")

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as z:
        for p in STAGE.rglob("*"):
            if p.is_file():
                z.write(p, p.relative_to(STAGE.parent))
    print(f"OK {ZIP_PATH} ({ZIP_PATH.stat().st_size} octets)")
    print("Contenu :")
    with zipfile.ZipFile(ZIP_PATH) as z:
        for n in z.namelist():
            print(" ", n)


if __name__ == "__main__":
    main()
