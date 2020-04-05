from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _
from core.models import BaseModel, LogModelMixin
from core.utils import custom_url_parse


class Link(LogModelMixin, BaseModel):

    # CHOICES

    # DATABASE FIELDS

    ## BaseModel fields replaced

    # id -> OK
    # created_at -> OK
    # changed_at -> OK
    # owner -> OK
    # title -> OK
    short_description = None  # no need to use this field in this model
    featured_image = None  # no need to use this field in this model
    license = None  # no need to use this field in this model
    # tags -> OK

    ## automatic fields

    # history = HistoricalRecords()  # done in translation.py

    ## mandatory fields

    url = models.URLField(max_length=2048)

    meta = JSONField(default=dict)

    ## optional fields

    # MANAGERS

    # META CLASS
    class Meta(BaseModel.Meta):
        verbose_name = _("link")
        verbose_name_plural = _("links")
        ordering = ["-changed_at"]

    # TO STRING METHOD
    def __str__(self):
        return self.title

    # SAVE METHOD
    def save(self, *args, **kwargs):
        if self._state.adding:
            self.collect_meta()
            if self.meta["title"]:
                self.title = self.meta["title"]
            if self.meta["tags"]:
                self.tags = self.meta["tags"]
            if self.meta["url"]:
                self.url = self.meta["url"]
        super(Link, self).save(*args, **kwargs)

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        # return reverse("core:link-detail", kwargs={"pk": self.pk})
        return reverse("accounts:user-labbook", kwargs={"pk": self.owner.pk})

    def get_update_url(self):
        return reverse("core:link-update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        # return reverse("core:link-delete", kwargs={"slug": self.slug})
        return reverse("core:link-update", kwargs={"pk": self.pk})

    # OTHER METHODS
    def collect_meta(self):
        self.meta = custom_url_parse(self.url)
