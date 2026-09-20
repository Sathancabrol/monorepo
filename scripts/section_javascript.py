from scripts.section_js_part1 import get_js_part1
from scripts.section_js_part2 import get_js_part2
from scripts.section_js_part3 import get_js_part3

def get_javascript():
    return get_js_part1() + "\n" + get_js_part2() + "\n" + get_js_part3()

def get_complete_javascript():
    return get_javascript()
