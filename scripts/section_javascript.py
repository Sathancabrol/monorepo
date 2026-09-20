import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from section_js_part1 import get_js_part1, get_js_part1_continued
from section_js_part2 import get_js_part2, get_js_part2_continued
from section_js_part3 import get_js_part3, get_js_part3_continued, get_js_helpers_and_actions

def get_complete_javascript():
    return (
        get_js_part1() +
        get_js_part1_continued() +
        get_js_part2() +
        get_js_part2_continued() +
        get_js_part3() +
        get_js_part3_continued() +
        get_js_helpers_and_actions()
    )

if __name__ == "__main__":
    js = get_complete_javascript()
    print(f"Aggregated JavaScript total size: {len(js)} bytes")
