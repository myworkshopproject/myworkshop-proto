from django.conf import settings
from django.urls import path, include
from django.views.generic.base import RedirectView
from core import views

app_name = "core"


favicon_view = RedirectView.as_view(
    url=settings.STATIC_URL + "core/img/favicon.ico", permanent=True
)

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("favicon.ico", favicon_view, name="favicon"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("images/", views.ImageListView.as_view(), name="image-list"),
    path("images/create/", views.ImageCreateView.as_view(), name="image-create"),
    path("images/<uuid:pk>/", views.ImageDetailView.as_view(), name="image-detail"),
    path(
        "images/<uuid:pk>/update/", views.ImageUpdateView.as_view(), name="image-update"
    ),
    path(
        "images/<uuid:pk>/thumbnail/",
        views.ImageThumbnailView.as_view(),
        name="image-thumbnail",
    ),
    # path("labbook/", views.LabbookView.as_view(), name="labbook"),
    path(
        "publications/create/<slug:slug>/",
        views.PublicationCreateView.as_view(),
        name="publication-create",
    ),
    path(
        "publications/<slug:slug>/",
        views.PublicationDetailView.as_view(),
        name="publication-detail",
    ),
    path(
        "publications/<slug:slug>/update/",
        views.PublicationUpdateView.as_view(),
        name="publication-update",
    ),
    path(
        "publications/<slug:slug>/update-meta/",
        views.PublicationUpdateMetaView.as_view(),
        name="publication-update-meta",
    ),
    path(
        "publications/<slug:slug>/update-body/",
        views.PublicationUpdateBodyView.as_view(),
        name="publication-update-body",
    ),
    path("publications/", views.PublicationListView.as_view(), name="publication-list"),
    path(
        "publications-by-type/<slug:type>/",
        views.PublicationListByTypeView.as_view(),
        name="publication-list-by-type",
    ),
    path(
        "projects/create/<slug:slug>/",
        views.ProjectCreateView.as_view(),
        name="project-create",
    ),
    path(
        "projects/<slug:slug>/",
        views.ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path(
        "projects/<slug:slug>/update/",
        views.ProjectUpdateView.as_view(),
        name="project-update",
    ),
    path(
        "projects/<slug:slug>/contributors/create/",
        views.ProjectContributorCreateView.as_view(),
        name="project-contributor-create",
    ),
    path(
        "projects/<slug:slug>/contributors/update/<uuid:pk>/",
        views.ProjectContributorUpdateView.as_view(),
        name="project-contributor-update",
    ),
    path(
        "projects/<slug:slug>/contributors/delete/<uuid:pk>/",
        views.ProjectContributorDeleteView.as_view(),
        name="project-contributor-delete",
    ),
    path(
        "projects/<slug:slug>/publications/update/",
        views.ProjectPublicationsUpdateView.as_view(),
        name="project-publications-update",
    ),
    path("projects/", views.ProjectListView.as_view(), name="project-list"),
    path(
        "projects-by-type/<slug:type>/",
        views.ProjectListByTypeView.as_view(),
        name="project-list-by-type",
    ),
]
