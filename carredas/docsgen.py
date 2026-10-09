# -*- coding: utf-8 -*-
"""Génération de documents : Markdown, HTML, DOCX, PPTX, CSV, Gantt SVG.

Tout est écrit avec la bibliothèque standard (`zipfile` + chaînes XML).
Conséquence voulue : aucune dépendance à installer, donc un poste fraîchement
installé produit un .docx et un .pptx valides dès la première seconde.

Modèle de document (dict) :
    {
      "titre": "...", "sous_titre": "...",
      "meta": {"Date": "...", "Lieu": "...", ...},
      "blocs": [
        {"type": "h1"|"h2"|"h3"|"p"|"quote"|"note", "texte": "..."},
        {"type": "ul"|"ol", "items": ["..."]},
        {"type": "kv", "items": [["Clé", "Valeur"]]},
        {"type": "table", "entetes": [...], "lignes": [[...]]},
        {"type": "hr"}, {"type": "vide"}
      ]
    }
"""

from __future__ import annotations

import csv
import datetime as _dt
import io
import zipfile
from xml.sax.saxutils import escape as _xesc

# ----------------------------------------------------------------- utilitaires


def esc(t) -> str:
    return _xesc(str(t if t is not None else ""))


def _today() -> str:
    return _dt.date.today().strftime("%d/%m/%Y")


def _now() -> str:
    return _dt.datetime.now().strftime("%d/%m/%Y %H:%M")


def _lines(text) -> list[str]:
    return [l for l in str(text or "").split("\n")]


# -------------------------------------------------------------------- Markdown


def to_markdown(doc: dict) -> str:
    o = io.StringIO()
    if doc.get("titre"):
        o.write(f"# {doc['titre']}\n\n")
    if doc.get("sous_titre"):
        o.write(f"*{doc['sous_titre']}*\n\n")
    for k, v in (doc.get("meta") or {}).items():
        o.write(f"**{k}** : {v}  \n")
    if doc.get("meta"):
        o.write("\n")
    for b in doc.get("blocs") or []:
        t = b.get("type")
        if t in ("h1", "h2", "h3"):
            o.write(f"\n{'#' * int(t[1])} {b.get('texte','')}\n\n")
        elif t == "p":
            o.write(f"{b.get('texte','')}\n\n")
        elif t in ("ul", "ol"):
            for i, it in enumerate(b.get("items") or [], 1):
                o.write(f"{'- ' if t == 'ul' else f'{i}. '}{it}\n")
            o.write("\n")
        elif t == "kv":
            for k, v in b.get("items") or []:
                o.write(f"- **{k}** : {v}\n")
            o.write("\n")
        elif t == "table":
            ent = b.get("entetes") or []
            o.write("| " + " | ".join(str(x) for x in ent) + " |\n")
            o.write("|" + "|".join(["---"] * len(ent)) + "|\n")
            for row in b.get("lignes") or []:
                o.write("| " + " | ".join(str(x).replace("|", "/") for x in row) + " |\n")
            o.write("\n")
        elif t == "quote":
            o.write("> " + "\n> ".join(_lines(b.get("texte"))) + "\n\n")
        elif t == "note":
            o.write(f"> ℹ️ {b.get('texte','')}\n\n")
        elif t in ("hr", "vide"):
            o.write("\n---\n\n" if t == "hr" else "\n")
    o.write(f"\n\n_Document généré par Carré d'As le {_now()}._\n")
    return o.getvalue()


