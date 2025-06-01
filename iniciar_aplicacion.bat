@echo off
echo Iniciando el Conversor de Word a PDF...
echo.

rem Verificar si LibreOffice está instalado
echo Verificando la instalación de LibreOffice...
.\Scripts\python.exe code\check_libreoffice.py
if %errorlevel% neq 0 (
    echo.
    echo Advertencia: La aplicación intentará ejecutarse sin LibreOffice.
    echo Es posible que la conversión no funcione correctamente.
    echo.
    pause
)

echo.
echo Iniciando la aplicación web...
echo.

rem Configurar variables de entorno
set FLASK_ENV=development
set FLASK_APP=code\app_new.py

rem Iniciar la aplicación Flask
.\Scripts\python.exe code\app_new.py

pause
