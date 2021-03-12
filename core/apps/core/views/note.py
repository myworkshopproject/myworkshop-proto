from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView
from core.models import Note


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ["title", "tags", "short_description"]
    template_name = "core/forms/object_create.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class NoteUpdateView(UpdateView):
    model = Note
    fields = ["title", "tags", "short_description"]
    template_name = "core/forms/object_update.html"