def to_text(doc: dict) -> str:
    """Version texte brut : pour un courriel, un SMS, un presse-papier."""
    o = io.StringIO()
    if doc.get("titre"):
        o.write(f"{doc['titre']}\n{'=' * len(doc['titre'])}\n\n")
    if doc.get("sous_titre"):
        o.write(f"{doc['sous_titre']}\n\n")
    for k, v in (doc.get("meta") or {}).items():
        o.write(f"{k} : {v}\n")
    if doc.get("meta"):
        o.write("\n")
    for b in doc.get("blocs") or []:
        t = b.get("type")
        if t in ("h1", "h2", "h3"):
            o.write(f"\n{b.get('texte','').upper()}\n{'-' * len(str(b.get('texte','')))}\n")
        elif t == "p":
            o.write(f"{b.get('texte','')}\n\n")
        elif t in ("ul", "ol"):
            for i, it in enumerate(b.get("items") or [], 1):
                o.write(f"  {'•' if t == 'ul' else str(i) + '.'} {it}\n")
            o.write("\n")
        elif t == "kv":
            for k, v in b.get("items") or []:
                o.write(f"  {k} : {v}\n")
            o.write("\n")
        elif t == "table":
            ent = [str(x) for x in (b.get("entetes") or [])]
            lignes = [[str(x) for x in r] for r in (b.get("lignes") or [])]
            widths = [max([len(ent[i])] + [len(r[i]) for r in lignes if i < len(r)] or [0])
                      for i in range(len(ent))]
            o.write("  ".join(e.ljust(widths[i]) for i, e in enumerate(ent)) + "\n")
            o.write("  ".join("-" * w for w in widths) + "\n")
            for r in lignes:
                o.write("  ".join((r[i] if i < len(r) else "").ljust(widths[i])
                                   for i in range(len(ent))) + "\n")
            o.write("\n")
        elif t == "quote":
            o.write(f"{b.get('texte','')}\n\n")
    return o.getvalue()


# ------------------------------------------------------------------------ HTML

_HTML_CSS = """
:root{--bg:#050508;--panel:#0F0F1A;--line:#23233A;--tx:#E8E8F0;--dim:#8A8AA8;--ac:#00E5CC;--warn:#FFB020;--bad:#FF3366}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);
font:15px/1.6 Inter,"Segoe UI",system-ui,sans-serif}
.wrap{max-width:900px;margin:0 auto;padding:48px 28px 80px}
h1{font-size:30px;letter-spacing:-.02em;margin:0 0 6px}
.sub{color:var(--dim);margin:0 0 22px;font-size:15px}
.meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px;
background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin-bottom:30px}
.meta div{font-size:13px}.meta b{display:block;color:var(--dim);font-weight:500;font-size:11px;
letter-spacing:.08em;text-transform:uppercase;margin-bottom:3px}
h2{font-size:19px;margin:34px 0 12px;padding-bottom:8px;border-bottom:1px solid var(--line)}
h3{font-size:15px;margin:22px 0 8px;color:var(--ac);letter-spacing:.02em}
p{margin:0 0 12px}ul,ol{margin:0 0 14px;padding-left:20px}li{margin:4px 0;color:#D6D6E4}
blockquote{margin:14px 0;padding:12px 16px;border-left:3px solid var(--ac);
background:var(--panel);color:#C9C9DC;border-radius:0 8px 8px 0}
table{width:100%;border-collapse:collapse;margin:12px 0 20px;font-size:14px}
th{text-align:left;font-size:11px;letter-spacing:.08em;text-transform:uppercase;
color:var(--dim);border-bottom:1px solid var(--line);padding:8px 10px;font-weight:600}
td{border-bottom:1px solid #171728;padding:9px 10px;vertical-align:top}
tr:hover td{background:#0C0C16}
hr{border:0;border-top:1px solid var(--line);margin:30px 0}
.foot{margin-top:44px;padding-top:16px;border-top:1px solid var(--line);
color:var(--dim);font-size:12px}
.tag{display:inline-block;padding:2px 8px;border-radius:99px;font-size:11px;
background:#12233A;color:#7FD4FF;border:1px solid #1E3A5C;margin-right:6px}
.tag.act{background:#3A2A12;color:#FFCC7A;border-color:#5C441E}
.tag.ris{background:#3A1220;color:#FF8FA6;border-color:#5C1E31}
.tag.ok{background:#12332C;color:#7AFFD8;border-color:#1E5C4C}
@media print{body{background:#fff;color:#111}
.wrap{max-width:none;padding:0}h2{border-color:#ccc}td,th{border-color:#ddd;color:#111}
li{color:#222}.meta{background:#f6f6f6;border-color:#ddd}}
"""


