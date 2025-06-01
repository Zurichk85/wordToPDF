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

# Crear un documento de ejemplo simple
RUN echo "<html><body><h1>Documento de Ejemplo</h1><p>Este es un documento de ejemplo para probar la conversión.</p></body></html>" > /tmp/ejemplo.html \
    && libreoffice --headless --convert-to docx --outdir /usr/src/app/static/examples /tmp/ejemplo.html \
    && mv /usr/src/app/static/examples/ejemplo.docx /usr/src/app/static/examples/documento_ejemplo.docx

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
