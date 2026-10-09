/* Carré d'As — interface
   Pas de framework, pas de build : le fichier est servi tel quel. */

'use strict';

/* ------------------------------------------------------------------ outils */
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, c =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
const nl2br = s => esc(s).replace(/\n/g, '<br>');

async function api(path, opts = {}) {
  const o = { headers: {}, ...opts };
  if (o.body && typeof o.body === 'object') {
    o.headers['Content-Type'] = 'application/json';
    o.body = JSON.stringify(o.body);
  }
  const r = await fetch(path, o);
  const txt = await r.text();
  let data; try { data = txt ? JSON.parse(txt) : {}; } catch { data = { brut: txt }; }
  if (!r.ok) { throw new Error(data.erreur || data.message || ('HTTP ' + r.status)); }
  return data;
}
const get = p => api(p);
const post = (p, b) => api(p, { method: 'POST', body: b || {} });
const put = (p, b) => api(p, { method: 'PUT', body: b || {} });
const del = p => api(p, { method: 'DELETE' });

function euro(n) {
  if (n == null) return '—';
  return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR',
    maximumFractionDigits: 0 }).format(n);
}
function joli(d) {
  if (!d) return '';
  const m = String(d).match(/^(\d{4})-(\d{2})-(\d{2})/);
  return m ? `${m[3]}/${m[2]}/${m[1]}` : String(d);
}
function toast(msg, type = 'info') {
  const el = document.createElement('div');
  el.style.cssText = `position:fixed;bottom:22px;left:50%;transform:translateX(-50%);
    padding:11px 18px;border-radius:10px;z-index:99;font-size:13px;
    background:${type === 'erreur' ? '#2A0E17' : '#0F2422'};
    color:${type === 'erreur' ? '#FF8FA6' : '#7AFFD8'};
    border:1px solid ${type === 'erreur' ? '#5C1E31' : '#1E5C4C'}`;
  el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 3200);
}

/* -------------------------------------------------------------------- état */
const S = {
  vue: 'accueil',
  modules: [],
  sante: null,
  tableau: null,
  reu: { session: null, data: null, onglet: 'direct' },
  carto: { couches: [], groupes: [], points: [], territoire: null },
  cogni: { profils: [], refs: [], annuaire: [] },
  prev: { indicateurs: [], familles: [], scenarios: [], famille: '' },
  osint: { outils: [], categories: [], cas: [], casId: null, categorie: '' },
  systeme: { infos: null, maj: null, fichiers: [], config: null },
  ongletAside: 'journal',
};

const RAIL = [
  { id: 'accueil', icone: '◈', texte: 'Accueil' },
  { id: 'reunion', icone: '◎', texte: 'Réunion' },
  { id: 'carto', icone: '▦', texte: 'Cartographie' },
  { id: 'cognitorium', icone: '◍', texte: 'Cognitorium' },
  { id: 'prevision', icone: '◷', texte: 'Prévision' },
  { id: 'osint', icone: '⌘', texte: 'OSINT' },
];

/* ----------------------------------------------------------------- rendu */
function rendreRail() {
  $('#rail-items').innerHTML = RAIL.map(r =>
    `<button class="rail-item ${S.vue === r.id ? 'actif' : ''}" data-action="vue" data-vue="${r.id}">
       <span class="ico">${r.icone}</span><span class="texte">${r.texte}</span></button>`).join('');
}

const VUES = { accueil, reunion, carto, cognitorium, prevision, osint, systeme };

async function render() {
  rendreRail();
  $$('.rail-item').forEach(b => b.classList.toggle('actif', b.dataset.vue === S.vue));
  const main = $('#main');
  main.classList.add('charge');
  try {
    const html = await VUES[S.vue]();
    main.innerHTML = html;
    main.scrollTop = 0;
  } catch (e) {
    main.innerHTML = `<div class="titre-page"><h1>Erreur</h1></div>
      <div class="avertissement">${esc(e.message)}</div>`;
  } finally {
    main.classList.remove('charge');
  }
}

async function aller(vue) {
  S.vue = vue;
  await render();
}

/* ================================================================ ACCUEIL */
async function accueil() {
  const [sante, tableau, modules, sessions] = await Promise.all([
    get('/api/health'), get('/api/tableau'), get('/api/modules'), get('/api/meeting')]);
  S.sante = sante; S.tableau = tableau; S.modules = modules.modules;
  const t = tableau;
  const terr = (await get('/api/carto/territoire')).territoire || {};

  const cartes = [
    ['Réunions', t.reunions.total || 0, `${t.reunions.en_cours || 0} en cours · ${t.reunions.documents || 0} documents`],
    ['Actions ouvertes', t.reunions.actions_ouvertes || 0, `${t.reunions.decisions || 0} décisions enregistrées`],
    ['Points cartographiés', t.carto.points || 0, `${t.carto.vues || 0} vue(s) mémorisée(s)`],
    ['Profils', t.profils.total || 0, `${t.profils.references || 0} références indexées`],
    ['Scénarios', t.prevision.scenarios || 0, `${t.prevision.valeurs || 0} valeurs saisies`],
    ['Cas OSINT', t.osint.cas || 0, `${t.osint.preuves || 0} élément(s) versé(s)`],
  ];

  const enCours = (sessions.sessions || []).filter(s => s.statut === 'en_cours');
  const recentes = (sessions.sessions || []).slice(0, 6);

  return `
  <div class="titre-page">
    <h1>${esc(terr.nom || 'Carré d\'As')}</h1>
    <div class="actions">
      <button class="primaire" data-action="nouvelle-reunion">＋ Nouvelle réunion</button>
    </div>
  </div>

  ${enCours.length ? `<div class="avertissement">
    <b>Réunion en cours :</b> ${esc(enCours[0].titre)}
    <button class="petit" data-action="ouvrir-reunion" data-id="${esc(enCours[0].id)}" style="margin-left:10px">Reprendre</button>
  </div>` : ''}

  <section class="bloc">
    <div class="grille g4">
      ${cartes.map(([c, v, s]) => `<div class="carte titre-grand">
        <div class="cle">${esc(c)}</div><div class="valeur">${v}</div>
        <div class="sous">${esc(s)}</div></div>`).join('')}
    </div>
  </section>

  <section class="bloc">
    <h2>Territoire de référence</h2>
    <div class="carte">
      <div class="grille g4">
        <div><div class="cle">Communes</div><div class="valeur" style="font-size:19px">${(terr.communes || []).length}</div></div>
        <div><div class="cle">Population</div><div class="valeur" style="font-size:19px">${(terr.population || 0).toLocaleString('fr-FR')}</div></div>
        <div><div class="cle">Couches disponibles</div><div class="valeur" style="font-size:19px">${terr.couches_disponibles ?? '—'}</div></div>
        <div><div class="cle">Documents produits</div><div class="valeur" style="font-size:19px">${t.documents || 0}</div></div>
      </div>
      ${terr.communes ? `<div style="margin-top:14px;display:flex;flex-wrap:wrap;gap:6px">
        ${terr.communes.map(c => `<span class="tag gris">${esc(c)}</span>`).join('')}</div>` : ''}
    </div>
  </section>

  <div class="grille g2">
    <section class="bloc">
      <h2>Réunions récentes</h2>
      ${recentes.length ? `<div class="liste">${recentes.map(s => `
        <div class="ligne cliquable" data-action="ouvrir-reunion" data-id="${esc(s.id)}">
          <div class="principal">
            <div class="nom elide">${esc(s.titre)}</div>
            <div class="meta">${esc(joli(s.date))} · ${esc(s.lieu || '—')} ·
              ${(s.decisions || []).length} déc. · ${(s.actions || []).length} act.</div>
          </div>
          <span class="tag ${s.statut === 'en_cours' ? 'ris' : 'gris'}">${esc(s.statut)}</span>
        </div>`).join('')}</div>`
        : `<div class="vide">Aucune réunion — créez la première.</div>`}
    </section>

    <section class="bloc">
      <h2>État des modules</h2>
      <div class="liste">
        ${(S.modules || []).map(m => `
          <div class="ligne">
            <div class="principal">
              <div class="nom">${esc(m.icone)} ${esc(m.titre)}</div>
              <div class="meta elide">${esc(m.resume || '')}</div>
            </div>
            <span class="tag ${m.charge === false ? 'ris' : 'deci'}">${m.charge === false ? 'en échec' : 'actif'}</span>
          </div>`).join('')}
      </div>
      <div class="note-info" style="margin-top:12px">
        Moteur de rédaction : <b>${esc((sante.modele || {}).provider_actif || 'aucun')}</b>.
        ${(sante.modele || {}).deterministe
          ? 'Les documents sont produits par gabarits déterministes : ils sortent quoi qu\'il arrive, sans réseau ni modèle.'
          : 'Le modèle enrichit l\'extraction ; le repli déterministe reste actif en cas de panne.'}
      </div>
    </section>
  </div>`;
}

