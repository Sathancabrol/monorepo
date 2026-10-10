@echo off
setlocal
chcp 65001 >nul
title Bone — Installateur
cd /d "%~dp0"
echo.
echo   Bone — installateur Discord
echo   Ne ferme pas cette fenetre.
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0installer.ps1"
set ERR=%ERRORLEVEL%
if not "%ERR%"=="0" (
  echo.
  echo   Installation interrompue. Code %ERR%
  echo.
)
pause
exit /b %ERR%