def to_html(doc: dict, standalone=True) -> str:
    b = io.StringIO()
    if doc.get("titre"):
        b.write(f"<h1>{esc(doc['titre'])}</h1>")
    if doc.get("sous_titre"):
        b.write(f'<p class="sub">{esc(doc["sous_titre"])}</p>')
    meta = doc.get("meta") or {}
    if meta:
        b.write('<div class="meta">')
        for k, v in meta.items():
            b.write(f"<div><b>{esc(k)}</b>{esc(v)}</div>")
        b.write("</div>")
    for blk in doc.get("blocs") or []:
        t = blk.get("type")
        if t in ("h1", "h2", "h3"):
            b.write(f"<{t}>{esc(blk.get('texte',''))}</{t}>")
        elif t == "p":
            b.write(f"<p>{esc(blk.get('texte','')).replace(chr(10), '<br>')}</p>")
        elif t in ("ul", "ol"):
            tag = "ul" if t == "ul" else "ol"
            b.write(f"<{tag}>")
            for it in blk.get("items") or []:
                b.write(f"<li>{esc(it)}</li>")
            b.write(f"</{tag}>")
        elif t == "kv":
            b.write('<div class="meta">')
            for k, v in blk.get("items") or []:
                b.write(f"<div><b>{esc(k)}</b>{esc(v)}</div>")
            b.write("</div>")
        elif t == "table":
            b.write("<table><thead><tr>")
            for h in blk.get("entetes") or []:
                b.write(f"<th>{esc(h)}</th>")
            b.write("</tr></thead><tbody>")
            for row in blk.get("lignes") or []:
                b.write("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in row) + "</tr>")
            b.write("</tbody></table>")
        elif t == "quote":
            b.write(f"<blockquote>{esc(blk.get('texte',''))}</blockquote>")
        elif t == "note":
            b.write(f'<blockquote>{esc(blk.get("texte",""))}</blockquote>')
        elif t == "hr":
            b.write("<hr>")
        elif t == "vide":
            b.write("<p></p>")
    b.write(f'<div class="foot">Document généré par Carré d\'As — {_now()}'
            f' — imprimable (Ctrl+P).</div>')
    if not standalone:
        return b.getvalue()
    return ("<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{esc(doc.get('titre','Document'))}</title>"
            f"<style>{_HTML_CSS}</style></head><body><div class='wrap'>"
            + b.getvalue() + "</div></body></html>")


# ----------------------------------------------------------------- CSV / table


def to_csv(entetes: list, lignes: list, sep=";") -> bytes:
    """CSV avec BOM UTF-8 et point-virgule : s'ouvre correctement dans Excel FR."""
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=sep, quoting=csv.QUOTE_MINIMAL, lineterminator="\r\n")
    w.writerow(list(entetes))
    for r in lignes:
        w.writerow(["" if c is None else c for c in r])
    return "\ufeff".encode("utf-8") + buf.getvalue().encode("utf-8")


# ------------------------------------------------------------------- Gantt SVG


