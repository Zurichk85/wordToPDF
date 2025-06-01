"""
Script para verificar si LibreOffice está instalado correctamente en el sistema.
"""
import subprocess
import sys
import os
import platform
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def check_libreoffice():
    """Verifica si LibreOffice está instalado y accesible."""
    system = platform.system()
    
    if system == "Windows":
        libreoffice_paths = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
            r"C:\Program Files\LibreOffice\soffice.exe"
        ]
    elif system == "Darwin":  # macOS
        libreoffice_paths = [
            "/Applications/LibreOffice.app/Contents/MacOS/soffice",
            "/Applications/LibreOffice.app/Contents/MacOS/soffice.bin"
        ]
    else:  # Linux y otros
        libreoffice_paths = [
            "libreoffice",
            "soffice",
            "/usr/bin/libreoffice",
            "/usr/bin/soffice"
        ]
    
    # Añadir búsqueda en PATH
    if system == "Windows":
        for path in os.environ.get("PATH", "").split(os.pathsep):
            if os.path.isdir(path):
                for exe in ["soffice.exe", "libreoffice.exe"]:
                    full_path = os.path.join(path, exe)
                    if os.path.isfile(full_path):
                        libreoffice_paths.append(full_path)
    
    for path in libreoffice_paths:
        try:
            result = subprocess.run([path, "--version"], check=True, capture_output=True, text=True)
            version = result.stdout.strip() if result.stdout else "Versión desconocida"
            logging.info(f"✅ LibreOffice encontrado: {path}")
            logging.info(f"   Versión: {version}")
            return True, path, version
        except (subprocess.SubprocessError, FileNotFoundError):
            continue
    
    return False, None, None

def print_installation_instructions():
    """Muestra instrucciones para instalar LibreOffice."""
    system = platform.system()
    
    print("\n" + "="*80)
    print("INSTRUCCIONES PARA INSTALAR LIBREOFFICE")
    print("="*80)
    
    if system == "Windows":
        print("""
1. Descarga LibreOffice desde el sitio oficial:
   https://www.libreoffice.org/download/download/

2. Ejecuta el instalador y sigue las instrucciones.

3. Asegúrate de reiniciar tu ordenador después de la instalación.
        """)
    elif system == "Darwin":  # macOS
        print("""
1. Descarga LibreOffice desde el sitio oficial:
   https://www.libreoffice.org/download/download/

2. Abre el archivo .dmg descargado y arrastra LibreOffice a la carpeta Aplicaciones.

3. Para iniciar LibreOffice, haz doble clic en el icono de la aplicación.
        """)
    else:  # Linux
        print("""
Instala LibreOffice usando el gestor de paquetes de tu distribución:

Ubuntu/Debian:
   sudo apt update
   sudo apt install libreoffice

Fedora:
   sudo dnf install libreoffice

Arch Linux:
   sudo pacman -S libreoffice-still
        """)
    
    print("\nDespués de instalar LibreOffice, ejecuta este script nuevamente para verificar.")
    print("="*80)

def main():
    print("Verificando la instalación de LibreOffice...")
    libreoffice_installed, path, version = check_libreoffice()
    
    if libreoffice_installed:
        print("\n✅ LibreOffice está correctamente instalado.")
        print(f"   Ruta: {path}")
        print(f"   Versión: {version}")
        print("\nEl conversor de Word a PDF debería funcionar correctamente.")
    else:
        print("\n❌ No se encontró LibreOffice en el sistema.")
        print("El conversor de Word a PDF no funcionará sin LibreOffice.")
        print_installation_instructions()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
