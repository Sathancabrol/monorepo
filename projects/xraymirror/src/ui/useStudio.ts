import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { buildSkeletalAnchors, isBoneVisible, type AnatomyLayer } from '../core/anatomy';
import { AudioAnalyser } from '../core/audio';
import { EventBus } from '../core/eventBus';
import { MediaPipeEngine, type EngineKind } from '../core/mediapipe';
import { PerceptionLoop, emptySnapshot, type PerceptionSnapshot } from '../core/perception';
import { PaintModel } from '../core/paint';
import { RuleEngine } from '../core/rules';
import { DEFAULT_RULES } from '../core/rules';
import type { DetectorSettings, RuleDefinition, StudioEvent } from '../core/types';
import { loadSettings, saveSettings, type StoredSettings } from '../core/clientStore';
import { clampBox, expandBox, faceBoxFromPoints } from './capture';

export type PermissionState = 'idle' | 'requesting' | 'granted' | 'denied' | 'unavailable';

export interface Toast {
  id: number;
  tone: 'info' | 'warn' | 'error' | 'ok';
  message: string;
}

const DEFAULT_SETTINGS: StoredSettings = {
  detectors: { face: true, hands: true, pose: true, objects: true, audio: true, gestures: false },
  rules: DEFAULT_RULES,
  modelCache: { mode: 'auto', note: 'Cache local prioritaire' },
  anatomy: {
    opacity: 0.72,
    lens: false,
    labels: true,
    layers: { skeleton: true, muscles: false, organs: true, nervous: false, vessels: false, labels: true },
  },
  paint: { clearWithFist: false },
  privacy: { storeRawMedia: false, anonymizeExports: false },
};

export interface StudioState {
  camera: PermissionState;
  microphone: PermissionState;
  running: boolean;
  error: string | null;
  events: StudioEvent[];
  snapshot: PerceptionSnapshot;
  settings: StoredSettings;
  timings: Record<string, number>;
  latency: Record<string, { p50: number; p95: number; samples: number }>;
  engineStatus: Record<string, string>;
  fps: number;
  inferenceMs: number;
  toasts: Toast[];
  audioLevels: number[];
}

