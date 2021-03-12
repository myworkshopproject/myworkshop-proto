from django.contrib import admin
from core.models import Workshop
from modeltranslation.admin import TranslationAdmin
from simple_history.admin import SimpleHistoryAdmin


class WorkshopAdmin(TranslationAdmin, SimpleHistoryAdmin):
    pass


admin.site.register(Workshop, WorkshopAdmin)
