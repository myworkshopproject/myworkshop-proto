"""
django.contrib.auth settings.
https://docs.djangoproject.com/fr/3.1/ref/settings/#auth
"""

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # Needed to login by username in Django admin, regardless of `allauth`
    "allauth.account.auth_backends.AuthenticationBackend",  # `allauth` specific authentication methods, such as login by e-mail
)
AUTH_USER_MODEL = "accounts.User"  # Default: "auth.User"
LOGIN_REDIRECT_URL = "core:home"  # Default: "/accounts/profile/"
# LOGIN_URL = "/accounts/login/"
LOGOUT_REDIRECT_URL = (
    "core:home"  # Default: None  # If None, the logout view will be rendered.
)
# PASSWORD_RESET_TIMEOUT = 259200  # 3 days
# PASSWORD_HASHERS = [
#     "django.contrib.auth.hashers.PBKDF2PasswordHasher",
#     "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
#     "django.contrib.auth.hashers.Argon2PasswordHasher",
#     "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
# ]
AUTH_PASSWORD_VALIDATORS = [  # Default: []
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
