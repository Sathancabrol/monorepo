import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_tool_registry import validate


class ToolRegistryValidationTests(unittest.TestCase):
    def setUp(self):
        self.valid_entry = {
            "id": "example-tool",
            "name": "Example",
            "category": "editor",
            "purpose": "Test fixture",
            "source_url": "https://example.org/project",
            "license": "MIT",
            "license_status": "declared",
            "maturity": "experimental",
            "platforms": ["windows"],
            "integrations": [],
            "requirements": {},
            "install_methods": [],
            "security_notes": "Test only",
            "verification_status": "not_tested_locally",
            "last_verified": "2026-10-09",
            "evidence": [],
        }

    def validate_data(self, data):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalogue.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            return validate(path)

    def test_valid_catalogue_passes(self):
        self.assertEqual(
            self.validate_data({"schema_version": "1.0", "tools": [self.valid_entry]}),
            [],
        )

    def test_duplicate_ids_are_rejected(self):
        errors = self.validate_data({
            "schema_version": "1.0",
            "tools": [self.valid_entry, dict(self.valid_entry)],
        })
        self.assertTrue(any("duplicate id" in error for error in errors))

    def test_unknown_maturity_is_rejected(self):
        entry = dict(self.valid_entry, maturity="super-stable")
        errors = self.validate_data({"schema_version": "1.0", "tools": [entry]})
        self.assertTrue(any("invalid maturity" in error for error in errors))

    def test_non_https_source_is_rejected(self):
        entry = dict(self.valid_entry, source_url="http://example.org/project")
        errors = self.validate_data({"schema_version": "1.0", "tools": [entry]})
        self.assertTrue(any("HTTPS" in error for error in errors))

    def test_missing_fields_are_reported(self):
        errors = self.validate_data({"schema_version": "1.0", "tools": [{"id": "minimal"}]})
        self.assertTrue(any("missing required fields" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
