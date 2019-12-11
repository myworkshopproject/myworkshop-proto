from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("", include("core.urls")),
    url(r"^accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
]


if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
