# Django Base Project

Este es un proyecto base de Django diseñado específicamente para estructurar y organizar proyectos grandes. Proporciona una estructura escalable y está preparado para ser utilizado con una base de datos PostgreSQL.

## 🚀 Pasos de instalación

### 1. Crear un entorno virtual

Utilizamos `venv` para manejar entornos virtuales. Para crear un nuevo entorno virtual llamado `optica-total`, ejecuta:

python3 -m venv optica-total


Activar el entorno virtual:

- **Linux o Mac**:

source optica-total/bin/activate

- **Windows**:

cd optica-total

cd Scripts

```\.activate```


### 2. Instalación de dependencias

Una vez dentro del entorno virtual, navega hasta la raíz del proyecto y ejecuta:

pip install -r requirements/base.txt

Para el desarrollo local, instala las dependencias específicas con:

pip install -r requirements/local.txt

Y para producción:

pip install -r requirements/prod.txt

### 3. Configuración de credenciales

Dentro de la raíz del proyecto, crea un archivo llamado `secret.json` con la siguiente estructura:

```json
{
    "FILENAME": "secret.json",
    "SECRET_KEY": "clave_secreta_pedir_administrador_del_sistema",
    "DB_NAME": "name_db",
    "DB_USER": "name_user_db",
    "DB_PASSWORD": "password_db"
}
```
Nota: Asegúrate de cambiar los valores de SECRET_KEY, DB_NAME, DB_USER y DB_PASSWORD a los apropiados para tu configuración.

### 4. Configuración de la base de datos

Dado que utilizamos PostgreSQL como base de datos, asegúrate de tenerlo instalado y en ejecución.

### 5. Crear y aplicar migraciones

Para crear las migraciones y aplicarlas, ejecuta:

python project/manage.py makemigrations
python project/manage.py migrate

### 5. Ejecutar el proyecto

python project/manage.py runserver

¡Listo! Ahora puedes acceder a tu proyecto Django desde http://localhost:8000/.