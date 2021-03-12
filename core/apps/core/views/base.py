from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = "core/index.html"
