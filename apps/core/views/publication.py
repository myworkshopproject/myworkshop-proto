from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext, gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from core.models import PublicationType, Publication


class PublicationDetailView(DetailView):
    model = Publication
    template_name = "core/publication_detail.html"


class PublicationListByTypeView(ListView):
    template_name = "core/object_list.html"

    def get_queryset(self):
        self.type = get_object_or_404(PublicationType, slug=self.kwargs["type"])
        if self.request.user.is_authenticated:
            return Publication.members_objects.filter(type=self.type)
        else:
            return Publication.public_objects.filter(type=self.type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = PublicationType.objects.get(slug=self.kwargs["type"])
        return context


class PublicationListView(ListView):
    model = Publication
    template_name = "core/object_list.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Publication.members_objects.all()
        else:
            return Publication.public_objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = {
            "title": _("All publications"),
            "short_description": _("All publications"),
        }
        return context


class PublicationCreateView(LoginRequiredMixin, CreateView):
    model = Publication
    fields = [
        # "type",
        # "status",
        # "visibility",
        "title",
        "short_description",
        # "featured_image",
        "license",
        "tags",
        # "slug",
        # "body",
    ]
    template_name = "core/forms/object_create.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.type = self.publication_type
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        type = get_object_or_404(PublicationType, slug=kwargs["slug"])
        self.publication_type = type
        return super().dispatch(request, *args, **kwargs)


class PublicationUpdateView(UpdateView):
    model = Publication
    fields = [
        # "type",
        "status",
        # "visibility",
        "title",
        "slug",
        "short_description",
        "featured_image",
        "license",
        "tags",
        # "body",
    ]
    template_name = "core/forms/object_update.html"

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if request.user != object.owner:
            return redirect("core:home")
        return super().dispatch(request, *args, **kwargs)


class PublicationUpdateMetaView(UpdateView):
    model = Publication
    fields = ["meta"]
    template_name = "core/forms/object_update_meta.html"

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if request.user != object.owner:
            return redirect("core:home")
        return super().dispatch(request, *args, **kwargs)


class PublicationUpdateBodyView(UpdateView):
    model = Publication
    fields = ["body"]
    template_name = "core/forms/object_update_body.html"

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if request.user != object.owner:
            return redirect("core:home")
        return super().dispatch(request, *args, **kwargs)
