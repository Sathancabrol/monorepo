# Installs only small optional pose assets; no administrator, no diffusion weights.
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$Vendor = Join-Path $Root 'vfxlab\vendor'
$Wasm = Join-Path $Vendor 'wasm'
New-Item -ItemType Directory -Force -Path $Wasm | Out-Null
$Version = '0.10.14'
$Base = "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@$Version"
$Files = @{
 'vision_bundle.mjs' = "$Base/vision_bundle.mjs"
 'wasm\vision_wasm_internal.js' = "$Base/wasm/vision_wasm_internal.js"
 'wasm\vision_wasm_internal.wasm' = "$Base/wasm/vision_wasm_internal.wasm"
 'wasm\vision_wasm_nosimd_internal.js' = "$Base/wasm/vision_wasm_nosimd_internal.js"
 'wasm\vision_wasm_nosimd_internal.wasm' = "$Base/wasm/vision_wasm_nosimd_internal.wasm"
 'pose_landmarker_lite.task' = 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task'
}
foreach($Name in $Files.Keys){
 $Path = Join-Path $Vendor $Name
 if(Test-Path $Path){ if((Get-Item $Path).Length -gt 0){ Write-Host "Reuse $Name"; continue } }
 $Temp = "$Path.download"
 try {
  Invoke-WebRequest -Uri $Files[$Name] -OutFile $Temp -UseBasicParsing -TimeoutSec 90
  if((Get-Item $Temp).Length -lt 100){ throw "Invalid asset $Name" }
  Move-Item -LiteralPath $Temp -Destination $Path -Force
 } finally { if(Test-Path $Temp){ Remove-Item -LiteralPath $Temp -Force } }
}
Get-ChildItem $Vendor -Recurse -File | Get-FileHash -Algorithm SHA256 | Format-Table -AutoSize
Write-Host 'Assets installed. Verify hashes and licenses against upstream; no runtime CDN required.'
