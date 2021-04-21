from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from publications.models import Image


class SiteCustomization(models.Model):
    # history = HistoricalRecords()  # done in translation.py

    site = models.OneToOneField(
        Site,
        on_delete=models.CASCADE,  # if Site is deleted, SiteCustomization will also be deleted!
        primary_key=True,
        verbose_name=_("site"),
    )

    is_open_for_signup = models.BooleanField(
        default=True, verbose_name=_("is open for signup")
    )

    tagline = models.CharField(  # [i18n]
        blank=True,
        max_length=settings.CORE_SITECUSTOMIZATION_TAGLINE_LENGHT,
        verbose_name=_("tagline"),
        help_text=_("A few words to describe this very website."),
        default="A few words to describe this very website.",
    )

    description = models.TextField(  # [i18n]
        blank=True,
        max_length=settings.CORE_SITECUSTOMIZATION_DESCRIPTION_LENGHT,
        verbose_name=_("description"),
        help_text=_("A short text to describe this very website."),
        default=_("A short text to describe this very website."),
    )

    image = models.ForeignKey(
        Image,
        blank=True,
        null=True,
        verbose_name=_("featured image"),
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = _("site customization")
        verbose_name_plural = _("site customizations")
        ordering = ["site"]

    def __str__(self):
        return self.site.name if self.site.name else str(_("unknown"))

    def save(self, *args, **kwargs):
        super(SiteCustomization, self).save(*args, **kwargs)

        # Clear cached content
        Site.objects.clear_cache()

    @property
    def github_repo_name(self):
        return settings.GITHUB_REPO_NAME

    @property
    def github_repo_url(self):
        return settings.GITHUB_REPO_URL

    @property
    def github_team_name(self):
        return settings.GITHUB_TEAM_NAME

    @property
    def github_team_url(self):
        return settings.GITHUB_TEAM_URL

    @property
    def github_contributors_url(self):
        return settings.GITHUB_CONTRIB_URL

    @property
    def license_name(self):
        return settings.LICENSE_NAME

    @property
    def license_url(self):
        return settings.LICENSE_URL

    @property
    def fontawesome_site_icon(self):
        return settings.FONTAWESOME_SITE_ICON
