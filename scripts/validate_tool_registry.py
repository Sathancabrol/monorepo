#!/usr/bin/env python3
"""Validate the research-only creative tool catalogue. No network or installs."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_MATURITY = {"stable", "beta", "alpha", "experimental", "unknown"}
ALLOWED_LICENSE_STATUS = {"confirmed", "declared", "unknown"}
REQUIRED = {
    "id", "name", "category", "purpose", "source_url", "license",
    "license_status", "maturity", "platforms", "integrations",
    "requirements", "install_methods", "security_notes",
    "verification_status", "last_verified", "evidence",
}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Cannot read valid JSON: {exc}"]

    if not isinstance(data, dict):
        return ["Root must be a JSON object."]
    if data.get("schema_version") != "1.0":
        errors.append("schema_version must be '1.0'.")
    tools = data.get("tools")
    if not isinstance(tools, list):
        return errors + ["tools must be a list."]

    seen: set[str] = set()
    for index, item in enumerate(tools):
        prefix = f"tools[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object.")
            continue
        missing = sorted(REQUIRED - item.keys())
        if missing:
            errors.append(f"{prefix} missing required fields: {', '.join(missing)}")
        identifier = item.get("id")
        if isinstance(identifier, str):
            if identifier in seen:
                errors.append(f"{prefix} duplicate id: {identifier}")
            seen.add(identifier)
            if not identifier or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in identifier):
                errors.append(f"{prefix} id must use lowercase letters, digits and hyphens.")
        if item.get("maturity") not in ALLOWED_MATURITY:
            errors.append(f"{prefix} has invalid maturity: {item.get('maturity')!r}")
        if item.get("license_status") not in ALLOWED_LICENSE_STATUS:
            errors.append(f"{prefix} has invalid license_status: {item.get('license_status')!r}")
        url = item.get("source_url")
        if not isinstance(url, str) or urlparse(url).scheme != "https" or not urlparse(url).netloc:
            errors.append(f"{prefix} source_url must be an HTTPS URL.")
        if not isinstance(item.get("install_methods"), list):
            errors.append(f"{prefix} install_methods must be a list.")
        if not isinstance(item.get("evidence"), list):
            errors.append(f"{prefix} evidence must be a list.")
    return errors


def main() -> int:
    default_path = Path(__file__).resolve().parents[1] / "data" / "tool_registry" / "creative-tools.json"
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_path
    errors = validate(path)
    if errors:
        print("Creative tool catalogue: INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    data = json.loads(path.read_text(encoding="utf-8"))
    print(f"Creative tool catalogue: OK ({len(data['tools'])} entries; no installs performed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
