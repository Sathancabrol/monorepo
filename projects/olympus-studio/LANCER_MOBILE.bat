@echo off
setlocal
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
 echo Node.js 20+ est requis. Installer depuis https://nodejs.org
 pause
 exit /b 1
)
if not exist "scripts\mobile-preview.mjs" (
 echo Passerelle mobile manquante : extraire le ZIP complet de la PR mobile.
 pause
 exit /b 1
)
echo.
echo OLYMPUS Studio + passerelle de previsualisation privee
echo Lancement de deux fenetres : laisser les deux ouvertes.
echo.
start "OLYMPUS Studio - local 8787" /D "%~dp0" cmd /k "node server.mjs"
timeout /t 2 /nobreak >nul
start "OLYMPUS Mobile - local 8788" /D "%~dp0" cmd /k "node scripts\mobile-preview.mjs"
echo.
echo 1. Verifier http://127.0.0.1:8787 sur la tour.
echo 2. Installer Tailscale sur la tour et le telephone, meme compte.
echo 3. Dans PowerShell: tailscale serve --bg 8788
echo 4. Lire l'URL privee: tailscale serve status
echo 5. Sur Samsung, ouvrir cette URL HTTPS avec Tailscale active.
echo.
echo NE PAS activer Tailscale Funnel ni de redirection de ports box.
echo Les API de commande du PC sont bloquees depuis le mobile.
echo.
pause
endlocal
