import simple_history
from django.contrib.auth.models import Group
from modeltranslation.translator import translator, TranslationOptions
from accounts.models import User

simple_history.register(Group, app="accounts")


class UserTranslationOptions(TranslationOptions):
    pass


translator.register(User, UserTranslationOptions)
simple_history.register(User, excluded_fields=["date_joined", "last_login", "password"])
