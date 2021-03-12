"""
Django base settings.
"""

import os
import sys
from django.utils.translation import ugettext_lazy as _
from pathlib import Path
from .allauth import *
from .auth import *

# Paths
BASE_DIR = Path(__file__).resolve().parents[2]
APPS_DIR = BASE_DIR / "apps"
sys.path.append(str(APPS_DIR))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.environ["SECRET_KEY"])

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str(os.environ["DEBUG"]) == "True"
MESSAGE_LEVEL = 10  # DEBUG

# Allowed hosts
ALLOWED_HOSTS = str(os.environ["ALLOWED_HOSTS"]).split(" ")

# Installed applications
INSTALLED_APPS = [
    "django.contrib.sites",  # before "accounts" to override SiteAdmin  # `allauth` needs this from django
    "accounts.apps.AccountsConfig",  # before "django.contrib.auth" to override templates
    "modeltranslation",  # before "django.contrib.admin" to use the admin integration
    "django.contrib.admin",
    "django.contrib.auth",  # `allauth` needs this from django
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",  # `allauth` needs this from django
    "django.contrib.staticfiles",
    "allauth",  # <- django-allauth
    "allauth.account",  # <- django-allauth
    "allauth.socialaccount",  # <- django-allauth
    "allauth.socialaccount.providers.github",
    # "allauth.socialaccount.providers.twitter",
    # "allauth.socialaccount.providers.openid",
    "core.apps.CoreConfig",
    "webpack_loader",
    "simple_history",
    "widget_tweaks",
    "django_celery_results",
]

# Middewares
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # after "SessionMiddleware" and "CacheMiddleware" ; before "CommonMiddleware"
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

# Root urls
ROOT_URLCONF = "myapp.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # `allauth` needs this from django
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

# WSGI application
WSGI_APPLICATION = "myapp.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": str(os.environ["POSTGRES_DB"]),
        "USER": str(os.environ["POSTGRES_USER"]),
        "PASSWORD": str(os.environ["POSTGRES_PASSWORD"]),
        "HOST": str(os.environ["POSTGRES_HOST"]),
        "PORT": 5432,
    }
}

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

# i18n
LANGUAGE_CODE = "en"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = (
    ("fr", _("French")),
    ("en", _("English")),
)
MODELTRANSLATION_FALLBACK_LANGUAGES = ("fr",)

# Time zone
TIME_ZONE = "UTC"
# TIME_ZONE = "Europe/Paris"


## Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
# STATICFILES_DIRS = [str(BASE_DIR / "dist")]

# django-webpack-loader
WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "dist/",  # must end with slash
        "STATS_FILE": BASE_DIR / "webpack-stats.json",
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": None,
        # "IGNORE": [r".+\.hot-update.js", r".+\.map"],
        "LOADER_CLASS": "webpack_loader.loader.WebpackLoader",
    }
}

## Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "webmaster@example.com"

# django-simple-history
# SIMPLE_HISTORY_HISTORY_CHANGE_REASON_USE_TEXT_FIELD = False
SIMPLE_HISTORY_HISTORY_ID_USE_UUID = True  # Default: False
SIMPLE_HISTORY_FILEFIELD_TO_CHARFIELD = True  # Default: False
# SIMPLE_HISTORY_REVERT_DISABLED = False

# Core App
CORE_DEFAULT_SITE_NAME = str(os.environ["SITE_NAME"])
CORE_SITECUSTOMIZATION_TAGLINE_LENGHT = 255
CORE_SITECUSTOMIZATION_DESCRIPTION_LENGHT = 2048
CORE_MIN_TAG_LENGHT = 3
CORE_MAX_TAG_LENGHT = 127
FONTAWESOME_SITE_ICON = str(os.environ["FONTAWESOME_SITE_ICON"])
GITHUB_REPO_NAME = str(os.environ["GITHUB_REPO_NAME"])
GITHUB_REPO_URL = str(os.environ["GITHUB_REPO_URL"])
GITHUB_TEAM_NAME = str(os.environ["GITHUB_TEAM_NAME"])
GITHUB_TEAM_URL = str(os.environ["GITHUB_TEAM_URL"])
GITHUB_CONTRIB_URL = str(os.environ["GITHUB_CONTRIB_URL"])
LICENSE_NAME = str(os.environ["LICENSE_NAME"])
LICENSE_URL = str(os.environ["LICENSE_URL"])

# Celery Configuration Options
CELERY_BROKER_URL = "amqp://{host}:5672/{vhost}".format(
    host=str(os.environ["RABBITMQ_HOST"]),
    vhost=str(os.environ["RABBITMQ_VHOST"]),
)
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# Configure Celery to use the django-celery-results backend:
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"
