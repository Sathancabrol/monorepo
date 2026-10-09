import json
import sys
from pathlib import Path

ROOT = Path('/home/user/monorepo')
TARGET = ROOT / 'projects' / 'btp-conduite-travaux'
sys.path.insert(0, str(ROOT))

from scripts.generate_obsidian_data import get_obsidian_dataset
from scripts.generate_extra_data import get_company_data
from scripts.generate_complete_dqe_data import get_dqe_dataset
from scripts.generate_technical_illustrations import get_vehicle_svg, get_tool_material_svg

# Load JSON Datasets
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
extra_data['dqe_items'] = get_dqe_dataset()

# Import the technical SVG generators
from scripts.generate_technical_illustrations import get_vehicle_svg, get_tool_material_svg

# Add SVGs to fleet and catalog items
for v in extra_data.get('fleet', []):
    v['svg_illustration'] = get_vehicle_svg(v.get('type', '') + ' ' + v.get('name', ''))

for m in extra_data.get('materials_catalog', []):
    m['svg_illustration'] = get_tool_material_svg(m.get('id', ''), m.get('name', ''))

for t in extra_data.get('tool_catalog', []):
    t['svg_illustration'] = get_tool_material_svg(t.get('id', ''), t.get('name', ''))

print("All SVG illustrations embedded in datasets.")
