# Script de PowerShell para iniciar el Conversor de Word a PDF

Write-Host "Iniciando el Conversor de Word a PDF..." -ForegroundColor Cyan
Write-Host ""

# Verificar si LibreOffice está instalado
Write-Host "Verificando la instalación de LibreOffice..." -ForegroundColor Yellow
.\Scripts\python.exe code\check_libreoffice.py
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Advertencia: La aplicación intentará ejecutarse sin LibreOffice." -ForegroundColor Red
    Write-Host "Es posible que la conversión no funcione correctamente." -ForegroundColor Red
    Write-Host ""
    Write-Host "Presiona cualquier tecla para continuar..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

Write-Host ""
Write-Host "Iniciando la aplicación web..." -ForegroundColor Green
Write-Host ""

# Configurar variables de entorno
$env:FLASK_ENV = "development"
$env:FLASK_APP = "code\app_new.py"

# Iniciar la aplicación Flask
.\Scripts\python.exe code\app_new.py

Write-Host "Presiona cualquier tecla para salir..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
