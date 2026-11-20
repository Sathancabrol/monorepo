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

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg not installed")
    def test_short_source_is_padded_to_exact_timeline(self):
        with tempfile.TemporaryDirectory() as d:
            src, dst = Path(d) / "short.wav", Path(d) / "timeline.wav"
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi",
                            "-i", "sine=frequency=660:duration=0.3", "-y", str(src)], check=True)
            mod.prepare_audio(src, dst, offset=.75, in_point=.1, volume=1, duration=3)
            import json
            result = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                                              "format=duration", "-of", "json", str(dst)], text=True)
            self.assertAlmostEqual(float(json.loads(result)["format"]["duration"]), 3, delta=.002)
            raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(dst),
                                           "-f", "s16le", "-ac", "1", "-ar", "48000", "-"])
            import array
            samples = array.array("h"); samples.frombytes(raw)
            self.assertEqual(max(map(abs, samples[:int(.7 * 48000)])), 0)
            self.assertGreater(max(map(abs, samples[int(.8 * 48000):int(.9 * 48000)])), 100)
            self.assertEqual(max(map(abs, samples[int(1.5 * 48000):])), 0)


    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg not installed")
    def test_prepared_audio_muxes_with_png_frames_and_opus(self):
        """Real fallback chain: PNG sequence + EDIT audio -> VP9/Opus WebM -> packet timing."""
        import importlib.util
        import json
        mux_path = MODULE.parent / "ffmpeg_mux_fallback.py"
        mux_spec = importlib.util.spec_from_file_location("ffmpeg_mux_fallback", mux_path)
        mux_module = importlib.util.module_from_spec(mux_spec)
        mux_spec.loader.exec_module(mux_module)
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            frames = root / "frames"
            frames.mkdir()
            frame = root / "frame.png"
            source = root / "source.wav"
            prepared = root / "prepared.wav"
            output = root / "render.webm"
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi",
                            "-i", "color=c=blue:s=160x90:r=24", "-frames:v", "1",
                            "-y", str(frame)], check=True, timeout=30)
            for index in range(1, 25):
                shutil.copyfile(frame, frames / f"{index:06d}.png")
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi",
                            "-i", "sine=frequency=440:duration=1", "-y", str(source)],
                           check=True, timeout=30)
            mod.prepare_audio(source, prepared, offset=.15, in_point=.05,
                              volume=.8, duration=1)
            mux_module.mux_png_sequence(frames, prepared, output, fps=24)
            streams = mux_module.probe(output)
            self.assertEqual({s.get("codec_name") for s in streams
                              if s.get("codec_type") in ("video", "audio")},
                             {"vp9", "opus"})
            report = mux_module.av_packet_report(output)
            self.assertLessEqual(abs(report["end_delta_s"]), .25, report)
            self.assertGreater(report["audio"]["packets"], 0)
            self.assertGreater(report["video"]["packets"], 0)
            self.assertTrue(source.exists())
            self.assertTrue(prepared.exists())
            self.assertEqual(len(list(frames.glob("*.png"))), 24)
            decoded = subprocess.check_output(
                ["ffmpeg", "-nostdin", "-v", "error", "-i", str(output),
                 "-map", "0:a:0", "-f", "s16le", "-ac", "1", "-ar", "48000", "-"],
                timeout=30)
            import array
            samples = array.array("h")
            samples.frombytes(decoded)
            self.assertGreater(max(map(abs, samples)), 100)

if __name__ == "__main__":
    unittest.main()
