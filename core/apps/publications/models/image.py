import os
import shutil
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from simple_history.models import HistoricalRecords
from publications.models import Publication


class OverwriteStorage(FileSystemStorage):
    """
    Update get_available_name to remove any previously stored file (if any)
    before returning the name.
    """

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def image_path(instance, filename):
    root, ext = os.path.splitext(filename)
    new_filename = "image{}".format(ext)
    return os.path.join(instance.get_storage_relative_path(), new_filename)


class Image(Publication):
    history = HistoricalRecords()

    picture = models.ImageField(
        upload_to=image_path,
        storage=OverwriteStorage(),
        verbose_name=_("picture"),
    )

    @property
    def icon(self):
        return settings.PUBLICATIONS_IMAGE_ICON

    @property
    def featured_image(self):
        return self

    @property
    def alt(self):
        return self.description

    @property
    def caption(self):
        return self.description

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")

    def get_update_url(self):
        return reverse("publications:image-update", args=[str(self.id)])

    def get_storage_relative_path(self):
        return os.path.join("images", str(self.id))

    def get_storage_absolute_path(self):
        return os.path.join(settings.MEDIA_ROOT, self.get_storage_relative_path())


@receiver(post_delete, sender=Image)
def storage_delete(sender, instance, **kwargs):
    """
    When deleting a Image object, deletes all the files linked to this object.
    """
    shutil.rmtree(
        instance.get_storage_absolute_path(),
        ignore_errors=True,
        onerror=None,
    )
