"""
Django settings for lunch_log project.

Generated by 'django-admin startproject' using Django 4.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path


def env(name, default=None):
    return os.environ.get(name, default)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", "add-your-secret-here")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", "false").lower() == "true"

ALLOWED_HOSTS = str(env("ALLOWED_HOSTS", "localhost:8000")).split(",")

# CORS settings
CORS_ALLOW_CREDENTIALS = env("CORS_ALLOW_CREDENTIALS", "false").lower() == "true"
CORS_ALLOW_ALL_ORIGINS = env("CORS_ALLOW_ALL_ORIGINS", "false").lower() == "true"
CORS_ALLOWED_ORIGINS = str(env("CORS_ALLOWED_ORIGINS", "http://localhost:3000")).split(
    ","
)
CSRF_TRUSTED_ORIGINS = str(env("CSRF_TRUSTED_ORIGINS", "http://localhost:8000")).split(
    ","
)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    # Custom apps
    "apps.common",
    "apps.users",
    "apps.receipts",
    "apps.recommendations",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "lunch_log.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "lunch_log.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DEFAULT_DB = str(os.path.join(BASE_DIR, "db.sqlite3"))

DATABASES = {
    "default": {
        "ENGINE": env("DATABASE_ENGINE", "django.db.backends.sqlite3"),
        "NAME": env("DATABASE_NAME", DEFAULT_DB),
        "USER": env("DATABASE_USER", "postgres"),
        "HOST": env("DATABASE_HOST", "localhost"),
        "PORT": env("DATABASE_PORT", 5432),
        "PASSWORD": env("DATABASE_PASSWORD", "postgres"),
    }
}


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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.AppUser"


# DRF settings
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

# OpenAPI/Swagger settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Lunch Log API",
    "DESCRIPTION": "Office Lunch Receipt Management and Recommendation System Backend",
    "VERSION": "1.0.0",
    # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
    },
    "SCHEMA_PATH_PREFIX": r"/api/",
    # Option for turning off error and warn messages
    "DISABLE_ERRORS_AND_WARNINGS": True,
    # include schema endpoint into schema
    "SERVE_INCLUDE_SCHEMA": False,
    # # CDNs for swagger and redoc. You can change the version or even host your
    # # own depending on your requirements. For self-hosting, have a look at
    # # the sidecar option in the README.
    # "SWAGGER_UI_DIST": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.3",
    # "SWAGGER_UI_FAVICON_HREF": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/favicon-32x32.png",
    # "REDOC_DIST": "https://cdn.jsdelivr.net/npm/redoc@latest",
    # Add djangorestframework-api-key annotation
    # https://github.com/tfranzel/drf-spectacular/blob/0.25.1/docs/blueprints.rst#djangorestframework-api-key
}
