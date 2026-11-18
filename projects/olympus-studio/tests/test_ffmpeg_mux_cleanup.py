"""Regression tests: failed mux must not leave an apparently usable WebM."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "ffmpeg_mux_fallback.py"
spec = importlib.util.spec_from_file_location("olympus_mux", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class MuxFailureTests(unittest.TestCase):
    def test_ffmpeg_failure_cleans_partial_output_and_preserves_inputs(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            video, audio, output = (root / name for name in ("video.webm", "audio.wav", "result.webm"))
            video.write_bytes(b"video original")
            audio.write_bytes(b"audio original")

            def fake_run(command, **kwargs):
                output.write_bytes(b"truncated webm")
                raise subprocess.CalledProcessError(1, command)

            with patch.object(module.shutil, "which", return_value="/usr/bin/ffmpeg"), \
                 patch.object(module, "probe", side_effect=[
                     [{"codec_type": "video"}], [{"codec_type": "audio"}]
                 ]), \
                 patch.object(module.subprocess, "run", side_effect=fake_run):
                with self.assertRaises(subprocess.CalledProcessError):
                    module.mux(video, audio, output)

            self.assertFalse(output.exists())
            self.assertEqual(video.read_bytes(), b"video original")
            self.assertEqual(audio.read_bytes(), b"audio original")

    def test_invalid_output_streams_are_removed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            video, audio, output = (root / name for name in ("video.webm", "audio.wav", "result.webm"))
            video.touch()
            audio.touch()

            def fake_run(command, **kwargs):
                output.write_bytes(b"video only")
                return None

            with patch.object(module.shutil, "which", return_value="/usr/bin/ffmpeg"), \
                 patch.object(module, "probe", side_effect=[
                     [{"codec_type": "video"}], [{"codec_type": "audio"}], [{"codec_type": "video"}]
                 ]), \
                 patch.object(module.subprocess, "run", side_effect=fake_run):
                with self.assertRaisesRegex(RuntimeError, "lacks video or audio"):
                    module.mux(video, audio, output)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
