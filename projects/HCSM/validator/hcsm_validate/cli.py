"""Command-line interface for the HCSM validator."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .admissibility import assess_admissibility, assess_bundle_requests
from .ontology import Ontology
from .schema import ValidationResult, validate_bundle, validate_object

CASES_DIR = Path(__file__).resolve().parents[1] / "cases"


def _load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _is_bundle(data: Any) -> bool:
    return isinstance(data, dict) and (
        data.get("type") in {"Bundle", "hcsm_bundle"}
        or isinstance(data.get("objects"), list)
    )


def _validate_data(data: Any, onto: Ontology) -> ValidationResult:
    if isinstance(data, list):
        return validate_bundle({"type": "Bundle", "objects": data}, onto)
    if _is_bundle(data):
        return validate_bundle(data, onto)
    if isinstance(data, dict):
        return validate_object(data, onto)
    r = ValidationResult(ok=False)
    r.add("V1-TYPE", "Root JSON must be an object or array.")
    return r


def _expected_from_meta(data: Any, path: Path) -> str | None:
    """Return expected outcome: pass | fail | admit | refuse."""
    if isinstance(data, dict):
        meta = data.get("_meta") or data.get("meta") or {}
        if isinstance(meta, dict) and meta.get("expect"):
            return str(meta["expect"]).lower()
    # path heuristic
    parts = {p.lower() for p in path.parts}
    name = path.name.lower()
    if "invalid" in parts or name.startswith("bad_") or name.startswith("invalid_"):
        return "fail"
    if "refuse" in name or name.startswith("refusal_"):
        return "refuse"
    if "valid" in parts:
        return "pass"
    return None


def _run_one(
    path: Path,
    onto: Ontology,
    *,
    admit_only: bool = False,
    quiet: bool = False,
) -> bool:
    data = _load_json(path)
    expect = _expected_from_meta(data, path)

    # strip meta before validation
    if isinstance(data, dict) and "_meta" in data:
        data = {k: v for k, v in data.items() if k != "_meta"}

    if admit_only or expect in {"admit", "refuse"}:
        if _is_bundle(data):
            results = assess_bundle_requests(data, onto)
            if not results:
                # single request at root
                results = [assess_admissibility(data, onto, bundle=data)]
        else:
            results = [assess_admissibility(data, onto, bundle=data)]

        all_adm = all(r.admissible for r in results)
        any_refuse = any(not r.admissible for r in results)

        if expect == "admit":
            success = all_adm
        elif expect == "refuse":
            success = any_refuse and not all_adm if len(results) == 1 else any_refuse
            if len(results) == 1:
                success = not results[0].admissible
            else:
                # for multi, expect at least one refusal if marked refuse
                success = any_refuse
        else:
            success = True  # report only

        if not quiet:
            status = "PASS" if success else "FAIL"
            print(f"[{status}] {path}")
            for r in results:
                flag = "ADMIT" if r.admissible else f"REFUSE:{r.refusal_code}"
                print(f"  {flag} construct={r.construct_id} — {r.message}")
                for c in r.checks:
                    mark = "✓" if c["pass"] else "✗"
                    print(f"    {mark} {c['check']}: {c.get('detail', '')}")
        return success

    result = _validate_data(data, onto)

    if expect == "fail":
        success = not result.ok
    elif expect == "pass":
        success = result.ok
    else:
        success = result.ok

    if not quiet:
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {path}")
        if result.ok:
            print(f"  OK type={result.object_type} id={result.object_id}")
        else:
            for iss in result.issues:
                print(f"  {iss}")
        # if pass and bundle has CE, also show admissibility
        if result.ok and _is_bundle(data):
            for ar in assess_bundle_requests(data, onto):
                flag = "ADMIT" if ar.admissible else f"REFUSE:{ar.refusal_code}"
                print(f"  admissibility: {flag} ({ar.construct_id})")
    return success


def _iter_case_files() -> list[Path]:
    files: list[Path] = []
    if not CASES_DIR.is_dir():
        return files
    for sub in sorted(CASES_DIR.rglob("*.json")):
        files.append(sub)
    return files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="hcsm-validate",
        description="HCSM V1 form validator + V5 admissibility filter. Does not estimate state.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="JSON file(s) to validate",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help=f"Run all cases under {CASES_DIR}",
    )
    parser.add_argument(
        "--admit",
        action="store_true",
        help="Run admissibility (V5) only",
    )
    parser.add_argument(
        "--ontology",
        type=Path,
        default=None,
        help="Path to hcsm-v0.1.yaml (default: repo ontology/)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Exit code only",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"hcsm-validate {__version__}",
    )
    args = parser.parse_args(argv)

    try:
        onto = Ontology(args.ontology) if args.ontology else Ontology()
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    paths: list[Path] = []
    if args.all:
        paths = _iter_case_files()
        if not paths:
            print("error: no cases found", file=sys.stderr)
            return 2
    else:
        paths = list(args.paths)

    if not paths:
        parser.print_help()
        return 2

    ok_count = 0
    fail_count = 0
    for path in paths:
        if not path.is_file():
            print(f"[FAIL] {path} (not found)")
            fail_count += 1
            continue
        # per-file expect drives admit vs form
        data_peek = _load_json(path)
        expect = _expected_from_meta(data_peek, path)
        admit_mode = args.admit or expect in {"admit", "refuse"}
        # for --all, valid form cases use form; invalid use form; refuse/admit use V5
        if args.all and expect in {"pass", "fail"}:
            admit_mode = False
        if args.all and expect in {"admit", "refuse"}:
            admit_mode = True

        success = _run_one(path, onto, admit_only=admit_mode, quiet=args.quiet)
        if success:
            ok_count += 1
        else:
            fail_count += 1

    if not args.quiet:
        print(f"\n{ok_count}/{ok_count + fail_count} passed")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
