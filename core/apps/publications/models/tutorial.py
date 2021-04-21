from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from simple_history.models import HistoricalRecords
from publications.models import Publication


class Tutorial(Publication):
    history = HistoricalRecords()

    @property
    def icon(self):
        return settings.PUBLICATIONS_TUTORIAL_ICON

    @property
    def difficulty(self):
        if "difficulty" in self.metadata:
            difficulty = self.metadata["difficulty"][0]
            if difficulty.isdigit():
                return max(min(int(difficulty), 3), 1)
        return None

    @property
    def duration(self):
        if "duration" in self.metadata:
            duration = self.metadata["duration"][0]
            if duration:
                return duration
        return None

    @property
    def cost(self):
        if "cost" in self.metadata:
            cost = self.metadata["cost"][0]
            if cost:
                return cost
        return None

    class Meta:
        verbose_name = _("tutorial")
        verbose_name_plural = _("tutorials")

    def get_update_url(self):
        return reverse("publications:tutorial-update", args=[str(self.id)])
