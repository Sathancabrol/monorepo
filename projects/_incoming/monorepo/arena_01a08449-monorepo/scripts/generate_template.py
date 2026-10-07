import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from section_head_and_styles import get_head_and_styles
from section_tab_panels import get_tab_panels
from section_modals import get_modals
from section_javascript import get_complete_javascript

def build_template():
    template_content = (
        get_head_and_styles() + "\n" +
        get_tab_panels() + "\n" +
        get_modals() + "\n" +
        get_complete_javascript() + "\n" +
        "</body>\n</html>"
    )
    
    out_path = Path('/home/user/monorepo/projects/btp-conduite-travaux/template.html')
    out_path.write_text(template_content, encoding='utf-8')
    print(f"template.html written successfully ({len(template_content)} bytes)")

if __name__ == "__main__":
    build_template()
