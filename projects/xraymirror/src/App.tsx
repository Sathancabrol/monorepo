import { useCallback, useMemo, useState } from 'react';
import {
  Aperture,
  AudioWaveform,
  Barcode,
  Bone,
  Brain,
  Camera,
  CameraOff,
  CircleAlert,
  CirclePlay,
  CircleStop,
  Copy,
  Download,
  Gauge,
  History,
  Layers,
  Menu,
  Paintbrush,
  Puzzle,
  ScanFace,
  Settings,
  ShieldCheck,
  SlidersHorizontal,
  Sparkles,
  TriangleAlert,
  Workflow,
  X,
} from 'lucide-react';
import { useStudio } from './ui/useStudio';
import { Card, ToastStack } from './ui/components';
import { DetectionPanel } from './ui/panels/DetectionPanel';
import { TimelinePanel } from './ui/panels/TimelinePanel';
import { AnatomyPanel } from './ui/panels/AnatomyPanel';
import { PaintPanel } from './ui/panels/PaintPanel';
import { PluginsPanel } from './ui/panels/PluginsPanel';
import { AudioPanel } from './ui/panels/AudioPanel';
import { NutritionPanel } from './ui/panels/NutritionPanel';
import { CognitionPanel } from './ui/panels/CognitionPanel';
import { RulesPanel } from './ui/panels/RulesPanel';
import { ModelsPanel } from './ui/panels/ModelsPanel';
import { OverviewPanel } from './ui/panels/OverviewPanel';
import { SettingsPanel } from './ui/panels/SettingsPanel';
import type { DetectorSettings } from './core/types';
import { buildSkeletalAnchors, coverageFromBones } from './core/anatomy';

type ViewId = 'overview' | 'detection' | 'anatomy' | 'paint' | 'audio' | 'nutrition' | 'cognition' | 'plugins' | 'timeline' | 'models' | 'rules' | 'settings';

const NAV: Array<{ id: ViewId; label: string; icon: React.ReactNode; group: string }> = [
  { id: 'overview', label: 'Vue d’ensemble', icon: <Aperture size={14} />, group: 'Studio' },
  { id: 'detection', label: 'Perception', icon: <ScanFace size={14} />, group: 'Studio' },
  { id: 'anatomy', label: 'Anatomie AR', icon: <Bone size={14} />, group: 'Studio' },
  { id: 'paint', label: 'AirPaint', icon: <Paintbrush size={14} />, group: 'Studio' },
  { id: 'audio', label: 'Audio Lab', icon: <AudioWaveform size={14} />, group: 'Studio' },
  { id: 'nutrition', label: 'Nutrition', icon: <Barcode size={14} />, group: 'Studio' },
  { id: 'cognition', label: 'Cognition', icon: <Brain size={14} />, group: 'Studio' },
  { id: 'plugins', label: 'Plugins', icon: <Puzzle size={14} />, group: 'Système' },
  { id: 'timeline', label: 'Timeline', icon: <History size={14} />, group: 'Système' },
  { id: 'models', label: 'Model Hub', icon: <Layers size={14} />, group: 'Système' },
  { id: 'rules', label: 'Règles', icon: <Workflow size={14} />, group: 'Système' },
  { id: 'settings', label: 'Réglages', icon: <Settings size={14} />, group: 'Système' },
];

const TITLES: Record<ViewId, { title: string; sub: string }> = {
  overview: { title: 'X-Ray Mirror Studio', sub: 'Socle expérimental local-first — v0.7.0-exp.1' },
  detection: { title: 'Perception temps réel', sub: 'Visage, mains, posture, objets et sons, traitement local' },
  anatomy: { title: 'Anatomie & ancrages AR', sub: 'Couches schématiques ancrées sur la pose, sans maillage Écorché embarqué' },
  paint: { title: 'AirPaint', sub: 'Dessin gestuel, pincement et poing' },
  audio: { title: 'Audio Lab', sub: 'Niveau micro et transitoires locaux' },
  nutrition: { title: 'Nutrition', sub: 'Open Food Facts à la demande, cache local' },
  cognition: { title: 'Cognition expérimentale', sub: 'Mesures de performance, jamais de diagnostic' },
  plugins: { title: 'Centre de plugins', sub: 'Catalogue, permissions, réseau, GPU et état de validation' },
  timeline: { title: 'Timeline', sub: 'Événements horodatés, filtres, export JSONL' },
  models: { title: 'Model Hub', sub: 'Modèles épinglés, cache local et provenance' },
  rules: { title: 'Automatisation', sub: 'Règles Quand → Conditions → Action' },
  settings: { title: 'Réglages & confidentialité', sub: 'Profils, diagnostics et données locales' },
};