def gantt_svg(taches: list, titre: str = "Planning", largeur=1100) -> str:
    """Diagramme de Gantt SVG autonome (aucune librairie)."""
    def d(s):
        if not s:
            return None
        for f in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%dT%H:%M:%S"):
            try:
                return _dt.datetime.strptime(str(s)[:10], f).date()
            except Exception:
                continue
        return None

    items = []
    for t in taches:
        a, z = d(t.get("debut")), d(t.get("fin"))
        if not a:
            continue
        items.append({"nom": t.get("label") or t.get("nom") or "—",
                      "deb": a, "fin": z or a, "resp": t.get("responsable") or "",
                      "av": float(t.get("avancement") or 0)})
    if not items:
        return ("<svg xmlns='http://www.w3.org/2000/svg' width='400' height='80'>"
                "<rect width='400' height='80' fill='#050508'/>"
                "<text x='20' y='44' fill='#8A8AA8' font-family='sans-serif' "
                "font-size='13'>Aucune tâche datée</text></svg>")

    start = min(i["deb"] for i in items)
    end = max(i["fin"] for i in items)
    total = max((end - start).days, 1)

    # bornes mensuelles
    mois = []
    cur = _dt.date(start.year, start.month, 1)
    while cur <= end:
        if cur >= start:
            mois.append(cur)
        cur = (_dt.date(cur.year + (cur.month == 12), (cur.month % 12) + 1, 1))
    if not mois:
        mois = [start]

    gl, hd, rh, pad = 300, 54, 34, 26
    width = largeur
    plot = max(width - gl - pad * 2, 200)
    height = hd + rh * len(items) + 46
    sx = lambda dt: gl + pad + (dt - start).days * plot / total

    o = io.StringIO()
    o.write(f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' "
            "font-family='Inter, Segoe UI, sans-serif'>")
    o.write(f"<rect width='{width}' height='{height}' fill='#08080F'/>")
    o.write(f"<text x='{pad}' y='30' fill='#E8E8F0' font-size='16' "
            f"font-weight='600'>{esc(titre)}</text>")
    for m in mois:
        x = sx(m)
        o.write(f"<line x1='{x:.1f}' y1='{hd - 12}' x2='{x:.1f}' y2='{hd + rh * len(items)}' "
                "stroke='#1C1C2E' stroke-width='1'/>")
        o.write(f"<text x='{x + 6:.1f}' y='{hd - 16}' fill='#8A8AA8' font-size='11'>"
                f"{m.strftime('%b %Y')}</text>")
    for n, it in enumerate(items):
        y = hd + n * rh
        if n % 2 == 0:
            o.write(f"<rect x='0' y='{y}' width='{width}' height='{rh}' fill='#0C0C16'/>")
        o.write(f"<text x='{pad}' y='{y + 21}' fill='#E8E8F0' font-size='12.5'>"
                f"{esc(it['nom'][:44])}</text>")
        x1, x2 = sx(it["deb"]), sx(it["fin"])
        w = max(x2 - x1, 6)
        o.write(f"<rect x='{x1:.1f}' y='{y + 8}' width='{w:.1f}' height='17' rx='4' "
                "fill='#12333A' stroke='#1E5C5C'/>")
        if it["av"] > 0:
            o.write(f"<rect x='{x1:.1f}' y='{y + 8}' width='{w * max(0, min(it['av'], 100)) / 100:.1f}' "
                    f"height='17' rx='4' fill='#00E5CC' opacity='.75'/>")
        o.write(f"<text x='{x1 + 8:.1f}' y='{y + 21}' fill='#04120F' font-size='10.5'>"
                f"{int(it['av'])} %</text>" if w > 46 else "")
        if it["resp"]:
            o.write(f"<text x='{x2 + 8:.1f}' y='{y + 21}' fill='#5A5A78' "
                    f"font-size='10.5'>{esc(it['resp'][:18])}</text>")
    o.write(f"<text x='{pad}' y='{height - 12}' fill='#4A4A6A' font-size='11'>"
            f"{start.strftime('%d/%m/%Y')} → {end.strftime('%d/%m/%Y')} · "
            f"{len(items)} tâche(s) · Carré d'As</text>")
    o.write("</svg>")
    return o.getvalue()


# ----------------------------------------------------------------------- DOCX


def _doc_styles() -> str:
    def st(sid, name, sz, bold, color, after, before=0, outline=None):
        ol = f'<w:outlineLvl w:val="{outline}"/>' if outline is not None else ""
        return (f'<w:style w:type="paragraph" w:styleId="{sid}">'
                f'<w:name w:val="{name}"/><w:basedOn w:val="Normal"/>'
                f'<w:qFormat/><w:pPr><w:spacing w:before="{before}" w:after="{after}"/></w:pPr>'
                f'<w:rPr><w:b w:val="{1 if bold else 0}"/><w:color w:val="{color}"/>'
                f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>{ol}</w:style>')

    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:docDefaults><w:rPrDefault><w:rPr>'
            '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>'
            '<w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:rPrDefault>'
            '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/>'
            '</w:pPr></w:pPrDefault></w:docDefaults>'
            '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
            '<w:name w:val="Normal"/><w:qFormat/></w:style>'
            + st("Title", "Title", 40, True, "1F3864", 120, 0, 0)
            + st("Subtitle", "Subtitle", 24, False, "595959", 240, 0, 1)
            + st("Heading1", "heading 1", 30, True, "0F5C58", 160, 320, 0)
            + st("Heading2", "heading 2", 25, True, "0F5C58", 120, 260, 1)
            + st("Heading3", "heading 3", 23, True, "2E2E3A", 100, 200, 2)
            + st("Quote", "Quote", 22, False, "3A3A4A", 160, 120)
            + "</w:styles>")