/* ================================================================ RÉUNION */
async function reunion() {
  if (!S.reu.session) return listeReunions();
  const id = S.reu.session;
  const { session: s } = await get('/api/meeting/' + id);
  S.reu.data = s;
  const sug = await get('/api/meeting/' + id + '/suggestions?statut=attente');
  S.reu.suggestions = sug.suggestions || [];

  const duree = (s.transcript || []).length;
  const enCours = s.statut === 'en_cours';
  const onglets = [['direct', 'Direct'], ['decisions', `Décisions ${(s.decisions || []).length}`],
    ['actions', `Actions ${(s.actions || []).length}`], ['budget', `Budget ${euro(totalBudget(s))}`],
    ['planning', `Planning ${(s.planning || []).length}`], ['documents', `Documents ${(s.documents || []).length}`]];

  return `
  <div class="titre-page">
    <h1>${esc(s.titre)}</h1>
    <div class="actions">
      <button class="fantome" data-action="vue" data-vue="reunion" data-reset="1">‹ Toutes les réunions</button>
      ${enCours
        ? `<button data-action="statut" data-statut="suspendu">⏸ Suspendre</button>
           <button class="danger" data-action="statut" data-statut="close">■ Clore</button>`
        : `<button class="primaire" data-action="statut" data-statut="en_cours">● Démarrer</button>`}
    </div>
  </div>

  <div class="reu-tete">
    <div>
      <div class="titre">${esc(s.titre)}</div>
      <div class="infos">
        <span>${esc(joli(s.date))} ${esc(s.heure || '')}</span>
        <span>${esc(s.lieu || '—')}</span>
        <span>${esc(s.type || '')}</span>
        ${enCours ? '<span class="pastille-live"><i class="pt"></i>en direct</span>'
                  : `<span class="tag gris">${esc(s.statut)}</span>`}
      </div>
    </div>
    <div class="actions">
      <span class="pastille"><i class="pt"></i>${duree} prise(s) de parole</span>
      <span class="pastille"><i class="pt"></i>${(s.compteur || {}).mots || 0} mots</span>
    </div>
  </div>

  <div class="onglets" style="margin-bottom:16px">
    ${onglets.map(([k, l]) => `<button class="onglet ${S.reu.onglet === k ? 'actif' : ''}"
      data-action="onglet-reu" data-onglet="${k}">${esc(l)}</button>`).join('')}
  </div>

  ${ongletReunion()}`;
}

function totalBudget(s) {
  return (s.budget || []).reduce((n, b) => n + (Number(b.total) || 0), 0);
}

function ongletReunion() {
  const s = S.reu.data, o = S.reu.onglet;
  if (o === 'direct') return ongletDirect(s);
  if (o === 'decisions') return ongletItems(s, 'decision');
  if (o === 'actions') return ongletItems(s, 'action');
  if (o === 'budget') return ongletBudget(s);
  if (o === 'planning') return ongletPlanning(s);
  return ongletDocuments(s);
}

function ongletDirect(s) {
  const enCours = s.statut === 'en_cours';
  return `
  <div class="grille g2" style="grid-template-columns:1.15fr .85fr">
    <div>
      <section class="bloc">
        <h2>Capture</h2>
        <div class="note-info">Collez ou dictez ce qui se dit. Chaque phrase est analysée
          immédiatement : les décisions et actions détectées tombent dans le bac,
          à droite. Rien n'entre dans le compte rendu sans votre accord.</div>
        <div class="capture">
          <textarea id="zone-capture" placeholder="« On décide de lancer l'étude de faisabilité avant fin novembre, Martin s'en charge… »"></textarea>
          <div style="display:flex;flex-direction:column;gap:9px">
            <label class="champ"><span>Qui parle</span>
              <input id="zone-locuteur" list="liste-participants" placeholder="Locuteur"></label>
            <datalist id="liste-participants">
              ${(s.participants || []).map(p => `<option value="${esc(p)}">`).join('')}
            </datalist>
            <button class="primaire" data-action="pousser">↓ Analyser</button>
          </div>
        </div>
        <div class="rangee" style="margin-top:9px">
          <button data-action="noter" class="sans-flex">＋ Note manuscrite</button>
          <button data-action="analyser" class="sans-flex" title="Relancer le modèle sur le verbatim">✦ Analyser</button>
        </div>
      </section>

      <section class="bloc">
        <h2>Verbatim <span class="dim">(${(s.transcript || []).length})</span></h2>
        <div class="liste" style="max-height:260px;overflow-y:auto">
          ${(s.transcript || []).length
            ? [...s.transcript].reverse().map(t => `
              <div class="ligne">
                <div class="principal">
                  <div class="meta mono">${esc(t.t || '')} ${t.locuteur ? '· <b>' + esc(t.locuteur) + '</b>' : ''}</div>
                  <div class="nom" style="font-weight:400">${esc(t.texte)}</div>
                </div></div>`).join('')
            : '<div class="vide">Rien encore.</div>'}
        </div>
      </section>
    </div>

    <div>
      <section class="bloc">
        <h2>Bac à suggestions <span class="dim">(${(S.reu.suggestions || []).length})</span></h2>
        <div class="liste bac">
          ${(S.reu.suggestions || []).length
            ? S.reu.suggestions.map(g => carteSuggestion(g)).join('')
            : '<div class="vide">Rien en attente. Le bac se remplit au fil de la réunion.</div>'}
        </div>
      </section>

      <section class="bloc">
        <h2>Points de vigilance</h2>
        ${(s.risques || []).length
          ? `<div class="liste">${s.risques.map(r => `
              <div class="ligne"><div class="principal"><div class="nom" style="font-weight:400">${esc(r.texte)}</div></div>
              <button class="petit danger" data-action="suppr-item" data-kind="risque" data-id="${esc(r.id)}">×</button></div>`).join('')}</div>`
          : '<div class="vide">Aucun.</div>'}
      </section>

      <section class="bloc">
        <h2>Participants</h2>
        <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:9px">
          ${(s.participants || []).length
            ? s.participants.map(p => `<span class="tag">${esc(p)}</span>`).join('')
            : '<span class="dim">Aucun renseigné</span>'}
        </div>
        <div class="rangee">
          <input id="ajout-participant" placeholder="Ajouter un participant">
          <button class="sans-flex" data-action="ajouter-participant">＋</button>
        </div>
      </section>
    </div>
  </div>`;
}

function carteSuggestion(g) {
  const cls = { decision: 'deci', action: 'act', risque: 'ris', question: 'qst' }[g.kind] || 'gris';
  const nom = { decision: 'décision', action: 'action', risque: 'risque', question: 'question' }[g.kind] || g.kind;
  return `<div class="suggestion attente">
    <div class="corps">
      <span class="tag ${cls}">${esc(nom)}</span>
      <span class="confiance">${Math.round((g.confiance || 0) * 100)} %</span>
      <div class="txt" style="margin-top:6px">${esc(g.texte)}</div>
      <div class="qui">${[
        g.responsable ? 'qui : ' + esc(g.responsable) : '',
        g.echeance ? 'pour : ' + esc(joli(g.echeance)) : '',
        g.montant ? 'montant : ' + euro(g.montant) : '',
        g.origine === 'modele' ? 'proposé par le modèle' : ''
      ].filter(Boolean).join(' · ') || '<span class="dim">ni responsable ni échéance détectés</span>'}</div>
    </div>
    <div class="boutons">
      <button class="petit primaire" data-action="accepter" data-id="${esc(g.id)}" title="Accepter">✓</button>
      <button class="petit" data-action="refuser" data-id="${esc(g.id)}" title="Refuser">✕</button>
    </div>
  </div>`;
}

function ongletItems(s, kind) {
  const liste = kind === 'action' ? (s.actions || []) : (s.decisions || []);
  const titre = kind === 'action' ? 'Actions' : 'Décisions';
  return `
  <section class="bloc">
    <h2>${titre} <span class="dim">(${liste.length})</span></h2>
    <div class="table-enveloppe">
      <table>
        <thead><tr>
          ${kind === 'action'
            ? '<th>Action</th><th>Responsable</th><th>Échéance</th><th>Montant</th><th>Statut</th>'
            : '<th>Décision</th><th>Responsable</th><th>Échéance</th>'}
          <th></th></tr></thead>
        <tbody>
          ${liste.length ? liste.map(a => `<tr>
            <td>${esc(a.texte)}</td>
            <td><input value="${esc(a.responsable || '')}" data-modif="${esc(kind)}" data-id="${esc(a.id)}" data-champ="responsable" style="min-width:110px"></td>
            <td><input type="date" value="${esc(String(a.echeance || '').slice(0, 10))}" data-modif="${esc(kind)}" data-id="${esc(a.id)}" data-champ="echeance"></td>
            ${kind === 'action' ? `<td class="mono">${a.montant ? euro(a.montant) : '—'}</td>
              <td><select data-modif="action" data-id="${esc(a.id)}" data-champ="statut">
                ${['à faire', 'en cours', 'fait', 'reporté'].map(v =>
                  `<option ${a.statut === v ? 'selected' : ''}>${v}</option>`).join('')}
              </select></td>` : ''}
            <td><button class="petit danger" data-action="suppr-item" data-kind="${esc(kind)}" data-id="${esc(a.id)}">×</button></td>
          </tr>`).join('')
            : `<tr><td colspan="5"><div class="vide">Aucun élément. Acceptez une suggestion ou ajoutez-en un.</div></td></tr>`}
        </tbody>
      </table>
    </div>
    <div class="rangee" style="margin-top:12px;align-items:flex-end">
      <input id="texte-item" placeholder="${kind === 'action' ? 'Nouvelle action…' : 'Nouvelle décision…'}" style="flex:3">
      <input id="resp-item" placeholder="Responsable">
      <input type="date" id="echeance-item" style="max-width:170px">
      <button class="primaire sans-flex" data-action="ajouter-item" data-kind="${esc(kind)}">＋ Ajouter</button>
    </div>
  </section>`;
}

