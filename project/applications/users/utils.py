import os
from PIL import Image, ImageDraw, ImageFont

from project.settings.local import MEDIA_ROOT

def generate_profile_img(first_name, last_name):
    # Definir el tamaño y el fondo de la imagen
    width, height = 200, 200
    background_color=(42,123,228)

    # Crear una nueva imagen
    image = Image.new('RGB', (width, height), background_color)

    # Obtener el objeto de dibujo
    draw = ImageDraw.Draw(image)

    # Definir las iniciales y el tamaño de la fuente
    initials = first_name[0] + last_name[0]
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

    # Crear el directorio de medios si no existe
    media_directory = MEDIA_ROOT
    if not os.path.exists(media_directory):
        os.makedirs(media_directory)

    # Ruta completa del archivo
    file_path = os.path.join(media_directory, f'{initials}.png')

    # Dibujar el texto en la imagen con el color especificado
    draw.text((x, y), initials, align='center', font=font)

    # Guardar la imagen en el directorio de medios
    image.save(file_path)
