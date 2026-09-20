import json
from pathlib import Path
import sys

sys.path.insert(0, '/home/user/monorepo')
from scripts.generate_obsidian_data import get_obsidian_dataset
from scripts.generate_extra_data import get_company_data

TARGET = Path('/home/user/monorepo/projects/btp-conduite-travaux')

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

obsidian_graph_data = get_obsidian_dataset()
extra_data = get_company_data()

inventory_json = json.dumps(inventory, ensure_ascii=False)
synthese_json = json.dumps(synthese, ensure_ascii=False)
confrontation_json = json.dumps(confrontation, ensure_ascii=False)
ledger_json = json.dumps(ledger_data, ensure_ascii=False)
reports_json = json.dumps(reports, ensure_ascii=False)
obsidian_json = json.dumps(obsidian_graph_data, ensure_ascii=False)
extra_data_json = json.dumps(extra_data, ensure_ascii=False)

print(f"Loaded all datasets: {len(reports)} reports, {len(obsidian_graph_data['nodes'])} obsidian nodes, {len(extra_data['projects'])} projects, {len(extra_data['fleet'])} fleet items, {len(extra_data['employees'])} employees.")
