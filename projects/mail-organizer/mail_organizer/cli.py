"""Interface en ligne de commande de mail-organizer.

Commandes :
  check        teste la connexion et liste les dossiers
  plan         analyse la boîte source sans rien déplacer
  organize     classe les messages dans les dossiers (rien n'est supprimé)
  attachments  télécharge les pièces jointes d'un dossier
  watch        organise en continu toutes les N secondes
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .client import MailClient
from .config import Settings, load_settings
from .organizer import collect_attachments, organize, plan, watch


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mail-organizer",
        description="Tri automatique d'une boîte mail via IMAP (Gmail, Outlook/Hotmail…).",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--config", default=None, help="chemin du config.json")
    parser.add_argument("--env", default=None, help="chemin du fichier .env")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check", help="tester la connexion et lister les dossiers")

    p_plan = sub.add_parser("plan", help="analyser sans rien déplacer")
    p_plan.add_argument("--limit", type=int, default=None,
                        help="analyser seulement les N messages les plus récents")

    p_org = sub.add_parser("organize", help="classer les messages dans les dossiers")
    p_org.add_argument("--limit", type=int, default=None,
                       help="ne traiter que les N messages les plus récents")

    p_att = sub.add_parser("attachments", help="télécharger les pièces jointes")
    p_att.add_argument("--folder", default=None,
                       help="dossier à parcourir (défaut : dossier source)")
    p_att.add_argument("--dest", default=None,
                       help="répertoire de destination (défaut : ./var/attachments)")
    p_att.add_argument("--limit", type=int, default=None)
    p_att.add_argument("--min-size", type=int, default=1,
                       help="taille minimale en octets")

    p_watch = sub.add_parser("watch", help="organiser en continu")
    p_watch.add_argument("--interval", type=int, default=900,
                         help="secondes entre deux passes (défaut 900)")
    p_watch.add_argument("--limit", type=int, default=None)

    return parser


def _connect(settings: Settings) -> MailClient:
    client = MailClient(settings.host, settings.user, settings.password, settings.port)
    try:
        client.connect()
    except Exception as exc:
        raise SystemExit(
            f"Connexion IMAP impossible ({settings.host}) : {exc}\n"
            "Vérifiez MAIL_HOST / MAIL_USER / MAIL_APP_PASSWORD dans .env — "
            "il faut un mot de passe d'application (voir README.md)."
        )
    return client


def cmd_check(settings: Settings) -> None:
    client = _connect(settings)
    try:
        print(f"Connecté à {settings.host} en tant que {settings.user}")
        folders = client.folders()
        print(f"{len(folders)} dossier(s) :")
        for name in sorted(folders):
            print(f"  - {name}")
        count = client.select(settings.source_folder, readonly=True)
        print(f"\n« {settings.source_folder} » contient {count} message(s).")
        print(f"{len(settings.rules)} règle(s) chargée(s).")
    finally:
        client.close()


def cmd_plan(settings: Settings, limit: int | None) -> None:
    client = _connect(settings)
    try:
        plan(settings, client, limit)
    finally:
        client.close()


def cmd_organize(settings: Settings, limit: int | None) -> None:
    client = _connect(settings)
    try:
        organize(settings, client, limit)
    finally:
        client.close()


def cmd_attachments(settings: Settings, folder: str | None, dest: str | None,
                    limit: int | None, min_size: int) -> None:
    client = _connect(settings)
    folder = folder or settings.source_folder
    dest_dir = Path(dest) if dest else Path(__file__).resolve().parent.parent / "var" / "attachments"
    try:
        saved = collect_attachments(settings, client, folder, dest_dir, limit, min_size)
        print(f"\n{len(saved)} fichier(s) téléchargé(s) dans {dest_dir}")
    finally:
        client.close()


def cmd_watch(settings: Settings, interval: int, limit: int | None) -> None:
    client = _connect(settings)
    try:
        watch(settings, client, interval, limit)
    finally:
        client.close()


def main(argv: list[str] | None = None) -> None:
    args = _build_parser().parse_args(argv)
    try:
        settings = load_settings(args.config, args.env)
    except SystemExit as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    if args.command == "check":
        cmd_check(settings)
    elif args.command == "plan":
        cmd_plan(settings, args.limit)
    elif args.command == "organize":
        cmd_organize(settings, args.limit)
    elif args.command == "attachments":
        cmd_attachments(settings, args.folder, args.dest, args.limit, args.min_size)
    elif args.command == "watch":
        cmd_watch(settings, args.interval, args.limit)


if __name__ == "__main__":
    main()
