# 📬 mail-organizer

> **Tri automatique d'une boîte mail via IMAP** — classement en dossiers par règles, extraction de pièces jointes, mode watch. **Zéro dépendance** (stdlib Python uniquement). Compatible **Gmail** et **Outlook.com / Hotmail**.

Conçu pour épiler une boîte de réception : les messages sont **déplacés** vers des dossiers, **jamais supprimés** (sur Gmail, le message reste dans « Tous les messages »).

## ⚙️ Installation

```bash
cd projects/mail-organizer
# rien à installer : Python 3.9+ suffit
python3 -m mail_organizer --help
```

## 🔑 Configuration (1 fois)

Créez `projects/mail-organizer/.env` (fichier ignoré par Git) :

```env
# Pour Gmail :
MAIL_HOST=imap.gmail.com
MAIL_USER=votre.adresse@gmail.com
MAIL_APP_PASSWORD=xxxxxxxxxxxxxxxx

# Pour Hotmail/Outlook.com :
# MAIL_HOST=outlook.office365.com
# MAIL_USER=nathancabrol@hotmail.fr
# MAIL_APP_PASSWORD=xxxxxxxxxxxxxxxx
```

**Le mot de passe d'application** (et non votre mot de passe habituel) :

- **Gmail** : compte Google → Sécurité → validation en deux étapes (obligatoire) → « Mots de passe des applications » → générer. Activez aussi IMAP : Gmail → Paramètres → *Transfert et POP/IMAP* → Activer l'IMAP.
- **Hotmail/Outlook.com** : compte Microsoft → Sécurité → Options de sécurité avancées → vérification en deux étapes → « Mot de passe d'application ».

## 🚀 Commandes

```bash
python3 -m mail_organizer check                     # test de connexion + liste des dossiers
python3 -m mail_organizer plan                      # analyse : qui irait où ? (rien ne bouge)
python3 -m mail_organizer plan --limit 500          # échantillon des 500 plus récents
python3 -m mail_organizer organize                  # classe la boîte source → dossiers
python3 -m mail_organizer organize --limit 1000     # par lots (prudent pour démarrer)
python3 -m mail_organizer attachments --folder "Achats et jeux vidéo"
python3 -m mail_organizer watch --interval 900      # tri en continu toutes les 15 min
```

Pièces jointes téléchargées dans `var/attachments/<dossier>/AAAA-MM-JJ_nom-du-fichier` (`var/` ignoré par Git).

## 🧠 Fonctionnement

1. Le dossier source (défaut `INBOX`) est lu **en lecture seule** pour l'analyse.
2. Chaque message est comparé aux règles de `config.json` — **la première règle qui gagne décide du dossier** ; sans règle → dossier par défaut `À trier`.
3. Les dossiers cibles sont créés automatiquement (sur Gmail : cela crée des libellés).
4. Déplacement prudent : `COPY` vers le dossier cible, puis retrait du dossier source. Aucun message n'est effacé.
5. `plan` affiche aussi les **domaines d'expéditeurs les plus fréquents** : parfait pour découvrir quelles règles ajouter.

## 🗂 Règles (config.json)

Copiez `config.example.json` en `config.json` puis adaptez. Chaque règle peut combiner :

```json
{
  "folder": "Dossier cible",
  "from_domains": ["exemple.fr"],
  "from_contains": ["adresse@exemple.fr"],
  "subject_contains": ["facture"],
  "has_header": ["list-unsubscribe"]
}
```

La comparaison ignore majuscules et accents. La règle incluse avec `has_header: ["list-unsubscribe"]` sert de **filet de sécurité newsletters**.

## 🧪 Tests

```bash
cd projects/mail-organizer
python3 -m unittest discover -s tests -v
```

## ⏰ Automatisation

```cron
# crontab : tri tous les quarts d'heure
*/15 * * * * cd /chemin/vers/projects/mail-organizer && python3 -m mail_organizer organize >> var/cron.log 2>&1
```

## ⚠️ Limites connues

- IMAP + mot de passe d'application : chez Microsoft, la politique d'authentification évolue régulièrement (OAuth2 obligatoire depuis 2026 pour de nombreux usages) ; si la connexion échoue, vérifiez que la vérification en deux étapes est active et régénérez le mot de passe d'application.
- Les règles ne voient que les en-têtes (expéditeur, sujet, présence de List-Unsubscribe) : c'est suffisant pour 95 % du tri, et très rapide même sur 20 000 messages.
- `attachments` télécharge le message complet : limitez avec `--limit` sur les gros dossiers.
