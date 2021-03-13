from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "publications/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = {
            "title": _("Publications"),
            "description": _("Publications app main page."),
        }
        return context
