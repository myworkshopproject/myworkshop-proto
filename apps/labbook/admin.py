from django.contrib import admin
from labbook.models import Entry, Note


class EntryAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Entry, EntryAdmin)


class NoteAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Note, NoteAdmin)
