from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from core.models import BaseModel, LogModelMixin


class Note(LogModelMixin, BaseModel):

    # CHOICES

    # DATABASE FIELDS

    ## BaseModel fields replaced

    # id -> OK
    # created_at -> OK
    # changed_at -> OK
    # owner -> OK
    # title -> OK
    # short_description -> OK
    featured_image = None  # no need to use this field in this model
    license = None  # no need to use this field in this model
    # tags -> OK

    ## automatic fields

    # history = HistoricalRecords()  # done in translation.py

    ## mandatory fields

    ## optional fields

    # MANAGERS

    # META CLASS
    class Meta(BaseModel.Meta):
        verbose_name = _("note")
        verbose_name_plural = _("notes")
        ordering = ["-changed_at"]

    # TO STRING METHOD
    def __str__(self):
        return self.title if self.title else str(_("untitled"))

    # SAVE METHOD
    def save(self, *args, **kwargs):
        super(Note, self).save(*args, **kwargs)

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        # return reverse("core:note-detail", kwargs={"pk": self.pk})
        return reverse("accounts:user-labbook", kwargs={"pk": self.owner.pk})

    def get_update_url(self):
        return reverse("core:note-update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        # return reverse("core:note-delete", kwargs={"slug": self.slug})
        return reverse("core:note-update", kwargs={"pk": self.pk})

    # OTHER METHODS
    def summary(self):
        if len(self.short_description) > 100:
            return self.short_description[:100] + "..."
        elif not self.short_description:
            return str(_("void"))
        else:
            return self.short_description
