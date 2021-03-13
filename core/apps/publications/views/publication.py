from django.shortcuts import redirect
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from publications.models import Publication


class PublicationListView(ListView):
    model = Publication

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = {
            "title": _("Publications"),
            "description": _("Publications list."),
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
