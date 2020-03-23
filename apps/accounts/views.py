from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from allauth.account.decorators import verified_email_required
from accounts.models import CustomUser
from django.utils.translation import gettext, gettext_lazy as _
from core.models import Image, Project, Publication


class CustomUserDetailView(DetailView):
    model = CustomUser
    context_object_name = "user"
    template_name = "accounts/user_detail.html"


class CustomUserListView(ListView):
    model = CustomUser
    context_object_name = "user_list"
    template_name = "core/object_list.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = super().get_queryset()
            return queryset.exclude(username="deleted").exclude(username="admin")
        else:
            return CustomUser.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = {
            "title": _("Users"),
            "fontawesome5_class": "fas fa-users",
            "short_description": _("All users"),
        }
        return context


class CustomUserImageListView(ListView):
    model = Image
    template_name = "core/object_list.html"

    def get_queryset(self):
        user = get_object_or_404(CustomUser, pk=self.kwargs["pk"])
        if self.request.user.is_authenticated:
            if self.request.user == user:
                return Image.objects.filter(owner=user)
            else:
                return Image.members_objects.filter(owner=user)
        else:
            return Image.public_objects.filter(owner=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, pk=self.kwargs["pk"])
        if self.request.user == user:
            context["type"] = {
                "title": _("My images"),
                "short_description": _("My images"),
            }
        else:
            context["type"] = {
                "title": _("All images"),
                "short_description": _("All images"),
            }
        return context


class CustomUserProjectListView(ListView):
    model = Project
    template_name = "core/object_list.html"

    def get_queryset(self):
        user = get_object_or_404(CustomUser, pk=self.kwargs["pk"])
        if self.request.user.is_authenticated:
            if self.request.user == user:
                return Project.objects.filter(contributors=user)
            else:
                return Project.members_objects.filter(contributors=user)
        else:
            return Project.public_objects.filter(contributors=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, pk=self.kwargs["pk"])
        if self.request.user == user:
            context["type"] = {
                "title": _("My projects"),
                "short_description": _("My projects"),
            }
        else:
            context["type"] = {
                "title": _("All projects"),
                "short_description": _("All projects"),
            }
        return context


class CustomUserPublicationListView(ListView):
    model = Publication
    template_name = "core/object_list.html"

    def get_queryset(self):
        user = get_object_or_404(CustomUser, pk=self.kwargs["pk"])
        if self.request.user.is_authenticated:
            if self.request.user == user:
                return Publication.objects.filter(owner=user)
            else:
                return Publication.members_objects.filter(owner=user)
        else:
            return Publication.public_objects.filter(owner=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, pk=self.kwargs["pk"])
        if self.request.user == user:
            context["type"] = {
                "title": _("My publications"),
                "short_description": _("My publications"),
            }
        else:
            context["type"] = {
                "title": _("All publications"),
                "short_description": _("All publications"),
            }
        return context
