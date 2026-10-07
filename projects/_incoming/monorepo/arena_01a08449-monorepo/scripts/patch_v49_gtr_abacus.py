# -*- coding: utf-8 -*-
"""
Fix LaTeX artifacts in section_tab_panels.py, make GTR table rows clickable,
and add applyGtrPreset to section_js_part3.py.
"""

with open('scripts/section_tab_panels.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace LaTeX expressions with unicode
text = text.replace(r'$\ge 80$', '≥ 80')
text = text.replace(r'$\le 2.0$', '≤ 2.0')
text = text.replace(r'$\ge 50$', '≥ 50')
text = text.replace(r'$\ge 80$', '≥ 80')
text = text.replace(r'$\ge 120$', '≥ 120')
text = text.replace(r'$\ge 60$', '≥ 60')

# Make the rows clickable
text = text.replace(
    '<tr>\n                                        <td style="padding: 0.45rem; font-weight: 800; color: #38bdf8;">V1 / V2</td>',
    '<tr onclick="applyGtrPreset(\'V1/V2\', 4.0, 7, 20, 50)" style="border-top: 1px solid rgba(51,65,85,0.4); cursor: pointer;" title="Cliquer pour charger ces paramètres dans le simulateur">'
)
text = text.replace(
    '<tr>\n                                        <td style="padding: 0.45rem; font-weight: 800; color: var(--emerald);">V3 / V4</td>',
    '<tr onclick="applyGtrPreset(\'V3/V4\', 3.5, 6, 30, 80)" style="border-top: 1px solid rgba(51,65,85,0.4); cursor: pointer;" title="Cliquer pour charger ces paramètres dans le simulateur">'
)
text = text.replace(
    '<tr>\n                                        <td style="padding: 0.45rem; font-weight: 800; color: var(--amber);">V5</td>',
    '<tr onclick="applyGtrPreset(\'V5\', 3.0, 5, 45, 120)" style="border-top: 1px solid rgba(51,65,85,0.4); cursor: pointer;" title="Cliquer pour charger ces paramètres dans le simulateur">'
)
text = text.replace(
    '<tr>\n                                        <td style="padding: 0.45rem; font-weight: 800; color: #a855f7;">P1 / P2</td>',
    '<tr onclick="applyGtrPreset(\'P1/P2\', 5.0, 8, 15, 50)" style="border-top: 1px solid rgba(51,65,85,0.4); cursor: pointer;" title="Cliquer pour charger ces paramètres dans le simulateur">'
)
text = text.replace(
    '<tr>\n                                        <td style="padding: 0.45rem; font-weight: 800; color: #ec4899;">P3</td>',
    '<tr onclick="applyGtrPreset(\'P3\', 4.5, 6, 25, 80)" style="border-top: 1px solid rgba(51,65,85,0.4); cursor: pointer;" title="Cliquer pour charger ces paramètres dans le simulateur">'
)
text = text.replace(
    '<tr>\n                                        <td style="padding: 0.45rem; font-weight: 800; color: #e2e8f0;">PQ1 - PQ4</td>',
    '<tr onclick="applyGtrPreset(\'PQ1-PQ4\', 2.5, 4, 35, 60)" style="border-top: 1px solid rgba(51,65,85,0.4); cursor: pointer;" title="Cliquer pour charger ces paramètres dans le simulateur">'
)

with open('scripts/section_tab_panels.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("section_tab_panels.py updated.")

# Add applyGtrPreset in section_js_part3.py
with open('scripts/section_js_part3.py', 'r', encoding='utf-8') as f:
    js_text = f.read()

gtr_fn = r'''
    function applyGtrPreset(classe, spd, passes, thick, targetEv2) {
        const spdInput = document.getElementById('cmp-spd-range');
        const passesInput = document.getElementById('cmp-passes-range');
        const thickInput = document.getElementById('cmp-thick-range');

        if (spdInput) spdInput.value = spd;
        if (passesInput) passesInput.value = passes;
        if (thickInput) thickInput.value = thick;

        updateCompactageParams();
        logCockpit(`Abaque GTR appliqué : Classe ${classe} (${spd} km/h, ${passes} passes, e=${thick}cm, EV2 cible ≥ ${targetEv2} MPa).`, 'info');
    }
'''

if 'function applyGtrPreset' not in js_text:
    pos = js_text.find('function updateCompactageParams()')
    if pos != -1:
        js_text = js_text[:pos] + gtr_fn.strip() + "\n\n    " + js_text[pos:]
        with open('scripts/section_js_part3.py', 'w', encoding='utf-8') as f:
            f.write(js_text)
        print("applyGtrPreset added to section_js_part3.py")
