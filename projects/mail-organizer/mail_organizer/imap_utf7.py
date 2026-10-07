"""Encodage/décodage UTF-7 modifié (RFC 3501) pour les noms de dossiers IMAP.

Les noms de dossiers contenant des caractères non-ASCII (accents, émojis)
doivent être encodés en « modified UTF-7 » avant d'être envoyés au serveur
IMAP : séquences non-ASCII → UTF-16BE → base64 (avec ',' au lieu de '/'),
entourées de '&' et '-'. Le caractère '&' littéral s'écrit '&-'.
"""

import base64

_ASCII_MIN, _ASCII_MAX = 0x20, 0x7E


def encode(name: str) -> str:
    """Encode un nom de dossier Unicode en UTF-7 modifié (retourne str ASCII)."""
    out: list[str] = []
    buf = ""

    def flush() -> None:
        nonlocal buf
        if not buf:
            return
        b64 = base64.b64encode(buf.encode("utf-16-be")).decode("ascii")
        b64 = b64.replace("/", ",").rstrip("=")
        out.append("&" + b64 + "-")
        buf = ""

    for ch in name:
        code = ord(ch)
        if _ASCII_MIN <= code <= _ASCII_MAX:
            flush()
            out.append("&-" if ch == "&" else ch)
        else:
            buf += ch
    flush()
    return "".join(out)


def decode(name) -> str:
    """Décode un nom de dossier UTF-7 modifié vers Unicode."""
    if isinstance(name, bytes):
        name = name.decode("ascii")
    out: list[str] = []
    i = 0
    while i < len(name):
        ch = name[i]
        if ch == "&":
            j = name.index("-", i + 1)
            if j == i + 1:
                out.append("&")
            else:
                b64 = name[i + 1:j].replace(",", "/")
                pad = "=" * ((4 - len(b64) % 4) % 4)
                out.append(base64.b64decode(b64 + pad).decode("utf-16-be"))
            i = j + 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)
