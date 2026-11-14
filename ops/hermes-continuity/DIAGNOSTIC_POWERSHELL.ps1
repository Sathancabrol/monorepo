# Diagnostic Hermes / Chronos — lecture seule, Windows PowerShell
# Copiez ce script dans PowerShell ou enregistrez-le comme DIAGNOSTIC.ps1.
# Aucun changement de configuration ; aucune cle API n'est lue ou envoyee.
$ErrorActionPreference = 'Continue'
$Stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$Out = Join-Path ([Environment]::GetFolderPath('Desktop')) "hermes_diagnostic_$Stamp.txt"
$Results = New-Object System.Collections.Generic.List[string]
function Record([string]$Line) {
  $Results.Add($Line)
  Write-Host $Line
}
function SafeCommand([string]$Name, [string[]]$CommandArgs) {
  Record ("=== " + $Name + " ===")
  try {
    $Result = & $CommandArgs[0] $CommandArgs[1..($CommandArgs.Length-1)] 2>&1 | Out-String
    foreach ($Line in ($Result -split '\r?\n')) {
      if ($Line -match '(?i)(api.?key|password|secret|authorization|bearer|credential|token|sk-[A-Za-z0-9_-]{10,}|AIza[A-Za-z0-9_-]{12,})') {
        Record '[ligne potentiellement sensible masquee]'
      } elseif ($Line.Trim()) { Record $Line }
    }
  } catch { Record ('Erreur commande ' + $Name + ': ' + $_.Exception.GetType().Name) }
}
Record ("Diagnostic Hermes " + (Get-Date -Format 's'))
$Root = Join-Path $env:LOCALAPPDATA 'hermes'
Record ("Hermes root present: " + (Test-Path $Root))
foreach ($Profile in @('default','cronos','cronoslocal')) {
  $Config = if ($Profile -eq 'default') { Join-Path $Root 'config.yaml' } else { Join-Path $Root "profiles\$Profile\config.yaml" }
  Record ("[$Profile] config: " + (Test-Path $Config))
  if (Test-Path $Config) {
    $Text = [IO.File]::ReadAllText($Config)
    Record ("[$Profile] fallback_providers: " + [regex]::IsMatch($Text, '(?m)^fallback_providers\s*:'))
  }
}
if (Get-Command hermes -ErrorAction SilentlyContinue) {
  SafeCommand 'version' @('hermes','--version')
  SafeCommand 'profils' @('hermes','profile','list')
  SafeCommand 'gateway' @('hermes','gateway','status')
  SafeCommand 'fallback cronos' @('hermes','-p','cronos','fallback','check')
  SafeCommand 'fallback cronoslocal' @('hermes','-p','cronoslocal','fallback','check')
} else { Record 'hermes absent du PATH' }
if (Get-Command ollama -ErrorAction SilentlyContinue) {
  SafeCommand 'ollama list' @('ollama','list')
  SafeCommand 'ollama ps' @('ollama','ps')
} else { Record 'ollama absent du PATH' }
$Results | Set-Content -LiteralPath $Out -Encoding UTF8
Record ("Rapport ecrit : " + $Out)
Record 'Avant de partager un rapport, relisez-le pour verifier les donnees privees.'
