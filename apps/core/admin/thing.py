from django.contrib import admin
from core.models import Thing, ThingMaker


class ThingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Thing, ThingAdmin)


class ThingMakerAdmin(admin.ModelAdmin):
    pass


admin.site.register(ThingMaker, ThingMakerAdmin)
