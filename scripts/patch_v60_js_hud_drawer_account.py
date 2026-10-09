#!/usr/bin/env python3
"""
Patch v60: Add JavaScript logic for Drawer Flyout, 4X Topbar Live Updating,
Dynamic News Ticker, and Unified Account & Identity Management
"""

import re

with open("scripts/section_js_part3.py", "r", encoding="utf-8") as f:
    js_text = f.read()

# Update switchNav to also update drawer-nav-item active state
old_switch_nav = """function switchNav(tabId, btn) {
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));

        const target = document.getElementById('tab-' + tabId);
        if (target) target.classList.add('active');
        if (btn) btn.classList.add('active');

        currentNav = tabId;"""

new_switch_nav = """function switchNav(tabId, btn) {
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.drawer-nav-item').forEach(b => b.classList.remove('active'));

        const target = document.getElementById('tab-' + tabId);
        if (target) target.classList.add('active');
        if (btn) btn.classList.add('active');
        const drawerBtn = document.querySelector('.drawer-nav-item[data-tab="' + tabId + '"]');
        if (drawerBtn) drawerBtn.classList.add('active');

        currentNav = tabId;"""

if old_switch_nav in js_text:
    js_text = js_text.replace(old_switch_nav, new_switch_nav)
    print("Updated switchNav in js_part3!")

