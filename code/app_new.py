import base64
import tempfile
import os
import subprocess
import shutil
import json
from PyPDF2 import PdfMerger
import logging
from flask import Flask, request, Response, render_template, send_from_directory, jsonify
from waitress import serve

app = Flask(__name__, template_folder='templates', static_folder='static')

# Ruta principal
@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

# Ruta para verificar si LibreOffice está disponible
@app.route("/check-libreoffice", methods=["GET"])
def check_libreoffice():
    libreoffice_paths = [
        "libreoffice",  # Linux/Mac o Windows con LibreOffice en PATH
        r"C:\Program Files\LibreOffice\program\soffice.exe",  # Instalación típica en Windows
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",  # Instalación típica en Windows (32 bits)
        r"C:\Program Files\LibreOffice\soffice.exe"  # Otra ubicación posible
    ]
    
    for path in libreoffice_paths:
        try:
            # Intentamos ejecutar con --version para verificar si existe
            result = subprocess.run([path, "--version"], check=True, capture_output=True, text=True)
            version = result.stdout.strip() if result.stdout else "Versión desconocida"
            
            # Si llegamos aquí, LibreOffice está instalado
            logging.info(f"LibreOffice encontrado: {path} ({version})")
            return jsonify({
                "available": True,
                "path": path,
                "version": version,
                "message": f"LibreOffice está disponible: {version}"
            })
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logging.warning(f"Intento fallido con {path}: {str(e)}")
            continue
      # Si llegamos aquí, no se encontró LibreOffice
    logging.error("No se encontró LibreOffice instalado en el sistema")
    return jsonify({
        "available": False,
        "message": "No se encontró LibreOffice instalado en el sistema. La conversión podría no funcionar correctamente. Para una experiencia completa, considera usar Docker o instalar LibreOffice."
    })

# Ruta para acceder a los ejemplos
@app.route("/examples/<filename>", methods=["GET"])
def get_example(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'examples'),
                              filename)

@app.route("/hello", methods=["GET"])
def hello_world():
    return "Hello, World!"

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.svg', mimetype='image/svg+xml')

@app.route("/convert", methods=["POST"])
def convert_word_to_pdf():
    logging.info("La función de activación HTTP de Python procesa una solicitud.")

    # Inicializar pdf_final_path
    pdf_final_path = None
    temp_dir = None

    try:
        # Obtener los archivos Word en Base64 desde la solicitud HTTP
        req_body = request.get_json()
        archivos_base64 = req_body.get("archivos")

        logging.info(f"Archivos recibidos: {len(archivos_base64)}")

        if not archivos_base64 or not isinstance(archivos_base64, list):
            return Response(
                "Debe proporcionar una lista de archivos Word en Base64.",
                status=400
            )

        # Crear un directorio temporal para los archivos DOCX y PDFs
        temp_dir = tempfile.mkdtemp()
        pdf_paths = []

        # Procesar cada archivo DOCX
        for i, archivo_base64 in enumerate(archivos_base64):
            logging.info(f"Procesando archivo {i + 1}...")

            try:
                # Validar y decodificar el archivo Word desde Base64
                archivo_bytes = base64.b64decode(archivo_base64, validate=True)
            except base64.binascii.Error:
                logging.error(f"Archivo {i + 1} no es Base64 válido.")
                return Response(
                    f"Archivo {i + 1} no es Base64 válido.",
                    status=400
                )

            # Guardar el archivo Word temporalmente
            docx_path = os.path.join(temp_dir, f"temp_{i}.docx")
            with open(docx_path, "wb") as temp_file:
                temp_file.write(archivo_bytes)
                  
            # Convertir el archivo DOCX a PDF usando LibreOffice
            pdf_path = os.path.join(temp_dir, f"temp_{i}.pdf")
            logging.info(f"Convirtiendo {docx_path} a {pdf_path}...")
            if not convert_docx_to_pdf_with_libreoffice(docx_path, pdf_path):
                logging.error(f"Falló la conversión del archivo {docx_path}. Continuando con el siguiente...")
                continue  # Continuar con el siguiente archivo si hay un error
            
            pdf_paths.append(pdf_path)

            # Eliminar el archivo DOCX temporal
            os.unlink(docx_path)

        if not pdf_paths:
            return Response(
                "No se pudo convertir ningún archivo a PDF.",
                status=400
            )

        # Combinar todos los PDFs en uno solo
        pdf_final_path = os.path.join(temp_dir, "output.pdf")
        merger = PdfMerger()

        for pdf_path in pdf_paths:
            merger.append(pdf_path)

        merger.write(pdf_final_path)
        merger.close()

        # Leer el PDF final y devolverlo como respuesta
        with open(pdf_final_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()

        return Response(
            pdf_bytes,
            mimetype="application/pdf",
            headers={"Content-Disposition": "attachment; filename=output.pdf"}
        )

    except Exception as e:
        logging.error(f"Error: {str(e)}", exc_info=True)
        return Response(
            f"Ocurrió un error al procesar los archivos: {str(e)}",
            status=500
        )

    finally:
        # Eliminar los archivos y directorios temporales
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)

