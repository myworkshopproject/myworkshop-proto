from django.urls import path, re_path
from publications import views


app_name = "publications"

# https://stackoverflow.com/questions/14351048/django-optional-url-parameters
# https://stackoverflow.com/questions/2325433/making-a-regex-django-url-token-optional
REGEX = r"(?P<pk>[\w]+)/(?:(?P<slug>[\w-]+)/)?"

urlpatterns = [
    path(
        "create/article/",
        views.ArticleCreateView.as_view(),
        name="article-create",
    ),
    path(
        "update/article/<str:pk>/",
        views.ArticleUpdateView.as_view(),
        name="article-update",
    ),
    path(
        "create/tutorial/",
        views.TutorialCreateView.as_view(),
        name="tutorial-create",
    ),
    path(
        "update/tutorial/<str:pk>/",
        views.TutorialUpdateView.as_view(),
        name="tutorial-update",
    ),
    path(
        "create/image/",
        views.ImageCreateView.as_view(),
        name="image-create",
    ),
    path(
        "update/image/<str:pk>/",
        views.ImageUpdateView.as_view(),
        name="image-update",
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
