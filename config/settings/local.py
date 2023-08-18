from .base import *


DEBUG = True
ALLOWED_HOSTS = [
    '*'
]

DJANGO_APPS += []

PROJECT_APPS += []

THIRD_PARTY_APPS += [
    'debug_toolbar',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware" # django-debug-toolbar requirement
    ] + MIDDLEWARE

# 디폴트 데이터베이스 사용
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = BASE_DIR / 'static'

INTERNAL_IPS += [
    "127.0.0.1", # django-debug-toolbar requirement
]
