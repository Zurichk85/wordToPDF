from PIL import Image
import os

# Obtener la ruta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'static')

# Crear un favicon básico (azul con rojo)
img = Image.new('RGB', (48, 48), color=(37, 99, 235))  # Color azul de nuestro tema

# Crear una forma simple para el favicon
for x in range(10, 38):
    for y in range(10, 38):
        # Dibujar un cuadrado rojo más pequeño dentro
        if 15 <= x <= 33 and 15 <= y <= 33:
            img.putpixel((x, y), (239, 68, 68))  # Color rojo de nuestro tema

# Guardar como ICO
favicon_path = os.path.join(static_dir, 'favicon.ico')
img.save(favicon_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])

print(f"Favicon creado en: {favicon_path}")
