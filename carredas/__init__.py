"""Carré d'As — cœur de l'application.

Contraintes fondatrices (non négociables) :
  * aucune dépendance obligatoire : le cœur tourne avec la seule bibliothèque standard.
    Les dépendances lourdes (STT, export OOXML via librairie, LLM distant) sont
    optionnelles et dégradables — une réunion doit toujours produire un document,
    même sans réseau et sans modèle.
  * tout est stocké en JSON lisible dans le dossier de données, jamais dans une base
    opaque : on peut ouvrir, corriger, versionner (Git) à la main.
  * chaque module est un dossier avec un `module.json` : plug in / plug out.
"""

__version__ = "0.1.0"

DEFAULT_VERSION = __version__
