# Usar una imagen base ligera
FROM python:3.9-slim

# Crear el directorio de trabajo
WORKDIR /usr/src/app/

# Copiar los archivos necesarios
COPY ./code /usr/src/app/
COPY ./requirements.txt /usr/src/app/requirements.txt

# Instalar dependencias necesarias de LibreOffice
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice-common \
    libreoffice-core \
    libreoffice-writer \
    fonts-dejavu-core \
    fonts-liberation \
    fonts-noto \
    fonts-noto-cjk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade -r /usr/src/app/requirements.txt

# Crear directorios necesarios
RUN mkdir -p /usr/src/app/static/examples

# Crear un documento de ejemplo simple usando python-docx
RUN echo 'from docx import Document; \
doc = Document(); \
doc.add_heading("Documento de Ejemplo", 0); \
doc.add_paragraph("Este es un documento de ejemplo para probar la conversión de Word a PDF."); \
doc.add_heading("Características", level=1); \
doc.add_paragraph("• Conversión rápida y precisa"); \
doc.add_paragraph("• Mantiene el formato original"); \
doc.add_paragraph("• Soporta documentos complejos"); \
doc.save("/usr/src/app/static/examples/documento_ejemplo.docx")' > /tmp/create_example.py && \
    python /tmp/create_example.py

# Configurar variables de entorno para Flask
ENV FLASK_APP=app_new.py
ENV FLASK_RUN_HOST=0.0.0.0
# PORT lo establecerá automáticamente Render
ENV PYTHONUNBUFFERED=1
# Indicar que estamos en un entorno de producción en Docker
ENV DOCKER=yes

# Exponer el puerto (Render asignará su propio puerto)
EXPOSE $PORT

# Comando para ejecutar la aplicación con Waitress para producción
CMD python app_new.py
