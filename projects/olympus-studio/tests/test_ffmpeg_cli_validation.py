"""CLI regression: rejected A/V exports must never announce success."""
import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("olympus_mux", ROOT / "tools" / "ffmpeg_mux_fallback.py")
mux = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mux)


class ValidationOutputTests(unittest.TestCase):
    def run_cli(self, report):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "result.webm"
            def fake_mux(*args):
                output.write_bytes(b"synthetic candidate")
                return output
            stdout = io.StringIO()
            argv = ["mux", "--frames-dir", temp, "--audio", "audio.wav",
                    "--output", str(output), "--max-end-delta", "0.2", "--av-report"]
            with patch.object(sys, "argv", argv), patch.object(mux, "mux_png_sequence", side_effect=fake_mux), \
                 patch.object(mux, "av_packet_report", **({"side_effect": report} if isinstance(report, Exception) else {"return_value": report})), contextlib.redirect_stdout(stdout):
                if isinstance(report, Exception) or report["end_delta_s"] > 0.2:
                    with self.assertRaises((RuntimeError, ValueError)):
                        mux.main()
                    self.assertFalse(output.exists())
                    self.assertEqual(stdout.getvalue(), "")
                else:
                    mux.main()
                    self.assertTrue(output.exists())
                    self.assertIn(str(output), stdout.getvalue())
                    self.assertIn("end_delta_s", stdout.getvalue())

    def test_excessive_desync_does_not_print_success(self):
        self.run_cli({"end_delta_s": 0.759})

    def test_probe_failure_removes_candidate(self):
        self.run_cli(ValueError("missing audio packets"))

    def test_valid_report_prints_success(self):
        self.run_cli({"end_delta_s": 0.01})


if __name__ == "__main__":
    unittest.main()
