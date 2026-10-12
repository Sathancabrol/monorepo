import importlib.util
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "project_audit" / "audit_portfolio.py"
SPEC = importlib.util.spec_from_file_location("audit_portfolio", SCRIPT)
audit_portfolio = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_portfolio)


class PortfolioAuditTests(unittest.TestCase):
    def test_request_pages_collects_every_page(self):
        first_page = [{"name": f"branch-{index}"} for index in range(100)]
        second_page = [{"name": "branch-100"}]

        def fake_request(url):
            page = parse_qs(urlparse(url).query).get("page")
            if page == ["1"]:
                return first_page, None
            if page == ["2"]:
                return second_page, None
            self.fail(f"Unexpected pagination URL: {url}")

        with patch.object(audit_portfolio, "request_json", side_effect=fake_request) as mocked:
            rows, error = audit_portfolio.request_pages("https://api.github.com/repos/example/repo/branches")

        self.assertEqual(len(rows), 101)
        self.assertIsNone(error)
        self.assertEqual(mocked.call_count, 2)

    def test_request_pages_preserves_partial_results_and_error(self):
        first_page = [{"name": f"branch-{index}"} for index in range(100)]

        def fake_request(url):
            page = parse_qs(urlparse(url).query).get("page")
            if page == ["1"]:
                return first_page, None
            return None, "HTTP 503"

        with patch.object(audit_portfolio, "request_json", side_effect=fake_request):
            rows, error = audit_portfolio.request_pages("https://api.github.com/repos/example/repo/branches")

        self.assertEqual(rows, first_page)
        self.assertEqual(error, "HTTP 503")


if __name__ == "__main__":
    unittest.main()
