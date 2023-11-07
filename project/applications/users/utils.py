from PIL import Image, ImageDraw, ImageFont
import io

from applications.employes.models import Employee_Objetives
from applications.branches.models import Branch_Objetives

def generate_profile_img_and_assign(user):
    # Definir el tamaño y el fondo de la imagen
    width, height = 200, 200
    background_color = (42, 123, 228)

    # Crear una nueva imagen
    image = Image.new('RGB', (width, height), background_color)

    # Obtener el objeto de dibujo
    draw = ImageDraw.Draw(image)

    # Definir las iniciales y el tamaño de la fuente
    initials = user.first_name[0].upper() + user.last_name[0].upper()
    font_size = 100

    # Utilizar la fuente "DejaVu Sans"
    try:
        font = ImageFont.truetype('DejaVuSans.ttf', font_size)
    except OSError:
        font = ImageFont.load_default()

    # Obtener el cuadro delimitador del texto
    text_bbox = draw.textbbox((0, 0), initials)

    # Calcular el ancho y alto del texto a partir del cuadro delimitador
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Calcular la posición del texto en el centro de la imagen
    x = (width - text_width) // 1.5
    y = (height - text_height) // 2

    # Dibujar el texto en la imagen con el color especificado
    draw.text(((width - x) / 2 - 14, (height - y) / 2 - 14), initials, fill=(255, 255, 255), font=font, align='center')

    # Guardar la imagen en un búfer de memoria
    image_buffer = io.BytesIO()
    image.save(image_buffer, format='PNG')
    image_buffer.seek(0)

    # Asignar la imagen al campo imagen_perfil del usuario
    user.imagen.save(f'{initials}.png', image_buffer, save=True)

    # Guardar el usuario para actualizar la imagen en la base de datos
    user.save()





def fix_image_orientation(image):
    from PIL import ExifTags

    try:
        exif = image._getexif()
        if exif is not None:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            if orientation in exif:
                if exif[orientation] == 3:
                    image = image.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    image = image.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # No se pudo obtener información de orientación EXIF o la imagen no la tiene.
        pass

    return image






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


def get_emp_branch_objetives(branch, employee_objetives=None):
    employees_obj = Employee_Objetives.objects.filter(deleted_at=None, employee__user__branch=branch)
    branch_obj = Branch_Objetives.objects.filter(deleted_at=None, branch=branch)

    if employee_objetives is not None:
        employees_obj = employees_obj.exclude(id__in=employee_objetives.values('id'))

    return employees_obj, branch_obj