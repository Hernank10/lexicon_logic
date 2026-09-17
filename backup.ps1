$fecha = Get-Date -Format "yyyyMMdd_HHmm"
$origen = "E:\02_proyectos\lexicon_logic\_original"
$destino = "E:\01_entorno\backups\lexicon_logic_$fecha"

Write-Host "=== Backup Lexicon Logic ==="
Write-Host "Origen:  $origen"
Write-Host "Destino: $destino"
Write-Host ""

robocopy $origen $destino /E /XD __pycache__ .git /XF *.pyc

Write-Host ""
Write-Host "=== Backup completado ==="
Write-Host "Ruta: $destino"