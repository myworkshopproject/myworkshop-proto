import simple_history
from core.models import PublicationType, Publication
from modeltranslation.translator import translator, TranslationOptions


class PublicationTypeTranslationOptions(TranslationOptions):
    fields = ("title", "short_description")


translator.register(PublicationType, PublicationTypeTranslationOptions)
simple_history.register(PublicationType)


class PublicationTranslationOptions(TranslationOptions):
    fields = ("title", "short_description")


translator.register(Publication, PublicationTranslationOptions)
simple_history.register(Publication)
