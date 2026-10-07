#!/usr/bin/env python3
import re

with open("scripts/section_js_part3.py", "r", encoding="utf-8") as f:
    text = f.read()

# Let's inspect if closing triple quotes is at the end
# First, let's find the def get_js_part3():
p_start = text.find('def get_js_part3():')
print("Found get_js_part3 at", p_start)

# Let's check where the triple quotes were
# We want the file to start with:
# def get_js_part3():
#     return r"""
#     ...
# """
# Using raw string r""" avoids any backslash issues!

# Let's locate the python code part
# Let's see if there are any triple quotes before the end
# Let's find all triple quotes
tq_matches = [m.start() for m in re.finditer(r'"""', text)]
print("Triple quote positions:", tq_matches)

# Let's clean up
# Keep from def get_js_part3():\n    return r"""
# and end with \n"""\n
js_content = text
if p_start != -1:
    first_tq = text.find('"""', p_start)
    if first_tq != -1:
        # extract JS content between first_tq+3 and last_tq
        last_tq = text.rfind('"""')
        if last_tq > first_tq:
            js_body = text[first_tq+3:last_tq]
        else:
            js_body = text[first_tq+3:]
    else:
        js_body = text
else:
    js_body = text

# In js_body, let's fix any occurrences of 'd\'ensablement' or similar that got distorted
js_body = js_body.replace("d'ensablement", "d ensablement").replace("d'érosion", "d erosion").replace("d'éclairage", "d eclairage").replace("d'équilibre", "d equilibre").replace("d'approvisionnement", "d approvisionnement").replace("d'intervention", "d intervention").replace("d'intempérie", "d intemperie").replace("d'intempéries", "d intemperies").replace("d'accueil", "d accueil").replace("d'évaluation", "d evaluation").replace("d'heures", "d heures").replace("d'emploi", "d emploi").replace("d'écoulement", "d ecoulement").replace("d'ajutage", "d ajutage")
# Fix any double backslash escapes if raw string
fixed_text = 'def get_js_part3():\n    return r"""' + js_body.rstrip() + '\n"""\n'

with open("scripts/section_js_part3.py", "w", encoding="utf-8") as f:
    f.write(fixed_text)

print("scripts/section_js_part3.py fixed with raw string literal!")
