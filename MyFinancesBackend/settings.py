"""
Django settings for MyFinancesBackend project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from MyFinancesBackend.seguridad import configuracion
import os
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-@lz_xzsi44yc0^k*m(=_c$=75vuyw##792e3--!mktl6beh3gy'
SECRET_KEY = os.environ.get('SECRET_KEY',default='clave secreta')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = 'RENDER' not in os.environ
if DEBUG:
    allow_host = configuracion.LOCAL_ALLOW_HOST
    
    # ALLOWED_HOSTS = [allow_host]
    ALLOWED_HOSTS = ['10.10.0.204']

else:
   ALLOWED_HOSTS = [] 


# ALLOWED_HOSTS = ["*"]

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    ALLOWED_HOSTS.append('http://localhost:5173/')
    ALLOWED_HOSTS.append('https://my-finances-web-btxv.vercel.app/')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'Conexion',
    'rest_framework.authtoken',
    'drf_yasg',
    'corsheaders',
    'rest_framework_simplejwt',  
    'rest_framework_simplejwt.token_blacklist',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TOKEN_EXPIRED_AFTER_SECONDS=10
TOKEN_EXPIRED_AFTER_HOURS=8
TIEMPO_SESION_HORAS=8
TOKEN_SESION_TIEMPO=20

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
    ,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
ROOT_URLCONF = 'MyFinancesBackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'MyFinancesBackend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if DEBUG:
    pass_db = configuracion.PASS
    user_db = configuracion.USER
    name_db = configuracion.NAME
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': name_db,
            'USER':user_db,
            'PASSWORD':pass_db,
            'HOST':'localhost',
            'PORT':'',
            
        }
    }
else :
    DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default='postgres://conex_finanzas_user:KSOnYs6IPvVeLcDeuM9TqQZJtR1Ym72w@dpg-cnucdfmd3nmc73a9s860-a/conex_finanzas',
        conn_max_age=600
    )
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'es-py'
# TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Asuncion'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
if not DEBUG:
    
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',  
    'x-requested-with',
    'Sesion',  
    'user',
    'signal',
    'Access-Control-Allow-Origin'
]

CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:8080",
    "http://10.10.0.204:8000",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    'http://localhost:3000',
    'http://localhost:5173',
    'exp://192.168.1.103:8081',
    'http://localhost:8081',
    'https://my-finances-web-btxv.vercel.app',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_WHITELIST = [
"http://10.10.0.204:8000",
'http://127.0.0.1:3000'
'http://localhost:5173',
'http://127.0.0.1:5173',
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=20),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True
}

hostmail=configuracion.DIR_EMAIL
passmail=configuracion.PASS_EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT = 587 
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = hostmail
EMAIL_HOST_PASSWORD = passmail