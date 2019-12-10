from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path


urlpatterns = [
    path("", include("core.urls")),
    url(r"^accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
]
