from itertools import chain
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext, gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, redirect
from allauth.account.decorators import verified_email_required
from accounts.models import CustomUser
from core.models import Image, Link, Note, Project, Publication


class CustomUserDetailView(DetailView):
    model = CustomUser
    context_object_name = "user"
    template_name = "accounts/user_detail.html"


class CustomUserListView(ListView):
    model = CustomUser
    template_name = "core/user_list.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = super().get_queryset()
            return queryset.exclude(username="deleted").exclude(username="admin")
        else:
            return CustomUser.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = {
            "title": _("Users"),
            "fontawesome5_class": "fas fa-users",
            "short_description": _("All users"),
        }
        return context


class CustomUserLabbookView(ListView):
    template_name = "core/labbook.html"

    def get_queryset(self):
        user = get_object_or_404(CustomUser, pk=self.kwargs["pk"])
        image_list = Image.objects.filter(owner=user)
        link_list = Link.objects.filter(owner=user)
        note_list = Note.objects.filter(owner=user)
        result_list = sorted(
            chain(image_list, link_list, note_list),
            key=lambda instance: instance.changed_at,
            reverse=True,
        )
        return result_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = {
            "title": _("My laboratory notebook"),
            "fontawesome5_class": "fas fa-book",
            "short_description": _("My laboratory notebook"),
        }
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=kwargs["pk"])
        if request.user != user:
            return redirect(request.user.get_labbook_url())
        return super().dispatch(request, *args, **kwargs)


class CustomUserImageListView(ListView):
    model = Image
    template_name = "core/image_list.html"

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
            context["object"] = {
                "title": _("My images"),
                "fontawesome5_class": "far fa-images",
                "short_description": _("My images"),
            }
        else:
            context["object"] = {
                "title": _("{}'s images").format(user.get_full_name()),
                "fontawesome5_class": "far fa-images",
                "short_description": _("{}'s images").format(user.get_full_name()),
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
            context["object"] = {
                "title": _("My projects"),
                "fontawesome5_class": "fas fa-cogs",
                "short_description": _("My projects"),
            }
        else:
            context["object"] = {
                "title": _("{}'s projects").format(user.get_full_name()),
                "fontawesome5_class": "fas fa-cogs",
                "short_description": _("{}'s projects").format(user.get_full_name()),
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
            context["object"] = {
                "title": _("My publications"),
                "fontawesome5_class": "fas fa-feather-alt",
                "short_description": _("My publications"),
            }
        else:
            context["object"] = {
                "title": _("{}'s publications").format(user.get_full_name()),
                "fontawesome5_class": "fas fa-feather-alt",
                "short_description": _("{}'s publications").format(
                    user.get_full_name()
                ),
            }
        return context
