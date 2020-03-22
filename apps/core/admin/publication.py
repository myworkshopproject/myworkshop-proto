from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from simple_history.admin import SimpleHistoryAdmin
from core.admin import (
    BaseAdminMixin,
    LogAdminMixin,
    SaveOwnerModelMixin,
    SlugAdminMixin,
)
from core.models import PublicationType, Publication


class PublicationTypeAdmin(
    BaseAdminMixin,
    SaveOwnerModelMixin,
    LogAdminMixin,
    SlugAdminMixin,
    TranslationAdmin,
    SimpleHistoryAdmin,
):
    list_display = ("title", "has_steps")
    readonly_fields = []
    fieldsets = [
        (
            _("Mandatory"),
            {
                "fields": (
                    "bootstrap4_color",
                    "fontawesome5_class",
                    "meta_schema",
                    "has_steps",
                )
            },
        )
    ]


admin.site.register(PublicationType, PublicationTypeAdmin)


class PublicationAdmin(
    BaseAdminMixin,
    SaveOwnerModelMixin,
    LogAdminMixin,
    SlugAdminMixin,
    TranslationAdmin,
    SimpleHistoryAdmin,
):
    list_display = (
        "title",
        "slug",
        "changed_at",
        "type",
        "status",
        "visibility",
        "is_awaiting_moderation",
        "owner",
    )
    list_filter = ("type", "status", "visibility", "owner")
    readonly_fields = []
    fieldsets = [
        (
            _("Mandatory"),
            {"fields": ("type", "status", "visibility", "body", "published_at")},
        )
    ]


admin.site.register(Publication, PublicationAdmin)
