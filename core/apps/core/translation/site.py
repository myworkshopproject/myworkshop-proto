import simple_history
from django.contrib.sites.models import Site
from modeltranslation.translator import translator, TranslationOptions
from core.models import SiteCustomization

simple_history.register(Site, app="core")


class SiteCustomizationTranslationOptions(TranslationOptions):
    fields = ("tagline", "description")


translator.register(SiteCustomization, SiteCustomizationTranslationOptions)
simple_history.register(SiteCustomization)
