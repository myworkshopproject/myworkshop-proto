import uuid
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext, ugettext_lazy as _
from accounts.models import get_sentinel_user


class BaseModel(models.Model):

    # CHOICES

    CC_BY_4_0 = "CC BY 4.0"
    CC_BY_SA_4_0 = "CC BY-SA 4.0"
    CC_BY_ND_4_0 = "CC BY-ND 4.0"
    CC_BY_NC_4_0 = "CC BY-NC 4.0"
    CC_BY_NC_SA_4_0 = "CC BY-NC-SA 4.0"
    CC_BY_NC_ND_4_0 = "CC BY-NC-ND 4.0"
    CC0_1_0 = "CC0 1.0"
    MIT = "MIT"
    GNU_GPLV3 = "GNU GPLv3"
    GNU_AGPLV3 = "GNU AGPLv3"
    GNU_LGPLV3 = "GNU LGPLv3"
    CECILL_V2_1 = "CeCILL v2.1"
    CERN_OHL_S_V2 = "CERN-OHL-S v2"
    CERN_OHL_W_V2 = "CERN-OHL-W v2"
    CERN_OHL_P_V2 = "CERN-OHL-P v2"
    TAPR_OHL_V1_0 = "TAPR OHL v1.0"
    WTFPL = "WTFPL"

    LICENSE_ALL_CHOICES = [
        (CC_BY_4_0, _("Creative Commons Attribution 4.0 International (CC BY 4.0) ")),
        (
            CC_BY_SA_4_0,
            _(
                "Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)"
            ),
        ),
        (
            CC_BY_ND_4_0,
            _(
                "Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)"
            ),
        ),
        (
            CC_BY_NC_4_0,
            _(
                "Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)"
            ),
        ),
        (
            CC_BY_NC_SA_4_0,
            _(
                "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)"
            ),
        ),
        (
            CC_BY_NC_ND_4_0,
            _(
                "Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)"
            ),
        ),
        (CC0_1_0, _("Creative Commons CC0 1.0 Universal (CC0 1.0)")),
        (MIT, _("MIT License")),
        (GNU_GPLV3, _("GNU General Public License v3.0 (GNU GPLv3)")),
        (GNU_AGPLV3, _("GNU Affero General Public License v3.0 (GNU AGPLv3)")),
        (GNU_LGPLV3, _("GNU Lesser General Public License v3.0 (GNU LGPLv3)")),
        (CECILL_V2_1, _("Ce(a) C(nrs) I(nria) L(ogiciel) L(ibre) (CeCILL v2.1)")),
        (
            CERN_OHL_S_V2,
            _(
                "CERN Open Hardware Licence Version 2 - Strongly Reciprocal (CERN-OHL-S v2)"
            ),
        ),
        (
            CERN_OHL_W_V2,
            _(
                "CERN Open Hardware Licence Version 2 - Weakly Reciprocal (CERN-OHL-W v2)"
            ),
        ),
        (
            CERN_OHL_P_V2,
            _("CERN Open Hardware Licence Version 2 - Permissive (CERN-OHL-P v2)"),
        ),
        (TAPR_OHL_V1_0, _("TAPR Open Hardware License v1.0 (TAPR OHL v1.0)")),
        (WTFPL, _("Do What The Fuck You Want to Public License (WTFPL)")),
    ]

    # DATABASE FIELDS

    ## automatic fields

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    ## mandatory fields

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("creation date")
    )

    changed_at = models.DateTimeField(auto_now=True, verbose_name=_("update date"))

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET(
            get_sentinel_user
        ),  # if the related user is deleted, set the author to the "deleted" user!
        related_name="%(app_label)s_%(class)ss_as_owner",
        related_query_name="%(app_label)s_%(class)s_as_owner",
        verbose_name=_("owner"),
        help_text=_("The owner of this very object."),
        editable=False,
    )

    title = models.CharField(
        max_length=settings.MYWORKSHOP_TITLE_LENGHT,
        verbose_name=_("title"),
        default="untitled",
    )  # [i18n]

    # is_pinned

    # enable_comments

    ## optional fields

    short_description = models.TextField(
        blank=True,
        max_length=settings.MYWORKSHOP_SHORT_DESCRIPTION_LENGHT,  # It will be reflected in the Textarea widget of the auto-generated form field. However it is not enforced at the model or database level.
        verbose_name=_("short description"),
    )  # [i18n]

    featured_image = models.ForeignKey(
        "core.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,  # if the featured_image is deleted, do not delete the BaseModel!
        related_name="%(app_label)s_%(class)ss_as_featured_image",
        related_query_name="%(app_label)s_%(class)s_as_featured_image",
        verbose_name=_("featured image"),
    )

    license = models.CharField(
        blank=True,
        max_length=20,
        choices=LICENSE_ALL_CHOICES,
        default=None,
        verbose_name=_("open source license"),
        help_text=_(
            "How to <a href='https://choosealicense.com/'>Choose an open source license</a>?"
        ),
    )

    tags = ArrayField(
        models.CharField(max_length=settings.MYWORKSHOP_TAG_LENGHT),
        blank=True,
        default=list,
        verbose_name=_("tags"),
        help_text=_("Comma separated keywords."),
    )

    # MANAGERS

    # META CLASS
    class Meta:
        abstract = True
        ordering = ["-changed_at"]

    # TO STRING METHOD
    def __str__(self):
        return self.title if self.title else str(_("unknown"))

    # SAVE METHOD

    # ABSOLUTE URL METHOD

    # OTHER METHODS


