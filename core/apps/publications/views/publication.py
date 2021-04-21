from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from publications.models import Article, Image, Publication, Tutorial


def get_item_list(items, name, current, base_url, extra=None):
    output = []
    for key, value in items.items():
        output.append(
            {
                "url": (
                    "{}?{}={}{}".format(base_url, name, key, extra if extra else "")
                ),
                "icon": value["icon"],
                "text": value["text"],
                "active": (current == key),
            }
        )
    return output


class PublicationListView(ListView):
    template_name = "publications/publication_list.html"

    paginate_by = 5

    types = {
        "article": {
            "text": _("Articles"),
            "icon": settings.PUBLICATIONS_ARTICLE_ICON,
        },
        "tutorial": {
            "text": _("Tutorials"),
            "icon": settings.PUBLICATIONS_TUTORIAL_ICON,
        },
        "image": {
            "text": _("Images"),
            "icon": settings.PUBLICATIONS_IMAGE_ICON,
        },
        "all": {
            "text": _("All publications"),
            "icon": settings.PUBLICATIONS_PUBLICATIONS_ICON,
        },
    }
    default_type = "all"

    sorts = {
        "-changed_at": {
            "text": _("Newest"),
            "icon": "far fa-clock",
        },
        "changed_at": {
            "text": _("Oldest"),
            "icon": "fas fa-history",
        },
    }
    default_sort = "-changed_at"

    def get_queryset(self):
        type = self.default_type
        if "type" in self.request.GET:
            if self.request.GET["type"] in self.types:
                type = self.request.GET["type"]

        sort = self.default_sort
        if "sort" in self.request.GET:
            if self.request.GET["sort"] in self.sorts:
                sort = self.request.GET["sort"]

        if type == "article":
            queryset = Article.objects.all()
        elif type == "tutorial":
            queryset = Tutorial.objects.all()
        elif type == "image":
            queryset = Image.objects.all()
        else:
            queryset = Publication.objects.all().select_subclasses()

        return queryset.order_by(sort)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        type = self.default_type
        if "type" in self.request.GET:
            if self.request.GET["type"] in self.types:
                type = self.request.GET["type"]

        sort = self.default_sort
        if "sort" in self.request.GET:
            if self.request.GET["sort"] in self.sorts:
                sort = self.request.GET["sort"]

        context["object"] = {
            "title": _("Publications"),
            "description": _("Publications list."),
            "menus": [
                {
                    "title": _("Filter"),
                    "icon": "fas fa-filter",
                    "items": get_item_list(
                        items=self.types,
                        name="type",
                        current=type,
                        base_url=reverse_lazy("publications:publication-list"),
                        extra="&sort={}".format(sort),
                    ),
                },
                {
                    "title": _("Sort"),
                    "icon": "fas fa-sort-amount-down-alt",
                    "items": get_item_list(
                        items=self.sorts,
                        name="sort",
                        current=sort,
                        base_url=reverse_lazy("publications:publication-list"),
                        extra="&type={}".format(type),
                    ),
                },
            ],
        }
        return context


class PublicationDetailView(DetailView):
    template_name = "publications/publication_detail.html"

    def get_queryset(self):
        return Publication.objects.all().select_subclasses()

    def dispatch(self, *args, **kwargs):
        slug = slugify(self.get_object().title)

        if "slug" in kwargs:
            if slug == kwargs["slug"]:
                return super().dispatch(*args, **kwargs)

        kwargs["slug"] = slug
        return redirect("publications:publication-detail", permanent=True, **kwargs)


class PublicationCreateView(LoginRequiredMixin, CreateView):
    model = Publication
    template_name = "publications/publication_form.html"
    fields = ["source"]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        if "continue" in self.request.POST:
            return self.object.get_update_url()
        return self.object.get_absolute_url()


class ArticleCreateView(PublicationCreateView):
    model = Article
    fields = ["source"]

    initial = {
        "source": "title: {title}\ndescription: {description}\n\n{text}\n".format(
            title=settings.PUBLICATIONS_DEFAULT_ARTICLE_TITLE,
            description=settings.PUBLICATIONS_DEFAULT_ARTICLE_DESCRIPTION,
            text=settings.PUBLICATIONS_DEFAULT_ARTICLE_TEXT,
        )
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = {
            "title": settings.PUBLICATIONS_DEFAULT_ARTICLE_TITLE,
            "description": settings.PUBLICATIONS_DEFAULT_ARTICLE_DESCRIPTION,
            "icon": settings.PUBLICATIONS_ARTICLE_ICON,
            "get_cancel_url": reverse_lazy("publications:publication-list"),
        }
        return context


class TutorialCreateView(PublicationCreateView):
    model = Tutorial
    fields = ["source"]

    initial = {
        "source": "title: {title}\ndescription: {description}\ndifficulty: {difficulty}\nduration: {duration}\ncost: {cost}\n\n{text}\n".format(
            title=settings.PUBLICATIONS_DEFAULT_TUTORIAL_TITLE,
            description=settings.PUBLICATIONS_DEFAULT_TUTORIAL_DESCRIPTION,
            difficulty=settings.PUBLICATIONS_DEFAULT_TUTORIAL_DIFFICULTY,
            duration=settings.PUBLICATIONS_DEFAULT_TUTORIAL_DURATION,
            cost=settings.PUBLICATIONS_DEFAULT_TUTORIAL_COST,
            text=settings.PUBLICATIONS_DEFAULT_TUTORIAL_TEXT,
        )
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = {
            "title": settings.PUBLICATIONS_DEFAULT_TUTORIAL_TITLE,
            "description": settings.PUBLICATIONS_DEFAULT_TUTORIAL_DESCRIPTION,
            "icon": settings.PUBLICATIONS_TUTORIAL_ICON,
            "get_cancel_url": reverse_lazy("publications:publication-list"),
            "difficulty": settings.PUBLICATIONS_DEFAULT_TUTORIAL_DIFFICULTY,
            "duration": settings.PUBLICATIONS_DEFAULT_TUTORIAL_DURATION,
            "cost": settings.PUBLICATIONS_DEFAULT_TUTORIAL_COST,
        }
        return context


class ImageCreateView(PublicationCreateView):
    model = Image
    fields = [
        "picture",
        "source",
    ]

    initial = {
        "source": """title: {title}
description: {description}
""".format(
            title=settings.PUBLICATIONS_DEFAULT_IMAGE_TITLE,
            description=settings.PUBLICATIONS_DEFAULT_IMAGE_DESCRIPTION,
        )
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = {
            "title": settings.PUBLICATIONS_DEFAULT_IMAGE_TITLE,
            "description": settings.PUBLICATIONS_DEFAULT_IMAGE_DESCRIPTION,
            "icon": settings.PUBLICATIONS_IMAGE_ICON,
            "get_cancel_url": reverse_lazy("publications:publication-list"),
        }
        return context


class PublicationUpdateView(LoginRequiredMixin, UpdateView):
    model = Publication
    template_name = "publications/publication_form.html"
    fields = ["source"]

    def get_success_url(self):
        if "continue" in self.request.POST:
            return self.object.get_update_url()
        return self.object.get_absolute_url()


class ArticleUpdateView(PublicationUpdateView):
    model = Article
    fields = ["source"]


class TutorialUpdateView(PublicationUpdateView):
    model = Tutorial
    fields = ["source"]


class ImageUpdateView(PublicationUpdateView):
    model = Image
    fields = [
        "picture",
        "source",
    ]


class PublicationDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "publications/publication_confirm_delete.html"

    def get_queryset(self):
        return Publication.objects.all().select_subclasses()

    success_url = reverse_lazy("publications:publication-list")
