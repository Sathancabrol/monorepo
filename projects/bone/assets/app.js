import { loadPersona, createBrain } from './persona.js';

const CHANNELS = [
  { cat: 'Accueil', id: 'regles', name: 'règles', topic: 'Sois pas chiant. Ping Bone si t’ennuies.' },
  { cat: 'Accueil', id: 'annonces', name: 'annonces', topic: 'Satan parle. Les autres écoutent.' },
  { cat: 'Olympus', id: 'general', name: 'général', topic: 'Cour de récré. Bone habite ici.' },
  { cat: 'Olympus', id: 'memes', name: 'memes', topic: 'Construction paper only.' },
  { cat: 'Lab', id: 'watchtower', name: 'watchtower', topic: 'Globe 3D · /urgence · l’œil cyan' },
  { cat: 'Lab', id: 'cognitorium', name: 'cognitorium', topic: 'Visu cognitive. Pas un QI 2.0.' },
  { cat: 'Lab', id: 'hcsm', name: 'hcsm', topic: 'Human Cognitive State Model' },
  { cat: 'Chantier', id: 'travaux', name: 'travaux', topic: 'Bordures, enrobés, DICT, AIPR.' },
];

const QUICK = [
  { t: 'Salut Bone', l: 'salut' },
  { t: 'T’es qui ?', l: 'qui es-tu' },
  { t: 'Roast-moi', l: 'roast' },
  { t: 'Watchtower', l: 'watchtower' },
  { t: 'HCSM', l: 'hcsm' },
  { t: 'Épisode', l: 'épisode' },
  { t: 'Projets', l: 'projets' },
  { t: 'Aide', l: 'aide' },
];

const YOU = { name: 'Satan', sub: 'owner', av: null };
const BONE_AV = './assets/bone.png';

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

function nowStamp() {
  return new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
}

function el(html) {
  const t = document.createElement('template');
  t.innerHTML = html.trim();
  return t.content.firstElementChild;
}

function addMsg(box, { author, av, text, bot, time }) {
  const node = el(`
    <article class="msg">
      <img class="av" src="${av || BONE_AV}" alt="">
      <div>
        <div class="meta">${author}${bot ? '<span class="bot">BOT</span>' : ''}<time>${time || nowStamp()}</time></div>
        <div class="body"></div>
      </div>
    </article>`);
  node.querySelector('.body').textContent = text;
  box.appendChild(node);
  box.scrollTop = box.scrollHeight;
  return node;
}

function addSys(box, text) {
  const n = el(`<div class="sys">${text}</div>`);
  box.appendChild(n);
  box.scrollTop = box.scrollHeight;
}

