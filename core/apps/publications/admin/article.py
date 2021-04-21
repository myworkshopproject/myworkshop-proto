from django import forms
from django.conf import settings
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from publications.admin import BaseModelMixin
from publications.models import Article


class ArticleAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleAdminForm, self).__init__(*args, **kwargs)

        if "source" in self.fields:
            self.fields["source"].initial = settings.DEFAULT_ARTICLE_SOURCE_TEXT


class ArticleAdmin(BaseModelMixin, SimpleHistoryAdmin):
    form = ArticleAdminForm

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


admin.site.register(Article, ArticleAdmin)
