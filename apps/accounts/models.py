import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _
from core.utils import (
    UsernameValidator,
    FacebookUsernameValidator,
    GithubUsernameValidator,
    InstagramUsernameValidator,
    LinkedinPublicUrlValidator,
    TwitterUsernameValidator,
    YoutubeChannelUrlValidator,
)

# TO-DO:
# - trouver un moyen de mette à jour le profil depuis le provider à chaque login

# references:
# - https://github.com/pennersr/django-allauth/blob/master/allauth/account/models.py


def customuser_file_name(instance, filename):
    return "/".join(["users", str(instance.username), filename])


def customuser_photo_file_name(instance, filename):
    extension = filename.split(".")[-1]
    return "/".join(["users", str(instance.username), "photo.{}".format(extension)])


def get_sentinel_user():
    return CustomUser.objects.get_or_create(username="deleted")[0]


class CustomUser(AbstractUser):

    # CHOICES

    # DATABASE FIELDS

    ## BaseModel fields replaced

    ## automatic fields

    # history = HistoricalRecords()  # done in translation.py

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    ## mandatory fields

    username_validator = UsernameValidator()

    username = models.CharField(
        primary_key=True,
        unique=True,
        max_length=20,
        verbose_name=_("username"),
        help_text=_("Required. 20 characters or fewer. Letters, digits and _ only."),
        validators=[username_validator],
        error_messages={"unique": _("A user with that username already exists.")},
    )

    ## optional fields

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

    twitter_username_validator = TwitterUsernameValidator()

    twitter_username = models.CharField(
        max_length=16,
        blank=True,
        validators=[twitter_username_validator],
        verbose_name=_("Twitter's username"),
    )

    youtube_channel_url_validator = YoutubeChannelUrlValidator()

    youtube_channel_url = models.URLField(
        max_length=2048,
        blank=True,
        verbose_name=_("YouTube channel url"),
        validators=[youtube_channel_url_validator],
    )

    photo = models.ImageField(
        upload_to=customuser_photo_file_name,
        blank=True,
        null=True,
        verbose_name=_("profile picture"),
    )

    # gender ['male', 'female']

    # biography
    short_description = models.TextField(
        blank=True,
        max_length=settings.MYWORKSHOP_SHORT_DESCRIPTION_LENGHT,  # It will be reflected in the Textarea widget of the auto-generated form field. However it is not enforced at the model or database level.
        verbose_name=_("biography"),
        help_text=_("A short text to describe you."),
    )  # [i18n]

    tags = ArrayField(
        models.CharField(max_length=settings.MYWORKSHOP_TAG_LENGHT),
        blank=True,
        default=list,
        verbose_name=_("tags"),
        help_text=_(
            "Comma separated keywords to describe your hobbies, your skills, etc."
        ),
    )

    # MANAGERS

    # META CLASS
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["username"]

    # TO STRING METHOD
    def __str__(self):
        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name, self.last_name)
        else:
            return self.username

    # SAVE METHOD

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        return reverse("accounts:user-detail", kwargs={"pk": self.username})

    def get_update_url(self):
        return reverse("accounts:user-update", kwargs={"pk": self.username})

    def get_labbook_url(self):
        return reverse("accounts:user-labbook", kwargs={"pk": self.username})

    def get_projects_url(self):
        return reverse("accounts:user-project-list", kwargs={"pk": self.username})

    def get_images_url(self):
        return reverse("accounts:user-image-list", kwargs={"pk": self.username})

    def get_publications_url(self):
        return reverse("accounts:user-publication-list", kwargs={"pk": self.username})

    # OTHER METHODS
    def get_full_name(self):
        if self.first_name:
            if self.last_name:
                return "{} {}".format(self.first_name, self.last_name)
            else:
                return self.first_name
        return self.username

    def has_verified_emailaddress(self):
        if self.emailaddress_set.filter(verified=True):
            return True
        return False

    has_verified_emailaddress.boolean = True

    @property
    def title(self):
        return self.get_full_name()
