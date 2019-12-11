from django.contrib import admin
from projects.models import Project, Part


class ProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)


class PartAdmin(admin.ModelAdmin):
    pass


admin.site.register(Part, PartAdmin)
