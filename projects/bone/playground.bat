@echo off
cd /d "%~dp0"
where py >nul 2>&1 && (set PY=py -3) || (set PY=python)
echo Playground Bone → http://127.0.0.1:8765
start "" http://127.0.0.1:8765
%PY% -m http.server 8765
pause
