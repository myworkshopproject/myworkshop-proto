from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _
from core.models import BaseModel, LogModelMixin, SlugModel


class PublicationType(LogModelMixin, SlugModel, BaseModel):

    # CHOICES

    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    DANGER = "danger"
    WARNING = "warning"
    INFO = "info"
    LIGHT = "light"
    DARK = "dark"
    WHITE = "white"

    BOOTSTRAP4_COLOR_CHOICES = [
        (PRIMARY, "primary"),
        (SECONDARY, "secondary"),
        (SUCCESS, "success"),
        (DANGER, "danger"),
        (WARNING, "warning"),
        (INFO, "info"),
        (LIGHT, "light"),
        (DARK, "dark"),
        (WHITE, "white"),
    ]

    # DATABASE FIELDS

    ## BaseModel fields replaced

    ## automatic fields

    # history = HistoricalRecords()  # done in translation.py

    ## mandatory fields

    bootstrap4_color = models.CharField(
        max_length=10,
        choices=BOOTSTRAP4_COLOR_CHOICES,
        default=PRIMARY,
        verbose_name=_("Bootstrap4 color"),
        help_text=_(
            "Used for color of icons. See: <a href='https://getbootstrap.com/docs/4.4/utilities/colors/'>getbootstrap.com</a>?"
        ),
    )

    fontawesome5_class = models.CharField(
        max_length=100,
        default="fas fa-feather-alt",
        verbose_name=_("Font Awesome 5 class"),
        help_text=_(
            "Used for icons. See <a href='https://fontawesome.com/'>fontawesome.com</a>."
        ),
    )

    meta_schema = JSONField(default=dict)

    # body_schema = JSONField(default=dict)  # [i18n]

    # has_prerequities: BooleanField
    # has_numbered_steps: BooleanField

    has_steps = models.BooleanField(
        default=True, verbose_name=_("has this publication steps?")
    )

    # has_components: BooleanField
    # has_mades: BooleanField
    # are_comments_allowed: BooleanField
    # is_component_sheet: BooleanField

    ## optional fields

    # MANAGERS

    # META CLASS
    class Meta:
        verbose_name = _("publication type")
        verbose_name_plural = _("publication types")

    # TO STRING METHOD
    def __str__(self):
        return self.title

    # SAVE METHOD
    def save(self, *args, **kwargs):
        # some stuff ...
        super(PublicationType, self).save(*args, **kwargs)

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        return reverse("core:publication-list-by-type", kwargs={"type": self.slug})
        # return reverse("core:publication-type-detail", kwargs={"pk": self.pk})

    # OTHER METHODS
    def get_create_url(self):
        return reverse("core:publication-create", kwargs={"slug": self.slug})


class Publication(LogModelMixin, SlugModel, BaseModel):

    # CHOICES

    # DATABASE FIELDS

    ## BaseModel fields replaced

    ## automatic fields

    # history = HistoricalRecords()  # done in translation.py

    ## mandatory fields

    type = models.ForeignKey(
        PublicationType,
        on_delete=models.PROTECT,  # to delete the type object, you need to delete all the related publications!
        related_name="%(app_label)s_%(class)ss_as_type",
        related_query_name="%(app_label)s_%(class)s_as_type",
        verbose_name=_("publication type"),
        help_text=_("?"),
    )

    meta = JSONField(default=dict)

    body = JSONField(default=dict)

    # is_published: BooleanField
    # published_at: MonitorField(monitor="is_published",when=[True])
    # version: ?

    ## optional fields

    # MANAGERS

    # META CLASS
    class Meta:
        verbose_name = _("publication")
        verbose_name_plural = _("publications")
        ordering = ["-changed_at"]

    # TO STRING METHOD
    def __str__(self):
        return self.title

    # SAVE METHOD
    def save(self, *args, **kwargs):
        # some stuff ...
        super(Publication, self).save(*args, **kwargs)

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        return reverse("core:publication-detail", kwargs={"slug": self.slug})
        # return reverse("core:publication-detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("core:publication-update", kwargs={"slug": self.slug})

    def get_update_body_url(self):
        return reverse("core:publication-update-body", kwargs={"slug": self.slug})

    # OTHER METHODS


"""

class Publication(LogModelMixin, BaseModel):
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



license = models.ForeignKey(
    "core.License",
    null=True,
    blank=True,
    on_delete=models.SET_NULL,  # if the license is deleted, do not delete the BaseModel!
    related_name="%(app_label)s_%(class)ss_as_license",
    related_query_name="%(app_label)s_%(class)s_as_license",
    verbose_name=_("open source license"),
    help_text=_(
        "How to <a href='https://choosealicense.com/'>Choose an open source license</a>?"
    ),
)
"""
