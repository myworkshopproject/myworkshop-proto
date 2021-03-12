from django.urls import path
from flatpages import views

app_name = "flatpages"


urlpatterns = [path("<slug:slug>/", views.FlatPageView.as_view(), name="page-detail")]
