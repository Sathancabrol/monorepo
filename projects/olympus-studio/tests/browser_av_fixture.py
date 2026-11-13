"""Generate a real synthetic WebM A/V in Chromium and inspect its streams.

This is a browser encoder capability test, NOT proof of Studio's EDIT export.
Requires playwright+Chromium and ffprobe on PATH. No webcam, audio device or user files.
"""
import json
import re
from pathlib import Path
import shutil
import subprocess
import tempfile

from playwright.sync_api import sync_playwright


def main():
    probe = shutil.which("ffprobe")
    if not probe:
        raise RuntimeError("ffprobe required for A/V codec verification")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--autoplay-policy=no-user-gesture-required"])
        try:
            page = browser.new_page()
            # Web Audio oscillator -> MediaStreamDestination, Canvas -> captureStream.
            # Use AudioContext clock as source; generated samples are not user audio.
            payload = page.evaluate("""async () => {
              const canvas=document.createElement('canvas');
              canvas.width=160;canvas.height=90;
              const ctx=canvas.getContext('2d');
              const ac=new AudioContext();
              const oscillator=ac.createOscillator();
              oscillator.frequency.value=440;
              const gain=ac.createGain();
              gain.gain.value=0.15;
              const destination=ac.createMediaStreamDestination();
              oscillator.connect(gain).connect(destination);
              const visual=canvas.captureStream(15);
              const stream=new MediaStream([...visual.getVideoTracks(), ...destination.stream.getAudioTracks()]);
              const candidates=['video/webm;codecs=vp8,opus','video/webm;codecs=vp9,opus'];
              const mime=candidates.find(x=>MediaRecorder.isTypeSupported(x));
              if(!mime) throw Error('Chromium lacks WebM Opus encoder');
              const recorder=new MediaRecorder(stream,{mimeType:mime});
              const chunks=[];
              recorder.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
              const stopped=new Promise((resolve,reject)=>{
                recorder.onerror=e=>reject(Error('MediaRecorder error '+e.error?.message));
                recorder.onstop=resolve;
              });
              oscillator.start();
              recorder.start(100);
              const start=performance.now();
              await new Promise(resolve=>{
                const draw=()=>{
                  const elapsed=performance.now()-start;
                  ctx.fillStyle=elapsed<500?'#fff':'#222';
                  ctx.fillRect(0,0,160,90);
                  if(elapsed<1250)requestAnimationFrame(draw);
                  else resolve();
                };
                draw();
              });
              recorder.stop();
              await stopped;
              oscillator.stop();
              stream.getTracks().forEach(t=>t.stop());
              await ac.close();
              const blob=new Blob(chunks,{type:mime});
              if(blob.size<1000)throw Error('A/V fixture unexpectedly empty');
              const bytes=new Uint8Array(await blob.arrayBuffer());
              // Returning a plain numeric array avoids filesystem access from the browser.
              return {mime,bytes:Array.from(bytes)};
            }""")
            with tempfile.TemporaryDirectory(prefix="olympus-av-") as tmp:
                filename = Path(tmp) / "synthetic-av.webm"
                filename.write_bytes(bytes(payload["bytes"]))
                result = subprocess.run(
                    [probe, "-v", "error", "-show_streams", "-of", "json", str(filename)],
                    capture_output=True, text=True, check=True, timeout=15,
                )
                streams = json.loads(result.stdout)["streams"]
                video = [s for s in streams if s.get("codec_type") == "video"]
                audio = [s for s in streams if s.get("codec_type") == "audio"]
                assert video and video[0]["codec_name"] in ("vp8", "vp9"), streams
                assert audio and audio[0]["codec_name"] == "opus", streams
                assert filename.stat().st_size > 1000
                # Check actual encoded packets, not only codec declarations. These
                # tolerances account for Chromium's variable first video-frame time.
                packets = subprocess.run(
                    [probe, "-v", "error", "-show_packets",
                     "-show_entries", "packet=stream_index,pts_time,duration_time",
                     "-of", "json", str(filename)],
                    capture_output=True, text=True, check=True, timeout=15,
                )
                packet_rows = json.loads(packets.stdout)["packets"]
                def bounds(index):
                    items = [
                        (float(p["pts_time"]), float(p.get("duration_time", 0)))
                        for p in packet_rows
                        if p.get("stream_index") == index and "pts_time" in p
                    ]
                    assert len(items) >= 2, f"Not enough packets for stream {index}"
                    return min(t for t, _ in items), max(t + d for t, d in items)
                vstart, vend = bounds(video[0]["index"])
                astart, aend = bounds(audio[0]["index"])
                assert 0.7 < vend - vstart < 2.5, ("video duration", vstart, vend)
                assert 0.7 < aend - astart < 2.5, ("audio duration", astart, aend)
                assert abs(vstart - astart) < 0.5, ("A/V start offset", vstart, astart)
                assert abs(vend - aend) < 0.5, ("A/V end offset", vend, aend)

                # An Opus stream can be entirely silent. Decode it and assert
                # nonzero sound energy; this is not a human listening test.
                ffmpeg = shutil.which("ffmpeg")
                if not ffmpeg:
                    raise RuntimeError("ffmpeg required for decoded-audio verification")
                volume = subprocess.run(
                    [ffmpeg, "-hide_banner", "-nostats", "-i", str(filename),
                     "-map", "0:a:0", "-af", "volumedetect", "-f", "null", "-"],
                    capture_output=True, text=True, check=True, timeout=20,
                )
                match = re.search(r"mean_volume:\s*(-?[\d.]+) dB", volume.stderr)
                assert match, "Decoded audio has no measurable volume"
                mean_db = float(match.group(1))
                assert -55 < mean_db < -3, ("Silent or clipped synthetic tone", mean_db)
                print("Chromium synthetic A/V verified with ffprobe + decoded audio:",
                      {"mime": payload["mime"], "video": video[0]["codec_name"],
                       "audio": audio[0]["codec_name"], "bytes": filename.stat().st_size,
                       "start_offset_s": round(vstart - astart, 3),
                       "end_offset_s": round(vend - aend, 3),
                       "audio_mean_db": mean_db})
        finally:
            browser.close()


if __name__ == "__main__":
    main()
