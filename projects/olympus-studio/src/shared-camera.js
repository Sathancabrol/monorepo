// OLYMPUS Studio — opt-in shared camera preview over private Tailscale Serve.
// No cloud. No audio. No access to ComfyUI / OBS / Hermes APIs.
// JPEG frames ~4fps are a low-latency prototype, not full WebRTC video.
import { acquireCamera, releaseCamera } from './camera-pool.js';
const holder = document.getElementById('sharedCameras');
const status = document.createElement('p');
status.className = 'notice';
status.textContent = 'Chargement des caméras partagées…';

const heading = document.createElement('h2');
heading.textContent = 'CAMÉRAS · APPAREILS CONNECTÉS';
const details = document.createElement('p');
details.className = 'muted';
details.textContent = 'La webcam locale ne se partage pas automatiquement. Utilise « Diffuser ma caméra » pour transmettre volontairement des images aux autres appareils OLYMPUS du réseau privé. Sans audio.';
const controls = document.createElement('div');
controls.className = 'actions';
const nameInput = document.createElement('input');
nameInput.placeholder = 'Nom de cet appareil';
nameInput.value = 'Caméra ' + (navigator.userAgentData?.mobile ? 'téléphone' : 'ordinateur');
nameInput.maxLength = 40;
nameInput.setAttribute('aria-label','Nom de cet appareil');
const startButton = document.createElement('button');
startButton.textContent = 'Diffuser ma caméra';
const stopButton = document.createElement('button');
stopButton.textContent = '■ Arrêter la diffusion';
stopButton.disabled = true;
const ownPreview = document.createElement('div');
ownPreview.className = 'cards';
const remoteFeeds = document.createElement('div');
remoteFeeds.className = 'cards';
controls.append(nameInput, startButton, stopButton);
holder?.append(heading, details, controls, status, ownPreview, remoteFeeds);

const remote = new Map();
let published = null;
let available = false;
let busy = false;
const cameraCanvas = document.createElement('canvas');
cameraCanvas.width = 640;
cameraCanvas.height = 360;
const cameraCtx = cameraCanvas.getContext('2d', { alpha:false });

function message(value) { status.textContent = value; }
function identity() { return { id:crypto.randomUUID(), key:crypto.randomUUID() }; }

function stopLocal() {
  if (!published) return;
  const old = published;
  published = null;
  releaseCamera('shared-preview');
  clearTimeout(old.timer);
  ownPreview.replaceChildren();
  startButton.disabled = !available;
  stopButton.disabled = true;
  nameInput.disabled = false;
  // Best effort; stale frames are automatically forgotten by the relay within 12 s.
  fetch('/api/live/frame?id=' + encodeURIComponent(old.id), {
    method:'DELETE', headers:{ 'X-Olympus-Stream-Key':old.key }, keepalive:true,
  }).catch(() => {});
  message('Diffusion arrêtée : ta caméra n’est plus publiée.');
}
async function publishFrame() {
  const active = published;
  if (!active || busy) return;
  if (active.video.readyState < 2) {
    active.timer = setTimeout(publishFrame, 250);
    return;
  }
  busy = true;
  try {
    cameraCtx.drawImage(active.video, 0, 0, cameraCanvas.width, cameraCanvas.height);
    const image = await new Promise(resolve => cameraCanvas.toBlob(resolve, 'image/jpeg', .58));
    if (!image || published !== active) return;
    const res = await fetch('/api/live/frame', {
      method:'POST', headers:{
        'Content-Type':'image/jpeg',
        'X-Olympus-Stream-ID':active.id,
        'X-Olympus-Stream-Key':active.key,
        'X-Olympus-Device-Name':nameInput.value.trim().slice(0,40) || 'Appareil',
      }, body:image,
    });
    if (!res.ok) throw new Error('Relais HTTP ' + res.status);
    message('Caméra diffusée sur OLYMPUS · image sans audio · arrêter avec ■');
  } catch(e) {
    message('Transmission temporairement indisponible : '+ e.message);
  } finally {
    busy = false;
    if (published === active) active.timer = setTimeout(publishFrame, 230);
  }
}
async function startLocal() {
  if (!available || published) return;
  startButton.disabled = true;
  try {
    const media = await acquireCamera('shared-preview', { preferRear:true });
    const video = document.createElement('video');
    video.autoplay = true;
    video.playsInline = true;
    video.muted = true;
    video.style.cssText = 'width:100%;max-width:360px;border-radius:8px;background:black';
    video.srcObject = media;
    const ended = () => stopLocal();
    media.getVideoTracks().forEach(track => track.addEventListener('ended', ended, {once:true}));
    try { await video.play(); }
    catch(e) { releaseCamera('shared-preview'); throw e; }
    const id = identity();
    published = { ...id, media, video, timer:null };
    ownPreview.replaceChildren(video);
    stopButton.disabled = false;
    nameInput.disabled = true;
    message('Caméra activée sur cet appareil. Connexion au relais…');
    publishFrame();
  } catch(e) {
    releaseCamera('shared-preview');
    startButton.disabled = !available;
    message('Caméra indisponible (' + (e.name || 'Erreur') + ') : ' + e.message + '. Ferme les autres applis caméra, puis recharge la page.');
  }
}
startButton.onclick = startLocal;
stopButton.onclick = stopLocal;

