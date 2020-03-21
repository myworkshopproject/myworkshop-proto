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
    list_display = ("title", "is_public")
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
    list_display = ("title", "slug", "changed_at", "is_public", "type", "owner")
    list_filter = ("is_public", "type", "owner")
    readonly_fields = []
    fieldsets = [(_("Mandatory"), {"fields": ("type",)})]

    inlines = [ProjectContributorInline]


admin.site.register(Project, ProjectAdmin)
