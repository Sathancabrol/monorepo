/* Bone — cerveau JS (playground). Miroir de persona.py */
export async function loadPersona(url = './persona.json') {
  const r = await fetch(url);
  if (!r.ok) throw new Error('persona.json introuvable');
  return r.json();
}

function strip(s) {
  return (s || '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/\p{Diacritic}/gu, '')
    .replace(/\s+/g, ' ')
    .trim();
}

const FR_HINTS = [' le ', ' la ', ' les ', ' un ', ' une ', ' des ', ' je ', ' tu ', ' on ', ' pas ', ' que ', ' et ', " c'est ", ' ça', ' ca ', 'oui', 'non', 'quoi', 'wesh', 'putain', 'salut', 'merci', 'chef', 'ouais'];
const EN_HINTS = [' the ', ' you ', ' are ', ' is ', ' and ', ' what ', ' who ', ' how ', 'hey', 'hello', 'thanks', 'please', "i'm "];

export function detectLang(text) {
  const t = ` ${strip(text)} `;
  let fr = 0, en = 0;
  for (const h of FR_HINTS) if (t.includes(h)) fr++;
  for (const h of EN_HINTS) if (t.includes(h)) en++;
  return en > fr + 1 ? 'en' : 'fr';
}

function score(textN, keys) {
  let s = 0;
  for (const k of keys) {
    const kn = strip(k);
    if (kn && textN.includes(kn)) s += Math.max(3, kn.length);
  }
  return s;
}

export function matchIntent(data, text) {
  const tn = ` ${strip(text)} `;
  let best = null, bestS = 0;
  for (const intent of data.intents) {
    const s = score(tn, intent.keys);
    if (s > bestS) { best = intent; bestS = s; }
  }
  return bestS < 3 ? null : best;
}

function pick(seq, avoid) {
  if (!seq || !seq.length) return 'Ouais.';
  const c = seq.filter((x) => x !== avoid);
  const bag = c.length ? c : seq;
  return bag[Math.floor(Math.random() * bag.length)];
}

export function createBrain(data) {
  const st = { mood: 'chill', last: null, history: [], quiet: false };

  function decorate(text) {
    const info = data.moods[st.mood] || data.moods.chill;
    const prefixes = info.prefix || [];
    if (prefixes.length && Math.random() < 0.45) {
      const p = prefixes[Math.floor(Math.random() * prefixes.length)];
      if (!text.startsWith(p)) return `${p} ${text}`;
    }
    return text;
  }

  function opener(lang = 'fr') {
    const bag = data.openers[lang] || data.openers.fr;
    return pick(bag);
  }

  function reply(text, author) {
    const raw = (text || '').trim();
    if (!raw) return opener();
    const lowered = strip(raw);
    if (['tg', 'silence', 'chut', 'quiet'].includes(lowered)) {
      st.quiet = true;
      return "Ok. J'me tais. Rappelle-moi avec !bone parle.";
    }
    if (['parle', 'speak', 'reviens'].includes(lowered)) {
      st.quiet = false;
      return "Ok. J'parle. Ça t'étonne ?";
    }
    const lang = detectLang(raw);
    const intent = matchIntent(data, raw);
    if (intent?.id === 'insult') st.mood = 'agace';
    else if (intent?.id === 'towelie') st.mood = 'high';
    else if (intent?.id === 'love' || intent?.id === 'thanks') st.mood = 'chill';
    else if (intent?.id === 'episode') st.mood = 'hype';
    else if (intent?.id === 'death') st.mood = 'mort';

    let textOut;
    if (intent) {
      const bag = intent[lang] || intent.fr || [];
      textOut = pick(bag, st.last);
    } else {
      let kn = null;
      for (const [key, blurb] of Object.entries(data.knowledge)) {
        if (lowered.includes(strip(key))) { kn = blurb; break; }
      }
      if (kn) {
        const wraps = lang === 'en'
          ? [kn, `Yeah. ${kn}`]
          : [`${kn} Voilà. J'ai lu le README. T'es fier ?`, `Ouais. ${kn}`, `${kn} Demande-moi le roast si tu veux la version méchante.`];
        textOut = pick(wraps, st.last);
      } else {
        textOut = pick(data.fallback[lang] || data.fallback.fr, st.last);
      }
    }
    if (author && Math.random() < 0.18 && intent && (intent.id === 'greet' || intent.id === 'how')) {
      textOut = `${author}. ${textOut}`;
    }
    textOut = decorate(textOut);
    st.last = textOut;
    st.history.push({ role: 'user', text: raw }, { role: 'bone', text: textOut });
    if (st.history.length > 16) st.history.splice(0, st.history.length - 16);
    return textOut;
  }

  return { reply, opener, state: st, setMood(m) { if (data.moods[m]) st.mood = m; } };
}
