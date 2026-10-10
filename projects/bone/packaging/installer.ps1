# Bone — assistant d'installation Windows
# Lance via INSTALLER.bat (double-clic).

$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}
$Host.UI.RawUI.WindowTitle = 'Bone — Installateur'

function Say([string]$msg, [string]$color = 'White') {
    Write-Host $msg -ForegroundColor $color
}
function Title([string]$msg) {
    Write-Host ''
    Write-Host "  $msg" -ForegroundColor Yellow
    Write-Host ('  ' + ('-' * 46)) -ForegroundColor DarkGray
}
function Pause-Bone([string]$msg = 'Appuie sur Entree pour continuer') {
    Write-Host ''
    Read-Host "  $msg" | Out-Null
}
function Ask([string]$msg) {
    Write-Host ''
    return (Read-Host "  $msg").Trim()
}

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Payload = Join-Path $Here 'payload'
$InstallDir = Join-Path $env:LOCALAPPDATA 'Bone'
$Perms = '277092879424'
$Portal = 'https://discord.com/developers/applications'

if (-not (Test-Path $Payload)) {
    Say 'Dossier payload introuvable. Extraie TOUT le zip, puis relance INSTALLER.bat.' 'Red'
    Pause-Bone
    exit 1
}

Clear-Host
Say ''
Say '   ██████╗  ██████╗ ███╗   ██╗███████╗' 'Yellow'
Say '   ██╔══██╗██╔═══██╗████╗  ██║██╔════╝' 'Yellow'
Say '   ██████╔╝██║   ██║██╔██╗ ██║█████╗  ' 'Yellow'
Say '   ██╔══██╗██║   ██║██║╚██╗██║██╔══╝  ' 'Yellow'
Say '   ██████╔╝╚██████╔╝██║ ╚████║███████╗' 'Yellow'
Say '   ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝' 'Yellow'
Say '   agent South Park  ·  installateur Discord' 'DarkYellow'
Say ''
Say '   Tu vas :' 'Gray'
Say '   1. installer Bone sur ce PC' 'Gray'
Say '   2. coller le token du bot (une fois)' 'Gray'
Say '   3. CHOISIR le serveur Discord dans la fenetre qui s ouvre' 'Gray'
Say '   4. Bone apparait en ligne. Boom.' 'Gray'
Pause-Bone

# --- Python -----------------------------------------------------------
Title '1/5  Python'
$py = $null
foreach ($c in @('py -3', 'py', 'python', 'python3')) {
    try {
        $v = & cmd.exe /c "$c --version 2>&1"
        if ($LASTEXITCODE -eq 0 -and $v -match 'Python 3\.(\d+)') {
            $minor = [int]$Matches[1]
            if ($minor -ge 10) { $py = $c; break }
        }
    } catch {}
}

