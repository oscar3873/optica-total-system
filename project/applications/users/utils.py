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
    initials = user.first_name[0].upper() + user.last_name[0].upper()
    font_size = 100

    # Definir el tipo de fuente
    try:
        font = ImageFont.truetype('arial.ttf', font_size)
    except OSError:
        font = ImageFont.load_default()

    # Obtener el cuadro delimitador del texto
    text_bbox = draw.textbbox((0, 0), initials)

    # Calcular el ancho y alto del texto a partir del cuadro delimitador
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Calcular la posición del texto en el centro de la imagen
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    # Dibujar el texto en la imagen con el color especificado, esta hardcodeado ...  (ESTOY CANSADO VIEJOOOO)
    draw.text(((width-x)/2 - 14, (height-y)/2 - 14), initials, fill=(255, 255, 255), font=font, align='center')

    # Guardar la imagen en un búfer de memoria
    image_buffer = io.BytesIO()
    image.save(image_buffer, format='PNG')
    image_buffer.seek(0)

    # Asignar la imagen al campo imagen_perfil del usuario
    user.imagen.save(f'{initials}.png', image_buffer, save=True)

    # Guardar el usuario para actualizar la imagen en la base de datos
    user.save()







"""Si no funcionara lo de arriba dejo algo como para implementar y refactorizar"""
"""
from PIL import Image, ImageDraw, ImageFont


def create_image(size, bgColor, message, font, fontColor):
    W, H = size
    image = Image.new('RGB', size, bgColor)
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((W-w)/2, (H-h)/2), message, font=font, fill=fontColor)
    return image

myFont = ImageFont.truetype('Roboto-Regular.ttf', 16)
myMessage = 'Hello World'
myImage = create_image((300, 200), 'yellow', myMessage, myFont, 'black')
myImage.save('hello_world.png', "PNG")


"""