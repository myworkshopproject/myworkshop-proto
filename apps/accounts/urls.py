from django.conf import settings
from django.urls import path, include
from django.views.generic.base import RedirectView
from accounts import views

app_name = "accounts"


urlpatterns = [
    path("", views.CustomUserListView.as_view(), name="user-list"),
    path("<str:pk>/", views.CustomUserDetailView.as_view(), name="user-detail"),
]
