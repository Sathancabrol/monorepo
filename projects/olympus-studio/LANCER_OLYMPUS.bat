@echo off
setlocal
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
  echo.
  echo OLYMPUS Studio necessite Node.js 20 ou plus recent.
  echo Installe Node.js depuis https://nodejs.org puis relance ce fichier.
  echo Aucun outil ou modele ne sera installe automatiquement.
  echo.
  pause
  exit /b 1
)
echo.
echo Demarrage de OLYMPUS Studio en local...
echo Adresse : http://127.0.0.1:8787
echo Cette fenetre doit rester ouverte pendant l'utilisation.
echo Pour arreter : CTRL+C dans cette fenetre.
echo.
start "" "http://127.0.0.1:8787"
node server.mjs
if errorlevel 1 (
  echo.
  echo Le serveur n'a pas pu demarrer. Le port 8787 est peut-etre occupe.
  pause
)
endlocal
