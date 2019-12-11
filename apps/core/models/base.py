import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext, gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("creation date")
    )

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("update date"))

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
        verbose_name=_("created by"),
        help_text=_("the creator of this object"),
        blank=True,
        null=True,
        editable=False,
    )

    # updated_by ?

    class Meta:
        abstract = True
