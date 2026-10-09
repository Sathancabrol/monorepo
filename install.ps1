#Requires -Version 5.1
<#
.SYNOPSIS
    Installe Carré d'As sur un poste Windows.

.DESCRIPTION
    Le cœur de l'application n'a aucune dépendance : Python suffit.
    Ce script crée un environnement virtuel, pose un lanceur et un raccourci
    sur le bureau, puis démarre l'application.

    Par défaut il installe depuis le dossier courant (le dépôt).
    Avec -Depot, il clone le dépôt GitHub à la place — ce qui active
    immédiatement les mises à jour par Git depuis l'application.

.EXAMPLE
    .\install.ps1
    .\install.ps1 -Depot                 # clone depuis GitHub
    .\install.ps1 -Chemin C:\CarreDAs    # dossier d'installation choisi
    .\install.ps1 -Portable              # installe à côté du script (clé USB)
#>
[CmdletBinding()]
param(
    [string] $Chemin = "",
    [switch] $Depot,
    [switch] $Portable,
    [switch] $SansRaccourci,
    [switch] $NePasLancer,
    [string] $Branche = "main"
)

$ErrorActionPreference = "Stop"
$AppTitre = "Carré d'As"
$DepotUrl = "https://github.com/Sathancabrol/monorepo.git"

function Ecrire($msg, $couleur = "White") { Write-Host $msg -ForegroundColor $couleur }

Ecrire ""
Ecrire "  ╔══════════════════════════════════════════╗" Cyan
Ecrire "  ║   Carré d'As — installation Windows      ║" Cyan
Ecrire "  ╚══════════════════════════════════════════╝" Cyan
Ecrire ""

# ------------------------------------------------------------------ 1. Python
Ecrire "[1/6] Recherche de Python…" Gray
$python = $null
foreach ($cand in @("py", "python", "python3")) {
    try {
        $cmd = Get-Command $cand -ErrorAction Stop
        $ver = & $cmd.Source -c "import sys;print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
        if ($ver) {
            $maj, $min = $ver.Split(".")
            if ([int]$maj -ge 3 -and [int]$min -ge 10) { $python = $cmd.Source; break }
        }
    } catch { }
}
if (-not $python) {
    Ecrire ""
    Ecrire "  Python 3.10 ou plus est nécessaire et n'a pas été trouvé." Red
    Ecrire "  Deux options :" Yellow
    Ecrire "    • Microsoft Store :  winget install Python.Python.3.12" Yellow
    Ecrire "    • python.org       : https://www.python.org/downloads/" Yellow
    Ecrire ""
    Ecrire "  Pendant l'installation, cocher « Add python.exe to PATH »." Yellow
    Ecrire ""
    exit 1
}
$versionPython = & $python -c "import sys;print('.'.join(map(str,sys.version_info[:3])))"
Ecrire "      Python $versionPython — $python" Green

# ------------------------------------------------------------- 2. Destination
Ecrire "[2/6] Dossier d'installation…" Gray
if ($Portable) { $cible = Join-Path (Get-Location) "CarreDAs" }
elseif ($Chemin) { $cible = $Chemin }
else { $cible = Join-Path $env:LOCALAPPDATA "CarreDAs" }
$cible = [System.IO.Path]::GetFullPath($cible)
New-Item -ItemType Directory -Force -Path $cible | Out-Null
Ecrire "      $cible" Green

# -------------------------------------------------------------- 3. Les fichiers
Ecrire "[3/6] Récupération de l'application…" Gray
$source = Split-Path -Parent $PSCommandPath
if ($Depot) {
    $git = Get-Command git -ErrorAction SilentlyContinue
    if (-not $git) {
        Ecrire "      Git n'est pas installé — installation depuis le dossier courant." Yellow
        $Depot = $false
    }
}
if ($Depot) {
    if (Test-Path (Join-Path $cible ".git")) {
        Ecrire "      Dépôt déjà présent : mise à jour." Gray
        & git -C $cible pull --ff-only 2>$null
    } else {
        & git clone --depth 1 --branch $Branche $DepotUrl $cible
    }
} else {
    # on ne copie que ce qui sert à l'application
    $aCopier = @("carredas", "main.py", "scripts", "docs", "shell", "README.md", "requirements.txt")
    foreach ($item in $aCopier) {
        $src = Join-Path $source $item
        if (Test-Path $src) {
            Copy-Item -Path $src -Destination $cible -Recurse -Force
        }
    }
}
if (-not (Test-Path (Join-Path $cible "main.py"))) {
    Ecrire "      main.py introuvable dans $cible — installation interrompue." Red
    exit 1
}
Ecrire "      fait." Green

# ----------------------------------------------------------------- 4. Environnement
Ecrire "[4/6] Environnement virtuel…" Gray
$venv = Join-Path $cible ".venv"
if (-not (Test-Path (Join-Path $venv "Scripts/python.exe"))) {
    & $python -m venv $venv
    if ($LASTEXITCODE -ne 0) { Ecrire "      venv impossible — on continue sans." Yellow }
}
$venvPython = Join-Path $venv "Scripts/python.exe"
if (Test-Path $venvPython) {
    & $venvPython -m pip install --quiet --disable-pip-version-check --upgrade pip 2>$null
    # pywebview : seule dépendance utile (fenêtre native). Facultative.
    & $venvPython -m pip install --quiet --disable-pip-version-check pywebview 2>$null
    if ($LASTEXITCODE -eq 0) { Ecrire "      pywebview installé (fenêtre native)." Green }
    else { Ecrire "      sans pywebview : ouverture en mode application Edge (équivalent)." Yellow }
}

# -------------------------------------------------------------- 5. Lanceur
Ecrire "[5/6] Lanceur et raccourcis…" Gray
$lanceur = Join-Path $cible "Carré d'As.bat"
@"
@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" main.py
) else (
    start "" pythonw main.py
)
"@ | Set-Content -Path $lanceur -Encoding ASCII

if ($Portable) {
    "Mode portable : les données sont stockées dans ce dossier." |
        Set-Content (Join-Path $cible "PORTABLE") -Encoding ASCII
}

if (-not $SansRaccourci) {
    $ws = New-Object -ComObject WScript.Shell
    $bureau = [System.IO.Path]::Combine($env:USERPROFILE, "Desktop")
    if (-not (Test-Path $bureau)) { $bureau = [Environment]::GetFolderPath("Desktop") }
    $raccourci = $ws.CreateShortcut((Join-Path $bureau "Carré d'As.lnk"))
    $raccourci.TargetPath = $lanceur
    $raccourci.WorkingDirectory = $cible
    $raccourci.Description = "Carré d'As — point d'accès aux modules"
    $raccourci.Save()

    $menu = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs"
    $r2 = $ws.CreateShortcut((Join-Path $menu "Carré d'As.lnk"))
    $r2.TargetPath = $lanceur
    $r2.WorkingDirectory = $cible
    $r2.Description = "Carré d'As — point d'accès aux modules"
    $r2.Save()
    Ecrire "      raccourcis créés (bureau et menu Démarrer)." Green
}

# ------------------------------------------------------------------- 6. Démarrage
Ecrire "[6/6] Terminé." Green
Ecrire ""
Ecrire "  Dossier   : $cible" Gray
Ecrire "  Lanceur   : $lanceur" Gray
Ecrire "  Mise à jour : depuis l'application, bouton « ⟳ Mise à jour »" Gray
Ecrire ""

if (-not $NePasLancer) {
    $rep = Read-Host "  Démarrer Carré d'As maintenant ? (O/n)"
    if ($rep -eq "" -or $rep -match "^o" ) { Start-Process $lanceur }
}
