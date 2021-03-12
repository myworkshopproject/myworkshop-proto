from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("pages/", include("flatpages.urls")),
    path("users/", include("accounts.urls")),
    path("", include("core.urls")),
]


if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
