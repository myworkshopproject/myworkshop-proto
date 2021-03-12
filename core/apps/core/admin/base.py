from django.utils.translation import ugettext, ugettext_lazy as _


class BaseAdminMixin(object):
    def __init__(self, *args, **kwargs):
        super(BaseAdminMixin, self).__init__(*args, **kwargs)

        readonly_fields = ["id", "owner"]
        for field in readonly_fields:
            self.readonly_fields.append(field)

        fieldset = (None, {"fields": ("id",)})
        self.fieldsets.insert(0, fieldset)

        fieldset = (
            _("Base model"),
            {
                "fields": (
                    "title",
                    "short_description",
                    "featured_image",
                    "license",
                    "tags",
                )
            },
        )
        self.fieldsets.insert(1, fieldset)


class LogAdminMixin(object):
    def __init__(self, *args, **kwargs):
        super(LogAdminMixin, self).__init__(*args, **kwargs)

        readonly_fields = ["created_at", "created_by", "changed_at", "changed_by"]
        for field in readonly_fields:
            self.readonly_fields.append(field)

        fieldsets = (
            _("Log model"),
            {"fields": ("created_at", "created_by", "changed_at", "changed_by")},
        )
        self.fieldsets.append(fieldsets)


class SaveOwnerModelMixin(object):
    def save_model(self, request, obj, form, change):
        if not change:
            # Only set added_by during the first save.
            obj.owner = request.user
        super().save_model(request, obj, form, change)


class SlugAdminMixin(object):
    # prepopulated_fields = {"slug": ("title",)} # do not work with modeltranslation

    def __init__(self, *args, **kwargs):
        super(SlugAdminMixin, self).__init__(*args, **kwargs)

        fieldset = (_("Slug model"), {"fields": ("slug",)})
        self.fieldsets.append(fieldset)
