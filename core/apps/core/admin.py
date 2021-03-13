from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import ugettext, ugettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from simple_history.admin import SimpleHistoryAdmin
from core.models import BaseModel, SiteCustomization


class BaseModelMixin(object):
    def get_fieldsets(self, request, obj=None):
        fieldsets_base = (
            (
                _("generic fields"),
                {
                    "classes": ("collapse",),
                    "fields": (
                        "id",
                        "created_at",
                        "created_by",
                        "changed_at",
                        "changed_by",
                    ),
                },
            ),
            (
                _("common editable fields"),
                {
                    "fields": (
                        "owner",
                        "metadata",
                    ),
                },
            ),
        )
        if self.fields:
            return fieldsets_base + ((_("specific fields"), {"fields": self.fields}),)
        return fieldsets_base

    def get_readonly_fields(self, request, obj=None):
        readonly_fields_base = (
            "id",
            "created_at",
            "created_by",
            "changed_at",
            "changed_by",
        )

        if obj:
            return self.readonly_fields + readonly_fields_base
        else:
            return self.readonly_fields + readonly_fields_base + ("owner",)

    def get_list_display(self, request):
        list_display_base = (
            "created_at",
            "created_by",
            "changed_at",
            "changed_by",
        )
        return self.list_display + list_display_base

    def get_search_fields(self, request):
        return self.search_fields + ("id",)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        """Méthode appellée lorsqu'un objet est créé via un formulaire inline"""

        for formset in formsets:

            if issubclass(formset.model, BaseModel):
                instances = formset.save(commit=False)

                for added_obj in formset.new_objects:
                    added_obj.owner = request.user

                for deleted_obj in formset.deleted_objects:
                    pass

        super(BaseModelMixin, self).save_related(request, form, formsets, change)


class SiteAdmin(SimpleHistoryAdmin):
    pass


admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)


class SiteCustomizationAdmin(TranslationAdmin, SimpleHistoryAdmin):
    pass


admin.site.register(SiteCustomization, SiteCustomizationAdmin)