function removeRemote(id) {
  const item = remote.get(id);
  if (!item) return;
  clearInterval(item.interval);
  item.root.remove();
  remote.delete(id);
  window.olympusRemoveRemoteCamera?.(id);
}
function addRemote(stream) {
  const root = document.createElement('div');
  root.className = 'mini-card';
  const title = document.createElement('h3');
  title.textContent = stream.name;
  const img = document.createElement('img');
  img.alt = 'Caméra distante : ' + stream.name;
  img.style.cssText = 'display:block;width:100%;aspect-ratio:16/9;object-fit:contain;background:black;border-radius:8px';
  const addButton = document.createElement('button');
  addButton.textContent = 'Ajouter à ma scène LIVE';
  addButton.onclick = () => {
    if (typeof window.olympusAddRemoteCamera === 'function') {
      window.olympusAddRemoteCamera(stream.id, stream.name, img);
      message('Caméra distante ajoutée à la scène locale (non synchronisée).');
    }
  };
  root.append(title, img, addButton);
  remoteFeeds.append(root);
  let pending = false;
  const reload = () => {
    if (pending || document.hidden) return;
    pending = true;
    const query = '/api/live/frame?id='+encodeURIComponent(stream.id)+'&v='+Date.now();
    // This frame remains an image-only, read-only request.
    img.onload = () => { pending = false; };
    img.onerror = () => { pending = false; };
    img.src = query;
  };
  const interval = setInterval(reload, 280);
  remote.set(stream.id, { root, img, interval });
  reload();
}
async function refreshPeers() {
  try {
    const res = await fetch('/api/live/streams', { cache:'no-store' });
    if (!res.ok) throw new Error('Relais absent');
    const data = await res.json();
    if (!Array.isArray(data.streams)) throw new Error('Réponse invalide');
    available = true;
    if (!published) startButton.disabled = false;
    const seen = new Set();
    for (const item of data.streams) {
      if (published?.id === item.id) continue;
      seen.add(item.id);
      if (!remote.has(item.id)) addRemote(item);
    }
    for (const id of remote.keys()) if (!seen.has(id)) removeRemote(id);
    if (!published) message('Relais actif · '+ remote.size + ' caméra(s) distante(s). Clique sur « Diffuser ma caméra » pour partager celle de cet appareil.');
  } catch {
    available = false;
    startButton.disabled = true;
    if (!published) message('Relais caméra absent sur cette adresse. Ouvre OLYMPUS sur le port 8788 ou via l’URL Tailscale HTTPS.');
  }
}

startButton.disabled = true;
if (holder) {
  refreshPeers();
  setInterval(refreshPeers, 1700);
  window.addEventListener('pagehide', stopLocal);
}