export default function App() {
  const { videoRef, canvasRef, paint, state, actions } = useStudio();
  const [dismissedToasts, setDismissedToasts] = useState<number[]>([]);
  const dismissToast = useCallback((id: number) => {
    setDismissedToasts((current) => [...current, id]);
  }, []);
  const visibleToasts = state.toasts.filter((toast) => !dismissedToasts.includes(toast.id));
  const [view, setView] = useState<ViewId>('overview');
  const [railOpen, setRailOpen] = useState(false);
  const [showLegal, setShowLegal] = useState(false);

  const groups = useMemo(() => {
    const map = new Map<string, typeof NAV>();
    for (const item of NAV) {
      map.set(item.group, [...(map.get(item.group) ?? []), item]);
    }
    return [...map.entries()];
  }, []);

  const toggleDetector = useCallback(
    (key: keyof DetectorSettings) => {
      actions.toggleDetector(key);
      if (key === 'audio') actions.pushToast('Le micro nécessite un redémarrage de la caméra', 'info');
    },
    [actions],
  );

  const grab = useCallback(() => {
    const data = actions.grabFrame();
    if (!data) {
      actions.pushToast('Aucune image disponible — démarre la caméra', 'warn');
      return;
    }
    const anchor = document.createElement('a');
    anchor.href = data;
    anchor.download = `xraymirror-capture-${Date.now()}.png`;
    anchor.click();
    actions.pushToast('Capture PNG enregistrée', 'ok');
  }, [actions]);

  return (
    <div className="layout">
      <aside className="rail" data-open={railOpen ? 'true' : 'false'} style={railOpen ? { display: 'flex' } : undefined}>
        <div className="brand">
          <div className="brand-mark"><Aperture size={18} /></div>
          <div>
            <div className="brand-title">X-Ray Mirror</div>
            <div className="brand-sub">Studio · expérimental</div>
          </div>
          <button className="icon-btn btn ghost" style={{ marginLeft: 'auto' }} onClick={() => setRailOpen(false)} aria-label="Fermer le menu">
            <X size={14} />
          </button>
        </div>

        {groups.map(([group, items]) => (
          <div key={group}>
            <div className="rail-group-label">{group}</div>
            <nav className="nav">
              {items.map((item) => (
                <button
                  key={item.id}
                  className={view === item.id ? 'active' : ''}
                  onClick={() => {
                    setView(item.id);
                    setRailOpen(false);
                  }}
                >
                  {item.icon}
                  {item.label}
                  {item.id === 'timeline' && state.events.length > 0 && <span className="nav-count">{state.events.length}</span>}
                  {item.id === 'plugins' && <span className="nav-count">24</span>}
                </button>
              ))}
            </nav>
          </div>
        ))}

        <div className="rail-foot">
          <div className="rail-badge"><span className={`dot ${state.running ? 'on' : ''}`} /> Caméra {state.camera === 'granted' ? 'active' : state.camera}</div>
          <div className="rail-badge"><span className={`dot ${state.microphone === 'granted' ? 'on' : 'warn'}`} /> Micro {state.microphone}</div>
          <div className="rail-badge"><span className={`dot ${state.snapshot.pose.length ? 'on' : ''}`} /> Pose {state.snapshot.pose.length ? 'suivie' : 'absente'}</div>
          <button className="btn small ghost" onClick={() => setShowLegal(true)}><ShieldCheck size={12} /> Limites & sécurité</button>
        </div>
      </aside>

      <main className="stage">
        <header className="topbar">
          <button className="btn icon-btn ghost" onClick={() => setRailOpen(true)} aria-label="Menu"><Menu size={15} /></button>
          <div className="grow">
            <h1>{TITLES[view].title}</h1>
            <div className="sub">{TITLES[view].sub}</div>
          </div>
          <span className={`badge ${state.running ? 'live' : ''}`}>{state.running ? '● local live' : 'hors ligne'}</span>
          <span className="badge" title="Version du socle">v0.7.0-exp.1</span>
          {state.running ? (
            <button className="btn danger" onClick={actions.stopCamera}><CircleStop size={13} /> Arrêter</button>
          ) : (
            <button className="btn primary" onClick={() => void actions.startCamera()} disabled={state.camera === 'requesting'}>
              {state.camera === 'requesting' ? <Sparkles size={13} /> : <CirclePlay size={13} />}
              {state.camera === 'requesting' ? 'Autorisation…' : 'Démarrer'}
            </button>
          )}
        </header>

        <section className="viewport-wrap">
          <div className="viewport">
            <video ref={videoRef} muted playsInline autoPlay />
            <canvas ref={canvasRef} className="overlay" />
            {!state.running && (
              <div className="placeholder" style={{ zIndex: 2 }}>
                <div>
                  <div className="ring"><Camera size={28} color="var(--accent)" /></div>
                  <h2>Perception locale, aucune image envoyée</h2>
                  <p>
                    Autorise la caméra pour démarrer le suivi visage, mains, posture et objets. Les modèles MediaPipe sont
                    téléchargés une fois puis mis en cache par le navigateur.
                  </p>
                  <button className="btn primary" style={{ marginTop: 14 }} onClick={() => void actions.startCamera()}>
                    <Camera size={14} /> Autoriser la caméra
                  </button>
                  <div style={{ marginTop: 10, color: 'var(--muted)', fontSize: 10.5 }}>
                    Sans caméra, l’audio, la nutrition et les exercices restent utilisables.
                  </div>
                </div>
              </div>
            )}
            {state.running && (
              <>
                <div className="hud">
                  <span className="hud-pill">{state.fps} FPS rendu</span>
                  <span className="hud-pill neutral">visage {state.snapshot.face.length ? '✓' : '—'}</span>
                  <span className="hud-pill neutral">mains {state.snapshot.hands.length}</span>
                  <span className="hud-pill neutral">objets {state.snapshot.objects.length}</span>
                  {Object.entries(state.timings).map(([key, ms]) => (
                    <span className="hud-pill neutral" key={key}>{key} {ms.toFixed(0)} ms</span>
                  ))}
                </div>
                <div className="overlay-chips">
                  {state.snapshot.hands.map((hand) => (
                    <div className="chip" key={hand.handedness}>
                      <span className="tag">main</span>{hand.handedness} · {hand.gesture.gesture}
                    </div>
                  ))}
                  {state.events.filter((event) => event.type === 'sound.detected').slice(-1).map((event) => (
                    <div className="chip sound" key={event.id}><span className="tag">son</span>{event.label} {Math.round((event.confidence ?? 0) * 100)} %</div>
                  ))}
                  {state.snapshot.objects.slice(0, 4).map((object, index) => (
                    <div className="chip" key={`${object.label}-${index}`}><span className="tag">objet</span>{object.label} {Math.round(object.confidence * 100)} %</div>
                  ))}
                </div>
                <div className="hud-bottom">
                  <button className="btn small" onClick={grab}><Camera size={12} /> Capture</button>
                  <button className="btn small ghost" onClick={() => actions.pushToast(`${paint.strokes.length} trait(s) — dessine avec un pincement`, 'info')}><Paintbrush size={12} /> Traits {paint.strokes.length}</button>
                  <span className="hud-pill neutral">micro {state.microphone}</span>
                  <span className="grow" />
                  <span className="hud-pill neutral">traitement local</span>
                </div>
              </>
            )}
          </div>
        </section>

        {state.error && (
          <div className="note warn" style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <CircleAlert size={14} />
            <span style={{ flex: 1 }}>{state.error}</span>
            <button className="btn small ghost" onClick={() => { actions.setError(null); void actions.startCamera(); }}>Réessayer</button>
          </div>
        )}

        {view === 'overview' && (
          <>
            <div className="plugin-grid">
              <QuickCard title="Démarrage" icon={<Camera size={14} />} text={state.running ? 'Caméra active. Clique sur un module.' : 'Autorise la caméra, puis active les modules utiles.'} />
              <QuickCard title="Confidentialité" icon={<ShieldCheck size={14} />} text="Aucune frame vidéo n’est transmise. Seul Open Food Facts sort, sur action explicite." />
              <QuickCard title="Realité du prototype" icon={<TriangleAlert size={14} />} text="Les fonctions marquées « prévues » ne sont pas intégrées. Les mesures sont locales et non cliniques." />
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1.2fr) minmax(0, 1fr)', gap: 12 }}>
              <TimelinePanel state={state} onClear={actions.clearEvents} getExport={actions.exportEvents} />
              <OverviewPanel state={state} getExport={actions.exportEvents} onGrab={grab} />
            </div>
          </>
        )}

        {view === 'detection' && (
          <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 1fr)', gap: 12 }}>
            <DetectionPanel state={state} onToggle={toggleDetector} />
            <TimelinePanel state={state} onClear={actions.clearEvents} getExport={actions.exportEvents} />
          </div>
        )}

        {view === 'anatomy' && (
          <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 1fr)', gap: 12 }}>
            <AnatomyPanel state={state} onChange={actions.updateSettings} />
            <Card title="Légende des mesures" icon={<Gauge size={14} color="var(--accent)" />} subtitle="Ce qui est calculé, ce qui ne l’est pas">
              <div className="list">
                <div className="row"><div className="grow"><div className="t">Ancrages depuis la pose</div><div className="s">Coordonnées normalisées 33 points MediaPipe</div></div><span className="tag">approximatif</span></div>
                <div className="row"><div className="grow"><div className="t">Longueur des os</div><div className="s">Distance en pixels normalisés, sans calibration</div></div><span className="tag">relatif</span></div>
                <div className="row"><div className="grow"><div className="t">Atlas Écorché</div><div className="s">Non embarqué dans ce socle</div></div><span className="tag">prévu</span></div>
                <div className="row"><div className="grow"><div className="t">Mesure clinique</div><div className="s">Volontairement absente</div></div><span className="tag">non</span></div>
              </div>
              <div className="note warn" style={{ marginTop: 9 }}>
                Pour utiliser les 634 structures Écorché, il faudra importer les GLB licites et valider les ancrages un par un. Ce prototype ne les invente pas.
              </div>
            </Card>
          </div>
        )}

        {view === 'paint' && (
          <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 1fr)', gap: 12 }}>
            <PaintPanel paint={paint} state={state} onChange={actions.updateSettings} />
            <TimelinePanel state={state} onClear={actions.clearEvents} getExport={actions.exportEvents} />
          </div>
        )}

        {view === 'audio' && (
          <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 1fr)', gap: 12 }}>
            <AudioPanel state={state} onToggle={() => toggleDetector('audio')} />
            <TimelinePanel state={state} onClear={actions.clearEvents} getExport={actions.exportEvents} />
          </div>
        )}

        {view === 'nutrition' && (
          <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1.1fr) minmax(0, 1fr)', gap: 12 }}>
            <NutritionPanel onToast={actions.pushToast} />
            <Card title="Ce qui marche et ce qui manque" icon={<Barcode size={14} color="var(--accent-2)" />}>
              <div className="list">
                <div className="row"><div className="grow"><div className="t">Recherche EAN</div><div className="s">Open Food Facts v2, cache 7 jours</div></div><span className="tag">réel</span></div>
                <div className="row"><div className="grow"><div className="t">Mode hors ligne</div><div className="s">Produits déjà consultés</div></div><span className="tag">réel</span></div>
                <div className="row"><div className="grow"><div className="t">Scan caméra</div><div className="s">BarcodeDetector/ZXing non branché</div></div><span className="tag">prévu</span></div>
                <div className="row"><div className="grow"><div className="t">Calories/portion</div><div className="s">Aucune estimation inventée</div></div><span className="tag">prévu</span></div>
              </div>
            </Card>
          </div>
        )}

        {view === 'cognition' && (
          <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1.1fr) minmax(0, 1fr)', gap: 12 }}>
            <CognitionPanel onToast={actions.pushToast} />
            <Card title="Ce que ces exercices ne sont pas" icon={<Brain size={14} color="var(--warn)" />}>
              <div className="list">
                <div className="row"><div className="grow"><div className="t">Un test de QI</div><div className="s">Non — seulement des essais de performance</div></div></div>
                <div className="row"><div className="grow"><div className="t">Une mesure d’attention en direct</div><div className="s">Non — les indicateurs vidéo sont des proxys</div></div></div>
                <div className="row"><div className="grow"><div className="t">Un diagnostic médical</div><div className="s">Non — aucune interprétation clinique</div></div></div>
              </div>
              <div className="note warn" style={{ marginTop: 9 }}>
                Les résultats dépendent du dispositif, de la latence et de l’apprentissage de la tâche. Ils doivent rester locaux et ne pas être utilisés pour évaluer autrui.
              </div>
            </Card>
          </div>
        )}

        {view === 'plugins' && <PluginsPanel onToast={actions.pushToast} />}
        {view === 'timeline' && <TimelinePanel state={state} onClear={actions.clearEvents} getExport={actions.exportEvents} />}
        {view === 'models' && (
          <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1.2fr) minmax(0, 1fr)', gap: 12 }}>
            <ModelsPanel engineStatus={state.engineStatus} />
            <Card title="Empreintes" icon={<ShieldCheck size={14} color="var(--ok)" />} subtitle="Aucune valeur inventée">
              <div className="note">
                Les entrées du catalogue ont une URL et une taille approximative, avec pour instruction de calculer les SHA-256 sur la machine cible. Le code refuse aujourd’hui de prétendre que les modèles sont vérifiés.
              </div>
              <div className="inline" style={{ marginTop: 9 }}>
                <button className="btn" onClick={() => { void navigator.clipboard?.writeText(location.href); actions.pushToast('Lien copié', 'ok'); }}><Copy size={12} /> Copier le lien</button>
                <button className="btn" onClick={() => window.open('https://github.com/toyxyz/toyxyz_RGBMocap', '_blank', 'noopener')}><Download size={12} /> Référence externe</button>
              </div>
            </Card>
          </div>
        )}
        {view === 'rules' && (
          <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1.1fr) minmax(0, 1fr)', gap: 12 }}>
            <RulesPanel state={state} onUpdate={actions.updateRule} />
            <Card title="Journal système" icon={<SlidersHorizontal size={14} color="var(--muted)" />}>
              <div className="list">
                {state.events.filter((event) => event.type === 'session.state').slice(-8).reverse().map((event) => (
                  <div className="row" key={event.id}>
                    <div className="grow"><div className="t">{event.label}</div><div className="s">{new Date(event.timestamp).toLocaleTimeString('fr-FR', { hour12: false })}</div></div>
                  </div>
                ))}
                {state.events.filter((event) => event.type === 'session.state').length === 0 && <div className="empty">Aucun événement de session.</div>}
              </div>
              <div className="note" style={{ marginTop: 9 }}>
                Les règles ne peuvent pas exécuter de commande système, appeler une URL ni lire un fichier. C’est une contrainte volontaire pour cette version de démonstration.
              </div>
            </Card>
          </div>
        )}
        {view === 'settings' && <SettingsPanel state={state} onChange={actions.updateSettings} onToast={actions.pushToast} />}

        <div className="footer-note">
          X-Ray Mirror Studio — socle expérimental local-first. Aucun diagnostic médical, aucune identification biométrique, aucun envoi de frames vidéo.
        </div>
      </main>

      <aside className="side">
        <Card title="Session" icon={<Camera size={14} color="var(--accent)" />} subtitle={`${state.fps} fps · ${state.events.length} événements`}>
          <div className="toolbar">
            {state.running ? (
              <button className="btn danger" onClick={actions.stopCamera}><CameraOff size={13} /> Arrêter</button>
            ) : (
              <button className="btn primary" onClick={() => void actions.startCamera()}><Camera size={13} /> Caméra</button>
            )}
            <button className="btn" onClick={grab} disabled={!state.running}><Camera size={13} /> Capture</button>
            <button className="btn ghost" onClick={() => actions.pushToast(state.running ? 'Traitement local, caméra active' : 'Caméra inactive', 'info')}><Gauge size={13} /> État</button>
          </div>
          <div className="metrics-grid" style={{ marginTop: 10 }}>
            <div className="metric"><div className="k">Caméra</div><div className="v" style={{ fontSize: 13 }}>{state.camera}</div></div>
            <div className="metric"><div className="k">Micro</div><div className="v" style={{ fontSize: 13 }}>{state.microphone}</div></div>
            <div className="metric"><div className="k">Visage</div><div className="v">{state.snapshot.face.length ? '✓' : '—'}</div></div>
            <div className="metric"><div className="k">Mains</div><div className="v">{state.snapshot.hands.length}</div></div>
            <div className="metric"><div className="k">Pose</div><div className="v">{state.snapshot.pose.length ? '✓' : '—'}</div></div>
            <div className="metric"><div className="k">Objets</div><div className="v">{state.snapshot.objects.length}</div></div>
          </div>
          {state.snapshot.objects.length > 0 && (
            <div className="list" style={{ marginTop: 9 }}>
              {state.snapshot.objects.slice(0, 4).map((object, index) => (
                <div className="row" key={`${object.label}-${index}`}>
                  <div className="grow"><div className="t">{object.label}</div><div className="s">{Math.round(object.confidence * 100)} % · COCO</div></div>
                  <div className="progress" style={{ width: 42, marginTop: 6 }}><span style={{ width: `${object.confidence * 100}%` }} /></div>
                </div>
              ))}
            </div>
          )}
        </Card>

        <Card title="Événements récents" icon={<History size={14} color="var(--accent-2)" />} subtitle="Flux du bus local" bodyClassName="scroll-panel" actions={
          <button className="btn small ghost" onClick={() => setView('timeline')}><CirclePlay size={12} /></button>
        }>
          {state.events.length === 0 ? (
            <div className="empty">Démarre la caméra : les détections apparaîtront ici en moins d’une seconde.</div>
          ) : (
            <div className="feed">
              {[...state.events].reverse().slice(0, 14).map((event) => (
                <div className="feed-item" key={event.id}>
                  <span className={`dot ${event.type.startsWith('sound') ? 'warn' : 'on'}`} />
                  <div>
                    <div className="name">{event.label ?? event.type}</div>
                    <div className="meta">{event.type}</div>
                  </div>
                  <time>{new Date(event.timestamp).toLocaleTimeString('fr-FR', { hour12: false })}</time>
                </div>
              ))}
            </div>
          )}
        </Card>

        <Card title="Qualité du suivi" icon={<Gauge size={14} color="var(--accent-2)" />} subtitle="Lecture des ancrages réellement exploitables">
          <div className="list">
            <div className="row">
              <div className="grow"><div className="t">Visage</div><div className="s">{faceQuality(state)}</div></div>
              <span className={`status-dot ${state.snapshot.face.length ? 'ready' : ''}`} />
            </div>
            <div className="row">
              <div className="grow"><div className="t">Pose</div><div className="s">{poseQuality(state)}</div></div>
              <span className={`status-dot ${state.snapshot.pose.length ? 'ready' : ''}`} />
            </div>
            <div className="row">
              <div className="grow"><div className="t">Mains</div><div className="s">{state.snapshot.hands.length === 0 ? 'aucune main détectée' : state.snapshot.hands.map((hand) => hand.handedness).join(' + ')}</div></div>
              <span className={`status-dot ${state.snapshot.hands.length ? 'ready' : ''}`} />
            </div>
          </div>
          <div className="note" style={{ marginTop: 8 }}>
            Une pose détectée hors-champ n’est pas comptée comme valide : seuls les segments dont les deux extrémités sont
            visibles alimentent l’overlay anatomique.
          </div>
        </Card>

        <Card title="Limites assumées" icon={<TriangleAlert size={14} color="var(--warn)" />}>
          <div className="note warn">
            Aucun test réel webcam/GTX 1060 n’a été exécuté ici. Les moteurs peuvent échouer selon les accès réseau, WebGL ou les droits caméra. Ce n’est pas un audit de sécurité.
          </div>
          <div className="note" style={{ marginTop: 7 }}>
            Les noms « anatomie », « cognition » et « nutrition » désignent des outils éducatifs expérimentaux, jamais un dispositif médical.
          </div>
        </Card>

        <div className="rail-badge"><span className={`dot ${state.running ? 'on' : 'warn'}`} /> {state.running ? 'Pipeline actif' : 'Pipeline en pause'}</div>
        <div className="rail-badge"><span className="dot on" /> Aucun frame vidéo transmis</div>
      </aside>

      <ToastStack toasts={state.toasts} onDismiss={(id) => {}} />

      {showLegal && (
        <div className="modal-backdrop" onClick={() => setShowLegal(false)}>
          <div className="modal" onClick={(event) => event.stopPropagation()}>
            <div className="modal-head">
              <ShieldCheck size={16} color="var(--accent)" />
              <h3>Limites, sécurité et honnêteté du prototype</h3>
              <button className="icon-btn btn ghost" onClick={() => setShowLegal(false)}><X size={14} /></button>
            </div>
            <div className="modal-body">
              <div className="note">
                Ce socle est une base expérimentale de démonstration. Il ne contient pas le code v0.6.0 de X-Ray Mirror Studio, ni les maillages Écorché, ni aucun modèle de langage local.
              </div>
              <div className="list">
                <div className="row"><div className="grow"><div className="t">Confidentialité</div><div className="s">Traitement des frames local. Open Food Facts est appelé seulement après validation d’un code-barres.</div></div></div>
                <div className="row"><div className="grow"><div className="t">Biométrie</div><div className="s">Aucune identification de personne. Les gestes et expressions sont des signaux visibles, pas des émotions prouvées.</div></div></div>
                <div className="row"><div className="grow"><div className="t">Santé</div><div className="s">Aucune finalité diagnostique. Les ancrages anatomiques sont approximatifs et schématiques.</div></div></div>
                <div className="row"><div className="grow"><div className="t">Réseau</div><div className="s">Téléchargement MediaPipe depuis Google, ou cache local. Aucune télémétrie applicative ajoutée.</div></div></div>
              </div>
              <div className="inline">
                <button className="btn" onClick={() => { void navigator.clipboard?.writeText(location.href); actions.pushToast('Lien copié', 'ok'); }}><Copy size={12} /> Copier le lien</button>
                <button className="btn primary" onClick={() => setShowLegal(false)}>Compris</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function faceQuality(state: ReturnType<typeof useStudio>['state']): string {
  if (!state.snapshot.face.length) return 'aucun visage dans le champ';
  const visible = state.snapshot.face.filter((point) => (point.visibility ?? 1) > 0.3).length;
  return `${visible}/${state.snapshot.face.length} points fiables`;
}

function poseQuality(state: ReturnType<typeof useStudio>['state']): string {
  if (!state.snapshot.pose.length) return 'pose absente';
  return `${Math.round(coverageRatio(state) * 100)} % des ancrages exploitables`;
}

function coverageRatio(state: ReturnType<typeof useStudio>['state']): number {
  if (!state.snapshot.pose.length) return 0;
  const anchors = buildSkeletalAnchors(state.snapshot.pose);
  return coverageFromBones(anchors).ratio;
}

function QuickCard({ title, text, icon }: { title: string; text: string; icon: React.ReactNode }) {
  return (
    <div className="plugin-card" style={{ minHeight: 96 }}>
      <div className="head"><div className="brand-mark" style={{ width: 28, height: 28 }}>{icon}</div><div className="grow"><h4>{title}</h4></div></div>
      <div className="desc">{text}</div>
    </div>
  );
}
