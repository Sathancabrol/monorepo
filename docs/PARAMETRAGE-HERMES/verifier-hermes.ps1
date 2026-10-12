<#
.SYNOPSIS
  verifier-hermes.ps1 — état des lieux du montage Hermes + OmniRoute + Ollama (Windows natif).

.DESCRIPTION
  Vérifie, sans rien modifier :
    1. Hermes (CLI, chemins config/.env, route provider/modèle, `hermes doctor` et son code de sortie)
    2. OmniRoute sur 127.0.0.1:20128 (TCP + /v1/models)
    3. Ollama sur 127.0.0.1:11434 (TCP + modèles installés)
    4. Présence des variables sensibles (les VALEURS ne sont jamais affichées) + permissions du .env
    5. Quota payant (openai-codex) si -Quota, journalisé dans quota-log.csv si -Log

.PARAMETER Quota
  Interroge `hermes usage --provider openai-codex --json` et affiche les fenêtres (Session / Weekly).

.PARAMETER Log
  Ajoute une ligne (date UTC, session %, weekly %, machine) à quota-log.csv. Implique -Quota.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File .\verifier-hermes.ps1 -Quota -Log

.NOTES
  Code de sortie : 0 = socle complet, 1 = au moins un élément manquant.
  Règle n°8 de projects/watchtower/AGENTS.md : une vérification se termine par un code de sortie.
  Aucun secret n'est ni affiché ni écrit.
#>

param(
  [switch]$Quota,
  [switch]$Log
)

if ($Log) { $Quota = $true }

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Csv       = Join-Path $ScriptDir 'quota-log.csv'
$Problemes = 0

function Ecrire-Titre { param([string]$Texte) Write-Host ""; Write-Host ("== " + $Texte + " ==") -ForegroundColor Cyan }
function Ecrire-Ok    { param([string]$Texte) Write-Host ("  [OK]   " + $Texte) -ForegroundColor Green }
function Ecrire-Ko    { param([string]$Texte) Write-Host ("  [KO]   " + $Texte) -ForegroundColor Red; $script:Problemes++ }
function Ecrire-Warn  { param([string]$Texte) Write-Host ("  [?]    " + $Texte) -ForegroundColor Yellow }

function Test-PortOuvert {
  param([int]$Port, [string]$Hote = '127.0.0.1', [int]$TimeoutMs = 1200)
  $client = New-Object System.Net.Sockets.TcpClient
  try {
    $async = $client.BeginConnect($Hote, $Port, $null, $null)
    if (-not $async.AsyncWaitHandle.WaitOne($TimeoutMs, $false)) { return $false }
    $client.EndConnect($async)
    return $true
  } catch {
    return $false
  } finally {
    try { $client.Close() } catch { }
  }
}

function Get-CodeHttp {
  param([string]$Url)
  try {
    $r = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
    return [int]$r.StatusCode
  } catch {
    if ($_.Exception.Response -ne $null) {
      try { return [int]$_.Exception.Response.StatusCode } catch { return 0 }
    }
    return 0
  }
}

function Invoke-Hermes {
  param([string[]]$Arguments)
  $exe = Get-Command hermes -ErrorAction SilentlyContinue
  if (-not $exe) { return $null }
  try {
    return (& hermes @Arguments 2>$null | Out-String).Trim()
  } catch {
    return $null
  }
}

# ---------------------------------------------------------------- 1. Hermes
Ecrire-Titre "1. Hermes"
$hermesExe = Get-Command hermes -ErrorAction SilentlyContinue
$CfgPath = $null
$EnvPath = $null

if ($hermesExe) {
  $version = Invoke-Hermes @('--version')
  Ecrire-Ok ("hermes présent : " + $version)

  $CfgPath = Invoke-Hermes @('config','path')
  $EnvPath = Invoke-Hermes @('config','env-path')
  if ($CfgPath) { Ecrire-Ok ("config.yaml : " + $CfgPath) } else { Ecrire-Warn "chemin de config non résolu (hermes config path)" }
  if ($EnvPath) { Ecrire-Ok (".env : " + $EnvPath) } else { Ecrire-Warn "chemin .env non résolu (hermes config env-path)" }

  $provider = Invoke-Hermes @('config','get','model.provider')
  $modele   = Invoke-Hermes @('config','get','model.default')
  Write-Host ("  route : provider=" + $(if ($provider) { $provider } else { '<vide>' }) + "  modèle=" + $(if ($modele) { $modele } else { '<vide>' }))

  if ($provider -match 'omniroute' -or $provider -match 'custom') {
    Ecrire-Ok "route principale = endpoint personnalisé (OmniRoute / local)"
  } elseif ([string]::IsNullOrWhiteSpace($provider) -or $provider -eq 'auto') {
    Ecrire-Ko "route principale non définie (étape 2 du README)"
  } else {
    Ecrire-Warn ("route principale = " + $provider + " (le payant doit rester un choix manuel)")
  }

  # doctor : on capture le code de sortie réel, sans pipe qui le masquerait
  $doctorOut = Join-Path $env:TEMP ("hermes-doctor-" + (Get-Random) + ".log")
  & hermes doctor *> $doctorOut
  $doctorCode = $LASTEXITCODE
  if ($doctorCode -eq 0) {
    Ecrire-Ok "hermes doctor : exit 0 (aucun problème non résolu)"
  } else {
    $queue = (Get-Content $doctorOut -ErrorAction SilentlyContinue | Select-Object -Last 3) -join ' '
    Ecrire-Ko ("hermes doctor : exit " + $doctorCode + " — " + $queue)
  }
  Remove-Item $doctorOut -ErrorAction SilentlyContinue
} else {
  Ecrire-Ko "commande `hermes` absente du PATH (relancer la console après l'installation)"
}

