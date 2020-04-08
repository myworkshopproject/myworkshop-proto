from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
from core.models import BaseModel, LogModelMixin
from core.utils import (
    UsernameValidator,
    FacebookUsernameValidator,
    GithubUsernameValidator,
    InstagramUsernameValidator,
    LinkedinPublicUrlValidator,
    TwitterUsernameValidator,
    YoutubeChannelUrlValidator,
)


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

    is_open_for_signup = models.BooleanField(default=True)

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

    facebook_app_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("Facebook app ID"),
        help_text=_(
            "In order to use Facebook Insights you must add the app ID to your page."  # Afin de pouvoir utiliser les Insights Facebook, vous devez ajouter l’ID d’app à votre page.
        ),
    )

    facebook_username_validator = FacebookUsernameValidator()

    facebook_username = models.CharField(
        max_length=255,
        blank=True,
        validators=[facebook_username_validator],
        verbose_name=_("Facebook's username"),
    )

    github_username_validator = GithubUsernameValidator()

    github_username = models.CharField(
        max_length=40,
        blank=True,
        validators=[github_username_validator],
        verbose_name=_("GitHub's username"),
    )

    instagram_username_validator = InstagramUsernameValidator()

    instagram_username = models.CharField(
        max_length=255,
        blank=True,
        validators=[instagram_username_validator],
        verbose_name=_("Instagram's username"),
    )

    linkedin_public_url_validator = LinkedinPublicUrlValidator()

    linkedin_public_url = models.URLField(
        max_length=2048,
        blank=True,
        verbose_name=_("LinkedIn public profile url"),
        validators=[linkedin_public_url_validator],
    )

    twitter_site_validator = TwitterUsernameValidator()

    twitter_site = models.CharField(
        blank=True,
        max_length=16,
        validators=[twitter_site_validator],
        verbose_name=_("Twitter's username"),
        help_text=_("@username for the website used in the card footer."),
    )

    youtube_channel_url_validator = YoutubeChannelUrlValidator()

    youtube_channel_url = models.URLField(
        max_length=2048,
        blank=True,
        verbose_name=_("YouTube channel url"),
        validators=[youtube_channel_url_validator],
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