export function useStudio() {
  const [settings, setSettings] = useState<StoredSettings>(() => loadSettings(DEFAULT_SETTINGS));
  const [camera, setCamera] = useState<PermissionState>('idle');
  const [microphone, setMicrophone] = useState<PermissionState>('idle');
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [snapshot, setSnapshot] = useState<PerceptionSnapshot>(emptySnapshot());
  const [events, setEvents] = useState<StudioEvent[]>([]);
  const [timings, setTimings] = useState<Record<string, number>>({});
  const [latency, setLatency] = useState<Record<string, { p50: number; p95: number; samples: number }>>({});
  const [engineStatus, setEngineStatus] = useState<Record<string, string>>({});
  const [fps, setFps] = useState(0);
  const [toasts, setToasts] = useState<Toast[]>([]);

  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const audioStreamRef = useRef<MediaStream | null>(null);
  const engineRef = useRef<MediaPipeEngine | null>(null);
  const loopRef = useRef<PerceptionLoop | null>(null);
  const busRef = useRef<EventBus | null>(null);
  const audioRef = useRef<AudioAnalyser | null>(null);
  const paintRef = useRef<PaintModel>(new PaintModel());
  const rulesRef = useRef<RuleEngine | null>(null);
  const settingsRef = useRef(settings);
  const frameCount = useRef(0);
  const fpsWindowStart = useRef(performance.now());
  const audioBars = useRef<number[]>([]);
  const [audioLevels, setAudioLevels] = useState<number[]>(new Array(20).fill(0));
  const pinchRef = useRef(false);
  const fistFrames = useRef(0);
  const latestSnapshotRef = useRef<PerceptionSnapshot>(emptySnapshot());
  const lastPoseSeen = useRef(0);
  const lastFaceSeen = useRef(0);
  const lastSnapshotUi = useRef(0);
  const lastEventsUi = useRef(0);
  const startLock = useRef(false);
  const lastAudioUi = useRef(0);

  settingsRef.current = settings;

  const pushToast = useCallback((message: string, tone: Toast['tone'] = 'info') => {
    const id = Date.now() + Math.random();
    setToasts((previous) => [...previous.slice(-3), { id, tone, message }]);
    window.setTimeout(() => {
      setToasts((previous) => previous.filter((toast) => toast.id !== id));
    }, 4200);
  }, []);

  useEffect(() => {
    saveSettings(settings);
  }, [settings]);

  const bus = useMemo(() => {
    if (!busRef.current) busRef.current = new EventBus(3000);
    return busRef.current;
  }, []);

  useEffect(() => {
    const unsubscribe = bus.subscribe((event) => {
      rulesRef.current?.evaluate(event);
      if (
        event.type === 'face.detected' ||
        event.type === 'hand.gesture' ||
        event.type === 'object.detected' ||
        event.type === 'sound.detected' ||
        event.type === 'pose.detected' ||
        event.type === 'rule.fired'
      ) {
        // Batch UI updates: the bus stays live at full rate, React sees ~4 Hz.
        const now = performance.now();
        if (now - lastEventsUi.current > 250) {
          lastEventsUi.current = now;
          setEvents(bus.recent(120));
        }
      }
    });
    return unsubscribe;
  }, [bus]);

  useEffect(() => {
    rulesRef.current = new RuleEngine(
      settings.rules,
      (rule) => {
        if (rule.action.type === 'toggle-layer') {
          setSettings((current) => {
            const layers = { ...current.anatomy.layers };
            for (const key of Object.keys(layers)) {
              if (key !== 'labels') layers[key] = !layers[key];
            }
            return { ...current, anatomy: { ...current.anatomy, layers } };
          });
          pushToast(`Règle « ${rule.name} » : couches anatomiques inversées`, 'ok');
        } else if (rule.action.type === 'clear-paint') {
          paintRef.current.clear();
          pushToast('AirPaint effacé par geste', 'ok');
        } else if (rule.action.type === 'show-toast') {
          pushToast(String(rule.action.payload?.message ?? rule.name), 'info');
        }
        bus.emit({
          type: 'rule.fired',
          source: 'system.rules',
          label: rule.id,
          attributes: { action: rule.action.type },
        });
      },
    );
  }, [bus, pushToast]);

  useEffect(() => {
    rulesRef.current?.setRules(settings.rules);
  }, [settings.rules]);

  const updateSettings = useCallback((updater: (current: StoredSettings) => StoredSettings) => {
    setSettings((current) => updater(current));
  }, []);

  const toggleDetector = useCallback((key: keyof DetectorSettings) => {
    setSettings((current) => ({
      ...current,
      detectors: { ...current.detectors, [key]: !current.detectors[key] },
    }));
  }, []);

  const ensureEngine = useCallback(
    async (kinds: EngineKind[]) => {
      if (!engineRef.current) {
        engineRef.current = new MediaPipeEngine('GPU', settingsRef.current.modelCache.mode);
      }
      const engine = engineRef.current;
      for (const kind of kinds) {
        if (engine.ready[kind]) continue;
        setEngineStatus((current) => ({ ...current, [kind]: 'chargement…' }));
        try {
          await engine.ensure(kind);
          setEngineStatus((current) => ({ ...current, [kind]: 'prêt' }));
        } catch (cause) {
          setEngineStatus((current) => ({
            ...current,
            [kind]: `erreur: ${cause instanceof Error ? cause.message : 'inconnue'}`,
          }));
          setError((current) => current ?? `Moteur ${kind} indisponible. Les autres modules continuent.`);
        }
      }
    },
    [],
  );

  const startCamera = useCallback(async () => {
    if (startLock.current) return;
    startLock.current = true;
    setError(null);
    setCamera('requesting');
    try {
      // Camera first: a denied microphone must never prevent video tracking.
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: 'user' },
      });
      streamRef.current = stream;
      setCamera('granted');
      const video = videoRef.current;
      if (video) {
        video.srcObject = stream;
        await video.play().catch(() => undefined);
      }

      if (settingsRef.current.detectors.audio) {
        try {
          const micStream = await navigator.mediaDevices.getUserMedia({
            audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true },
          });
          audioStreamRef.current = micStream;
          setMicrophone('granted');
          if (!audioRef.current) audioRef.current = new AudioAnalyser(bus);
          await audioRef.current.start(micStream);
        } catch {
          setMicrophone('denied');
          pushToast('Caméra active, mais micro refusé ou indisponible.', 'warn');
        }
      } else {
        setMicrophone('idle');
      }

      const detectors = settingsRef.current.detectors;
      const kinds: EngineKind[] = [];
      if (detectors.face) kinds.push('face');
      if (detectors.hands) kinds.push('hands');
      if (detectors.pose) kinds.push('pose');
      if (detectors.objects) kinds.push('objects');
      if (detectors.gestures) kinds.push('gestures');
      if (video) {
        if (!loopRef.current) {
          loopRef.current = new PerceptionLoop(video, engineRef.current!, bus, (next) => {
            const nowMs = performance.now();
            if (next.pose.length) lastPoseSeen.current = nowMs;
            if (next.face.length) lastFaceSeen.current = nowMs;
            // Hold the last pose for 500 ms so a single missed frame does not
            // make the anatomy overlay blink or report "absent".
            if (!next.pose.length && nowMs - lastPoseSeen.current < 500) {
              next = { ...next, pose: latestSnapshotRef.current.pose };
            }
            if (!next.face.length && nowMs - lastFaceSeen.current < 500) {
              next = { ...next, face: latestSnapshotRef.current.face };
            }
            latestSnapshotRef.current = next;
            const now = performance.now();
            if (now - lastSnapshotUi.current > 110) {
              lastSnapshotUi.current = now;
              setSnapshot(next);
            }
          });
        }
        loopRef.current.errors.length = 0;
        loopRef.current.start();
      }
      setRunning(true);
      bus.emit({ type: 'session.state', source: 'core.media', label: 'camera-start', attributes: {} });

      // Model downloads / GPU warmup can take seconds: keep the UI live and let
      // each engine appear as soon as it is ready.
      void ensureEngine(kinds);
    } catch (cause) {
      setCamera('denied');
      setError(
        cause instanceof Error && cause.name === 'NotAllowedError'
          ? 'Accès caméra refusé. Tu peux réessayer avec le bouton caméra.'
          : `Caméra indisponible : ${cause instanceof Error ? cause.message : 'erreur inconnue'}`,
      );
    } finally {
      startLock.current = false;
    }
  }, [bus, ensureEngine, pushToast]);

  const stopCamera = useCallback(() => {
    setRunning(false);
    loopRef.current?.stop();
    loopRef.current = null;
    audioRef.current?.stop();
    streamRef.current?.getTracks().forEach((track) => track.stop());
    audioStreamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
    audioStreamRef.current = null;
    if (videoRef.current) videoRef.current.srcObject = null;
    latestSnapshotRef.current = emptySnapshot();
    setSnapshot(emptySnapshot());
    setRunning(false);
    bus.emit({ type: 'session.state', source: 'core.media', label: 'camera-stop', attributes: {} });
  }, [bus]);

  useEffect(() => {
    return () => {
      stopCamera();
      engineRef.current?.close();
      engineRef.current = null;
      loopRef.current = null;
    };
  }, [stopCamera]);

  /** FPS / audio sampling loop (independent from inference). */
  useEffect(() => {
    let raf = 0;
    const tick = () => {
      const now = performance.now();
      frameCount.current += 1;
      if (now - fpsWindowStart.current >= 1000) {
        setFps(Math.round((frameCount.current * 1000) / (now - fpsWindowStart.current)));
        frameCount.current = 0;
        fpsWindowStart.current = now;
        if (loopRef.current) {
          setTimings({ ...loopRef.current.timings });
          setLatency(loopRef.current.summary());
        }
      }
      if (audioRef.current) {
        const band = audioRef.current.sample(now);
        audioBars.current = [...audioBars.current.slice(-19), Math.max(0, Math.min(1, band.rms * 9))];
        // 60 setState/s would re-render the whole studio for a VU-meter.
        if (now - lastAudioUi.current > 90) {
          lastAudioUi.current = now;
          setAudioLevels([...audioBars.current]);
        }
      }
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, []);

  /** Overlay renderer: relies on snapshot in a ref to avoid React re-render per frame. */
  useEffect(() => {
    let raf = 0;
    const draw = () => {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      if (canvas && video) {
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        const width = canvas.clientWidth;
        const height = canvas.clientHeight;
        if (canvas.width !== Math.round(width * dpr) || canvas.height !== Math.round(height * dpr)) {
          canvas.width = Math.round(width * dpr);
          canvas.height = Math.round(height * dpr);
        }
        const context = canvas.getContext('2d');
        if (context) {
          context.setTransform(dpr, 0, 0, dpr, 0, 0);
          context.clearRect(0, 0, width, height);
          drawOverlay(context, width, height, latestSnapshotRef.current, settingsRef.current, paintRef.current);
        }
      }
      raf = requestAnimationFrame(draw);
    };
    raf = requestAnimationFrame(draw);
    return () => cancelAnimationFrame(raf);
  }, []);

  /**
   * AirPaint pump: uses the stabilized snapshot and not raw per-frame events.
   * Pinch draws, a closed fist held ~400 ms clears the canvas.
   */
  useEffect(() => {
    const pinch = snapshot.hands.find((hand) => hand.gesture.gesture === 'pincement');
    const fist = snapshot.hands.some((hand) => hand.gesture.gesture === 'poing');
    const model = paintRef.current;

    if (pinch) {
      const tip = pinch.points[8] ?? pinch.points[4];
      if (tip) {
        if (!pinchRef.current || !model.isDrawing) {
          model.begin({ x: tip.x, y: tip.y });
          pinchRef.current = true;
        } else {
          model.append({ x: tip.x, y: tip.y });
        }
      }
    } else if (pinchRef.current) {
      model.end();
      pinchRef.current = false;
    }

    if (fist && settings.paint.clearWithFist) {
      fistFrames.current += 1;
      if (fistFrames.current > 8) {
        model.clear();
        fistFrames.current = 0;
        pushToast('Poing maintenu — AirPaint effacé', 'ok');
      }
    } else {
      fistFrames.current = 0;
    }
  }, [snapshot, settings.paint.clearWithFist, pushToast]);

  /**
   * Capture is the only place a raw frame is materialised. If the user enabled
   * "anonymiser les exports", every detected face box is blurred before the PNG
   * is produced — the raw frame never gets exported in that mode.
   */
  const grabFrame = useCallback((): string | null => {
    const video = videoRef.current;
    if (!video || video.readyState < 2) return null;
    const offscreen = document.createElement('canvas');
    offscreen.width = video.videoWidth;
    offscreen.height = video.videoHeight;
    const context = offscreen.getContext('2d');
    if (!context) return null;
    context.drawImage(video, 0, 0);

    if (settingsRef.current.privacy.anonymizeExports) {
      const faceBox = faceBoxFromPoints(
        latestSnapshotRef.current.face,
        offscreen.width,
        offscreen.height,
      );
      if (faceBox) {
        const box = clampBox(expandBox(faceBox, 0.18), offscreen.width, offscreen.height);
        const snapshot = context.getImageData(box.x, box.y, box.width, box.height);
        const blurred = blurredCopy(snapshot, Math.max(12, Math.round(box.width / 8)));
        context.putImageData(blurred, box.x, box.y);
      }
    }
    return offscreen.toDataURL('image/png');
  }, []);

  const exportEvents = useCallback(() => bus.exportJsonLines(), [bus]);

  const clearEvents = useCallback(() => {
    bus.clear();
    setEvents([]);
  }, [bus]);

  const updateRule = useCallback((ruleId: string, patch: Partial<RuleDefinition>) => {
    updateSettings((current) => ({
      ...current,
      rules: current.rules.map((rule) => (rule.id === ruleId ? { ...rule, ...patch } : rule)),
    }));
  }, [updateSettings]);

  return {
    videoRef,
    canvasRef,
    bus,
    paint: paintRef.current,
    state: {
      camera,
      microphone,
      running,
      error,
      events,
      snapshot,
      settings,
      timings,
      latency,
      engineStatus,
      fps,
      inferenceMs:
        Object.values(timings).length > 0
          ? Math.round(Object.values(timings).reduce((sum, value) => sum + value, 0))
          : 0,
      toasts,
      audioLevels,
    } as StudioState,
    actions: {
      startCamera,
      stopCamera,
      toggleDetector,
      updateSettings,
      pushToast,
      grabFrame,
      exportEvents,
      clearEvents,
      updateRule,
      setError,
    },
  };
}

/** Canvas filter path used when available; falls back to scaled re-draw. */
function blurredCopy(source: ImageData, radius: number): ImageData {
  const canvas = document.createElement('canvas');
  canvas.width = source.width;
  canvas.height = source.height;
  const context = canvas.getContext('2d');
  if (!context) return source;
  const input = document.createElement('canvas');
  input.width = source.width;
  input.height = source.height;
  const inputContext = input.getContext('2d');
  if (!inputContext) return source;
  inputContext.putImageData(source, 0, 0);
  context.filter = `blur(${radius}px)`;
  context.drawImage(input, 0, 0);
  return context.getImageData(0, 0, source.width, source.height);
}

function drawOverlay(
  context: CanvasRenderingContext2D,
  width: number,
  height: number,
  snapshot: PerceptionSnapshot,
  settings: StoredSettings,
  paint: PaintModel,
): void {
  const faceColor = 'rgba(89, 242, 200, 0.85)';
  const handColor = 'rgba(124, 199, 255, 0.9)';
  const poseColor = 'rgba(255, 212, 121, 0.8)';

  // Mirror coordinates to match the CSS-mirrored video.
  const px = (x: number) => (1 - x) * width;
  const py = (y: number) => y * height;

  if (snapshot.face.length) {
    context.fillStyle = faceColor;
    for (const point of snapshot.face) {
      context.fillRect(px(point.x) - 0.8, py(point.y) - 0.8, 1.6, 1.6);
    }
    const nose = snapshot.face[1];
    if (nose) {
      context.strokeStyle = 'rgba(89, 242, 200, 0.35)';
      context.lineWidth = 1;
      context.beginPath();
      context.arc(px(nose.x), py(nose.y), 42 + Math.sin(performance.now() / 600) * 2, 0, Math.PI * 2);
      context.stroke();
    }
  }

  if (snapshot.hands.length) {
    context.strokeStyle = handColor;
    context.fillStyle = handColor;
    context.lineWidth = 2;
    for (const hand of snapshot.hands) {
      for (const point of hand.points) {
        context.beginPath();
        context.arc(px(point.x), py(point.y), 2.4, 0, Math.PI * 2);
        context.fill();
      }
      const connections: Array<[number, number]> = [
        [0, 1], [1, 2], [2, 3], [3, 4],
        [0, 5], [5, 6], [6, 7], [7, 8],
        [5, 9], [9, 10], [10, 11], [11, 12],
        [9, 13], [13, 14], [14, 15], [15, 16],
        [13, 17], [17, 18], [18, 19], [19, 20],
        [0, 17],
      ];
      context.strokeStyle = 'rgba(124, 199, 255, 0.55)';
      for (const [a, b] of connections) {
        const start = hand.points[a];
        const end = hand.points[b];
        if (!start || !end) continue;
        context.beginPath();
        context.moveTo(px(start.x), py(start.y));
        context.lineTo(px(end.x), py(end.y));
        context.stroke();
      }
    }
  }

  if (snapshot.pose.length) {
    context.strokeStyle = poseColor;
    context.lineWidth = 1.6;
    const links: Array<[number, number]> = [
      [11, 12], [11, 13], [13, 15], [12, 14], [14, 16],
      [11, 23], [12, 24], [23, 24],
      [23, 25], [25, 27], [24, 26], [26, 28],
    ];
    for (const [a, b] of links) {
      const start = snapshot.pose[a];
      const end = snapshot.pose[b];
      if (!start || !end) continue;
      context.beginPath();
      context.moveTo(px(start.x), py(start.y));
      context.lineTo(px(end.x), py(end.y));
      context.stroke();
    }
    context.fillStyle = poseColor;
    for (const point of snapshot.pose) {
      context.beginPath();
      context.arc(px(point.x), py(point.y), 1.8, 0, Math.PI * 2);
      context.fill();
    }
  }

  if (snapshot.objects.length) {
    context.font = '11px Inter, sans-serif';
    for (const object of snapshot.objects) {
      const x = px(object.box.x + object.box.width);
      const y = py(object.box.y);
      const w = object.box.width * width;
      const h = object.box.height * height;
      context.strokeStyle = 'rgba(89, 242, 200, 0.7)';
      context.lineWidth = 1.2;
      context.strokeRect(x, y, w, h);
      const label = `${object.label} ${Math.round(object.confidence * 100)}%`;
      const textWidth = context.measureText(label).width + 8;
      context.fillStyle = 'rgba(2, 14, 11, 0.72)';
      context.fillRect(x, Math.max(0, y - 15), textWidth, 14);
      context.fillStyle = '#9ff5dc';
      context.fillText(label, x + 4, Math.max(10, y - 4));
    }
  }

  // Anatomy overlay (schematic, explicitly educational).
  if (snapshot.pose.length >= 29) {
    const anchors = buildSkeletalAnchors(snapshot.pose);
    const opacity = settings.anatomy.opacity;
    const layers: Record<string, boolean> = settings.anatomy.layers;
    const layerColor: Record<AnatomyLayer, string> = {
      skeleton: '#e8f6ff',
      muscles: '#ff7c8a',
      nervous: '#ffd166',
      organs: '#8fe3a5',
      vessels: '#ff5c5c',
      labels: '#9ad7ff',
    };
    for (const bone of anchors) {
      if (!layers[bone.system]) continue;
      if (!isBoneVisible(bone)) continue;
      const color = layerColor[bone.system as AnatomyLayer] ?? '#e8f6ff';
      context.strokeStyle = color;
      context.globalAlpha = opacity * (settings.anatomy.lens ? 0.55 : 1);
      context.lineWidth = 3.2;
      context.beginPath();
      context.moveTo(px(bone.a.x), py(bone.a.y));
      context.lineTo(px(bone.b.x), py(bone.b.y));
      context.stroke();
      context.globalAlpha = 1;
      if (settings.anatomy.labels) {
        context.font = '9px Inter, sans-serif';
        context.fillStyle = 'rgba(220, 245, 255, 0.78)';
        context.fillText(bone.label, px(bone.b.x) + 5, py(bone.b.y) - 4);
      }
    }
  }

  // AirPaint strokes (mirrored horizontally, like the camera).
  for (const stroke of paint.strokes) {
    if (stroke.points.length < 2) continue;
    context.strokeStyle = stroke.color;
    context.lineWidth = Math.max(1.4, stroke.width * width);
    context.lineCap = 'round';
    context.lineJoin = 'round';
    context.beginPath();
    stroke.points.forEach((point, index) => {
      const x = px(point.x);
      const y = py(point.y);
      if (index === 0) context.moveTo(x, y);
      else context.lineTo(x, y);
    });
    context.stroke();
  }
}
