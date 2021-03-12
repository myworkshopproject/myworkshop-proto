from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView
from core.models import Link


class LinkCreateView(LoginRequiredMixin, CreateView):
    model = Link
    fields = ["url"]
    template_name = "core/forms/object_create.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class LinkUpdateView(LoginRequiredMixin, UpdateView):
    model = Link
    fields = ["title", "url", "tags"]
    template_name = "core/forms/link_update.html"