function ongletBudget(s) {
  const lignes = s.budget || [];
  return `
  <section class="bloc">
    <h2>Enveloppe <span class="dim">(${euro(totalBudget(s))})</span></h2>
    ${lignes.length ? `<div class="table-enveloppe"><table>
      <thead><tr><th>Poste</th><th>Catégorie</th><th>Qté</th><th>Coût unitaire</th><th>Total</th><th></th></tr></thead>
      <tbody>${lignes.map(b => `<tr>
        <td>${esc(b.libelle)}</td><td>${esc(b.categorie)}</td>
        <td class="mono">${esc(b.quantite)} ${esc(b.unite || '')}</td>
        <td class="mono">${euro(b.cout_unitaire)}</td>
        <td class="mono"><b>${euro(b.total)}</b></td>
        <td><button class="petit danger" data-action="suppr-budget" data-id="${esc(b.id)}">×</button></td>
      </tr>`).join('')}</tbody></table></div>`
      : '<div class="vide">Aucun poste. Un montant prononcé en séance est détecté automatiquement.</div>'}
    <div class="grille-form" style="margin-top:14px">
      <label class="champ"><span>Poste</span><input id="bud-libelle" placeholder="Étude de faisabilité"></label>
      <label class="champ"><span>Catégorie</span><select id="bud-categorie">
        <option>Fonctionnement</option><option>Investissement</option>
        <option>Étude</option><option>Travaux</option><option>Prestation</option></select></label>
      <label class="champ"><span>Quantité</span><input id="bud-qte" type="number" value="1" step="0.5"></label>
      <label class="champ"><span>Unité</span><input id="bud-unite" value="forfait"></label>
      <label class="champ"><span>Coût unitaire €</span><input id="bud-cout" type="number" step="1"></label>
      <label class="champ"><span>Financeur</span><input id="bud-financeur" placeholder="Agglo / État / Fonds vert…"></label>
    </div>
    <button class="primaire" data-action="ajouter-budget">＋ Ajouter le poste</button>
  </section>`;
}

function ongletPlanning(s) {
  const taches = s.planning || [];
  return `
  <section class="bloc">
    <h2>Calendrier</h2>
    ${taches.length ? `<div class="table-enveloppe"><table>
      <thead><tr><th>Tâche</th><th>Début</th><th>Fin</th><th>Responsable</th><th>Avancement</th><th></th></tr></thead>
      <tbody>${taches.map(t => `<tr>
        <td>${esc(t.label)}</td><td class="mono">${esc(joli(t.debut))}</td>
        <td class="mono">${esc(joli(t.fin))}</td><td>${esc(t.responsable || '—')}</td>
        <td class="mono">${Math.round(t.avancement || 0)} %</td>
        <td><button class="petit danger" data-action="suppr-tache" data-id="${esc(t.id)}">×</button></td>
      </tr>`).join('')}</tbody></table></div>`
      : '<div class="vide">Aucune tâche datée.</div>'}
    <div class="grille-form" style="margin-top:14px">
      <label class="champ"><span>Tâche</span><input id="tch-label" placeholder="Consultation des PPA"></label>
      <label class="champ"><span>Début</span><input id="tch-debut" type="date"></label>
      <label class="champ"><span>Fin</span><input id="tch-fin" type="date"></label>
      <label class="champ"><span>Responsable</span><input id="tch-resp"></label>
      <label class="champ"><span>Avancement %</span><input id="tch-av" type="number" value="0" min="0" max="100"></label>
    </div>
    <button class="primaire" data-action="ajouter-tache">＋ Ajouter la tâche</button>
  </section>`;
}

const GABARITS = [
  ['recap', 'Compte rendu', 'Le document de référence, prêt à envoyer.', ['md', 'html', 'docx', 'txt']],
  ['note', 'Note de synthèse', 'Objet, contexte, analyse, propositions.', ['md', 'html', 'docx']],
  ['deliberation', 'Projet de délibération', 'Vu / Considérant / Articles — à relecture du service.', ['md', 'docx', 'html']],
  ['courrier', 'Courrier', 'Lettre de suite adressée à un partenaire.', ['md', 'docx', 'html']],
  ['presentation', 'Présentation', 'Diaporama projetable, généré depuis la séance.', ['pptx', 'html']],
  ['planning', 'Planning', 'Échéancier, diagramme de Gantt.', ['svg', 'csv', 'html']],
  ['budget', 'Budget', 'Tableau des postes et total.', ['csv', 'html', 'docx']],
];

function ongletDocuments(s) {
  const docs = s.documents || [];
  return `
  <section class="bloc">
    <h2>Générer</h2>
    <div class="grille g3">
      ${GABARITS.map(([id, nom, desc, fmts]) => `
        <div class="carte">
          <div class="cle">${esc(nom)}</div>
          <div style="font-size:12.5px;color:var(--dim);margin:6px 0 11px">${esc(desc)}</div>
          <div style="display:flex;flex-wrap:wrap;gap:6px">
            ${fmts.map(f => `<button class="petit" data-action="generer"
              data-gabarit="${id}" data-format="${f}">${esc(f)}</button>`).join('')}
          </div>
        </div>`).join('')}
    </div>
  </section>
  <section class="bloc">
    <h2>Documents produits <span class="dim">(${docs.length})</span></h2>
    ${docs.length ? `<div class="docs-liste">${[...docs].reverse().map(d => `
      <div class="doc-item">
        <span class="ext">${esc(d.format)}</span>
        <div class="principal" style="flex:1;min-width:0">
          <div class="elide">${esc(d.titre || d.nom)}</div>
          <div class="meta" style="font-size:11.5px;color:var(--dim)">${esc(d.cree_le || '')} · ${(d.taille / 1024).toFixed(0)} Ko</div>
        </div>
        <a class="bouton petit" href="/api/fichiers/${esc(d.nom)}" target="_blank">Ouvrir</a>
        <a class="bouton petit" href="/api/fichiers/${esc(d.nom)}?dl=1">↓</a>
      </div>`).join('')}</div>`
      : '<div class="vide">Aucun document généré pour cette réunion.</div>'}
  </section>`;
}

async function listeReunions() {
  const { sessions } = await get('/api/meeting');
  const terr = await get('/api/carto/territoire');
  return `
  <div class="titre-page">
    <h1>Réunions</h1>
    <div class="actions"><button class="primaire" data-action="nouvelle-reunion">＋ Nouvelle réunion</button></div>
  </div>
  <section class="bloc">
    <div class="carte">
      <div class="cle">Nouvelle réunion</div>
      <div class="grille-form" style="margin-top:10px">
        <label class="champ"><span>Titre</span><input id="nv-titre" placeholder="Comité de pilotage — Frange Sud"></label>
        <label class="champ"><span>Lieu</span><input id="nv-lieu" placeholder="Sète"></label>
        <label class="champ"><span>Date</span><input id="nv-date" type="date" value="${new Date().toISOString().slice(0, 10)}"></label>
        <label class="champ"><span>Type</span><select id="nv-type">
          <option>réunion de travail</option><option>comité de pilotage</option>
          <option>conseil communautaire</option><option>atelier de concertation</option>
          <option>entretien</option></select></label>
        <label class="champ"><span>Structure</span><input id="nv-organisme" value="${esc((terr.territoire || {}).nom || '')}"></label>
      </div>
      <label class="champ"><span>Ordre du jour (une ligne par point)</span>
        <textarea id="nv-odj" placeholder="Point 1 : …"></textarea></label>
      <label class="champ"><span>Participants (une ligne par personne)</span>
        <textarea id="nv-participants"></textarea></label>
      <button class="primaire" data-action="creer-reunion">Créer et ouvrir</button>
    </div>
  </section>
  <section class="bloc">
    <h2>Toutes les réunions <span class="dim">(${sessions.length})</span></h2>
    ${sessions.length ? `<div class="liste">${sessions.map(s => `
      <div class="ligne cliquable" data-action="ouvrir-reunion" data-id="${esc(s.id)}">
        <div class="principal">
          <div class="nom elide">${esc(s.titre)}</div>
          <div class="meta">${esc(joli(s.date))} · ${esc(s.lieu || '—')} ·
            ${(s._resume || {}).segments || 0} prises · ${(s._resume || {}).decisions || 0} déc. ·
            ${(s._resume || {}).documents || 0} doc.</div>
        </div>
        <span class="tag ${s.statut === 'en_cours' ? 'ris' : s.statut === 'close' ? 'gris' : 'act'}">${esc(s.statut)}</span>
        <button class="petit danger" data-action="suppr-reunion" data-id="${esc(s.id)}">×</button>
      </div>`).join('')}</div>`
      : '<div class="vide">Aucune réunion enregistrée.</div>'}
  </section>`;
}

