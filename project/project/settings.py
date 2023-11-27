"""
Configuracion base que todos necesitan para funcionar.
"""
import pytz
import os
import environ
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # El directorio raiz de la aplicacion.
# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get('SECRET_KEY', 'your-fallback-secret-key')

# Configura la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd50er38v1mgi7v',
        'USER': 'qzjbmjiyvpiyki',
        'PASSWORD': '1f7b60eca03f688320b893eaec182c3d77e49ce4130463d6b0144672f3206cc7',
        'HOST': 'ec2-34-238-201-192.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

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
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

ASGI_APPLICATION = "project.asgi.application"  # Reemplaza 'project' con el nombre real de tu proyecto
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

# Separadores de miles y decimales
THOUSAND_SEPARATOR = ','
DECIMAL_SEPARATOR = '.'

# Configuraciones de email
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# Configuraciones de login
LOGIN_URL = 'users_app:login'
LOGIN_REDIRECT_URL = 'core_app:home'
LOGOUT_URL = 'users_app:logout'
LOGOUT_REDIRECT_URL = 'users_app:login'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# Configuraciones de static y media
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR/ "media"
