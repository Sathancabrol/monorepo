"""Orchestration : plan (analyse), organize (classement), pièces jointes, watch."""

from __future__ import annotations

import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from .client import MailClient, iter_attachments
from .config import Settings
from .rules import MessageMeta, classify, top_domains


def _slug(folder: str) -> str:
    slug = folder.replace("/", "__")
    return re.sub(r'[<>:"\\|?*\x00-\x1f]', "_", slug).strip() or "dossier"


def scan(client: MailClient, folder: str, limit: int | None = None) -> list[MessageMeta]:
    count = client.select(folder, readonly=True)
    uids = client.uids()
    uids.sort(reverse=True)  # les plus récents d'abord
    if limit:
        uids = uids[:limit]
    metas = client.fetch_metas(uids)
    return [metas[u] for u in uids if u in metas]


def plan(settings: Settings, client: MailClient, limit: int | None = None) -> Counter:
    """Analyse sans rien déplacer : répartition prévue par dossier."""
    metas = scan(client, settings.source_folder, limit)
    counts: Counter = Counter()
    for meta in metas:
        counts[classify(meta, settings.rules, settings.default_folder)] += 1

    print(f"\nAnalyse de « {settings.source_folder} » — {len(metas)} message(s) "
          f"(sur {len(client.uids()) if not limit else 'échantillon'})\n")
    for folder, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {n:>6}  → {folder}")

    print("\nDomaines d'expéditeurs les plus fréquents :")
    for dom, n in top_domains(metas):
        print(f"  {n:>6}  {dom}")
    print("\nAstuce : ajoutez des règles pour les gros domaines non classés "
          "(voir config.example.json).")
    return counts


def organize(settings: Settings, client: MailClient, limit: int | None = None,
             quiet: bool = False) -> dict[str, int]:
    """Classe les messages du dossier source vers leurs dossiers cibles.

    Retourne {dossier: nb déplacés}. Ne supprime jamais rien : les messages
    quittent uniquement le dossier source.
    """
    metas = scan(client, settings.source_folder, limit)
    if not metas:
        if not quiet:
            print(f"« {settings.source_folder} » est vide : rien à trier.")
        return {}

    groups: dict[str, list[int]] = {}
    for meta in metas:
        folder = classify(meta, settings.rules, settings.default_folder)
        groups.setdefault(folder, []).append(meta.uid)

    client.select(settings.source_folder, readonly=False)
    summary: dict[str, int] = {}
    for folder, uids in sorted(groups.items()):
        moved = client.move_uids(uids, folder)
        summary[folder] = summary.get(folder, 0) + moved
        if not quiet:
            print(f"  {moved:>6}  message(s) → {folder}")
    if not quiet:
        total = sum(summary.values())
        print(f"\nTerminé : {total} message(s) classé(s), 0 supprimé.")
    return summary


def collect_attachments(settings: Settings, client: MailClient, folder: str,
                        dest_dir: Path, limit: int | None = None,
                        min_size: int = 1) -> list[Path]:
    """Télécharge les pièces jointes d'un dossier dans dest_dir/<dossier>/.

    Les fichiers sont préfixés par la date du message pour l'ordre chronologique.
    """
    metas = scan(client, folder, limit)
    client.select(folder, readonly=True)
    out_root = dest_dir / _slug(folder)
    saved: list[Path] = []
    for meta in metas:
        msg = client.fetch_message(meta.uid)
        if msg is None:
            continue
        stamp = _date_stamp(meta.date)
        for filename, payload in iter_attachments(msg):
            if len(payload) < min_size:
                continue
            out_root.mkdir(parents=True, exist_ok=True)
            dest = _unique_path(out_root / f"{stamp}_{_safe_name(filename)}")
            dest.write_bytes(payload)
            saved.append(dest)
            print(f"  ↓ {dest} ({len(payload)} octets)")
    if not saved:
        print(f"Aucune pièce jointe trouvée dans « {folder} ».")
    return saved


def _date_stamp(date_header: str) -> str:
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(date_header)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _safe_name(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name)
    return name.strip()[:150] or "piece_jointe"


def _unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    for i in range(1, 1000):
        cand = path.with_name(f"{stem} ({i}){suffix}")
        if not cand.exists():
            return cand
    return path.with_name(f"{stem}_{int(time.time())}{suffix}")


def watch(settings: Settings, client: MailClient, interval: int,
          limit: int | None = None) -> None:
    """Boucle infinie : organise la boîte toutes les `interval` secondes."""
    print(f"Mode watch : tri de « {settings.source_folder} » toutes les "
          f"{interval}s. Ctrl-C pour arrêter.")
    try:
        while True:
            stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n[{stamp}] passe de tri…")
            try:
                organize(settings, client, limit, quiet=True)
            except Exception as exc:  # reconnexion silencieuse au prochain tour
                print(f"  erreur : {exc}", file=sys.stderr)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nWatch arrêté.")
