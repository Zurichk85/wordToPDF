# Conversor de Word a PDF

Una aplicación web moderna para convertir documentos de Microsoft Word (.docx) a formato PDF utilizando LibreOffice.

## Características

- ✅ Interfaz web moderna y atractiva
- ✅ Soporte para arrastrar y soltar archivos (drag & drop)
- ✅ Conversión de alta calidad utilizando LibreOffice
- ✅ Combinación de múltiples documentos en un solo PDF
- ✅ Diseño responsive para dispositivos móviles
- ✅ Verificación automática de LibreOffice
- ✅ Documentos de ejemplo incluidos

## Requisitos previos

- Python 3.9 o superior
- LibreOffice (para la conversión de documentos)
- Pip (gestor de paquetes de Python)

## Instalación

### Opción 1: Instalación local

1. Clona este repositorio:
   ```
   git clone https://github.com/tu-usuario/wordtopdf.git
   cd wordtopdf
   ```

2. Crea un entorno virtual e instala las dependencias:
   ```
   python -m venv venv
   venv\Scripts\activate  # En Windows
   pip install -r requirements.txt
   ```

3. Ejecuta la aplicación:
   ```
   cd code
   set FLASK_ENV=development  # En Windows
   python app_new.py
   ```

4. Abre tu navegador en `http://localhost:5000`

### Opción 2: Usando Docker

1. Asegúrate de tener Docker y Docker Compose instalados

2. Ejecuta:
   ```
   docker-compose up -d
   ```

3. Abre tu navegador en `http://localhost:5000`

## Cómo usar

1. Arrastra y suelta tus archivos Word (.docx) en el área designada o haz clic para seleccionarlos
2. Haz clic en "Convertir a PDF"
3. Espera a que se complete la conversión
4. Descarga el archivo PDF resultante

## Solución de problemas

Si la conversión no funciona correctamente, verifica:

1. Que LibreOffice esté instalado correctamente en tu sistema
2. Que los archivos Word estén en formato .docx (no .doc)
3. Que los archivos no contengan macros complejas

Para un funcionamiento sin problemas, se recomienda usar la versión Docker.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.
