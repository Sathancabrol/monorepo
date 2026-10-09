import re
import json
from pathlib import Path

TARGET = Path("/home/user/monorepo/projects/btp-conduite-travaux")
SOURCE_BUILD = Path("/home/user/monorepo/scripts/build_html_dashboard.py")

with open(SOURCE_BUILD, "r", encoding="utf-8") as f:
    text = f.read()

idx_header_end = text.find('html_content = f"""')
header = text[:idx_header_end]

idx_footer_start = text.rfind('"""\n\nwith open(TARGET')
body = text[idx_header_end + len('html_content = f"""'):idx_footer_start]

# Replace dataset placeholders
body = body.replace("{inventory_json}", "__INVENTORY_JSON__")
body = body.replace("{synthese_json}", "__SYNTHESE_JSON__")
body = body.replace("{confrontation_json}", "__CONFRONTATION_JSON__")
body = body.replace("{ledger_json}", "__LEDGER_JSON__")
body = body.replace("{reports_json}", "__REPORTS_JSON__")
body = body.replace("{obsidian_json}", "__OBSIDIAN_JSON__")
body = body.replace("{extra_data_json}", "__EXTRA_DATA_JSON__")

# Convert escaped {{ and }} back to single { and }
body = body.replace("{{", "{").replace("}}", "}")

template_path = TARGET / "template.html"
with open(template_path, "w", encoding="utf-8") as f:
    f.write(body)

print(f"Created clean {template_path} (size: {len(body)} chars)")

# Now rewrite scripts/build_html_dashboard.py to load template.html and replace placeholders
new_build_script = header + f"""
with open(TARGET / 'template.html', 'r', encoding='utf-8') as f:
    template = f.read()

html_content = template.replace('__INVENTORY_JSON__', inventory_json) \\
                       .replace('__SYNTHESE_JSON__', synthese_json) \\
                       .replace('__CONFRONTATION_JSON__', confrontation_json) \\
                       .replace('__LEDGER_JSON__', ledger_json) \\
                       .replace('__REPORTS_JSON__', reports_json) \\
                       .replace('__OBSIDIAN_JSON__', obsidian_json) \\
                       .replace('__EXTRA_DATA_JSON__', extra_data_json)

with open(TARGET / 'index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Successfully generated full BTP Autonomous Command v4.6 application at", TARGET / 'index.html')
"""

with open(SOURCE_BUILD, "w", encoding="utf-8") as f:
    f.write(new_build_script)

print("Rewrote scripts/build_html_dashboard.py to use modular template!")
