// OBS WebSocket 5 client. Browser-only, no dependencies, localhost only.
// Authentication is performed in memory; passwords are never persisted.
const encoder = new TextEncoder();

export function normaliseLocalOBSURL(value = 'ws://127.0.0.1:4455') {
  const url = new URL(value);
  const host = url.hostname.toLowerCase();
  if (url.protocol !== 'ws:' || !['127.0.0.1', 'localhost', '[::1]'].includes(host) ||
      (url.pathname !== '/' && url.pathname !== '') || url.search || url.hash || url.username || url.password) {
    throw new Error('OBS doit être accessible par WebSocket local uniquement (ws://127.0.0.1:4455).');
  }
  const port = Number(url.port || '80');
  if (!Number.isInteger(port) || port < 1 || port > 65535) throw new Error('Port OBS invalide');
  return url.toString();
}

async function hashBase64(value, cryptoAPI) {
  if (!cryptoAPI?.subtle) throw new Error('WebCrypto indisponible : page locale HTTPS/localhost requise.');
  const digest = await cryptoAPI.subtle.digest('SHA-256', encoder.encode(value));
  return btoa(String.fromCharCode(...new Uint8Array(digest)));
}

export async function obsAuthentication(password, salt, challenge, cryptoAPI = globalThis.crypto) {
  if (typeof salt !== 'string' || typeof challenge !== 'string') throw new Error('Défi OBS invalide');
  const secret = await hashBase64(String(password) + salt, cryptoAPI);
  return hashBase64(secret + challenge, cryptoAPI);
}

export class OBSClient {
  constructor({ WebSocketClass = globalThis.WebSocket, cryptoAPI = globalThis.crypto, timeoutMs = 6000 } = {}) {
    this.WebSocketClass = WebSocketClass;
    this.cryptoAPI = cryptoAPI;
    this.timeoutMs = timeoutMs;
    this.socket = null;
    this.connected = false;
    this.pending = new Map();
    this.onEvent = () => {};
    this.onStatus = () => {};
    this.nextId = 0;
  }

  async connect({ url = 'ws://127.0.0.1:4455', password = '' } = {}) {
    const validatedURL = normaliseLocalOBSURL(url);
    if (!this.WebSocketClass) throw new Error('WebSocket indisponible');
    this.disconnect();
    const socket = new this.WebSocketClass(validatedURL);
    this.socket = socket;
    return new Promise((resolve, reject) => {
      let settled = false;
      const timer = setTimeout(() => {
        fail(new Error('Délai de connexion OBS dépassé'));
      }, this.timeoutMs);
      const fail = (error) => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        if (this.socket === socket) this.socket = null;
        try { socket.close(); } catch {}
        reject(error);
      };
      socket.onmessage = async (event) => {
        if (this.socket !== socket) return;
        try {
          const packet = JSON.parse(event.data);
          if (packet.op === 0) {
            const hello = packet.d || {};
            if (hello.rpcVersion < 1) throw new Error('Version du protocole OBS incompatible');
            const identification = { rpcVersion: 1, eventSubscriptions: (1 << 2) | (1 << 6) };
            if (hello.authentication) {
              if (!password) throw new Error('OBS demande un mot de passe WebSocket');
              identification.authentication = await obsAuthentication(password, hello.authentication.salt, hello.authentication.challenge, this.cryptoAPI);
            }
            socket.send(JSON.stringify({ op: 1, d: identification }));
          } else if (packet.op === 2) {
            if (settled) return;
            settled = true;
            clearTimeout(timer);
            this.connected = true;
            this.onStatus('connected');
            resolve(packet.d || {});
          } else if (packet.op === 5) {
            this.onEvent(packet.d?.eventType, packet.d?.eventData || {});
          } else if (packet.op === 7) {
            const response = packet.d || {};
            const pending = this.pending.get(response.requestId);
            if (!pending) return;
            clearTimeout(pending.timer);
            this.pending.delete(response.requestId);
            if (response.requestStatus?.result === true) pending.resolve(response.responseData || {});
            else pending.reject(new Error(response.requestStatus?.comment || 'Requête OBS refusée'));
          }
        } catch (error) {
          if (!this.connected) fail(error);
          else this.onStatus('error', error);
        }
      };
      socket.onerror = () => { if (!settled) fail(new Error('Impossible de joindre OBS WebSocket')); };
      socket.onclose = (event) => {
        if (!settled) { fail(new Error('OBS a fermé la connexion (' + (event.code || 'sans code') + ')')); return; }
        if (this.socket !== socket) return;
        this.socket = null;
        this.connected = false;
        this.rejectPending('Connexion OBS fermée');
        this.onStatus('disconnected');
      };
    });
  }

  rejectPending(message) {
    for (const item of this.pending.values()) {
      clearTimeout(item.timer);
      item.reject(new Error(message));
    }
    this.pending.clear();
  }

  disconnect() {
    const old = this.socket;
    this.socket = null;
    this.connected = false;
    this.rejectPending('Connexion OBS interrompue');
    if (old) {
      old.onmessage = null;
      old.onerror = null;
      old.onclose = null;
      try { old.close(); } catch {}
    }
    this.onStatus('disconnected');
  }

  request(requestType, requestData = {}) {
    if (!this.connected || !this.socket) return Promise.reject(new Error('OBS non connecté'));
    const requestId = 'olympus-' + (++this.nextId);
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(requestId);
        reject(new Error('OBS ne répond pas à ' + requestType));
      }, this.timeoutMs);
      this.pending.set(requestId, { resolve, reject, timer });
      try {
        this.socket.send(JSON.stringify({ op: 6, d: { requestType, requestId, requestData } }));
      } catch (error) {
        clearTimeout(timer);
        this.pending.delete(requestId);
        reject(error);
      }
    });
  }

  getScenes() { return this.request('GetSceneList'); }
  getRecordStatus() { return this.request('GetRecordStatus'); }
  setProgramScene(sceneName) { return this.request('SetCurrentProgramScene', { sceneName }); }
  startRecord() { return this.request('StartRecord'); }
  stopRecord() { return this.request('StopRecord'); }
}
