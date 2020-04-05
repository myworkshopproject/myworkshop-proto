import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _
from core.utils import UsernameValidator, TwitterUsernameValidator

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

    twitter_username_validator = TwitterUsernameValidator()

    twitter_username = models.CharField(
        max_length=16,
        blank=True,
        validators=[twitter_username_validator],
        verbose_name=_("Twitter's username"),
    )

    photo = models.ImageField(
        upload_to=customuser_photo_file_name,
        blank=True,
        null=True,
        verbose_name=_("profile picture"),
    )

    # gender ['male', 'female']

    # biography

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
