import uuid
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from core.models import BaseModel, LogModelMixin
from datetime import datetime
from PIL.ExifTags import TAGS
from PIL import Image as PImage


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


def get_copyright(exif, default):
    if default:
        copyright = default
    else:
        copyright = ""

    if 33432 in exif:  # EXIF Copyright
        copyright = str(exif[33432])

    return copyright


def images_file_name(instance, filename):
    return "/".join(["images", str(uuid.uuid4()), filename])


class PublicImageManager(models.Manager):
    # todo: retourner les images utilisée dans une documentation ou un projet publiés
    def get_queryset(self):
        return super().get_queryset().none()


class MembersImageManager(models.Manager):
    # todo: retourner les images utilisée dans une documentation ou un projet réservés aux membres
    def get_queryset(self):
        return super().get_queryset()


class Image(LogModelMixin, BaseModel):

    # CHOICES

    PENDING = "PE"
    PUBLIC = "PU"
    BLOCKED = "BL"

    VISIBILITY_CHOICES = [
        (PENDING, _("pending")),
        (PUBLIC, _("public")),
        (BLOCKED, _("blocked")),
    ]

    # DATABASE FIELDS

    ## BaseModel fields replaced

    featured_image = None  # avoid self-referencing of this model

    ## automatic fields

    # history = HistoricalRecords()  # done in translation.py

    # mime

    exif = models.TextField(blank=True, verbose_name=_("EXIF"), editable=False)

    shooted_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("shooting_date"),
        # editable=False
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

    visibility = models.CharField(
        max_length=2,
        choices=VISIBILITY_CHOICES,
        default=PUBLIC,
        verbose_name=_("visibility"),
    )

    ## optional fields

    credit = models.CharField(
        max_length=settings.MYWORKSHOP_IMAGE_CREDIT_LENGHT,
        blank=True,
        verbose_name=_("credit"),
        help_text=_("Don't forget to credit the possible author of this image!"),
    )

    # MANAGERS
    objects = models.Manager()  # The default manager.
    public_objects = PublicImageManager()
    members_objects = MembersImageManager()

    # META CLASS
    class Meta(BaseModel.Meta):
        verbose_name = _("image")
        verbose_name_plural = _("images")
        ordering = ["-shooted_at"]

    # TO STRING METHOD
    def __str__(self):
        return self.title if self.title else str(_("untitled"))

    # SAVE METHOD
    def save(self, *args, **kwargs):
        if self._state.adding:
            exif = get_exif(self.picture)
            self.exif = str(exif)
            self.shooted_at = get_date_time_original(exif, self.created_at)
            self.credit = get_copyright(exif, self.credit)
        super(Image, self).save(*args, **kwargs)

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        return reverse("core:image-detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("core:image-update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        # return reverse("core:image-delete", kwargs={"slug": self.slug})
        return reverse("core:image-detail", kwargs={"pk": self.pk})

    # OTHER METHODS
    def get_create_url(self):
        return reverse("core:image-create")

    def get_labeled_exif(self):
        return get_labeled_exif(get_exif(self.picture))