async function main() {
  const data = await loadPersona('./persona.json');
  const brains = {};
  const brainOf = (id) => (brains[id] ||= createBrain(data));

  let channel = 'general';
  const msgsEl = $('#msgs');
  const typing = $('#typing');
  const stage = $('#stage');
  const input = $('#input');
  const topic = $('#topic');
  const chName = $('#ch-name');

  function renderChannels() {
    const list = $('#ch-list');
    list.innerHTML = '';
    let last = '';
    for (const c of CHANNELS) {
      if (c.cat !== last) {
        last = c.cat;
        list.appendChild(el(`<div class="cat">${c.cat}</div>`));
      }
      const b = el(`<button class="ch${c.id === channel ? ' on' : ''}" data-id="${c.id}"><span class="hash">#</span> ${c.name}</button>`);
      b.addEventListener('click', () => switchChannel(c.id));
      list.appendChild(b);
    }
  }

  function seed(id) {
    const box = msgsEl;
    box.innerHTML = '';
    const c = CHANNELS.find((x) => x.id === id);
    box.appendChild(el(`<div class="day">Aujourd’hui</div>`));
    addSys(box, `Bienvenue dans #${c.name} — ${c.topic}`);
    if (id === 'general') {
      addMsg(box, {
        author: 'Bone', av: BONE_AV, bot: true, time: nowStamp(),
        text: brainOf(id).opener('fr'),
      });
    } else if (id === 'regles') {
      addMsg(box, {
        author: 'Bone', av: BONE_AV, bot: true,
        text: "Règles d’Olympus : 1. sois pas chiant. 2. ping Bone. 3. touche pas aux rôles de Satan. 4. Kenny a le droit de mourir. 5. les PDF de bordures vont dans #travaux.",
      });
    } else if (id === 'watchtower') {
      addMsg(box, {
        author: 'Bone', av: BONE_AV, bot: true,
        text: "La tour. Globe, urgence, l’œil cyan. Moi j’suis l’autre mascotte. Celle qui parle. Tape watchtower.",
      });
    } else if (id === 'travaux') {
      addMsg(box, {
        author: 'Bone', av: BONE_AV, bot: true,
        text: "Ah. Le vrai fonds de commerce. Bordures, enrobés, DICT. Pose ta question, conducteur de travaux.",
      });
    }
  }

  function switchChannel(id) {
    channel = id;
    const c = CHANNELS.find((x) => x.id === id);
    chName.textContent = c.name;
    topic.textContent = c.topic;
    input.placeholder = `Message #${c.name}`;
    renderChannels();
    seed(id);
  }

  function talkOn(on) {
    stage.classList.toggle('talk', on);
  }

  async function boneSay(userText) {
    const b = brainOf(channel);
    typing.classList.add('on');
    talkOn(true);
    let out = null;
    try {
      const r = await fetch('/api/bone/chat', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ text: userText, channel, author: 'Satan' }),
      });
      if (r.ok) {
        const j = await r.json();
        if (j && j.text) out = j.text;
      }
    } catch (_) { /* preview statique : cerveau JS */ }
    if (!out) {
      const wait = Math.min(1800, 380 + String(userText || '').length * 12);
      await new Promise((res) => setTimeout(res, wait));
      out = b.reply(userText, 'Satan');
    }
    addMsg(msgsEl, { author: 'Bone', av: BONE_AV, bot: true, text: out });
    $('#stage-line').textContent = out.length > 72 ? `${out.slice(0, 70)}…` : out;
    typing.classList.remove('on');
    talkOn(false);
    return out;
  }

  $('#form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    input.value = '';
    addMsg(msgsEl, { author: YOU.name, av: BONE_AV, text });
    // use a generic human avatar color — keep bone.png only for Bone
    const last = msgsEl.querySelector('.msg:last-child img');
    if (last) {
      last.style.objectPosition = 'center';
      last.style.background = '#c41e3a';
      last.style.filter = 'hue-rotate(200deg) saturate(.6)';
    }
    let payload = text;
    if (/^!bone\s*/i.test(payload)) payload = payload.replace(/^!bone\s*/i, '');
    if (/^\/(\w+)/.test(payload)) {
      const cmd = payload.slice(1).split(/\s+/)[0].toLowerCase();
      const map = { aide: 'aide', help: 'aide', roast: 'roast', mood: 'mood', episode: 'épisode', projets: 'projets' };
      payload = map[cmd] || payload;
    }
    await boneSay(payload);
  });

  const quick = $('#quick');
  for (const q of QUICK) {
    const b = el(`<button type="button">${q.t}</button>`);
    b.addEventListener('click', () => {
      input.value = q.l;
      $('#form').dispatchEvent(new Event('submit', { cancelable: true }));
    });
    quick.appendChild(b);
  }

  renderChannels();
  switchChannel('general');

  $('#skip').addEventListener('click', enter);
  setTimeout(enter, 2800);
  let entered = false;
  function enter() {
    if (entered) return;
    entered = true;
    $('#intro').classList.add('gone');
    $('#app').classList.add('on');
    input.focus();
  }
}

main().catch((err) => {
  document.body.innerHTML = `<pre style="color:#faa;padding:24px">Bone a crash. Kenny aussi.\n${err}</pre>`;
});
