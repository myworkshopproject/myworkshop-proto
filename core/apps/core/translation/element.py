import simple_history
from core.models import Image, Link, Note
from modeltranslation.translator import translator, TranslationOptions


class ImageTranslationOptions(TranslationOptions):
    fields = ("title", "short_description", "alt")


translator.register(Image, ImageTranslationOptions)
simple_history.register(Image)

simple_history.register(Link)

simple_history.register(Note)
