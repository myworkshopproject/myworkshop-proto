from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from simple_history.models import HistoricalRecords
from publications.models import Publication


class Article(Publication):
    history = HistoricalRecords()

    @property
    def icon(self):
        return settings.PUBLICATIONS_ARTICLE_ICON

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("articles")

    def get_update_url(self):
        return reverse("publications:article-update", args=[str(self.id)])
