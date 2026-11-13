# Audit local en lecture seule. Ne touche ni aux profils ni au Kanban.
$ErrorActionPreference = 'Continue'
function Run([string[]]$ArgsArray) {
  Write-Host "`n> hermes $($ArgsArray -join ' ')"
  try { & hermes @ArgsArray 2>&1 | Select-Object -Last 75 } catch { Write-Warning "Hermes indisponible: $($_.Exception.Message)" }
}
Write-Host "=== CHRONOS/HERMES - DIAGNOSTIC READ-ONLY ==="
try { hermes --version } catch { Write-Warning "hermes absent du PATH" }
Run @('profile','list')
Run @('-p','cronos','status')
Run @('-p','cronos','fallback','list')
Run @('-p','cronos','fallback','check')
Run @('--version')
Run @('kanban','--board','default','list')
Run @('kanban','--board','default','show','t_67b6eb5e','--json')
Run @('kanban','--board','default','runs','t_67b6eb5e')
Run @('kanban','--board','default','log','t_67b6eb5e','--tail','5000')
Write-Host "`n=== OLLAMA ==="
try { ollama list } catch { Write-Warning "Ollama indisponible" }
foreach ($url in @('http://127.0.0.1:11434/api/tags','http://127.0.0.1:18888/health')) {
  try { $d=Invoke-RestMethod -Uri $url -TimeoutSec 4; Write-Host "OK $url"; ($d | ConvertTo-Json -Depth 5) }
  catch { Write-Warning "KO $url : $($_.Exception.Message)" }
}
Write-Host "`nLecture seule terminée. Ne partage pas de clé API ou d'URL avec jeton dans des journaux publics."