def _runs(text, bold=False, italic=False, size=None, color=None) -> str:
    props = []
    if bold:
        props.append('<w:b/>')
    if italic:
        props.append('<w:i/>')
    if size:
        props.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    if color:
        props.append(f'<w:color w:val="{color}"/>')
    rpr = f"<w:rPr>{''.join(props)}</w:rPr>" if props else ""
    out = []
    for i, line in enumerate(_lines(text)):
        if i:
            out.append(f"<w:r>{rpr}<w:br/></w:r>")
        out.append(f'<w:r>{rpr}<w:t xml:space="preserve">{esc(line)}</w:t></w:r>'
                   if line else f"<w:r>{rpr}</w:r>")
    return "".join(out)


def _para(text, style=None, bold=False, italic=False, size=None, color=None,
          align=None, after=None) -> str:
    ppr = []
    if style:
        ppr.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        ppr.append(f'<w:jc w:val="{align}"/>')
    if after is not None:
        ppr.append(f'<w:spacing w:after="{after}"/>')
    pprs = f"<w:pPr>{''.join(ppr)}</w:pPr>" if ppr else ""
    return f"<w:p>{pprs}{_runs(text, bold, italic, size, color)}</w:p>"


def _table_block(entetes, lignes) -> str:
    if not entetes:
        return ""
    borders = ('<w:tblBorders>'
               + "".join(f'<w:{k} w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
                         for k in ("top", "left", "bottom", "right", "insideH", "insideV"))
               + "</w:tblBorders>")
    xml = ['<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/>', borders,
           '<w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:left w:w="90" w:type="dxa"/>'
           '<w:bottom w:w="60" w:type="dxa"/><w:right w:w="90" w:type="dxa"/>'
           '</w:tblCellMar></w:tblPr><w:tblGrid>']
    for _ in entetes:
        xml.append('<w:gridCol w:w="2000"/>')
    xml.append("</w:tblGrid>")
    xml.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>')
    for h in entetes:
        xml.append('<w:tc><w:tcPr><w:tcW w:w="2000" w:type="dxa"/>'
                   '<w:shd w:val="clear" w:fill="E8F1F0"/></w:tcPr>'
                   + _para(str(h), bold=True, size=20) + "</w:tc>")
    xml.append("</w:tr>")
    for row in lignes or []:
        xml.append("<w:tr>")
        for c in row:
            xml.append('<w:tc><w:tcPr><w:tcW w:w="2000" w:type="dxa"/></w:tcPr>'
                       + _para(str(c if c is not None else ""), size=20) + "</w:tc>")
        xml.append("</w:tr>")
    xml.append("</w:tbl>")
    xml.append(_para("", size=8, after=60))
    return "".join(xml)


def _doc_body(doc: dict) -> str:
    out = []
    if doc.get("titre"):
        out.append(_para(doc["titre"], style="Title"))
    if doc.get("sous_titre"):
        out.append(_para(doc["sous_titre"], style="Subtitle", italic=True))
    for k, v in (doc.get("meta") or {}).items():
        out.append(f"<w:p><w:pPr><w:spacing w:after='40'/></w:pPr>"
                   + _runs(f"{k} : ", bold=True, size=20) + _runs(str(v), size=20) + "</w:p>")
    if doc.get("meta"):
        out.append(_para("", size=8, after=80))

    style_of = {"h1": "Heading1", "h2": "Heading2", "h3": "Heading3"}
    for b in doc.get("blocs") or []:
        t = b.get("type")
        if t in style_of:
            out.append(_para(b.get("texte", ""), style=style_of[t]))
        elif t == "p":
            out.append(_para(b.get("texte", "")))
        elif t in ("ul", "ol"):
            for it in b.get("items") or []:
                out.append('<w:p><w:pPr><w:pStyle w:val="ListParagraph"/>'
                           '<w:ind w:left="454"/><w:spacing w:after="40"/></w:pPr>'
                           + _runs(("• " if t == "ul" else "– ") + str(it), size=22) + "</w:p>")
            out.append(_para("", size=6, after=60))
        elif t == "kv":
            for k, v in b.get("items") or []:
                out.append(f"<w:p><w:pPr><w:spacing w:after='40'/></w:pPr>"
                           + _runs(f"{k} : ", bold=True, size=21) + _runs(str(v), size=21)
                           + "</w:p>")
            out.append(_para("", size=6, after=60))
        elif t == "table":
            out.append(_table_block(b.get("entetes") or [], b.get("lignes") or []))
        elif t in ("quote", "note"):
            out.append('<w:p><w:pPr><w:pStyle w:val="Quote"/><w:ind w:left="340"/>'
                       '<w:pBdr><w:left w:val="single" w:sz="12" w:space="8" w:color="00E5CC"/>'
                       '</w:pBdr></w:pPr>'
                       + _runs(b.get("texte", ""), italic=True) + "</w:p>")
        elif t == "hr":
            out.append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" '
                       'w:space="1" w:color="BFBFBF"/></w:pBdr></w:pPr></w:p>')
        elif t == "vide":
            out.append(_para("", after=80))
    out.append(_para(f"Document généré par Carré d'As — {_now()}", size=16,
                     color="808080", italic=True))
    return "".join(out)


