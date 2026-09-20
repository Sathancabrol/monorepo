import json
from pathlib import Path
import sys
import os

sys.path.insert(0, '/home/user/monorepo')
sys.path.insert(0, '/home/user/monorepo/scripts')

from generate_obsidian_data import get_obsidian_dataset
from generate_extra_data import get_company_data
from generate_complete_dqe_data import get_dqe_dataset
from generate_template import build_template

TARGET = Path('/home/user/monorepo/projects/btp-conduite-travaux')

# Ensure template is built fresh
build_template()

with open(TARGET / 'data' / 'corpus_btp_inventory.json', 'r', encoding='utf-8') as f:
    inventory = json.load(f)

with open(TARGET / 'data' / 'synthese_chantiers_et_prix.json', 'r', encoding='utf-8') as f:
    synthese = json.load(f)

with open(TARGET / 'data' / 'confrontation_theorie_etatdelart_insitu.json', 'r', encoding='utf-8') as f:
    confrontation = json.load(f)

with open(TARGET / 'data' / 'btp_audit_ledger.json', 'r', encoding='utf-8') as f:
    ledger_data = json.load(f)

reports = {}
for rfile in sorted((TARGET / 'rapports').glob('*.md')):
    reports[rfile.name] = rfile.read_text(encoding='utf-8')

# Populate comprehensive DQE items
raw_dqe = get_dqe_dataset()
dqe_items = []
for item in raw_dqe:
    mo = item.get('mo_u', 0)
    mat = item.get('mat_u', 0)
    eq = item.get('eq_u', 0)
    st = item.get('st_u', 0)
    unit_ds = mo + mat + eq + st
    k = item.get('k', 1.35)
    unit_pv = unit_ds * k
    dqe_items.append({
        'id': item.get('id'),
        'project_id': item.get('project_id'),
        'project_name': item.get('project_name'),
        'lot': item.get('lot'),
        'code': item.get('code'),
        'designation': item.get('designation'),
        'unit': item.get('unite', 'u'),
        'quantity': item.get('qte', 1),
        'ds_mo': mo,
        'ds_mat': mat,
        'ds_eq': eq,
        'ds_st': st,
        'unit_ds': unit_ds,
        'unit_pv': unit_pv,
        'status': item.get('statut', 'En cours')
    })

synthese['dqe_items'] = dqe_items

obsidian_graph_data = get_obsidian_dataset()
extra_data = get_company_data()

# Ensure catalog in extra_data has consistent structure
catalog_items = []
for c in extra_data.get('catalog', []):
    catalog_items.append(c)
extra_data['catalog'] = catalog_items

inventory_json = json.dumps(inventory, ensure_ascii=False)
synthese_json = json.dumps(synthese, ensure_ascii=False)
confrontation_json = json.dumps(confrontation, ensure_ascii=False)
ledger_json = json.dumps(ledger_data, ensure_ascii=False)
reports_json = json.dumps(reports, ensure_ascii=False)
obsidian_json = json.dumps(obsidian_graph_data, ensure_ascii=False)
extra_data_json = json.dumps(extra_data, ensure_ascii=False)

print("Compiling full BTP Autonomous Command suite v4.6...")

with open(TARGET / 'template.html', 'r', encoding='utf-8') as f:
    template = f.read()

html_content = template.replace('__INVENTORY_JSON__', inventory_json) \
                       .replace('__SYNTHESE_JSON__', synthese_json) \
                       .replace('__CONFRONTATION_JSON__', confrontation_json) \
                       .replace('__LEDGER_JSON__', ledger_json) \
                       .replace('__REPORTS_JSON__', reports_json) \
                       .replace('__OBSIDIAN_JSON__', obsidian_json) \
                       .replace('__EXTRA_DATA_JSON__', extra_data_json)

with open(TARGET / 'index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully generated full BTP Autonomous Command v4.6 application ({len(html_content)} bytes) at {TARGET / 'index.html'}")
