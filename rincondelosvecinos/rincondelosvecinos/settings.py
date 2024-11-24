from pathlib import Path
import os

from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-4_xg*7l*j$3=6s&ipv7_6fqb_x9f8vppu=!2cznj(l!+(j3^os'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rincondelosvecinos',  # Otros apps de tu proyecto
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rincondelosvecinos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'rincondelosvecinos' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rincondelosvecinos.wsgi.application'

# Configuración de la base de datos RDS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Tienda',
        'USER': 'PauxSy',
        'PASSWORD': 'nYsyHGzsjGmU3HNc4N6t',
        'HOST': 'database-1.cfaqqaiswgff.us-east-2.rds.amazonaws.com',
        'PORT': '3306'
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Configuración de archivos estáticos en local
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'rincondelosvecinos' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directorio para `collectstatic`

# Configuración de archivos media en local
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'





# Gmail que será utilizado como remitente para enviar los correos electrónicos.

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'           # Servidor SMTP de Gmail
EMAIL_PORT = 587                        # Puerto para conexiones TLS
EMAIL_USE_TLS = True                    # Habilitar TLS
EMAIL_HOST_USER = 'elrincondelosvecinoschile@gmail.com' # Tu correo de Gmail
EMAIL_HOST_PASSWORD = 'oaqm gsfk dddg cumr'      # Tu contraseña de Gmail (o la contraseña de aplicación)
DEFAULT_FROM_EMAIL = 'elrincondelosvecinoschile@gmail.com'

AUTH_USER_MODEL = 'rincondelosvecinos.Usuario'

SESSION_SAVE_EVERY_REQUEST = True

AUTHENTICATION_BACKENDS = [
    'rincondelosvecinos.backends.EmailBackend',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 semanas
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False