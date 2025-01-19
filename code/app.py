import base64
import tempfile
import os
import subprocess
import shutil
from PyPDF2 import PdfMerger
import logging
from flask import Flask, request, Response
from waitress import serve

app = Flask(__name__)

@app.route("/hello", methods=["GET"])
def hello_world():
    return "Hello, World!"

@app.route("/convert", methods=["POST"])
def convert_word_to_pdf():
    logging.info("La función de activación HTTP de Python procesa una solicitud.")

    # Inicializar pdf_final_path
    pdf_final_path = None

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
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)

def convert_docx_to_pdf_with_libreoffice(docx_path, pdf_path):
    try:
        subprocess.run(
            ["libreoffice", "--headless", "--convert-to", "pdf", docx_path, "--outdir", os.path.dirname(pdf_path)],
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al convertir {docx_path} a PDF con LibreOffice: {str(e)}")
        return False

if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Verifica si estamos en un entorno de desarrollo
    print(f"FLASK_ENV: {os.environ.get('FLASK_ENV')}")
    if os.environ.get("FLASK_ENV") == "development":
        print("Iniciando el servidor en modo de desarrollo...")
        port = int(os.environ.get("PORT", 5000))  # Usa el puerto de la variable de entorno
        app.run(host="0.0.0.0", port=port)
    else:
        # Ejecuta Waitress en producción
        print("Iniciando el servidor con Waitress...")
        port = int(os.environ.get("PORT", 5000))  # Usa el puerto de la variable de entorno
        serve(app, host="0.0.0.0", port=port, threads=4)
