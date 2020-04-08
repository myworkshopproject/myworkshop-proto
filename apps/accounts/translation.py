import simple_history
from accounts.models import CustomUser
from modeltranslation.translator import translator, TranslationOptions


class CustomUserTranslationOptions(TranslationOptions):
    fields = ("short_description",)


translator.register(CustomUser, CustomUserTranslationOptions)
simple_history.register(CustomUser)
