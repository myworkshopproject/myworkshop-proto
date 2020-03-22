from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _
from model_utils.fields import MonitorField
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


class PublicPublicationManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(visibility=Publication.PUBLIC)
                & (Q(status=Publication.PUBLISH) | Q(status=Publication.ARCHIVE))
            )
        )


class MembersPublicationManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                (
                    Q(visibility=Publication.PUBLIC)
                    | Q(visibility=Publication.MEMBERS_ONLY)
                )
                & (Q(status=Publication.PUBLISH) | Q(status=Publication.ARCHIVE))
            )
        )


class Publication(LogModelMixin, SlugModel, BaseModel):

    # CHOICES

    DRAFT = "DR"
    PUBLISH = "PU"
    ARCHIVE = "AR"
    TRASH = "TR"

    STATUS_CHOICES = [
        (DRAFT, _("draft")),
        (PUBLISH, _("publish")),
        (ARCHIVE, _("archive")),
        (TRASH, _("trash")),
    ]

    PENDING = "PE"
    PUBLIC = "PU"
    MEMBERS_ONLY = "ME"
    BLOCKED = "BL"

    VISIBILITY_CHOICES = [
        (PENDING, _("pending")),
        (PUBLIC, _("public")),
        (MEMBERS_ONLY, _("members only")),
        (BLOCKED, _("blocked")),
    ]

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

    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default=DRAFT, verbose_name=_("status")
    )

    visibility = models.CharField(
        max_length=2,
        choices=VISIBILITY_CHOICES,
        default=PENDING,
        verbose_name=_("visibility"),
    )

    published_at = MonitorField(monitor="status", when=[PUBLISH])

    # version: ?

    ## optional fields

    # MANAGERS
    objects = models.Manager()  # The default manager.
    public_objects = PublicPublicationManager()
    members_objects = MembersPublicationManager()

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
    def is_awaiting_moderation(self):
        if self.status == self.PUBLISH and self.visibility == self.PENDING:
            return True
        else:
            return False

    is_awaiting_moderation.boolean = True

    def get_statuses(self):
        statuses = []
        if self.status == self.DRAFT:
            statuses.append({"name": "draft", "color": "warning"})

        if self.status == self.PUBLISH or self.status == self.ARCHIVE:
            if self.visibility == self.PENDING:
                statuses.append({"name": "pending", "color": "info"})
            if self.visibility == self.MEMBERS_ONLY:
                statuses.append({"name": "restricted", "color": "dark"})
            if self.visibility == self.PUBLIC:
                statuses.append({"name": "public", "color": "success"})

        if self.status == self.ARCHIVE:
            statuses.append({"name": "archived", "color": "secondary"})

        if self.status == self.TRASH:
            statuses.append({"name": "deleted", "color": "dark"})

        if self.visibility == self.BLOCKED:
            statuses.append({"name": "blocked", "color": "danger"})

        return statuses


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