/* =========================================================== CARTOGRAPHIE */
async function carto() {
  const [couches, groupes, points, territoire] = await Promise.all([
    get('/api/carto/couches'), get('/api/carto/groupes'),
    get('/api/carto/points'), get('/api/carto/territoire')]);
  S.carto = { couches: couches.couches, groupes: groupes.groupes,
              points: points.points, territoire };

  return `
  <div class="titre-page">
    <h1>Cartographie</h1>
    <div class="actions">
      <button data-action="sauver-vue">Mémoriser la vue</button>
    </div>
  </div>
  <div class="note-info">
    Le catalogue ci-dessous rassemble les couches territoriales réellement utiles
    sur le Bassin de Thau, avec leur licence vérifiée. Le moteur 3D complet
    (Cesium) vit dans <span class="mono">projects/watchtower</span> et viendra
    s'y brancher. <b>Rappel :</b> Mapbox GL JS v2 est propriétaire — on reste sur
    MapLibre (BSD-3).
  </div>

  <div class="grille g4" style="margin-bottom:22px">
    <div class="carte"><div class="cle">Couches référencées</div><div class="valeur">${couches.total}</div></div>
    <div class="carte"><div class="cle">Points d'observation</div><div class="valeur">${points.points.length}</div></div>
    <div class="carte"><div class="cle">Communes couvertes</div><div class="valeur">${(territoire.territoire.communes || []).length}</div></div>
    <div class="carte"><div class="cle">Moteur 3D</div><div class="valeur" style="font-size:13px">${esc(territoire.moteur_3d)}</div></div>
  </div>

  ${(S.carto.groupes || []).map(g => {
    const sel = (S.carto.couches || []).filter(c => c.groupe === g.id);
    if (!sel.length) return '';
    return `<section class="bloc">
      <h2>${esc(g.nom)} <span class="dim">(${sel.length})</span></h2>
      <div class="liste">${sel.map(c => `
        <div class="ligne">
          <div class="principal">
            <div class="nom">${esc(c.nom)}
              <span class="tag ${c.risque === 'fort' ? 'ris' : c.risque === 'moyen' ? 'act' : 'deci'}">${esc(c.licence)}</span>
            </div>
            <div class="meta" style="margin-top:4px">${esc(c.usage || '')}</div>
            <div class="meta mono" style="margin-top:3px">${esc(c.source || '')}</div>
          </div>
          <label style="flex:0 0 auto"><input type="checkbox" data-couche="${esc(c.id)}"
            ${c.active ? 'checked' : ''}> </label>
        </div>`).join('')}</div>
    </section>`;
  }).join('')}

  <section class="bloc">
    <h2>Points d'observation</h2>
    <div class="grille-form" style="margin-bottom:12px">
      <label class="champ"><span>Nom</span><input id="pt-nom" placeholder="Frange Sud — îlot A"></label>
      <label class="champ"><span>Latitude</span><input id="pt-lat" placeholder="43.44"></label>
      <label class="champ"><span>Longitude</span><input id="pt-lon" placeholder="3.75"></label>
      <label class="champ"><span>Commune</span><input id="pt-commune" list="liste-communes">
        <datalist id="liste-communes">${(territoire.territoire.communes || []).map(c =>
          `<option value="${esc(c)}">`).join('')}</datalist></label>
      <label class="champ"><span>Description</span><input id="pt-desc"></label>
      <div style="display:flex;align-items:flex-end">
        <button class="primaire" data-action="ajouter-point">＋ Ajouter</button></div>
    </div>
    ${S.carto.points.length ? `<div class="table-enveloppe"><table>
      <thead><tr><th>Point</th><th>Commune</th><th>Lat / Lon</th><th>État</th><th></th></tr></thead>
      <tbody>${S.carto.points.map(p => `<tr>
        <td>${esc(p.nom)}<div class="meta" style="font-size:11.5px;color:var(--dim)">${esc(p.description || '')}</div></td>
        <td>${esc(p.commune || '—')}</td>
        <td class="mono">${esc(p.lat)}, ${esc(p.lon)}</td>
        <td><span class="tag gris">${esc(p.etat || 'à vérifier')}</span></td>
        <td><button class="petit danger" data-action="suppr-point" data-id="${esc(p.id)}">×</button></td>
      </tr>`).join('')}</tbody></table></div>`
      : '<div class="vide">Aucun point.</div>'}
  </section>`;
}

/* ============================================================ COGNITORIUM */
async function cognitorium() {
  const [profils, refs, annuaire] = await Promise.all([
    get('/api/cognitorium/profils'), get('/api/cognitorium/references'),
    get('/api/cognitorium/annuaire')]);
  S.cogni = { profils: profils.profils, refs: refs.references, annuaire: annuaire.annuaire };

  return `
  <div class="titre-page">
    <h1>Cognitorium</h1>
    <div class="actions">
      <input id="rech-profil" placeholder="Rechercher…" style="width:220px"
        oninput="if(event.target.value.length>1)location.hash='#x'">
      <button data-action="indexer">Indexer un dossier</button>
    </div>
  </div>

  <div class="grille g2">
    <section class="bloc">
      <h2>Profils <span class="dim">(${S.cogni.profils.length})</span></h2>
      <div class="carte" style="margin-bottom:12px">
        <div class="grille-form">
          <label class="champ"><span>Nom</span><input id="pf-nom"></label>
          <label class="champ"><span>Prénom</span><input id="pf-prenom"></label>
          <label class="champ"><span>Rôle</span><input id="pf-role" placeholder="Directrice de cabinet"></label>
          <label class="champ"><span>Structure</span><input id="pf-structure"></label>
          <label class="champ"><span>Commune</span><input id="pf-commune"></label>
          <label class="champ"><span>Type</span><select id="pf-type">
            <option value="individu">Individu</option><option value="structure">Structure</option>
            <option value="partenaire">Partenaire</option></select></label>
          <label class="champ"><span>Courriel</span><input id="pf-courriel"></label>
          <label class="champ"><span>Tags (virgules)</span><input id="pf-tags" placeholder="élu, mobilité"></label>
        </div>
        <button class="primaire" data-action="creer-profil">＋ Créer la fiche</button>
      </div>
      ${S.cogni.profils.length ? `<div class="liste">${S.cogni.profils.map(p => `
        <div class="ligne">
          <div class="principal">
            <div class="nom">${esc((p.prenom + ' ' + p.nom).trim() || p.structure)}
              <span class="tag gris">${esc(p.type)}</span></div>
            <div class="meta">${[p.role, p.structure, p.commune].filter(Boolean).map(esc).join(' · ')}</div>
          </div>
          <button class="petit danger" data-action="suppr-profil" data-id="${esc(p.id)}">×</button>
        </div>`).join('')}</div>` : '<div class="vide">Aucun profil.</div>'}
    </section>

    <section class="bloc">
      <h2>État de l'art <span class="dim">(${S.cogni.refs.length})</span></h2>
      <div class="note-info">L'indexeur parcourt les dossiers déjà présents dans le
        dépôt (COGNITORIUM, psychologie, mémoires) et les rend interrogeables.</div>
      <div class="rangee" style="margin-bottom:12px">
        <input id="idx-racine" value="projects/COGNITORIUM" style="flex:2">
        <input id="idx-domaine" placeholder="domaine" value="cognitorium">
        <button class="sans-flex" data-action="indexer">Indexer</button>
      </div>
      ${S.cogni.refs.length ? `<div class="liste" style="max-height:420px;overflow-y:auto">
        ${S.cogni.refs.slice(0, 120).map(r => `
        <div class="ligne"><div class="principal">
          <div class="nom elide" style="font-weight:400">${esc(r.titre)}</div>
          <div class="meta">${esc(r.domaine || '')} · ${esc(r.type || '')}
            ${r.chemin ? ' · <span class="mono">' + esc(r.chemin) + '</span>' : ''}</div>
        </div>
        <button class="petit danger" data-action="suppr-ref" data-id="${esc(r.id)}">×</button></div>`).join('')}
      </div>` : '<div class="vide">Aucune référence indexée.</div>'}
    </section>
  </div>`;
}

