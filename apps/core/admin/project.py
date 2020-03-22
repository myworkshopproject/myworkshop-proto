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
from core.models import ProjectType, Project, ProjectContributor


class ProjectContributorInline(admin.TabularInline):
    model = ProjectContributor
    extra = 0


class ProjectTypeAdmin(
    BaseAdminMixin,
    SaveOwnerModelMixin,
    LogAdminMixin,
    SlugAdminMixin,
    TranslationAdmin,
    SimpleHistoryAdmin,
):
    list_display = ("title",)
    readonly_fields = []
    fieldsets = [
        (_("Mandatory"), {"fields": ("bootstrap4_color", "fontawesome5_class")})
    ]


admin.site.register(ProjectType, ProjectTypeAdmin)


class ProjectAdmin(
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
    fieldsets = [(_("Mandatory"), {"fields": ("type", "status", "visibility")})]

    inlines = [ProjectContributorInline]


admin.site.register(Project, ProjectAdmin)
