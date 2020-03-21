import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _
from core.models import BaseModel, LogModelMixin, SlugModel
from simple_history.models import HistoricalRecords


class ProjectType(LogModelMixin, SlugModel, BaseModel):

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
        default="fas fa-question",
        verbose_name=_("Font Awesome 5 class"),
        help_text=_(
            "Used for icons. See <a href='https://fontawesome.com/'>fontawesome.com</a>."
        ),
    )

    # has_forge: BooleanField
    # has_issues: BooleanField
    # has_forums: BooleanField

    ## optional fields

    # MANAGERS

    # META CLASS
    class Meta:
        verbose_name = _("project type")
        verbose_name_plural = _("project types")
        ordering = ["-changed_at"]

    # TO STRING METHOD
    def __str__(self):
        return self.title

    # SAVE METHOD
    def save(self, *args, **kwargs):
        # some stuff ...
        super(ProjectType, self).save(*args, **kwargs)

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        return reverse("core:project-list-by-type", kwargs={"type": self.slug})
        # return reverse("core:project-type-detail", kwargs={"pk": self.pk})

    # OTHER METHODS
    def get_create_url(self):
        return reverse("core:project-create", kwargs={"slug": self.slug})


class Project(LogModelMixin, SlugModel, BaseModel):

    # CHOICES

    # DATABASE FIELDS

    ## BaseModel fields replaced

    ## automatic fields

    # history = HistoricalRecords()  # done in translation.py

    ## mandatory fields

    type = models.ForeignKey(
        ProjectType,
        on_delete=models.PROTECT,  # to delete the type object, you need to delete all the related projects!
        related_name="%(app_label)s_%(class)ss_as_type",
        related_query_name="%(app_label)s_%(class)s_as_type",
        verbose_name=_("project type"),
        help_text=_("?"),
    )

    # is_published: BooleanField
    # is_pinned: BooleanField

    ## optional fields

    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ProjectContributor",
        through_fields=("project", "contributor"),
        related_name="projects",
        related_query_name="project",
        verbose_name=_("contributors"),
    )

    publications = models.ManyToManyField(
        "core.Publication",
        # on_delete=models.PROTECT,  # to delete the parent object, you need to delete all his children!
        related_name="projects",
        related_query_name="project",
        verbose_name=_("publications"),
        help_text=_("Related publications."),
    )

    # metadata ?
    # master_lang ?
    # tags ?
    # repo_github ?
    # liked_by ?
    # view_nb / seen_by ?
    # are_comments_allowed ?

    # MANAGERS

    # META CLASS
    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    # TO STRING METHOD
    def __str__(self):
        return self.title

    # SAVE METHOD
    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)
        if self._state.adding:
            project_contributor = ProjectContributor(
                project=self, contributor=self.owner, role=ProjectContributor.OWNER
            )
            project_contributor.save()

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        return reverse("core:project-detail", kwargs={"slug": self.slug})

    # OTHER METHODS
    def get_update_url(self):
        return reverse("core:project-update", kwargs={"slug": self.slug})

    def get_publications_update_url(self):
        return reverse("core:project-publications-update", kwargs={"slug": self.slug})

    def get_mades(self):
        return list()

    def get_related_projects(self):
        return list()

    def is_owner(self, user):
        if user.is_authenticated:
            try:
                project_contributor = ProjectContributor.objects.get(
                    project=self, contributor=user
                )
                if project_contributor.role == ProjectContributor.OWNER:
                    return True
            except:
                return False
        return False

    def is_owner_or_editor(self, user):
        if user.is_authenticated:
            try:
                project_contributor = ProjectContributor.objects.get(
                    project=self, contributor=user
                )
                if project_contributor.role in [
                    ProjectContributor.OWNER,
                    ProjectContributor.EDITOR,
                ]:
                    return True
            except:
                return False
        return False


class ProjectContributor(LogModelMixin, models.Model):

    # CHOICES

    OWNER = "OW"
    EDITOR = "ED"
    CONTRIBUTOR = "CO"

    ROLE_CHOICES = [
        (OWNER, _("Owner")),
        (EDITOR, _("Editor")),
        (CONTRIBUTOR, _("Contributor")),
    ]

    # DATABASE FIELDS

    ## BaseModel fields replaced

    ## automatic fields

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    history = HistoricalRecords()

    ## mandatory fields

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("creation date")
    )

    changed_at = models.DateTimeField(auto_now=True, verbose_name=_("update date"))

    project = models.ForeignKey(
        Project, on_delete=models.PROTECT, verbose_name=_("the related project")
    )

    contributor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_("the related contributor"),
        # limit_choices_to={"projectcontributor__project": self.project},
    )

    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default=CONTRIBUTOR)

    # can_edit: BooleanField
    # can_admin: BooleanField

    ## optional fields

    # function: CharField ? ( exemple : « Porteur de projet, Project Owner », « Rédacteur de la doc », etc. ) # [i18n]

    # MANAGERS

    # META CLASS
    class Meta:
        verbose_name = _("Project/Contributor relationship")
        verbose_name_plural = _("Project/Contributor relationships")
        constraints = [
            models.UniqueConstraint(
                fields=["project", "contributor"], name="unique_per_contributor"
            )
        ]
        ordering = ["created_at"]

    # TO STRING METHOD
    def __str__(self):
        return "{} - {}".format(self.project, self.contributor)

    # SAVE METHOD
    def save(self, *args, **kwargs):
        # some stuff ...
        super(ProjectContributor, self).save(*args, **kwargs)

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        return reverse("core:project-detail", kwargs={"slug": self.project.slug})

    # OTHER METHODS
    @property
    def title(self):
        return "role of “{}” in the project “{}”".format(self.contributor, self.project)

    def get_delete_url(self):
        return reverse(
            "core:project-contributor-delete",
            kwargs={"slug": self.project.slug, "pk": self.id},
        )

    def get_update_url(self):
        return reverse(
            "core:project-contributor-update",
            kwargs={"slug": self.project.slug, "pk": self.id},
        )
