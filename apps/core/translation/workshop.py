import simple_history
from core.models import Workshop
from django.contrib.sites.models import Site
from modeltranslation.translator import translator, TranslationOptions

simple_history.register(Site)


class WorkshopTranslationOptions(TranslationOptions):
    fields = ("short_description", "tagline", "footer")


translator.register(Workshop, WorkshopTranslationOptions)
simple_history.register(Workshop)
