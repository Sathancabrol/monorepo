import { test } from 'node:test';
import assert from 'node:assert/strict';
import { webcrypto, createHash } from 'node:crypto';
import { OBSClient, normaliseLocalOBSURL, obsAuthentication } from '../src/obs-client.js';

test('URL OBS limitée à la machine locale', () => {
  assert.equal(normaliseLocalOBSURL('ws://127.0.0.1:4455'), 'ws://127.0.0.1:4455/');
  assert.equal(normaliseLocalOBSURL('ws://localhost:5555'), 'ws://localhost:5555/');
  for (const url of ['wss://example.com', 'ws://192.168.1.10:4455', 'ws://127.0.0.1:4455/anything',
    'ws://user:secret@localhost:4455', 'ws://localhost:4455/?token=bad']) {
    assert.throws(() => normaliseLocalOBSURL(url));
  }
});

test('Défi SHA-256 OBS v5 conforme', async () => {
  const secret = createHash('sha256').update('secret' + 'salt').digest('base64');
  const expected = createHash('sha256').update(secret + 'challenge').digest('base64');
  assert.equal(await obsAuthentication('secret', 'salt', 'challenge', webcrypto), expected);
});

class MockOBSWebSocket {
  constructor(url) {
    this.url = url;
    this.sent = [];
    this.closed = false;
    queueMicrotask(() => this.deliver({ op: 0, d: { rpcVersion: 1 } }));
  }
  deliver(message) { this.onmessage?.({ data: JSON.stringify(message) }); }
  send(value) {
    const packet = JSON.parse(value);
    this.sent.push(packet);
    if (packet.op === 1) {
      queueMicrotask(() => this.deliver({ op: 2, d: { negotiatedRpcVersion: 1 } }));
    }
    if (packet.op === 6) {
      const replies = {
        GetSceneList: { currentProgramSceneName: 'Studio', scenes: [{ sceneName: 'Studio' }, { sceneName: 'Écran' }] },
        GetRecordStatus: { outputActive: false },
        SetCurrentProgramScene: {},
        StartRecord: {},
        StopRecord: {},
      };
      queueMicrotask(() => this.deliver({
        op: 7, d: { requestId: packet.d.requestId, requestStatus: { result: true, code: 100 },
          responseData: replies[packet.d.requestType] || {} },
      }));
    }
  }
  close() {
    this.closed = true;
    queueMicrotask(() => this.onclose?.({ code: 1000 }));
  }
}

test('OBS : identification, scènes, commandes explicites et déconnexion', async () => {
  const client = new OBSClient({ WebSocketClass: MockOBSWebSocket, cryptoAPI: webcrypto, timeoutMs: 1000 });
  await client.connect();
  assert.equal(client.connected, true);
  const ws = client.socket;
  assert.equal(ws.sent[0].op, 1);
  const scenes = await client.getScenes();
  assert.equal(scenes.scenes.length, 2);
  assert.deepEqual(await client.getRecordStatus(), { outputActive: false });
  await client.setProgramScene('Écran');
  await client.startRecord();
  await client.stopRecord();
  const requests = ws.sent.filter(p => p.op === 6).map(p => p.d.requestType);
  assert.deepEqual(requests, ['GetSceneList', 'GetRecordStatus', 'SetCurrentProgramScene', 'StartRecord', 'StopRecord']);
  client.disconnect();
  assert.equal(client.connected, false);
  assert.equal(ws.closed, true);
  await assert.rejects(client.getScenes(), /non connecté/);
});

test('Un serveur OBS qui demande un mot de passe ne peut pas être identifié sans secret', async () => {
  class ProtectedOBS extends MockOBSWebSocket {
    constructor(url) {
      super(url);
      this.deliver = (packet) => {
        if (packet.op === 0) packet.d.authentication = { salt: 'a', challenge: 'b' };
        this.onmessage?.({ data: JSON.stringify(packet) });
      };
    }
  }
  const client = new OBSClient({ WebSocketClass: ProtectedOBS, cryptoAPI: webcrypto, timeoutMs: 1000 });
  await assert.rejects(client.connect(), /mot de passe/);
  assert.equal(client.connected, false);
});
