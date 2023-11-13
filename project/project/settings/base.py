"""
Configuracion base que todos necesitan para funcionar.
"""
from datetime import datetime
from django.core.exceptions import ImproperlyConfigured
import json
from pathlib import Path

import pytz

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # El directorio raiz de la aplicacion.
# SECURITY WARNING: keep the secret key used in production secret!

with open("secret.json") as f:
    secret = json.loads(f.read())
    
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