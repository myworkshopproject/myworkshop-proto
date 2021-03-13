from random import choice
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from simple_history.models import HistoricalRecords
from publications.models import BaseModel


class Publication(BaseModel):
    history = HistoricalRecords()

    id = models.CharField(
        primary_key=True, max_length=settings.PUBLICATIONSAPP_ID_LENGHT, editable=False
    )

    @property
    def title(self):
        """For debug purpose only!
        Will be replaced by an extracted value from the Markdown source field...
        """
        return _("untitled")

    @property
    def description(self):
        """For debug purpose only!
        Will be replaced by an extracted value from the Markdown source field...
        """
        return _("No description.")

    class Meta(BaseModel.Meta):
        verbose_name = _("publication")
        verbose_name_plural = _("publications")

    def get_absolute_url(self):
        return reverse("publications:publication-detail", args=[str(self.id)])

    def save(self, *args, **kwargs):
        ALL_EXCLUDE_SIMILAR = (
            "23456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"  # 57
        )
        LETTERS_EXCLUDE_SIMILAR = (
            "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"  # 49
        )

        if not self.id:
            is_unique = False
            while not is_unique:
                id = "".join(
                    [choice(LETTERS_EXCLUDE_SIMILAR)]
                    + [
                        choice(ALL_EXCLUDE_SIMILAR)
                        for i in range(settings.PUBLICATIONSAPP_ID_LENGHT - 1)
                    ]
                )
                is_unique = not Publication.objects.filter(id=id).exists()
            self.id = id

        super(Publication, self).save(*args, **kwargs)
