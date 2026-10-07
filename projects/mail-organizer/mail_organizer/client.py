"""Client IMAP minimaliste : dossiers, en-têtes, déplacements, pièces jointes.

Stratégie de « déplacement » volontairement prudente :
  COPY vers le dossier cible → marquer \\Deleted dans le dossier source →
  EXPUNGE. Sur Gmail, cela revient à ajouter le libellé cible et retirer le
  message de la boîte de réception (le message reste dans « Tous les
  messages », rien n'est supprimé). Sur Outlook, c'est un vrai déplacement.
"""

from __future__ import annotations

import email
import email.header
import imaplib
import re
from typing import Iterator

from .imap_utf7 import decode as utf7_decode
from .imap_utf7 import encode as utf7_encode
from .rules import MessageMeta

_UID_LINE = re.compile(rb"^(\d+) \(?")
HEADER_FIELDS = "(FROM TO SUBJECT DATE LIST-UNSUBSCRIBE)"


def decode_header_value(value: str | None) -> str:
    """Décode un en-tête éventuellement encodé RFC 2047 (=?utf-8?B?…?=)."""
    if not value:
        return ""
    parts = email.header.decode_header(value)
    chunks: list[str] = []
    for data, charset in parts:
        if isinstance(data, bytes):
            try:
                chunks.append(data.decode(charset or "utf-8", errors="replace"))
            except LookupError:
                chunks.append(data.decode("utf-8", errors="replace"))
        else:
            chunks.append(data)
    return " ".join(chunks).strip()