/* ============================================================== PRÉVISION */
async function prevision() {
  const [familles, inds, scen] = await Promise.all([
    get('/api/prevision/familles'), get('/api/prevision/indicateurs'),
    get('/api/prevision/scenarios')]);
  S.prev = { familles: familles.familles, indicateurs: inds.indicateurs,
             scenarios: scen.scenarios };

  const parFamille = f => (S.prev.indicateurs || []).filter(i => i.famille === f);
  const couverture = inds.renseignes + ' / ' + inds.total;

  return `
  <div class="titre-page">
    <h1>Prévision</h1>
    <div class="actions">
      <span class="pastille"><i class="pt"></i>${esc(couverture)} renseignés</span>
      <button class="primaire" data-action="generer-prevision">✦ Note de prévision</button>
    </div>
  </div>
  <div class="note-info">
    Aucun chiffre n'est inventé : un indicateur non collecté reste marqué
    <b>à collecter</b> et la note de prévision signale explicitement les lacunes.
    C'est ce qui rend le document défendable devant une collectivité.
  </div>

  ${S.prev.familles.map(f => {
    const sel = parFamille(f.id);
    if (!sel.length) return '';
    return `<section class="bloc">
      <h2>${esc(f.nom)} — <span class="dim" style="text-transform:none;letter-spacing:0">${esc(f.question)}</span></h2>
      <div class="table-enveloppe"><table>
        <thead><tr><th>Indicateur</th><th>Valeur</th><th>Tendance</th><th>Source</th><th>Licence</th><th>Confiance</th></tr></thead>
        <tbody>${sel.map(i => `<tr>
          <td>${esc(i.nom)}<div class="meta" style="font-size:11.5px;color:var(--dim)">${esc(i.interpretation || '')}</div></td>
          <td><input class="mono" style="min-width:90px" value="${i.valeur == null ? '' : esc(i.valeur)}"
                placeholder="—" data-ind="${esc(i.id)}" data-unite="${esc(i.unite || '')}"
                onchange="saisirIndicateur(this)">
             <div class="meta" style="font-size:11px;color:var(--dim-2)">${esc(i.unite || '')}</div></td>
          <td class="mono">${esc(i.tendance.sens)}${i.tendance.variation != null ? ' ' + (i.tendance.variation > 0 ? '+' : '') + i.tendance.variation + ' %' : ''}</td>
          <td>${esc(i.source)}<div class="meta mono" style="font-size:11px;color:var(--dim-2)">${esc((i.url || '').replace(/^https?:\/\//, '').slice(0, 40))}</div></td>
          <td><span class="tag gris">${esc(i.licence)}</span></td>
          <td><span class="tag ${i.confiance === 'haute' ? 'deci' : i.confiance === 'faible' ? 'ris' : 'act'}">${esc(i.confiance)}</span></td>
        </tr>`).join('')}</tbody></table></div>
    </section>`;
  }).join('')}

  <section class="bloc">
    <h2>Scénarios</h2>
    <div class="grille-form" style="margin-bottom:12px">
      <label class="champ"><span>Nom</span><input id="sc-nom" placeholder="Récession prolongée"></label>
      <label class="champ"><span>Horizon</span><input id="sc-horizon" value="12 mois"></label>
      <label class="champ"><span>Probabilité %</span><input id="sc-proba" type="number" min="0" max="100"></label>
      <label class="champ"><span>Hypothèses (une par ligne)</span><textarea id="sc-hyp"></textarea></label>
      <label class="champ"><span>Impacts (une par ligne)</span><textarea id="sc-imp"></textarea></label>
      <label class="champ"><span>Signaux à surveiller</span><textarea id="sc-sig"></textarea></label>
    </div>
    <button class="primaire" data-action="creer-scenario">＋ Ajouter le scénario</button>
    ${S.prev.scenarios.length ? `<div class="liste" style="margin-top:14px">
      ${S.prev.scenarios.map(s => `<div class="ligne"><div class="principal">
        <div class="nom">${esc(s.nom)} <span class="tag gris">${esc(s.horizon)}</span>
          ${s.probabilite != null ? `<span class="tag act">${esc(s.probabilite)} %</span>` : ''}</div>
        <div class="meta">${(s.impacts || []).map(esc).join(' · ')}</div>
      </div>
      <button class="petit danger" data-action="suppr-scenario" data-id="${esc(s.id)}">×</button></div>`).join('')}
    </div>` : ''}
  </section>`;
}

async function saisirIndicateur(input) {
  const v = input.value.trim();
  try {
    await post('/api/prevision/indicateurs', {
      id: input.dataset.ind, valeur: v === '' ? null : (isNaN(Number(v)) ? v : Number(v)) });
    toast('Valeur enregistrée');
  } catch (e) { toast(e.message, 'erreur'); }
}
window.saisirIndicateur = saisirIndicateur;

