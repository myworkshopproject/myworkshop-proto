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
    list_display = ("title", "is_public", "has_steps")
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
    list_display = ("title", "slug", "changed_at", "is_public", "type", "owner")
    list_filter = ("is_public", "type", "owner")
    readonly_fields = []
    fieldsets = [(_("Mandatory"), {"fields": ("type", "body")})]


admin.site.register(Publication, PublicationAdmin)
