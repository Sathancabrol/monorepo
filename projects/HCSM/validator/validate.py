#!/usr/bin/env python3
"""Entry point: python validate.py [--all] [files...]"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running without install
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hcsm_validate.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
