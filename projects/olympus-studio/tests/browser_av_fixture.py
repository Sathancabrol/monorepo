"""Generate a real synthetic WebM A/V in Chromium and inspect its streams.

This is a browser encoder capability test, NOT proof of Studio's EDIT export.
Requires playwright+Chromium and ffprobe on PATH. No webcam, audio device or user files.
"""
import json
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
                print("Chromium synthetic A/V verified with ffprobe:",
                      {"mime": payload["mime"], "video": video[0]["codec_name"],
                       "audio": audio[0]["codec_name"], "bytes": filename.stat().st_size})
        finally:
            browser.close()


if __name__ == "__main__":
    main()
