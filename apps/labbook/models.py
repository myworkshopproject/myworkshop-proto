import os
from django.conf import settings
from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
from core.models import BaseModel


def entries_file_name(instance, filename):
    return "/".join(["entries", filename])


class Entry(BaseModel):
    # is_public ?
    # tags ? < ArrayField/CharField >
    # lang ?

    class Meta:
        verbose_name = _("entry")
        verbose_name_plural = _("entries")
        ordering = ["-updated_at"]


class Image(Entry):
    picture = models.ImageField(upload_to=entries_file_name, verbose_name=_("picture"))

    caption = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("caption")
    )

    # credit ?
    # license ?

    def __str__(self):
        return self.caption

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.picture.name))
        super(Image, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")


class Note(Entry):
    body = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("body"),
        help_text=_("You can use Markdown to write your contents."),
    )

    @property
    def summary(self):
        return self.body[:300] + "..."

    def __str__(self):
        return self.summary

    class Meta:
        verbose_name = _("note")
        verbose_name_plural = _("notes")


"""
class Alert(Entry):
    # type ?
    # message ?
    # title ?
    pass


class Snippet(Entry):
    # language ?
    # code ?
    # title ?
    pass


class Gallery(Entry):
    # title ?
    # images ? < MtoM (Images) >
    pass


class Link(Entry):
    # ?
    pass


class File(Entry):
    # ?
    pass
"""
