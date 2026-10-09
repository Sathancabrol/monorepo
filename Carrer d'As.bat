@echo off
chcp 65001 >nul
title Carré d'As
cd /d "%~dp0"
echo.
echo   ◈ Carré d'As — lancement...
echo.
where python >nul 2>nul
if errorlevel 1 (
  echo   ERREUR : Python n'est pas installé ou n'est pas dans le PATH.
  echo   Téléchargez-le sur https://www.python.org/downloads/ ^(cochez
  echo   "Add Python to PATH" pendant l'installation^), puis relancez.
  pause
  exit /b 1
)
python main.py --serve --port 8000
echo.
echo   Serveur arrêté.
pause
