@echo off
setlocal
cd /d "%~dp0"
title Bone Setup
REM Wizard graphique (STA). Si WPF refuse, fallback console.
powershell -STA -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "%~dp0setup-ui.ps1"
if "%ERRORLEVEL%"=="0" exit /b 0
echo.
echo  Wizard graphique indisponible — mode console.
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0installer.ps1"
set ERR=%ERRORLEVEL%
if not "%ERR%"=="0" (
  echo Installation interrompue. Code %ERR%
  pause
)
exit /b %ERR%
