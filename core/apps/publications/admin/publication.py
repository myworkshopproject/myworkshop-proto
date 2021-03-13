from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from publications.admin import BaseModelMixin
from publications.models import Publication


class PublicationAdmin(BaseModelMixin, SimpleHistoryAdmin):
    readonly_fields = (
        "owner",
        "metadata",
    )


admin.site.register(Publication, PublicationAdmin)