if (-not $py) {
    Say '   Python 3.10+ introuvable. Tentative winget...' 'DarkYellow'
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($winget) {
        try {
            winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
            $env:Path = [System.Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' +
                        [System.Environment]::GetEnvironmentVariable('Path', 'User')
            $py = 'py -3'
        } catch {
            Say "   winget : $($_.Exception.Message)" 'DarkYellow'
        }
    }
}

if (-not $py) {
    Say '   J ouvre python.org — installe Python 3.12.' 'Yellow'
    Say '   IMPORTANT : coche  Add python.exe to PATH' 'Yellow'
    Start-Process 'https://www.python.org/downloads/'
    Pause-Bone 'Ferme cette fenetre, installe Python, puis RELANCE INSTALLER.bat'
    exit 1
}
Say "   OK  $(& cmd.exe /c "$py --version 2>&1")" 'Green'

# --- Copie ------------------------------------------------------------
Title '2/5  Fichiers'
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
Copy-Item -Path (Join-Path $Payload '*') -Destination $InstallDir -Recurse -Force
Say "   Installe dans  $InstallDir" 'Green'

# --- venv + pip -------------------------------------------------------
Title '3/5  Dependances'
$venvPy = Join-Path $InstallDir '.venv\Scripts\python.exe'
if (-not (Test-Path $venvPy)) {
    Say '   Creation de l environnement...' 'Gray'
    & cmd.exe /c "$py -m venv `"$InstallDir\.venv`""
    if ($LASTEXITCODE -ne 0) { throw 'venv a echoue' }
}
Say '   pip install discord.py (30 secondes)...' 'Gray'
& $venvPy -m pip install -q --upgrade pip
& $venvPy -m pip install -q -r (Join-Path $InstallDir 'requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'pip install a echoue (reseau ?)' }
Say '   OK  discord.py' 'Green'

# --- Token ------------------------------------------------------------
Title '4/5  Token Discord  +  choix du serveur'

$envFile = Join-Path $InstallDir '.env'
$token = $null
if (Test-Path $envFile) {
    foreach ($line in Get-Content $envFile -Encoding UTF8) {
        if ($line -match '^\s*DISCORD_TOKEN\s*=\s*(.+)\s*$') {
            $cand = $Matches[1].Trim().Trim('"').Trim("'")
            if ($cand.Length -gt 20) { $token = $cand }
        }
    }
}

if (-not $token) {
    Say '   Bone a besoin d une application Discord (2 minutes, une seule fois).' 'Gray'
    Say ''
    Say '   Je vais ouvrir le Developer Portal. Fais EXACTEMENT ca :' 'Yellow'
    Say '     1. New Application  →  nom : Bone' 'White'
    Say '     2. Menu Bot  →  Add Bot  →  Yes' 'White'
    Say '     3. Privileged Gateway Intents  →  MESSAGE CONTENT INTENT  =  ON  →  Save' 'White'
    Say '     4. Reset Token  →  Yes  →  Copy  (tu ne le reverras plus)' 'White'
    Say '     5. Reviens ici, colle le token' 'White'
    Say ''
    Pause-Bone 'Entree = j ouvre le portail'
    Start-Process $Portal
    Say ''
    while ($true) {
        $token = Ask 'Colle le TOKEN du bot (il s affiche pas dans Discord ensuite)'
        if ($token.Length -gt 20) { break }
        Say '   Trop court. Recopie le token (Reset Token → Copy).' 'Red'
    }
}

Say '   Verification du token aupres de Discord...' 'Gray'
$headers = @{ Authorization = "Bot $token" }
try {
    $me = Invoke-RestMethod -Uri 'https://discord.com/api/v10/users/@me' -Headers $headers
} catch {
    Say '   Token refuse. Reset Token dans le portail, puis relance l installeur.' 'Red'
    Pause-Bone
    exit 1
}
$clientId = [string]$me.id
Say "   OK  bot @$($me.username)  id $clientId" 'Green'

@"
DISCORD_TOKEN=$token
BONE_GUILD=Olympus
BONE_CHATTY=1
BONE_CHANNELS=général,general,olympus,bone,chat,lounge,accueil,welcome
"@ | Set-Content -Path $envFile -Encoding UTF8

# --- Choix du serveur -------------------------------------------------
Title '5/5  Choisis TON serveur Discord'
Say '   Une fenetre Discord s ouvre.' 'Yellow'
Say '   Dans le menu deroulant : choisis le serveur (Olympus ou un autre).' 'Yellow'
Say '   Puis clique  Autoriser.' 'Yellow'
Say '   Il te faut le droit de GERER le serveur (ou d etre proprio).' 'Gray'
Pause-Bone 'Entree = j ouvre le choix du serveur'

$invite = "https://discord.com/oauth2/authorize?client_id=$clientId&permissions=$Perms&scope=bot%20applications.commands"
Start-Process $invite

Pause-Bone 'Tu as clique Autoriser ? Entree pour lancer Bone'

# --- Premier demarrage ------------------------------------------------
Get-ChildItem (Join-Path $InstallDir 'ready.json') -ErrorAction SilentlyContinue | Remove-Item -Force
$logFile = Join-Path $InstallDir 'bone.log'
if (Test-Path $logFile) { Remove-Item $logFile -Force }

Say '   Demarrage de Bone...' 'Gray'
$proc = Start-Process -FilePath $venvPy -ArgumentList 'discord_bot.py' -WorkingDirectory $InstallDir -PassThru -WindowStyle Minimized

$ready = $null
for ($i = 0; $i -lt 40; $i++) {
    Start-Sleep -Milliseconds 500
    $readyPath = Join-Path $InstallDir 'ready.json'
    if (Test-Path $readyPath) {
        try { $ready = Get-Content $readyPath -Raw -Encoding UTF8 | ConvertFrom-Json } catch {}
        if ($ready) { break }
    }
    if ($proc.HasExited) { break }
}

if (-not $ready) {
    Say '   Bone ne s est pas connecte. Regarde bone.log' 'Red'
    if (Test-Path $logFile) { Get-Content $logFile -Tail 20 }
    Pause-Bone
    exit 1
}

if (-not $ready.guilds -or $ready.guilds.Count -eq 0) {
    Say '   Bone est en ligne mais dans AUCUN serveur.' 'Yellow'
    Say '   L invitation n a pas abouti. On reouvre le choix.' 'Yellow'
    Start-Process $invite
    Pause-Bone 'Autorise le serveur, puis Entree'
    Start-Sleep 3
    if (Test-Path (Join-Path $InstallDir 'ready.json')) {
        try { $ready = Get-Content (Join-Path $InstallDir 'ready.json') -Raw -Encoding UTF8 | ConvertFrom-Json } catch {}
    }
}

$guildNames = @()
if ($ready.guilds) { $guildNames = @($ready.guilds | ForEach-Object { $_.name }) }

# --- Raccourcis -------------------------------------------------------
$w = New-Object -ComObject WScript.Shell
$ico = Join-Path $InstallDir 'assets\bone.ico'
if (-not (Test-Path $ico)) { $ico = Join-Path $InstallDir 'assets\bone.png' }

$demarrer = @"
@echo off
cd /d "%LOCALAPPDATA%\Bone"
if exist ready.json del ready.json
start "Bone" /MIN ".venv\Scripts\python.exe" discord_bot.py
"@
$arreter = @"
@echo off
cd /d "%LOCALAPPDATA%\Bone"
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { `$_.CommandLine -like '*discord_bot.py*' } | ForEach-Object { Stop-Process -Id `$_.ProcessId -Force -ErrorAction SilentlyContinue }"
echo Bone arrete.
"@
Set-Content -Path (Join-Path $InstallDir 'demarrer.bat') -Value $demarrer -Encoding ASCII
Set-Content -Path (Join-Path $InstallDir 'arreter.bat') -Value $arreter -Encoding ASCII
$desinst = @"
@echo off
cd /d "%LOCALAPPDATA%\Bone"
call arreter.bat
del /q "%USERPROFILE%\Desktop\Bone.lnk" 2>nul
del /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Bone.lnk" 2>nul
rmdir /s /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Bone" 2>nul
cd /d "%TEMP%"
rmdir /s /q "%LOCALAPPDATA%\Bone"
echo Bone desinstalle.
pause
"@
Set-Content -Path (Join-Path $InstallDir 'desinstaller.bat') -Value $desinst -Encoding ASCII

$desktop = [Environment]::GetFolderPath('Desktop')
$startDir = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Bone'
New-Item -ItemType Directory -Force -Path $startDir | Out-Null

function Make-Shortcut($path, $target, $args, $work, $icon) {
    $s = $w.CreateShortcut($path)
    $s.TargetPath = $target
    if ($args) { $s.Arguments = $args }
    $s.WorkingDirectory = $work
    if (Test-Path $icon) { $s.IconLocation = $icon }
    $s.Save()
}

Make-Shortcut (Join-Path $desktop 'Bone.lnk') (Join-Path $InstallDir 'demarrer.bat') $null $InstallDir $ico
Make-Shortcut (Join-Path $startDir 'Bone.lnk') (Join-Path $InstallDir 'demarrer.bat') $null $InstallDir $ico
Make-Shortcut (Join-Path $startDir 'Arreter Bone.lnk') (Join-Path $InstallDir 'arreter.bat') $null $InstallDir $ico

$boot = Ask 'Lancer Bone au demarrage de Windows ?  O / n'
if ($boot -notmatch '^[nN]') {
    $startup = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Startup'
    Make-Shortcut (Join-Path $startup 'Bone.lnk') (Join-Path $InstallDir 'demarrer.bat') $null $InstallDir $ico
    Say '   OK  Bone se lancera a l ouverture de session' 'Green'
}

# --- Fin --------------------------------------------------------------
Write-Host ''
Say '   ========================================' 'Green'
Say '   BONE EST INSTALLE' 'Green'
if ($guildNames.Count -gt 0) {
    Say ("   Serveur(s) :  " + ($guildNames -join ', ')) 'Green'
} else {
    Say '   Ouvre Discord : Bone doit apparaitre en ligne.' 'Yellow'
}
Say '   Raccourci Bureau : Bone' 'Gray'
Say '   Dossier : ' + $InstallDir 'Gray'
Say '   ========================================' 'Green'
Say ''
Say '   Dans Discord :  @Bone salut   ou   /roast' 'Yellow'
Say '   Laisse le PC allume (ou relance Bone au boot).' 'Gray'
Say ''
Pause-Bone 'Termine'
exit 0
