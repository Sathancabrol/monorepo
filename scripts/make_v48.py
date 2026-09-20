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

print("Generating v4.8 template and full application...")
