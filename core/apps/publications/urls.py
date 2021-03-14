from django.urls import path, re_path
from publications import views


app_name = "publications"

# https://stackoverflow.com/questions/14351048/django-optional-url-parameters
# https://stackoverflow.com/questions/2325433/making-a-regex-django-url-token-optional
REGEX = r"(?P<pk>[\w]+)/(?:(?P<slug>[\w-]+)/)?"

urlpatterns = [
    path(
        "create/",
        views.PublicationCreateView.as_view(),
        name="publication-create",
    ),
    path(
        "update/<str:pk>/",
        views.PublicationUpdateView.as_view(),
        name="publication-update",
    ),
    path(
        "delete/<str:pk>/",
        views.PublicationDeleteView.as_view(),
        name="publication-delete",
    ),
    path(
        "",
        views.PublicationListView.as_view(),
        name="publication-list",
    ),
    re_path(
        r"^{}".format(REGEX),
        views.PublicationDetailView.as_view(),
        name="publication-detail",
    ),
]
