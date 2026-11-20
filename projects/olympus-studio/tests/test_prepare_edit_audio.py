"""Regression tests for EDIT audio preparation; no Windows or GPU assumptions."""
import importlib.util
import math
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "tools" / "prepare_edit_audio.py"
spec = importlib.util.spec_from_file_location("prepare_edit_audio", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class PrepareAudioTests(unittest.TestCase):
    def test_reject_invalid_without_touching_files(self):
        with tempfile.TemporaryDirectory() as d:
            src, dst = Path(d) / "missing.wav", Path(d) / "out.wav"
            for kwargs in (
                dict(offset=math.nan, in_point=0, volume=1, duration=2),
                dict(offset=0, in_point=-1, volume=1, duration=2),
                dict(offset=0, in_point=0, volume=1.1, duration=2),
                dict(offset=0, in_point=0, volume=1, duration=0),
            ):
                with self.assertRaises(ValueError):
                    mod.prepare_audio(src, dst, **kwargs)
                self.assertFalse(dst.exists())

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg not installed")
    def test_trim_delay_gain_and_duration(self):
        with tempfile.TemporaryDirectory() as d:
            src, dst = Path(d) / "source.wav", Path(d) / "prepared.wav"
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi",
                            "-i", "sine=frequency=440:duration=2", "-y", str(src)], check=True)
            mod.prepare_audio(src, dst, offset=.5, in_point=.25, volume=.5, duration=2.5)
            self.assertTrue(dst.exists())
            import json
            info = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                                            "format=duration", "-of", "json", str(dst)], text=True)
            self.assertAlmostEqual(float(json.loads(info)["format"]["duration"]), 2.5, delta=.03)
            # First 400 ms must be digital silence; subsequent source must be audible.
            raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(dst),
                                           "-f", "s16le", "-ac", "1", "-ar", "48000", "-"])
            import array
            samples = array.array("h")
            samples.frombytes(raw)
            self.assertEqual(max(map(abs, samples[:int(.4*48000)])), 0)
            self.assertGreater(max(map(abs, samples[int(.7*48000):int(.9*48000)])), 100)
            with self.assertRaises(ValueError):
                mod.prepare_audio(src, dst, offset=0, in_point=0, volume=1, duration=2)


if __name__ == "__main__":
    unittest.main()
