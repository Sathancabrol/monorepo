from pathlib import Path
import re

template_path = Path("/home/user/monorepo/projects/btp-conduite-travaux/template.html")
with open(template_path, "r", encoding="utf-8") as f:
    text = f.read()

tabs = re.findall(r'<div id="(tab-[a-zA-Z0-9_]+)"', text)
print(f"Total tabs in template: {len(tabs)}")
for t in tabs:
    print(" -", t)

# Check all modals
modals = re.findall(r'<div class="modal-backdrop" id="([a-zA-Z0-9_-]+)"', text)
print(f"\nTotal modals in template: {len(modals)}")
for m in modals:
    print(" -", m)

