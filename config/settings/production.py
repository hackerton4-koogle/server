from .base import *

DEBUG = False
ALLOWED_HOSTS = [
    "223.130.139.5",
    "127.0.0.1",
]

DJANGO_APPS += []

PROJECT_APPS += []

THIRD_PARTY_APPS += []

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

# 디폴트 데이터베이스 사용
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
