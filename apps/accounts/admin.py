from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _
from allauth.account.models import EmailAddress
from accounts.models import CustomUser


class EmailAddressInline(admin.TabularInline):
    model = EmailAddress
    extra = 0


class CustomUserAdmin(UserAdmin):
    # see https://github.com/django/django/blob/master/django/contrib/auth/admin.py
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            _("Optional"),
            {
                "fields": (
                    "photo",
                    "short_description",
                    "tags",
                    "facebook_username",
                    "github_username",
                    "instagram_username",
                    "linkedin_public_url",
                    "twitter_username",
                    "youtube_channel_url",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "has_verified_emailaddress",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    inlines = [EmailAddressInline]


admin.site.register(CustomUser, CustomUserAdmin)
