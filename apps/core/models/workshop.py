from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
from core.models import BaseModel, LogModelMixin
from core.utils import TwitterUsernameValidator


def workshop_file_name(instance, filename):
    return "/".join(["workshops", str(instance.site), filename])


def workshop_logo_file_name(instance, filename):
    ext = filename.split(".")[-1]
    return "/".join(["workshops", str(instance.site), "logo.{}".format(ext)])


class Workshop(LogModelMixin, BaseModel):

    # CHOICES

    # DATABASE FIELDS

    ## BaseModel fields replaced

    id = None  # the field "site" below is used as primary key
    owner = None  # no need to use this field in this model
    title = None  # no need to use this field in this model
    slug = None  # no need to use this field in this model
    featured_image = None  # no need to use this field in this model
    license = None  # no need to use this field in this model

    ## automatic fields

    # history = HistoricalRecords()  # done in translation.py

    ## mandatory fields

    site = models.OneToOneField(
        Site,
        on_delete=models.CASCADE,  # if Site is deleted, Workshop will also be deleted!
        primary_key=True,
        verbose_name=_("site"),
    )

    ## optional fields

    tagline = models.CharField(
        blank=True,
        max_length=settings.MYWORKSHOP_WORKSHOP_TAGLINE_LENGHT,
        verbose_name=_("tagline"),
        help_text="A short text that best describes your activity.",
    )  # [i18n]

    logo = models.ImageField(
        null=True, blank=True, upload_to=workshop_logo_file_name, verbose_name=_("logo")
    )

    footer = models.TextField(
        blank=True,
        max_length=settings.MYWORKSHOP_WORKSHOP_FOOTER_LENGHT,
        verbose_name=_("footer"),
    )  # [i18n]

    twitter_site_validator = TwitterUsernameValidator()

    twitter_site = models.CharField(
        blank=True,
        max_length=16,
        validators=[twitter_site_validator],
        verbose_name=_("Twitter's username"),
        help_text=_("@username for the website used in the card footer."),
    )

    facebook_app_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("Facebook app ID"),
        help_text=_(
            "In order to use Facebook Insights you must add the app ID to your page."  # Afin de pouvoir utiliser les Insights Facebook, vous devez ajouter l’ID d’app à votre page.
        ),
    )

    # MANAGERS

    # META CLASS
    class Meta(BaseModel.Meta):
        verbose_name = _("workshop")
        verbose_name_plural = _("workshops")

    # TO STRING METHOD
    def __str__(self):
        return self.site.name if self.site.name else str(_("unknown"))

    # SAVE METHOD
    def save(self, *args, **kwargs):
        super(Workshop, self).save(*args, **kwargs)

        # Clear cached content
        Site.objects.clear_cache()

    # ABSOLUTE URL METHOD

    # OTHER METHODS