# ------------------------------------------------------------- 2. OmniRoute
Ecrire-Titre "2. OmniRoute (127.0.0.1:20128)"
if (Test-PortOuvert -Port 20128) {
  Ecrire-Ok "port 20128 ouvert"
  $code = Get-CodeHttp 'http://127.0.0.1:20128/v1/models'
  switch ($code) {
    200 { Ecrire-Ok "/v1/models répond 200" }
    401 { Ecrire-Warn "/v1/models répond 401 : clé OmniRoute requise (normal sans en-tête Authorization)" }
    0   { Ecrire-Warn "port ouvert mais /v1/models injoignable" }
    default { Ecrire-Warn ("/v1/models répond " + $code) }
  }
  Write-Host "  dashboard : http://127.0.0.1:20128  (Providers → connecter un fournisseur ; Endpoints → clé)"
} else {
  Ecrire-Ko "port 20128 fermé (OmniRoute non démarré — étape 1)"
}

# ---------------------------------------------------------------- 3. Ollama
Ecrire-Titre "3. Ollama (127.0.0.1:11434)"
if (Test-PortOuvert -Port 11434) {
  Ecrire-Ok "port 11434 ouvert"
  try {
    $tags = Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 3 -ErrorAction Stop
    $noms = @()
    foreach ($m in $tags.models) { $noms += $m.name }
    if ($noms.Count -eq 0) {
      Ecrire-Ko "aucun modèle Ollama installé (ollama pull …)"
    } else {
      Write-Host ("  modèles : " + ($noms -join ', '))
      Ecrire-Ok "au moins un modèle local disponible"
    }
  } catch {
    Ecrire-Warn "réponse /api/tags illisible"
  }
} else {
  Ecrire-Ko "port 11434 fermé (Ollama non démarré — étape 3)"
}

# ------------------------------------------------- 4. Variables et .env
Ecrire-Titre "4. Variables sensibles (présence seulement)"
if ($EnvPath -and (Test-Path $EnvPath)) {
  try {
    $acl = Get-Acl $EnvPath
    $identites = @($acl.Access | Where-Object { $_.FileSystemRights -match 'FullControl' -or $_.FileSystemRights -match 'Modify' } | ForEach-Object { $_.IdentityReference.Value })
    $tropLarge = $false
    foreach ($i in $identites) {
      if ($i -match 'Everyone|Tout le monde|BUILTIN\\Users|Utilisateurs|Authenticated Users') { $tropLarge = $true }
    }
    if ($tropLarge) {
      Ecrire-Warn ".env accessible à un groupe large — restreindre à ton compte (icône Propriétaire → Sécurité)"
    } else {
      Ecrire-Ok ".env sans droit large détecté"
    }
  } catch {
    Ecrire-Warn "permissions du .env non lisibles"
  }
  foreach ($nom in @('OMNIROUTE_API_KEY','OPENAI_API_KEY','OPENROUTER_API_KEY','GOOGLE_API_KEY','GROQ_API_KEY')) {
    $present = Select-String -Path $EnvPath -Pattern ('^' + $nom + '=') -Quiet -ErrorAction SilentlyContinue
    if ($present) { Write-Host ("  présent : " + $nom) } else { Write-Host ("  absent  : " + $nom) }
  }
} else {
  Ecrire-Warn "fichier .env non trouvé — les clés n'ont pas encore été posées"
}

# ----------------------------------------------------------------- 5. Quota
$ligneQuota = $null
if ($Quota) {
  Ecrire-Titre "5. Quota payant (openai-codex)"
  $json = Invoke-Hermes @('usage','--provider','openai-codex','--json')
  if ($json) {
    try {
      $o = $json | ConvertFrom-Json
      if ($o.plan) { Write-Host ("  plan : " + $o.plan) }
      $session = ''
      $weekly  = ''
      foreach ($w in $o.windows) {
        $libelle = [string]$w.label
        $pct = ''
        if ($null -ne $w.used_percent) { $pct = [string]$w.used_percent }
        Write-Host ("  " + $libelle.PadRight(9) + " utilisé=" + $(if ($pct -ne '') { $pct + '%' } else { '?' }) + "  reset=" + $w.resets_at)
        if ($libelle -match '(?i)session') { $session = $pct }
        if ($libelle -match '(?i)week')    { $weekly  = $pct }
      }
      if ($o.unavailable_reason) { Write-Host ("  indisponible : " + $o.unavailable_reason) }
      $ligneQuota = $session + "`t" + $weekly
    } catch {
      Write-Host ("  " + $json)
    }
  } else {
    Ecrire-Warn "pas de réponse JSON (identifiants Codex absents, ou hermes absent)"
  }
}

if ($Log) {
  if (-not (Test-Path $Csv)) { Add-Content -Path $Csv -Value "date_utc`tsession_pct`tweekly_pct`tnode" }
  $horodatage = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
  $node = $env:COMPUTERNAME
  if ($ligneQuota) {
    Add-Content -Path $Csv -Value ($horodatage + "`t" + $ligneQuota + "`t" + $node)
    Ecrire-Ok ("ligne ajoutée à " + $Csv)
  } else {
    Add-Content -Path $Csv -Value ($horodatage + "`t`t`t" + $node)
    Ecrire-Warn ("ligne sans quota ajoutée (quota indisponible) → " + $Csv)
  }
}

# ---------------------------------------------------------------- Verdict
Write-Host ""
Write-Host "===== VERDICT =====" -ForegroundColor Cyan
if ($Problemes -eq 0) {
  Write-Host "socle complet : rien de manquant." -ForegroundColor Green
  exit 0
} else {
  Write-Host ($Problemes.ToString() + " élément(s) à corriger — voir les lignes [KO] ci-dessus.") -ForegroundColor Red
  exit 1
}