def to_docx(doc: dict) -> bytes:
    body = _doc_body(doc)
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                f"<w:body>{body}"
                '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
                '<w:pgMar w:top="1417" w:right="1417" w:bottom="1417" w:left="1417" '
                'w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>'
                "</w:body></w:document>")
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
          '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
          "</Types>")
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
            "</Relationships>")
    drels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
             "</Relationships>")
    now = _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties '
            'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f"<dc:title>{esc(doc.get('titre','Document'))}</dc:title>"
            "<dc:creator>Carré d'As</dc:creator><cp:lastModifiedBy>Carré d'As</cp:lastModifiedBy>"
            f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>'
            f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>'
            "</cp:coreProperties>")
    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
           "<Application>CarreDAs</Application></Properties>")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", document)
        z.writestr("word/_rels/document.xml.rels", drels)
        z.writestr("word/styles.xml", _doc_styles())
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
    return buf.getvalue()


# ----------------------------------------------------------------------- PPTX

EMU_W, EMU_H = 12192000, 6858000


def _sp(sid, name, x, y, w, h, paragraphs, anchor="t"):
    """Forme texte simple."""
    ps = "".join(paragraphs)
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="{name}"/>'
            '<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square"><a:normAutofit/></a:bodyPr><a:lstStyle/>{ps}'
            '</p:txBody></p:sp>')


def _ap(text, size, bold=False, color="FFFFFF", bullet=False, level=0, space_before=0):
    if isinstance(text, (list, tuple)):
        runs = "".join(_ar(t, size, bold, color) for t in text)
    else:
        runs = _ar(text, size, bold, color)
    ppr = f'<a:pPr lvl="{max(level, 0)}" marL="{342900 * (level + 1)}" indent="-342900">'
    if bullet:
        ppr += '<a:buClr><a:srgbClr val="00E5CC"/></a:buClr><a:buSzPct val="80000"/>' \
               '<a:buFont typeface="Arial"/><a:buChar char="•"/>'
    else:
        ppr += '<a:buNone/>'
    if space_before:
        ppr += f'<a:spcBef><a:spcPts val="{space_before}"/></a:spcBef>'
    ppr += "</a:pPr>"
    return f"<a:p>{ppr}{runs}</a:p>"


def _ar(text, size, bold=False, color="FFFFFF"):
    return ('<a:r><a:rPr lang="fr-FR" sz="%d" b="%d" dirty="0">'
            '<a:solidFill><a:srgbClr val="%s"/></a:solidFill>'
            '<a:latin typeface="+mn-lt"/></a:rPr><a:t>%s</a:t></a:r>'
            % (size, 1 if bold else 0, color, esc(text)))