def convert_docx_to_pdf_with_libreoffice(docx_path, pdf_path):
    try:
        # Verificamos que exista LibreOffice en el sistema
        libreoffice_paths = [
            "libreoffice",  # Linux/Mac o Windows con LibreOffice en PATH
            r"C:\Program Files\LibreOffice\program\soffice.exe",  # Instalación típica en Windows
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",  # Instalación típica en Windows (32 bits)
            r"C:\Program Files\LibreOffice\soffice.exe"  # Otra ubicación posible
        ]
        
        libreoffice_cmd = None
        for path in libreoffice_paths:
            try:
                # Intentamos ejecutar con --version para verificar si existe
                subprocess.run([path, "--version"], check=True, capture_output=True)
                libreoffice_cmd = path
                logging.info(f"Usando LibreOffice en: {path}")
                break
            except (subprocess.SubprocessError, FileNotFoundError):
                continue
        
        if not libreoffice_cmd:
            logging.error("No se pudo encontrar LibreOffice en el sistema.")
            return False
        
        # Verificar que el archivo DOCX existe
        if not os.path.exists(docx_path):
            logging.error(f"El archivo no existe: {docx_path}")
            return False
        
        # Crear el directorio de salida si no existe
        output_dir = os.path.dirname(pdf_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # Ejecutar LibreOffice para convertir el documento
        # Añadir --nologo para evitar la pantalla de inicio
        logging.info(f"Convirtiendo {docx_path} a PDF usando LibreOffice...")
        result = subprocess.run(
            [libreoffice_cmd, "--headless", "--nologo", "--convert-to", "pdf", docx_path, "--outdir", output_dir],
            check=True,
            capture_output=True,
            text=True,
            timeout=60  # Timeout de 60 segundos
        )
        
        # Registrar la salida de LibreOffice para depuración
        if result.stdout:
            logging.info(f"Salida de LibreOffice: {result.stdout}")
        
        # Verificar que el PDF fue creado correctamente
        expected_pdf_path = os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(docx_path))[0] + ".pdf"
        )
        
        if expected_pdf_path != pdf_path and os.path.exists(expected_pdf_path):
            # Si LibreOffice generó el PDF con un nombre diferente, lo renombramos
            logging.info(f"Renombrando {expected_pdf_path} a {pdf_path}")
            os.rename(expected_pdf_path, pdf_path)
        
        # Verificar que el archivo PDF se creó y tiene un tamaño razonable
        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
            logging.info(f"PDF creado correctamente: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
            return True
        else:
            logging.error(f"No se pudo crear el PDF o el archivo está vacío: {pdf_path}")
            return False
            
    except subprocess.TimeoutExpired:
        logging.error(f"Timeout al convertir {docx_path} a PDF")
        return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al convertir {docx_path} a PDF con LibreOffice: {str(e)}")
        if e.stderr:
            logging.error(f"Salida de error: {e.stderr}")
        return False
    except Exception as e:
        logging.error(f"Error inesperado al convertir {docx_path} a PDF: {str(e)}")
        return False

if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Verifica si estamos en un entorno de desarrollo
    if os.environ.get("FLASK_ENV") == "development":
        print("Iniciando el servidor en modo de desarrollo...")
        port = int(os.environ.get("PORT", 5000))
        print(f"📋 Conversor Word a PDF disponible en: http://localhost:{port}")
        print(f"🔗 Abre esta URL en tu navegador: http://localhost:{port}")
        app.run(host="0.0.0.0", port=port, debug=True)
    else:
        # Ejecuta Waitress en producción
        print("Iniciando el servidor con Waitress...")
        port = int(os.environ.get("PORT", 5000))
        print(f"📋 Conversor Word a PDF disponible en: http://localhost:{port}")
        print(f"🔗 Abre esta URL en tu navegador: http://localhost:{port}")
        serve(app, host="0.0.0.0", port=port, threads=4)
