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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade -r /usr/src/app/requirements.txt

# Configurar variables de entorno para Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
# ENV FLASK_ENV=production
ENV FLASK_ENV=development
ENV FLASK_DEBUG=True

# Exponer el puerto que Render usará dinámicamente
EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]
# # Comando para ejecutar la aplicación con Gunicorn
# CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
