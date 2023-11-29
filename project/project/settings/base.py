"""
Configuracion base que todos necesitan para funcionar.
"""
import django_on_heroku
import json
import pytz
import os

from datetime import datetime
from django.core.exceptions import ImproperlyConfigured
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # El directorio raiz de la aplicacion.
# SECURITY WARNING: keep the secret key used in production secret!

# Verificar si estamos en entorno de desarrollo o producción
DEVELOPMENT_ENVIRONMENT = os.environ.get("DEVELOPMENT_ENVIRONMENT", "False").lower() == "true"

# Configuración de secretos
if DEVELOPMENT_ENVIRONMENT:
    # En entorno de desarrollo, cargar desde secret.json
    with open("secret.json") as f:
        secret = json.loads(f.read())
else:
    # En entorno de producción, usar variables de entorno
    secret = {
        "SECRET_KEY": os.environ.get("SECRET_KEY"),
        "EMAIL_HOST": os.environ.get("EMAIL_HOST"),
        "EMAIL_HOST_USER": os.environ.get("EMAIL_HOST_USER"),
        "EMAIL_HOST_PASSWORD": os.environ.get("EMAIL_HOST_PASSWORD"),
        "DB_NAME": os.environ.get('DB_NAME'),
        "DB_USER": os.environ.get('DB_USER'),
        "DB_PASSWORD": os.environ.get('DB_PASSWORD'),
        "DB_HOST": os.environ.get('DB_HOST'),
        "DB_PORT": os.environ.get('DB_PORT'),
        # Agrega otras variables según sea necesario
    }

def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except KeyError:
        raise ImproperlyConfigured("Set the {} environment variable".format(secret_name))

SECRET_KEY = get_secret('SECRET_KEY')


# Application definition
DJANGO_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize"
)

LOCAL_APPS = (
    "applications.users",
    "applications.clients",
    "applications.branches",
    "applications.core",
    "applications.employes",
    "applications.notes",
    "applications.products",
    "applications.suppliers",
    "applications.dashboard",
    "applications.sales",
    "applications.cashregister",
    "applications.notifications",
    "applications.promotions",
)

THIRD_PARTY_APPS = (
    "daphne",
    # "pyafipws"
    "django_afip",
)


###########  *CHANNEL PARA NOTIFICACIONES DE NOTAS*  ############## 
ASGI_APPLICATION = "project.asgi.application"  # Reemplaza 'project' con el nombre real de tu proyecto

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/1")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
        "OPTIONS": {
            "websocket_timeout": 300,
            "websocket_max_connections": 10000,
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [REDIS_URL],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "ssl_cert_reqs": None
            },
        }
    }
}

####################################################################


INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # BRANCH context_processors: para que este siempre presente el "switch" para cambiar sucursal (ADMIN)
                'applications.branches.context_processors.branches',
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "users.User"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "es"

TIME_ZONE = "America/Argentina/Buenos_Aires"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ZONE_TIME = pytz.timezone('America/Argentina/Buenos_Aires')
DATE_NOW = datetime.now(ZONE_TIME)

# Separadores de miles y decimales
# https://docs.djangoproject.com/en/4.2/ref/settings/#localization

THOUSAND_SEPARATOR = ','
DECIMAL_SEPARATOR = '.'

# Email settings for sending emails
EMAIL_HOST = get_secret('EMAIL_HOST')
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# Login
LOGIN_URL = 'users_app:login'
LOGIN_REDIRECT_URL = 'core_app:home'
LOGOUT_URL = 'users_app:logout'
LOGOUT_REDIRECT_URL = 'users_app:login'

# prod.py
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Configuración para el uso de base de datos en Heroku

if DEVELOPMENT_ENVIRONMENT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': get_secret('DB_NAME'),
            'USER': get_secret('DB_USER'),
            'PASSWORD': get_secret('DB_PASSWORD'),
            'HOST': get_secret('DB_HOST'),
            'PORT': get_secret('DB_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'DB_NAME': os.environ.get('DB_NAME'),
            'DB_USER': os.environ.get('DB_USER'),
            'DB_PASSWORD': os.environ.get('DB_PASSWORD'),
            'DB_HOST': os.environ.get('DB_HOST'),
            'DB_PORT': os.environ.get('DB_PORT'),
        }
    }

# Configuraciones de static y media
STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

django_on_heroku.settings(locals())