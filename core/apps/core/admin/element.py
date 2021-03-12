from django.contrib import admin
from django.utils.translation import ugettext, ugettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from simple_history.admin import SimpleHistoryAdmin
from core.admin import LogAdminMixin, SaveOwnerModelMixin
from core.models import Image, Link, Note


class ImageAdmin(
    SaveOwnerModelMixin, LogAdminMixin, TranslationAdmin, SimpleHistoryAdmin
):
    list_display = (
        "title",
        "alt",
        "owner",
        "shooted_at",
        "license",
        "visibility",
        "changed_at",
    )
    list_filter = ("owner", "visibility", "changed_at")

    readonly_fields = ["id", "owner", "exif", "get_labeled_exif", "shooted_at"]

    fieldsets = [
        (None, {"fields": ("id",)}),
        (
            _("Base model"),
            {
                "fields": (
                    "title",
                    "short_description",
                    # "featured_image",
                    "license",
                    "tags",
                )
            },
        ),
        (_("Mandatory"), {"fields": ("picture", "alt", "visibility")}),
        (_("Optional"), {"fields": ("credit",)}),
        (_("Calculated"), {"fields": ("exif", "get_labeled_exif", "shooted_at")}),
    ]


admin.site.register(Image, ImageAdmin)


class LinkAdmin(SaveOwnerModelMixin, LogAdminMixin, SimpleHistoryAdmin):
    list_display = ("title", "url", "owner", "changed_at")
    list_filter = ("owner", "changed_at")

    readonly_fields = ["id", "owner"]

    fieldsets = [
        (None, {"fields": ("id",)}),
        (
            _("Base model"),
            {
                "fields": (
                    "title",
                    # "short_description",
                    # "featured_image",
                    # "license",
                    "tags",
                )
            },
        ),
        (_("Mandatory"), {"fields": ("url", "meta")}),
    ]


admin.site.register(Link, LinkAdmin)


class NoteAdmin(SaveOwnerModelMixin, LogAdminMixin, SimpleHistoryAdmin):
    list_display = ("title", "summary", "owner", "changed_at")
    list_filter = ("owner", "changed_at")

    readonly_fields = ["id", "owner"]

    fieldsets = [
        (None, {"fields": ("id",)}),
        (
            _("Base model"),
            {
                "fields": (
                    "title",
                    "short_description",
                    # "featured_image",
                    # "license",
                    "tags",
                )
            },
        ),
    ]


admin.site.register(Note, NoteAdmin)