def _slide_xml(titre, lignes, sous_titre="", n=1, total=1):
    sh = []
    sh.append(f'<p:sp><p:nvSpPr><p:cNvPr id="1" name="Fond"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
              f'<p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{EMU_W}" cy="{EMU_H}"/></a:xfrm>'
              '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
              '<a:solidFill><a:srgbClr val="08080F"/></a:solidFill>'
              '<a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr/><a:lstStyle/>'
              '<a:p><a:endParaRPr lang="fr-FR"/></a:p></p:txBody></p:sp>')
    sh.append(f'<p:sp><p:nvSpPr><p:cNvPr id="2" name="Liseret"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
              f'<p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{EMU_W}" cy="45720"/></a:xfrm>'
              '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
              '<a:solidFill><a:srgbClr val="00E5CC"/></a:solidFill>'
              '<a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr/><a:lstStyle/>'
              '<a:p><a:endParaRPr lang="fr-FR"/></a:p></p:txBody></p:sp>')
    paras = [_ap(titre, 3200, True, "FFFFFF")]
    if sous_titre:
        paras.append(_ap(sous_titre, 1600, False, "8A8AA8", space_before=600))
    sh.append(_sp(3, "Titre", 685800, 640000, 10817000, 1500000, paras))
    body = []
    for ln in lignes:
        if isinstance(ln, tuple):
            txt, lvl = ln
        else:
            txt, lvl = ln, 0
        body.append(_ap(txt, 1800 if lvl == 0 else 1500, lvl == 0,
                        "E8E8F0" if lvl == 0 else "A8A8C4", bullet=(lvl > 0), level=max(lvl - 1, 0)))
    if body:
        sh.append(_sp(4, "Corps", 685800, 2320000, 10817000, 4000000, body))
    sh.append(_sp(5, "Pied", 685800, 6172000, 10817000, 350000,
                  [_ap(f"{n} / {total} · Carré d'As", 1000, False, "4A4A6A")]))
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
            "<p:cSld><p:spTree>"
            '<p:nvGrpSpPr><p:cNvPr id="0" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
            '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
            + "".join(sh) + "</p:spTree></p:cSld>"
            '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')


_THEME = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="CarreDAs">'
          '<a:themeElements>'
          '<a:clrScheme name="Nuit">'
          '<a:dk1><a:srgbClr val="08080F"/></a:dk1><a:lt1><a:srgbClr val="E8E8F0"/></a:lt1>'
          '<a:dk2><a:srgbClr val="1F2937"/></a:dk2><a:lt2><a:srgbClr val="A8A8C4"/></a:lt2>'
          '<a:accent1><a:srgbClr val="00E5CC"/></a:accent1>'
          '<a:accent2><a:srgbClr val="9B59B6"/></a:accent2>'
          '<a:accent3><a:srgbClr val="FFB020"/></a:accent3>'
          '<a:accent4><a:srgbClr val="4A90D9"/></a:accent4>'
          '<a:accent5><a:srgbClr val="FF3366"/></a:accent5>'
          '<a:accent6><a:srgbClr val="7FD4FF"/></a:accent6>'
          '<a:hlink><a:srgbClr val="7FD4FF"/></a:hlink><a:folHlink><a:srgbClr val="9B59B6"/></a:folHlink>'
          "</a:clrScheme>"
          '<a:fontScheme name="Inter"><a:majorFont><a:latin typeface="Inter"/>'
          '<a:ea typeface=""/><a:cs typeface=""/></a:majorFont>'
          '<a:minorFont><a:latin typeface="Inter"/><a:ea typeface=""/><a:cs typeface=""/>'
          "</a:minorFont></a:fontScheme>"
          '<a:fmtScheme name="Nuit">'
          '<a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
          '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
          '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>'
          '<a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
          '<a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
          '<a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>'
          '<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle>'
          '<a:effectStyle><a:effectLst/></a:effectStyle>'
          '<a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>'
          '<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
          '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
          '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>'
          "</a:fmtScheme></a:themeElements></a:theme>")


