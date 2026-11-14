import { OBSClient } from './obs-client.js';

// Remote control of an OBS process already running on this computer.
// This does not replace the local MJPEG /obs output; it complements it.
export function mountOBSPanel(root) {
  if (!root) return null;
  const client = new OBSClient();
  root.innerHTML = `
    <div class="obs-panel">
      <p class="obs-hint">OBS 28+ · WebSocket intégré · réseau local uniquement.</p>
      <label class="obs-field">Adresse locale<input class="obs-url" value="ws://127.0.0.1:4455" spellcheck="false"></label>
      <label class="obs-field">Mot de passe OBS<input class="obs-password" type="password" autocomplete="off" placeholder="Non enregistré"></label>
      <div class="obs-buttons">
        <button class="obs-connect" type="button">Connecter</button>
        <button class="obs-disconnect" type="button" disabled>Déconnecter</button>
      </div>
      <p class="obs-feedback" role="status" aria-live="polite">Non connecté</p>
      <div class="obs-connected" hidden>
        <label class="obs-field">Scène programme<select class="obs-scenes" aria-label="Scène OBS"></select></label>
        <div class="obs-buttons">
          <button class="obs-refresh" type="button">Actualiser</button>
          <button class="obs-record" type="button">Démarrer REC</button>
        </div>
        <p class="obs-recstate">Enregistrement : état inconnu</p>
      </div>
      <p class="obs-hint">Activer « Outils → WebSocket Server Settings » dans OBS. Les commandes affectent OBS et non la scène Canvas OLYMPUS. Aucun stream n'est lancé automatiquement.</p>
    </div>`;
  const el = (selector) => root.querySelector(selector);
  const connectButton = el('.obs-connect'), disconnectButton = el('.obs-disconnect');
  const urlInput = el('.obs-url'), passwordInput = el('.obs-password');
  const connectedBox = el('.obs-connected'), feedback = el('.obs-feedback');
  const sceneSelect = el('.obs-scenes'), recButton = el('.obs-record');
  let recording = false;
  let busy = false;

  function message(value, isError = false) {
    feedback.textContent = value;
    feedback.classList.toggle('obs-error', isError);
  }
  function sync() {
    connectButton.disabled = busy || client.connected;
    disconnectButton.disabled = !client.connected;
    connectedBox.hidden = !client.connected;
    el('.obs-refresh').disabled = busy || !client.connected;
    sceneSelect.disabled = busy || !client.connected;
    recButton.disabled = busy || !client.connected;
    recButton.textContent = recording ? 'Arrêter REC' : 'Démarrer REC';
    el('.obs-recstate').textContent = 'Enregistrement OBS : ' + (recording ? 'ACTIF' : 'inactif');
  }

  async function refresh() {
    if (!client.connected) return;
    const [sceneData, recData] = await Promise.all([client.getScenes(), client.getRecordStatus()]);
    const previous = sceneData.currentProgramSceneName || sceneSelect.value;
    sceneSelect.replaceChildren();
    for (const scene of sceneData.scenes || []) {
      const opt = document.createElement('option');
      opt.value = scene.sceneName;
      opt.textContent = scene.sceneName;
      sceneSelect.append(opt);
    }
    if ([...sceneSelect.options].some(option => option.value === previous)) sceneSelect.value = previous;
    recording = recData.outputActive === true;
    sync();
    message('OBS connecté · ' + (sceneData.scenes || []).length + ' scène(s)');
  }

  client.onStatus = (kind, error) => {
    if (kind === 'disconnected') {
      recording = false;
      sync();
      message('OBS déconnecté');
    } else if (kind === 'error') {
      message('Erreur OBS : ' + (error?.message || 'inconnue'), true);
    }
  };
  client.onEvent = (type, data) => {
    if (type === 'CurrentProgramSceneChanged' && data.sceneName) sceneSelect.value = data.sceneName;
    if (type === 'RecordStateChanged') {
      recording = data.outputActive === true;
      sync();
    }
  };

  connectButton.addEventListener('click', async () => {
    busy = true; sync(); message('Connexion locale à OBS…');
    try {
      await client.connect({ url: urlInput.value.trim(), password: passwordInput.value });
      passwordInput.value = ''; // no password persistence after authentication
      await refresh();
    } catch (error) {
      client.disconnect();
      message('Connexion refusée : ' + error.message, true);
    } finally { busy = false; sync(); }
  });

  disconnectButton.addEventListener('click', () => {
    client.disconnect();
    passwordInput.value = '';
    message('OBS déconnecté manuellement');
  });

  el('.obs-refresh').addEventListener('click', async () => {
    busy = true; sync();
    try { await refresh(); } catch (error) { message('Actualisation impossible : ' + error.message, true); }
    finally { busy = false; sync(); }
  });

  sceneSelect.addEventListener('change', async () => {
    const name = sceneSelect.value;
    if (!name || !client.connected) return;
    busy = true; sync();
    try {
      await client.setProgramScene(name);
      message('Scène programme OBS : ' + name);
    } catch (error) { message('Changement de scène refusé : ' + error.message, true); }
    finally { busy = false; sync(); }
  });

  recButton.addEventListener('click', async () => {
    if (!client.connected) return;
    busy = true; sync();
    try {
      const current = await client.getRecordStatus();
      if (current.outputActive) {
        await client.stopRecord();
        message('Arrêt de l’enregistrement demandé à OBS');
      } else {
        await client.startRecord();
        message('Démarrage de l’enregistrement demandé à OBS');
      }
      await refresh();
    } catch (error) { message('Commande REC échouée : ' + error.message, true); }
    finally { busy = false; sync(); }
  });

  window.addEventListener('beforeunload', () => client.disconnect(), { once: true });
  sync();
  return client;
}
mountOBSPanel(document.getElementById('obsControl'));
