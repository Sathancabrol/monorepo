"""Noyau partagé : contrats de données du monorepo.

`canonical.py` définit l'enregistrement canonique — la forme commune à toute
information qui traverse les modules. Les schémas JSON sont publiés à côté pour
les outils qui savent les lire ; la validation Python reste volontairement
minimale et sans dépendance.
"""