# New JS engine for 4X Topbar, News Ticker, Drawer Flyout, and Account CRUD
v60_js_engine = r"""

    /* ========================================================================== */
    /* V60: LEFT FLYOUT DRAWER & NAVIGATION CONTROLLER                            */
    /* ========================================================================== */
    let isSidebarDrawerOpen = false;

    function toggleSidebarDrawer(forceState) {
        if (typeof forceState === 'boolean') {
            isSidebarDrawerOpen = forceState;
        } else {
            isSidebarDrawerOpen = !isSidebarDrawerOpen;
        }

        const drawer = document.getElementById('sidebar-drawer');
        const backdrop = document.getElementById('sidebar-backdrop');

        if (drawer && backdrop) {
            if (isSidebarDrawerOpen) {
                drawer.classList.add('active');
                backdrop.classList.add('active');
            } else {
                drawer.classList.remove('active');
                backdrop.classList.remove('active');
            }
        }
    }

    function filterDrawerItems(query) {
        const q = (query || '').toLowerCase().trim();
        const items = document.querySelectorAll('.drawer-nav-item');
        const pillars = document.querySelectorAll('.drawer-pillar');

        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            if (!q || text.includes(q)) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });

        // Hide pillars if all child items hidden
        pillars.forEach(pillar => {
            const visibleItems = pillar.querySelectorAll('.drawer-nav-item:not([style*="display: none"])');
            if (visibleItems.length === 0 && q) {
                pillar.style.display = 'none';
            } else {
                pillar.style.display = 'block';
            }
        });
    }

    /* ========================================================================== */
    /* V60: DYNAMIC BREAKING NEWS TICKER ENGINE                                   */
    /* ========================================================================== */
    let currentTickerMode = 'general';

    const tickerFeeds = {
        'general': '🚀 FLASH : Décompte mensuel Chorus Pro validé (+48 500 €) • DICT Sète PK 0+240 purgée sans réserve • 29.4t BBSG 0/10 livrées à 168°C par centrale Saint-Thibéry • Inspection CSPS conforme (100% EPI portés) • Avancement global chantiers : 94%.',
        'finance': '💰 FINANCE : Caisse active 485 200 € (+14 200 € ce mois) • Acompte Barbazan n°3 encaissé (94 500 € HT) • Retenue de garantie 5% libérée sur Aurouer • Dépenses carburant & centrales à jour.',
        'safety': '🚨 SÉCURITÉ : Vigilance Météo Tramontane 14 km/h (Feu Vert pour finisseur) • Blindage tranchée R.4534 actif sur Pézenas (P = 1.80m) • Session 1/4h sécurité effectuée ce matin • Zéro accident en 420 jours.',
        'logistics': '🚛 LOGISTIQUE : 3x 8x4 en rotation continue carrière GSM ➔ Chantier Sète • Rotation moyenne : 42 min • Température benne enrobé : 165°C • Consommation GNT conforme au DQE.'
    };

    function setTickerMode(mode) {
        currentTickerMode = mode;
        document.querySelectorAll('.ticker-mode-btn').forEach(b => b.classList.remove('active'));
        const btn = document.getElementById('btn-ticker-' + mode);
        if (btn) btn.classList.add('active');

        const tickerEl = document.getElementById('live-news-ticker-text');
        if (tickerEl) {
            tickerEl.textContent = tickerFeeds[mode] || tickerFeeds['general'];
        }
    }

    /* ========================================================================== */
    /* V60: UNIFIED ACCOUNT, IDENTITY & HEADCOUNT HIERARCHY ENGINE                */
    /* ========================================================================== */
    let userAccountState = {
        userName: 'Jean DUPONT',
        userRole: 'patron',
        roleLabel: 'Direction & Gérant',
        roleIcon: '👑',
        headcount: 24,
        companyKey: 'occitanie_tp',
        companyName: 'Occitanie TP & VRD SAS'
    };

    function openAccountModal() {
        const modal = document.getElementById('account-modal') || document.getElementById('company-switch-modal');
        if (modal) {
            modal.style.display = 'flex';
            setAccountTab('login');
            loadAccountFormValues();
        }
    }

    function closeAccountModal() {
        const modal = document.getElementById('account-modal') || document.getElementById('company-switch-modal');
        if (modal) modal.style.display = 'none';
    }

    function setAccountTab(tabKey) {
        document.querySelectorAll('.account-tab-btn').forEach(b => b.classList.remove('active'));
        const btn = document.getElementById('btn-acc-' + tabKey);
        if (btn) btn.classList.add('active');

        document.querySelectorAll('.acc-tab-content').forEach(c => c.style.display = 'none');
        const tab = document.getElementById('acc-tab-' + tabKey);
        if (tab) tab.style.display = 'block';
    }

    function loadAccountFormValues() {
        const nameInput = document.getElementById('user-fullname');
        const roleSelect = document.getElementById('user-role-select');
        const headSlider = document.getElementById('user-headcount-slider');
        const headDisp = document.getElementById('user-headcount-display');

        if (nameInput) nameInput.value = userAccountState.userName;
        if (roleSelect) roleSelect.value = userAccountState.userRole;
        if (headSlider) headSlider.value = userAccountState.headcount;
        if (headDisp) headDisp.textContent = userAccountState.headcount + ' Salariés';
    }

    function updateRolePreview(roleKey) {
        const icons = { 'patron': '👑', 'conduite': '👷', 'chef': '🦺', 'compagnon': '🛠️' };
        const labels = {
            'patron': 'Direction & Gérant',
            'conduite': 'Conduite de Travaux',
            'chef': 'Chef de Chantier',
            'compagnon': 'Compagnon VRD'
        };
        userAccountState.userRole = roleKey;
        userAccountState.roleIcon = icons[roleKey] || '👷';
        userAccountState.roleLabel = labels[roleKey] || 'Collaborateur';
    }

    function updateHeadcountSlider(val) {
        const count = parseInt(val, 10);
        userAccountState.headcount = count;
        const headDisp = document.getElementById('user-headcount-display');
        const hudHead = document.getElementById('hud-effectif-val');
        if (headDisp) headDisp.textContent = count + ' Salariés';
        if (hudHead) hudHead.textContent = count + ' Salariés';
    }

    function handleSaveUserIdentity(e) {
        e.preventDefault();
        const nameInput = document.getElementById('user-fullname');
        if (nameInput) userAccountState.userName = nameInput.value.trim() || 'Jean DUPONT';

        // Update HUD
        const hudName = document.getElementById('hud-user-name-display');
        const hudRole = document.getElementById('hud-role-icon');
        const hudEffectif = document.getElementById('hud-effectif-val');

        if (hudName) hudName.textContent = userAccountState.userName;
        if (hudRole) hudRole.textContent = userAccountState.roleIcon;
        if (hudEffectif) hudEffectif.textContent = userAccountState.headcount + ' Salariés';

        closeAccountModal();
        showNotification(`Profil mis à jour : ${userAccountState.userName} (${userAccountState.roleLabel})`, 'success');
    }

    function loginCompanyProfile(profileKey) {
        switchCompanyProfile(profileKey);
        const compNames = {
            'occitanie_tp': 'Occitanie TP & VRD SAS',
            'artisan_2k': 'Artisan Sud VRD',
            'stagiaire_tp': 'Formation Conduite Travaux',
            'compte_neuf': 'Nouvelle Entreprise TP'
        };
        userAccountState.companyKey = profileKey;
        userAccountState.companyName = compNames[profileKey] || 'Occitanie TP';

        const hudComp = document.getElementById('hud-company-name-display');
        if (hudComp) hudComp.textContent = userAccountState.companyName + ' ▾';

        closeAccountModal();
        showNotification(`Entreprise connectée : ${userAccountState.companyName}`, 'info');
    }

    function handleCreateCompany(e) {
        e.preventDefault();
        const name = document.getElementById('new-comp-name')?.value || 'Nouvelle Entreprise TP';
        const treasury = parseFloat(document.getElementById('new-comp-treasury')?.value || 100000);
        const headcount = parseInt(document.getElementById('new-comp-headcount-slider')?.value || 12, 10);

        userAccountState.companyName = name;
        userAccountState.headcount = headcount;

        // Update HUD
        const hudComp = document.getElementById('hud-company-name-display');
        const hudCaisse = document.getElementById('caisse-balance-top');
        const hudHead = document.getElementById('hud-effectif-val');

        if (hudComp) hudComp.textContent = name + ' ▾';
        if (hudCaisse) hudCaisse.textContent = Math.round(treasury).toLocaleString() + ' €';
        if (hudHead) hudHead.textContent = headcount + ' Salariés';

        closeAccountModal();
        showNotification(`Entreprise "${name}" créée et activée avec succès !`, 'success');
    }

    function deleteActiveCompany() {
        if (confirm(`Êtes-vous sûr de vouloir supprimer l'entreprise active "${userAccountState.companyName}" ?`)) {
            loginCompanyProfile('compte_neuf');
            showNotification('Entreprise supprimée. Retour sur profil neutre.', 'warning');
        }
    }

    function resetAllDataFactory() {
        if (confirm('Réinitialiser l\'intégralité des données et recharger la configuration d\'usine ?')) {
            localStorage.clear();
            location.reload();
        }
    }
"""

# Append before closing </script>
pos_close_script = js_text.rfind('</script>')
if pos_close_script != -1:
    js_text = js_text[:pos_close_script] + v60_js_engine + '\n' + js_text[pos_close_script:]
else:
    tq_pos = js_text.rfind('"""')
    if tq_pos != -1:
        js_text = js_text[:tq_pos] + v60_js_engine + '\n</script>\n' + js_text[tq_pos:]
    else:
        js_text += v60_js_engine + '\n</script>\n'

with open("scripts/section_js_part3.py", "w", encoding="utf-8") as f:
    f.write(js_text)

print("scripts/section_js_part3.py updated with v60 JS controllers!")
