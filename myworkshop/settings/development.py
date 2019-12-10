"""
Django development settings for myworkshop project.
"""

from .base import *
from django.utils.translation import ugettext_lazy as _

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "-p8*re#k&^_g$s)j(dssim+nxe!yx_o51o6ik_2y*t-k4jpu0o"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, "site_media", "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "site_media", "media")

# i18n
LANGUAGES = (("en", _("English")), ("fr", _("French")))

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Django OAuth Toolkit
OAUTH_SERVER_BASEURL = "http://127.0.0.1:8001"