/* ================================================================== OSINT */
async function osint() {
  const [outils, categories, cas, cadre, registres, besoins] = await Promise.all([
    get('/api/osint/outils'), get('/api/osint/categories'),
    get('/api/osint/cas'), get('/api/osint/cadre'),
    get('/api/osint/registres'), get('/api/osint/besoins')]);
  S.osint = { outils: outils.outils, categories: categories.categories,
              cas: cas.cas, cadre, registres: registres.registres || [],
              besoins: besoins.besoins || [] };

  if (S.osint.casId) return casDetail(S.osint.casId);

  const regs = S.osint.registres;
  return `
  <div class="titre-page">
    <h1>OSINT</h1>
    <div class="actions">
      ${regs.map(r => `<span class="pastille ${r.id === 'watchtower' ? 'ac' : 'ok'}">
        <i class="pt"></i>${esc(r.nom)} · ${r.outils}</span>`).join('')}
      <button class="primaire" data-action="nouveau-cas">＋ Nouveau cas</button>
    </div>
  </div>

  <div class="note-info">
    Deux registres branchés, <b>sans duplication</b> : les sources ouvertes
    françaises (registre local) et le registre Watchtower déjà présent dans le
    dépôt, lu là où il est. ${regs.filter(r => r.id === 'watchtower').map(r =>
      `<span class="mono">${esc(r.chemin || '')}</span> — ${esc(r.genere_le || '')}`).join('')}
  </div>

  <div class="avertissement">
    <b>Cadre.</b> ${(cadre.cadre_legal || []).map(esc).join('<br>')}
  </div>

  <section class="bloc">
    <h2>Par besoin <span class="dim">(${S.osint.besoins.length}) — « j'ai besoin de… »</span></h2>
    <div class="liste">
      ${S.osint.besoins.map(b => `
        <div class="ligne">
          <div class="principal">
            <div class="nom">${b.besoin.replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')}</div>
            <div style="display:flex;flex-wrap:wrap;gap:5px;margin-top:5px">
              ${(b.outils_resolus || []).map(o =>
                `<span class="tag gris" title="${esc(o.licence || '')}">${esc(o.nom)}</span>`).join('')}
            </div>
            ${b.note ? `<div class="meta" style="margin-top:5px">${esc(b.note)}</div>` : ''}
          </div>
        </div>`).join('') || '<div class="vide">Registre Watchtower non trouvé.</div>'}
    </div>
  </section>

  <section class="bloc">
    <h2>Cas en cours <span class="dim">(${S.osint.cas.length})</span></h2>
    ${S.osint.cas.length ? `<div class="liste">${S.osint.cas.map(c => `
      <div class="ligne cliquable" data-action="ouvrir-cas" data-id="${esc(c.id)}">
        <div class="principal">
          <div class="nom elide">${esc(c.titre)}</div>
          <div class="meta">${esc(c.objet || '')} · ${(c.preuves || []).length} élément(s)</div>
        </div>
        <span class="tag ${c.statut === 'clos' ? 'gris' : 'act'}">${esc(c.statut)}</span>
      </div>`).join('')}</div>` : '<div class="vide">Aucun cas ouvert.</div>'}
  </section>

  ${(S.osint.categories || []).map(cat => {
    const sel = (S.osint.outils || []).filter(o => o.categorie === cat.id);
    if (!sel.length) return '';
    return `<section class="bloc">
      <h2>${esc(cat.nom)} <span class="dim">(${sel.length})</span>
        ${cat.note ? `<span class="dim" style="text-transform:none;letter-spacing:0">— ${esc(cat.note)}</span>` : ''}</h2>
      <div class="liste">${sel.map(o => `
        <div class="ligne">
          <div class="principal">
            <div class="nom">${esc(o.nom)}
              <span class="tag ${o.risque === 'intrusif' ? 'ris' : o.risque === 'actif' ? 'act' : 'deci'}">${esc(o.risque)}</span>
              <span class="tag gris">${esc(o.licence)}</span>
              <span class="tag ${o.registre === 'watchtower' ? 'qst' : 'vide'}">${o.registre === 'watchtower' ? 'watchtower' : 'local'}</span>
              ${o.etoiles ? `<span class="confiance">★ ${o.etoiles.toLocaleString('fr-FR')}</span>` : ''}
            </div>
            <div class="meta" style="margin-top:4px">${esc(o.description || '')}</div>
            ${o.usage ? `<div class="meta" style="margin-top:2px;color:var(--ac)">${esc(o.usage)}</div>` : ''}
            ${o.install ? `<div class="meta mono" style="margin-top:3px;color:var(--tx-2)"> installer : ${esc(String(o.install).slice(0, 150))}</div>` : ''}
            ${o.verifier ? `<div class="meta mono" style="margin-top:2px"> vérifier : ${esc(o.verifier)}</div>` : ''}
            ${o.gpu ? `<div class="meta" style="margin-top:2px"> matériel : ${esc(o.gpu)}</div>` : ''}
            ${o.requete_type ? `<div class="meta mono" style="margin-top:3px">${esc(o.requete_type)}</div>` : ''}
          </div>
          ${o.url ? `<a class="bouton petit" href="${esc(o.url)}" target="_blank" rel="noopener">Source</a>` : ''}
        </div>`).join('')}</div>
    </section>`;
  }).join('')}`;
}

async function casDetail(id) {
  const { cas: c } = await get('/api/osint/cas/' + id);
  const prev = c.preuves || [];
  return `
  <div class="titre-page">
    <h1>${esc(c.titre)}</h1>
    <div class="actions">
      <button class="fantome" data-action="fermer-cas">‹ Tous les cas</button>
      <button class="primaire" data-action="generer-note-osint" data-id="${esc(c.id)}">✦ Note</button>
    </div>
  </div>
  <div class="carte" style="margin-bottom:20px">
    <div class="cle">Question posée</div>
    <div style="font-size:15px">${esc(c.question || c.titre)}</div>
    <div class="grille g3" style="margin-top:14px">
      <div><div class="cle">Objet</div>${esc(c.objet || '—')}</div>
      <div><div class="cle">Périmètre</div>${esc(c.perimetre || '—')}</div>
      <div><div class="cle">Cadre</div>${esc(c.cadre || '—')}</div>
    </div>
  </div>

  <section class="bloc">
    <h2>Chaîne de preuves <span class="dim">(${prev.length})</span></h2>
    ${prev.length ? `<div class="table-enveloppe"><table>
      <thead><tr><th>Élément</th><th>Source</th><th>Outil</th><th>Collecté le</th><th>Fiabilité</th><th></th></tr></thead>
      <tbody>${prev.map(p => `<tr>
        <td>${esc(p.titre)}<div class="meta" style="font-size:11.5px;color:var(--dim)">${nl2br(p.contenu || '')}</div></td>
        <td>${esc(p.source)}<div class="meta mono" style="font-size:11px">${esc((p.url || '').slice(0, 48))}</div></td>
        <td>${esc(p.outil)}</td><td class="mono">${esc(p.collecte_le)}</td>
        <td><span class="tag ${p.fiabilite === 'A' || p.fiabilite === 'B' ? 'deci' : p.fiabilite === 'D' ? 'ris' : 'act'}">${esc(p.fiabilite)}</span></td>
        <td><button class="petit danger" data-action="suppr-preuve" data-cas="${esc(c.id)}" data-id="${esc(p.id)}">×</button></td>
      </tr>`).join('')}</tbody></table></div>`
      : '<div class="vide">Aucun élément versé au dossier.</div>'}

    <div class="grille-form" style="margin-top:14px">
      <label class="champ"><span>Élément</span><input id="pv-titre" placeholder="Extrait de délibération"></label>
      <label class="champ"><span>Source (obligatoire)</span><input id="pv-source" placeholder="Délibération n° 2026-xx, site de l'Agglo"></label>
      <label class="champ"><span>URL</span><input id="pv-url"></label>
      <label class="champ"><span>Outil</span><input id="pv-outil" value="saisie"></label>
      <label class="champ"><span>Fiabilité</span><select id="pv-fiab">
        <option value="A">A — source officielle</option><option value="B">B — secondaire fiable</option>
        <option value="C">C — à corroborer</option><option value="D">D — non vérifiée</option>
        <option value="X" selected>X — non évalué</option></select></label>
      <label class="champ"><span>Contenu / citation</span><textarea id="pv-contenu"></textarea></label>
    </div>
    <button class="primaire" data-action="ajouter-preuve" data-cas="${esc(c.id)}">＋ Verser au dossier</button>
  </section>`;
}

/* ================================================================ SYSTÈME */
async function systeme() {
  const [infos, maj, fichiers, config, tableau] = await Promise.all([
    get('/api/infos'), get('/api/mise-a-jour'), get('/api/fichiers'),
    get('/api/config'), get('/api/tableau')]);
  S.systeme = { infos, maj, fichiers: fichiers.fichiers, config: config.config };
  const m = maj;

  return `
  <div class="titre-page"><h1>Système</h1></div>

  <div class="grille g2">
    <section class="bloc">
      <h2>Application</h2>
      <div class="carte">
        <div class="grille g2">
          ${Object.entries({
            'Version': infos.version, 'Python': infos.python, 'Système': infos.systeme,
            'Mode': infos.portable ? 'portable' : (infos.gele ? 'installé' : 'depuis les sources'),
            'Code': infos.dossier_code, 'Données': infos.dossier_donnees,
            'Modules': (infos.modules || []).join(', '),
          }).map(([k, v]) => `<div><div class="cle">${esc(k)}</div>
            <div class="mono" style="font-size:12px">${esc(v)}</div></div>`).join('')}
        </div>
      </div>
    </section>

    <section class="bloc">
      <h2>Mise à jour — canal ${esc(m.canal)}</h2>
      <div class="carte">
        <div class="grille g2" style="margin-bottom:12px">
          <div><div class="cle">Installée</div><div class="valeur" style="font-size:18px">${esc(m.actuelle)}</div></div>
          <div><div class="cle">Disponible</div><div class="valeur" style="font-size:18px">${esc(m.disponible || '—')}</div></div>
        </div>
        <div class="note-info">${esc(m.message)}</div>
        ${m.sale ? '<div class="avertissement">La copie de travail contient des modifications non enregistrées. Enregistrez-les avant toute mise à jour.</div>' : ''}
        <div class="rangee">
          <button class="sans-flex" data-action="verifier-maj">⟳ Vérifier</button>
          ${!m.a_jour && !m.sale ? `<button class="primaire sans-flex" data-action="appliquer-maj">↓ Mettre à jour</button>` : ''}
          <button class="sans-flex" data-action="annuler-maj">↺ Annuler</button>
        </div>
        ${(m.etiquettes || []).length ? `<div style="margin-top:12px" class="mono dim">
          Étiquettes : ${m.etiquettes.slice(0, 8).map(esc).join(' · ')}</div>` : ''}
      </div>
    </section>
  </div>

  <section class="bloc">
    <h2>Configuration</h2>
    <div class="carte">
      <div class="grille-form">
        <label class="champ"><span>Canal de mise à jour</span>
          <select id="cfg-canal">
            ${['git', 'release', 'desactive'].map(v =>
              `<option ${(S.systeme.config.mises_a_jour || {}).canal === v ? 'selected' : ''}>${v}</option>`).join('')}
          </select></label>
        <label class="champ"><span>Dépôt</span><input id="cfg-depot" value="${esc((S.systeme.config.mises_a_jour || {}).depot || '')}"></label>
        <label class="champ"><span>Fournisseur de modèle</span>
          <select id="cfg-llm">
            ${['auto', 'ollama', 'openai', 'none'].map(v =>
              `<option ${(S.systeme.config.llm || {}).provider === v ? 'selected' : ''}>${v}</option>`).join('')}
          </select></label>
        <label class="champ"><span>URL Ollama</span><input id="cfg-ollama" value="${esc((S.systeme.config.llm || {}).ollama_url || '')}"></label>
        <label class="champ"><span>Modèle Ollama</span><input id="cfg-modele" value="${esc((S.systeme.config.llm || {}).ollama_model || '')}"></label>
      </div>
      <button class="primaire" data-action="sauver-config">Enregistrer</button>
      <span class="dim" style="margin-left:10px;font-size:12px">Ollama installé localement =
        gratuit, hors ligne, aucune donnée ne sort du poste.</span>
    </div>
  </section>

  <section class="bloc">
    <h2>Documents produits <span class="dim">(${S.systeme.fichiers.length})</span></h2>
    ${S.systeme.fichiers.length ? `<div class="liste">${S.systeme.fichiers.slice(0, 40).map(f => `
      <div class="ligne">
        <span class="tag">${esc(f.nom.split('.').pop())}</span>
        <div class="principal"><div class="nom mono elide">${esc(f.nom)}</div>
          <div class="meta">${esc(f.maj_le)} · ${(f.taille / 1024).toFixed(0)} Ko</div></div>
        <a class="bouton petit" href="${esc(f.url)}" target="_blank">Ouvrir</a>
      </div>`).join('')}</div>` : '<div class="vide">Aucun document.</div>'}
    <div class="rangee" style="margin-top:12px">
      <button class="sans-flex" data-action="sauvegarde">Sauvegarder les données</button>
    </div>
  </section>`;
}

/* ================================================================== AIDE */
const AIDE = {
  accueil: `Vue d'ensemble. Le territoire de référence est paramétrable dans la configuration.<br><br>
    <b>Commencer :</b> « Nouvelle réunion ».`,
  reunion: `Pendant la séance, collez ou dictez ce qui se dit dans la zone de capture.
    Chaque phrase est analysée ; les propositions tombent dans le <b>bac</b>.
    Vous acceptez (✓) ou refusez (✕) — rien n'entre dans le compte rendu sans votre accord.<br><br>
    Une fois la réunion close, l'onglet <b>Documents</b> produit le compte rendu, la note,
    la délibération, la présentation, le planning et le budget.<br><br>
    <b>Sans modèle :</b> l'extraction déterministe fonctionne quand même, et tous les
    documents sortent. Le modèle ajoute de la finesse, il n'est jamais indispensable.`,
  carto: `Chaque couche porte sa licence et son risque. Cochez ce qui vous intéresse
    puis « Mémoriser la vue ».<br><br>
    <b>Vigilance :</b> les couches marquées « fort » (vidéoprotection, réseaux
    d'exploitation) ne doivent jamais être diffusées publiquement.`,
  cognitorium: `Fiches individus / structures / partenaires + bibliothèque de l'état de l'art.
    L'indexeur parcourt les dossiers du dépôt : indiquez un chemin relatif
    (projects/COGNITORIUM, projects/ETAT-DE-LART-PSYCHOLOGIE…).`,
  prevision: `Saisissez une valeur dans la colonne « Valeur » : elle est enregistrée
    immédiatement. Une série de valeurs fait apparaître la tendance.<br><br>
    La note de prévision ne comble jamais un trou : elle le signale.`,
  osint: `Registre d'outils + conduite d'investigation. On ne lance rien depuis
    l'application : on documente, on prépare la commande, on trace.<br><br>
    Un élément sans source n'est pas une preuve — le formulaire l'exige.`,
  systeme: `Version, canal de mise à jour, configuration du modèle, sauvegarde.<br><br>
    Le canal <b>git</b> ne nécessite aucune infrastructure : on bascule d'étiquette.`,
};

/* ============================================================== ÉVÉNEMENTS */
document.addEventListener('click', async e => {
  const t = e.target.closest('[data-action]');
  if (!t) return;
  const act = t.dataset.action;
  try {
    await ACTIONS[act]?.(t, e);
  } catch (err) {
    toast(err.message || String(err), 'erreur');
    console.error(err);
  }
});

document.addEventListener('change', async e => {
  const el = e.target.closest('[data-modif]');
  if (!el) return;
  const kind = el.dataset.modif, id = el.dataset.id, champ = el.dataset.champ;
  try {
    await put(`/api/meeting/${S.reu.session}/item/${kind}/${id}`, { [champ]: el.value });
    toast('Enregistré');
  } catch (err) { toast(err.message, 'erreur'); }
});

document.addEventListener('keydown', e => {
  if (e.key === 'Enter' && e.ctrlKey && $('#zone-capture')) {
    ACTIONS['pousser']?.($('[data-action="pousser"]'), e);
  }
});

const ACTIONS = {
  /* ------------------------------------------------------------ navigation */
  'vue': async (t) => {
    if (t.dataset.reset) S.reu.session = null;
    await aller(t.dataset.vue);
  },
  'ouvrir-reunion': async (t) => { S.reu.session = t.dataset.id; S.reu.onglet = 'direct'; await render(); },
  'onglet-reu': async (t) => { S.reu.onglet = t.dataset.onglet; await render(); },
  'onglet': (t) => {
    S.ongletAside = t.dataset.onglet;
    $$('.onglet').forEach(o => o.classList.toggle('actif', o === t));
    rendreAside();
  },

  /* --------------------------------------------------------------- réunion */
  'creer-reunion': async () => {
    const v = id => ($(id) || {}).value || '';
    const r = await post('/api/meeting', {
      titre: v('#nv-titre'), lieu: v('#nv-lieu'), date: v('#nv-date'), type: v('#nv-type'),
      organisme: v('#nv-organisme'),
      ordre_du_jour: v('#nv-odj').split('\n').map(x => x.trim()).filter(Boolean),
      participants: v('#nv-participants').split('\n').map(x => x.trim()).filter(Boolean),
    });
    S.reu.session = r.session.id; S.reu.onglet = 'direct';
    await render();
    toast('Réunion créée');
  },
  'nouvelle-reunion': async () => { S.reu.session = null; S.vue = 'reunion'; await render(); },
  'suppr-reunion': async (t) => {
    if (!confirm('Supprimer cette réunion et tout son contenu ?')) return;
    await del('/api/meeting/' + t.dataset.id);
    await render();
  },
  'statut': async (t) => {
    await post(`/api/meeting/${S.reu.session}/statut`, { statut: t.dataset.statut });
    await render();
  },
  'pousser': async () => {
    const zone = $('#zone-capture'), loc = $('#zone-locuteur');
    const texte = (zone.value || '').trim();
    if (!texte) return;
    zone.disabled = true;
    try {
      const r = await post(`/api/meeting/${S.reu.session}/segment`,
        { texte, locuteur: (loc.value || '').trim(), source: 'saisie' });
      zone.value = '';
      const n = (r.suggestions || []).length;
      if (n) toast(`${n} proposition(s) dans le bac`);
      await render();
      $('#zone-capture')?.focus();
    } finally { zone.disabled = false; }
  },
  'noter': async () => {
    const txt = prompt('Note manuscrite :');
    if (!txt) return;
    await post(`/api/meeting/${S.reu.session}/note`, { texte: txt });
    await render();
  },
  'analyser': async () => {
    try {
      const r = await post(`/api/meeting/${S.reu.session}/analyser`, {});
      toast(`${(r.suggestions || []).length} proposition(s)`);
      await render();
    } catch (err) { toast(err.message, 'erreur'); }
  },
  'accepter': async (t) => {
    await post(`/api/meeting/${S.reu.session}/suggestion/${t.dataset.id}/accepter`, {});
    await render();
  },
  'refuser': async (t) => {
    await post(`/api/meeting/${S.reu.session}/suggestion/${t.dataset.id}/refuser`, {});
    await render();
  },
  'ajouter-item': async (t) => {
    const kind = t.dataset.kind;
    const texte = ($('#texte-item') || {}).value || '';
    if (!texte.trim()) return;
    await post(`/api/meeting/${S.reu.session}/item`, {
      kind, texte, responsable: ($('#resp-item') || {}).value || '',
      echeance: ($('#echeance-item') || {}).value || '' });
    await render();
  },
  'suppr-item': async (t) => {
    await del(`/api/meeting/${S.reu.session}/item/${t.dataset.kind}/${t.dataset.id}`);
    await render();
  },
  'ajouter-participant': async () => {
    const v = (($('#ajout-participant') || {}).value || '').trim();
    if (!v) return;
    const s = S.reu.data;
    await put('/api/meeting/' + S.reu.session, { participants: [...(s.participants || []), v] });
    await render();
  },
  'ajouter-budget': async () => {
    const v = id => ($(id) || {}).value;
    await post(`/api/meeting/${S.reu.session}/budget`, {
      libelle: v('#bud-libelle') || 'Poste', categorie: v('#bud-categorie'),
      quantite: Number(v('#bud-qte') || 1), unite: v('#bud-unite') || 'forfait',
      cout_unitaire: Number(v('#bud-cout') || 0), financeur: v('#bud-financeur') || '' });
    await render();
  },
  'suppr-budget': async (t) => {
    await del(`/api/meeting/${S.reu.session}/budget/${t.dataset.id}`); await render();
  },
  'ajouter-tache': async () => {
    const v = id => ($(id) || {}).value;
    await post(`/api/meeting/${S.reu.session}/planning`, {
      label: v('#tch-label') || 'Tâche', debut: v('#tch-debut'), fin: v('#tch-fin'),
      responsable: v('#tch-resp'), avancement: Number(v('#tch-av') || 0) });
    await render();
  },
  'suppr-tache': async (t) => {
    await del(`/api/meeting/${S.reu.session}/planning/${t.dataset.id}`); await render();
  },
  'generer': async (t) => {
    t.disabled = true; const lbl = t.textContent; t.textContent = '…';
    try {
      const r = await post(`/api/meeting/${S.reu.session}/generer`,
        { gabarit: t.dataset.gabarit, format: t.dataset.format });
      toast(r.document.titre || 'Document généré');
      S.reu.onglet = 'documents';
      await render();
      if (t.dataset.format === 'html' || t.dataset.format === 'svg') {
        window.open(r.telechargement, '_blank');
      }
    } catch (e) {
      toast(e.message, 'erreur'); t.disabled = false; t.textContent = lbl;
    }
  },

  /* ----------------------------------------------------------- cartographie */
  'sauver-vue': async () => {
    const actives = $$('[data-couche]').filter(c => c.checked).map(c => c.dataset.couche);
    const nom = prompt('Nom de la vue :', 'Vue du ' + new Date().toLocaleDateString('fr-FR'));
    if (!nom) return;
    await post('/api/carto/vue', { nom, actives, par_defaut: true });
    toast(`${actives.length} couche(s) mémorisée(s)`);
  },
  'ajouter-point': async () => {
    const v = id => ($(id) || {}).value || '';
    await post('/api/carto/points', { nom: v('#pt-nom'), lat: v('#pt-lat'), lon: v('#pt-lon'),
      commune: v('#pt-commune'), description: v('#pt-desc') });
    await render();
  },
  'suppr-point': async (t) => { await del('/api/carto/points/' + t.dataset.id); await render(); },

  /* ----------------------------------------------------------- cognitorium */
  'creer-profil': async () => {
    const v = id => ($(id) || {}).value || '';
    await post('/api/cognitorium/profils', {
      nom: v('#pf-nom'), prenom: v('#pf-prenom'), role: v('#pf-role'),
      structure: v('#pf-structure'), commune: v('#pf-commune'), type: v('#pf-type'),
      courriel: v('#pf-courriel'),
      tags: v('#pf-tags').split(',').map(x => x.trim()).filter(Boolean) });
    await render(); toast('Fiche créée');
  },
  'suppr-profil': async (t) => { await del('/api/cognitorium/profils/' + t.dataset.id); await render(); },
  'suppr-ref': async (t) => { await del('/api/cognitorium/references/' + t.dataset.id); await render(); },
  'indexer': async () => {
    const racine = (($('#idx-racine') || {}).value || 'projects/COGNITORIUM').trim();
    const domaine = (($('#idx-domaine') || {}).value || '').trim();
    const r = await post('/api/cognitorium/indexer', { racine, domaine });
    toast(`${r.ajoutees} référence(s) indexée(s) — ${r.total} au total`);
    await render();
  },

  /* -------------------------------------------------------------- prévision */
  'creer-scenario': async () => {
    const v = id => ($(id) || {}).value || '';
    await post('/api/prevision/scenario', {
      nom: v('#sc-nom'), horizon: v('#sc-horizon'),
      probabilite: v('#sc-proba') === '' ? null : Number(v('#sc-proba')),
      hypotheses: v('#sc-hyp').split('\n').filter(Boolean),
      impacts: v('#sc-imp').split('\n').filter(Boolean),
      signaux: v('#sc-sig').split('\n').filter(Boolean) });
    await render(); toast('Scénario ajouté');
  },
  'suppr-scenario': async (t) => { await del('/api/prevision/scenario/' + t.dataset.id); await render(); },
  'generer-prevision': async () => {
    const r = await post('/api/prevision/generer', { format: 'html' });
    toast('Note générée'); window.open(r.telechargement, '_blank');
  },

  /* ------------------------------------------------------------------ osint */
  'nouveau-cas': async () => {
    const titre = prompt('Intitulé du cas :');
    if (!titre) return;
    const question = prompt('Question posée :') || '';
    const r = await post('/api/osint/cas', { titre, question,
      cadre: 'données publiques uniquement' });
    S.osint.casId = r.cas.id;
    await render();
  },
  'ouvrir-cas': async (t) => { S.osint.casId = t.dataset.id; await render(); },
  'fermer-cas': async () => { S.osint.casId = null; await render(); },
  'ajouter-preuve': async (t) => {
    const v = id => ($(id) || {}).value || '';
    await post(`/api/osint/cas/${t.dataset.cas}/preuve`, {
      titre: v('#pv-titre'), source: v('#pv-source'), url: v('#pv-url'),
      outil: v('#pv-outil'), fiabilite: v('#pv-fiab'), contenu: v('#pv-contenu') });
    await render(); toast('Élément versé');
  },
  'suppr-preuve': async (t) => {
    await del(`/api/osint/cas/${t.dataset.cas}/preuve/${t.dataset.id}`); await render();
  },
  'generer-note-osint': async (t) => {
    const r = await post(`/api/osint/cas/${t.dataset.id}/generer`, { format: 'html' });
    toast('Note générée'); window.open(r.telechargement, '_blank');
  },

  /* ---------------------------------------------------------------- système */
  'verifier-maj': async () => {
    const r = await get('/api/mise-a-jour');
    toast(r.a_jour ? 'À jour' : ('Version ' + r.disponible + ' disponible'));
    if (S.vue === 'systeme') await render();
    majPilote(r);
  },
  'appliquer-maj': async () => {
    if (!confirm('Mettre à jour maintenant ? Une sauvegarde sera créée automatiquement.')) return;
    const r = await post('/api/mise-a-jour/appliquer', {});
    toast(r.ok ? ('Mise à jour appliquée : ' + r.message) : r.message, r.ok ? 'info' : 'erreur');
    await render();
  },
  'annuler-maj': async () => {
    if (!confirm('Revenir à la version précédente ?')) return;
    const r = await post('/api/mise-a-jour/annuler', {});
    toast(r.ok ? 'Retour arrière effectué' : r.message, r.ok ? 'info' : 'erreur');
    await render();
  },
  'sauver-config': async () => {
    const v = id => ($(id) || {}).value;
    await put('/api/config', {
      mises_a_jour: { canal: v('#cfg-canal'), depot: v('#cfg-depot') },
      llm: { provider: v('#cfg-llm'), ollama_url: v('#cfg-ollama'), ollama_model: v('#cfg-modele') } });
    toast('Configuration enregistrée — le modèle sera retesté au prochain appel');
    majPilote(await get('/api/mise-a-jour'));
  },
  'sauvegarde': async () => {
    const r = await post('/api/sauvegarde', {});
    toast('Sauvegarde créée : ' + r.sauvegarde);
  },
};

/* ============================================================ FLUX / ASIDE */
function rendreAside() {
  const j = $('#journal');
  if (S.ongletAside === 'aide') {
    j.innerHTML = `<div style="font-family:var(--sans);font-size:13px;line-height:1.65;color:var(--tx-2)">
      ${AIDE[S.vue] || ''}</div>`;
    return;
  }
  j.innerHTML = (S.journal || []).length
    ? S.journal.map(r => `<div class="entree ${esc(r.canal || r.niveau || '')}">
        <span class="h">${esc(r.t || '')}</span>
        ${esc(r.message || r.evt || r.kind || '')}</div>`).join('')
    : '<div class="dim">En attente d\'activité…</div>';
}

let source = null;
function connecter() {
  if (source) source.close();
  source = new EventSource('/api/events');
  const MAX = 90;
  S.journal = S.journal || [];
  for (const canal of ['journal', 'meeting', 'carto', 'cognitorium', 'prevision', 'osint']) {
    source.addEventListener(canal, e => {
      try {
        const d = JSON.parse(e.data);
        S.journal.push({ ...d, t: d.t || new Date().toLocaleTimeString('fr-FR') });
        S.journal = S.journal.slice(-MAX);
        rendreAside();
        const j = $('#journal'); if (j) j.scrollTop = j.scrollHeight;
        // rafraîchissement léger de la vue concernée
        if (S.vue === 'accueil' && canal === 'meeting') render();
      } catch (_) { }
    });
  }
  source.onerror = () => { };
}

function majPilote(maj) {
  const el = $('#pil-modules'), el2 = $('#pil-modele');
  if (el && S.modules) {
    const ok = S.modules.filter(m => m.charge !== false).length;
    el.className = 'pastille ' + (ok === S.modules.length ? 'ok' : 'warn');
    el.querySelector('span').textContent = `${ok}/${S.modules.length} modules`;
  }
  if (el2 && maj) {
    el2.className = 'pastille ' + (maj.a_jour ? 'ok' : 'warn');
    el2.querySelector('span').textContent = maj.a_jour ? 'à jour' : ('maj ' + (maj.disponible || ''));
  }
}

/* =================================================================== DÉMARRAGE */
(async function demarrer() {
  try {
    const sante = await get('/api/health');
    $('#version').textContent = 'v' + sante.version;
    const modele = sante.modele || {};
    const el = $('#pil-modele');
    el.className = 'pastille ' + (modele.deterministe ? 'warn' : 'ac');
    el.querySelector('span').textContent =
      modele.deterministe ? 'sans modèle (gabarits)' : ('modèle : ' + modele.provider_actif);
    el.title = modele.deterministe
      ? 'Aucun modèle détecté : les documents sont produits par gabarits. Installer Ollama pour enrichir.'
      : `Fournisseur ${modele.provider_actif} — ${modele.ollama_modele || modele.openai_modele}`;
    $('#pied-infos').textContent = new Date().toLocaleString('fr-FR');
  } catch (e) {
    $('#pied-infos').textContent = 'serveur injoignable';
  }
  connecter();
  await render();
  rendreAside();
  try { majPilote(await get('/api/mise-a-jour')); } catch (_) { }
})();
