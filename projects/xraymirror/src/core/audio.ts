import { EventBus } from './eventBus';
import { clamp01 } from './filters';

export interface AudioBand {
  rms: number;
  peak: number;
  db: number;
}

export interface TransientDetector {
  isTransient: boolean;
  confidence: number;
  kind: 'claquement' | 'bruit' | 'silence';
}

/**
 * Lightweight acoustic transient detector used before (or without) a learned
 * audio classifier. It detects short broadband attacks, not speech content and
 * never uploads audio.
 */
export class AudioAnalyser {
  private context: AudioContext | null = null;
  private stream: MediaStream | null = null;
  private analyser: AnalyserNode | null = null;
  private source: MediaStreamAudioSourceNode | null = null;
  private buffer = new Float32Array(1024);
  private history: number[] = [];
  private cooldownUntil = 0;
  private silentSince = 0;

  constructor(private readonly bus: EventBus) {}

  get activeAudioContext(): AudioContext | null {
    return this.context;
  }

  async start(stream: MediaStream): Promise<void> {
    this.stop();
    const AudioCtor = window.AudioContext ?? (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    this.context = new AudioCtor();
    await this.context.resume();
    this.source = this.context.createMediaStreamSource(stream);
    this.analyser = this.context.createAnalyser();
    this.analyser.fftSize = 2048;
    this.analyser.smoothingTimeConstant = 0.65;
    this.source.connect(this.analyser);
    this.buffer = new Float32Array(this.analyser.fftSize);
  }

  stop(): void {
    this.source?.disconnect();
    this.analyser?.disconnect();
    void this.context?.close();
    this.context = null;
    this.source = null;
    this.analyser = null;
    this.history = [];
  }

  sample(now = performance.now()): AudioBand {
    if (!this.analyser) return { rms: 0, peak: 0, db: -96 };
    this.analyser.getFloatTimeDomainData(this.buffer);
    let sum = 0;
    let peak = 0;
    for (const sample of this.buffer) {
      sum += sample * sample;
      peak = Math.max(peak, Math.abs(sample));
    }
    const rms = Math.sqrt(sum / this.buffer.length);
    const db = rms > 1e-6 ? 20 * Math.log10(rms) : -96;

    this.history.push(rms);
    if (this.history.length > 32) this.history.shift();

    const transient = this.detectTransient(rms, now);
    if (transient.isTransient) {
      this.bus.emit({
        type: 'sound.detected',
        source: 'audio.transient',
        label: transient.kind,
        confidence: transient.confidence,
        timestamp: now,
        attributes: { rms, db },
      });
    }
    return { rms, peak, db };
  }

  private detectTransient(rms: number, now: number): TransientDetector {
    const recent = this.history.slice(-12, -2);
    const baseline = recent.length
      ? recent.reduce((sum, value) => sum + value, 0) / recent.length
      : 0;
    const ratio = baseline > 0.002 ? rms / baseline : 0;
    const loud = rms > Math.max(0.035, baseline * 2.3);
    const isTransient = loud && ratio > 1.9 && now > this.cooldownUntil;

    if (rms < 0.006) {
      this.silentSince += 1;
    } else {
      this.silentSince = 0;
    }

    if (isTransient) {
      this.cooldownUntil = now + 450;
      return {
        isTransient: true,
        confidence: clamp01(0.45 + Math.min(0.45, (ratio - 1.9) / 10)),
        kind: 'claquement',
      };
    }
    return { isTransient: false, confidence: 0, kind: this.silentSince > 8 ? 'silence' : 'bruit' };
  }
}

/** Short WebAudio synth used to confirm a detected clap without any asset. */
export async function playConfirmationTone(frequency = 660, durationMs = 70): Promise<void> {
  const AudioCtor = window.AudioContext ?? (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
  const context = new AudioCtor();
  await context.resume();
  const oscillator = context.createOscillator();
  const gain = context.createGain();
  oscillator.type = 'sine';
  oscillator.frequency.value = frequency;
  gain.gain.setValueAtTime(0.0001, context.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.15, context.currentTime + 0.01);
  gain.gain.exponentialRampToValueAtTime(0.0001, context.currentTime + durationMs / 1000);
  oscillator.connect(gain).connect(context.destination);
  oscillator.start();
  oscillator.stop(context.currentTime + durationMs / 1000 + 0.02);
  oscillator.onended = () => void context.close();
}
