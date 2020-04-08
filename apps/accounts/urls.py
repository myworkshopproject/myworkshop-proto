from django.conf import settings
from django.urls import path, include
from django.views.generic.base import RedirectView
from accounts import views

app_name = "accounts"


urlpatterns = [
    path("", views.CustomUserListView.as_view(), name="user-list"),
    path("<str:pk>/", views.CustomUserDetailView.as_view(), name="user-detail"),
    path("<str:pk>/update/", views.CustomUserUpdateView.as_view(), name="user-update"),
    path(
        "<str:pk>/labbook/", views.CustomUserLabbookView.as_view(), name="user-labbook"
    ),
    path(
        "<str:pk>/images/",
        views.CustomUserImageListView.as_view(),
        name="user-image-list",
    ),
    path(
        "<str:pk>/projects/",
        views.CustomUserProjectListView.as_view(),
        name="user-project-list",
    ),
    path(
        "<str:pk>/publications/",
        views.CustomUserPublicationListView.as_view(),
        name="user-publication-list",
    ),
]
