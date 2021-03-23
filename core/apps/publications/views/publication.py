from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from publications.models import Publication


class PublicationListView(ListView):
    model = Publication

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = {
            "title": _("Publications"),
            "description": _("Publications list."),
            "icon": "fas fa-feather-alt",
        }
        return context


class PublicationDetailView(DetailView):
    model = Publication

    def dispatch(self, *args, **kwargs):
        slug = slugify(self.get_object().title)

        if "slug" in kwargs:
            if slug == kwargs["slug"]:
                return super().dispatch(*args, **kwargs)

        kwargs["slug"] = slug
        return redirect("publications:publication-detail", permanent=True, **kwargs)


class PublicationCreateView(LoginRequiredMixin, CreateView):
    model = Publication
    fields = ["source"]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = {
            "title": _("New publication"),
            "description": _("Create your own awesome publication!"),
            "icon": "fas fa-feather-alt",
            "get_cancel_url": reverse_lazy("publications:publication-list"),
        }
        return context

    def get_success_url(self):
        if "continue" in self.request.POST:
            return self.object.get_update_url()
        return self.object.get_absolute_url()


class PublicationUpdateView(LoginRequiredMixin, UpdateView):
    model = Publication
    fields = ["source"]

    def get_success_url(self):
        if "continue" in self.request.POST:
            return self.object.get_update_url()
        return self.object.get_absolute_url()


class PublicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Publication

    success_url = reverse_lazy("publications:publication-list")
