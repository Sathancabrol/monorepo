@echo off
setlocal EnableExtensions
cd /d "%~dp0"

where py >nul 2>&1
if %errorlevel%==0 (
  set "PY=py -3"
) else (
  where python >nul 2>&1
  if %errorlevel%==0 (
    set "PY=python"
  ) else (
    echo.
    echo  Python n'est pas installe.
    echo  1. Ouvre https://www.python.org/downloads/
    echo  2. Installe Python 3.11 ou plus
    echo  3. COCHE "Add python.exe to PATH"
    echo  4. Relance ce fichier.
    echo.
    pause
    exit /b 1
  )
)

if not exist ".venv\Scripts\python.exe" (
  echo Creation de l'environnement Bone...
  %PY% -m venv .venv
  if errorlevel 1 (
    echo Echec venv. Python 3.11+ est requis.
    pause
    exit /b 1
  )
)

call .venv\Scripts\activate.bat
python -m pip install -q --upgrade pip
python -m pip install -q -r requirements.txt

if not exist ".env" (
  copy /Y .env.example .env >nul
  echo.
  echo  ========================================
  echo   COLLE TON TOKEN DISCORD DANS .env
  echo   Ligne a remplir : DISCORD_TOKEN=...
  echo  ========================================
  echo.
  notepad .env
  echo Relance lancer.bat une fois le token sauve.
  pause
  exit /b 0
)

echo.
echo  Bone demarre. Laisse cette fenetre ouverte.
echo  Ctrl+C pour l'arreter.
echo.
python discord_bot.py
echo.
pause
