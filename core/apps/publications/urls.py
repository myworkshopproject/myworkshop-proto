from django.urls import path
from publications import views


app_name = "publications"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
]
