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
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, "site_media", "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "site_media", "media")

# i18n
LANGUAGES = (("fr", _("French")), ("en", _("English")))
MODELTRANSLATION_FALLBACK_LANGUAGES = ("fr",)

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# My Workshop
MYWORKSHOP_TITLE_LENGHT = 200
MYWORKSHOP_SLUG_LENGHT = (
    MYWORKSHOP_TITLE_LENGHT + 6
)  # up to 10.000 different slugs based
MYWORKSHOP_SHORT_DESCRIPTION_LENGHT = 1000
MYWORKSHOP_TAG_LENGHT = 200
MYWORKSHOP_IMAGE_ALT_LENGHT = 500
MYWORKSHOP_IMAGE_CREDIT_LENGHT = 200
MYWORKSHOP_WORKSHOP_TAGLINE_LENGHT = 200
MYWORKSHOP_WORKSHOP_FOOTER_LENGHT = 1000
