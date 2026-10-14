@echo off
chcp 65001 >nul
title Bone — Autorisations
cd /d "%~dp0"
if not exist "discord_bot.py" (
  if exist "%LOCALAPPDATA%\Bone\autorisations.ps1" (
    cd /d "%LOCALAPPDATA%\Bone"
  )
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%cd%\autorisations.ps1"
pause
