import importlib.util
import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "project_audit" / "audit_gaps.py"
SPEC = importlib.util.spec_from_file_location("audit_gaps", SCRIPT)
audit_gaps = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_gaps)


class AuditGapScannerTests(unittest.TestCase):
    def test_all_pages_continues_until_short_page(self):
        first_page = [{"name": f"branch-{i}"} for i in range(100)]
        second_page = [{"name": "branch-100"}]

        def fake_get_json(url):
            page = parse_qs(urlparse(url).query).get("page")
            if page == ["1"]:
                return first_page, None
            if page == ["2"]:
                return second_page, None
            self.fail(f"Unexpected pagination URL: {url}")

        with patch.object(audit_gaps, "get_json", side_effect=fake_get_json) as mocked:
            rows, errors = audit_gaps.all_pages("https://api.github.com/repos/example/repo/branches")

        self.assertEqual(len(rows), 101)
        self.assertEqual(errors, [])
        self.assertEqual(mocked.call_count, 2)

    def test_all_pages_preserves_api_error(self):
        with patch.object(audit_gaps, "get_json", return_value=(None, "HTTP 403")):
            rows, errors = audit_gaps.all_pages("https://api.github.com/repos/example/repo/branches")

        self.assertEqual(rows, [])
        self.assertEqual(errors, ["HTTP 403"])

    def test_load_returns_default_for_invalid_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text("{invalid", encoding="utf-8")
            result = audit_gaps.load(path, {"fallback": True})

        self.assertEqual(result, {"fallback": True})

    def test_metadata_error_preserves_prior_records(self):
        old = {
            "example/repo@main": {
                "repo": "example/repo",
                "branch": "main",
                "sha": "abc123",
                "status": "tree_inspected",
            }
        }
        current = {}

        audit_gaps.preserve_prior_records(old, current, "example/repo", "metadata_error", "HTTP 503")

        self.assertEqual(current["example/repo@main"]["sha"], "abc123")
        self.assertEqual(current["example/repo@main"]["status"], "metadata_error")
        self.assertEqual(current["example/repo@main"]["audit_error"], "HTTP 503")

    def test_branch_list_error_is_not_reported_as_missing(self):
        old = {
            "example/repo@main": {
                "repo": "example/repo",
                "branch": "main",
                "sha": "abc123",
                "status": "tree_inspected",
            }
        }
        current = {}

        audit_gaps.reconcile_unseen_records(old, current, "example/repo", set(), ["HTTP 503"])

        self.assertEqual(current["example/repo@main"]["status"], "branch_list_error")
        self.assertNotEqual(current["example/repo@main"]["status"], "not_listed_now")


if __name__ == "__main__":
    unittest.main()
