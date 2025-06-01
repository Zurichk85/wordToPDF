# Despliegue en Render.com

Esta guía te ayudará a desplegar el Conversor Word a PDF en Render.com.

## Requisitos previos

1. Una cuenta en [Render.com](https://render.com)
2. Una cuenta en GitHub, GitLab o Bitbucket para alojar tu código

## Pasos para el despliegue

### 1. Subir tu código a un repositorio Git

```bash
git init
git add .
git commit -m "Versión inicial del conversor Word a PDF"
git remote add origin https://github.com/tu-usuario/wordtopdf.git
git push -u origin main
```

### 2. Crear un nuevo servicio Web en Render

1. Inicia sesión en tu cuenta de Render
2. Haz clic en "New +" y selecciona "Web Service"
3. Conecta tu repositorio de GitHub/GitLab/Bitbucket
4. Selecciona el repositorio que contiene el código del conversor
5. Configura el servicio:
   - **Name**: wordtopdf-converter (o el nombre que prefieras)
   - **Environment**: Docker
   - **Branch**: main (o la rama que estés usando)
   - **Region**: El más cercano a tus usuarios
   - **Plan**: Free (o un plan de pago si necesitas más recursos)

### 3. Variables de entorno (opcional)

Ya están configuradas en el archivo `render.yaml`, pero puedes añadir más si es necesario:

- `FLASK_ENV`: production
- `DOCKER`: yes

### 4. Despliegue

Haz clic en "Create Web Service" y espera a que se complete el despliegue.

## Verificación

Una vez desplegado, podrás acceder a tu conversor en la URL proporcionada por Render, generalmente con el formato:
`https://wordtopdf-converter.onrender.com`

Para verificar que todo funciona correctamente, visita:
`https://wordtopdf-converter.onrender.com/hello`

Deberías recibir el mensaje "Hello, World!" si el servicio está funcionando correctamente.

## Solución de problemas

Si encuentras problemas con el despliegue:

1. Verifica los logs en el dashboard de Render
2. Asegúrate de que todas las dependencias están correctamente instaladas
3. Verifica que LibreOffice se haya instalado correctamente en el contenedor