class SlugModel(models.Model):
    # CHOICES

    # DATABASE FIELDS

    ## automatic fields

    slug = models.SlugField(
        # unique=True, # done manually with save()
        # editable=False,
        # null=True,
        blank=True,
        max_length=settings.MYWORKSHOP_SLUG_LENGHT,
        verbose_name=_("slug"),
        help_text=_("Warning! Changing the <em>slug</em> can affect external links!"),
    )

    ## mandatory fields

    ## optional fields

    # MANAGERS

    # META CLASS
    class Meta:
        abstract = True

    # TO STRING METHOD

    # SAVE METHOD
    def save(self, *args, **kwargs):
        # on s'assure que le slug est unique à chaque modification de l'objet

        """
        # s'il n'est pas renseigné, le slug est généré automatiquement à la création de l'objet
        if self._state.adding:
            slug = slugify(self.title)
        else:
            slug = self.slug
        """

        # s'il n'est pas renseigné, le slug est généré automatiquement à partir du titre
        if not self.slug:
            slug = slugify(self.title)
        else:
            slug = self.slug

        # n = SlugModel.objects.filter(slug=slug).exclude(id=self.id).count()
        n = type(self).objects.filter(slug=slug).exclude(id=self.id).count()
        if n != 0:
            i = 2
            while n != 0:
                test_slug = "{}-{}".format(slug, i)
                # n = SlugModel.objects.filter(slug=test_slug).exclude(id=self.id).count()
                n = (
                    type(self)
                    .objects.filter(slug=test_slug)
                    .exclude(id=self.id)
                    .count()
                )
                i += 1
            slug = test_slug
        self.slug = slug

        super(SlugModel, self).save(*args, **kwargs)
        # super().save(*args, **kwargs)

    # ABSOLUTE URL METHOD

    # OTHER METHODS


class LogModelMixin(object):
    """
    This mixin provides useful methods to interact with "django-simple-history".
    Needs to add "history = HistoricalRecords()" in the child class.
    """

    # OTHER METHODS

    @property
    def created_by(self):
        return self.history.earliest().history_user

    """
    @property
    def created_at(self):
        return self.history.earliest().history_date
    """

    @property
    def changed_by(self):
        return self.history.latest().history_user

    """
    @property
    def changed_at(self):
        return self.history.latest().history_date
    """
