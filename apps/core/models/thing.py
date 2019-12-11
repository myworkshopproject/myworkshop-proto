from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext, gettext_lazy as _
from .base import BaseModel


class Thing(BaseModel):
    slug = models.SlugField(
        max_length=(255 + 5),
        help_text=_(
            _(
                "<strong>Warning!</strong> Change the <em>slug</em> can affect external links!"
            )
        ),
    )

    title = models.CharField(max_length=255, verbose_name=_("title"))

    makers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ThingMaker",
        through_fields=("thing", "maker"),
        related_name="things",
        related_query_name="thing",
        verbose_name=_("makers"),
    )

    short_description = models.CharField(
        max_length=255, verbose_name=_("short description"), blank=True
    )

    featured_image = models.ForeignKey(
        "labbook.Image",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="image_things",
        related_query_name="image_thing",
        verbose_name=_("featured image"),
    )

    # metadata ?
    # master_lang ?
    # tags ?
    # repo_github ?
    # liked_by ?
    # view_nb / seen_by ?
    # are_comments_allowed ?

    def __str__(self):
        return "{} ({})".format(self.title, self.slug)

    def save(self, *args, **kwargs):
        # le slug est généré automatiquement à la création de l'objet
        # on s'assure qu'il est unique à chaque modification
        if self._state.adding:
            slug = slugify(self.title)
        else:
            slug = self.slug

        n = Thing.objects.filter(slug=slug).exclude(id=self.id).count()
        if n != 0:
            i = 2
            while n != 0:
                test_slug = "{}-{}".format(slug, i)
                n = Thing.objects.filter(slug=test_slug).exclude(id=self.id).count()
                i += 1
            slug = test_slug
        self.slug = slug
        n = Thing.objects.filter(slug=slug).exclude(id=self.id).count()
        if n != 0:
            i = 2
            while n != 0:
                test_slug = "{}-{}".format(slug, i)
                n = Thing.objects.filter(slug=test_slug).exclude(id=self.id).count()
                i += 1
            slug = test_slug
        self.slug = slug

        super(Thing, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("thing")
        verbose_name_plural = _("things")


class ThingMaker(BaseModel):
    OWNER = "OW"
    EDITOR = "ED"
    CONTRIBUTOR = "CO"

    ROLE_CHOICES = [
        (OWNER, _("Owner")),
        (EDITOR, _("Editor")),
        (CONTRIBUTOR, _("Contributor")),
    ]

    thing = models.ForeignKey(
        Thing, on_delete=models.CASCADE, verbose_name=_("the related thing")
    )

    maker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("the related maker"),
    )

    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default=CONTRIBUTOR)

    # fonction ? ( exemple : « Porteur de projet, Project Owner », « Rédacteur de la doc », etc. )

    def __str__(self):
        return "{} - {}".format(self.thing, self.maker)

    class Meta:
        verbose_name = _("Thing/Maker relationship")
        verbose_name_plural = _("Thing/Maker relationships")
        constraints = [
            models.UniqueConstraint(fields=["thing", "maker"], name="unique_per_maker")
        ]
