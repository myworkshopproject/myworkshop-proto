from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext, gettext_lazy as _
from .base import BaseModel


class Publication(BaseModel):
    # version < X.Y.Z >
    # thing -> Thing
    # thing_id
    # data < JSON >
    # type et/ou JSON Schema ...
    # publication_notes < Markdown >
    # published_at
    # is_published < bool >
    # lang
    # references < ArrayField (UUID) > (pour l'indexage)
    # tags < ArrayField > (*)
    # is_pinned < bool >
    # license
    # short_description (*)
    # featured_image (*)
    # title (*)
    # authors < ArrayField (UUID) >
    # (*) copie de « Thing » au moment de la publication

    class Meta:
        verbose_name = _("publication")
        verbose_name_plural = _("publications")
