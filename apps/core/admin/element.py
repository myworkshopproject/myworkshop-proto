from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from simple_history.admin import SimpleHistoryAdmin
from core.admin import LogAdminMixin, SaveOwnerModelMixin
from core.models import Image


class ImageAdmin(
    SaveOwnerModelMixin, LogAdminMixin, TranslationAdmin, SimpleHistoryAdmin
):
    list_display = ("title", "alt", "owner", "is_public", "shooted_at", "license")
    list_filter = ("is_public", "owner")

    readonly_fields = ["id", "owner", "exif", "get_labeled_exif", "shooted_at"]

    fieldsets = [
        (None, {"fields": ("id",)}),
        (
            _("Base model"),
            {
                "fields": (
                    "title",
                    "is_public",
                    "short_description",
                    # "featured_image",
                    "license",
                    "tags",
                )
            },
        ),
        (_("Mandatory"), {"fields": ("picture", "alt")}),
        (_("Optional"), {"fields": ("credit",)}),
        (_("Calculated"), {"fields": ("exif", "get_labeled_exif", "shooted_at")}),
    ]


admin.site.register(Image, ImageAdmin)
