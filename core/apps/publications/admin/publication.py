from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from publications.admin import BaseModelMixin
from publications.models import Publication


class PublicationAdmin(BaseModelMixin, SimpleHistoryAdmin):
    fields = (
        "source",
        "toc",
        "html",
    )

    readonly_fields = (
        "owner",
        "metadata",
        "toc",
        "html",
    )

    list_display = (
        "__str__",
        "title",
    )


admin.site.register(Publication, PublicationAdmin)
