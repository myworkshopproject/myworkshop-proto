import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _
from core.models import BaseModel, LogModelMixin

import json
from PIL.ExifTags import TAGS
from PIL import Image as PImage
from datetime import datetime


def get_exif(obj):
    i = PImage.open(obj)
    exif = {}
    try:
        exif = i._getexif()
    except:
        exif = None

    if exif == None:
        exif = {}

    return exif


def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val

    return labeled


def get_date_time_original(exif, default):
    if default:
        date_time_original = default
    else:
        date_time_original = datetime.now()

    if 36867 in exif:  # EXIF DateTimeOriginal
        try:
            date_time_original = datetime.strptime(exif[36867], "%Y:%m:%d %H:%M:%S")
        except:
            pass

    return date_time_original


def images_file_name(instance, filename):
    return "/".join(["images", str(uuid.uuid4()), filename])


class Image(LogModelMixin, BaseModel):

    # CHOICES

    # DATABASE FIELDS

    ## BaseModel fields replaced

    # title = None  # no need to use this field in this model
    featured_image = None  # avoid self-referencing of this model

    ## automatic fields

    # history = HistoricalRecords()  # done in translation.py

    # mime

    exif = models.TextField(blank=True, verbose_name=_("EXIF"), editable=False)

    shooted_at = models.DateTimeField(
        blank=True, null=True, verbose_name=_("shooting_date"), editable=False
    )

    ## mandatory fields

    picture = models.ImageField(upload_to=images_file_name, verbose_name=_("picture"))

    alt = models.CharField(
        max_length=settings.MYWORKSHOP_IMAGE_ALT_LENGHT,
        verbose_name=_("alternative text"),
        help_text=_(
            "The main purpose of the alternate text is to improve accessibility by enabling screen readers to read it out for visually impaired users."
        ),
    )  # [i18n]

    ## optional fields

    credit = models.CharField(
        max_length=settings.MYWORKSHOP_IMAGE_CREDIT_LENGHT,
        blank=True,
        verbose_name=_("credit"),
        help_text=_("Don't forget to credit the possible author of this image!"),
    )

    # MANAGERS

    # META CLASS
    class Meta(BaseModel.Meta):
        verbose_name = _("image")
        verbose_name_plural = _("images")
        ordering = ["-shooted_at"]

    # TO STRING METHOD
    def __str__(self):
        return self.title

    # SAVE METHOD
    def save(self, *args, **kwargs):
        exif = get_exif(self.picture)
        self.exif = str(exif)
        self.shooted_at = get_date_time_original(exif, self.created_at)
        super(Image, self).save(*args, **kwargs)

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        return reverse("core:image-detail", kwargs={"pk": self.pk})

    # OTHER METHODS
    def get_labeled_exif(self):
        # return get_labeled_exif(self.exif)
        return get_labeled_exif(get_exif(self.picture))


"""
class Note(LogModelMixin, BaseModel):

    # CHOICES

    # DATABASE FIELDS

    ## BaseModel fields replaced

    # id -> OK
    # created_at -> OK
    # changed_at -> OK
    # owner -> OK
    # title = None  # no need to use this field in this model
    # is_public -> OK
    # short_description -> ???
    # featured_image = None  # no need to use this field in this model
    # license = None  # no need to use this field in this model
    # tags -> ???

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
        return self.title

    # SAVE METHOD
    def save(self, *args, **kwargs):
        super(Note, self).save(*args, **kwargs)

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        return reverse("core:image-detail", kwargs={"pk": self.pk})

    # OTHER METHODS
"""

"""
class Link(LogModelMixin, Entry):
    history = HistoricalRecords()

    # uri

    class Meta:
        verbose_name = _("link")
        verbose_name_plural = _("links")
"""

"""
class Note(LogModelMixin, Entry, LangModelMixin):
    HTML = "HTML"
    MARKDOWN = "MD"
    PLAIN_TEXT = "TXT"
    RST = "RST"
    WIKITEXT = "WIKITEXT"

    FORMAT_CHOICES = [
        (HTML, _("HyperText Markup Language")),
        (MARKDOWN, _("Markdown")),
        (PLAIN_TEXT, _("plain text")),
        (RST, _("reStructuredText")),
        (WIKITEXT, _("Wikitext")),
    ]

    history = HistoricalRecords()

    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default=MARKDOWN)

    body = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("body"),
        help_text=_("You can use a markup language to write your contents."),
    )

    @property
    def summary(self):
        if len(self.body) > 100:
            return self.body[:100] + "..."
        elif not self.body:
            return str(_("unknown"))
        else:
            return self.body

    def __str__(self):
        return self.summary

    class Meta:
        verbose_name = _("note")
        verbose_name_plural = _("notes")
"""
