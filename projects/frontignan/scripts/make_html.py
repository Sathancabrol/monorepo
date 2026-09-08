# -*- coding: utf-8 -*-
"""Convertit le rapport Markdown en HTML autonome (images en base64, CSS intégré)."""
import base64, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
NAME = sys.argv[1] if len(sys.argv) > 1 else "rapport-frontignan-analyse-territoriale"
MD = os.path.join(BASE, NAME + ".md")
OUT = os.path.join(BASE, NAME + ".html")

import markdown
text = open(MD, encoding="utf-8").read()

# Images -> data URI
def img_to_datauri(m):
    alt, path = m.group(1), m.group(2)
    p = os.path.join(BASE, path)
    if not os.path.exists(p):
        return m.group(0)
    ext = p.rsplit(".", 1)[-1].lower()
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "gif": "image/gif"}.get(ext, "image/png")
    data = base64.b64encode(open(p, "rb").read()).decode("ascii")
    return f'![{alt}](data:{mime};base64,{data})'

text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', img_to_datauri, text)

html_body = markdown.markdown(text, extensions=["tables", "sane_lists", "smarty"], output_format="html5")

CSS = """
:root { --dark:#0F4C5C; --teal:#1B7F8C; --gold:#C99A2E; --ink:#1d2b30; --soft:#f4f7f8; }
* { box-sizing: border-box; }
body { font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; color: var(--ink);
       max-width: 980px; margin: 0 auto; padding: 40px 56px 80px; line-height: 1.62;
       font-size: 15.5px; background: #fff; }
h1 { color: var(--dark); font-size: 30px; border-bottom: 4px solid var(--gold); padding-bottom: 10px; margin-top: 8px; line-height:1.25; }
h2 { color: var(--dark); font-size: 22px; margin-top: 44px; border-left: 6px solid var(--teal); padding-left: 12px; page-break-after: avoid; line-height:1.3; }
h3 { color: var(--teal); font-size: 17.5px; margin-top: 30px; page-break-after: avoid; }
h4 { color: var(--dark); font-size: 15.5px; }
p { margin: 10px 0; text-align: justify; hyphens: auto; }
a { color: var(--teal); text-decoration: none; border-bottom: 1px dotted var(--teal); }
a:hover { color: var(--dark); }
img { max-width: 100%; height: auto; display: block; margin: 26px auto; border: 1px solid #e2e8ea; border-radius: 6px; box-shadow: 0 2px 10px rgba(15,76,92,.08); }
table { border-collapse: collapse; width: 100%; margin: 18px 0; font-size: 13.2px; page-break-inside: avoid; }
th { background: var(--dark); color: #fff; text-align: left; padding: 8px 10px; font-weight: 600; vertical-align: top; }
td { border: 1px solid #d9e1e4; padding: 7px 10px; vertical-align: top; }
tr:nth-child(even) td { background: var(--soft); }
blockquote { border-left: 5px solid var(--gold); background: #fdf9ef; margin: 16px 0; padding: 12px 18px; border-radius: 0 6px 6px 0; }
blockquote p { text-align: left; }
code { background: #eef2f3; padding: 1px 5px; border-radius: 4px; font-size: 13px; }
hr { border: none; border-top: 2px dashed #cfdae0; margin: 34px 0; }
li { margin: 4px 0; }
strong { color: #123; }
@media print {
  body { padding: 0; font-size: 11.5px; max-width: 100%; }
  h1 { font-size: 24px; } h2 { font-size: 18px; page-break-before: auto; } h3 { font-size: 14px; }
  table { font-size: 10px; } img { max-height: 88mm; }
  a { color: var(--dark); }
  @page { size: A4; margin: 14mm 12mm; }
}
"""
html_doc = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Frontignan la Peyrade — document (sept. 2026)</title>
<style>{CSS}</style></head><body>
{html_body}
</body></html>"""

open(OUT, "w", encoding="utf-8").write(html_doc)
print("OK :", OUT, "-", round(os.path.getsize(OUT)/1024), "Ko")
