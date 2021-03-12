import simple_history
from modeltranslation.translator import translator, TranslationOptions
from flatpages.models import FlatPage


class FlatPageTranslationOptions(TranslationOptions):
    fields = ("title", "short_description", "body")


translator.register(FlatPage, FlatPageTranslationOptions)
simple_history.register(FlatPage)
