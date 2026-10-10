# Bone — droits et connexions APRES install
$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}
$Host.UI.RawUI.WindowTitle = 'Bone — Autorisations'

function Say([string]$msg, [string]$color = 'White') { Write-Host $msg -ForegroundColor $color }
function Ask([string]$msg) { return (Read-Host "  $msg").Trim() }
function Yes([string]$msg) {
    $r = Ask "$msg  O/n"
    return ($r -notmatch '^[nN]')
}

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path (Join-Path $Here 'discord_bot.py'))) {
    $Here = Join-Path $env:LOCALAPPDATA 'Bone'
}
if (-not (Test-Path (Join-Path $Here 'discord_bot.py'))) {
    Say 'Bone n est pas installe. Lance INSTALLER.bat d abord.' 'Red'
    Read-Host 'Entree'
    exit 1
}

$envFile = Join-Path $Here '.env'
$token = $null
if (Test-Path $envFile) {
    foreach ($line in Get-Content $envFile -Encoding UTF8) {
        if ($line -match '^\s*DISCORD_TOKEN\s*=\s*(.+)\s*$') {
            $token = $Matches[1].Trim().Trim('"').Trim("'")
        }
    }
}
if (-not $token -or $token.Length -lt 20) {
    Say 'Pas de token dans .env. Relance l installeur.' 'Red'
    Read-Host 'Entree'
    exit 1
}

$headers = @{ Authorization = "Bot $token" }
try {
    $me = Invoke-RestMethod -Uri 'https://discord.com/api/v10/users/@me' -Headers $headers
} catch {
    Say 'Token refuse. Reset Token dans le portail, mets a jour .env' 'Red'
    Read-Host 'Entree'
    exit 1
}
$clientId = [string]$me.id

# bits = base + extras (voir perms.py — ne pas approximer)
$base = [int64]380172094528
$packs = [ordered]@{
    '1' = @{ n = 'Moderation (kick, timeout, messages)'; bit = [int64]1099511636102 }
    '2' = @{ n = 'Vocal (rejoindre, parler, mute, move)'; bit = [int64]66060800 }
    '3' = @{ n = 'Salons et threads'; bit = [int64]25769803792 }
    '4' = @{ n = 'Roles et pseudos'; bit = [int64]402653184 }
    '5' = @{ n = 'Webhooks'; bit = [int64]536870912 }
    '6' = @{ n = 'ADMIN (tout) — eviter'; bit = [int64]8 }
}

function Open-Invite([int64]$perm) {
    $url = "https://discord.com/oauth2/authorize?client_id=$clientId&permissions=$perm&scope=bot%20applications.commands"
    Say "   Ouverture Discord — re-choisis le serveur, puis Autoriser." 'Yellow'
    Start-Process $url
}

function Set-EnvKey([string]$key, [string]$value) {
    $lines = @()
    if (Test-Path $envFile) { $lines = Get-Content $envFile -Encoding UTF8 }
    $found = $false
    $out = foreach ($l in $lines) {
        if ($l -match "^(\s*#)?\s*$([regex]::Escape($key))\s*=") {
            $found = $true
            "$key=$value"
        } else { $l }
    }
    if (-not $found) { $out = @($out) + "$key=$value" }
    Set-Content -Path $envFile -Value $out -Encoding UTF8
}

while ($true) {
    Clear-Host
    Say ''
    Say "  BONE  —  autorisations & connexions    @$($me.username)" 'Yellow'
    Say '  ------------------------------------------------' 'DarkGray'
    Say '  1  Ajouter des DROITS Discord (re-choisir le serveur)'
    Say '  2  Intents privilegies (membres, presence) — portail'
    Say '  3  Connexions (cles API dans .env)'
    Say '  4  Ouvrir le .env'
    Say '  5  Portail Discord de Bone'
    Say '  Q  Quitter'
    Say ''
    $c = Ask 'Choix'
    if ($c -match '^[qQ]$') { break }

    if ($c -eq '1') {
        Say ''
        Say '  Coche ce que tu veux AJOUTER (deja installe : parler + slash).' 'Gray'
        $perm = [int64]$base
        foreach ($k in $packs.Keys) {
            $p = $packs[$k]
            if (Yes $p.n) {
                if ($k -eq '6') { $perm = [int64]8; break }
                $perm = $perm -bor $p.bit
            }
        }
        Open-Invite $perm
        Say '  Apres Autoriser, les droits sont a jour. Pas besoin de reinstaller.' 'Green'
        Read-Host '  Entree'
    }
    elseif ($c -eq '2') {
        Say ''
        Say '  Intents = interrupteurs cote Discord, PLUS dans .env, PUIS relancer Bone.' 'Gray'
        Say '  J ouvre l onglet Bot. Coche, Save Changes.' 'Yellow'
        Start-Process "https://discord.com/developers/applications/$clientId/bot"
        if (Yes 'SERVER MEMBERS INTENT (liste des membres)') {
            Set-EnvKey 'BONE_MEMBERS_INTENT' '1'
            Say '  .env : BONE_MEMBERS_INTENT=1' 'Green'
        }
        if (Yes 'PRESENCE INTENT (statut en ligne)') {
            Set-EnvKey 'BONE_PRESENCE_INTENT' '1'
            Say '  .env : BONE_PRESENCE_INTENT=1' 'Green'
        }
        Say '  Relance Bone (Arreter puis raccourci Bureau) pour prendre effet.' 'Yellow'
        Read-Host '  Entree'
    }
    elseif ($c -eq '3') {
        Say ''
        Say '  Connexions optionnelles — colle la cle, Entree vide = skip.' 'Gray'
        $oa = Ask 'OPENAI_API_KEY (vide = skip)'
        if ($oa) { Set-EnvKey 'OPENAI_API_KEY' $oa; Say '  OK OpenAI' 'Green' }
        $gr = Ask 'GROQ_API_KEY (vide = skip)'
        if ($gr) { Set-EnvKey 'GROQ_API_KEY' $gr; Say '  OK Groq' 'Green' }
        $ol = Ask 'OLLAMA_HOST (ex http://127.0.0.1:11434 — vide = skip)'
        if ($ol) { Set-EnvKey 'OLLAMA_HOST' $ol; Say '  OK Ollama' 'Green' }
        Say '  Relance Bone si tu as change une cle.' 'Yellow'
        Read-Host '  Entree'
    }
    elseif ($c -eq '4') {
        notepad $envFile
    }
    elseif ($c -eq '5') {
        Start-Process "https://discord.com/developers/applications/$clientId/information"
        Read-Host '  Entree'
    }
}

exit 0
