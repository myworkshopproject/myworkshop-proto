# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect

# from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from core.models import Image, ProjectType, Project, ProjectContributor


class ProjectDetailView(DetailView):
    model = Project
    template_name = "core/project_detail.html"


class ProjectListByTypeView(ListView):
    template_name = "core/object_list.html"

    def get_queryset(self):
        self.type = get_object_or_404(ProjectType, slug=self.kwargs["type"])
        if self.request.user.is_authenticated:
            return Project.members_objects.filter(type=self.type)
        else:
            return Project.public_objects.filter(type=self.type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = ProjectType.objects.get(slug=self.kwargs["type"])
        return context


class ProjectListView(ListView):
    model = Project
    template_name = "core/object_list.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Project.members_objects.all()
        else:
            return Project.public_objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = {
            "title": _("All projects"),
            "fontawesome5_class": "fas fa-cogs",
            "short_description": _("All projects"),
        }
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
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
        # "contributors",
        # "publications",
    ]
    template_name = "core/forms/object_create.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.type = self.project_type
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        type = get_object_or_404(ProjectType, slug=kwargs["slug"])
        self.project_type = type
        return super().dispatch(request, *args, **kwargs)


class ProjectUpdateView(UpdateView):
    model = Project
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
        # "contributors",
        # "publications",
    ]
    template_name = "core/forms/object_update.html"

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        # allow OWNERS only to access this view
        if not project.is_owner(request.user):
            return redirect(project.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)


class ProjectPublicationsUpdateView(UpdateView):
    model = Project
    fields = ["publications"]
    template_name = "core/forms/object_update.html"

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        # allow only OWNERS and EDITORS to access this view
        if not project.is_owner_or_editor(request.user):
            return redirect(project.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)


class ProjectContributorCreateView(LoginRequiredMixin, CreateView):
    model = ProjectContributor
    fields = ["contributor", "role"]
    template_name = "core/forms/object_create.html"

    def form_valid(self, form):
        if not ProjectContributor.objects.filter(
            project=self.project, contributor=form.instance.contributor
        ).exists():
            form.instance.project = self.project
            return super().form_valid(form)
        else:
            form.add_error(None, _("this user is already a contributor to the project"))
            return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs["slug"])
        self.project = project
        # allow OWNERS only to access this view
        if not project.is_owner(request.user):
            return redirect(project.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)


class ProjectContributorUpdateView(UpdateView):
    model = ProjectContributor
    fields = ["role"]

    template_name = "core/forms/object_update.html"

    def dispatch(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs["slug"])
        self.project = project
        # allow OWNERS only to access this view
        if not project.is_owner(request.user):
            return redirect(project.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)


class ProjectContributorDeleteView(DeleteView):
    model = ProjectContributor

    def get_success_url(self):
        return self.object.project.get_absolute_url()

    # Django DeleteView without confirmation template:
    # DeleteView responds to POST and GET requests,
    # GET request display confirmation template,
    # while POST deletes instance.
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
