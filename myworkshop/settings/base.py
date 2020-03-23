"""
Django base settings for myworkshop project.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APPS_DIR = os.path.abspath(os.path.join(BASE_DIR, "apps"))
sys.path.append(APPS_DIR)

INSTALLED_APPS = [
    "django.contrib.sites",  # before "accounts" to override SiteAdmin
    "accounts.apps.AccountsConfig",  # before "django.contrib.auth" to override templates
    "modeltranslation",  # before "django.contrib.admin" to use the admin integration
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "allauth",  # <- django-allauth
    "allauth.account",  # <- django-allauth
    "allauth.socialaccount",  # <- django-allauth
    # "allauth.socialaccount.providers.facebook",
    # "allauth.socialaccount.providers.github",
    # "allauth.socialaccount.providers.google",
    # "allauth.socialaccount.providers.twitter",
    # "allauth.socialaccount.providers.linkedin",
    "core.apps.CoreConfig",
    "flatpages.apps.FlatpagesConfig",
    "crispy_forms",
    "simple_history",
    "mptt",
]

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

ROOT_URLCONF = "myworkshop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"environment": "myworkshop.jinja2.environment"},
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # `allauth` needs this from django
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ]
        },
    },
]

WSGI_APPLICATION = "myworkshop.wsgi.application"


# Auth (django.contrib.auth)
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # Needed to login by username in Django admin, regardless of `allauth`
    "allauth.account.auth_backends.AuthenticationBackend",  # `allauth` specific authentication methods, such as login by e-mail
)
AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_REDIRECT_URL = "core:home"  # Default: '/accounts/profile/'
LOGIN_URL = "account_login"  # Default: '/accounts/login/'
LOGOUT_REDIRECT_URL = "core:home"  # If None, the logout view will be rendered.
PASSWORD_RESET_TIMEOUT_DAYS = 3  # days
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# django-allauth
ACCOUNT_ADAPTER = "accounts.adapter.CustomUserAccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_FORMS = {
    "login": "accounts.forms.CustomLoginForm",
    "signup": "accounts.forms.CustomSignupForm",
}
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400  # 1 day in seconds
ACCOUNT_LOGOUT_REDIRECT_URL = "core:home"
ACCOUNT_USERNAME_MIN_LENGTH = 8

# i18n
LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = "/site_media/static/"
MEDIA_URL = "/site_media/media/"

# crispy_forms
CRISPY_TEMPLATE_PACK = "bootstrap4"
