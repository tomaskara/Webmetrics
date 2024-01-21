import os
import re
from pathlib import Path

from django.template import base
from dotenv import load_dotenv

base.tag_re = re.compile(base.tag_re.pattern, re.DOTALL)
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = False

ALLOWED_HOSTS = ['www.webmetrics.cz', '127.0.0.1']

LOGIN_REDIRECT_URL = '/profile/'
LOGOUT_REDIRECT_URL = '/'

LOGIN_URL = '/login/'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'speedcheck',
    'markdownx',
    'articles',
    'allauth',
    'utm_generator'
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

ROOT_URLCONF = 'Chrome_UX_Report_website.urls'

STATIC_URL = '/static/'
if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
        '/static/',
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'Chrome_UX_Report_website.wsgi.application'

ACCOUNT_ACTIVATION_DAYS = 7


DATABASES = {
    'default': {
        'ENGINE': 'django_cockroachdb',
        'NAME': 'sp_db',
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'free-tier5.gcp-europe-west1.cockroachlabs.cloud',
        'PORT': '26257',
        'OPTIONS': {
            'sslmode': 'verify-full',
            'options': '--cluster=broad-larva-6597'
        },
    },
}

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

LANGUAGE_CODE = 'cs-cs'

TIME_ZONE = 'Europe/Prague'

USE_I18N = True

USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.seznam.cz'
EMAIL_HOST_USER = os.getenv('EMAIL')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_PORT = 465
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = 'alert@webmetrics.cz'

ACCOUNT_EMAIL_VERIFICATION = "none"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MARKDOWNX_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra'
]
