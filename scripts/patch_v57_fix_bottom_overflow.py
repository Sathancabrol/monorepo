#!/usr/bin/env python3
"""
Patch v57: Fix bottom of page overflow, missing <div in modals, unclosed script tag in js_part3, and add generous bottom padding
"""

import re

# 1. Fix scripts/section_modals.py
with open("scripts/section_modals.py", "r", encoding="utf-8") as f:
    modals_text = f.read()

# Fix missing <div in modal-add-livraison
modals_text = modals_text.replace(
    '</div>\n    </div>\nid="modal-add-livraison"',
    '</div>\n    </div>\n\n    <!-- ========================================== -->\n    <!-- MODAL: AJOUTER BON DE LIVRAISON / PESEE    -->\n    <!-- ========================================== -->\n    <div id="modal-add-livraison"'
)

# Also check for any direct id="modal-add-livraison" without <div
modals_text = re.sub(
    r'(?<!<div\s)id="modal-add-livraison"',
    '<div id="modal-add-livraison"',
    modals_text
)

with open("scripts/section_modals.py", "w", encoding="utf-8") as f:
    f.write(modals_text)

print("Fixed section_modals.py div tags!")

# 2. Fix scripts/section_js_part3.py
with open("scripts/section_js_part3.py", "r", encoding="utf-8") as f:
    js_text = f.read()

# Ensure </script> is present right before closing triple quotes
js_text = js_text.rstrip()
if js_text.endswith('"""'):
    js_text = js_text[:-3].rstrip()
    if not js_text.endswith('</script>'):
        js_text = js_text + '\n</script>\n'
    js_text = js_text + '"""\n'

with open("scripts/section_js_part3.py", "w", encoding="utf-8") as f:
    f.write(js_text)

print("Fixed section_js_part3.py script closing tag!")

# 3. Add bottom padding to .tab-panel and main content in scripts/section_head_and_styles.py
with open("scripts/section_head_and_styles.py", "r", encoding="utf-8") as f:
    styles_text = f.read()

styles_text = styles_text.replace(
    ".tab-panel {\n            display: none;",
    ".tab-panel {\n            display: none;\n            padding-bottom: 5rem;"
)

with open("scripts/section_head_and_styles.py", "w", encoding="utf-8") as f:
    f.write(styles_text)

print("Fixed section_head_and_styles.py bottom padding!")
