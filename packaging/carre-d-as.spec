# -*- mode: python ; coding: utf-8 -*-
"""Construction de l'exécutable Windows avec PyInstaller.

    pip install pyinstaller
    python -m PyInstaller packaging/carre-d-as.spec --noconfirm

Le point important : les dossiers `data/` de chaque module et l'interface
`carredas/ui` doivent être embarqués, sinon l'application démarre à vide.
"""

import glob
import os
from pathlib import Path

ICI = Path(SPECPATH).parent

donnees = [(str(ICI / "carredas" / "ui"), "carredas/ui")]
for dossier in sorted(glob.glob(str(ICI / "carredas" / "modules" / "*" / "data"))):
    rel = os.path.relpath(dossier, str(ICI))
    donnees.append((dossier, rel))

modules_caches = [
    "carredas.server",
    "carredas.updater",
    "carredas.desktop",
    "carredas.llm",
    "carredas.docsgen",
]

block_cipher = None

a = Analysis(
    [str(ICI / "main.py")],
    pathex=[str(ICI)],
    binaries=[],
    datas=donnees,
    hiddenimports=modules_caches,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter", "matplotlib", "numpy", "pandas", "PIL",
        "PyQt5", "PySide2", "pytest", "IPython",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="CarreDAs",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,          # aucune fenêtre de console : c'est une application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(ICI / "packaging" / "icone.ico") if (ICI / "packaging" / "icone.ico").exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="CarreDAs",
)
