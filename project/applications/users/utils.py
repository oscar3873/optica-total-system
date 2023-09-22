from django.contrib.auth.models import User  # O utiliza tu propio modelo de usuario si tienes uno personalizado
from PIL import Image, ImageDraw, ImageFont
import io

def generate_profile_img_and_assign(user):
    # Definir el tamaño y el fondo de la imagen
    width, height = 200, 200
    background_color=(42, 123, 228)

    # Crear una nueva imagen
    image = Image.new('RGB', (width, height), background_color)

    # Obtener el objeto de dibujo
    draw = ImageDraw.Draw(image)

    # Definir las iniciales y el tamaño de la fuente
    initials = user.first_name[0] + user.last_name[0]
    font_size = 120

    # Definir el tipo de fuente
    font = ImageFont.truetype('static/fonts/poppins-semibold.ttf', font_size)

    # Obtener el cuadro delimitador del texto
    text_bbox = draw.textbbox((0, 0), initials, font=font)

    # Calcular el ancho y alto del texto a partir del cuadro delimitador
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Calcular la posición del texto en el centro de la imagen
    x = (width - text_width) // 2
    y = (height - text_height) // 2 - text_bbox[1]

    # Dibujar el texto en la imagen con el color especificado
    draw.text((x, y), initials, align='center', font=font)

    # Guardar la imagen en un búfer de memoria
    image_buffer = io.BytesIO()
    image.save(image_buffer, format='PNG')
    image_buffer.seek(0)

    # Asignar la imagen al campo imagen_perfil del usuario
    user.imagen.save(f'{user.username}_profile.png', image_buffer, save=True)

    # Guardar el usuario para actualizar la imagen en la base de datos
    user.save()
