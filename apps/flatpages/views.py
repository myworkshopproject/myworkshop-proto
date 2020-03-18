from django.views.generic.detail import DetailView
from flatpages.models import FlatPage


class FlatPageView(DetailView):

    model = FlatPage

    def get_template_names(self):
        if self.object.template == self.object.FULL_WIDTH:
            return "core/flatpage.html"
        if self.object.template == self.object.FULL_PAGE:
            return "core/flatpage.html"
        return "core/flatpage.html"