class MailClient:
    def __init__(self, host: str, user: str, password: str, port: int = 993):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.conn: imaplib.IMAP4_SSL | None = None
        self._current_folder: str | None = None
        self._readonly = False

    # --- connexion ---------------------------------------------------------

    def connect(self) -> None:
        self.conn = imaplib.IMAP4_SSL(self.host, self.port)
        typ, _ = self.conn.login(self.user, self.password)
        if typ != "OK":
            raise RuntimeError("Échec de l'authentification IMAP.")

    def close(self) -> None:
        if self.conn is not None:
            try:
                self.conn.logout()
            except Exception:
                pass
            self.conn = None
        self._current_folder = None

    def _require(self) -> imaplib.IMAP4_SSL:
        if self.conn is None:
            raise RuntimeError("Non connecté — appelez connect() d'abord.")
        return self.conn

    # --- dossiers ----------------------------------------------------------

    def folders(self) -> list[str]:
        conn = self._require()
        typ, data = conn.list()
        names: list[str] = []
        if typ != "OK":
            return names
        for line in data:
            if not isinstance(line, bytes):
                continue
            # format : (flags) "delim" "nom"  |  (flags) "delim" nom
            match = re.search(rb'\s"?([^"]+)"?\s*$', line)
            if match:
                names.append(utf7_decode(match.group(1)))
        return names

    def folder_exists(self, folder: str) -> bool:
        conn = self._require()
        typ, _ = conn.select(self._quote(folder), readonly=True)
        if typ == "OK":
            conn.close()
            return True
        return False

    def ensure_folder(self, folder: str) -> None:
        """Crée le dossier (et ses parents) s'il n'existe pas."""
        conn = self._require()
        parts = folder.split("/")
        for i in range(1, len(parts) + 1):
            partial = "/".join(parts[:i])
            typ, _ = conn.create(self._quote(partial))
            if typ != "OK":
                # déjà existant ou autre — on vérifie via select
                if not self.folder_exists(partial):
                    raise RuntimeError(f"Impossible de créer le dossier « {partial} ».")
        self._current_folder = None  # le CREATE peut invalider la sélection

    @staticmethod
    def _quote(folder: str) -> str:
        encoded = utf7_encode(folder)
        return f'"{encoded}"'

    # --- sélection / recherche ----------------------------------------------

    def select(self, folder: str, readonly: bool = False) -> int:
        conn = self._require()
        typ, data = conn.select(self._quote(folder), readonly=readonly)
        if typ != "OK":
            raise RuntimeError(f"Dossier introuvable : « {folder} ».")
        self._current_folder = folder
        self._readonly = readonly
        try:
            return int(data[0])
        except (TypeError, ValueError):
            return 0

    def uids(self) -> list[int]:
        """UIDs de tous les messages du dossier sélectionné."""
        conn = self._require()
        typ, data = conn.uid("SEARCH", None, "ALL")
        if typ != "OK" or not data or data[0] is None:
            return []
        return [int(u) for u in data[0].split()]

    # --- en-têtes ------------------------------------------------------------

    def fetch_metas(self, uids: list[int], batch: int = 100) -> dict[int, MessageMeta]:
        """Récupère les métadonnées de classement pour une liste d'UIDs."""
        conn = self._require()
        metas: dict[int, MessageMeta] = {}
        for i in range(0, len(uids), batch):
            chunk = uids[i:i + batch]
            rng = ",".join(str(u) for u in chunk)
            typ, data = conn.uid("FETCH", rng,
                                 f"(BODY.PEEK[HEADER.FIELDS {HEADER_FIELDS}])")
            if typ != "OK":
                continue
            for item in data:
                if not isinstance(item, tuple) or len(item) < 2:
                    continue
                envelope, payload = item[0], item[1]
                m = _UID_LINE.match(envelope)
                if not m:
                    continue
                uid = int(m.group(1))
                msg = email.message_from_bytes(payload)
                metas[uid] = MessageMeta(
                    uid=uid,
                    from_addr=decode_header_value(msg.get("From")),
                    subject=decode_header_value(msg.get("Subject")),
                    date=msg.get("Date", ""),
                    header_names=frozenset(k.lower() for k in msg.keys()),
                )
        return metas

    # --- déplacement ---------------------------------------------------------

    def move_uids(self, uids: list[int], target_folder: str, batch: int = 200) -> int:
        """COPY + \\Deleted + EXPUNGE depuis le dossier sélectionné (lecture-écriture)."""
        if not uids:
            return 0
        conn = self._require()
        if self._readonly:
            raise RuntimeError("Le dossier sélectionné est en lecture seule.")
        self.ensure_folder(target_folder)
        # ensure_folder a pu fermer la sélection : re-sélectionner si besoin
        if self._current_folder and self.conn.state != "SELECTED":
            self.select(self._current_folder, readonly=False)
        target = self._quote(target_folder)
        moved = 0
        for i in range(0, len(uids), batch):
            chunk = uids[i:i + batch]
            rng = ",".join(str(u) for u in chunk)
            typ, _ = conn.uid("COPY", rng, target)
            if typ != "OK":
                raise RuntimeError(f"COPY a échoué vers « {target_folder} ».")
            conn.uid("STORE", rng, "+FLAGS.SILENT", "(\\Deleted)")
            moved += len(chunk)
        conn.expunge()
        return moved

    # --- message complet / pièces jointes ------------------------------------

    def fetch_message(self, uid: int) -> email.message.Message | None:
        conn = self._require()
        typ, data = conn.uid("FETCH", str(uid), "(BODY.PEEK[])")
        if typ != "OK":
            return None
        for item in data:
            if isinstance(item, tuple) and len(item) >= 2:
                return email.message_from_bytes(item[1])
        return None


def iter_attachments(msg: email.message.Message) -> Iterator[tuple[str, bytes]]:
    """Parcourt les parties du message et rend (nom, contenu) des pièces jointes."""
    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue
        disposition = str(part.get("Content-Disposition") or "").lower()
        filename = part.get_filename()
        if not filename and "attachment" not in disposition:
            continue
        payload = part.get_payload(decode=True)
        if payload is None:
            continue
        if filename:
            filename = decode_header_value(filename)
        else:
            ext = (part.get_content_type() or "").split("/")[-1] or "bin"
            filename = f"piece_jointe.{ext}"
        yield filename, payload