def to_pptx(diapos: list, titre_presentation="Présentation", sous_titre="") -> bytes:
    """`diapos` : [{"titre": str, "sous_titre": str, "lignes": [str | (str, niveau)]}]"""
    n = max(len(diapos), 1)
    slides = []
    for i, d in enumerate(diapos, 1):
        slides.append(_slide_xml(d.get("titre") or "", d.get("lignes") or [],
                                 d.get("sous_titre") or "", i, n))
    if not slides:
        slides.append(_slide_xml(titre_presentation, [], sous_titre, 1, 1))

    ct = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
          '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
          '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
          '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>']
    for i in range(len(slides)):
        ct.append(f'<Override PartName="/ppt/slides/slide{i + 1}.xml" '
                  'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
    ct.append('<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>')
    ct.append('<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>')
    ct.append("</Types>")

    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
            "</Relationships>")

    sld_ids = "".join(f'<p:sldId id="{256 + i}" r:id="rId{i + 2}"/>'
                      for i in range(len(slides)))
    pres = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
            'saveSubsetFonts="1">'
            '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
            f'<p:sldIdLst>{sld_ids}</p:sldIdLst>'
            f'<p:sldSz cx="{EMU_W}" cy="{EMU_H}" type="screen16x9"/>'
            f'<p:notesSz cx="{EMU_H}" cy="{EMU_W}"/>'
            "</p:presentation>")

    pres_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>']
    for i in range(len(slides)):
        pres_rels.append(f'<Relationship Id="rId{i + 2}" '
                         'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" '
                         f'Target="slides/slide{i + 1}.xml"/>')
    pres_rels.append("</Relationships>")

    master = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
              'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
              'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
              "<p:cSld><p:spTree>"
              '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
              '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
              '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
              "</p:spTree></p:cSld>"
              '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" '
              'accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" '
              'accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
              '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>'
              "</p:sldMaster>")
    master_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
                   '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>'
                   "</Relationships>")
    layout = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
              'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
              'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
              'type="blank" preserve="1">'
              "<p:cSld name=\"Vide\"><p:spTree>"
              '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
              '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
              '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
              "</p:spTree></p:cSld>"
              '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')
    layout_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>'
                   "</Relationships>")
    slide_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                  '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                  '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
                  "</Relationships>")
    now = _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties '
            'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f"<dc:title>{esc(titre_presentation)}</dc:title>"
            "<dc:creator>Carré d'As</dc:creator>"
            f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>'
            f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>'
            "</cp:coreProperties>")
    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
           "<Application>CarreDAs</Application></Properties>")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "".join(ct))
        z.writestr("_rels/.rels", rels)
        z.writestr("ppt/presentation.xml", pres)
        z.writestr("ppt/_rels/presentation.xml.rels", "".join(pres_rels))
        z.writestr("ppt/slideMasters/slideMaster1.xml", master)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", master_rels)
        z.writestr("ppt/slideLayouts/slideLayout1.xml", layout)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", layout_rels)
        z.writestr("ppt/theme/theme1.xml", _THEME)
        for i, s in enumerate(slides, 1):
            z.writestr(f"ppt/slides/slide{i}.xml", s)
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", slide_rels)
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
    return buf.getvalue()


# ------------------------------------------------------------------ rendu final

EXT = {"md": "text/markdown", "txt": "text/plain", "html": "text/html",
       "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
       "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
       "csv": "text/csv", "svg": "image/svg+xml", "json": "application/json"}


def render(fmt: str, doc: dict, diapos=None, entetes=None, lignes=None,
           taches=None, titre_gantt="Planning") -> tuple[bytes, str]:
    """Rend `(données, type MIME)` selon le format demandé."""
    f = (fmt or "md").lower()
    if f == "md":
        return to_markdown(doc).encode("utf-8"), EXT["md"]
    if f == "txt":
        return to_text(doc).encode("utf-8"), EXT["txt"]
    if f == "html":
        return to_html(doc).encode("utf-8"), EXT["html"]
    if f == "docx":
        return to_docx(doc), EXT["docx"]
    if f == "pptx":
        return to_pptx(diapos or _diapos_depuis_doc(doc)), EXT["pptx"]
    if f == "csv":
        return to_csv(entetes or [], lignes or []), EXT["csv"]
    if f == "svg":
        return gantt_svg(taches or [], titre_gantt).encode("utf-8"), EXT["svg"]
    if f == "json":
        import json as _json
        return _json.dumps(doc, ensure_ascii=False, indent=2).encode("utf-8"), EXT["json"]
    raise ValueError(f"format inconnu : {fmt}")


def _diapos_depuis_doc(doc: dict) -> list:
    """Secours : fabrique un jeu de diapositives depuis un document."""
    diapos = [{"titre": doc.get("titre") or "Présentation",
               "sous_titre": doc.get("sous_titre") or "", "lignes": []}]
    cur = None
    for b in doc.get("blocs") or []:
        t = b.get("type")
        if t == "h2":
            cur = {"titre": b.get("texte", ""), "lignes": []}
            diapos.append(cur)
        elif t in ("ul", "ol") and cur:
            for it in b.get("items") or []:
                cur["lignes"].append((str(it), 1))
        elif t == "p" and cur:
            cur["lignes"].append((b.get("texte", ""), 1))
        elif t == "table" and cur:
            cur["lignes"].append((" | ".join(str(x) for x in (b.get("entetes") or [])), 1))
            for r in (b.get("lignes") or [])[:8]:
                cur["lignes"].append((" | ".join(str(x) for x in r), 2))
    return [d for d in diapos if d.get("titre")] or diapos[:1]
