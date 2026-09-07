class CosmicSynthesizer {
  private ctx: AudioContext | null = null;
  private isRunning: boolean = false;
  private masterGain: GainNode | null = null;
  private subOsc: OscillatorNode | null = null;
  private subGain: GainNode | null = null;
  private coreOsc: OscillatorNode | null = null;
  private coreGain: GainNode | null = null;
  private noiseNode: AudioBufferSourceNode | null = null;
  private noiseGain: GainNode | null = null;

  public init() {
    if (this.ctx) return;
    const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    this.ctx = new AudioCtx();

    // Master gain
    this.masterGain = this.ctx.createGain();
    this.masterGain.gain.setValueAtTime(0, this.ctx.currentTime);
    this.masterGain.connect(this.ctx.destination);

    // 1. Deep Sub-Bass Event Horizon Resonance (38Hz with subtle slow vibrato)
    this.subOsc = this.ctx.createOscillator();
    this.subOsc.type = 'sine';
    this.subOsc.frequency.setValueAtTime(41.2, this.ctx.currentTime); // E1 note

    this.subGain = this.ctx.createGain();
    this.subGain.gain.setValueAtTime(0.3, this.ctx.currentTime);
    this.subOsc.connect(this.subGain);
    this.subGain.connect(this.masterGain);

    // Subtle LFO on sub oscillator
    const lfo = this.ctx.createOscillator();
    const lfoGain = this.ctx.createGain();
    lfo.frequency.setValueAtTime(0.08, this.ctx.currentTime); // 12.5s cycle
    lfoGain.gain.setValueAtTime(1.5, this.ctx.currentTime);
    lfo.connect(lfoGain);
    lfoGain.connect(this.subOsc.frequency);
    lfo.start();

    // 2. Cosmic Background Shimmer (soft pink noise filtered)
    const bufferSize = this.ctx.sampleRate * 2;
    const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    let b0 = 0, b1 = 0, b2 = 0;
    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      b0 = 0.99886 * b0 + white * 0.0555179;
      b1 = 0.99332 * b1 + white * 0.0750759;
      b2 = 0.96900 * b2 + white * 0.1538520;
      output[i] = (b0 + b1 + b2) * 0.04;
    }
    this.noiseNode = this.ctx.createBufferSource();
    this.noiseNode.buffer = noiseBuffer;
    this.noiseNode.loop = true;

    const noiseFilter = this.ctx.createBiquadFilter();
    noiseFilter.type = 'lowpass';
    noiseFilter.frequency.setValueAtTime(260, this.ctx.currentTime);

    this.noiseGain = this.ctx.createGain();
    this.noiseGain.gain.setValueAtTime(0.08, this.ctx.currentTime);

    this.noiseNode.connect(noiseFilter);
    noiseFilter.connect(this.noiseGain);
    this.noiseGain.connect(this.masterGain);

    // 3. Solitary Consciousness Core Harmonic (quiet high bell-like sine)
    this.coreOsc = this.ctx.createOscillator();
    this.coreOsc.type = 'sine';
    this.coreOsc.frequency.setValueAtTime(432, this.ctx.currentTime);

    this.coreGain = this.ctx.createGain();
    this.coreGain.gain.setValueAtTime(0.02, this.ctx.currentTime);
    this.coreOsc.connect(this.coreGain);
    this.coreGain.connect(this.masterGain);

    // Start sources
    this.subOsc.start();
    this.noiseNode.start();
    this.coreOsc.start();
  }

  public playAwakeningChime() {
    if (!this.ctx) {
      this.init();
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
    if (!this.ctx) return;

    const now = this.ctx.currentTime;
    // Harmonic celestial chords (cosmic resonance: E2, B2, E3, G#3, B3, D#4)
    const freqs = [82.4, 164.81, 246.94, 329.63, 415.3, 493.88, 622.25];
    freqs.forEach((freq, idx) => {
      const osc = this.ctx!.createOscillator();
      const gain = this.ctx!.createGain();
      osc.type = idx % 2 === 0 ? 'sine' : 'triangle';
      osc.frequency.setValueAtTime(freq, now);

      gain.gain.setValueAtTime(0.0001, now);
      gain.gain.linearRampToValueAtTime(0.07 / (idx * 0.6 + 1), now + 0.12 + idx * 0.04);
      gain.gain.exponentialRampToValueAtTime(0.00001, now + 3.8 + idx * 0.3);

      osc.connect(gain);
      gain.connect(this.ctx!.destination);
      osc.start(now);
      osc.stop(now + 4.5);
    });
  }

  public toggle(): boolean {
    if (!this.ctx) {
      this.init();
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }

    if (!this.masterGain || !this.ctx) return false;

    if (this.isRunning) {
      this.masterGain.gain.linearRampToValueAtTime(0, this.ctx.currentTime + 1.2);
      this.isRunning = false;
    } else {
      this.masterGain.gain.linearRampToValueAtTime(0.35, this.ctx.currentTime + 1.5);
      this.isRunning = true;
    }
    return this.isRunning;
  }

  public getActive(): boolean {
    return this.isRunning;
  }
}

export const cosmicAudio = new CosmicSynthesizer();

export function speakChronosSpeech(
  text: string,
  onStart?: () => void,
  onEnd?: () => void,
  playChime: boolean = true
): void {
  if (playChime) {
    cosmicAudio.playAwakeningChime();
  }

  if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
    try {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'fr-FR';
      // Voix: neutre, simple, calme, méthodique, scientifique
      utterance.rate = 0.88;
      utterance.pitch = 0.92;

      const setVoiceAndSpeak = () => {
        const voices = window.speechSynthesis.getVoices();
        // Look for clean neutral French voice
        const frVoice =
          voices.find((v) => v.lang === 'fr-FR' && !v.name.includes('Google') && !v.name.includes('Natural')) ||
          voices.find((v) => v.lang === 'fr-FR') ||
          voices.find((v) => v.lang.startsWith('fr'));
        if (frVoice) {
          utterance.voice = frVoice;
        }

        utterance.onstart = () => {
          onStart?.();
        };
        utterance.onend = () => {
          onEnd?.();
        };
        utterance.onerror = () => {
          onEnd?.();
        };

        window.speechSynthesis.speak(utterance);
      };

      if (window.speechSynthesis.getVoices().length > 0) {
        setTimeout(setVoiceAndSpeak, playChime ? 350 : 80);
      } else {
        window.speechSynthesis.onvoiceschanged = () => {
          setTimeout(setVoiceAndSpeak, playChime ? 350 : 80);
        };
        // Fallback if event doesn't fire
        setTimeout(setVoiceAndSpeak, playChime ? 450 : 150);
      }
    } catch {
      onEnd?.();
    }
  } else {
    onStart?.();
    setTimeout(() => onEnd?.(), 3000);
  }
}

export function speakChronosGreeting(onStart?: () => void, onEnd?: () => void): void {
  speakChronosSpeech('Bonjour, qui êtes-vous ?', onStart, onEnd, true);
}
